"""Config part of the CLI tool."""

from enum import Enum

import typer

from slough import Slough

from .exceptions import (
    ConfigConvertionAlreadyCorrectSufficError,
    ConfigMissingError,
)
from .generic import raise_for_missing_config
from .output_formatters import OutputFormatter, OutputType

config = typer.Typer(no_args_is_help=True)


class ConvertTarget(str, Enum):
    """Targets for the convert command."""

    JSON = 'json'
    YAML = 'yml'


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
        raise ConfigMissingError('Configuration is missing.')

    console = context['console']
    config_dict = slough.config

    if output in OutputFormatter.formatters:
        formatter = OutputFormatter.formatters[output](config_dict)
        console.print(formatter.format(), end='')
    else:
        raise TypeError(f'Output type {output} not supported.')


@config.command(name='convert')
def cli_config_convert(ctx: typer.Context, target: ConvertTarget) -> None:
    """Convert configuration to specific output formats.

    Args:
        ctx (typer.Context): Typer context.
        target (ConvertTarget): Target format.
    """
    context = ctx.obj
    slough: Slough = context['slough']
    raise_for_missing_config(slough)
    if (
        not isinstance(slough, Slough)
        or not slough.config
        or not slough.cfgfile
    ):
        raise ConfigMissingError('Configuration is missing.')

    # Check if conversion is valid
    if (
        slough.cfgfile.suffix.lower() in ('.yaml', '.yml')
        and target == ConvertTarget.YAML
    ) or (
        slough.cfgfile.suffix.lower() == '.json'
        and target == ConvertTarget.JSON
    ):
        raise ConfigConvertionAlreadyCorrectSufficError(
            '[yellow]Configuration is already in this format.[/yellow]'
        )

    # Convert configuration
    oldfile = slough.cfgfile
    slough.cfgfile = slough.cfgfile.with_suffix(f'.{target.value}')
    slough.save()

    # Remove old file
    oldfile.unlink()
