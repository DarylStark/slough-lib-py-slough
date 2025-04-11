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
    for index in range(0, 3):
        assert f'slough.configuration.container.tag.{index}' in result.stdout
    assert 'slough.configuration.container.tags' in result.stdout
    assert 'slough.configuration.container.tag.count' in result.stdout
    assert 'slough.development_environment' in result.stdout


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
