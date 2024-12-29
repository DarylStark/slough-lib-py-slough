"""Tests for the `chain_of_command` package."""

from chain_of_command import ChainOfCommand


def test_chain_of_command_success_failure(
    chain_of_command_success_failure: ChainOfCommand,
) -> None:
    """Test ChainOfCommand class."""
    assert chain_of_command_success_failure.handle()


def test_chain_of_command_failure_success(
    chain_of_command_failure_success: ChainOfCommand,
) -> None:
    """Test ChainOfCommand class."""
    assert chain_of_command_failure_success.handle()


def test_chain_of_command_success_only(
    chain_of_command_success_only: ChainOfCommand,
) -> None:
    """Test ChainOfCommand class."""
    assert chain_of_command_success_only.handle()


def test_chain_of_command_failure_only(
    chain_of_command_failure_only: ChainOfCommand,
) -> None:
    """Test ChainOfCommand class."""
    assert chain_of_command_failure_only.handle() is False
