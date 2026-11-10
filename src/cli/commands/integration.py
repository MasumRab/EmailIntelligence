"""
CLI Commands Integration Module

Provides centralized factory setup, command registration, and CLI dispatch.
This module bridges the modular command system with the CLI entry point.
"""

import asyncio
from typing import Any, Dict, Optional

from .factory import CommandFactory
from .registry import CommandRegistry


def create_default_dependencies() -> Dict[str, Any]:
    """
    Create default dependencies for all commands.

    Returns:
        Dict mapping dependency names to instances or error strings
    """
    dependencies = {}

    def try_import(name, factory_func):
        try:
            dependencies[name] = factory_func()
        except ImportError as e:
            dependencies[name] = f"Missing dependency: {str(e)}"
        except Exception as e:
            dependencies[name] = f"Error initializing dependency: {str(e)}"

    def _create_worktree():
        from ...git.worktree import WorktreeManager

        return WorktreeManager()

    try_import("worktree_manager", _create_worktree)

    def _create_conflict():
        from ...git.conflict_detector import GitConflictDetector

        return GitConflictDetector()

    try_import("conflict_detector", _create_conflict)

    def _create_repo():
        from ...git.repository import RepositoryOperations

        return RepositoryOperations

    try_import("repository_ops", _create_repo)

    def _create_analyzer():
        from ...analysis.constitutional.analyzer import ConstitutionalAnalyzer

        return ConstitutionalAnalyzer()

    try_import("analyzer", _create_analyzer)

    def _create_strategy():
        from ...strategy.generator import StrategyGenerator

        return StrategyGenerator()

    try_import("strategy_generator", _create_strategy)

    def _create_resolver():
        from ...resolution.auto_resolver import AutoResolver

        return AutoResolver()

    try_import("resolver", _create_resolver)

    def _create_validator():
        from ...validation.validator import Validator

        return Validator()

    try_import("validator", _create_validator)

    def _create_history():
        from ...git.history import GitHistory

        return GitHistory()

    try_import("history", _create_history)

    def _create_classifier():
        from ...git.history import CommitClassifier

        return CommitClassifier()

    try_import("classifier", _create_classifier)

    def _create_planner():
        from ...strategy.reordering import RebasePlanner

        return RebasePlanner()

    try_import("planner", _create_planner)

    return dependencies


def create_command_factory(
    dependencies: Optional[Dict[str, Any]] = None,
) -> CommandFactory:
    """
    Create and configure the command factory with dependencies.

    Args:
        dependencies: Optional pre-configured dependencies

    Returns:
        Configured CommandFactory instance
    """
    deps = dependencies or create_default_dependencies()
    return CommandFactory(deps)


def create_registry(factory: Optional[CommandFactory] = None) -> CommandRegistry:
    """
    Create and populate the command registry with all commands.

    Args:
        factory: Optional pre-configured factory

    Returns:
        Configured CommandRegistry with all commands registered
    """
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

    cmd_factory = factory or create_command_factory()
    registry = CommandRegistry(cmd_factory)

    # Register all commands with agent assignments
    registry.register_command(AnalyzeCommand, "agent-2")
    registry.register_command(ResolveCommand, "agent-3")
    registry.register_command(ValidateCommand, "agent-4")
    registry.register_command(AnalyzeHistoryCommand, "agent-5")
    registry.register_command(PlanRebaseCommand, "agent-5")
    registry.register_command(IdentifyCommand, "agent-5")

    # Extracted commands
    registry.register_command(MCPSyncCommand, agent="automation")
    registry.register_command(MonitorCommand, agent="automation")
    registry.register_command(GuideCommand, agent="docs")
    registry.register_command(IDECommand, agent="developer")
    registry.register_command(DeployCommand, agent="infra")
    registry.register_command(BackupCommand, agent="infra")
    registry.register_command(InstallToolsCommand, agent="infra")
    registry.register_command(VerifyCommand, agent="infra")

    return registry


def get_command_dispatcher(registry: Optional[CommandRegistry] = None):
    """
    Create a dispatcher function for CLI entry point.

    Args:
        registry: Optional pre-configured registry

    Returns:
        Dispatcher function that takes command_name and args, returns exit code
    """
    active_registry = registry or create_registry()
    deps_state = create_default_dependencies()

    def dispatch(command_name: str, args) -> int:
        """
        Dispatch a command by name.

        Args:
            command_name: Name of the command to execute
            args: Parsed command line arguments

        Returns:
            int: Exit code from the command
        """
        try:
            command = active_registry.get_command(command_name)

            missing = [
                (n, deps_state[n])
                for n in command.get_dependencies()
                if isinstance(deps_state.get(n), str)
            ]
            if missing:
                print(
                    f"Error: '{command_name}' cannot run — required dependencies are unavailable:"
                )
                for name, reason in missing:
                    print(f"  - {name}: {reason}")
                return 2

            # Check if command's execute method is a coroutine function
            import inspect

            if inspect.iscoroutinefunction(command.execute):
                return asyncio.run(command.execute(args))
            else:
                return command.execute(args)
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Error executing command '{command_name}': {str(e)}")
            return 1

    return dispatch


def add_modular_arguments(subparsers) -> Dict:
    """
    Add modular command arguments to a subparsers group.

    Args:
        subparsers: ArgumentParser subparsers object

    Returns:
        Dict mapping command names to their subparsers
    """
    command_parsers = {}

    # Create registry to get command argument configs
    registry = create_registry()

    for cmd_name, cmd_desc in registry.get_available_commands().items():
        cmd_parser = subparsers.add_parser(cmd_name, help=cmd_desc)
        command = registry.get_command(cmd_name)
        command.add_arguments(cmd_parser)
        command_parsers[cmd_name] = cmd_parser

    return command_parsers


def setup_modular_cli(parser):
    """
    Set up modular command system for an argument parser.

    Args:
        parser: The main ArgumentParser instance

    Returns:
        Tuple of (modular_subparsers, legacy_parser)
    """
    # Add command mode selection
    mode_subparsers = parser.add_subparsers(
        dest="command_mode", help="Command mode: legacy or modular"
    )

    # Legacy mode (existing commands)
    legacy_parser = mode_subparsers.add_parser(
        "legacy", help="Use legacy command system"
    )

    # Modular mode
    modular_parser = mode_subparsers.add_parser(
        "modular", help="Use new modular command system"
    )
    modular_subparsers = modular_parser.add_subparsers(
        dest="modular_command", help="Modular command to execute"
    )

    # Add modular command arguments
    add_modular_arguments(modular_subparsers)

    return modular_subparsers, legacy_parser


def handle_modular_command(args, dispatcher=None):
    """
    Handle execution of modular commands.

    Args:
        args: Parsed command-line arguments
        dispatcher: Optional pre-configured dispatcher

    Returns:
        Exit code from command execution
    """
    if not hasattr(args, "modular_command") or not args.modular_command:
        return 0

    cmd_dispatcher = dispatcher or get_command_dispatcher()
    return cmd_dispatcher(args.modular_command, args)
