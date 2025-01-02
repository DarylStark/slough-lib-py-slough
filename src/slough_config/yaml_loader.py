"""Module with a YAML configuration loader."""

from pathlib import Path

import yaml

from .config_loader import ConfigLoader


@ConfigLoader.register_loader(['yml', 'yaml'])
class YAMLLoader(ConfigLoader):
    """Class that loads a YAML configuration file."""

    def __init__(self, cfgfile: Path) -> None:
        """Initialize the ConfigLoader.

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
