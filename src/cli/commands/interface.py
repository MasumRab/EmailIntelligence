"""
Command Interface Module

Defines the abstract base class for all CLI commands following SOLID principles.
This interface establishes the contract that all commands must implement.
"""

from abc import ABC, abstractmethod
from argparse import Namespace
from typing import Any, Dict


class Command(ABC):
    """
    Abstract base class for all CLI commands.

    This interface defines the contract that all commands must follow,
    ensuring consistency across the command system and enabling the factory
    pattern for command creation and execution.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The command name used for CLI invocation.

        Returns:
            str: Command name (e.g., 'analyze', 'resolve')
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Human-readable description of what the command does.

        Returns:
            str: Description for help text
        """
        pass

    @abstractmethod
    def add_arguments(self, parser: Any) -> None:
        """
        Add command-specific arguments to the argument parser.

        Args:
            parser: Subparser for this command
        """
        pass

    @abstractmethod
    async def execute(self, args: Namespace) -> int:
        """
        Execute the command with parsed arguments.

        Args:
            args: Parsed command-line arguments

        Returns:
            int: Exit code (0 for success, non-zero for failure)
        """
        pass

    @abstractmethod
    def get_dependencies(self) -> Dict[str, Any]:
        """
        Get the dependencies required by this command.

        Returns:
            Dict[str, Any]: Dictionary of dependency names to instances
        """
        pass

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """
        Set the dependencies for this command.

        This method can be overridden by concrete implementations
        to store injected dependencies.

        Args:
            dependencies: Dictionary of dependency names to instances
        """
        # Default implementation does nothing
        # Concrete classes can override this to store dependencies
        pass
