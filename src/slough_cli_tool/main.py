"""Main module for slough-cli-tool."""

import logging
import os
import sys

import typer
from rich.console import Console
from rich.logging import RichHandler

from slough import Slough
from slough import __version__ as slough_version
from slough.exceptions import SloughError

from .config import config
from .dev_container import dev_container
from .exceptions import SloughCLIError
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


@app.callback()
def common_command_line_options(
    ctx: typer.Context,
    cfgfile: str = typer.Option(
        None, help='Path to the configuration file.', envvar='SLOUGH_CFGFILE'
    ),
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
    local_logger.debug('Given configuration file: "%s"', cfgfile)

    # Create a context aware object that can be used by all commands.
    ctx.obj = {
        'slough': Slough(
            cfgfile,
            max_directory_depth=int(os.environ.get('MAX_DIR_DEPTH', '6')),
        ),
        'console': Console(),
    }
    local_logger.debug('Created context object')
    local_logger.info(
        'Configuration file in context: "%s"', ctx.obj['slough'].cfgfile
    )


@app.command('version')
def version(ctx: typer.Context) -> None:
    """Print the version of slough-cli-tool."""
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
