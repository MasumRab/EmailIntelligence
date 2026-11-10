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

        Args:
            dependencies: Dictionary of dependency names to instances
        """
        self._missing_deps = []
        for name in self.get_dependencies():
            if name in dependencies and isinstance(dependencies[name], str):
                self._missing_deps.append((name, dependencies[name]))

        # Store for subclasses
        self._injected_dependencies = dependencies

    def check_dependencies(self) -> int:
        """
        Check if all dependencies were successfully injected.

        Returns:
            int: 0 if all dependencies are present, 1 otherwise
        """
        if hasattr(self, "_missing_deps") and self._missing_deps:
            print(f"Error: Command '{self.name}' is missing required dependencies:")
            for name, reason in self._missing_deps:
                print(f"  - {name}: {reason}")
            return 1
        return 0
