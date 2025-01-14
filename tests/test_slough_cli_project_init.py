"""Module with unit tests for the CLI app."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from slough_cli_tool import app


@pytest.mark.parametrize(
    'configfile',
    [
        'test.yml',
        'test.json',
        'subdir/test.yml',
        'subdir/test.json',
        'subdir/subdir/test.yml',
        'subdir/subdir/test.json',
    ],
)
def test_slough_cli_project_init_prompt_input(
    cli_runner: CliRunner, empty_test_dir: Path, configfile: str
) -> None:
    """Test the `project init` command."""
    result = cli_runner.invoke(
        app,
        ['--cfgfile', configfile, 'project', 'init'],
        input=(
            'test_project\n'
            + '0.1.0\n'
            + 'John Doe\n'
            + 'johndoe@example.com\n'
        ),
    )
    assert result.exit_code == 0

    result = cli_runner.invoke(app, ['--cfgfile', configfile, 'config', 'env'])
    assert 'SLOUGH_PROJECT_NAME="test_project"' in result.stdout
    assert 'SLOUGH_PROJECT_VERSION="0.1.0"' in result.stdout
    assert 'SLOUGH_PROJECT_AUTHORS_0_NAME="John Doe"' in result.stdout
    assert (
        'SLOUGH_PROJECT_AUTHORS_0_EMAIL="johndoe@example.com"' in result.stdout
    )


@pytest.mark.parametrize(
    'configfile',
    [
        'test.yml',
        'test.json',
        'subdir/test.yml',
        'subdir/test.json',
        'subdir/subdir/test.yml',
        'subdir/subdir/test.json',
    ],
)
def test_slough_cli_project_init_cmdline_input(
    cli_runner: CliRunner, empty_test_dir: Path, configfile: str
) -> None:
    """Test the `project init` command."""
    result = cli_runner.invoke(
        app,
        [
            '--cfgfile',
            configfile,
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
    assert result.exit_code == 0

    result = cli_runner.invoke(app, ['--cfgfile', configfile, 'config', 'env'])
    assert 'SLOUGH_PROJECT_NAME="test_project"' in result.stdout
    assert 'SLOUGH_PROJECT_VERSION="0.1.0"' in result.stdout
    assert 'SLOUGH_PROJECT_AUTHORS_0_NAME="John Doe"' in result.stdout
    assert (
        'SLOUGH_PROJECT_AUTHORS_0_EMAIL="johndoe@example.com"' in result.stdout
    )
