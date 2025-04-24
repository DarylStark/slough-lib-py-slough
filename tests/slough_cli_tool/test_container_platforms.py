"""Tests for the `container platforms` part of the CLI tool."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from slough_cli_tool import app


@pytest.mark.parametrize(
    'platform',
    [
        'linux/amd64',
        'linux/arm64',
        'linux/arm/v7',
    ],
)
def test_adding_platform_to_default_profile(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, platform: str
) -> None:
    """Test adding a container platform to the default profile.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        platform (str): Platform name to add.
    """
    cli_runner.invoke(
        app,
        [
            'container',
            'platforms',
            'add',
            platform,
        ],
    )

    result = cli_runner.invoke(
        app,
        [
            'container',
            'platforms',
            'list',
        ],
    )
    assert platform in result.stdout

    result = cli_runner.invoke(
        app, ['container', 'platforms', 'list', '--profile', '_default']
    )
    assert platform in result.stdout


@pytest.mark.parametrize(
    'platform',
    [
        'linux/amd64',
        'linux/arm64',
        'linux/arm/v7',
    ],
)
@pytest.mark.parametrize(
    'profile',
    [
        'production',
        'acceptance',
        'development',
    ],
)
def test_add_platforms_to_random_profiles(
    cli_runner: CliRunner,
    temp_folder_with_slough_config: Path,
    platform: str,
    profile: str,
) -> None:
    """Test adding a container platform to other profiles.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        platform (str): Platform name to add.
        profile (str): Profile name
    """
    cli_runner.invoke(app, ['profiles', 'add', profile])
    cli_runner.invoke(
        app,
        ['container', 'platforms', 'add', platform, '--profile', profile],
    )

    result = cli_runner.invoke(
        app, ['container', 'platforms', 'list', '--profile', profile]
    )
    assert platform in result.stdout


@pytest.mark.parametrize(
    'platforms',
    [
        ['linux/amd64', 'linux/arm64'],
        ['linux/arm/v7', 'linux/arm/v6'],
        ['linux/ppc64le', 'linux/s390x', 'linux/386'],
    ],
)
@pytest.mark.parametrize(
    'profile',
    [
        'production',
        'acceptance',
        'development',
    ],
)
def test_add_multiple_platforms_to_random_profiles(
    cli_runner: CliRunner,
    temp_folder_with_slough_config: Path,
    platforms: list[str],
    profile: str,
) -> None:
    """Test adding a container platform to other profiles.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        platforms (list[str]): Platforms to add.
        profile (str): Profile name
    """
    cli_runner.invoke(app, ['profiles', 'add', profile])
    cli_runner.invoke(
        app,
        ['container', 'platforms', 'add', *platforms, '--profile', profile],
    )

    result = cli_runner.invoke(
        app, ['container', 'platforms', 'list', '--profile', profile]
    )
    for platform in platforms:
        assert platform in result.stdout


@pytest.mark.parametrize(
    'platform', ['linux/amd64', 'linux/arm64', 'linux/arm/v7']
)
def test_add_platforms_multiple_times(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, platform: str
) -> None:
    """Test adding a container platform to other profiles.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        platform (str): Platform name to add.
    """
    for _ in range(5):
        cli_runner.invoke(
            app,
            ['container', 'platforms', 'add', platform],
        )

    result = cli_runner.invoke(app, ['container', 'platforms', 'list'])
    assert result.stdout.count(platform) == 1


@pytest.mark.parametrize(
    'platform',
    [
        'linux/amd64',
        'linux/arm64',
        'linux/arm/v7',
    ],
)
def test_add_platforms_to_all_profile(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, platform: str
) -> None:
    """Test adding a container platforms to the `_all` profile.

    It should only be listed once.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        platform (str): Platform name to add.
    """
    cli_runner.invoke(
        app,
        ['container', 'platforms', 'add', platform, '--profile', '_all'],
    )

    result = cli_runner.invoke(
        app, ['container', 'platforms', 'list', '--profile', '_all']
    )
    assert result.stdout.count(platform) == 1


def test_listing_platforms(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path
) -> None:
    """Test listing all container platforms.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
    """
    cli_runner.invoke(
        app,
        [
            'container',
            'platforms',
            'add',
            'linux/386',
            'linux/amd64',
            'linux/arm64',
        ],
    )
    result = cli_runner.invoke(app, ['container', 'platforms', 'list'])
    assert 'linux/386' in result.stdout
    assert 'linux/amd64' in result.stdout
    assert 'linux/arm64' in result.stdout


@pytest.mark.parametrize(
    'platform', ['linux/386', 'linux/amd64', 'linux/arm64']
)
def test_removing_a_single_platform(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, platform: str
) -> None:
    """Test removing container platforms.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        platform (str): Platform name to remove.
    """
    cli_runner.invoke(
        app,
        ['container', 'platforms', 'add', platform],
    )
    result = cli_runner.invoke(app, ['container', 'platforms', 'list'])
    assert platform in result.stdout

    cli_runner.invoke(app, ['container', 'platforms', 'remove', platform])
    result = cli_runner.invoke(app, ['container', 'platforms', 'list'])
    assert platform not in result.stdout


@pytest.mark.parametrize(
    'platforms',
    [
        ['linux/amd64', 'linux/arm64'],
        ['linux/arm/v7', 'linux/arm/v6'],
        ['linux/ppc64le', 'linux/s390x', 'linux/386'],
    ],
)
def test_removing_multiple_platforms(
    cli_runner: CliRunner,
    temp_folder_with_slough_config: Path,
    platforms: list[str],
) -> None:
    """Test removing container platforms.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        platforms (list[str]): Platforms to remove.
    """
    cli_runner.invoke(
        app,
        ['container', 'platforms', 'add', *platforms],
    )
    result = cli_runner.invoke(app, ['container', 'platforms', 'list'])
    for platform in platforms:
        assert platform in result.stdout

    cli_runner.invoke(app, ['container', 'platforms', 'remove', *platforms])
    result = cli_runner.invoke(app, ['container', 'platforms', 'list'])
    for platform in platforms:
        assert platform not in result.stdout
