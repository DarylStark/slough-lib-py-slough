"""Module with a interface for a ConfigLoader."""

from abc import ABC, abstractmethod


class ConfigLoader(ABC):
    """Interface for a ConfigLoader."""

    @abstractmethod
    def load_config(self) -> dict:
        """Abstract method that loads the config.

        Should return a dictionary with the configuration.

        Returns:
            dict: The configuration.
        """
