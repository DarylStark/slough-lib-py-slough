"""Module with a YAML configuration manager."""

from pathlib import Path

import yaml

from .config_manager import ConfigManager


@ConfigManager.register_manager(['yml', 'yaml'])
class YAMLManager(ConfigManager):
    """Class that manage a YAML configuration file."""

    def __init__(self, cfgfile: Path) -> None:
        """Initialize the ConfigManager.

        Args:
            cfgfile (Path): Path to the configuration file.
        """
        super().__init__(cfgfile)

    def _load_config(self) -> dict:
        """Load the configuration from a YAML file.

        Returns:
            dict: The configuration as a dictionary.
        """
        with self.cfgfile.open('r') as file:
            return yaml.safe_load(file)

    def save_config(self, config: dict) -> None:
        """Save the configuration to a YAML file.

        Args:
            config (dict): The configuration to save.
        """
        pass
