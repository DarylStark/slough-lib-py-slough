"""Module with unit tests for the CLI app."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from slough_cli_tool import app
from slough_cli_tool.exceptions import (
    ConfigConvertionAlreadyCorrectSufficError,
    ConfigMissingError,
)


def test_slough_cli_config_env(
    monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner
) -> None:
    """Test the `config env` command without a profile.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        cli_runner (CliRunner): Typer CLI runner.
    """
    monkeypatch.chdir('tests/test_data/project1/')
    result = cli_runner.invoke(app, ['config', 'env'])
    assert 'SLOUGH_PROJECT_NAME="project1"' in result.stdout
    assert 'SLOUGH_PROJECT_VERSION="0.0.1"' in result.stdout
    assert 'SLOUGH_PROJECT_AUTHORS_0_NAME="John Doe"' in result.stdout
    assert 'SLOUGH_PROJECT_AUTHORS_1_NAME="Daryl Stark"' in result.stdout


def test_slough_cli_config_env_with_profile(
    monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner
) -> None:
    """Test the `config env` command with a profile.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        cli_runner (CliRunner): Typer CLI runner.
    """
    monkeypatch.chdir('tests/test_data/project7/')
    result = cli_runner.invoke(
        app, ['config', 'env', '--profile', 'production']
    )
    assert 'SLOUGH_PROJECT_NAME="project7"' in result.stdout
    assert 'SLOUGH_PROJECT_VERSION="0.0.1"' in result.stdout
    assert 'SLOUGH_PROJECT_AUTHORS_0_NAME="Daryl Stark"' in result.stdout
    assert (
        'SLOUGH_CONTAINER_TAGS="latest-image,latest-prd,my_application,1.0.0"'
        in result.stdout
    )


def test_slough_cli_config_env_with_container_tags(
    monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner
) -> None:
    """Test the `config env` command with container tags.

    This runs the command on a project with container tags.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        cli_runner (CliRunner): Typer CLI runner.
    """
    monkeypatch.chdir('tests/test_data/project7/')
    result = cli_runner.invoke(app, ['config', 'env'])
    assert 'SLOUGH_PROJECT_NAME="project7"' in result.stdout
    assert 'SLOUGH_PROJECT_VERSION="0.0.1"' in result.stdout
    assert 'SLOUGH_PROJECT_AUTHORS_0_NAME="Daryl Stark"' in result.stdout
    assert 'SLOUGH_CFG_PROFILES__ALL_CONTAINER_TAGS_COUNT=1' in result.stdout
    assert (
        'SLOUGH_CFG_PROFILES__ALL_CONTAINER_TAGS="latest-image"'
        in result.stdout
    )
    assert (
        'SLOUGH_CFG_PROFILES__ALL_CONTAINER_TAGS="latest-image"'
        in result.stdout
    )
    assert (
        'SLOUGH_CFG_PROFILES__ALL_CONTAINER_TAGS_0="latest-image"'
        in result.stdout
    )
    assert (
        'SLOUGH_CFG_PROFILES_ACCEPTANCE_CONTAINER_TAGS="latest-rc,'
        + 'my_application,1.0.0-rc1"'
        in result.stdout
    )


def test_slough_cli_config_env_different_prefix(
    monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner
) -> None:
    """Test the `config env` command.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        cli_runner (CliRunner): Typer CLI runner.
    """
    monkeypatch.chdir('tests/test_data/project1/')
    result = cli_runner.invoke(app, ['config', 'env', '--prefix', 'TEST'])
    assert 'TEST_PROJECT_NAME="project1"' in result.stdout
    assert 'TEST_PROJECT_VERSION="0.0.1"' in result.stdout
    assert 'TEST_PROJECT_AUTHORS_0_NAME="John Doe"' in result.stdout
    assert 'TEST_PROJECT_AUTHORS_1_NAME="Daryl Stark"' in result.stdout


@pytest.mark.parametrize(
    'initial_file, target', [('config.yml', 'json'), ('config.json', 'yml')]
)
def test_slough_cli_config_convert(
    cli_runner: CliRunner,
    empty_test_dir: Path,
    initial_file: str,
    target: str,
) -> None:
    """Test the commando to convert configuration to specific target.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        empty_test_dir (Path): Path to the empty test directory.
        initial_file (str): Initial config file.
        target (str): Target format.
    """
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
        ['--cfgfile', new_config_file, 'config', 'env'],
    )
    assert 'SLOUGH_PROJECT_NAME="test_project"' in result.stdout
    assert 'SLOUGH_PROJECT_VERSION="1.2.3"' in result.stdout
    assert 'SLOUGH_PROJECT_AUTHORS_0_NAME="John Doe"' in result.stdout


def test_slough_cli_config_convert_same_extension(
    monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner
) -> None:
    """Test the converting to the already used format.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        cli_runner (CliRunner): Typer CLI runner.
    """
    monkeypatch.chdir('tests/test_data/project1/')
    # Convert to YAML
    result = cli_runner.invoke(app, ['config', 'convert', 'yml'])
    assert type(result.exception) is ConfigConvertionAlreadyCorrectSufficError


def test_slough_cli_config_convert_missing_config(
    monkeypatch: pytest.MonkeyPatch,
    cli_runner: CliRunner,
    empty_test_dir: Path,
) -> None:
    """Test the converting when there is no configfile.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        cli_runner (CliRunner): Typer CLI runner.
        empty_test_dir (Path): Path to the empty test directory.
    """
    monkeypatch.setenv('MAX_DIR_DEPTH', '0')
    result = cli_runner.invoke(
        app, ['--cfgfile', '', 'config', 'convert', 'yml']
    )
    assert type(result.exception) is ConfigMissingError


def test_slough_cli_config_generate_schema_json(
    monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner
) -> None:
    """Test creating a JSON schema.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        cli_runner (CliRunner): Typer CLI runner.
    """
    result = cli_runner.invoke(
        app, ['config', 'generate-schema', '--target-format', 'json']
    )
    assert '$defs' in result.stdout


def test_slough_cli_config_generate_schema_yaml(
    monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner
) -> None:
    """Test creating a YAML schema.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        cli_runner (CliRunner): Typer CLI runner.
    """
    result = cli_runner.invoke(
        app, ['config', 'generate-schema', '--target-format', 'yml']
    )
    assert '$defs' in result.stdout
