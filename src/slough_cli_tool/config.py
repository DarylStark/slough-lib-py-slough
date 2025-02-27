"""Config part of the CLI tool."""

import logging
from enum import Enum

import typer
import yaml

from .exceptions import (
    ConfigConvertionAlreadyCorrectSufficError,
)
from .generic import get_context_data_config

config = typer.Typer(no_args_is_help=True)


class ConvertTarget(str, Enum):
    """Targets for the convert command."""

    JSON = 'json'
    YAML = 'yml'


class SchemaTarget(str, Enum):
    """Targets for the generate-schema command."""

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
    local_logger = logging.getLogger('convert_to_envvars')
    output = ''
    for key, value in data.items():
        var_name = f'{prefix}_{key}'.upper()

        if isinstance(value, Enum):
            output += f'{var_name}="{str(value.value)}"\n'
        elif isinstance(value, str | int | float):
            output += f'{var_name}="{str(value)}"\n'
        elif isinstance(value, dict):
            output += convert_to_envvars(value, f'{prefix}_{key}')
        elif isinstance(value, list):
            if len(value) == 0:
                continue

            output += f'{var_name}_COUNT={len(value)}\n'
            if all([type(item) is str for item in value]):
                output += f'{var_name}="{','.join(value)}"\n'
            for i, item in enumerate(value):
                if isinstance(item, str | int | float):
                    output += f'{var_name}_{i}="{str(item)}"\n'
                elif isinstance(item, dict):
                    output += convert_to_envvars(item, f'{var_name}_{i}')
        else:
            local_logger.warning(
                'Cannot convert "%s", invalid type: "%s"', key, type(value)
            )

    return output


@config.command(
    name='env',
    help='Display the configuration as environment variables. This can be '
    + 'used in automations to get the configuration for the project.',
    short_help='Display the configuration as environment variables.',
)
def cli_config_env(
    ctx: typer.Context,
    prefix: str = typer.Option(
        default='SLOUGH', help='The prefix for the variables.'
    ),
    profile: str | None = typer.Option(
        None, help='Profile to use for the configuration.'
    ),
) -> None:
    """Show configuration as environment variables.

    Args:
        ctx (typer.Context): Typer context.
        prefix (str): Prefix for the environment variables
        profile (str | None): Profile to use for the configuration.
    """
    console, _, config, _ = get_context_data_config(ctx)
    config_model = config.model_dump()
    # We set the console width to 1024 to prevent line wrapping
    console.width = 1024
    console.print(convert_to_envvars(config_model, prefix), end='')


@config.command(
    name='convert',
    help='Convert the configurationfile to a different format. This can be '
    + 'useful when you need to convert a YAML file to JSON or visa versa.',
    short_help='Convert the configuration to a different format.',
)
def cli_config_convert(
    ctx: typer.Context,
    target: ConvertTarget = typer.Argument(
        help='Target format to convert to.'
    ),
) -> None:
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
    local_logger = logging.getLogger('cli_config_convert')
    local_logger.info('Converting configuration to "%s"', slough.cfgfile)
    slough.save()

    # Remove old file
    oldfile.unlink()


@config.command(
    name='generate-schema',
    help='Generate a schema for the configuration file. This can be used to '
    + 'validate the configuration file.',
    short_help='Generate a schema for the configuration file.',
)
def cli_config_generate_schema(
    ctx: typer.Context,
    target_format: SchemaTarget = typer.Option(
        SchemaTarget.JSON, help='Output format for the schema.'
    ),
) -> None:
    """Generate a schema for the configuration file.

    Args:
        ctx (typer.Context): Typer context.
        target_format (SchemaTarget): Target format.
    """
    console, _, config, _ = get_context_data_config(ctx)
    schema = config.model_json_schema()
    if target_format == SchemaTarget.JSON:
        console.print_json(data=schema)
    else:
        console.print(yaml.dump(config.model_json_schema()))
