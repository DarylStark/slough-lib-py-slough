"""Main module for slough-cli-tool."""

import typer
from rich.console import Console

from slough import Slough
from slough.exceptions import SloughError

from .config import config
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
    ctx.obj = {'slough': Slough(cfgfile), 'console': Console()}


def main() -> None:
    """Entry point for the slough-cli-tool."""
    try:
        app()
    except SloughError as exc:
        console = Console()
        console.print(f'Slough error: {str(exc)}', style='bold red')
