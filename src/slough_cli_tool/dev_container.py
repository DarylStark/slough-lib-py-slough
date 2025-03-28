"""Dev Container part of the CLI tool."""

from pathlib import Path

import typer

from dev_container_gen import DevContainer, Loader, Saver
from slough import Slough
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

    dev_environment = _get_development_environment(slough)
    config_filename = _get_dev_container_config_filename()

    # TODO: Create a class for this in the backend.

    # Load the current configuration
    dev_container_config = _load_existing_configuration(
        slough, config_filename
    )

    # Get the correct image
    image = _get_container_image(container_tag, dev_environment)

    # Update the configuration
    _update_configuration(
        name, bind_docker_socket, dev_container_config, image
    )

    # Save the configuration
    _save_configuration(config_filename, dev_container_config)


def _save_configuration(
    config_filename: Path, dev_container_config: DevContainer
) -> None:
    """Saves the given development container configuration to a specified file.

    Args:
        config_filename (Path): The path to the file where the configuration
            will be saved.
        dev_container_config (DevContainer): The development container
            configuration object to save.
    """
    saver = Saver(config_filename)
    saver.save(dev_container_config)


def _get_container_image(container_tag: str, dev_environment: DevEnv) -> str:
    """Retrieves the container image name.

    Args:
        container_tag (str): The tag to be used in the container image name.
        dev_environment (DevEnv): The development environment for which the
            container image is required.

    Returns:
        str: The formatted container image name with the specified tag.
    """
    image = DEV_CONTAINER_IMAGES.get(
        dev_environment, DEV_CONTAINER_IMAGES[DevEnv.GENERIC]
    )
    image = image.replace('{tag}', container_tag)
    return image


def _update_configuration(
    name: str | None,
    bind_docker_socket: bool | None,
    dev_container_config: DevContainer,
    image: str,
) -> None:
    """Updates the development container configuration.

    Args:
        name (str | None): The name for the dev container. If None, the
            existing name in the configuration is retained.
        bind_docker_socket (bool | None): Whether to bind the Docker socket.
            If True, the Docker socket is mounted. If False, it is removed.
        dev_container_config (DevContainer): The development container
            configuration object to update.
        image (str): The container image to use in the configuration.
    """
    dev_container_config.name = name or dev_container_config.name
    dev_container_config.image = image
    if bind_docker_socket:
        dev_container_config.add_docker_mount()
    elif bind_docker_socket is False:
        dev_container_config.remove_docker_mount()


def _load_existing_configuration(
    slough: Slough, config_filename: Path
) -> DevContainer:
    """Load an existing DevContainer configuration from a file.

    If the configuration file exists, it is loaded using the Loader class.
    If the file does not exist or is empty, a default DevContainer
    configuration is created using the project name from the provided Slough
    instance.

    Args:
        slough (Slough): An instance of the Slough class containing project
            configuration.
        config_filename (Path): The path to the configuration file to be
            loaded.

    Returns:
        DevContainer: The loaded or default DevContainer configuration.
    """
    loader = Loader(config_filename)
    dev_container_config = loader.load() or DevContainer(
        name=slough.config.project.name, image=''
    )

    return dev_container_config


def _get_development_environment(slough: Slough) -> DevEnv:
    """Retrieves the development environment configuration.

    If the development environment is not explicitly configured, a generic
    development environment is returned as the default.

    Args:
        slough (Slough): An instance of the Slough class containing
            configuration details.

    Returns:
        DevEnv: The development environment configuration, or a generic
        development environment if none is specified.
    """
    return slough.config.development_environment or DevEnv.GENERIC


def _get_dev_container_config_filename() -> Path:
    """Retrieves the absolute path to the dev container configuration file.

    This function constructs the path to the `.devcontainer/devcontainer.json`
    file relative to the current working directory and resolves it to an
    absolute path.

    Returns:
        Path: The absolute path to the `devcontainer.json` file.
    """
    config_filename = (Path() / '.devcontainer/devcontainer.json').resolve()
    return config_filename
