"""Profile part of the CLI tool."""

import typer
from rich import box
from rich.console import Console
from rich.table import Table

from slough.slough import Slough

profiles = typer.Typer(no_args_is_help=True)


@profiles.command(
    name='add',
    help='Add a profile to the Slough configuration.',
    short_help='Add a profile.',
)
def add_profile(
    ctx: typer.Context,
    profile_name: str = typer.Argument(help='The profile to add'),
) -> None:
    """Adds a profile to the CLI tool.

    Args:
        ctx (typer.Context): Typer context
        profile_name (str): The profile to add.
    """
    slough: Slough = ctx.obj['slough']
    slough.add_profile(profile_name)
    slough.save()


@profiles.command(
    name='list',
    help='List all available profiles.',
    short_help='List all available profiles.',
)
def list_profiles(ctx: typer.Context) -> None:
    """List all available profiles.

    Args:
        ctx (typer.Context): Typer context
    """
    slough: Slough = ctx.obj['slough']
    console: Console = ctx.obj['console']

    table = Table(box=box.SIMPLE)
    table.add_column('Profile name')
    for profile in slough.profile_list:
        table.add_row(profile)
    console.print(table)


@profiles.command(
    name='remove',
    help='Remove a profile from the Slough configuration.',
    short_help='Remove a profile.',
)
def remove_profile(
    ctx: typer.Context,
    profile_name: str = typer.Argument(help='The profile to remove'),
) -> None:
    """Removes a profile from the CLI tool.

    Args:
        ctx (typer.Context): Typer context
        profile_name (str): The profile to remove.
    """
    slough: Slough = ctx.obj['slough']
    slough.remove_profile(profile_name)
    slough.save()


@profiles.command(
    name='rename',
    help='Rename a profile.',
    short_help='Rename a profile.',
)
def rename_profile(
    ctx: typer.Context,
    profile_name: str = typer.Argument(help='The profile to rename'),
    new_name: str = typer.Argument(help='The new name for the profile'),
) -> None:
    """Rename a profile.

    Args:
        ctx (typer.Context): Typer context
        profile_name (str): The profile to remove.
        new_name (str): The new name for the profile.
    """
    slough: Slough = ctx.obj['slough']
    slough.rename_profile(profile_name, new_name)
    slough.save()
    typer.echo(f'Profile "{profile_name}" renamed to "{new_name}".')
