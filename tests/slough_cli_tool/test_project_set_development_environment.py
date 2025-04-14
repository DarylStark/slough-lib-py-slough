"""Module with unit tests for the `project` portion of the CLI app."""

from pathlib import Path

from typer.testing import CliRunner

from slough_cli_tool import app


def test_slough_cli_project_set_development_environment_when_empty(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path
) -> None:
    """Test the `project set-development-environment` command.

    Assumes the development environment is not set.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Temporary folder with slough
            config for testing.
    """
    # Set the development environment
    result = cli_runner.invoke(
        app,
        [
            'project',
            'set-development-environment',
            'python-generic',
        ],
    )
    assert result.exit_code == 0

    # Test if the `slough.yml` file is created
    config_file = temp_folder_with_slough_config / 'slough.yml'

    # Check if it contains the correct values
    with open(config_file) as file:
        config = file.read()
    assert 'development_environment: python-generic' in config
