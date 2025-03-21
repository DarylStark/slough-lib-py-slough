"""Module with custom exceptions for the Slough package."""


class SloughError(Exception):
    """Base exception for the Slough package."""

    pass


class StorageManagerError(Exception):
    """Base exception for the storage manager."""

    pass


class ConfigNogLoadedError(Exception):
    """Exception raised when the configuration is not loaded."""

    pass
