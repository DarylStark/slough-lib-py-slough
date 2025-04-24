"""Tests for the `container set` part of the CLI tool."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from slough_cli_tool import app


@pytest.mark.parametrize(
    'registry', ['docker.io', 'localhost', 'localhost:5000']
)
def test_setting_registry(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, registry: str
) -> None:
    """Test setting the container registry.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        registry (str): Tag name to add.
    """
    cli_runner.invoke(
        app,
        [
            'container',
            'set',
            'registry',
            registry,
        ],
    )

    result = cli_runner.invoke(app, ['--output', 'env', 'config', 'list'])
    assert registry in result.stdout

    result = cli_runner.invoke(
        app, ['--output', 'env', 'config', 'list', '--profile', '_default']
    )
    assert registry in result.stdout


@pytest.mark.parametrize(
    'registry', ['docker.io', 'localhost', 'localhost:5000']
)
def test_setting_registry_in_profile(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, registry: str
) -> None:
    """Test setting the container registry in a specific profile.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        registry (str): Tag name to add.
    """
    cli_runner.invoke(
        app,
        [
            'container',
            'set',
            'registry',
            registry,
            '--profile',
            'my_test_profile',
        ],
    )

    result = cli_runner.invoke(
        app,
        ['--output', 'env', 'config', 'list', '--profile', 'my_test_profile'],
    )
    assert registry in result.stdout


@pytest.mark.parametrize(
    'image', ['my-application', 'slough', 'my__application', 'my.application']
)
def test_setting_image(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, image: str
) -> None:
    """Test setting the container image.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        image (str): Tag name to add.
    """
    cli_runner.invoke(
        app,
        [
            'container',
            'set',
            'image',
            image,
        ],
    )

    result = cli_runner.invoke(app, ['--output', 'env', 'config', 'list'])
    assert image in result.stdout

    result = cli_runner.invoke(
        app, ['--output', 'env', 'config', 'list', '--profile', '_default']
    )
    assert image in result.stdout


@pytest.mark.parametrize(
    'image', ['my-application', 'slough', 'my__application', 'my.application']
)
def test_setting_image_in_profile(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, image: str
) -> None:
    """Test setting the container image in a specific profile.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        image (str): Tag name to add.
    """
    cli_runner.invoke(
        app,
        [
            'container',
            'set',
            'image',
            image,
            '--profile',
            'my_test_profile',
        ],
    )

    result = cli_runner.invoke(
        app,
        ['--output', 'env', 'config', 'list', '--profile', 'my_test_profile'],
    )
    assert image in result.stdout
