"""Package for Slough to manage configuration.

Will be used by the CLI tool to load configuration and can be used by any
other Python script that needs to load configuration from a Slough enabled
project.
"""

from .config_file_finder import ConfigFileFinder
from .config_manager import ConfigManager
from .config_model import Author, ProjectInformation, SloughConfig
from .json_manager import JSONManager
from .yaml_manager import YAMLManager

__all__ = [
    'Author',
    'ConfigFileFinder',
    'ConfigManager',
    'JSONManager',
    'ProjectInformation',
    'SloughConfig',
    'YAMLManager',
]
