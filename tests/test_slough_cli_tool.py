"""Module with unit tests for the CLI app."""

from typer.testing import CliRunner

from slough_cli_tool.main import app

runner = CliRunner()


def test_config_list() -> None:
    """Test the `config list` command."""
    result = runner.invoke(app, ['config', 'list'])
    assert result.exit_code == 0
    assert 'List configuration.' in result.stdout
