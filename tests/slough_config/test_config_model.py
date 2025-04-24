"""Tests for the Slough configuration model."""

import pytest
from pydantic import ValidationError

from slough_config import SloughConfig
from slough_config.config_model import (
    ConfigProfile,
    ContainerConfiguration,
    ProjectInformation,
)
from slough_config.exceptions import (
    DefaultProfileError,
    DuplicateProfileNameError,
    InvalidPlatformError,
    InvalidProfileNameError,
    ProfileNotFoundError,
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
    with pytest.raises(InvalidProfileNameError):
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
    with pytest.raises(DuplicateProfileNameError):
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
    with pytest.raises(InvalidProfileNameError):
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
    with pytest.raises(InvalidProfileNameError):
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
    with pytest.raises(ProfileNotFoundError):
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
    with pytest.raises(DuplicateProfileNameError):
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
    with pytest.raises(DefaultProfileError):
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
    with pytest.raises(ProfileNotFoundError):
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


def test_config_profle_container_retrieval(
    config_profile_model: ConfigProfile,
) -> None:
    """Test the config profile container retrieval.

    This test checks if the container retrieval works by retrieving a container
    from the config profile that doesn't have a `ContainerConfiguration` set.
    It should return a newly created `ContainerConfiguration` model.

    Args:
        config_profile_model (ConfigProfile): The config profile model to test.
    """
    assert config_profile_model.container is None
    assert config_profile_model.get_container_configuration() is not None
    assert config_profile_model.container is not None


def test_config_profile_container_retrieval_with_config(
    config_profile_model_with_container_config: ConfigProfile,
) -> None:
    """Test the config profile container retrieval.

    This test checks if the container retrieval works by retrieving a container
    from the config profile that does have a ContainerConfiguration set.

    Args:
        config_profile_model_with_container_config (ConfigProfile): The config
            profile model to test.
    """
    assert config_profile_model_with_container_config.container is not None
    assert (
        config_profile_model_with_container_config.get_container_configuration()
        is config_profile_model_with_container_config.container
    )


@pytest.mark.parametrize(
    'tag_name',
    [
        'test_tag1',
        'test_TAG2',
        'test_tag3',
        'test_tag4',
        'test_tag5',
    ],
)
def test_container_configuration_adding_one_tag(
    container_configuration_default_model: ContainerConfiguration,
    tag_name: str,
) -> None:
    """Test the container configuration adding one tag.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
        tag_name (str): The name of the tag to add.
    """
    container_configuration_default_model.add_tags(tag_name)
    assert container_configuration_default_model.tags == [tag_name.lower()]


@pytest.mark.parametrize(
    'tags',
    [
        ['test_tag1', 'test_tag2'],
        ['test_TAG1', 'TEST_TAG2'],
        ['a', 'b', 'c'],
    ],
)
def test_container_configuration_adding_tags(
    container_configuration_default_model: ContainerConfiguration,
    tags: list[str],
) -> None:
    """Test the container configuration adding nultiple tags.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
        tags (list[str]): The list of tags to add.
    """
    container_configuration_default_model.add_tags(tags)
    assert sorted(container_configuration_default_model.tags) == sorted(
        [tag_name.lower() for tag_name in tags]
    )


def test_retrieving_profile(config_model: SloughConfig) -> None:
    """Test the retrieval of a profile.

    Args:
        config_model (SloughConfig): The configuration model to test.
    """
    config_model.add_profile('new_profile')
    assert config_model.get_profile('new_profile') is not None
    assert config_model.get_profile('_default') is not None
    assert config_model.get_profile('_all') is not None
    assert config_model.get_profile('test') is not None


def test_retrieving_non_existing_profile(config_model: SloughConfig) -> None:
    """Test the retrieval of a non-existing profile.

    Args:
        config_model (SloughConfig): The configuration model to test.
    """
    with pytest.raises(ProfileNotFoundError):
        config_model.get_profile('non_existing_profile')


@pytest.mark.parametrize(
    'tag_name',
    [
        'test_tag1',
        'test_TAG2',
        'test_tag3',
        'test_tag4',
        'test_tag5',
    ],
)
def test_container_configuration_removing_one_tag(
    container_configuration_default_model: ContainerConfiguration,
    tag_name: str,
) -> None:
    """Test the container configuration removing one tag.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
        tag_name (str): The name of the tag to add.
    """
    container_configuration_default_model.add_tags(tag_name)
    assert container_configuration_default_model.tags == [tag_name.lower()]
    container_configuration_default_model.remove_tags(tag_name)
    assert container_configuration_default_model.tags == []


@pytest.mark.parametrize(
    'tags',
    [
        ['test_tag1', 'test_tag2'],
        ['test_TAG1', 'TEST_TAG2'],
        ['a', 'b', 'c'],
    ],
)
def test_container_configuration_removing_tags(
    container_configuration_default_model: ContainerConfiguration,
    tags: list[str],
) -> None:
    """Test the container configuration removing nultiple tags.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
        tags (list[str]): The list of tags to add.
    """
    container_configuration_default_model.add_tags(tags)
    assert sorted(container_configuration_default_model.tags) == sorted(
        [tag_name.lower() for tag_name in tags]
    )
    container_configuration_default_model.remove_tags(tags)
    assert container_configuration_default_model.tags == []


def test_combining_two_container_configurations(
    container_configuration_default_model: ContainerConfiguration,
) -> None:
    """Test the combining of two container configurations.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
    """
    container_configuration_default_model.add_tags(['test_tag1', 'test_tag2'])
    new_container = ContainerConfiguration()
    new_container.add_tags(['test_tag3', 'test_tag4'])
    combined_container = container_configuration_default_model.combine(
        new_container
    )
    assert sorted(combined_container.tags) == sorted(
        ['test_tag1', 'test_tag2', 'test_tag3', 'test_tag4']
    )


def test_combining_two_container_configurations_double_tags(
    container_configuration_default_model: ContainerConfiguration,
) -> None:
    """Test the combining of two container configurations.

    In this test, the tags from both objects are the same. The result should
    not contain duplicate tags.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
    """
    container_configuration_default_model.add_tags(['test_tag1', 'test_tag2'])
    new_container = ContainerConfiguration()
    new_container.add_tags(['test_tag1', 'test_tag3'])
    combined_container = container_configuration_default_model.combine(
        new_container
    )
    assert sorted(combined_container.tags) == sorted(
        ['test_tag1', 'test_tag2', 'test_tag3']
    )


def test_combining_container_configurations_with_none_object(
    container_configuration_default_model: ContainerConfiguration,
) -> None:
    """Test the combining of two container configurations.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
    """
    container_configuration_default_model.add_tags(['test_tag1', 'test_tag2'])
    combined_container = container_configuration_default_model.combine(None)
    assert sorted(combined_container.tags) == sorted(
        ['test_tag1', 'test_tag2']
    )


def test_combingin_container_configurations_with_empty_object(
    container_configuration_default_model: ContainerConfiguration,
) -> None:
    """Test the combining of two container configurations.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
    """
    container_configuration_default_model.add_tags(['test_tag1', 'test_tag2'])
    new_container = ContainerConfiguration()
    combined_container = container_configuration_default_model.combine(
        new_container
    )
    assert sorted(combined_container.tags) == sorted(
        ['test_tag1', 'test_tag2']
    )


def test_combining_two_configuration_profiles(
    config_profile_model_with_container_config: ConfigProfile,
) -> None:
    """Test the combining of two configuration profiles.

    Args:
        config_profile_model_with_container_config (ConfigProfile): The config
            profile model to test.
    """
    combined_profile = config_profile_model_with_container_config.combine(
        ConfigProfile(
            container=ContainerConfiguration(
                tags=['test_tag_second_container']
            )
        )
    )
    assert combined_profile.container is not None
    assert sorted(combined_profile.container.tags) == sorted(
        [
            'test_tag',
            'test_tag_second_container',
        ]
    )


def test_combining_configuration_profile_with_empty_profile(
    config_profile_model_with_container_config: ConfigProfile,
) -> None:
    """Test the combining of two configuration profiles.

    Args:
        config_profile_model_with_container_config (ConfigProfile): The config
            profile model to test.
    """
    combined_profile = config_profile_model_with_container_config.combine(
        ConfigProfile(container=None)
    )
    assert combined_profile.container is not None
    assert combined_profile.container.tags == ['test_tag']


def test_combining_empty_configuration_profile_with_full_profile(
    config_profile_model_with_container_config: ConfigProfile,
    config_profile_model: ConfigProfile,
) -> None:
    """Test the combining of two configuration profiles.

    Args:
        config_profile_model_with_container_config (ConfigProfile): The config
            profile model to test.
        config_profile_model (ConfigProfile): The config profile model to test.
    """
    combined_profile = config_profile_model.combine(
        config_profile_model_with_container_config
    )
    assert combined_profile.container is not None
    assert combined_profile.container.tags == ['test_tag']


@pytest.mark.parametrize(
    'registry',
    [
        'test-registry:5000',
        'test-registry',
        'localhost',
        'docker.io',
        'us-west1-docker.pkg.dev/my-project/',
        'us-west1-docker.pkg.dev/my-project',
        'us-west1-docker.pkg.dev/my-project/my-repo',
    ],
)
def test_container_configuration_registry_regex(
    container_configuration_default_model: ContainerConfiguration,
    registry: str,
) -> None:
    """Test the container configuration registry regex.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
        registry (str): The registry string to validate.
    """
    container_configuration_default_model.registry = registry


@pytest.mark.parametrize(
    'registry',
    [
        'wrong_hostname',
        'hostname with spaces',
        'https://with-protocol:1000',
        'wrong_port:aap',
    ],
)
def test_container_configuration_registry_regex_failing(
    container_configuration_default_model: ContainerConfiguration,
    registry: str,
) -> None:
    """Test the container configuration registry regex.

    This tests the regexes that should fail.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
        registry (str): The registry string to validate.
    """
    with pytest.raises(ValidationError):
        container_configuration_default_model.registry = registry


@pytest.mark.parametrize(
    'image',
    ['my-application', 'slough', 'my__application', 'my.application'],
)
def test_container_configuration_image_regex(
    container_configuration_default_model: ContainerConfiguration,
    image: str,
) -> None:
    """Test the container configuration image name regex.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
        image (str): The image string to validate.
    """
    container_configuration_default_model.image = image


@pytest.mark.parametrize(
    'image',
    ['my application', '_my_application', 'app:', 'app:latest'],
)
def test_container_configuration_image_regex_failing(
    container_configuration_default_model: ContainerConfiguration,
    image: str,
) -> None:
    """Test the container configuration image name regex.

    This tests the regexes that should fail.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
        image (str): The image string to validate.
    """
    with pytest.raises(ValidationError):
        container_configuration_default_model.image = image


@pytest.mark.parametrize(
    'platform_name',
    [
        'linux/amd64',
        'linux/arm64',
        'linux/arm/v7',
        'linux/arm/v6',
        'linux/ppc64le',
        'linux/s390x',
        'linux/386',
    ],
)
def test_container_configuration_adding_one_platform(
    container_configuration_default_model: ContainerConfiguration,
    platform_name: str,
) -> None:
    """Test the container configuration adding one platform.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
        platform_name (str): The name of the platform to add.
    """
    container_configuration_default_model.add_platforms(platform_name)
    assert (
        platform_name.lower()
        in container_configuration_default_model.platforms
    )


@pytest.mark.parametrize(
    'platforms',
    [
        ['linux/amd64', 'linux/arm64'],
        ['linux/arm/v7', 'linux/arm/v6'],
        ['linux/ppc64le', 'linux/s390x', 'linux/386'],
    ],
)
def test_container_configuration_adding_platforms(
    container_configuration_default_model: ContainerConfiguration,
    platforms: list[str],
) -> None:
    """Test the container configuration adding multiple platforms.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
        platforms (list[str]): The list of platforms to add.
    """
    container_configuration_default_model.add_platforms(platforms)
    assert sorted(container_configuration_default_model.platforms) == sorted(
        [platform_name.lower() for platform_name in platforms]
    )


@pytest.mark.parametrize(
    'platform_name',
    [
        'linux/amd64',
        'linux/arm64',
        'linux/arm/v7',
        'linux/arm/v6',
        'linux/ppc64le',
        'linux/s390x',
        'linux/386',
    ],
)
def test_container_configuration_removing_one_platform(
    container_configuration_default_model: ContainerConfiguration,
    platform_name: str,
) -> None:
    """Test the container configuration removing one platform.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
        platform_name (str): The name of the platform to remove.
    """
    container_configuration_default_model.add_platforms(platform_name)
    assert container_configuration_default_model.platforms == [
        platform_name.lower()
    ]
    container_configuration_default_model.remove_platforms(platform_name)
    assert container_configuration_default_model.platforms == []


@pytest.mark.parametrize(
    'platforms',
    [
        ['linux/amd64', 'linux/arm64'],
        ['linux/arm/v7', 'linux/arm/v6'],
        ['linux/ppc64le', 'linux/s390x', 'linux/386'],
    ],
)
def test_container_configuration_removing_platforms(
    container_configuration_default_model: ContainerConfiguration,
    platforms: list[str],
) -> None:
    """Test the container configuration removing multiple platforms.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
        platforms (list[str]): The list of platforms to remove.
    """
    container_configuration_default_model.add_platforms(platforms)
    assert sorted(container_configuration_default_model.platforms) == sorted(
        [platform_name.lower() for platform_name in platforms]
    )
    container_configuration_default_model.remove_platforms(platforms)
    assert container_configuration_default_model.platforms == []


@pytest.mark.parametrize(
    'platform_name',
    ['platform', 'linux', 'my platform', 'arm64', 'intel'],
)
def test_container_configuration_adding_invalid_platform(
    container_configuration_default_model: ContainerConfiguration,
    platform_name: str,
) -> None:
    """Test the container configuration adding invalid platform.

    Args:
        container_configuration_default_model (ContainerConfiguration): The
            container configuration model to test.
        platform_name (str): The name of the platform to add.
    """
    with pytest.raises(InvalidPlatformError):
        container_configuration_default_model.add_platforms(platform_name)
