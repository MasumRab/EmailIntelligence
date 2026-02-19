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
        Dict mapping dependency names to instances
    """
    dependencies = {}

    # Import dependencies lazily to avoid circular imports and handle missing modules
    try:
        from ..git.worktree import WorktreeManager

        dependencies["worktree_manager"] = WorktreeManager()
    except ImportError:
        dependencies["worktree_manager"] = None

    try:
        from ..git.conflict_detector import GitConflictDetector

        dependencies["conflict_detector"] = GitConflictDetector()
    except ImportError:
        dependencies["conflict_detector"] = None

    try:
        from ..git.repository import RepositoryOperations

        dependencies["repository_ops"] = RepositoryOperations
    except ImportError:
        dependencies["repository_ops"] = None

    try:
        from ..analysis.constitutional.analyzer import ConstitutionalAnalyzer

        dependencies["analyzer"] = ConstitutionalAnalyzer()
    except ImportError:
        dependencies["analyzer"] = None

    try:
        from ..strategy.generator import StrategyGenerator

        dependencies["strategy_generator"] = StrategyGenerator()
    except ImportError:
        dependencies["strategy_generator"] = None

    try:
        from ..resolution.auto_resolver import AutoResolver

        dependencies["resolver"] = AutoResolver()
    except ImportError:
        dependencies["resolver"] = None

    try:
        from ..validation.validator import Validator

        dependencies["validator"] = Validator()
    except ImportError:
        dependencies["validator"] = None

    try:
        from ..git.history import GitHistory

        dependencies["history"] = GitHistory()
    except ImportError:
        dependencies["history"] = None

    try:
        from ..analysis.commits import CommitClassifier

        dependencies["classifier"] = CommitClassifier()
    except ImportError:
        dependencies["classifier"] = None

    try:
        from ..strategy.reordering import RebasePlanner

        dependencies["planner"] = RebasePlanner()
    except ImportError:
        dependencies["planner"] = None

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

    cmd_factory = factory or create_command_factory()
    registry = CommandRegistry(cmd_factory)

    # Register all commands with agent assignments
    registry.register_command(AnalyzeCommand, "agent-2")
    registry.register_command(ResolveCommand, "agent-3")
    registry.register_command(ValidateCommand, "agent-4")
    registry.register_command(AnalyzeHistoryCommand, "agent-5")
    registry.register_command(PlanRebaseCommand, "agent-5")

    return registry


def get_command_dispatcher(registry: Optional[CommandRegistry] = None):
    """
    Create a dispatcher function for CLI entry point.

    Args:
        registry: Optional pre-configured registry

    Returns:
        Dispatcher function that takes command_name and args, returns exit code
    """
    cmd_registry = registry or create_registry()

    def dispatch(command_name: str, args) -> int:
        """
        Dispatch a command by name.

        Args:
            command_name: Name of the command to execute
            args: Parsed command-line arguments

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        try:
            command = cmd_registry.get_command(command_name)
            return asyncio.run(command.execute(args))
        except ValueError as e:
            print(f"Error: {e}")
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}")
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
