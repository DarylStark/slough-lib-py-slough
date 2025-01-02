"""Config part of the CLI tool."""

import typer

from slough import Slough

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
