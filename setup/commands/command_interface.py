"""
Command interface definition.

This module defines the base Command interface that all commands should implement.
"""

from abc import ABC, abstractmethod
from argparse import Namespace
from typing import Optional


class Command(ABC):
    """
    Abstract base class for commands.
    
    All commands should inherit from this class and implement the required methods.
    """

    def __init__(self, args: Namespace = None):
        """
        Initialize the command with arguments.
        
        Args:
            args: Parsed command-line arguments
        """
        self.args = args

    @abstractmethod
    def get_description(self) -> str:
        """
        Get the command description.
        
        Returns:
            Command description
        """
        pass

    @abstractmethod
    def validate_args(self) -> bool:
        """
        Validate command arguments.
        
        Returns:
            True if arguments are valid, False otherwise
        """
        pass

    @abstractmethod
    def execute(self) -> int:
        """
        Execute the command.
        
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        pass

    def cleanup(self) -> None:
        """
        Cleanup resources after command execution.
        """
        pass