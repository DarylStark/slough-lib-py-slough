"""Module with unit tests for the `project` portion of the CLI app."""

from pathlib import Path

from typer.testing import CliRunner

from slough_cli_tool import app


def test_slough_cli_project_set_development_environment_when_empty(
    cli_runner: CliRunner, empty_test_dir: Path
) -> None:
    """Test the `project set-development-environment` command.

    Assumes the development environment is not set.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        empty_test_dir (Path): Path to the empty test directory.
    """
    # First, we create a new project configuration
    result = cli_runner.invoke(
        app,
        ['--cfgfile', 'slough.yml', 'project', 'init'],
        input=(
            'test_project\n'
            + '0.1.0\n'
            + 'John Doe\n'
            + 'johndoe@example.com\n'
        ),
    )

    # Set the development environment
    result = cli_runner.invoke(
        app,
        [
            '--cfgfile',
            'slough.yml',
            'project',
            'set-development-environment',
            'python-generic',
        ],
    )

    # Check the new value
    result = cli_runner.invoke(
        app, ['--cfgfile', 'slough.yml', 'config', 'env']
    )
    assert 'SLOUGH_DEVELOPMENT_ENVIRONMENT="python-generic"' in result.stdout


def test_slough_cli_project_set_development_environment_when_not_empty(
    cli_runner: CliRunner, empty_test_dir: Path
) -> None:
    """Test the `project set-development-environment` command.

    Assumes the development environment is already set.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        empty_test_dir (Path): Path to the empty test directory.
    """
    # First, we create a new project configuration
    result = cli_runner.invoke(
        app,
        [
            '--cfgfile',
            'slough.yml',
            'project',
            'init',
            '--development-environment',
            'python-generic',
        ],
        input=(
            'test_project\n'
            + '0.1.0\n'
            + 'John Doe\n'
            + 'johndoe@example.com\n'
        ),
    )

    # Set the development environment
    result = cli_runner.invoke(
        app,
        [
            '--cfgfile',
            'slough.yml',
            'project',
            'set-development-environment',
            'nodejs-generic',
        ],
    )

    # Check the new value
    result = cli_runner.invoke(
        app, ['--cfgfile', 'slough.yml', 'config', 'env']
    )
    assert 'SLOUGH_DEVELOPMENT_ENVIRONMENT="nodejs-generic"' in result.stdout
