"""Module with a StorageManager for YAML files."""

from pathlib import Path

import yaml

from slough_config import SloughConfig

from .storage_manager import StorageManager


class YAMLStorageManager(StorageManager):
    """StorageManager for YAML files."""

    def __init__(self, file_path: Path) -> None:
        """Initialize the YAMLStorageManager.

        Args:
            file_path (Path): Path to the YAML file.
        """
        self.file_path = file_path

    def save(self, data: SloughConfig) -> None:
        """Save data to a YAML file.

        Args:
            data (SloughConfig): Data to save.
        """
        with open(self.file_path, 'w') as file:
            yaml.dump(data.model_dump(), file)

    def load(self) -> SloughConfig:
        """Load data from a YAML file.

        Returns:
            SloughConfig: Loaded data.
        """
        with open(self.file_path) as file:
            return SloughConfig(**yaml.load(file, Loader=yaml.FullLoader))
