"""Main module for slough-cli-tool."""

import os
import sys

import typer
from rich.console import Console

from slough import Slough
from slough import __version__ as slough_version
from slough.exceptions import SloughError

from .config import config
from .exceptions import SloughCLIError
from .project import project

app = typer.Typer(no_args_is_help=True)
app.add_typer(config, name='config')
app.add_typer(project, name='project')


@app.callback()
def common_command_line_options(
    ctx: typer.Context,
    cfgfile: str = typer.Option(
        None, help='Path to the configuration file.', envvar='SLOUGH_CFGFILE'
    ),
) -> None:
    """Common options for all commands.

    This is run for all commands, and makes sure the correct configuration file
    is loaded.

    Args:
        ctx (typer.Context): Typer context object.
        cfgfile (str): Path to the configuration file.
    """
    ctx.obj = {
        'slough': Slough(
            cfgfile,
            max_directory_depth=int(os.environ.get('MAX_DIR_DEPTH', '6')),
        ),
        'console': Console(),
    }


@app.command('version')
def version(ctx: typer.Context) -> None:
    """Print the version of slough-cli-tool."""
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
