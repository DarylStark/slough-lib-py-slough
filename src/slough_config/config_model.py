"""Module with the model for the configuration file."""

from pydantic import BaseModel


class ProjectInformation(BaseModel):
    """Model for the project information."""

    name: str
    version: str
    authors: list[str]


class SloughConfig(BaseModel):
    """Model for the configuration file."""

    project: ProjectInformation
