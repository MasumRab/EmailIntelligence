"""
Command Factory for creating launch commands.

This module implements the Factory pattern to create command instances
based on command names, promoting loose coupling and extensibility.
"""

from typing import Dict, Type, Optional
import logging
from argparse import Namespace

from .command_interface import Command
from .setup_command import SetupCommand
from .run_command import RunCommand
from .test_command import TestCommand

logger = logging.getLogger(__name__)


class CommandFactory:
    """
    Factory for creating command instances.

    Registers command classes and creates instances with proper
    dependency injection through the service container.
    """

    def __init__(self):
        self._commands: Dict[str, Type[Command]] = {}

        # Register built-in commands
        self.register_command('setup', SetupCommand)
        self.register_command('run', RunCommand)
        self.register_command('test', TestCommand)

    def register_command(self, name: str, command_class: Type[Command]) -> None:
        """
        Register a command class.

        Args:
            name: Command name
            command_class: Command class to register
        """
        self._commands[name] = command_class
        logger.debug(f"Registered command: {name}")

    def create_command(self, name: str, args: Namespace) -> Optional[Command]:
        """
        Create a command instance.

        Args:
            name: Command name
            args: Parsed command line arguments

        Returns:
            Command instance or None if command not found
        """
        if name not in self._commands:
            logger.error(f"Unknown command: {name}")
            return None

        command_class = self._commands[name]

        try:
            # Import container here to avoid circular imports
            from ..container import get_container
            container = get_container()

            command = command_class(args, container)
            logger.debug(f"Created command: {name}")
            return command
        except Exception as e:
            logger.error(f"Failed to create command '{name}': {e}")
            return None

    def get_available_commands(self) -> Dict[str, str]:
        """
        Get available commands with their descriptions.

        Returns:
            Dict mapping command names to descriptions
        """
        descriptions = {}
        for name, command_class in self._commands.items():
            try:
                # Create a dummy instance to get description
                dummy_args = Namespace()
                from ..container import get_container
                container = get_container()
                dummy_command = command_class(dummy_args, container)
                descriptions[name] = dummy_command.get_description()
            except Exception:
                descriptions[name] = f"{name} command"

        return descriptions

    def has_command(self, name: str) -> bool:
        """
        Check if a command is registered.

        Args:
            name: Command name

        Returns:
            bool: True if command is registered
        """
        return name in self._commands


# Global command factory instance
_factory: Optional[CommandFactory] = None


def get_command_factory() -> CommandFactory:
    """Get the global command factory instance."""
    global _factory
    if _factory is None:
        _factory = CommandFactory()
    return _factory