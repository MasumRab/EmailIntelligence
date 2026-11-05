#!/usr/bin/env python3
"""
EmailIntelligence CLI - Unified Entry Point

This is the main entry point for the modular CLI architecture. It uses the
CommandFactory and CommandRegistry to discover and execute the commands that
live in ``src/cli/commands/``.

Run it with the repository ``src`` directory on the path::

    PYTHONPATH=src python -m src.cli.main --help
"""

import argparse
import asyncio
import sys

from .commands import (
    AgentScaffoldCommand,
    AnalyzeCodeCommand,
    AnalyzeCommand,
    AnalyzeHistoryCommand,
    AnalyzeTasksCommand,
    ClusterBranchesCommand,
    CommandFactory,
    CommandRegistry,
    CompareCommand,
    ImportAuditCommand,
    ListTasksCommand,
    MergeSmartCommand,
    OrchExtractCommand,
    PlanRebaseCommand,
    ResolveCommand,
    RuleSyncCommand,
    StashResolveCommand,
    TaskmasterCommand,
    ValidateCommand,
)

#: Commands registered with the dispatcher, paired with the agent role that owns
#: them. Only commands that exist in this tree are listed — registering a name
#: whose module is absent would move the failure from import time to runtime.
COMMANDS = [
    (AnalyzeCommand, "analyst"),
    (ResolveCommand, "resolver"),
    (PlanRebaseCommand, "planner"),
    (AnalyzeHistoryCommand, "analyst"),
    (MergeSmartCommand, "resolver"),
    (StashResolveCommand, "resolver"),
    (OrchExtractCommand, "git"),
    (ValidateCommand, "validator"),
    (CompareCommand, "system"),
    (AnalyzeCodeCommand, "analyst"),
    (ImportAuditCommand, "analyst"),
    (TaskmasterCommand, "workflow"),
    (ListTasksCommand, "workflow"),
    (AnalyzeTasksCommand, "workflow"),
    (ClusterBranchesCommand, "analyst"),
    (AgentScaffoldCommand, "system"),
    (RuleSyncCommand, "system"),
]


def build_registry(dependencies: dict | None = None) -> CommandRegistry:
    """Create a registry with every available command registered."""
    factory = CommandFactory(dependencies or {})
    registry = CommandRegistry(factory)
    for command_class, agent in COMMANDS:
        registry.register_command(command_class, agent=agent)
    return registry


def build_parser(registry: CommandRegistry) -> argparse.ArgumentParser:
    """Build the top-level parser with one subparser per registered command."""
    parser = argparse.ArgumentParser(
        description="EmailIntelligence CLI - Unified modular command system",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    for command_name in registry.get_all_commands():
        command_instance = registry.get_command(command_name)
        subparser = subparsers.add_parser(
            command_instance.name,
            help=command_instance.description,
            description=command_instance.description,
        )
        command_instance.add_arguments(subparser)
    return parser


async def run_cli(args: list[str] | None = None, dependencies: dict | None = None) -> int:
    """Parse arguments and execute the selected command.

    Args:
        args: Argument list to parse. Defaults to ``sys.argv[1:]``.
        dependencies: Dependencies injected into every command instance.

    Returns:
        int: Exit code
    """
    registry = build_registry(dependencies)
    parser = build_parser(registry)
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        return 0

    try:
        command = registry.get_command(parsed_args.command)
        return await command.execute(parsed_args)
    except Exception as e:  # noqa: BLE001 - the CLI reports rather than crashes
        print(f"Error executing command '{parsed_args.command}': {e}")
        return 1


def main() -> None:
    """Main entry point."""
    try:
        exit_code = asyncio.run(run_cli())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(130)
    except Exception as e:  # noqa: BLE001 - the CLI reports rather than crashes
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
