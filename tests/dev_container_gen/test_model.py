"""Tests for the DevContainer model."""

import pytest

from dev_container_gen import DevContainer


def test_adding_docker_mount(dev_container_model: DevContainer) -> None:
    """Test adding a Docker mount to the DevContainer configuration.

    Args:
        dev_container_model (DevContainer): The DevContainer instance.
    """
    # Add the Docker mount
    dev_container_model.add_docker_mount()

    # Check if the mount was added correctly
    assert (
        'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind'
        in dev_container_model.mounts
    )


def test_removing_docker_mount(dev_container_model: DevContainer) -> None:
    """Test removing a Docker mount from the DevContainer configuration.

    Args:
        dev_container_model (DevContainer): The DevContainer instance.
    """
    # Add the Docker mount
    dev_container_model.add_docker_mount()

    # Remove the Docker mount
    dev_container_model.remove_docker_mount()

    # Check if the mount was added correctly
    assert (
        'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind'
        not in dev_container_model.mounts
    )


def test_removing_docker_mount_when_it_wasnt_there(
    dev_container_model: DevContainer,
) -> None:
    """Test removing a Docker mount from the DevContainer configuration.

    Test it on a model that doesn't have it.

    Args:
        dev_container_model (DevContainer): The DevContainer instance.
    """
    # Remove the Docker mount
    dev_container_model.remove_docker_mount()

    # Check if the mount was added correctly
    assert (
        'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind'
        not in dev_container_model.mounts
    )


@pytest.mark.parametrize(
    'mount',
    [
        'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind',
        'source=/another/path,target=/another/path,type=bind',
    ],
)
def test_adding_custom_mount(
    mount: str, dev_container_model: DevContainer
) -> None:
    """Test adding a custom mount to the DevContainer configuration.

    Args:
        mount (str): The custom mount to add.
        dev_container_model (DevContainer): The DevContainer instance.
    """
    # Create a DevContainer instance
    dev_container_model.add_mount(mount)

    # Check if the custom mount was added correctly
    assert mount in dev_container_model.mounts


@pytest.mark.parametrize(
    'mount',
    [
        'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind',
        'source=/another/path,target=/another/path,type=bind',
    ],
)
def test_adding_custom_mount_twice(
    mount: str, dev_container_model: DevContainer
) -> None:
    """Test adding a custom mount to the DevContainer configuration twice.

    It should only be in there one time.

    Args:
        mount (str): The custom mount to add.
        dev_container_model (DevContainer): The DevContainer instance.
    """
    # Create a DevContainer instance
    dev_container_model.add_mount(mount)
    dev_container_model.add_mount(mount)

    # Check if the custom mount was added correctly
    assert dev_container_model.mounts.count(mount) == 1


def test_adding_environment_variable(
    dev_container_model: DevContainer,
) -> None:
    """Test adding an environment variable.

    Args:
        dev_container_model (DevContainer): The DevContainer instance.
    """
    # Add an environment variable
    dev_container_model.add_environment_variable('TEST_VAR', 'test_value')

    # Check if the environment variable was added correctly
    assert dev_container_model.remote_environment['TEST_VAR'] == 'test_value'


def test_overwriting_environment_variable(
    dev_container_model: DevContainer,
) -> None:
    """Test overwriting an existing environment variable.

    Args:
        dev_container_model (DevContainer): The DevContainer instance.
    """
    # Add an environment variable
    dev_container_model.add_environment_variable('TEST_VAR', 'initial_value')

    # Overwrite the environment variable
    dev_container_model.add_environment_variable('TEST_VAR', 'new_value')

    # Check if the environment variable was updated correctly
    assert dev_container_model.remote_environment['TEST_VAR'] == 'new_value'
