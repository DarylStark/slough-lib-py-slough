"""Tests for the `main` module of the SloughCLI package."""

import pytest

from slough.exceptions import SloughError
from slough_cli_tool.cli_error_handeling import (
    display_error,
    get_exception_baseclasses,
)
from slough_config.exceptions import SloughConfigError


@pytest.mark.parametrize(
    'exception, expected_baseclasses',
    [
        (SloughError('Test error'), ['SloughError']),
        (SloughConfigError('Test config error'), ['SloughConfigError']),
    ],
)
def test_exception_baseclasses(
    exception: Exception, expected_baseclasses: list[str]
) -> None:
    """Test the `get_exception_baseclasses` function.

    Args:
        exception (BaseException): The exception instance.
        expected_baseclasses (list[str]): Expected base class names.
    """
    base_classes = get_exception_baseclasses(exception)
    assert base_classes == expected_baseclasses


def test_display_error(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the `display_error` function.

    Args:
        capsys (pytest.CaptureFixture[str]): The pytest fixture for capturing
            output.
    """
    exception = SloughError('Test error')
    display_error(exception)

    captured = capsys.readouterr()
    assert 'SloughError' in captured.err
    assert 'Test error' in captured.err
