"""Module with custom exceptions for the Slough package."""


class SloughError(Exception):
    """Base exception for the Slough package."""

    pass


class StorageManagerError(SloughError):
    """Base exception for the storage manager."""

    pass


class ConfigNogLoadedError(SloughError):
    """Exception raised when the configuration is not loaded."""

    pass


class ProfileNotFoundError(SloughError):
    """Error raised when the profile is not found."""

    pass
