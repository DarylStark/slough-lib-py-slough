"""Container tags part of the CLI tool."""

import typer
from rich import box
from rich.table import Table

from slough_cli_tool.generic import get_context_data_config
from slough_config.config_model import ContainerConfiguration

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
    console, slough, _, _ = get_context_data_config(ctx)
    for tag in tags:
        slough.add_container_tag(tag, profile_name=profile)
        console.print(f'Tag "{tag}" added to profile "{profile}".')
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
    console, _, config, _ = get_context_data_config(ctx)

    # Get data
    tags: list[tuple[str, str]] = []
    profile_set = {'_all', profile}
    for profile_name in list(profile_set):
        if (
            profile_name in config.cfg_profiles
            and config.cfg_profiles[profile_name].container
        ):
            container_object: ContainerConfiguration | None = (
                config.cfg_profiles[profile_name].container
            )
            if container_object:
                for tag in container_object.tags:
                    tags.append((tag, profile_name))

    # Print data
    if len(tags):
        table = Table(box=box.SIMPLE)
        table.add_column('Tag')
        table.add_column('Profile')
        for tag, profile_name in tags:
            table.add_row(tag, profile_name)
        console.print(table)
    else:
        console.print('There are no tags configured.')


@tags.command(
    name='remove',
    help='Remove a container tag from a specific profile.',
    short_help='Remove container tags.',
)
def remove_container_tags(
    ctx: typer.Context,
    tags: str = typer.Argument(help='The tag to remove from the profile.'),
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
    console, slough, _, _ = get_context_data_config(ctx)
    slough.remove_container_tag(tags, profile_name=profile)
    console.print(f'Tag "{tags}" removed from profile "{profile}".')
    slough.save()
