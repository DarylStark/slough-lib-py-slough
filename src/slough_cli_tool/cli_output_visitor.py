"""Visitors for outputting data."""

from abc import ABC, abstractmethod

from rich import box
from rich.console import Console
from rich.table import Table

from .cli_output_models import DataSetOutput, MessageOutput


class CLIOutputVisitor(ABC):
    """Base class for output visitors."""

    @abstractmethod
    def out_dataset(self, model: DataSetOutput) -> None:
        """Output the dataset using the given visitor.

        Args:
            model (DataSetOutput): The dataset to output.
        """

    @abstractmethod
    def out_message(self, model: MessageOutput) -> None:
        """Output the message using the given visitor.

        Args:
            model (MessageOutput): The message to output.
        """


class ConsoleOutput(CLIOutputVisitor):
    """Output visitor that uses the console for output."""

    def __init__(self) -> None:
        """Initialize the console output visitor."""
        self._console = Console()

    def out_dataset(self, model: DataSetOutput) -> None:
        """Output the dataset using the console.

        Args:
            model (DataSetOutput): The dataset to output.
        """
        table = Table(box=box.SIMPLE)
        for column in model.fields:
            table.add_column(column)

        for row in model.data:
            table.add_row(*row)

        self._console.print(table)

    def out_message(self, model: MessageOutput) -> None:
        """Output the message using the console.

        Args:
            model (MessageOutput): The message to output.
        """
        self._console.print(model.message)
