"""Config part of the CLI tool."""

import typer

from slough import Slough
from slough_config import Author, ProjectInformation, SloughConfig

project = typer.Typer(no_args_is_help=True)


@project.command(name='init')
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
    context = ctx.obj
    slough: Slough = context['slough']

    # Create a new Slough object
    slough_config = SloughConfig(
        project=ProjectInformation(
            name=title,
            version=version,
            authors=[Author(name=author_name, email=author_email)],
        )
    )

    # Set the configuration in the `Slough` object
    # TODO: Make sure it is only done when there is no configurationfile
    #       yet.
    slough.config = slough_config

    # Save the configuration
    slough.save()
