"""Module with unit tests for the CLI app."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from slough_cli_tool import app
from slough_cli_tool.exceptions import (
    ConfigConvertionAlreadyCorrectSufficError,
)


def test_slough_cli_config_show(
    monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner
) -> None:
    """Test the `config show --output envvar` command."""
    monkeypatch.chdir('tests/test_data/project1/')
    result = cli_runner.invoke(app, ['config', 'show', '--output', 'envvars'])
    assert 'SLOUGH_PROJECT_NAME="project1"' in result.stdout
    assert 'SLOUGH_PROJECT_VERSION="0.0.1"' in result.stdout
    assert 'SLOUGH_PROJECT_AUTHORS_0_NAME="John Doe"' in result.stdout
    assert 'SLOUGH_PROJECT_AUTHORS_1_NAME="Daryl Stark"' in result.stdout


@pytest.mark.parametrize(
    'initial_file, target', [('config.yml', 'json'), ('config.json', 'yml')]
)
def test_slough_cli_config_convert(
    cli_runner: CliRunner,
    empty_test_dir: Path,
    initial_file: str,
    target: str,
) -> None:
    """Test the commando to convert configuration to specific target."""
    # Create a new project
    cli_runner.invoke(
        app,
        ['--cfgfile', initial_file, 'project', 'init'],
        input='test_project\n1.2.3\nJohn Doe\njohndoe@example.com\n',
    )

    # Convert to the target format
    cli_runner.invoke(
        app, ['--cfgfile', initial_file, 'config', 'convert', target]
    )

    # Check the new config
    new_config_file = initial_file.split('.')[0] + f'.{target}'
    result = cli_runner.invoke(
        app,
        [
            '--cfgfile',
            new_config_file,
            'config',
            'show',
            '--output',
            'envvars',
        ],
    )
    assert 'SLOUGH_PROJECT_NAME="test_project"' in result.stdout
    assert 'SLOUGH_PROJECT_VERSION="1.2.3"' in result.stdout
    assert 'SLOUGH_PROJECT_AUTHORS_0_NAME="John Doe"' in result.stdout


def test_slough_cli_config_convert_same_extension(
    monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner
) -> None:
    """Test the converting to the already used format."""
    monkeypatch.chdir('tests/test_data/project1/')
    # Convert to YAML
    result = cli_runner.invoke(app, ['config', 'convert', 'yml'])
    assert type(result.exception) is ConfigConvertionAlreadyCorrectSufficError
