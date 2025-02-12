"""Module with a YAML configuration manager."""

import logging
from pathlib import Path

import yaml

from slough_config.config_model import DevelopmentEnvironment

from .config_manager import ConfigManager


def development_environment_representer(
    dumper: yaml.Dumper, data: DevelopmentEnvironment
) -> yaml.ScalarNode:
    """Custom YAML representer for the DevelopmentEnvironment class.

    This function defines how instances of the DevelopmentEnvironment class
    should be represented when dumping to a YAML file. It converts the
    DevelopmentEnvironment instance to a YAML scalar with the appropriate tag.

    Args:
        dumper (yaml.Dumper): The YAML dumper instance.
        data (DevelopmentEnvironment): The DevelopmentEnvironment instance to
            be represented.

    Returns:
        yaml.ScalarNode: The YAML node representing the DevelopmentEnvironment
            instance.
    """
    return dumper.represent_scalar('tag:yaml.org,2002:str', data.value)


yaml.add_representer(
    DevelopmentEnvironment, development_environment_representer
)


@ConfigManager.register_manager(['yml', 'yaml'])
class YAMLManager(ConfigManager):
    """Class that manage a YAML configuration file."""

    def __init__(self, cfgfile: Path) -> None:
        """Initialize the ConfigManager.

        Args:
            cfgfile (Path): Path to the configuration file.
        """
        super().__init__(cfgfile)
        self._logger = logging.getLogger('YAMLManager')
        self._logger.debug(f'YAMLManager initialized for "{cfgfile}"')

    def _load_config(self) -> dict:
        """Load the configuration from a YAML file.

        Returns:
            dict: The configuration as a dictionary.
        """
        self._logger.debug('Loading configuration')
        with self.cfgfile.open('r') as file:
            return yaml.safe_load(file)

    def save_config(self, config: dict) -> None:
        """Save the configuration to a YAML file.

        Args:
            config (dict): The configuration to save.
        """
        self._logger.debug('Saving configuration')
        self._create_parent_directory()
        with self.cfgfile.open('w') as file:
            return yaml.dump(config, file)
