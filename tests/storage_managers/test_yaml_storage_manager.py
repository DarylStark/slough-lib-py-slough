"""Module with tests for the YAMLStorageManager class."""

from pathlib import Path

import pytest

from slough.yaml_storage_manager import YAMLStorageManager
from slough_config.config_model import SloughConfig


def test_saving_a_configuration(
    temp_folder: Path, config_model: SloughConfig
) -> None:
    """Test the ConfigFileFinder with a file in the root.

    Args:
        temp_folder (Path): Temporary folder for testing.
        config_model (SloughConfig): Configuration model for testing.
    """
    config_file = temp_folder / 'slough.yml'
    manager = YAMLStorageManager(file_path=config_file)
    manager.save(data=config_model)

    assert config_file.exists()
    file_contents = config_file.read_text()

    assert 'cfg_profiles' in file_contents
    assert 'development_environment: generic' in file_contents
    assert '  name: test' in file_contents
    assert '  version: 0.0.1' in file_contents


def test_loading_a_configuration(
    temp_folder: Path, config_model: SloughConfig
) -> None:
    """Test the ConfigFileFinder with a file in the root.

    Args:
        temp_folder (Path): Temporary folder for testing.
        config_model (SloughConfig): Configuration model for testing.
    """
    config_file = temp_folder / 'slough.yml'
    manager = YAMLStorageManager(file_path=config_file)
    manager.save(data=config_model)

    loaded_config = manager.load()

    assert loaded_config == config_model


def test_loading_a_configuration_no_existing_file(temp_folder: Path) -> None:
    """Test the ConfigFileFinder with a file in the root.

    Args:
        temp_folder (Path): Temporary folder for testing.
    """
    config_file = temp_folder / 'slough.yml'
    manager = YAMLStorageManager(file_path=config_file)

    with pytest.raises(FileNotFoundError):
        _ = manager.load()
