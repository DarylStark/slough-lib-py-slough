"""Module with the Slough class."""

from pathlib import Path

from slough_config import ConfigFileFinder


class Slough:
    """Class that represents a Slough application."""

    def __init__(self, cfgfile: str | None = None) -> None:
        """Initialize the Slough object.

        Args:
            cfgfile (str): Path to the configuration file. If none is given,
                the configuration file will be searched for.
        """
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
        finder = ConfigFileFinder()
        self.cfgfile = finder.find_config_file() or Path('.slough/slough.yml')
