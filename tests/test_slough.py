"""Tests for the Slough module."""

from pathlib import Path

import pytest

from slough import Slough


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
    """Test that the correct configuration file is set by default."""
    monkeypatch.chdir(f'tests/test_data/{directory}')
    slough = Slough()
    assert slough.cfgfile is not None
    assert slough.cfgfile == Path(expected_file)


@pytest.mark.parametrize(
    'directory, expected_file',
    (
        ('project1', 'slough.yml'),
        ('project3', '.slough/slough.yaml'),
    ),
    ids=[
        'project1-subdir-slough-yml',
        'project3-subdir-slough-yml',
    ],
)
def test_correct_configuration_file_slough_subdir(
    monkeypatch: pytest.MonkeyPatch, directory: str, expected_file: str
) -> None:
    """Test that the correct configuration file is set by default."""
    monkeypatch.chdir(f'tests/test_data/{directory}/subdir/subdir/subdir')
    slough = Slough()
    assert slough.cfgfile is not None
    assert slough.cfgfile == Path(f'../../../{expected_file}')
