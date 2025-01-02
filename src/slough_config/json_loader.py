"""Module with a JSON configuration loader."""

import json
from pathlib import Path

from .config_loader import ConfigLoader


@ConfigLoader.register_loader(['json'])
class JSONLoader(ConfigLoader):
    """Class that loads a JSON configuration file."""

    def __init__(self, cfgfile: Path) -> None:
        """Initialize the ConfigLoader.

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
