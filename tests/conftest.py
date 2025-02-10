"""File with the required fixtures."""

import shutil
from collections.abc import Generator
from pathlib import Path

import pytest
from typer.testing import CliRunner

from chain_of_responsibility import ChainHandler, NotHandledError


@pytest.fixture
def chain_of_responsibility_handlers() -> dict[str, type[ChainHandler[str]]]:
    """Fixture that returns a dictionary with ChainHandlers.

    Returns:
        dict[str, type[ChainHandler[str]]]: A dictionary with ChainHandlers.
    """

    class SuccessFullHandler(ChainHandler[str]):
        """ChainHandler that "processes" the request."""

        def _handle(self) -> str:
            """Handle the command.

            Returns:
                str: A string with the result of the processing.
            """
            return 'processed'

    class FailingHandler(ChainHandler[str]):
        """ChainHandler that doesn't process the request."""

        def _handle(self) -> str:
            """Handle the command.

            Returns:
                str: A string with the result of the processing.
            """
            raise NotHandledError

    return {
        'success': SuccessFullHandler,
        'failure': FailingHandler,
    }


@pytest.fixture
def chain_of_responsibility_success(
    chain_of_responsibility_handlers: dict[str, type[ChainHandler[str]]],
) -> ChainHandler[str]:
    """Fixture that returns a successful ChainHandler instance.

    A success ChainHandler.

    Args:
        chain_of_responsibility_handlers (dict[str, type[ChainHandler[str]]]):
            A dictionary with ChainHandlers. Should come from a fixture.

    Returns:
        ChainHandler: A ChainHandler instance.
    """
    success = chain_of_responsibility_handlers['success']()
    return success


@pytest.fixture
def chain_of_responsibility_failure(
    chain_of_responsibility_handlers: dict[str, type[ChainHandler[str]]],
) -> ChainHandler[str]:
    """Fixture that returns a failing ChainHandler instance.

    A failing ChainHandler.

    Args:
        chain_of_responsibility_handlers (dict[str, type[ChainHandler[str]]]):
            A dictionary with ChainHandlers. Should come from a fixture.

    Returns:
        ChainHandler: A ChainHandler instance.
    """
    success = chain_of_responsibility_handlers['failure']()
    return success


@pytest.fixture
def chain_of_responsibility_success_failure(
    chain_of_responsibility_handlers: dict[str, type[ChainHandler[str]]],
) -> ChainHandler[str]:
    """Fixture that returns a ChainHandler instance.

    The first handler in this chain will be a success handler, and the second
    handler will be a failure handler.

    Args:
        chain_of_responsibility_handlers (dict[str, type[ChainHandler[str]]]):
            A dictionary with ChainHandlers. Should come from a fixture.

    Returns:
        ChainHandler: A ChainHandler instance.
    """
    success = chain_of_responsibility_handlers['success']()
    success.set_next(chain_of_responsibility_handlers['failure']())
    return success


@pytest.fixture
def chain_of_responsibility_failure_success(
    chain_of_responsibility_handlers: dict[str, type[ChainHandler[str]]],
) -> ChainHandler[str]:
    """Fixture that returns a ChainHandler instance.

    The first handler in this chain will be a failure handler, and the second
    handler will be a success handler.

    Args:
        chain_of_responsibility_handlers (dict[str, type[ChainHandler[str]]]):
            A dictionary with ChainHandlers. Should come from a fixture.

    Returns:
        ChainHandler: A ChainHandler instance.
    """
    success = chain_of_responsibility_handlers['failure']()
    success.set_next(chain_of_responsibility_handlers['success']())
    return success


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
