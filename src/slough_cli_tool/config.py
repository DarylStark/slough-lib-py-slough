"""Config part of the CLI tool."""

from enum import Enum

import typer

from .exceptions import (
    ConfigConvertionAlreadyCorrectSufficError,
)
from .generic import get_context_data_config

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


@config.command(
    name='env',
    help='Display the configuration as environment variables. This can be '
    + 'used in automations to get the configuration for the project.',
    short_help='Display the configuration as environment variables.',
)
def cli_config_env(
    ctx: typer.Context,
    prefix: str = typer.Option(default='SLOUGH'),
) -> None:
    """Show configuration as environment variables.

    Args:
        ctx (typer.Context): Typer context.
        prefix (str): Prefix for the environment variables
    """
    console, _, config, _ = get_context_data_config(ctx)
    console.print(convert_to_envvars(config.model_dump(), prefix), end='')


@config.command(
    name='convert',
    help='Convert the configurationfile to a different format. This can be '
    + 'useful when you need to convert a YAML file to JSON or visa versa.',
    short_help='Convert the configuration to a different format.',
)
def cli_config_convert(ctx: typer.Context, target: ConvertTarget) -> None:
    """Convert configuration to specific output formats.

    Args:
        ctx (typer.Context): Typer context.
        target (ConvertTarget): Target format.
    """
    _, slough, _, cfgfile = get_context_data_config(ctx)

    # Check if conversion is valid
    if (
        cfgfile.suffix.lower() in ('.yaml', '.yml')
        and target == ConvertTarget.YAML
    ) or (cfgfile.suffix.lower() == '.json' and target == ConvertTarget.JSON):
        raise ConfigConvertionAlreadyCorrectSufficError(
            '[yellow]Configuration is already in this format.[/yellow]'
        )

    # Convert configuration
    oldfile = cfgfile
    slough.cfgfile = cfgfile.with_suffix(f'.{target.value}')
    slough.save()

    # Remove old file
    oldfile.unlink()
