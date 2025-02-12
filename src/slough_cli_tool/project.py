"""Config part of the CLI tool."""

import logging

import typer

from slough_config import (
    Author,
    DevelopmentEnvironment,
    ProjectInformation,
    SloughConfig,
)

from .exceptions import ConfigAlreadySetError
from .generic import get_context_data

project = typer.Typer(no_args_is_help=True)


@project.command(
    name='init',
    help='Initialize a new project configuration. This command will prompt'
    + ' you for the project title, version, author name, and author email. If'
    + 'the configuration already exists, this command will fail.',
    short_help='Initialize a new project configuration.',
)
def cli_project_init(
    ctx: typer.Context,
    title: str = typer.Option(
        ...,
        prompt='📛 Please enter the project title',
        help='The project title',
    ),
    version: str = typer.Option(
        ...,
        prompt='🏷️  Please enter the project version',
        help='The project version',
    ),
    author_name: str = typer.Option(
        ...,
        prompt='👤 Please enter the name of the author',
        help='The project author name',
    ),
    author_email: str = typer.Option(
        ...,
        prompt='📧 Please enter the email of the author',
        help='The project author email',
    ),
    development_environment: DevelopmentEnvironment | None = typer.Option(
        default=None,
        help='The development environment',
    ),
) -> None:
    """Initialize a configuration file for a project.

    Args:
        ctx (typer.Context): Typer context.
        title (str): The project title.
        version (str): The project version.
        author_name (str): The author name.
        author_email (str): The author.
        development_environment (DevelopmentEnvironment): The development
            environment.
    """
    _, slough = get_context_data(ctx)

    # Create a new Slough object
    slough_config = SloughConfig(
        project=ProjectInformation(
            name=title,
            version=version,
            authors=[Author(name=author_name, email=author_email)],
        ),
        development_environment=development_environment,
    )

    # Set the configuration in the `Slough` object
    local_logger = logging.getLogger('cli_project_init')
    if not slough.config:
        slough.config = slough_config
        local_logger.info('Created configuration')
    else:
        raise ConfigAlreadySetError('Configuration already set')

    # Save the configuration
    slough.save()
