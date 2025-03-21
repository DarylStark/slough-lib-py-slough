"""Module with Mocks for the tests."""

from slough import StorageManager
from slough_config.config_model import SloughConfig


class MockStorageManager(StorageManager):
    """Mock StorageManager for unit testing.

    This class is used to test the Slough class without the need to interact
    with the filesystem.

    The configuration to test with is given in the constructor. The `load`
    method will return the configuration given in the constructor. The `save`
    method will udpate the configuration given in the constructor.
    """

    def __init__(self, config: SloughConfig) -> None:
        """Initialize the MockStorageManager.

        Args:
            config (SloughConfig): The configuration to use.
        """
        self._cached_config = config

    def save(self, data: SloughConfig) -> None:
        """Save the configuration to nothing.

        Args:
            data (SloughConfig): The configuration to save.
        """
        self._cached_config = data

    def load(self) -> SloughConfig:
        """Load the configuration.

        Returns:
            SloughConfig: The configuration given in the constructor.
        """
        return self._cached_config
