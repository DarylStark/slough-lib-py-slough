"""Config part of the CLI tool."""

import typer

from slough.slough import Slough
from slough_cli_tool.cli_output_models import DataSetOutput
from slough_config.config_model import (
    Author,
    ConfigProfile,
    ContainerConfiguration,
    ProjectInformation,
    SloughConfig,
)
from slough_config.config_model_visitor import ConfigModelVisitor

config = typer.Typer(no_args_is_help=True)


class KeyValueConfigVisitor(ConfigModelVisitor):
    """Visitor that collects key-value pairs from the configuration model.

    This visitor is used to output the configuration as key-value pairs.
    """

    def __init__(self, prefix: str) -> None:
        """Initialize the visitor.

        Args:
            prefix (str): The prefix for the configuration variables.
        """
        # self._key_value_pairs: list[tuple[str, str]] = []
        self._key_value_pairs: dict[str, str] = {}
        self._prefix: str = prefix

    def _add_key_value_pair(self, key: str, value: str | int) -> None:
        """Add a key-value pair to the list.

        Args:
            key (str): The key.
            value (str): The value.
        """
        key = f'{self._prefix}.{key}'
        # self._key_value_pairs.append((key, str(value)))
        self._key_value_pairs[key] = str(value)

    def visit_slough_config(self, config_model: SloughConfig) -> None:
        """Visit the configuration model.

        Args:
            config_model (SloughConfig): The configuration model.
        """
        if config_model.development_environment:
            self._add_key_value_pair(
                'development_environment',
                config_model.development_environment.value,
            )
        config_model.project.visit(self)

    def visit_project_information(
        self, config_model: ProjectInformation
    ) -> None:
        """Visit the configuration model.

        Args:
            config_model (ProjectInformation): The project information model.
        """
        self._add_key_value_pair('project.name', config_model.name)
        self._add_key_value_pair('project.version', config_model.version)
        self._add_key_value_pair(
            'project.authors.count', len(config_model.authors)
        )
        for index, author in enumerate(config_model.authors):
            self._add_author(index, author)

    def _add_author(self, index: int, author: Author) -> None:
        """Add author information to the key-value pairs.

        Args:
            index (int): The index of the author.
            author (Author): The author model.
        """
        self._add_key_value_pair(f'project.authors.{index}.name', author.name)
        self._add_key_value_pair(
            f'project.authors.{index}.email', author.email
        )

    def visit_container_configuration(
        self, container_configuration: ContainerConfiguration
    ) -> None:
        """Visit the container configuration.

        Args:
            container_configuration (ContainerConfiguration): The container
                configuration model.
        """
        self._add_key_value_pair(
            'configuration.container.tag.count',
            len(container_configuration.tags),
        )
        self._add_key_value_pair(
            'configuration.container.tags',
            ','.join(container_configuration.tags),
        )
        for index, tag in enumerate(container_configuration.tags):
            self._add_key_value_pair(
                f'configuration.container.tag.{index}', tag
            )
        if container_configuration.registry:
            self._add_key_value_pair(
                'configuration.container.registry',
                container_configuration.registry,
            )
        if container_configuration.image:
            self._add_key_value_pair(
                'configuration.container.image',
                container_configuration.image,
            )

    def visit_config_profile(self, config_profile: ConfigProfile) -> None:
        """Visit the configuration profile.

        Args:
            config_profile (ConfigProfile): The configuration profile model.
        """
        config_profile.get_container_configuration().visit(self)

    @property
    def key_value_pairs(self) -> list[tuple[str, str]]:
        """Get the key-value pairs.

        Returns:
            list[tuple[str, str]]: The key-value pairs.
        """
        return [(key, value) for key, value in self._key_value_pairs.items()]


@config.command(
    name='list',
    help='List the configuration.',
    short_help='List the configuration',
)
def cli_config_list(
    ctx: typer.Context,
    prefix: str = typer.Option(
        default='slough', help='The prefix for the configuration variables.'
    ),
    profile: str = typer.Option(
        '_default', help='Profile to use for the configuration.'
    ),
) -> None:
    """Show configuration as key-value pairs.

    Args:
        ctx (typer.Context): Typer context.
        prefix (str): Prefix for the environment variables
        profile (str | None): Profile to use for the configuration.
    """
    slough: Slough = ctx.obj.slough
    visitor = KeyValueConfigVisitor(prefix=prefix)
    slough.config.visit(visitor)

    cfg_profile = slough.get_profile_with_all(profile_name=profile)
    cfg_profile.visit(visitor)

    output_data = DataSetOutput(['Setting', 'Value'])
    output_data.data = sorted(visitor.key_value_pairs, key=lambda x: x[0])
    output_data.out(ctx.obj.output_visitor)
