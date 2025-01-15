"""Tests for the Slough module."""

from pathlib import Path

import pytest

from slough import Slough
from slough.exceptions import (
    ConfigAlreadySetError,
    ConfigFileNotSetError,
    ConfigManagerNotRegisteredError,
    ConfigNotSetError,
)
from slough_config.config_model import ProjectInformation, SloughConfig


def test_correct_configuration_file_static() -> None:
    """Test that the correct configuration file is set when configured."""
    slough = Slough(cfgfile='tests/data/config.yaml')
    assert slough.cfgfile is not None
    assert slough.cfgfile == Path('tests/data/config.yaml')


@pytest.mark.parametrize(
    'directory, expected_file',
    (
        ('project1', 'slough.yml'),
        ('project2', 'slough.yaml'),
        ('project3', '.slough/slough.yml'),
        ('project4', '.slough/slough.yaml'),
        ('project5', 'slough.json'),
        ('project6', '.slough/slough.json'),
    ),
    ids=[
        'project1-root-slough-yml',
        'project2-root-slough-yaml',
        'project3-subdir-slough-yml',
        'project3-subdir-slough-yaml',
        'project4-root-slough-json',
        'project5-subdir-slough-json',
    ],
)
def test_correct_configuration_file_slough_root(
    monkeypatch: pytest.MonkeyPatch, directory: str, expected_file: str
) -> None:
    """Test that the correct configuration file is set by default.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        directory (str): Test data directory.
        expected_file (str): Expected config file name.
    """
    monkeypatch.chdir(f'tests/test_data/{directory}')
    slough = Slough(max_directory_depth=0)
    assert slough.cfgfile is not None
    assert slough.cfgfile == Path(expected_file).resolve()


@pytest.mark.parametrize(
    'directory, expected_file',
    (
        ('project1', 'slough.yml'),
        ('project3', '.slough/slough.yml'),
    ),
    ids=[
        'project1-subdir-slough-yml',
        'project3-subdir-slough-yml',
    ],
)
def test_correct_configuration_file_slough_subdir(
    monkeypatch: pytest.MonkeyPatch, directory: str, expected_file: str
) -> None:
    """Test that the correct configuration file is set by default.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
        directory (str): Test data directory.
        expected_file (str): Expected config file name.
    """
    monkeypatch.chdir(f'tests/test_data/{directory}/subdir/subdir/subdir')
    slough = Slough(max_directory_depth=3)
    assert slough.cfgfile is not None
    assert slough.cfgfile == Path(f'../../../{expected_file}').resolve()


def test_config_retrieval(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that the configuration is loaded.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
    """
    monkeypatch.chdir('tests/test_data/project1')
    slough = Slough(max_directory_depth=0)
    assert slough.config is not None
    assert slough.config.project.name == 'project1'
    assert slough.config.project.version == '0.0.1'


def test_config_retrieval_empty_file(empty_test_dir: Path) -> None:
    """Test if we get a None object when no configu exists.

    Args:
        empty_test_dir (Path): Path to the empty test directory
    """
    slough = Slough(max_directory_depth=0)
    assert slough.config is None


def test_config_set_config_empty_project(empty_test_dir: Path) -> None:
    """Test if we can set a config when there is None.

    Args:
        empty_test_dir (Path): Path to the empty test directory
    """
    slough = Slough(max_directory_depth=0)
    slough.config = SloughConfig(
        project=ProjectInformation(
            name='empty_project', version='0.0.1', authors=[]
        )
    )
    assert slough.config.project.name == 'empty_project'
    assert slough.config.project.version == '0.0.1'


def test_config_set_config(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test if we can get an error when overwriting a config.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
    """
    monkeypatch.chdir('tests/test_data/project1')
    slough = Slough(max_directory_depth=0)
    with pytest.raises(ConfigAlreadySetError):
        slough.config = SloughConfig(
            project=ProjectInformation(
                name='empty_project', version='0.0.1', authors=[]
            )
        )


def test_config_save_config_empty_project(empty_test_dir: Path) -> None:
    """Test if we get on error on saving a empty config.

    Args:
        empty_test_dir (Path): Path to the empty test directory
    """
    slough = Slough(max_directory_depth=0)
    with pytest.raises(ConfigNotSetError):
        slough.save()


def test_config_save_config_yaml(empty_test_dir: Path) -> None:
    """Test if saving the config works for YAML files.

    Args:
        empty_test_dir (Path): Path to the empty test directory
    """
    # Save the config
    slough = Slough(cfgfile='test-config.yml')
    slough.config = SloughConfig(
        project=ProjectInformation(
            name='empty_project', version='0.0.1', authors=[]
        )
    )
    slough.save()

    # Load the config
    slough = Slough(cfgfile='test-config.yml')
    assert slough.config is not None
    assert slough.config.project.name == 'empty_project'
    assert slough.config.project.version == '0.0.1'


def test_config_save_config_json(empty_test_dir: Path) -> None:
    """Test if saving the config works for JSON files.

    Args:
        empty_test_dir (Path): Path to the empty test directory
    """
    # Save the config
    slough = Slough(cfgfile='test-config.json')
    slough.config = SloughConfig(
        project=ProjectInformation(
            name='empty_project', version='0.0.1', authors=[]
        )
    )
    slough.save()

    # Load the config
    slough = Slough(cfgfile='test-config.json')
    assert slough.config is not None
    assert slough.config.project.name == 'empty_project'
    assert slough.config.project.version == '0.0.1'


def test_wrong_configfile_extensions() -> None:
    """Test if we get an error when the cfg file extension is not supported.

    Args:
        empty_test_dir (Path): Path to the empty test directory
    """
    slough = Slough(cfgfile='test-config.wrong-extension')
    with pytest.raises(ConfigManagerNotRegisteredError):
        _ = slough.config


def test_error_when_no_config_file_is_set() -> None:
    """Test if we get an error when the cfg file extension is not supported.

    Args:
        empty_test_dir (Path): Path to the empty test directory
    """
    slough = Slough()
    slough.cfgfile = None
    with pytest.raises(ConfigFileNotSetError):
        _ = slough.config
