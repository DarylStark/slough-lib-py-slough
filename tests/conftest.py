"""File with the required fixtures."""

import shutil
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from mocks import MockStorageManager, MockStorageManagerFailing
from typer.testing import CliRunner

from dev_container_gen.model import DevContainer
from slough.slough import Slough
from slough_cli_tool import app
from slough_config.config_model import (
    Author,
    ConfigProfile,
    ContainerConfiguration,
    DevelopmentEnvironment,
    ProjectInformation,
    SloughConfig,
)


@pytest.fixture(scope='function')
def empty_test_dir(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[Path]:
    """Fixture that creates and removes a empty directory.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.

    Yields:
        Generator[Path]: A Path object with the path to the created directory.
    """
    path = Path('tests/test_data/empty_test_dir').resolve()
    path.mkdir(parents=True, exist_ok=True)
    monkeypatch.chdir(path)
    yield path

    # Cleanup; remove the directory and all files in it
    shutil.rmtree(path)


@pytest.fixture
def cli_runner() -> CliRunner:
    """Fixture with a Typer CLI runner.

    This fixture returns a Typer CLI runner instance that can be used to test
    CLI applications.

    Returns:
        CliRunner: A Typer CLI runner instance.
    """
    return CliRunner()


@pytest.fixture(scope='function')
def remove_dev_container() -> Generator[None]:
    """Fixture that removes the dev container folder."""
    yield None

    # Cleanup; remove the directory and all files in it
    path = '.devcontainer'
    shutil.rmtree(path)


@pytest.fixture(scope='function')
def dev_container(
    monkeypatch: pytest.MonkeyPatch, remove_dev_container: None
) -> None:
    """Fixture that creates a dev container configuration file."""
    # First we create the initial code
    monkeypatch.chdir('tests/test_data/project2/')
    runner = CliRunner()
    runner.invoke(
        app,
        [
            'dev-container',
            'generate-config',
            '--name',
            'test-container',
            '--container-tag',
            'latest',
        ],
    )


@pytest.fixture(scope='function')
def empty_test_dir_with_config(
    empty_test_dir: Path,
    cli_runner: CliRunner,
) -> Generator[Path]:
    """Fixture that creates a empty testdir with a config file.

    In the cleanup, the directory and all files in it are removed.

    Args:
        empty_test_dir (Path): Path to the empty test directory.
        cli_runner (CliRunner): Typer CLI runner.

    Yields:
        Generator[Path]: A Path object with the path to the created directory.
    """
    cli_runner.invoke(
        app,
        [
            '--cfgfile',
            'slough.yml',
            'project',
            'init',
            '--title',
            'test_project',
            '--version',
            '1.0.0',
            '--author-name',
            'test_author',
            '--author-email',
            'test@example.com',
        ],
    )
    yield empty_test_dir

    pass


@pytest.fixture(scope='function')
def project_model() -> ProjectInformation:
    """Create a `ProjectInformation` object for testing."""
    return ProjectInformation(
        name='test',
        version='0.0.1',
        authors=[Author(name='John Doe', email='johndoe@example.com')],
    )


@pytest.fixture(scope='function')
def config_model(project_model: ProjectInformation) -> SloughConfig:
    """Create a `SloughConfig` object for testing.

    Args:
        project_model (ProjectInformation): The project information model.
    """
    return SloughConfig(
        project=project_model,
        development_environment=DevelopmentEnvironment.GENERIC,
        cfg_profiles={
            'test': ConfigProfile(
                container=ContainerConfiguration(
                    tags=['test_tag'],
                )
            ),
            '_all': ConfigProfile(
                container=ContainerConfiguration(
                    tags=['_all_tag'],
                )
            ),
            '_default': ConfigProfile(
                container=ContainerConfiguration(
                    tags=['_default_tag'],
                )
            ),
        },
    )


@pytest.fixture(scope='function')
def temp_folder(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[Path]:
    """Create a temporary folder for testing.

    Creates a temporary directory with a random name. Removes it after the test
    is done.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        monkeypatch.chdir(tmpdirname)
        yield Path(tmpdirname).resolve()


@pytest.fixture(scope='function')
def slough_object(config_model: SloughConfig) -> Slough:
    """Create a Slough object for testing.

    Returns:
        Slough: A configured Slough object.
    """
    mock_storage_manager = MockStorageManager(config_model)
    slough = Slough(mock_storage_manager)
    return slough


@pytest.fixture(scope='function')
def failing_slough_object() -> Slough:
    """Create a Slough object for testing a failing loader.

    Returns:
        Slough: A configured Slough object.
    """
    mock_storage_manager = MockStorageManagerFailing()
    slough = Slough(mock_storage_manager)
    return slough


@pytest.fixture(scope='function')
def temp_folder_with_slough_config(
    monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner
) -> Generator[Path]:
    """Create a temporary folder with Slough config for testing.

    Creates a temporary directory with a random name and initializes a Slough
    project in it. Removes it after the test is done.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        cli_runner (CliRunner): Typer CLI runner.
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        monkeypatch.chdir(tmpdirname)
        cli_runner.invoke(
            app,
            [
                'project',
                'init',
                '--title',
                'test_project',
                '--version',
                '0.1.0',
                '--author-name',
                'John Doe',
                '--author-email',
                'johndoe@example.com',
                '--development-environment',
                'generic',
            ],
        )
        yield Path(tmpdirname).resolve()


@pytest.fixture(scope='function')
def temp_folder_with_slough_config_no_dev_env(
    monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner
) -> Generator[Path]:
    """Create a temporary folder with Slough config for testing.

    Creates a temporary directory with a random name and initializes a Slough
    project in it. Removes it after the test is done. This object does not
    container a development environment.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        cli_runner (CliRunner): Typer CLI runner.
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        monkeypatch.chdir(tmpdirname)
        cli_runner.invoke(
            app,
            [
                'project',
                'init',
                '--title',
                'test_project',
                '--version',
                '0.1.0',
                '--author-name',
                'John Doe',
                '--author-email',
                'johndoe@example.com',
            ],
        )
        yield Path(tmpdirname).resolve()


@pytest.fixture(scope='function')
def temp_folder_with_dev_containers(temp_folder: Path) -> Path:
    """Create a temporary folder with a Dev Container config for testing.

    Creates a temporary directory with a random name and creates multiple
    DevContainer configuration files in it. Removes it after the test is done.

    Args:
        temp_folder (Path): Path to the temporary folder.
    """
    dev_container_filename = temp_folder / '.devcontainer/devcontainer.json'
    dev_container_filename.parent.mkdir(parents=True, exist_ok=True)
    with open(dev_container_filename, 'w') as f:
        f.write('{"name": "test-container", "image": "latest"}')
    with open(temp_folder / 'devcontainer1.json', 'w') as f:
        f.write('{"name": "test-container", "image": "latest"}')
    with open(temp_folder / 'devcontainer2.json', 'w') as f:
        f.write(
            '{"name": "test-container", "image": "latest", '
            + '"remoteEnv": {"TEST_VAR": "test_value"}}'
        )
    with open(temp_folder / 'devcontainer3.json', 'w') as f:
        f.write(
            '{"name": "test-container", "image": "latest", '
            + '"mounts": ["test_mount"]}'
        )
    return temp_folder


@pytest.fixture(scope='function')
def dev_container_model() -> DevContainer:
    """Fixture for a default dev container."""
    return DevContainer(name='test', image='test_image')
