"""Module with tests for the Dev Container management."""

import json

import pytest
from typer.testing import CliRunner

from slough_cli_tool import app


def test_dev_container_generate_config_no_options(
    monkeypatch: pytest.MonkeyPatch, remove_dev_container: None
) -> None:
    """Generate a dev conatiner configuration without any options.

    Args:
        monkeypatch (pytest.MonkeyPatch): The monkeypatch fixture.
        remove_dev_container (None): Remove the generated dev container.
    """
    monkeypatch.chdir('tests/test_data/project1/')
    runner = CliRunner()
    result = runner.invoke(
        app,
        ['dev-container', 'generate-config'],
    )
    assert result.exit_code == 0

    # Get the created file
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert data['image'] == 'dast1986/slough-dev-dc-python:latest'


@pytest.mark.parametrize('tag', ['latest', '1.0.0', 'latest-dev'])
def test_dev_container_generate_config_specific_tag(
    monkeypatch: pytest.MonkeyPatch, tag: str, remove_dev_container: None
) -> None:
    """Generate a dev conatiner configuration with a tag.

    Args:
        monkeypatch (pytest.MonkeyPatch): The monkeypatch fixture.
        tag (str): The tag to use.
        remove_dev_container (None): Remove the generated dev container.
    """
    monkeypatch.chdir('tests/test_data/project1/')
    runner = CliRunner()
    result = runner.invoke(
        app,
        ['dev-container', 'generate-config', '--container-tag', tag],
    )
    assert result.exit_code == 0

    # Get the created file
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert data['image'] == f'dast1986/slough-dev-dc-python:{tag}'


@pytest.mark.parametrize('name', ['dc-01', 'dc-02', 'my-dev-container'])
def test_dev_container_generate_config_specific_name(
    monkeypatch: pytest.MonkeyPatch, name: str, remove_dev_container: None
) -> None:
    """Generate a dev conatiner configuration with a tag.

    Args:
        monkeypatch (pytest.MonkeyPatch): The monkeypatch fixture.
        name (str): The name to use.
        remove_dev_container (None): Remove the generated dev container.
    """
    monkeypatch.chdir('tests/test_data/project1/')
    runner = CliRunner()
    result = runner.invoke(
        app,
        ['dev-container', 'generate-config', '--name', name],
    )
    assert result.exit_code == 0

    # Get the created file
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert data['name'] == name


def test_dev_container_generate_config_bind_docker_socket(
    monkeypatch: pytest.MonkeyPatch, remove_dev_container: None
) -> None:
    """Generate a dev conatiner configuration with a Docker socket bind.

    Args:
        monkeypatch (pytest.MonkeyPatch): The monkeypatch fixture.
        remove_dev_container (None): Remove the generated dev container.
    """
    monkeypatch.chdir('tests/test_data/project1/')
    runner = CliRunner()
    result = runner.invoke(
        app,
        ['dev-container', 'generate-config', '--bind-docker-socket'],
    )
    assert result.exit_code == 0

    # Get the created file
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert (
        'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind'
        in data['mounts']
    )


def test_dev_container_generate_config_no_bind_docker_socket(
    monkeypatch: pytest.MonkeyPatch, remove_dev_container: None
) -> None:
    """Generate a dev conatiner configuration without a Docker socket bind.

    Args:
        monkeypatch (pytest.MonkeyPatch): The monkeypatch fixture.
        remove_dev_container (None): Remove the generated dev container.
    """
    monkeypatch.chdir('tests/test_data/project1/')
    runner = CliRunner()
    result = runner.invoke(
        app,
        ['dev-container', 'generate-config', '--no-bind-docker-socket'],
    )
    assert result.exit_code == 0

    # Get the created file
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert 'mounts' not in data
