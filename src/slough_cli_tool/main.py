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
    cli_logger = create_default_cli_logger(verbosity)

    # Find the needed configfile
    cfgfile_path = create_cfgfile_path()

    # Get a StorageManager
    slough = create_slough_object(cfgfile_path)

    # Create a context aware object that can be used by all commands.
    ctx.obj = {
        'slough': slough,
        'console': Console(),
        'logger': cli_logger,
    }
    cli_logger.debug('Created context object')
    cli_logger.info('Configuration file in context: "%s"', str(cfgfile_path))


def create_slough_object(cfgfile_path: Path) -> Slough:
    """Create a Slough object.

    Args:
        cfgfile_path (Path): Path to the configuration file.

    Returns:
        Slough: Slough object.
    """
    cfgfile_path = create_cfgfile_path()
    storage_manager = YAMLStorageManager(cfgfile_path)

    # Create a Slough object
    slough = Slough(storage_manager=storage_manager)
    return slough


def create_cfgfile_path() -> Path:
    """Create the path to the configuration file.

    Returns:
        Path: Path to the configuration file.
    """
    cfgfile_path = ConfigFileFinder(filename='slough.yml').find()
    if not cfgfile_path:
        cfgfile_path = Path.cwd() / 'slough.yml'
    return cfgfile_path


def create_default_cli_logger(verbosity: int) -> logging.Logger:
    """Create a defaullt CLI logger.

    Args:
        verbosity (int): Verbosity level.

    Returns:
        logging.Logger: Configured logger.
    """
    logging.basicConfig(
        level=logging.WARNING - (verbosity * 10),
        format='"%(name)s": %(message)s',
        datefmt='[%X]',
        handlers=[RichHandler()],
    )
    cli_logger = logging.getLogger('cli')
    return cli_logger


@app.command('version')
def version(ctx: typer.Context) -> None:
    """Print the version of slough-cli-tool.

    Args:
        ctx (typer.Context): Typer context object.
    """
    console = ctx.obj['console']
    console.print(f'[b]slough-cli-tool[/b] version: [u]{slough_version}[/u]')


def main() -> None:
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
