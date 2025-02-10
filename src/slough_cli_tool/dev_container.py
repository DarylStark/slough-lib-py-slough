"""Dev Container part of the CLI tool."""

import json

import typer

from slough_cli_tool.exceptions import ConfigMissingError
from slough_config import DevelopmentEnvironment as DevEnv

from .generic import get_context_data

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
    console, slough = get_context_data(ctx)

    if slough.config is None or slough.config.development_environment is None:
        raise ConfigMissingError('Configuration is missing.')

    dev_container_folder = (
        slough.project_folder / '.devcontainer' / 'devcontainer.json'
    )

    # Load the current configuration
    try:
        with open(dev_container_folder, encoding='utf-8') as infile:
            dev_container_config = json.load(infile)
    except FileNotFoundError:
        dev_container_config = {}

    # Update the configuration with the new image
    dev_container_config['image'] = DEV_CONTAINER_IMAGES[
        slough.config.development_environment
    ].replace('{tag}', container_tag)

    # Update the name
    if name is not None:
        dev_container_config['name'] = name

    # Update the Docker socket binding
    docker_mount = (
        'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind'
    )
    if bind_docker_socket:
        if docker_mount not in dev_container_config.get('mounts', []):
            dev_container_config['mounts'] = dev_container_config.get(
                'mounts', []
            ) + [docker_mount]
    elif bind_docker_socket is False:
        dev_container_config['mounts'] = [
            mount
            for mount in dev_container_config.get('mounts', [])
            if mount != docker_mount
        ]
    if len(dev_container_config.get('mounts', [])) == 0:
        dev_container_config.pop('mounts', None)

    # Make sure the folder exists
    dev_container_folder.parent.mkdir(parents=True, exist_ok=True)

    # Write the updated configuration
    with open(dev_container_folder, 'w', encoding='utf-8') as outfile:
        json.dump(dev_container_config, outfile, indent=4, sort_keys=True)
