"""Module with tests for the container management."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from slough_cli_tool import app


def test_slough_cli_container_tags_list(
    monkeypatch: pytest.MonkeyPatch,
    cli_runner: CliRunner,
) -> None:
    """Test the `container tags list` command without specifying a profile.

    This should list all container tags for the `_default` profile. This means
    that the tags for the `_default` profiles should be listed and the tags
    for the `_all` profile should be listed.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        cli_runner (CliRunner): Typer CLI runner.
    """
    monkeypatch.chdir('tests/test_data/project7/')
    result = cli_runner.invoke(app, ['container', 'tags', 'list'])
    assert 'latest-image' in result.stdout
    assert 'latest' in result.stdout


@pytest.mark.parametrize(
    'profile, expected_tags',
    [
        ('_default', ['latest']),
        ('production', ['latest-prd', 'my_application', '1.0.0']),
        ('acceptance', ['latest-rc', 'my_application', '1.0.0-rc1']),
        ('development', ['latest-alpha', 'my_application', '1.0.0-a0']),
    ],
)
def test_slough_cli_container_tags_list_specific_profiles(
    monkeypatch: pytest.MonkeyPatch,
    cli_runner: CliRunner,
    profile: str,
    expected_tags: list[str],
) -> None:
    """Test the `container tags list` command for a specific profile.

    This should list all container tags for the specified profile and the
    '_all' profile.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        cli_runner (CliRunner): Typer CLI runner.
        profile (str): Profile name.
        expected_tags (list[str]): List of expected tags for the profile.
    """
    monkeypatch.chdir('tests/test_data/project7/')
    result = cli_runner.invoke(
        app, ['container', 'tags', 'list', '--profile', profile]
    )
    assert 'latest-image' in result.stdout
    for tag in expected_tags:
        assert tag in result.stdout


def test_slough_cli_container_tags_list_no_tags(
    monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner
) -> None:
    """Test the `container tags list` command when there are no tags.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        cli_runner (CliRunner): Typer CLI runner.
    """
    monkeypatch.chdir('tests/test_data/project2/')
    result = cli_runner.invoke(app, ['container', 'tags', 'list'])
    assert 'There are no tags configured.' in result.stdout


@pytest.mark.parametrize('tag', ['test-tag', 'latest', 'my_app'])
def test_slough_cli_container_tags_add_default_profile(
    empty_test_dir_with_config: Path, cli_runner: CliRunner, tag: str
) -> None:
    """Test adding a container tag to the default profile.

    Args:
        empty_test_dir_with_config (Path): Path to the empty test directory
            with a configuration file.
        cli_runner (CliRunner): Typer CLI runner.
        tag (str): Tag name to add.
    """
    result = cli_runner.invoke(
        app,
        [
            'container',
            'tags',
            'add',
            tag,
        ],
    )
    assert f'Tag "{tag}" added to profile "_default".' in result.stdout

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
def test_slough_cli_container_tags_add_random_profiles(
    empty_test_dir_with_config: Path,
    cli_runner: CliRunner,
    profile: str,
    tag: str,
) -> None:
    """Test adding a container tag other profiles.

    Args:
        empty_test_dir_with_config (Path): Path to the empty test directory
            with a configuration file.
        cli_runner (CliRunner): Typer CLI runner.
        profile (str): Profile name
        tag (str): Tag name to add.
    """
    result = cli_runner.invoke(
        app,
        ['container', 'tags', 'add', tag, '--profile', profile],
    )
    assert f'Tag "{tag}" added to profile "{profile}".' in result.stdout

    result = cli_runner.invoke(
        app, ['container', 'tags', 'list', '--profile', profile]
    )
    assert tag in result.stdout

    result = cli_runner.invoke(
        app, ['container', 'tags', 'list', '--profile', profile]
    )
    assert tag in result.stdout


def test_slough_cli_container_tags_add_multiple_tags(
    empty_test_dir_with_config: Path, cli_runner: CliRunner
) -> None:
    """Test adding multiple container tags to the default profile.

    Args:
        empty_test_dir_with_config (Path): Path to the empty test directory
            with a configuration file.
        cli_runner (CliRunner): Typer CLI runner.
    """
    tags = ['tag1', 'tag2', 'tag3']
    result = cli_runner.invoke(
        app,
        [
            'container',
            'tags',
            'add',
            *tags,
        ],
    )
    for tag in tags:
        assert f'Tag "{tag}" added to profile "_default".' in result.stdout

    result = cli_runner.invoke(app, ['container', 'tags', 'list'])
    for tag in tags:
        assert tag in result.stdout

    result = cli_runner.invoke(
        app, ['container', 'tags', 'list', '--profile', '_default']
    )
    for tag in tags:
        assert tag in result.stdout


def test_slough_cli_container_tags_add_existing(
    empty_test_dir_with_config: Path, cli_runner: CliRunner
) -> None:
    """Test adding an existing container tag.

    This should raise an error.

    Args:
        empty_test_dir_with_config (Path): Path to the empty test directory
            with a configuration file.
        cli_runner (CliRunner): Typer CLI runner.
    """
    tag = 'latest'
    result = cli_runner.invoke(
        app,
        [
            'container',
            'tags',
            'add',
            tag,
        ],
    )
    assert f'Tag "{tag}" added to profile "_default".' in result.stdout

    result = cli_runner.invoke(
        app,
        [
            'container',
            'tags',
            'add',
            tag,
        ],
    )
    assert type(result.exception) is ValueError


def test_slough_cli_container_tags_delete_non_existing(
    empty_test_dir_with_config: Path, cli_runner: CliRunner
) -> None:
    """Test deleting a non-existing container tag.

    This should raise an error.

    Args:
        empty_test_dir_with_config (Path): Path to the empty test directory
            with a configuration file.
        cli_runner (CliRunner): Typer CLI runner.
    """
    tag = 'latest'
    result = cli_runner.invoke(
        app,
        [
            'container',
            'tags',
            'remove',
            tag,
        ],
    )
    assert type(result.exception) is ValueError


def test_slough_cli_container_tags_delete_from_default_profile(
    empty_test_dir_with_config: Path, cli_runner: CliRunner
) -> None:
    """Test deleting a container tag from the default profile.

    Args:
        empty_test_dir_with_config (Path): Path to the empty test directory
            with a configuration file.
        cli_runner (CliRunner): Typer CLI runner.
    """
    tag = 'test-tag'
    cli_runner.invoke(
        app,
        [
            'container',
            'tags',
            'add',
            tag,
        ],
    )

    result = cli_runner.invoke(
        app,
        [
            'container',
            'tags',
            'remove',
            tag,
        ],
    )

    assert f'Tag "{tag}" removed from profile "_default".' in result.stdout

    result = cli_runner.invoke(app, ['container', 'tags', 'list'])
    assert tag not in result.stdout


def test_slough_cli_container_tags_delete_from_other_profiles(
    empty_test_dir_with_config: Path, cli_runner: CliRunner
) -> None:
    """Test deleting a container tag from other profiles.

    Args:
        empty_test_dir_with_config (Path): Path to the empty test directory
            with a configuration file.
        cli_runner (CliRunner): Typer CLI runner.
    """
    tag = 'test-tag'
    profile = '_all'
    cli_runner.invoke(
        app,
        [
            'container',
            'tags',
            'add',
            tag,
            '--profile',
            profile,
        ],
    )

    result = cli_runner.invoke(
        app,
        [
            'container',
            'tags',
            'remove',
            tag,
            '--profile',
            profile,
        ],
    )

    assert f'Tag "{tag}" removed from profile "{profile}".' in result.stdout

    result = cli_runner.invoke(
        app, ['container', 'tags', 'list', '--profile', profile]
    )
    assert tag not in result.stdout
