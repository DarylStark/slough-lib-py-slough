"""Tests for the `container tags` part of the CLI tool."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from slough_cli_tool import app


@pytest.mark.parametrize('tag', ['test-tag', 'latest', 'my_app'])
def test_adding_tag_to_default_profiile(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, tag: str
) -> None:
    """Test adding a container tag to the default profile.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        tag (str): Tag name to add.
    """
    cli_runner.invoke(
        app,
        [
            'container',
            'tags',
            'add',
            tag,
        ],
    )

    result = cli_runner.invoke(app, ['container', 'tags', 'list'])
    assert tag in result.stdout

    result = cli_runner.invoke(
        app, ['container', 'tags', 'list', '--profile', '_default']
    )
    assert tag in result.stdout


@pytest.mark.parametrize('tag', ['test-tag', 'latest', 'my_app'])
@pytest.mark.parametrize(
    'profile',
    [
        'production',
        'acceptance',
        'development',
    ],
)
def test_add_tags_to_random_profiles(
    cli_runner: CliRunner,
    temp_folder_with_slough_config: Path,
    tag: str,
    profile: str,
) -> None:
    """Test adding a container tag other profiles.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        tag (str): Tag name to add.
        profile (str): Profile name
    """
    cli_runner.invoke(app, ['profiles', 'add', profile])
    cli_runner.invoke(
        app,
        ['container', 'tags', 'add', tag, '--profile', profile],
    )

    result = cli_runner.invoke(
        app, ['container', 'tags', 'list', '--profile', profile]
    )
    assert tag in result.stdout


@pytest.mark.parametrize(
    'tags',
    [
        ['test-tag1', 'test-tag2'],
        ['latest', 'latest-dev'],
        ['my_app', 'my_app-dev', 'my_app-prod'],
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
def test_add_multiple_tags_to_random_profiles(
    cli_runner: CliRunner,
    temp_folder_with_slough_config: Path,
    tags: list[str],
    profile: str,
) -> None:
    """Test adding a container tag other profiles.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        tags (list[str]): Tags to add.
        profile (str): Profile name
    """
    cli_runner.invoke(app, ['profiles', 'add', profile])
    cli_runner.invoke(
        app,
        ['container', 'tags', 'add', *tags, '--profile', profile],
    )

    result = cli_runner.invoke(
        app, ['container', 'tags', 'list', '--profile', profile]
    )
    for tag in tags:
        assert tag in result.stdout


@pytest.mark.parametrize('tag', ['test-tag', 'latest', 'my_app'])
def test_add_tags_multiple_times(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, tag: str
) -> None:
    """Test adding a container tag other profiles.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        tag (str): Tag name to add.
    """
    for _ in range(5):
        cli_runner.invoke(
            app,
            ['container', 'tags', 'add', tag],
        )

    result = cli_runner.invoke(app, ['container', 'tags', 'list'])
    assert result.stdout.count(tag) == 1


@pytest.mark.parametrize('tag', ['test-tag', 'latest', 'my_app'])
def test_add_tags_to_all_profile(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, tag: str
) -> None:
    """Test adding a container tags to the `_all` profile.

    It should only be listed once.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        tag (str): Tag name to add.
    """
    cli_runner.invoke(
        app,
        ['container', 'tags', 'add', tag, '--profile', '_all'],
    )

    result = cli_runner.invoke(
        app, ['container', 'tags', 'list', '--profile', '_all']
    )
    assert result.stdout.count(tag) == 1


def test_listing_tags(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path
) -> None:
    """Test listing all container tags.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
    """
    cli_runner.invoke(
        app,
        ['container', 'tags', 'add', 'test-tag', 'latest', 'my_app'],
    )
    result = cli_runner.invoke(app, ['container', 'tags', 'list'])
    assert 'test-tag' in result.stdout
    assert 'latest' in result.stdout
    assert 'my_app' in result.stdout


@pytest.mark.parametrize('tag', ['test-tag', 'latest', 'my_app'])
def test_removing_a_single_tag(
    cli_runner: CliRunner, temp_folder_with_slough_config: Path, tag: str
) -> None:
    """Test removing container tags.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        tag (str): Tag name to remove.
    """
    cli_runner.invoke(
        app,
        ['container', 'tags', 'add', tag],
    )
    result = cli_runner.invoke(app, ['container', 'tags', 'list'])
    assert tag in result.stdout

    cli_runner.invoke(app, ['container', 'tags', 'remove', tag])
    result = cli_runner.invoke(app, ['container', 'tags', 'list'])
    assert tag not in result.stdout


@pytest.mark.parametrize(
    'tags',
    [
        ['test-tag', 'latest', 'my_app'],
        ['latest', 'dev-latest', 'acc-latest'],
        ['my_app', 'app', '1.2.3'],
    ],
)
def test_removing_multiple_tags(
    cli_runner: CliRunner,
    temp_folder_with_slough_config: Path,
    tags: list[str],
) -> None:
    """Test removing container tags.

    Args:
        cli_runner (CliRunner): Typer CLI runner.
        temp_folder_with_slough_config (Path): Path to temporary folder with
            Slough configuration.
        tags (list[str]): Tags to remove.
    """
    cli_runner.invoke(
        app,
        ['container', 'tags', 'add', *tags],
    )
    result = cli_runner.invoke(app, ['container', 'tags', 'list'])
    for tag in tags:
        assert tag in result.stdout

    cli_runner.invoke(app, ['container', 'tags', 'remove', *tags])
    result = cli_runner.invoke(app, ['container', 'tags', 'list'])
    for tag in tags:
        assert tag not in result.stdout
