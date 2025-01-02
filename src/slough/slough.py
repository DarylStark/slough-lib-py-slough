"""Module with the Slough class."""

from pathlib import Path

from slough_config import ConfigFileFinder, ConfigLoader
from slough_config.config_model import SloughConfig


class Slough:
    """Class that represents a Slough application."""

    def __init__(
        self,
        cfgfile: str | None = None,
        max_directory_depth: int = 6,
    ) -> None:
        """Initialize the Slough object.

        Args:
            cfgfile (str): Path to the configuration file. If none is given,
                the configuration file will be searched for.
            max_directory_depth (int): The maximum directory depth to search
                for the configuration file.
        """
        self._config: SloughConfig | None = None
        self._max_directory_depth = max_directory_depth
        self.cfgfile: Path | None = None
        if cfgfile:
            self.cfgfile = Path(cfgfile)
        else:
            self._set_correct_configfile()

    def _set_correct_configfile(self) -> None:
        """Set the correct configuration file.

        Args:
            cfgfile (str): Path to the configuration file.
        """
        # Configfile is not set, find one
        finder = ConfigFileFinder(
            max_directory_depth=self._max_directory_depth
        )
        self.cfgfile = finder.find_config_file() or Path('.slough/slough.yml')

    def _load_config(self) -> None:
        """Load the configuration.

        Uses a configloader that fits the configurationfile.
        """
        if not self.cfgfile:
            return

        # Find the extension for the configuration file
        extension = self.cfgfile.suffix[1:].lower()
        if extension not in ConfigLoader.loaders:
            # TODO: Custom exception
            raise ValueError(f'No loader for extension {extension}')

        # Load the configuration
        self._config = ConfigLoader.loaders[extension](
            self.cfgfile
        ).load_config()

    @property
    def config(self) -> SloughConfig | None:
        """Return the configuration."""
        if not self._config:
            self._load_config()
        return self._config
