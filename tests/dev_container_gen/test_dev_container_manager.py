"""Tests for the DevContainerManager class."""

import json
from pathlib import Path

import pytest

from dev_container_gen import DevContainerManager


@pytest.mark.parametrize('name', ['test-project', 'another-project'])
def test_default_config(temp_folder: Path, name: str) -> None:
    """Test if we get the default name when no devcontainer.json exists.

    Args:
        temp_folder (Path): Temporary folder for testing.
        name (str): The name for the dev container.
    """
    manager = DevContainerManager(default_name=name)
    assert manager._dev_container_config.name == name  # noqa: SLF001


def test_loader_configuration(temp_folder_with_dev_containers: Path) -> None:
    """Test if we get the correct configuration when a config exists.

    Args:
        temp_folder_with_dev_containers (Path): Temporary folder with dev
            containers for testing.
    """
    manager = DevContainerManager(default_name='default_name')
    assert manager._dev_container_config.name == 'test-container'  # noqa: SLF001


@pytest.mark.parametrize('new_name', ['test-project', 'another-project'])
def test_updating_name(
    temp_folder_with_dev_containers: Path, new_name: str
) -> None:
    """Test if we can update the name of the dev container.

    Args:
        temp_folder_with_dev_containers (Path): Temporary folder with dev
            containers for testing.
        new_name (str): The new name for the dev container.
    """
    manager = DevContainerManager(default_name='default_name')
    manager.update_configuration(image='test_image', name=new_name)
    assert manager._dev_container_config.name == new_name  # noqa: SLF001


def test_adding_docker_bind(temp_folder_with_dev_containers: Path) -> None:
    """Test if we can add a Docker bind mount to the dev container.

    Args:
        temp_folder_with_dev_containers (Path): Temporary folder with dev
            containers for testing.
    """
    manager = DevContainerManager(default_name='default_name')
    manager.update_configuration(image='test_image', bind_docker_socket=True)
    assert (
        'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind'
        in manager._dev_container_config.mounts  # noqa: SLF001
    )


def test_removing_docker_bind(temp_folder_with_dev_containers: Path) -> None:
    """Test if we can remove a Docker bind mount from the dev container.

    Args:
        temp_folder_with_dev_containers (Path): Temporary folder with dev
            containers for testing.
    """
    manager = DevContainerManager(default_name='default_name')
    manager.update_configuration(image='test_image', bind_docker_socket=False)
    assert (
        'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind'
        not in manager._dev_container_config.mounts  # noqa: SLF001
    )


@pytest.mark.parametrize(
    'image_name',
    [
        'test-image1',
        'dev-container-image',
        'another_image',
    ],
)
def test_updating_the_image(
    temp_folder_with_dev_containers: Path, image_name: str
) -> None:
    """Test if we can update the image of the dev container.

    Args:
        temp_folder_with_dev_containers (Path): Temporary folder with dev
            containers for testing.
        image_name (str): The new image name for the dev container.
    """
    manager = DevContainerManager(default_name='default_name')
    manager.update_configuration(image=image_name)
    assert (
        manager._dev_container_config.image == f'{image_name}:latest'  # noqa: SLF001
    )


@pytest.mark.parametrize(
    'image_name',
    [
        'test-image1',
        'dev-container-image',
        'another_image',
    ],
)
@pytest.mark.parametrize(
    'tag_name',
    [
        '1.0.0',
        'latest-dev',
        'acc',
    ],
)
def test_updating_the_image_tag(
    temp_folder_with_dev_containers: Path, image_name: str, tag_name: str
) -> None:
    """Test if we can update the image and tag of the dev container.

    Args:
        temp_folder_with_dev_containers (Path): Temporary folder with dev
            containers for testing.
        image_name (str): The new image name for the dev container.
        tag_name (str): The new tag name for the dev container.
    """
    manager = DevContainerManager(default_name='default_name')
    manager.update_configuration(image=image_name, tag=tag_name)
    assert (
        manager._dev_container_config.image == f'{image_name}:{tag_name}'  # noqa: SLF001
    )


@pytest.mark.parametrize('name', ['test-project', 'another-project'])
def test_saving_config(temp_folder: Path, name: str) -> None:
    """Test if we can save the configuration.

    Args:
        temp_folder (Path): Temporary folder for testing.
        name (str): The name for the dev container.
    """
    manager = DevContainerManager(default_name=name)
    manager.save()
    with open('.devcontainer/devcontainer.json') as f:
        config = json.load(f)
        assert config['name'] == name
