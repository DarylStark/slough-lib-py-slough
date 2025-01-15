"""Tests for the `chain_of_command` package."""

from chain_of_responsibility import ChainHandler


def test_chain_of_responsibility_success(
    chain_of_responsibility_success: ChainHandler[str],
) -> None:
    """Test ChainHandler class.

    Args:
        chain_of_responsibility_success (ChainHandler[str]): A ChainHandler
            instance.
    """
    assert chain_of_responsibility_success.handle() == 'processed'


def test_chain_of_responsibility_failure(
    chain_of_responsibility_failure: ChainHandler[str],
) -> None:
    """Test ChainHandler class.

    Args:
        chain_of_responsibility_failure (ChainHandler[str]): A ChainHandler
    """
    assert chain_of_responsibility_failure.handle() is None


def test_chain_of_responsibility_success_failure(
    chain_of_responsibility_success_failure: ChainHandler[str],
) -> None:
    """Test ChainHandler class.

    Args:
        chain_of_responsibility_success_failure (ChainHandler[str]): A
            ChainHandler
    """
    assert chain_of_responsibility_success_failure.handle() == 'processed'


def test_chain_of_responsibility_failure_success(
    chain_of_responsibility_failure_success: ChainHandler[str],
) -> None:
    """Test ChainHandler class.

    Args:
        chain_of_responsibility_failure_success (ChainHandler[str]): A
            ChainHandler
    """
    assert chain_of_responsibility_failure_success.handle() == 'processed'
