"""Dev Container part of the CLI tool."""

import typer

from .generic import get_context_data

dev_container = typer.Typer(no_args_is_help=True)


@dev_container.command(
    name='generate-config',
    help='Initialize configuration for a dev container. This uses the '
    + '"dev-environment" value from the Slough configuration file to choose '
    + 'a specific container image.',
    short_help='Initialize a new project configuration.',
)
def cli_dev_container_generate_config(ctx: typer.Context) -> None:
    """Initialize configuration for a dev container."""
    console, slough = get_context_data(ctx)
    console.print('[bold]Generating dev container configuration[/bold]')
