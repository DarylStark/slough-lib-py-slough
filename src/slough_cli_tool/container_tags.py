"""Container tags part of the CLI tool."""

import typer

tags = typer.Typer(no_args_is_help=True)


@tags.command(
    name='add',
    help='Add a container tag to a specific profile.',
    short_help='Add container tags.',
)
def add_container_tags(
    tags: list[str] = typer.Argument(help='The tags to add to the profile.'),
    profile: str | None = typer.Option(
        default='_default',
        help='The profile to add the container tag to.',
    ),
) -> None:
    """Adds tags to a profile.

    Args:
        tags (list[str]): The tags to add to the profile.
        profile (str, optional): The profile to add container tags for.
            Defaults to the default profile.
    """
    pass


@tags.command(
    name='list',
    help='List all available container tags with their profile. You can '
    + 'enter a profile to see all tags for that profile, including the '
    + '`_all` profile.',
    short_help='List all available container tags.',
)
def list_container_tags(
    profile: str | None = typer.Option(
        default=None,
        help='The profile to list container tags for.',
    ),
) -> None:
    """List all available container tags with their profile.

    Args:
        profile (str, optional): The profile to list container tags for.
            Defaults to None.
    """
    pass


@tags.command(
    name='remove',
    help='Remove a container tag from a specific profile.',
    short_help='Remove container tags.',
)
def remove_container_tags(
    tags: list[str] = typer.Argument(
        help='The tags to remove from the profile.'
    ),
    profile: str | None = typer.Option(
        default='_default',
        help='The profile to remove the container tags from.',
    ),
) -> None:
    """Removes tags from a profile.

    Args:
        tags (list[str]): The tags to remove from the profile.
        profile (str, optional): The profile to remove the container tags from.
            Defaults to the default profile.
    """
    pass
