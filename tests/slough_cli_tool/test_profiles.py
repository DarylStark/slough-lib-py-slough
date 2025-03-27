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
        'my-profile',
        'another_profile-with-dashes',
    ],
)
def test_slough_cli_profiles_add(
    cli_runner: CliRunner, temp_folder: Path, profile_name: str
) -> None:
    """Test the `profiles add` command.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder (Path): Temporary folder for testing.
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
    result_add = cli_runner.invoke(app, ['profiles', 'add', profile_name])
    assert result_add.exit_code == 0
    result_list = cli_runner.invoke(app, ['profiles', 'list'])
    assert profile_name in result_list.stdout


@pytest.mark.parametrize(
    'profile_name',
    ['production', 'acceptance', 'development'],
)
def test_slough_cli_profiles_add_existing_profile(
    cli_runner: CliRunner,
    temp_folder: Path,
    profile_name: str,
) -> None:
    """Test the `profiles add` command with a profile that already exists.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder (Path): Temporary folder for testing.
        profile_name (str): Profile name.
    """
    _ = cli_runner.invoke(app, ['profiles', 'add', profile_name])
    result = cli_runner.invoke(app, ['profiles', 'add', profile_name])
    assert result.exit_code == 1
    assert type(result.exception) is ValueError


@pytest.mark.parametrize(
    'profile_name',
    ['_all', '_default', '1test', 'with spaces', 'with.dots', 'with,commas'],
)
def test_slough_cli_profiles_add_invalid_profile(
    cli_runner: CliRunner,
    temp_folder: Path,
    profile_name: str,
) -> None:
    """Test the `profiles add` command with a invalid profile name.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder (Path): Temporary folder for testing.
        profile_name (str): Profile name.
    """
    result = cli_runner.invoke(app, ['profiles', 'add', profile_name])
    assert result.exit_code == 1
    assert type(result.exception) is ValueError


def test_slough_cli_profiles_list(
    cli_runner: CliRunner,
    temp_folder: Path,
) -> None:
    """Test the `profiles list` command.

    Args:
        temp_folder (Path): Temporary folder for testing.
        cli_runner (CliRunner): Typer CLI runner.
    """
    for profile_name in [
        'production',
        'acceptance',
        'development',
    ]:
        cli_runner.invoke(app, ['profiles', 'add', profile_name])
    result = cli_runner.invoke(app, ['profiles', 'list'])
    assert '_all' in result.stdout
    assert '_default' in result.stdout
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
    temp_folder: Path,
    profile_name: str,
) -> None:
    """Test the `profiles remove` command.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder (Path): Temporary folder for testing.
        profile_name (str): Profile name.
    """
    cli_runner.invoke(app, ['profiles', 'add', profile_name])
    cli_runner.invoke(app, ['profiles', 'remove', profile_name])
    result = cli_runner.invoke(app, ['profiles', 'list'])
    assert profile_name not in result.stdout


@pytest.mark.parametrize(
    'profile_name',
    ['_all', '_default'],
)
def test_slough_cli_profiles_remove_default_profile(
    cli_runner: CliRunner, temp_folder: Path, profile_name: str
) -> None:
    """Test the `profiles remove` command with the default profile.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder (Path): Temporary folder for testing.
        profile_name (str): Profile name.
    """
    result = cli_runner.invoke(app, ['profiles', 'remove', profile_name])
    assert result.exit_code == 1
    assert type(result.exception) is ValueError


@pytest.mark.parametrize(
    'profile_name',
    ['non-existing-profile', 'my_profile', 'another_profile'],
)
def test_slough_cli_profiles_remove_non_existing_profile(
    cli_runner: CliRunner, temp_folder: Path, profile_name: str
) -> None:
    """Test the `profiles remove` command with a non-existing profile.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder (Path): Temporary folder for testing.
        profile_name (str): Profile name.
    """
    result = cli_runner.invoke(app, ['profiles', 'remove', profile_name])
    assert result.exit_code == 1
    assert type(result.exception) is ValueError


@pytest.mark.parametrize(
    'profile_name, new_name',
    [
        ('production', 'test_name'),
        ('acceptance', 'test_name'),
        ('development', 'test_name'),
    ],
)
def test_slough_cli_profiles_rename(
    cli_runner: CliRunner,
    temp_folder: Path,
    profile_name: str,
    new_name: str,
) -> None:
    """Test the `profiles rename` command.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder (Path): Temporary folder for testing.
        profile_name (str): Profile name.
        new_name (str): New profile name.
    """
    cli_runner.invoke(app, ['profiles', 'add', profile_name])
    cli_runner.invoke(app, ['profiles', 'rename', profile_name, new_name])
    result = cli_runner.invoke(app, ['profiles', 'list'])
    assert new_name in result.stdout


@pytest.mark.parametrize(
    'profile_name, new_name',
    [
        ('production', 'acceptance'),
        ('acceptance', 'development'),
        ('development', 'production'),
    ],
)
def test_slough_cli_profiles_rename_to_existing(
    cli_runner: CliRunner,
    temp_folder: Path,
    profile_name: str,
    new_name: str,
) -> None:
    """Test the `profiles rename` command.

    Ranames the profile to a existing profile name. Should fail.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder (Path): Temporary folder for testing.
        profile_name (str): Profile name.
        new_name (str): New profile name.
    """
    cli_runner.invoke(app, ['profiles', 'add', profile_name])
    cli_runner.invoke(app, ['profiles', 'add', new_name])

    result = cli_runner.invoke(
        app, ['profiles', 'rename', profile_name, new_name]
    )
    assert result.exit_code == 1
    assert type(result.exception) is ValueError
