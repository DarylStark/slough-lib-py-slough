"""Tests for the DevContainer model."""

import pytest

from dev_container_gen.model import DevContainer


def test_adding_docker_mount() -> None:
    """Test adding a Docker mount to the DevContainer configuration."""
    # Create a DevContainer instance
    dev_container = DevContainer(name='test', image='test_image')

    # Add the Docker mount
    dev_container.add_docker_mount()

    # Check if the mount was added correctly
    assert (
        'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind'
        in dev_container.mounts
    )


@pytest.mark.parametrize(
    'mount',
    [
        'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind',
        'source=/another/path,target=/another/path,type=bind',
    ],
)
def test_adding_custom_mount(mount: str) -> None:
    """Test adding a custom mount to the DevContainer configuration.

    Args:
        mount (str): The custom mount to add.
    """
    # Create a DevContainer instance
    dev_container = DevContainer(name='test', image='test_image')
    dev_container.add_mount(mount)

    # Check if the custom mount was added correctly
    assert mount in dev_container.mounts


@pytest.mark.parametrize(
    'mount',
    [
        'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind',
        'source=/another/path,target=/another/path,type=bind',
    ],
)
def test_adding_custom_mount_twice(mount: str) -> None:
    """Test adding a custom mount to the DevContainer configuration twice.

    It should only be in there one time.

    Args:
        mount (str): The custom mount to add.
    """
    # Create a DevContainer instance
    dev_container = DevContainer(name='test', image='test_image')
    dev_container.add_mount(mount)
    dev_container.add_mount(mount)

    # Check if the custom mount was added correctly
    assert dev_container.mounts.count(mount) == 1


def test_adding_environment_variable() -> None:
    """Test adding an environment variable."""
    # Create a DevContainer instance
    dev_container = DevContainer(name='test', image='test_image')

    # Add an environment variable
    dev_container.add_environment_variable('TEST_VAR', 'test_value')

    # Check if the environment variable was added correctly
    assert dev_container.remote_environment['TEST_VAR'] == 'test_value'


def test_overwriting_environment_variable() -> None:
    """Test overwriting an existing environment variable."""
    # Create a DevContainer instance
    dev_container = DevContainer(name='test', image='test_image')

    # Add an environment variable
    dev_container.add_environment_variable('TEST_VAR', 'initial_value')

    # Overwrite the environment variable
    dev_container.add_environment_variable('TEST_VAR', 'new_value')

    # Check if the environment variable was updated correctly
    assert dev_container.remote_environment['TEST_VAR'] == 'new_value'
