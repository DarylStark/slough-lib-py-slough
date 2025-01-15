"""Module with custom exceptions for the Slough CLI package."""


class SloughCLIError(Exception):
    """Base exception for the Slough CLI package."""

    pass


class ConfigMissingError(SloughCLIError):
    """Error raised when the configuration is missing."""

    pass


class ConfigConvertionAlreadyCorrectSufficError(SloughCLIError):
    """Error raised when the configuration is already in the correct suffix."""

    pass


class ConfigAlreadySetError(SloughCLIError):
    """Error raised when the configuration is already set."""

    pass
