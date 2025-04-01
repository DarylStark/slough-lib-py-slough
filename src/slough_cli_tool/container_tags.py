"""Container tags part of the CLI tool."""

import rich.box
import typer
from rich.console import Console
from rich.table import Table

from slough.slough import Slough

tags = typer.Typer(no_args_is_help=True)


@tags.command(
    name='add',
    help='Add a container tag to a specific profile.',
    short_help='Add container tags.',
)
def add_container_tags(
    ctx: typer.Context,
    tags: list[str] = typer.Argument(help='The tags to add to the profile.'),
    profile: str = typer.Option(
        default='_default',
        help='The profile to add the container tag to.',
    ),
) -> None:
    """Adds tags to a profile.

    Args:
        ctx (typer.Context): Typer context
        tags (list[str]): The tags to add to the profile.
        profile (str, optional): The profile to add container tags for.
            Defaults to the default profile.
    """
    slough: Slough = ctx.obj['slough']
    slough.get_profile(profile).get_container_configuration().add_tags(tags)
    slough.save()


@tags.command(
    name='list',
    help='List all available container tags with their profile. You can '
    + 'enter a profile to see all tags for that profile, including the '
    + '`_all` profile.',
    short_help='List all available container tags.',
)
def list_container_tags(
    ctx: typer.Context,
    profile: str = typer.Option(
        default='_default',
        help='The profile to list container tags for.',
    ),
) -> None:
    """List all available container tags with their profile.

    Args:
        ctx (typer.Context): Typer context
        profile (str, optional): The profile to list container tags for.
            Defaults to None.
    """
    slough: Slough = ctx.obj['slough']
    tags = [
        (tag, '_all')
        for tag in slough.get_profile('_all')
        .get_container_configuration()
        .tags
    ]
    if profile != '_all':
        tags += [
            (tag, profile)
            for tag in slough.get_profile(profile)
            .get_container_configuration()
            .tags
        ]

    console: Console = ctx.obj['console']
    table = Table(title='Container Tags', box=rich.box.SIMPLE)
    table.add_column('Profile', justify='left', style='magenta')
    table.add_column('Tag', justify='left', style='cyan')
    for tag in tags:
        table.add_row(tag[1], tag[0])
    console.print(table)


@tags.command(
    name='remove',
    help='Remove a container tag from a specific profile.',
    short_help='Remove container tags.',
)
def remove_container_tags(
    ctx: typer.Context,
    tags: list[str] = typer.Argument(
        help='The tags to remove from the profile.'
    ),
    profile: str = typer.Option(
        default='_default',
        help='The profile to remove the container tags from.',
    ),
) -> None:
    """Removes tags from a profile.

    Args:
        ctx (typer.Context): Typer context
        tags (list[str]): The tags to remove from the profile.
        profile (str, optional): The profile to remove the container tags from.
            Defaults to the default profile.
    """
    slough: Slough = ctx.obj['slough']
    slough.get_profile(profile).get_container_configuration().remove_tags(tags)
    slough.save()
