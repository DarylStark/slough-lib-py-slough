"""Tests for the generation of dev container configuration."""

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from slough_cli_tool import app


def test_dev_container_generate_config_no_options(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path
) -> None:
    """Generate a dev container configuration without any options.

    Args:
        cli_runner (CliRunner): The CLI runner.
        temp_folder_with_slough_config (Path): Temporary folder for testing.
    """
    result = cli_runner.invoke(
        app,
        ['dev-container', 'generate-config'],
    )
    assert result.exit_code == 0

    # Get the created file
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert data['image'] == 'dast1986/slough-dev-dc-generic-base:latest'
    assert data['name'] == 'test_project'


def test_dev_container_generate_config_no_dev_environment(
    cli_runner: CliRunner, temp_folder_with_slough_config_no_dev_env: Path
) -> None:
    """Generate a dev container configuration without any options.

    Args:
        cli_runner (CliRunner): The CLI runner.
        temp_folder_with_slough_config_no_dev_env (Path): Temporary folder for
            testing.
    """
    result = cli_runner.invoke(
        app,
        ['dev-container', 'generate-config'],
    )
    assert result.exit_code == 0

    # Get the created file
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert data['image'] == 'dast1986/slough-dev-dc-generic-base:latest'
    assert data['name'] == 'test_project'


@pytest.mark.parametrize(
    'name', ['test_name', 'test_name2', 'my_dev_container']
)
def test_dev_container_generate_config_with_name(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, name: str
) -> None:
    """Generate a dev container configuration with a name.

    Args:
        cli_runner (CliRunner): The CLI runner.
        temp_folder_with_slough_config (Path): Temporary folder for testing.
        name (str): The name of the dev container.
    """
    result = cli_runner.invoke(
        app,
        ['dev-container', 'generate-config', '--name', name],
    )
    assert result.exit_code == 0

    # Get the created file
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert data['image'] == 'dast1986/slough-dev-dc-generic-base:latest'
    assert data['name'] == name


@pytest.mark.parametrize('tag', ['test_tag', 'latest', '1.2.3', '4.3.2-rc0'])
def test_dev_container_generate_config_with_tag(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, tag: str
) -> None:
    """Generate a dev container configuration with a tag.

    Args:
        cli_runner (CliRunner): The CLI runner.
        temp_folder_with_slough_config (Path): Temporary folder for testing.
        tag (str): The tag of the dev container.
    """
    result = cli_runner.invoke(
        app,
        ['dev-container', 'generate-config', '--container-tag', tag],
    )
    assert result.exit_code == 0

    # Get the created file
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert data['image'] == f'dast1986/slough-dev-dc-generic-base:{tag}'


def test_dev_container_generate_config_with_docker_mount(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path
) -> None:
    """Generate a dev container configuration with a Docker mount.

    Args:
        cli_runner (CliRunner): The CLI runner.
        temp_folder_with_slough_config (Path): Temporary folder for testing.
    """
    result = cli_runner.invoke(
        app,
        ['dev-container', 'generate-config', '--bind-docker-socket'],
    )
    assert result.exit_code == 0

    # Get the created file
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert data['mounts'] == [
        'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind'
    ]


def test_dev_container_generate_config_without_docker_mount(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path
) -> None:
    """Generate a dev container configuration with a Docker mount.

    Args:
        cli_runner (CliRunner): The CLI runner.
        temp_folder_with_slough_config (Path): Temporary folder for testing.
    """
    result = cli_runner.invoke(
        app,
        ['dev-container', 'generate-config', '--no-bind-docker-socket'],
    )
    assert result.exit_code == 0

    # Get the created file
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert 'mounts' not in data


def test_dev_container_generate_config_remove_docker_mount(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path
) -> None:
    """Generate a dev container configuration with a Docker mount.

    Args:
        cli_runner (CliRunner): The CLI runner.
        temp_folder_with_slough_config (Path): Temporary folder for testing.
    """
    cli_runner.invoke(
        app,
        ['dev-container', 'generate-config', '--bind-docker-socket'],
    )

    result = cli_runner.invoke(
        app,
        ['dev-container', 'generate-config', '--no-bind-docker-socket'],
    )
    assert result.exit_code == 0

    # Get the created file
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert 'mounts' not in data
