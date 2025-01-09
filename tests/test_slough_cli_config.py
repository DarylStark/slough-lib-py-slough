"""Module with unit tests for the CLI app."""

import pytest
from typer.testing import CliRunner

from slough_cli_tool import app


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
