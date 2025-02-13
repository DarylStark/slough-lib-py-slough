"""Module with the model for the configuration file."""

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


class SloughConfig(BaseModel):
    """Model for the configuration file.

    Attributes:
        project (ProjectInformation): The project information.
        development_environment (DevelopmentEnvironment | None): The
            development environment, if specified.
    """

    project: ProjectInformation
    development_environment: DevelopmentEnvironment | None = None
