"""Module with unit tests for the CLI app."""

from typer.testing import CliRunner

from slough import __version__ as slough_version
from slough_cli_tool import app


def test_slough_cli_version(cli_runner: CliRunner) -> None:
    """Test the `config show --output envvar` command."""
    result = cli_runner.invoke(app, ['version'])
    assert f'slough-cli-tool version: {slough_version}' in result.stdout
