"""Config part of the CLI tool."""

import typer

from slough_config import Author, ProjectInformation, SloughConfig

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
) -> None:
    """Initialize a configuration file for a project.

    Args:
        ctx (typer.Context): Typer context.
        title (str): The project title.
        version (str): The project version.
        author_name (str): The author name.
        author_email (str): The author
    """
    _, slough = get_context_data(ctx)

    # Create a new Slough object
    slough_config = SloughConfig(
        project=ProjectInformation(
            name=title,
            version=version,
            authors=[Author(name=author_name, email=author_email)],
        )
    )

    # Set the configuration in the `Slough` object
    if not slough.config:
        slough.config = slough_config
    else:
        raise ConfigAlreadySetError('Configuration already set')

    # Save the configuration
    slough.save()
