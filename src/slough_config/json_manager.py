"""Module with a JSON configuration manager."""

import json
from pathlib import Path

from .config_manager import ConfigManager


@ConfigManager.register_manager(['json'])
class JSONManager(ConfigManager):
    """Class that manages a JSON configuration file."""

    def __init__(self, cfgfile: Path) -> None:
        """Initialize the ConfigManager.

        Args:
            cfgfile (Path): Path to the configuration file.
        """
        super().__init__(cfgfile)

    def _load_config(self) -> dict:
        """Load the configuration from a JSON file.

        Returns:
            dict: The configuration as a dictionary.
        """
        with self.cfgfile.open('r') as file:
            return json.load(file)

    def save_config(self, config: dict) -> None:
        """Save the configuration to a JSON file.

        Args:
            config (dict): The configuration to save.
        """
        self._create_parent_directory()
        with self.cfgfile.open('w') as file:
            return json.dump(config, file, indent=4)
