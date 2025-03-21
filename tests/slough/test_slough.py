"""Tests for the Slough module."""

from slough import Slough
from slough_config.config_model import SloughConfig


def test_config_retrieval(
    config_model: SloughConfig, slough_object: Slough
) -> None:
    """Test the retrieval of the configuration."""
    assert slough_object.config == config_model


def test_saving_config(slough_object: Slough) -> None:
    """Test the saving of the configuration."""
    slough_object.add_profile('my_new_profile')
    slough_object.save()

    # Reload the configuration
    slough_object = Slough(slough_object._storage_manager)  # noqa: SLF001

    assert sorted(slough_object.profile_list) == sorted(
        [
            '_all',
            '_default',
            'my_new_profile',
            'test',
        ]
    )


def test_profile_list(slough_object: Slough) -> None:
    """Test the retrieval of the profile list."""
    assert sorted(slough_object.profile_list) == sorted(
        ['_default', '_all', 'test']
    )


def test_add_profile(slough_object: Slough) -> None:
    """Test the addition of a profile."""
    slough_object.add_profile('new_profile')
    assert sorted(slough_object.profile_list) == sorted(
        ['_default', '_all', 'test', 'new_profile']
    )


def test_remove_profile(slough_object: Slough) -> None:
    """Test the addition of a profile."""
    slough_object.add_profile('new_profile')
    assert sorted(slough_object.profile_list) == sorted(
        ['_default', '_all', 'test', 'new_profile']
    )
    slough_object.remove_profile('new_profile')
    assert sorted(slough_object.profile_list) == sorted(
        ['_default', '_all', 'test']
    )
