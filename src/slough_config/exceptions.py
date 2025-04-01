"""Exceptions for slough_config module."""


class SloughConfigError(Exception):
    """Base class for all exceptions in the slough_config module."""


class ProfileNotFoundError(SloughConfigError):
    """Exception raised when a profile is not found in the configuration."""
