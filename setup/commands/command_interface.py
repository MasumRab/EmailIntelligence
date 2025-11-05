"""
Command Interface for SOLID launch system.

This module defines the Command interface following the Command design pattern.
All launch commands must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from argparse import Namespace


class Command(ABC):
    """
    Abstract base class for all launch commands.

    This interface defines the contract that all commands must follow,
    enabling polymorphic command execution and proper dependency injection.
    """

    def __init__(self, args: Namespace, container: 'ServiceContainer'):
        """
        Initialize command with arguments and service container.

        Args:
            args: Parsed command line arguments
            container: Service container for dependency injection
        """
        self.args = args
        self.container = container

    @abstractmethod
    def execute(self) -> int:
        """
        Execute the command.

        Returns:
            int: Exit code (0 for success, non-zero for failure)
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        Get human-readable description of the command.

        Returns:
            str: Command description
        """
        pass

    def validate_args(self) -> bool:
        """
        Validate command arguments.

        Returns:
            bool: True if arguments are valid
        """
        return True

    def cleanup(self) -> None:
        """
        Cleanup resources after command execution.
        """
        pass