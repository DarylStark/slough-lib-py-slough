"""Module with a interface for a ConfigManager."""

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

    @abstractmethod
    def _load_config(self) -> dict:
        """Abstract method that loads the config.

        Should return a dictionary with the configuration.

        Returns:
            dict: The configuration.
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
            return SloughConfig(**self._load_config())
        except FileNotFoundError:
            return None
