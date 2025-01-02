"""Module with generic CLI functions."""

from slough import Slough


def raise_for_missing_config(slough: Slough) -> None:
    """Raise an error if the configuration is not loaded.

    Args:
        slough (Slough): Slough object.
    """
    if not slough.config:
        # TODO: Custom exception
        raise ValueError('No configuration loaded.')
