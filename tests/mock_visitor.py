"""Mock visitor for the configuration model."""

# TODO: Check if this can be done with a Unit Test Mock.

from slough_config.config_model import (
    Author,
    ConfigProfile,
    ContainerConfiguration,
    ProjectInformation,
    SloughConfig,
)
from slough_config.config_model_visitor import ConfigModelVisitor


class MockVisitor(ConfigModelVisitor):
    """Mock visitor for the configuration model."""

    def __init__(self) -> None:
        """Initialize the visitor."""
        self.visited: list[str] = []

    def visit_author(self, author: Author) -> None:
        """Visit the author information.

        Args:
            author (SloughConfigModel): The author information.
        """
        self.visited.append('author')

    def visit_project_information(
        self, project_information: ProjectInformation
    ) -> None:
        """Visit the project information.

        Args:
            project_information (ProjectInformation): The project information.
        """
        self.visited.append('project_information')
        for author in project_information.authors:
            author.visit(self)

    def visit_container_configuration(
        self, container_configuration: ContainerConfiguration
    ) -> None:
        """Visit the container configuration.

        Args:
            container_configuration (ContainerConfiguration): The container
                configuration.
        """
        self.visited.append('container_configuration')

    def visit_config_profile(self, config_profile: ConfigProfile) -> None:
        """Visit the configuration profile.

        Args:
            config_profile (ConfigProfile): The configuration profile.
        """
        self.visited.append('config_profile')
        if config_profile.container:
            config_profile.container.visit(self)

    def visit_slough_config(self, config_model: SloughConfig) -> None:
        """Visit the configuration model.

        Args:
            config_model (SloughConfig): The configuration model.
        """
        self.visited.append('config_model')
        config_model.project.visit(self)
        for profile in config_model.cfg_profiles.values():
            profile.visit(self)
