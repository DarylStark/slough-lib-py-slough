"""Tests for the Slough module."""

import pytest

from slough import Slough
from slough.exceptions import ProfileNotFoundError
from slough_config.config_model import SloughConfig


def test_config_retrieval(
    config_model: SloughConfig, slough_object: Slough
) -> None:
    """Test the retrieval of the configuration."""
    assert slough_object.config == config_model


def test_default_config(
    failing_slough_object: Slough,
) -> None:
    """Test if the default configuration is loaded.

    This test checks if the default configuration is loaded when the
    configuration file is not found or is invalid.

    Args:
        failing_slough_object (Slough): The Slough object to test.
    """
    assert failing_slough_object.config.project.name == 'empty_project'
    assert failing_slough_object.is_default_config


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


def test_rename_profile(slough_object: Slough) -> None:
    """Test renaming a profile."""
    slough_object.add_profile('new_profile')
    slough_object.rename_profile('new_profile', 'test2')
    assert sorted(slough_object.profile_list) == sorted(
        ['_default', '_all', 'test', 'test2']
    )


def test_retrieving_profile(slough_object: Slough) -> None:
    """Test the retrieval of a profile."""
    slough_object.add_profile('new_profile')
    assert slough_object.get_profile('new_profile') is not None
    assert slough_object.get_profile('_default') is not None
    assert slough_object.get_profile('_all') is not None
    assert slough_object.get_profile('test') is not None


def test_retrieving_non_existing_profile(
    slough_object: Slough,
) -> None:
    """Test the retrieval of a non-existing profile."""
    with pytest.raises(ProfileNotFoundError):
        slough_object.get_profile('non_existing_profile')


# TODO: Test the retrieval of the profiles
