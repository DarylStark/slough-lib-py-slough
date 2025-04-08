"""Tests for the CLIOutputModel classes."""

from unittest.mock import Mock

from slough_cli_tool.cli_output_models import DataSetOutput


def test_data_set_output_setting_fields() -> None:
    """Test setting fields in a DataSetOutput.

    Sets the fields and check if they are retrieved correctly.
    """
    # Arrange
    fields = ['column1', 'column2', 'column3']
    data_set_output = DataSetOutput(fields)

    # Assert
    assert data_set_output.fields == fields


def test_data_set_output_setting_data() -> None:
    """Test setting data in a DataSetOutput.

    Sets the data and check if they are retrieved correctly.
    """
    # Arrange
    fields = ['column1', 'column2', 'column3']
    data = [
        ['value1', 'value2', 'value3'],
        ['value4', 'value5', 'value6'],
    ]
    data_set_output = DataSetOutput(fields)
    data_set_output.data = data

    # Assert
    assert data_set_output.data == data


def test_data_set_output_visitor() -> None:
    """Test the output method of DataSetOutput.

    Create a mock visitor and check if the out_dataset method is called.
    """
    # Arrange
    fields = ['column1', 'column2', 'column3']
    data = [
        ['value1', 'value2', 'value3'],
        ['value4', 'value5', 'value6'],
    ]
    data_set_output = DataSetOutput(fields)
    data_set_output.data = data

    # Act
    mock_visitor = Mock()
    data_set_output.out(mock_visitor)

    # Assert
    mock_visitor.out_dataset.assert_called_once_with(data_set_output)
