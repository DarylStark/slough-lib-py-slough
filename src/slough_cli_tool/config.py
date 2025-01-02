"""Config part of the CLI tool."""

from enum import Enum

import typer
import yaml

from slough import Slough

from .generic import raise_for_missing_config

config = typer.Typer(no_args_is_help=True)


class OutputType(str, Enum):
    """Output type for the configuration."""

    json = 'json'
    yaml = 'yaml'


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

    if output == OutputType.json:
        console.print(config_dict.model_dump_json(indent=4))
    elif output == OutputType.yaml:
        console.print(
            yaml.dump(
                config_dict.model_dump(),
                default_flow_style=False,
                sort_keys=False,
            )
        )
