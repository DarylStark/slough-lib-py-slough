"""Module with a interface for a ConfigManager."""

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from pathlib import Path

from slough_config.config_model import SloughConfig


class ConfigManager(ABC):
    """Interface for a ConfigManager."""

    managers: dict[str, type['ConfigManager']] = {}

    @classmethod
    def register_manager(
        cls, extensions: list[str]
    ) -> Callable[[type['ConfigManager']], type['ConfigManager']]:
        """Register a ConfigManager.

        Args:
            extensions (list[str]): List of extensions that the manager should
                be registered for.

        Returns:
            Callable[[type['ConfigManager']], type['ConfigManager']]:
                The decorator.
        """

        def decorator(
            subclass: type['ConfigManager'],
        ) -> type['ConfigManager']:
            """Decorator that registers the manager.

            Args:
                subclass (type['ConfigManager']): The subclass to register.

            Returns:
                type['ConfigManager']: The subclass.
            """
            for extension in extensions:
                cls.managers[extension] = subclass
            return subclass

        return decorator

    def __init__(self, cfgfile: Path) -> None:
        """Initialize the ConfigManager.

        Args:
            cfgfile (Path): Path to the configuration file.
        """
        self.cfgfile = cfgfile
        self._logger = logging.getLogger('ConfigManager')
        self._logger.debug(f'ConfigManager initialized for "{cfgfile}"')

    def _create_parent_directory(self) -> None:
        """Create the parent directory of the configuration file."""
        self._logger.debug(f'Creating parent directory for "{self.cfgfile}"')
        self.cfgfile.resolve().parent.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def _load_config(self) -> dict:
        """Abstract method that loads the config.

        Should return a dictionary with the configuration.

        Returns:
            dict: The configuration.
        """

    @abstractmethod
    def save_config(self, config: dict) -> None:
        """Abstract method that saves the config.

        Saves the config to the configured configuration file.

        Args:
            config (dict): The configuration to save.
        """

    def load_config(self) -> SloughConfig | None:
        """Load the configuration and validates it.

        The `_load_config` method loads the configuration from a file in the
        way it needs to be done for the specific file type. The `load_config`
        method makes sure it becomes a `SloughConfig` object.

        Returns:
            SloughConfig: The configuration as SloughConfig object.
        """
        try:
            self._logger.debug(f'Loading configuration from "{self.cfgfile}"')
            return SloughConfig(**self._load_config())
        except FileNotFoundError:
            return None
