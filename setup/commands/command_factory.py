"""
Command factory implementation.

This module provides a factory for creating command instances based on command names.
"""

from argparse import Namespace
from typing import Optional

from .command_interface import Command
from .setup_command import SetupCommand
from .run_command import RunCommand
from .test_command import TestCommand
from .check_command import CheckCommand
from .cleanup_command import CleanupCommand
from .guide_dev_command import GuideDevCommand
from .guide_pr_command import GuidePrCommand


class CommandFactory:
    """
    Factory class for creating command instances.
    
    This factory maps command names to their corresponding command classes
    and creates instances with the provided arguments.
    """

    def __init__(self):
        """Initialize the command factory with available commands."""
        self._commands = {
            'setup': SetupCommand,
            'run': RunCommand,
            'test': TestCommand,
            'check': CheckCommand,
            'cleanup': CleanupCommand,
            'guide-dev': GuideDevCommand,
            'guide-pr': GuidePrCommand,
        }

    def create_command(self, command_name: str, args: Namespace) -> Optional[Command]:
        """
        Create a command instance based on the command name.
        
        Args:
            command_name: Name of the command to create
            args: Parsed command-line arguments
            
        Returns:
            Command instance or None if command is not found
        """
        command_class = self._commands.get(command_name)
        if command_class is None:
            return None
            
        command = command_class(args)
        return command

    def get_available_commands(self) -> list:
        """
        Get a list of available command names.
        
        Returns:
            List of available command names
        """
        return list(self._commands.keys())

    def get_command_description(self, command_name: str) -> str:
        """
        Get the description of a command.
        
        Args:
            command_name: Name of the command
            
        Returns:
            Description of the command or empty string if not found
        """
        command_class = self._commands.get(command_name)
        if command_class is None:
            return ""
            
        # Create a temporary instance to get the description
        try:
            command = command_class()
            return command.get_description()
        except Exception:
            return ""


# Global factory instance
_command_factory = None


def get_command_factory() -> CommandFactory:
    """
    Get the global command factory instance.
    
    Returns:
        CommandFactory instance
    """
    global _command_factory
    if _command_factory is None:
        _command_factory = CommandFactory()
    return _command_factory