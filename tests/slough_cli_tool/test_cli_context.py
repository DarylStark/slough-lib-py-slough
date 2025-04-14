"""Tests for the CLI context."""

from slough_cli_tool.cli_context import SloughCLIContext


def test_lazy_loading_of_logger() -> None:
    """Test that the logger is lazily loaded."""
    context = SloughCLIContext()
    assert context._logger is None  # noqa: SLF001
    new_logger = context.logger
    assert context._logger is not None  # noqa: SLF001
    assert context.logger is new_logger


def test_lazy_loading_of_slough() -> None:
    """Test that the Slough object is lazily loaded."""
    context = SloughCLIContext()
    assert context._slough is None  # noqa: SLF001
    new_slough = context.slough
    assert context._slough is not None  # noqa: SLF001
    assert context.slough is new_slough


def test_lazy_loading_of_output_visitor() -> None:
    """Test that the output visitor object is lazily loaded."""
    context = SloughCLIContext()
    assert context._cli_output_visitor is None  # noqa: SLF001
    new_output_visitor = context.output_visitor
    assert context._cli_output_visitor is not None  # noqa: SLF001
    assert context.output_visitor is new_output_visitor
