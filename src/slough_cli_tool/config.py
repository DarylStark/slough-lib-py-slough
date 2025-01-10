"""Config part of the CLI tool."""

from enum import Enum

import typer

from slough import Slough

from .exceptions import (
    ConfigConvertionAlreadyCorrectSufficError,
    ConfigMissingError,
)
from .generic import raise_for_missing_config

config = typer.Typer(no_args_is_help=True)


class ConvertTarget(str, Enum):
    """Targets for the convert command."""

    JSON = 'json'
    YAML = 'yml'


def convert_to_envvars(data: dict, prefix: str) -> str:
    """Format dictionary to environment variables.

    Args:
        data (dict): Dictionary to format.
        prefix (str): Prefix for the environment variables.

    Returns:
        str: Formatted data.
    """
    output = ''
    for key, value in data.items():
        var_name = f'{prefix}_{key}'.upper()

        if type(value) in [str, int, float]:
            output += f'{var_name}="{value}"\n'
        elif type(value) is dict:
            output += convert_to_envvars(value, f'{prefix}_{key}')
        elif type(value) is list:
            output += f'{var_name}_COUNT={len(value)}\n'
            for i, item in enumerate(value):
                output += convert_to_envvars(item, f'{var_name}_{i}')
    return output


@config.command(name='env')
def cli_config_env(
    ctx: typer.Context,
    prefix: str = typer.Option(default='SLOUGH'),
) -> None:
    """Show configuration as environment variables.

    Args:
        ctx (typer.Context): Typer context.
        prefix (str): Prefix for the environment variables
    """
    context = ctx.obj
    slough: Slough = context['slough']
    raise_for_missing_config(slough)
    if not isinstance(slough, Slough) or not slough.config:
        raise ConfigMissingError('Configuration is missing.')

    console = context['console']
    config_dict = slough.config
    console.print(convert_to_envvars(config_dict.model_dump(), prefix), end='')


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
