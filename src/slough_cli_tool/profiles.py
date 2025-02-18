"""Profile part of the CLI tool."""

import typer

profiles = typer.Typer(no_args_is_help=True)


@profiles.command(
    name='add',
    help='Add a profile to the Slough configuration.',
    short_help='Add a profile.',
)
def add_profile(
    profile_name: str = typer.Argument(help='The profile to add'),
) -> None:
    """Adds a profile to the CLI tool.

    Args:
        profile_name (str): The profile to add.
    """
    pass


@profiles.command(
    name='list',
    help='List all available profiles.',
    short_help='List all available profiles.',
)
def list_profiles() -> None:
    """List all available profiles."""
    pass


@profiles.command(
    name='remove',
    help='Remove a profile from the Slough configuration.',
    short_help='Remove a profile.',
)
def remove_profile(
    profile_name: str = typer.Argument(help='The profile to remove'),
) -> None:
    """Removes a profile from the CLI tool.

    Args:
        profile_name (str): The profile to remove.
    """
    pass


@profiles.command(
    name='rename',
    help='Rename a profile.',
    short_help='Rename a profile.',
)
def rename_profile(
    profile_name: str = typer.Argument(help='The profile to rename'),
    new_name: str = typer.Argument(help='The new name for the profile'),
) -> None:
    """Rename a profile.

    Args:
        profile_name (str): The profile to remove.
        new_name (str): The new name for the profile.
    """
    pass
