"""Package for Slough to manage configuration.

Will be used by the CLI tool to load configuration and can be used by any
other Python script that needs to load configuration from a Slough enabled
project.
"""

from .config_manager import ConfigManager
from .config_model import (
    Author,
    ConfigProfile,
    ContainerConfiguration,
    DevelopmentEnvironment,
    ProjectInformation,
    SloughConfig,
)
from .json_manager import JSONManager
from .yaml_manager import YAMLManager

__all__ = [
    'Author',
    'ConfigManager',
    'ConfigProfile',
    'ContainerConfiguration',
    'DevelopmentEnvironment',
    'JSONManager',
    'ProjectInformation',
    'SloughConfig',
    'YAMLManager',
]
