"""Tests for the Slough configuration model."""

import pytest
from pydantic import ValidationError

from slough_config import SloughConfig
from slough_config.config_model import ProjectInformation


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
def test_profile_name_validation_valid_names(
    profile_name: str, config_model: SloughConfig
) -> None:
    """Test the profile name validation for correct names.

    Test if correct names are accepted.

    Args:
        profile_name (str): The name of the profile to test.
        config_model (SloughConfig): The configuration model to test.
    """
    assert config_model._is_valid_profile_name(profile_name)  # noqa: SLF001


@pytest.mark.parametrize(
    'profile_name',
    ['_all', '_default', '_test', 'name with spaces'],
)
def test_profile_name_validation_invalid_names(
    profile_name: str, config_model: SloughConfig
) -> None:
    """Test the profile name validation for incorrect names.

    Test if incorrect names are not accepted.

    Args:
        profile_name (str): The name of the profile to test.
        config_model (SloughConfig): The configuration model to test.
    """
    assert not config_model._is_valid_profile_name(profile_name)  # noqa: SLF001


@pytest.mark.parametrize('profile_name', ['_default', '_all', 'test'])
def test_profile_exists_existing_profile(
    config_model: SloughConfig, profile_name: str
) -> None:
    """Test the profile existence check.

    Args:
        config_model (SloughConfig): The configuration model to test.
        profile_name (str): The name of the profile to check.
    """
    assert config_model._profile_exists(profile_name)  # noqa: SLF001


@pytest.mark.parametrize('profile_name', ['non_existing', 'fake', 'not_there'])
def test_profile_exists_mnon_existing_profile(
    config_model: SloughConfig, profile_name: str
) -> None:
    """Test the profile existence check for a non-existing profile.

    Args:
        config_model (SloughConfig): The configuration model to test.
        profile_name (str): The name of the profile to check.
    """
    assert not config_model._profile_exists(profile_name)  # noqa: SLF001


def test_profile_creation(config_model: SloughConfig) -> None:
    """Test the profile creation.

    Args:
        config_model (SloughConfig): The configuration model to test.
    """
    config_model.add_profile('new_profile')
    assert 'new_profile' in config_model.profile_list


@pytest.mark.parametrize(
    'profile_name',
    ['_all', '_default'],
)
def test_profile_creation_when_already_exists_default_profiles(
    profile_name: str, config_model: SloughConfig
) -> None:
    """Test the profile creation when the profile already exists.

    This test is for the default profiles (`_all` and `_default`).

    Args:
        profile_name (str): The name of the profile to test.
        config_model (SloughConfig): The configuration model to test.
    """
    with pytest.raises(ValueError):
        config_model.add_profile(profile_name)


def test_profile_creation_when_already_exists(
    config_model: SloughConfig,
) -> None:
    """Test the profile creation when the profile already exists.

    This test creates a profile with the name `test` and then tries to create
    it again. It should raise a ValueError.

    Args:
        config_model (SloughConfig): The configuration model to test.
    """
    with pytest.raises(ValueError):
        config_model.add_profile('test')


@pytest.mark.parametrize(
    'profile_name',
    ['_all', '_default', '_test', 'name with spaces'],
)
def test_profile_creation_with_invalid_name(
    config_model: SloughConfig,
    profile_name: str,
) -> None:
    """Test the profile creation with an invalid name.

    Args:
        config_model (SloughConfig): The configuration model to test.
        profile_name (str): The name of the profile to test.
    """
    with pytest.raises(ValueError):
        config_model.add_profile(profile_name)


def test_profile_retrieval(config_model: SloughConfig) -> None:
    """Test the profile retrieval.

    Args:
        config_model (SloughConfig): The configuration model to test.
    """
    profile = config_model.cfg_profiles['test']
    assert profile is not None
    assert 'container' in profile.__dict__


def test_profile_removal(config_model: SloughConfig) -> None:
    """Test the profile removal.

    Args:
        config_model (SloughConfig): The configuration model to test.
    """
    config_model.remove_profile('test')
    assert 'test' not in config_model.profile_list
    assert 'test' not in config_model.cfg_profiles


def test_profile_rename(config_model: SloughConfig) -> None:
    """Test the profile rename.

    Args:
        config_model (SloughConfig): The configuration model to test.
    """
    config_model.rename_profile('test', 'new_test')
    assert 'new_test' in config_model.profile_list
    assert 'test' not in config_model.profile_list
    assert 'new_test' in config_model.cfg_profiles
    assert 'test' not in config_model.cfg_profiles


@pytest.mark.parametrize(
    'profile_name',
    ['_all', '_default', '_test', 'name with spaces'],
)
def test_profile_rename_invalid_name(
    config_model: SloughConfig, profile_name: str
) -> None:
    """Test the profile rename with a invalid name.

    Args:
        config_model (SloughConfig): The configuration model to test.
        profile_name (str): The name of the profile to test.
    """
    with pytest.raises(ValueError):
        config_model.rename_profile('test', profile_name)


@pytest.mark.parametrize(
    'profile_name',
    ['test1', 'test2', 'test3'],
)
def test_profile_rename_non_existing_profile(
    config_model: SloughConfig, profile_name: str
) -> None:
    """Test the profile rename with a non existing profile.

    Args:
        config_model (SloughConfig): The configuration model to test.
        profile_name (str): The name of the profile to test.
    """
    with pytest.raises(ValueError):
        config_model.rename_profile(profile_name, 'new_test')


@pytest.mark.parametrize(
    'profile_name',
    ['test1', 'test2', 'test3'],
)
def test_profile_rename_to_existing_profile(
    config_model: SloughConfig, profile_name: str
) -> None:
    """Test the profile rename with a non existing profile.

    Args:
        config_model (SloughConfig): The configuration model to test.
        profile_name (str): The name to rename to.
    """
    config_model.add_profile(profile_name)
    with pytest.raises(ValueError):
        config_model.rename_profile('test', profile_name)


@pytest.mark.parametrize(
    'profile_name',
    ['_all', '_default'],
)
def test_profile_removal_default_profiles(
    config_model: SloughConfig, profile_name: str
) -> None:
    """Test the profile removal of default profiles.

    This test is for the default profiles (`_all` and `_default`).

    Args:
        config_model (SloughConfig): The configuration model to test.
        profile_name (str): The name of the profile to test.
    """
    with pytest.raises(ValueError):
        config_model.remove_profile(profile_name)


@pytest.mark.parametrize('profile_name', ['non_existing', 'fake', 'not_there'])
def test_profile_removal_non_existing_profiles(
    config_model: SloughConfig, profile_name: str
) -> None:
    """Test the profile removal of non existing profiles.

    Args:
        config_model (SloughConfig): The configuration model to test.
        profile_name (str): The name of the profile to test.
    """
    with pytest.raises(ValueError):
        config_model.remove_profile(profile_name)


@pytest.mark.parametrize(
    'version',
    ['0.1.0', '1.0.0', '1.1.0', '1.1.1', '1.1.2-a0', '1.1.2-a10', '1.1.2-rc0'],
)
def test_project_information_valid_versions(
    project_model: ProjectInformation, version: str
) -> None:
    """Test the project information version validation.

    Args:
        project_model (ProjectInformation): The project information model to
            test.
        version (str): The version to test.
    """
    project_model.version = version
    assert project_model.version == version


@pytest.mark.parametrize(
    'version',
    ['', 'wrong', '1.0.0-rc', '1.1.0rc0', '1.1.1rc', 'v1.2.3'],
)
def test_project_information_invalid_versions(
    project_model: ProjectInformation, version: str
) -> None:
    """Test the project information version validation with invalid versions.

    Args:
        project_model (ProjectInformation): The project information model to
            test.
        version (str): The version to test.
    """
    with pytest.raises(ValidationError):
        project_model.version = version


# TODO: Add tests for the emailaddress validation
