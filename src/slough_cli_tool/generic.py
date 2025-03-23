"""Module with generic CLI functions."""

import warnings
from pathlib import Path

import typer
from rich.console import Console

from slough import Slough
from slough_config import SloughConfig

from .exceptions import ConfigMissingError


def get_context_data(ctx: typer.Context) -> tuple[Console, Slough]:
    """Get context data from Typer context.

    Args:
        ctx (typer.Context): Typer context.

    Returns:
        tuple[Slough, Console]: onsole object, Slough object.
    """
    warnings.warn(
        'get_context_data is deprecated and will be removed after refactoring',
        DeprecationWarning,
        stacklevel=2,
    )
    slough = ctx.obj['slough']
    console = ctx.obj['console']
    return console, slough


def get_context_data_config(
    ctx: typer.Context,
) -> tuple[Console, Slough, SloughConfig, Path]:
    """Get context data from Typer context with config.

    Args:
        ctx (typer.Context): Typer context.

    Returns:
        tuple[Console, Slough, SloughConfig, str]]: Console object, Slough
            object, SloughConfig object, and configuration file path.
    """
    console, slough = get_context_data(ctx)

    if (
        not isinstance(slough, Slough) or not slough.config
        # or not slough.cfgfile
    ):
        raise ConfigMissingError('Configuration is missing.')

    return console, slough, slough.config, Path()  # , slough.cfgfile
