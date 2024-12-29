"""Module with a `CommandHandler` class."""

from abc import ABC, abstractmethod
from typing import Optional


class CommandHandler(ABC):
    """Abstract class for command handlers."""

    def __init__(
        self, next_handler: Optional['CommandHandler'] = None
    ) -> None:
        """Initialize the command handler."""
        self._next_handler: CommandHandler | None = None
        if next_handler:
            self.set_next_handler(next_handler)

    def set_next_handler(self, handler: 'CommandHandler') -> 'CommandHandler':
        """Set the next handler.

        Args:
            handler: The next handler.

        Returns:
            The next handler. Can be used to chain handlers.
        """
        self._next_handler = handler
        return handler

    @abstractmethod
    def _handle(self) -> bool:
        """Handle the command."""

    def handle(self) -> bool:
        """Handle the command.

        This will call the `_handle` method and then call the next handler if
        it exists.
        """
        result = self._handle()
        if not result and self._next_handler:
            return self._next_handler.handle()
        return result
