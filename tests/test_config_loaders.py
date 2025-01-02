"""Module with tests for the ConfigLoader."""

from pathlib import Path

from slough_config import ConfigLoader, JSONLoader, YAMLLoader


def test_config_loader_registration() -> None:
    """Test that the ConfigLoader has the correct loaders registered."""
    assert ConfigLoader.loaders == {
        'yml': YAMLLoader,
        'yaml': YAMLLoader,
        'json': JSONLoader,
    }


def test_config_loader_yaml_loader() -> None:
    """Test that the YAMLLoader can load a YAML file."""
    cfgfile = Path('tests/test_data/project1/slough.yml')
    loader = YAMLLoader(cfgfile)
    config = loader.load_config()
    assert config.model_dump() == {
        'project': {
            'name': 'project1',
            'version': '0.0.1',
            'authors': [
                {'name': 'John Doe', 'email': 'johndoe@example.com'},
                {'name': 'Daryl Stark', 'email': 'darylstark@example.com'},
            ],
        }
    }


def test_config_lodaer_json_loader() -> None:
    """Test that the JSONLoader can load a JSON file."""
    cfgfile = Path('tests/test_data/project5/slough.json')
    loader = JSONLoader(cfgfile)
    config = loader.load_config()
    assert config.model_dump() == {
        'project': {
            'name': 'project5',
            'version': '0.0.1',
            'authors': [
                {'name': 'John Doe', 'email': 'johndoe@example.com'},
                {'name': 'Daryl Stark', 'email': 'darylstark@example.com'},
            ],
        }
    }
