"""Tests for the ConfigFileFinder."""

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from slough.config_file_finder import ConfigFileFinder


@pytest.fixture(scope='function')
def temp_folder() -> Generator[Path]:
    """Create a temporary folder for testing.

    Creates a temporary directory with a random name. Removes it after the test
    is done.
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname).resolve()


def test_config_file_finder_no_config_file(temp_folder: Path) -> None:
    """Test the ConfigFileFinder when there is no file present."""
    assert (
        ConfigFileFinder(
            'slough.yml', working_dir=temp_folder, max_directory_depth=1
        ).find()
        is None
    )


def test_config_file_finder_existing_file_root(temp_folder: Path) -> None:
    """Test the ConfigFileFinder with a file in the root."""
    config_file = temp_folder / 'slough.yml'
    config_file.touch()
    assert (
        ConfigFileFinder(
            'slough.yml', working_dir=temp_folder, max_directory_depth=1
        ).find()
        == config_file.resolve()
    )


def test_config_file_finder_existing_file_subdir(temp_folder: Path) -> None:
    """Test the ConfigFileFinder when cwd is in a subdirectory."""
    subdir = temp_folder / 'subdir'
    subdir.mkdir()
    config_file = temp_folder / 'slough.yml'
    config_file.touch()
    assert (
        ConfigFileFinder(
            'slough.yml', working_dir=subdir, max_directory_depth=2
        ).find()
        == config_file.resolve()
    )


def test_config_file_finder_existing_file_three_deep_subdir(
    temp_folder: Path,
) -> None:
    """Test the ConfigFileFinder when cwd is in a three deep subdirectory."""
    subdir = temp_folder / 'subdir' / 'subdir' / 'subdir'
    subdir.mkdir(parents=True)
    config_file = temp_folder / 'slough.yml'
    config_file.touch()
    assert (
        ConfigFileFinder(
            'slough.yml', working_dir=subdir, max_directory_depth=4
        ).find()
        == config_file.resolve()
    )
