"""Module with tests for the container management."""

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
