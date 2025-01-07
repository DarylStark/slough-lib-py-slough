"""Module with the model for the configuration file."""

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


class SloughConfig(BaseModel):
    """Model for the configuration file."""

    project: ProjectInformation
