"""
CLI Commands Package

This package provides a modular command system following SOLID principles.
Commands are organized as individual classes with dependency injection.
"""

from .factory import CommandFactory
from .interface import Command
from .registry import CommandRegistry

# Command implementations
from .analyze_command import AnalyzeCommand
from .resolve_command import ResolveCommand
from .validate_command import ValidateCommand
from .analyze_history_command import AnalyzeHistoryCommand
from .plan_rebase_command import PlanRebaseCommand
from .identify_command import IdentifyCommand
from .automation.mcp_sync import MCPSyncCommand
from .automation.monitor import MonitorCommand
from .guide import GuideCommand
from .ide import IDECommand
from .infra.deploy import DeployCommand
from .infra.backup import BackupCommand
from .infra.install_tools import InstallToolsCommand
from .infra.verify import VerifyCommand

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
    "IdentifyCommand",
    "MCPSyncCommand",
    "MonitorCommand",
    "GuideCommand",
    "IDECommand",
    "DeployCommand",
    "BackupCommand",
    "InstallToolsCommand",
    "VerifyCommand",
]
