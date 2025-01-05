"""Config part of the CLI tool."""

import typer

from slough import Slough
from slough_config import Author, ProjectInformation, SloughConfig

from .generic import raise_for_missing_config
from .output_formatters import OutputFormatter, OutputType

config = typer.Typer(no_args_is_help=True)


@config.command(name='show')
def cli_config_show(
    ctx: typer.Context, output: OutputType = typer.Option(OutputType.yaml)
) -> None:
    """Show configuration in specific output formats.

    Args:
        ctx (typer.Context): Typer context.
        output (OutputType, optional): Output format. Defaults to YAML.
    """
    context = ctx.obj
    slough: Slough = context['slough']
    raise_for_missing_config(slough)
    if not isinstance(slough, Slough) or not slough.config:
        # TODO: Custom exception
        return

    console = context['console']
    config_dict = slough.config

    if output in OutputFormatter.formatters:
        formatter = OutputFormatter.formatters[output](config_dict)
        console.print(formatter.format(), end='')
    else:
        raise TypeError(f'Output type {output} not supported.')


@config.command(name='init')
def cli_config_init(
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
    """Initialize a configuration file.

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
