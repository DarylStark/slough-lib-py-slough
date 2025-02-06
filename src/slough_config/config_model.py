"""Module with the model for the configuration file."""

from enum import Enum

from pydantic import BaseModel, Field


class Author(BaseModel):
    """Model for the author information."""

    name: str
    email: str = Field(pattern=r'^\S+@\S+\.\S+$')


class ProjectInformation(BaseModel):
    """Model for the project information."""

    name: str
    version: str = Field(pattern=r'^(\d+)\.(\d+)\.(\d+)(?:-\S+(?:\.(\d+))?)?$')
    authors: list[Author]


class DevelopmentEnvironment(str, Enum):
    """Enum for the development environment."""

    PYTHON_GENERIC = 'python-generic'
    NODEJS_GENERIC = 'nodejs-generic'


class SloughConfig(BaseModel):
    """Model for the configuration file."""

    project: ProjectInformation
    development_environment: DevelopmentEnvironment | None = None
