"""
CLI Commands Package

This package provides a modular command system following SOLID principles.
Commands are organized as individual classes with dependency injection.
"""

# Command implementations
from .analyze_command import AnalyzeCommand
from .analyze_history_command import AnalyzeHistoryCommand
from .factory import CommandFactory
from .interface import Command
from .plan_rebase_command import PlanRebaseCommand
from .registry import CommandRegistry
from .resolve_command import ResolveCommand
from .validate_command import ValidateCommand

__all__ = [
    # Core architecture
    "Command",
    "CommandFactory",
    "CommandRegistry",
    # Command implementations
    "AnalyzeCommand",
    "ResolveCommand",
    "ValidateCommand",
    "AnalyzeHistoryCommand",
    "PlanRebaseCommand",
]
