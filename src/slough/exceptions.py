"""Module with custom exceptions for the Slough package."""


class SloughError(Exception):
    """Base exception for the Slough package."""

    pass


class ConfigFileNotSetError(SloughError):
    """Exception raised when the configuration file is not set."""

    pass


class ConfigManagerNotRegisteredError(SloughError):
    """Exception raised when the configuration manager is not registered."""

    pass


class ConfigNotSetError(SloughError):
    """Exception raised when the configuration is not set."""

    pass
