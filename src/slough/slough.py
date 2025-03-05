"""Module with the Slough class."""

import logging
from pathlib import Path

from slough_config import ConfigFileFinder, ConfigManager
from slough_config.config_model import (
    ConfigProfile,
    ContainerConfiguration,
    SloughConfig,
)

from .exceptions import (
    ConfigAlreadySetError,
    ConfigFileNotSetError,
    ConfigManagerNotRegisteredError,
    ConfigNotSetError,
)


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
        self._logger = logging.getLogger('Slough')
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
        self._logger.info(f'Configuration file set to {self.cfgfile}')

    def _get_config_manager(self) -> ConfigManager:
        """Get the correct configuration manager.

        Returns the correct configuration manager based on the extension of the
        configuration file.

        Returns:
            ConfigManager: The configuration manager.
        """
        if not self.cfgfile:
            raise ConfigFileNotSetError('No configuration file set.')

        extension = self.cfgfile.suffix[1:].lower()
        if extension not in ConfigManager.managers:
            raise ConfigManagerNotRegisteredError(
                f'No manager registered for extension {extension}'
            )
        self._logger.debug(
            f'Using "{ConfigManager.managers[extension].__name__}" class '
            + f'for extension "{extension}"'
        )
        return ConfigManager.managers[extension](self.cfgfile)

    def _load_config(self) -> None:
        """Load the configuration."""
        cfg_manager = self._get_config_manager()
        self._logger.info(f'Loading configuration from {self.cfgfile}')
        self._config = cfg_manager.load_config()
        self._logger.info(f'Loaded configuration from {self.cfgfile}')

    def save(self) -> None:
        """Save the configuration."""
        if not self._config:
            raise ConfigNotSetError('No configuration file set.')

        cfg_manager = self._get_config_manager()
        self._logger.info(f'Saving configuration to {self.cfgfile}')
        cfg_manager.save_config(self._config.model_dump())
        self._logger.info(f'Saved configuration to {self.cfgfile}')

    def get_config_for_profile(self, profile_name: str) -> SloughConfig:
        """Get the configuration for a specific profile.

        Args:
            profile_name (str): The name of the profile.

        Returns:
            ConfigProfile: The configuration for the profile.
        """
        if not self._config:
            self._load_config()
        if not self._config:
            raise ConfigNotSetError('No configuration set.')

        if profile_name not in self._config.cfg_profiles:
            raise ValueError(f'Profile "{profile_name}" not found.')

        return self._config

    @property
    def config(self) -> SloughConfig | None:
        """Return the configuration."""
        if not self._config:
            self._load_config()
        return self._config

    @config.setter
    def config(self, value: SloughConfig) -> None:
        """Set the configuration."""
        if self.config is not None:
            raise ConfigAlreadySetError('Configuration already set.')
        self._config = value

    @property
    def project_folder(self) -> Path:
        """Return the project folder.

        This can be the folder where the configuration file is located, or if
        the configuration file is in a `.slough` folder, the directory above
        that.

        Returns:
            Path: The project folder.
        """
        if not self.cfgfile:
            raise ConfigFileNotSetError('No configuration file set.')

        if self.cfgfile.parent.name == '.slough':
            return self.cfgfile.parent.parent.resolve()
        return self.cfgfile.parent.resolve()

    def add_container_tag(
        self, tag: str, *, profile_name: str = '_default'
    ) -> None:
        """Add a container tag to the configuration.

        If the given profile does not exist, it will be created.

        Args:
            tag (str): The tag to add.
            profile_name (str): The profile to add the tag to.
        """
        if not self._config:
            self._load_config()
        if not self._config:
            raise ConfigNotSetError('No configuration set.')

        # Create the profile if it doesn't exist
        if profile_name not in self._config.cfg_profiles:
            self._config.cfg_profiles[profile_name] = ConfigProfile()

        # Retrieve and update the profile
        profile = self._config.cfg_profiles[profile_name]
        if not profile.container:
            profile.container = ContainerConfiguration()
        if tag in profile.container.tags:
            raise ValueError(f'Tag "{tag}" already exists in profile.')
        profile.container.tags.append(tag)

    def remove_container_tag(
        self, tag: str, *, profile_name: str = '_default'
    ) -> None:
        """Delete a container tag from the configuration.

        If the tag is not found in the profile, a ValueError is raised.

        Args:
            tag (str): The tag to remove.
            profile_name (str): The profile to remove the tag from.
        """
        if not self._config:
            self._load_config()
        if not self._config:
            raise ConfigNotSetError('No configuration set.')

        # Retrieve and update the profile
        profile = self._config.cfg_profiles[profile_name]
        if not profile.container:
            raise ValueError(
                f'Profile "{profile_name}" has no container configuration.'
            )
        if tag not in profile.container.tags:
            raise ValueError(f'Tag "{tag}" doesn\'t exist in profile.')
        profile.container.tags.remove(tag)
