"""Tests for the config finder."""

from pathlib import Path

import pytest

from slough_config import ConfigFileFinder


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
def test_config_file_finder_root_yml(
    directory: str, expected_file: str
) -> None:
    """Test the config file finder.

    Args:
        directory (str): Test data directory.
        expected_file (str): Expected config file name.
    """
    finder = ConfigFileFinder(
        working_dir=Path() / 'tests' / 'test_data' / directory,
        max_directory_depth=0,
    )
    expected_path = Path(f'tests/test_data/{directory}/{expected_file}')
    assert finder.find_config_file() is not None
    assert finder.find_config_file() == expected_path.resolve()


@pytest.mark.parametrize(
    'max_depth', (0, 1, 2), ids=['Current dir', 'One deep', 'Two deep']
)
def test_config_file_finder_root_parent_dir_too_deep(max_depth: int) -> None:
    """Test the config file finder.

    Args:
        max_depth (int): Maximum directory depth.
    """
    finder = ConfigFileFinder(
        working_dir=Path()
        / 'tests'
        / 'test_data'
        / 'project1'
        / 'subdir/subdir/subdir',
        max_directory_depth=max_depth,
    )
    assert finder.find_config_file() is None


@pytest.mark.parametrize(
    'max_depth', (0, 1, 2), ids=['Current dir', 'One deep', 'Two deep']
)
def test_config_file_finder_subdir_parent_dir_too_deep(max_depth: int) -> None:
    """Test the config file finder.

    Args:
        max_depth (int): Maximum directory
    """
    finder = ConfigFileFinder(
        working_dir=Path()
        / 'tests'
        / 'test_data'
        / 'project3'
        / 'subdir/subdir/subdir',
        max_directory_depth=max_depth,
    )
    assert finder.find_config_file() is None


@pytest.mark.parametrize(
    'max_depth',
    (3, 4, 5, 6, 7),
    ids=['Three deep', 'Four deep', 'Five deep', 'Six deep', 'Seven deep'],
)
def test_config_file_finder_root_parent_dir(max_depth: int) -> None:
    """Test the config file finder.

    Args:
        max_depth (int): Maximum directory depth.
    """
    finder = ConfigFileFinder(
        working_dir=Path()
        / 'tests'
        / 'test_data'
        / 'project1'
        / 'subdir/subdir/subdir',
        max_directory_depth=max_depth,
    )
    expected_path = Path('tests/test_data/project1/slough.yml')
    assert finder.find_config_file() == expected_path.resolve()


@pytest.mark.parametrize(
    'max_depth',
    (3, 4, 5),
    ids=['Three deep', 'Four deep', 'Five deep'],
)
def test_config_file_finder_subdir_parent_dir(max_depth: int) -> None:
    """Test the config file finder.

    Args:
        max_depth (int): Maximum directory depth.
    """
    finder = ConfigFileFinder(
        working_dir=Path()
        / 'tests'
        / 'test_data'
        / 'project3'
        / 'subdir/subdir/subdir',
        max_directory_depth=max_depth,
    )
    expected_path = Path('tests/test_data/project3/.slough/slough.yml')
    assert finder.find_config_file() == expected_path.resolve()
