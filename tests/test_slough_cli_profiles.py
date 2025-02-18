"""Module with tests for the profile management."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from slough_cli_tool import app


@pytest.mark.parametrize(
    'profile_name',
    [
        'test_profile',
        'new_profile',
        'another_profile',
        'production',
        'acceptance',
        'development',
        'production',
    ],
)
def test_slough_cli_profiles_add(
    cli_runner: CliRunner, empty_test_dir: Path, profile_name: str
) -> None:
    """Test the `profiles add` command.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        empty_test_dir (Path): Empty test directory.
        profile_name (str): Profile name.
    """
    cli_runner.invoke(
        app,
        [
            'project',
            'init',
            '--title',
            'test_project',
            '--version',
            '1.0.0',
            '--author-name',
            'Daryl Stark',
            '--author-email',
            'daryl@example.com',
        ],
    )
    cli_runner.invoke(app, ['profiles', 'add', profile_name])
    result = cli_runner.invoke(app, ['profiles', 'list'])
    assert profile_name in result.stdout


def test_slough_cli_profiles_list(
    monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner
) -> None:
    """Test the `profiles list` command.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        cli_runner (CliRunner): Typer CLI runner.
    """
    monkeypatch.chdir('tests/test_data/project7/')
    result = cli_runner.invoke(app, ['profiles', 'list'])
    assert 'production' in result.stdout
    assert 'acceptance' in result.stdout
    assert 'development' in result.stdout


@pytest.mark.parametrize(
    'profile_name',
    [
        'test_profile',
        'new_profile',
        'another_profile',
        'production',
        'acceptance',
        'development',
        'production',
    ],
)
def test_slough_cli_profiles_remove(
    cli_runner: CliRunner,
    empty_test_dir: Path,
    profile_name: str,
) -> None:
    """Test the `profiles remove` command.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        empty_test_dir (Path): Empty test directory.
        profile_name (str): Profile name.
    """
    # Create a project
    cli_runner.invoke(
        app,
        [
            'project',
            'init',
            '--title',
            'test_project',
            '--version',
            '1.0.0',
            '--author-name',
            'Daryl Stark',
            '--author-email',
            'daryl@example.com',
        ],
    )

    # Add a profile
    cli_runner.invoke(app, ['profiles', 'add', profile_name])
    result = cli_runner.invoke(app, ['profiles', 'list'])
    assert profile_name in result.stdout

    # Remove the profile
    cli_runner.invoke(app, ['profiles', 'remove', profile_name])

    # Check if the profile is removed
    result = cli_runner.invoke(app, ['profiles', 'list'])
    assert profile_name not in result.stdout


@pytest.mark.parametrize(
    'profile_name, new_name',
    [
        ('production', 'test_name'),
        ('acceptance', 'test_name'),
        ('development', 'test_name'),
    ],
)
def test_slough_cli_profiles_rename(
    monkeypatch: pytest.MonkeyPatch,
    cli_runner: CliRunner,
    profile_name: str,
    new_name: str,
) -> None:
    """Test the `profiles rename` command.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        cli_runner (CliRunner): Typer CLI runner.
        profile_name (str): Profile name.
        new_name (str): New profile name.
    """
    monkeypatch.chdir('tests/test_data/project7/')
    cli_runner.invoke(app, ['profiles', 'rename', profile_name, new_name])
    result = cli_runner.invoke(app, ['profiles', 'list'])
    assert new_name in result.stdout

    cli_runner.invoke(app, ['profiles', 'rename', new_name, profile_name])
