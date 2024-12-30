"""File with the required fixtures."""

import pytest

from chain_of_responsibility import ChainHandler, NotHandledError


@pytest.fixture
def chain_of_responsibility_handlers() -> dict[str, type[ChainHandler[str]]]:
    """Fixture that returns a dictionary with ChainHandlers."""

    class SuccessFullHandler(ChainHandler[str]):
        """ChainHandler that "processes" the request."""

        def _handle(self) -> str:
            """Handle the command."""
            return 'processed'

    class FailingHandler(ChainHandler[str]):
        """ChainHandler that doesn't process the request."""

        def _handle(self) -> str:
            """Handle the command."""
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
