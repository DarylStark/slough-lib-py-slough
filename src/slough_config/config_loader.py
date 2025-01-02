"""Module with a interface for a ConfigLoader."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from pathlib import Path

from slough_config.config_model import SloughConfig


class ConfigLoader(ABC):
    """Interface for a ConfigLoader."""

    loaders: dict[str, type['ConfigLoader']] = {}

    @classmethod
    def register_loader(
        cls, extensions: list[str]
    ) -> Callable[[type['ConfigLoader']], type['ConfigLoader']]:
        """Register a loader.

        Args:
            extensions (list[str]): List of extensions that the loader should
                be registered for.

        Returns:
            Callable[[type['ConfigLoader']], type['ConfigLoader']]:
                The decorator.
        """

        def decorator(subclass: type['ConfigLoader']) -> type['ConfigLoader']:
            """Decorator that registers the loader.

            Args:
                subclass (type['ConfigLoader']): The subclass to register.

            Returns:
                type['ConfigLoader']: The subclass.
            """
            for extension in extensions:
                cls.loaders[extension] = subclass
            return subclass

        return decorator

    def __init__(self, cfgfile: Path) -> None:
        """Initialize the ConfigLoader.

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

    def load_config(self) -> SloughConfig:
        """Load the configuration and validates it.

        The `_load_config` method loads the configuration from a file in the
        way it needs to be done for the specific file type. The `load_config`
        method makes sure it becomes a `SloughConfig` object.

        Returns:
            SloughConfig: The configuration as SloughConfig object.
        """
        return SloughConfig(**self._load_config())
