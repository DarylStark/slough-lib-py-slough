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
        self._key_value_pairs: list[tuple[str, str]] = []
        self._prefix = prefix

    def visit_slough_config(self, config_model: SloughConfig) -> None:
        """Visit the configuration model.

        Args:
            config_model (SloughConfig): The configuration model.
        """
        if config_model.development_environment:
            self._key_value_pairs.extend(
                [
                    (
                        f'{self._prefix}.development_environment',
                        config_model.development_environment.value,
                    )
                ]
            )
        config_model.project.visit(self)

    def visit_project_information(
        self, config_model: ProjectInformation
    ) -> None:
        """Visit the configuration model.

        Args:
            config_model (ProjectInformation): The project information model.
        """
        self._key_value_pairs.extend(
            [
                (f'{self._prefix}.project.name', config_model.name),
                (f'{self._prefix}.project.version', config_model.version),
                (
                    f'{self._prefix}.project.authors.count',
                    str(len(config_model.authors)),
                ),
            ]
        )
        for index, author in enumerate(config_model.authors):
            self._add_author(index, author)

    def _add_author(self, index: int, author: Author) -> None:
        """Add author information to the key-value pairs.

        Args:
            index (int): The index of the author.
            author (Author): The author model.
        """
        self._key_value_pairs.extend(
            [
                (f'{self._prefix}.project.authors.{index}.name', author.name),
                (
                    f'{self._prefix}.project.authors.{index}.email',
                    author.email,
                ),
            ]
        )

    def visit_container_configuration(
        self, container_configuration: ContainerConfiguration
    ) -> None:
        """Visit the container configuration.

        Args:
            container_configuration (ContainerConfiguration): The container
                configuration model.
        """
        self._key_value_pairs.append(
            (
                f'{self._prefix}.configuration.container.tag.count',
                str(len(container_configuration.tags)),
            )
        )
        self._key_value_pairs.append(
            (
                f'{self._prefix}.configuration.container.tags',
                ','.join(container_configuration.tags),
            )
        )
        for index, tag in enumerate(container_configuration.tags):
            self._key_value_pairs.append(
                (f'{self._prefix}.configuration.container.tag.{index}', tag)
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
        return self._key_value_pairs


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
