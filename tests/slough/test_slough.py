"""Tests for the Slough module."""

import pytest

from slough import Slough
from slough_config.config_model import SloughConfig
from slough_config.exceptions import ProfileNotFoundError


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
    with slough_object:
        slough_object.add_profile('my_new_profile')

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


def test_retrieving_profile_with_all(slough_object: Slough) -> None:
    """Test the retrieval of a profile with all profiles."""
    slough_object.add_profile('new_profile')
    slough_object.get_profile(
        'new_profile'
    ).get_container_configuration().add_tags(['tag1', 'tag2'])
    slough_object.get_profile('_all').get_container_configuration().add_tags(
        ['tag3', 'tag4']
    )

    combined_profile = slough_object.get_profile_with_all('new_profile')
    assert sorted(
        combined_profile.get_container_configuration().tags
    ) == sorted(
        [
            '_all_tag',
            'tag1',
            'tag2',
            'tag3',
            'tag4',
        ]
    )


def test_context_manager(slough_object: Slough) -> None:
    """Test using the Slough object as a context manager.

    Args:
        slough_object (Slough): The Slough object to test.
    """
    with slough_object as s:
        assert s is slough_object
        assert s.config == slough_object.config
        assert s.profile_list == slough_object.profile_list
        assert s.get_profile('_default') == slough_object.get_profile(
            '_default'
        )
        assert s.get_profile('test') == slough_object.get_profile('test')


def test_context_manager_exception(
    slough_object: Slough,
) -> None:
    """Test using the Slough object as a context manager with an exception.

    Args:
        slough_object (Slough): The Slough object to test.
    """
    with pytest.raises(ValueError), slough_object as _:
        raise ValueError('Test exception')
    assert not slough_object.is_default_config
