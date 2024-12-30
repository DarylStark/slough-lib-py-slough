"""Entry point for the Chain of Responsibility package."""

from .chain_handler import ChainHandler, NotHandledError

__all__ = ['ChainHandler', 'NotHandledError']
