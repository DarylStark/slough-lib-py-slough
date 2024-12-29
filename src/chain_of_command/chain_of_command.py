"""Module with ChainOfCommand class."""

from .command_handler import CommandHandler


class ChainOfCommand:
    """Class that represents a chain of command."""

    def __init__(self, first_handler: CommandHandler) -> None:
        """Initialize the chain of command."""
        self._first_handler = first_handler

    def handle(self) -> bool:
        """Handle the command."""
        return self._first_handler.handle()
