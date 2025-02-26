"""Tests for the Slough configuration model."""

import pytest

from slough_config import (
    Author,
    ContainerConfiguration,
    ProjectInformation,
    SloughConfig,
)


@pytest.mark.parametrize(
    'profile_name',
    [
        'test',
        'test-name',
        'test_name',
        'test-name-123',
        'test_name_123',
    ],
)
def test_profile_name_passing_validation(profile_name: str) -> None:
    """Test the profile name validation on adding a profile.

    Test if correct names are accepted.

    Args:
        profile_name (str): The name of the profile to test.
    """
    # Create a object of the model
    obj = SloughConfig(
        project=ProjectInformation(
            name='test',
            version='0.0.1',
            authors=[Author(name='John Doe', email='john@example.com')],
        )
    )

    # Add the profile
    obj.create_profile(profile_name)

    # Check if the profile is created
    assert profile_name in obj.cfg_profiles


@pytest.mark.parametrize(
    'profile_name',
    ['_all', '_default', '_test'],
)
def test_profile_name_failing_validation(profile_name: str) -> None:
    """Test the profile name validation on adding a profile.

    Test if correct names are rejected.

    Args:
        profile_name (str): The name of the profile to test.
    """
    # Create a object of the model
    obj = SloughConfig(
        project=ProjectInformation(
            name='test',
            version='0.0.1',
            authors=[Author(name='John Doe', email='john@example.com')],
        )
    )

    # Add the profile. Should give a ValueError for failing the validation.
    with pytest.raises(ValueError):
        obj.create_profile(profile_name)


@pytest.mark.parametrize(
    'profile_name',
    ['_all', '_default'],
)
def test_profile_creation_when_already_exists_default_profiles(
    profile_name: str,
) -> None:
    """Test the profile creation when the profile already exists.

    This test is for the default profiles (`_all` and `_default`).
    """
    # Create a object of the model
    obj = SloughConfig(
        project=ProjectInformation(
            name='test',
            version='0.0.1',
            authors=[Author(name='John Doe', email='john@example.com')],
        )
    )

    # Add the profile. Should give a ValueError for failing the validation.
    with pytest.raises(ValueError):
        obj.create_profile(profile_name)


def test_profile_creation_when_already_exists() -> None:
    """Test the profile creation when the profile already exists.

    This test creates a profile with the name `test` and then tries to create
    it again. It should raise a ValueError.
    """
    # Create a object of the model
    obj = SloughConfig(
        project=ProjectInformation(
            name='test',
            version='0.0.1',
            authors=[Author(name='John Doe', email='john@example.com')],
        )
    )

    # Add the profile
    obj.create_profile('test')

    # Add the profile again . Should give a ValueError because it already
    # exists.
    with pytest.raises(ValueError):
        obj.create_profile('test')


def test_profile_retrieval() -> None:
    """Test the profile retrieval."""
    # Create a object of the model
    # Create a object of the model
    obj = SloughConfig(
        project=ProjectInformation(
            name='test',
            version='0.0.1',
            authors=[Author(name='John Doe', email='john@example.com')],
        )
    )

    # Add the profile
    obj.create_profile('test')

    # Retrieve the profile
    profile = obj.cfg_profiles['test']

    # Add container images to the profile
    if not profile.container:
        profile.container = ContainerConfiguration()

    profile.container.tags.append('latest')

    # Retrieve the profile again
    profile = obj.cfg_profiles['test']

    # Check if the tag is in there
    assert profile.container is not None
    assert 'latest' in profile.container.tags
