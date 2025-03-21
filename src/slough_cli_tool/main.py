"""Main module for slough-cli-tool."""

import logging
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.logging import RichHandler

from slough import Slough
from slough import __version__ as slough_version
from slough.config_file_finder import ConfigFileFinder
from slough.exceptions import SloughError
from slough.yaml_storage_manager import YAMLStorageManager
from slough_config.config_model import Author, ProjectInformation, SloughConfig

from .config import config
from .container import container
from .dev_container import dev_container
from .exceptions import SloughCLIError
from .profiles import profiles
from .project import project

app = typer.Typer(no_args_is_help=True)
app.add_typer(
    config,
    name='config',
    help='Commands to work with configuration.',
    short_help='Configuration related commands.',
)
app.add_typer(
    project,
    name='project',
    help='Manage the project.',
    short_help='Project related commands.',
)
app.add_typer(
    dev_container,
    name='dev-container',
    help='Generate and manage dev container configuration.',
    short_help='Dev container commands.',
)
app.add_typer(
    container,
    name='container',
    help='Manage container configuration.',
    short_help='Container commands.',
)
app.add_typer(
    profiles,
    name='profiles',
    help='Manage configuration profiles.',
    short_help='Configuration profiles.',
)


@app.callback()
def common_command_line_options(
    ctx: typer.Context,
    verbosity: int = typer.Option(
        0,
        '--verbosity',
        '-v',
        count=True,
        help='Increase output verbosity.',
        max=2,
    ),
) -> None:
    """Common options for all commands.

    This is run for all commands, and makes sure the correct configuration file
    is loaded.

    Args:
        ctx (typer.Context): Typer context object.
        cfgfile (str): Path to the configuration file.
        verbosity (int): Verbosity level
    """
    # Set up logging
    logging.basicConfig(
        level=logging.WARNING - (verbosity * 10),
        format='"%(name)s": %(message)s',
        datefmt='[%X]',
        handlers=[RichHandler()],
    )

    local_logger = logging.getLogger('common_command_line_options')

    # Find the needed configfile
    cfgfile_path = ConfigFileFinder(filename='slough.yml').find()
    if not cfgfile_path:
        cfgfile_path = Path.cwd() / 'slough.yml'

    # Get a StorageManager
    storage_manager = YAMLStorageManager(cfgfile_path)
    try:
        config = storage_manager.load()
    except FileNotFoundError:
        config = SloughConfig(
            project=ProjectInformation(
                name='empty_project',
                version='0.0.1',
                authors=[Author(name='nobody', email='nobody@nobody.com')],
            )
        )

    # Create a Slough object
    slough = Slough(config=config)

    # Create a context aware object that can be used by all commands.
    ctx.obj = {
        'slough': slough,
        'console': Console(),
    }
    local_logger.debug('Created context object')
    local_logger.info('Configuration file in context: "%s"', str(cfgfile_path))


@app.command('version')
def version(ctx: typer.Context) -> None:
    """Print the version of slough-cli-tool.

    Args:
        ctx (typer.Context): Typer context object.
    """
    console = ctx.obj['console']
    console.print(f'[b]slough-cli-tool[/b] version: [u]{slough_version}[/u]')


def main() -> None:  # pragma: no cover
    """Entry point for the slough-cli-tool."""
    try:
        app()
    except SloughError as exc:
        console = Console()
        console.print(f'[b][u]Slough error:[/u][/b] {str(exc)}', style='red')
        sys.exit(1)
    except SloughCLIError as exc:
        console = Console()
        console.print(
            f'[b][u]Slough CLI error:[/u][/b] {str(exc)}', style='red'
        )
        sys.exit(2)
