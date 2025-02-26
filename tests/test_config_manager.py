"""Module with tests for the ConfigManager."""

from pathlib import Path

from slough_config import ConfigManager, JSONManager, YAMLManager


def test_config_manager_registration() -> None:
    """Test that the ConfigManager has the correct managers registered."""
    assert ConfigManager.managers == {
        'yml': YAMLManager,
        'yaml': YAMLManager,
        'json': JSONManager,
    }


def test_config_manager_yaml_manager() -> None:
    """Test that the YAMLManager can load a YAML file."""
    cfgfile = Path('tests/test_data/project1/slough.yml')
    manager = YAMLManager(cfgfile)
    config = manager.load_config()
    assert config is not None
    assert config.model_dump() == {
        'project': {
            'name': 'project1',
            'version': '0.0.1',
            'authors': [
                {'name': 'John Doe', 'email': 'johndoe@example.com'},
                {'name': 'Daryl Stark', 'email': 'darylstark@example.com'},
            ],
        },
        'development_environment': 'python-generic',
        'cfg_profiles': {
            '_default': {'container': None},
            '_all': {'container': None},
        },
    }


def test_config_lodaer_json_manager() -> None:
    """Test that the JSONManager can load a JSON file."""
    cfgfile = Path('tests/test_data/project5/slough.json')
    manager = JSONManager(cfgfile)
    config = manager.load_config()
    assert config is not None
    assert config.model_dump() == {
        'project': {
            'name': 'project5',
            'version': '0.0.1',
            'authors': [
                {'name': 'John Doe', 'email': 'johndoe@example.com'},
                {'name': 'Daryl Stark', 'email': 'darylstark@example.com'},
            ],
        },
        'development_environment': 'nodejs-generic',
        'cfg_profiles': {
            '_default': {'container': None},
            '_all': {'container': None},
        },
    }


def test_config_lodaer_yaml_no_file() -> None:
    """Test that the YAMLManager returns empty dict on a non-existing file."""
    cfgfile = Path('tests/test_data/non-existing.yaml')
    manager = YAMLManager(cfgfile)
    config = manager.load_config()
    assert config is None


def test_config_lodaer_json_no_file() -> None:
    """Test that the JSONManager returns empty dict on a non-existing file."""
    cfgfile = Path('tests/test_data/non-existing.json')
    manager = YAMLManager(cfgfile)
    config = manager.load_config()
    assert config is None
