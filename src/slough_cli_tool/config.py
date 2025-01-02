"""Config part of the CLI tool."""

import typer

config = typer.Typer(no_args_is_help=True)


@config.command(name='list')
def cli_config_list(ctx: typer.Context) -> None:
    """List all configuration."""
    print('List configuration.')
    print(ctx.obj.cfgfile.resolve())
