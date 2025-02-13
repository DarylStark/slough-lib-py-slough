"""Module with tests for the Dev Container management."""

import json

import pytest
from typer.testing import CliRunner

from slough_cli_tool import app
from slough_cli_tool.exceptions import DevelopmentEnvironmentNotSetError


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


def test_dev_container_generate_config_with_existing_config_tag(
    dev_container: None,
) -> None:
    """Generate a dev conatiner configuration when one already exists.

    This test changes the tag of the existing configuration.

    Args:
        dev_container (None): The test_dev_container fixture.
    """
    runner = CliRunner()

    # Then we try to create a new one with a different tag
    result = runner.invoke(
        app,
        ['dev-container', 'generate-config', '--container-tag', '0.0.1'],
    )
    assert result.exit_code == 0

    # Check if the file was updated
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert data['image'] == 'dast1986/slough-dev-dc-python:0.0.1'


def test_dev_container_generate_config_with_existing_config_name(
    dev_container: None,
) -> None:
    """Generate a dev conatiner configuration when one already exists.

    This test changes the name of the existing configuration.

    Args:
        dev_container (None): The test_dev_container fixture.
    """
    runner = CliRunner()

    # Then we try to create a new one with a different tag
    result = runner.invoke(
        app,
        ['dev-container', 'generate-config', '--name', 'new-test-name'],
    )
    assert result.exit_code == 0

    # Check if the file was updated
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert data['name'] == 'new-test-name'


def test_dev_container_generate_config_with_existing_config_docker_bind(
    dev_container: None,
) -> None:
    """Generate a dev conatiner configuration when one already exists.

    This test changes the Docker bind of the existing configuration.

    Args:
        dev_container (None): The test_dev_container fixture.
    """
    runner = CliRunner()

    # Then we try to create a new one with a different tag
    result = runner.invoke(
        app,
        ['dev-container', 'generate-config', '--bind-docker-socket'],
    )
    assert result.exit_code == 0

    # Check if the file was updated
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert (
        'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind'
        in data['mounts']
    )

    # Remove the Docker bind again
    result = runner.invoke(
        app,
        ['dev-container', 'generate-config', '--no-bind-docker-socket'],
    )

    # Check if the file was updated
    with open('.devcontainer/devcontainer.json', encoding='utf-8') as infile:
        data = json.load(infile)

    # Check values
    assert 'mounts' not in data


def test_dev_container_generate_config_with_existing_config_docker_bind_true(
    dev_container: None,
) -> None:
    """Generate a dev conatiner configuration when one already exists.

    This tests if the Docker bind stays the same when generating a new
    Dev Container configuration with the same options.

    Args:
        dev_container (None): The test_dev_container fixture.
    """
    runner = CliRunner()

    # Then we try to create a new one with a different tag
    for _ in range(2):
        result = runner.invoke(
            app,
            ['dev-container', 'generate-config', '--bind-docker-socket'],
        )
        assert result.exit_code == 0

        # Check if the file was updated
        with open(
            '.devcontainer/devcontainer.json', encoding='utf-8'
        ) as infile:
            data = json.load(infile)

        # Check values
        assert (
            'source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind'
            in data['mounts']
        )


def test_dev_container_generate_with_no_development_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Generate a dev conatiner configuration when no environment is set.

    Should always result in a error.

    Args:
        monkeypatch (pytest.MonkeyPatch): The monkeypatch fixture.
    """
    monkeypatch.chdir('tests/test_data/project3/')
    runner = CliRunner()
    result = runner.invoke(
        app,
        ['dev-container', 'generate-config'],
    )
    assert result.exit_code == 1
    assert type(result.exception) is DevelopmentEnvironmentNotSetError
