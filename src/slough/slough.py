"""Module with the Slough class."""

import logging

from slough_config.config_model import (
    SloughConfig,
)


class Slough:
    """Class that represents a Slough application."""

    def __init__(self, config: SloughConfig) -> None:
        """Initialize the Slough object.

        Args:
            config (SloughConfig): The configuration to use.
        """
        self._logger = logging.getLogger('Slough')
        self._config = config

    @property
    def config(self) -> SloughConfig | None:
        """Return the configuration.

        Returns:
            SloughConfig: The configuration.
        """
        return self._config

    @property
    def profile_list(self) -> list[str]:
        """Return a list with the profile names.

        Returns:
            list[str]: A list with the profile names.
        """
        return self._config.profile_list

    def add_profile(self, profile_name: str) -> None:
        """Add a profile to the configuration.

        Args:
            profile_name (str): The name of the profile to add.
        """
        self._config.add_profile(profile_name)

    def remove_profile(self, profile_name: str) -> None:
        """Remove a profile from the configuration.

        Args:
            profile_name (str): The name of the profile to remove.
        """
        self._config.remove_profile(profile_name)
