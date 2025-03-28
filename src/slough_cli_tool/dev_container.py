"""Dev Container part of the CLI tool."""

from pathlib import Path

import typer

from dev_container_gen import DevContainer, Loader, Saver
from slough import Slough
from slough_cli_tool.exceptions import (
    DevelopmentEnvironmentNotSetError,
)
from slough_config import DevelopmentEnvironment as DevEnv

dev_container = typer.Typer(no_args_is_help=True)

# Dictionary with all images for specific Dev Containers
DEV_CONTAINER_IMAGES = {
    DevEnv.CPP_GENERIC: 'dast1986/slough-dev-dc-cpp:{tag}',
    DevEnv.NODEJS_GENERIC: 'dast1986/slough-dev-dc-nodejs:{tag}',
    DevEnv.PYTHON_GENERIC: 'dast1986/slough-dev-dc-python:{tag}',
    DevEnv.RUST_GENERIC: 'dast1986/slough-dev-dc-rust:{tag}',
    DevEnv.GENERIC: 'dast1986/slough-dev-dc-generic-base:{tag}',
}


@dev_container.command(
    name='generate-config',
    help='Initialize configuration for a dev container. This uses the '
    + '"dev-environment" value from the Slough configuration file to choose '
    + 'a specific container image.',
    short_help='Initialize a new project configuration.',
)
def cli_dev_container_generate_config(
    ctx: typer.Context,
    name: str | None = typer.Option(
        default=None,
        help='The name for the dev container',
    ),
    container_tag: str = typer.Option(
        default='latest',
        help='The tag for the dev container. Useful if you want a specific '
        + 'version.',
    ),
    bind_docker_socket: bool | None = typer.Option(
        default=None,
        help='Mount the Docker socket inside the dev container. This is '
        + 'useful if you want to build Docker images inside the dev '
        + 'container.',
    ),
) -> None:
    """Initialize configuration for a dev container.

    Args:
        ctx (typer.Context): The context object.
        name (str, optional): The name for the dev container. Defaults to None.
        container_tag (str, optional): The tag for the dev container. Defaults
            to 'latest'.
        bind_docker_socket (bool, optional): Mount the Docker socket inside the
            dev container. Defaults to False.
    """
    slough: Slough = ctx.obj['slough']

    if slough.config.development_environment is None:
        raise DevelopmentEnvironmentNotSetError(
            'Development environment is not set in the Slough configuration.'
        )

    # Get the path for the dev container configuration
    config_filename = (Path() / '.devcontainer/devcontainer.json').resolve()

    # Load the current configuration
    loader = Loader(config_filename)
    dev_container_config = loader.load() or DevContainer(
        name=slough.config.project.name, image=''
    )

    # Get the correct image
    image = DEV_CONTAINER_IMAGES.get(
        slough.config.development_environment, DevEnv.GENERIC
    )
    image = image.replace('{tag}', container_tag)

    # Update the configuration
    dev_container_config.name = name or dev_container_config.name
    dev_container_config.image = image
    if bind_docker_socket:
        dev_container_config.add_docker_mount()
    elif bind_docker_socket is False:
        dev_container_config.remove_docker_mount()

    # Save the configuration
    saver = Saver(config_filename)
    saver.save(dev_container_config)
