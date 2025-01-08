"""Module with generic CLI functions."""

from slough import Slough

from .exceptions import ConfigMissingError


def raise_for_missing_config(slough: Slough) -> None:
    """Raise an error if the configuration is not loaded.

    Args:
        slough (Slough): Slough object.
    """
    if not slough.config:
        raise ConfigMissingError('No configuration loaded.')
