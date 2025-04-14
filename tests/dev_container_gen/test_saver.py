"""Tests for the Saver class."""

from pathlib import Path

from dev_container_gen import DevContainer, Saver


def test_saving_file_without_options(
    temp_folder: Path, dev_container_model: DevContainer
) -> None:
    """Test saving a file without options.

    Args:
        temp_folder (Path): The path to the temporary folder.
        dev_container_model (DevContainer): The DevContainer instance.
    """
    # Create a Saver instance
    saver = Saver(temp_folder / 'devcontainer.json')

    # Save the DevContainer configuration
    saver.save(dev_container_model)

    # Check if the file was saved correctly
    with open(temp_folder / 'devcontainer.json') as file:
        content = file.read()
        assert '"name": "test"' in content
        assert '"image": "test_image"' in content


def test_saving_file_with_docker_mount(
    temp_folder: Path, dev_container_model: DevContainer
) -> None:
    """Test saving a file with a Docker mount.

    Args:
        temp_folder (Path): The path to the temporary folder.
        dev_container_model (DevContainer): The DevContainer instance.
    """
    dev_container_model.add_docker_mount()

    # Create a Saver instance
    saver = Saver(temp_folder / 'devcontainer.json')

    # Save the DevContainer configuration
    saver.save(dev_container_model)

    # Check if the file was saved correctly
    with open(temp_folder / 'devcontainer.json') as file:
        content = file.read()
        assert '"name": "test"' in content
        assert '"image": "test_image"' in content
        assert (
            'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind'
        ) in content


def test_saving_file_with_environment_variables(
    temp_folder: Path, dev_container_model: DevContainer
) -> None:
    """Test saving a file with environment variables.

    Args:
        temp_folder (Path): The path to the temporary folder.
        dev_container_model (DevContainer): The DevContainer instance.
    """
    dev_container_model.add_environment_variable('TEST_VAR', 'test_value')

    # Create a Saver instance
    saver = Saver(temp_folder / 'devcontainer.json')

    # Save the DevContainer configuration
    saver.save(dev_container_model)

    # Check if the file was saved correctly
    with open(temp_folder / 'devcontainer.json') as file:
        content = file.read()
        assert '"name": "test"' in content
        assert '"image": "test_image"' in content
        assert '"TEST_VAR": "test_value"' in content
