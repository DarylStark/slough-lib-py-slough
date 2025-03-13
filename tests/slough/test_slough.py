"""Tests for the Slough module."""

from slough import Slough
from slough_config.config_model import SloughConfig


def test_config_retrieval(config_model: SloughConfig) -> None:
    """Test the retrieval of the configuration."""
    slough = Slough(config_model)
    assert slough.config == config_model


def test_profile_list(config_model: SloughConfig) -> None:
    """Test the retrieval of the profile list."""
    slough = Slough(config_model)
    assert sorted(slough.profile_list) == sorted(['_default', '_all', 'test'])


def test_add_profile(config_model: SloughConfig) -> None:
    """Test the addition of a profile."""
    slough = Slough(config_model)
    slough.add_profile('new_profile')
    assert sorted(slough.profile_list) == sorted(
        ['_default', '_all', 'test', 'new_profile']
    )


def test_remove_profile(config_model: SloughConfig) -> None:
    """Test the addition of a profile."""
    slough = Slough(config_model)
    slough.add_profile('new_profile')
    assert sorted(slough.profile_list) == sorted(
        ['_default', '_all', 'test', 'new_profile']
    )
    slough.remove_profile('new_profile')
    assert sorted(slough.profile_list) == sorted(['_default', '_all', 'test'])
