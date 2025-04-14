"""Module with unit tests for the `project` portion of the CLI app."""

from pathlib import Path

from typer.testing import CliRunner

from slough_cli_tool import app
from slough_cli_tool.exceptions import ConfigAlreadySetError


def test_slough_cli_project_init_prompt_input(
    cli_runner: CliRunner, temp_folder: Path
) -> None:
    """Test the `project init` command.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder (Path): Temporary folder for testing.
    """
    result = cli_runner.invoke(
        app,
        ['project', 'init'],
        input=(
            'test_project\n'
            + '0.1.0\n'
            + 'John Doe\n'
            + 'johndoe@example.com\n'
        ),
    )
    assert result.exit_code == 0

    # Test if the `slough.yml` file is created
    config_file = temp_folder / 'slough.yml'
    assert config_file.exists()

    # Check if it contains the correct values
    with open(config_file) as file:
        config = file.read()
    assert 'name: test_project' in config
    assert 'version: 0.1.0' in config


def test_slough_cli_project_init_cmdline_input(
    cli_runner: CliRunner, temp_folder: Path
) -> None:
    """Test the `project init` command.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder (Path): Temporary folder for testing.
    """
    result = cli_runner.invoke(
        app,
        [
            'project',
            'init',
            '--title',
            'test_project',
            '--version',
            '0.1.0',
            '--author-name',
            'John Doe',
            '--author-email',
            'johndoe@example.com',
            '--development-environment',
            'python-generic',
        ],
    )
    assert result.exit_code == 0

    # Test if the `slough.yml` file is created
    config_file = temp_folder / 'slough.yml'
    assert config_file.exists()

    # Check if it contains the correct values
    with open(config_file) as file:
        config = file.read()
    assert 'name: test_project' in config
    assert 'version: 0.1.0' in config


def test_slough_cli_project_init_config_already_present(
    temp_folder_with_slough_config: Path, cli_runner: CliRunner
) -> None:
    """Test the `project init` command when there is already a config.

    Args:
        temp_folder_with_slough_config (Path): Temporary folder with slough
            config for testing.
        cli_runner (CliRunner): Typer CLI runner.
    """
    result = cli_runner.invoke(
        app,
        [
            'project',
            'init',
            '--title',
            'test_project',
            '--version',
            '0.1.0',
            '--author-name',
            'John Doe',
            '--author-email',
            'johndoe@example.com',
        ],
    )
    assert result.exit_code == 1
    assert type(result.exception) is ConfigAlreadySetError
