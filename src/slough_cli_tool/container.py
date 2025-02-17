"""Container part of the CLI tool."""

import typer

from .container_tags import tags

container = typer.Typer(no_args_is_help=True)

container.add_typer(
    tags,
    name='tags',
    help='Manage container tags in specific profiles.',
    short_help='Manage container tags.',
)
