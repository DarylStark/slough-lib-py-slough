"""Module with the model for the configuration file."""

import re
from enum import Enum

from pydantic import BaseModel, Field


class Author(BaseModel):
    """Model for the author information.

    Attributes:
        name (str): The name of the author.
        email (str): The email address of the author. Must match the specified
            pattern.
    """

    name: str
    email: str = Field(pattern=r'^\S+@\S+\.\S+$')


class ProjectInformation(BaseModel):
    """Model for the project information.

    Attributes:
        name (str): The name of the project.
        version (str): The version of the project. Must follow semantic
            versioning.
        authors (list[Author]): A list of authors involved in the project.
    """

    name: str
    version: str = Field(pattern=r'^(\d+)\.(\d+)\.(\d+)(?:-\S+(?:\.(\d+))?)?$')
    authors: list[Author]


class DevelopmentEnvironment(str, Enum):
    """Enum for the development environment.

    Attributes:
        PYTHON_GENERIC (str): Represents a generic Python development
            environment.
        NODEJS_GENERIC (str): Represents a generic Node.js development
            environment.
    """

    CPP_GENERIC = 'cpp-generic'
    GENERIC = 'generic'
    NODEJS_GENERIC = 'nodejs-generic'
    PYTHON_GENERIC = 'python-generic'
    RUST_GENERIC = 'rust-generic'


class ContainerConfiguration(BaseModel):
    """Configuration for a container.

    Attributes:
        tags (list[str] | None): A list of tags for the container.
    """

    tags: list[str] = []


class ConfigProfile(BaseModel):
    """Model for the configuration profile.

    Contains all settins for a specific project.

    Attributes:
        container (ContainerConfiguration | None): The container configuration.
    """

    container: ContainerConfiguration | None = None


class SloughConfig(BaseModel):
    """Model for the configuration file.

    Attributes:
        project (ProjectInformation): The project information.
        development_environment (DevelopmentEnvironment | None): The
            development environment, if specified.
    """

    project: ProjectInformation
    development_environment: DevelopmentEnvironment | None = None
    cfg_profiles: dict[str, ConfigProfile] = {
        '_default': ConfigProfile(),
        '_all': ConfigProfile(),
    }

    def create_profile(self, profile_name: str) -> None:
        """Create a new configuration profile.

        Will create a new profile with the specified name if it does not exist.
        The name is validated against the pattern.

        Args:
            profile_name (str): The name of the profile to create.

        Raises:
            ValueError: If the profilename is already in use or if the
                profilename is invalid.
        """
        if profile_name in self.cfg_profiles:
            raise ValueError(f'Profile "{profile_name}" already exists.')

        if not re.match(r'^[a-zA-Z][A-Za-z0-9_-]+$', profile_name):
            raise ValueError(
                'Invalid profile name. Only alphanumeric characters, '
                'dashes, and underscores are allowed.'
            )
        self.cfg_profiles[profile_name] = ConfigProfile()

    def remove_profile(self, profile_name: str) -> None:
        """Remove a configuration profile.

        Will remove the profile with the specified name if it exists.

        Args:
            profile_name (str): The name of the profile to remove.

        Raises:
            ValueError: If the profile does not exist.
        """
        if profile_name not in self.cfg_profiles:
            raise ValueError(f'Profile "{profile_name}" does not exist.')
        del self.cfg_profiles[profile_name]
