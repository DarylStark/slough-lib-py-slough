"""Module with the model for the configuration file."""

from pydantic import BaseModel


class Author(BaseModel):
    """Model for the author information."""

    name: str
    email: str


class ProjectInformation(BaseModel):
    """Model for the project information."""

    name: str
    version: str
    authors: list[Author]


class SloughConfig(BaseModel):
    """Model for the configuration file."""

    project: ProjectInformation
