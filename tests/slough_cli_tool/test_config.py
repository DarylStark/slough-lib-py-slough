"""Test for `config` part of the CLI tool."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from slough_cli_tool import app


@pytest.mark.parametrize(
    'profile',
    [
        '_default',
        'my_test_profile',
    ],
)
def test_config_list(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, profile: str
) -> None:
    """Test the `config list` command.

    Args:
        cli_runner (CliRunner): The CLI runner.
        temp_folder_with_slough_config (Path): Temporary folder for testing.
        profile (str): The profile to test.
    """
    result = cli_runner.invoke(
        app,
        ['config', 'list', '--profile', profile],
    )
    assert result.exit_code == 0
    for index in range(0, 4):
        assert f'slough.configuration.container.tag.{index}' in result.stdout
    assert 'slough.configuration.container.tags' in result.stdout
    assert 'slough.configuration.container.tag.count' in result.stdout
    assert 'slough.development_environment' in result.stdout
    assert 'slough.configuration.container.platforms.count' in result.stdout


def test_config_list_without_dev_environment(
    cli_runner: CliRunner,
    temp_folder_with_slough_config_no_dev_env: Path,
) -> None:
    """Test the `config list` command.

    Args:
        cli_runner (CliRunner): The CLI runner.
        temp_folder_with_slough_config_no_dev_env (Path): Temporary folder for
            testing.
    """
    result = cli_runner.invoke(
        app,
        ['config', 'list'],
    )
    assert result.exit_code == 0
    assert 'slough.development_environment' not in result.stdout


def test_config_list_as_env(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path
) -> None:
    """Test the `config list` command with environment output.

    Args:
        cli_runner (CliRunner): The CLI runner.
        temp_folder_with_slough_config (Path): Temporary folder for testing.
    """
    result = cli_runner.invoke(
        app,
        ['--output', 'env', 'config', 'list'],
    )
    assert result.exit_code == 0
    for index in range(0, 3):
        assert f'SLOUGH_CONFIGURATION_CONTAINER_TAG_{index}' in result.stdout
    assert 'SLOUGH_CONFIGURATION_CONTAINER_TAGS' in result.stdout
    assert 'SLOUGH_CONFIGURATION_CONTAINER_TAG_COUNT' in result.stdout
    assert 'SLOUGH_DEVELOPMENT_ENVIRONMENT' in result.stdout


def test_config_list_as_exported_env(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path
) -> None:
    """Test the `config list` command with exporeted environment output.

    Args:
        cli_runner (CliRunner): The CLI runner.
        temp_folder_with_slough_config (Path): Temporary folder for testing.
    """
    result = cli_runner.invoke(
        app,
        ['--output', 'exported-env', 'config', 'list'],
    )
    assert result.exit_code == 0
    for index in range(0, 3):
        assert (
            f'export SLOUGH_CONFIGURATION_CONTAINER_TAG_{index}='
            in result.stdout
        )
    assert 'export SLOUGH_CONFIGURATION_CONTAINER_TAGS=' in result.stdout
    assert 'export SLOUGH_CONFIGURATION_CONTAINER_TAG_COUNT=' in result.stdout
    assert 'export SLOUGH_DEVELOPMENT_ENVIRONMENT=' in result.stdout


@pytest.mark.parametrize(
    'prefix',
    ['slough', 'test_prefix', 'test.prefix', 'TEST', 'TEST_PREFIX'],
)
def test_config_list_custom_prefixes(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, prefix: str
) -> None:
    """Test the `config list` command.

    Args:
        cli_runner (CliRunner): The CLI runner.
        temp_folder_with_slough_config (Path): Temporary folder for testing.
        prefix (str): The prefix to test.
    """
    result = cli_runner.invoke(
        app,
        ['config', 'list', '--prefix', prefix],
    )
    assert result.exit_code == 0
    assert f'{prefix}.project.name' in result.stdout
