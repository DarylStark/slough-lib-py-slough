"""Config part of the CLI tool."""

import typer

config = typer.Typer(no_args_is_help=True)


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
    raise NotImplementedError('Not implemented yet')
