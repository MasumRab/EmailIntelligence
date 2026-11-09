"""
Command Factory Module

Implements the Factory pattern for creating command instances.
This factory manages command creation and provides dependency injection.
"""

from typing import Any, Dict, Optional, Type

from .interface import Command


class CommandFactory:
    """
    Factory for creating command instances with dependency injection.

    This factory pattern implementation allows for:
    - Centralized command creation
    - Dependency injection for all commands
    - Easy testing with mocked dependencies
    - Consistent initialization across commands
    """

    def __init__(self, dependencies: Optional[Dict[str, Any]] = None):
        """
        Initialize the command factory.

        Args:
            dependencies: Global dependencies available to all commands
        """
        self._dependencies = dependencies or {}
        self._command_classes: Dict[str, Type[Command]] = {}

    def register_command(self, command_class: Type[Command]) -> None:
        """
        Register a command class with the factory.

        Args:
            command_class: The command class to register
        """
        command_instance = command_class()
        self._command_classes[command_instance.name] = command_class

    def create_command(self, command_name: str) -> Optional[Command]:
        """
        Create an instance of the specified command.

        Args:
            command_name: Name of the command to create

        Returns:
            Command instance or None if command not found
        """
        command_class = self._command_classes.get(command_name)
        if not command_class:
            return None

        # Create command instance
        command = command_class()

        # Inject dependencies
        command_dependencies = command.get_dependencies()
        resolved_dependencies = {}

        for dep_name, dep_type in command_dependencies.items():
            if dep_name in self._dependencies:
                resolved_dependencies[dep_name] = self._dependencies[dep_name]
            else:
                # Try to create dependency if it's a class
                if isinstance(dep_type, type):
                    try:
                        resolved_dependencies[dep_name] = dep_type()
                    except Exception:
                        # If we can't create it, it will be None
                        resolved_dependencies[dep_name] = None
                else:
                    resolved_dependencies[dep_name] = None

        # Set dependencies on command (if it supports it)
        if hasattr(command, "set_dependencies"):
            command.set_dependencies(resolved_dependencies)

        return command

    def get_available_commands(self) -> Dict[str, str]:
        """
        Get all available commands with their descriptions.

        Returns:
            Dict mapping command names to descriptions
        """
        commands = {}
        for command_class in self._command_classes.values():
            command_instance = command_class()
            commands[command_instance.name] = command_instance.description
        return commands

    def has_command(self, command_name: str) -> bool:
        """
        Check if a command is registered.

        Args:
            command_name: Name of the command to check

        Returns:
            True if command exists, False otherwise
        """
        return command_name in self._command_classes
