"""Tests for the CLIOutputVisitor classes."""

from io import StringIO
from unittest.mock import patch

import pytest

from slough_cli_tool.cli_output_models import DataSetOutput, MessageOutput
from slough_cli_tool.cli_output_visitor import EnvironmentVariableOutput
from slough_cli_tool.exceptions import OutputTypeUnsupportedError


def test_environment_variable_output_invalid_data() -> None:
    """Test if we get an error when we give invalid data."""
    model = DataSetOutput(fields=['column1'])
    model.data = ['test']
    output = EnvironmentVariableOutput()
    with pytest.raises(OutputTypeUnsupportedError):
        model.out(output)


def test_environment_variable_output_message() -> None:
    """Test if we can output a message."""
    model = MessageOutput(message='test')
    output = EnvironmentVariableOutput()
    model.out(output)

    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        model.out(output)
        actual_output = mock_stdout.getvalue()
        assert actual_output == 'MESSAGE="test"\n'
