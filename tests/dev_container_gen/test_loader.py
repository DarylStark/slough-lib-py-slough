"""Tests for the Loader class."""

from pathlib import Path

from dev_container_gen import Loader


def test_load_non_existing_file(temp_folder: Path) -> None:
    """Test loading a non existing file.

    Args:
        temp_folder (Path): The path to the temporary folder.
    """
    loader = Loader(temp_folder / 'devcontainer.json')
    dev_container = loader.load()
    assert dev_container is None


def test_loading_file_without_options(
    temp_folder_with_dev_containers: Path,
) -> None:
    """Test loading a file without options.

    Args:
        temp_folder_with_dev_containers (Path): The path to the temporary
            folder with dev containers.
    """
    loader = Loader(temp_folder_with_dev_containers / 'devcontainer1.json')
    dev_container = loader.load()
    assert dev_container is not None
    assert dev_container.name == 'test-container'
    assert dev_container.image == 'latest'


def test_loading_file_with_environment_variables(
    temp_folder_with_dev_containers: Path,
) -> None:
    """Test loading a file with environment variables.

    Args:
        temp_folder_with_dev_containers (Path): The path to the temporary
            folder with dev containers.
    """
    loader = Loader(temp_folder_with_dev_containers / 'devcontainer2.json')
    dev_container = loader.load()
    assert dev_container is not None
    assert dev_container.name == 'test-container'
    assert dev_container.image == 'latest'
    assert dev_container.remote_environment['TEST_VAR'] == 'test_value'


def test_loading_file_with_mounts(
    temp_folder_with_dev_containers: Path,
) -> None:
    """Test loading a file with mounts.

    Args:
        temp_folder_with_dev_containers (Path): The path to the temporary
            folder with dev containers.
    """
    loader = Loader(temp_folder_with_dev_containers / 'devcontainer3.json')
    dev_container = loader.load()
    assert dev_container is not None
    assert dev_container.name == 'test-container'
    assert dev_container.image == 'latest'
    assert dev_container.mounts == ['test_mount']
