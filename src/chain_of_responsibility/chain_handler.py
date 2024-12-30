"""Module with the ChainHandler interface."""

from abc import ABC, abstractmethod


class NotHandledError(Exception):
    """Exception raised when a handler does not handle the request.

    This exception will be raised when a handler does not handle the request.
    The calling method can then move to the next handler in the chain (if there
    is one).
    """

    pass


class ChainHandler[T = str](ABC):
    """Interface for the chain of responsibility pattern."""

    def __init__(self) -> None:
        """Initializes the handler."""
        self._next_handler: ChainHandler[T] | None = None

    def set_next(self, handler: 'ChainHandler[T]') -> 'ChainHandler[T]':
        """Sets the next handler in the chain.

        Args:
            handler (ChainHandler): The next handler in the chain.

        Returns:
            ChainHandler: The next handler in the chain.
        """
        self._next_handler = handler
        return handler

    @abstractmethod
    def _handle(self) -> T:
        """Handles the request.

        This method should be implemented by the concrete handlers. It should
        handle the request and return the result. If it cannot handle the
        request, for whatever reasong, it should raise a `NotHandledError`.

        Returns:
            T: The result of the request.
        """

    def handle(self) -> T | None:
        """Handles the request.

        Uses the `_handle` method to handle the request. If the request is not
        handled, the method will try to pass the request to the next handler in
        the chain.

        Returns:
            T: The result of the request.
        """
        try:
            return self._handle()
        except NotHandledError:
            if self._next_handler:
                return self._next_handler.handle()
        return None
