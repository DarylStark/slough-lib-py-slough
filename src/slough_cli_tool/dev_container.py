"""Dev Container part of the CLI tool."""

import json

import typer

from slough_cli_tool.exceptions import ConfigMissingError
from slough_config import DevelopmentEnvironment as DevEnv

from .generic import get_context_data

dev_container = typer.Typer(no_args_is_help=True)

# Dictionary with all images for specific Dev Containers
DEV_CONTAINER_IMAGES = {
    DevEnv.CPP_GENERIC: 'dast1986/slough-dev-dc-cpp:latest',
    DevEnv.NODEJS_GENERIC: 'dast1986/slough-dev-dc-nodejs:latest',
    DevEnv.PYTHON_GENERIC: 'dast1986/slough-dev-dc-python:latest',
    DevEnv.RUST_GENERIC: 'dast1986/slough-dev-dc-rust:latest',
}


@dev_container.command(
    name='generate-config',
    help='Initialize configuration for a dev container. This uses the '
    + '"dev-environment" value from the Slough configuration file to choose '
    + 'a specific container image.',
    short_help='Initialize a new project configuration.',
)
def cli_dev_container_generate_config(ctx: typer.Context) -> None:
    """Initialize configuration for a dev container."""
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
    ]

    # Write the updated configuration
    with open(dev_container_folder, 'w', encoding='utf-8') as outfile:
        json.dump(dev_container_config, outfile, indent=4, sort_keys=True)

    pass
