"""A Abstract Factory for creating CLI commands."""

import logging
from abc import ABC, abstractmethod
from pathlib import Path

from slough.slough import Slough
from slough.yaml_storage_manager import YAMLStorageManager
from slough_cli_tool.cli_output_visitor import CLIOutputVisitor, ConsoleOutput


class CLIFactory(ABC):
    """Abstract Factory for creating CLI commands."""

    @abstractmethod
    def get_logger(self) -> logging.Logger:
        """Create a logger.

        Returns:
            Logger: The created logger.
        """

    @abstractmethod
    def get_slough_object(self) -> Slough:
        """Create a Slough object.

        Returns:
            Slough: Slough object.
        """

    @abstractmethod
    def get_output_visitor(self) -> CLIOutputVisitor:
        """Create an output visitor.

        Returns:
            CLIOutputVisitor: The created output visitor.
        """


class SloughCLIFactory(CLIFactory):
    """Concrete Factory for creating Slough CLI commands."""

    def __init__(self, cfg_file_path: Path) -> None:
        """Initialize the Slough CLI factory."""
        self._cfg_file_path: Path = cfg_file_path

    def get_logger(self) -> logging.Logger:
        """Create a logger.

        Returns:
            logging.Logger: The created logger.
        """
        cli_logger = logging.getLogger('cli')
        return cli_logger

    def get_slough_object(self) -> Slough:
        """Create a Slough object.

        Returns:
            Slough: Slough object.
        """
        # Create a Slough object
        return Slough(storage_manager=YAMLStorageManager(self._cfg_file_path))

    def get_output_visitor(self) -> CLIOutputVisitor:
        """Create an output visitor.

        Returns:
            CLIOutputVisitor: The created output visitor.
        """
        # Create a ConsoleOutputVisitor
        return ConsoleOutput()
