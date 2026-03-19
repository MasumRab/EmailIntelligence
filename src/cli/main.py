#!/usr/bin/env python3
"""
EmailIntelligence CLI - Unified Entry Point

This is the main entry point for the modular CLI architecture.
It uses the CommandFactory and CommandRegistry to discover and execute commands.
"""

import argparse
import asyncio
import sys
from typing import List, Optional

from .commands import (
    CommandFactory,
    CommandRegistry,
    AnalyzeCommand,
    ResolveCommand,
    ValidateCommand,
    AnalyzeHistoryCommand,
    PlanRebaseCommand,
    CompareCommand,
    VerifyCommand
)

async def run_cli(args: Optional[List[str]] = None) -> int:
    """
    Run the unified CLI.

    Args:
        args: Command-line arguments (uses sys.argv if None)

    Returns:
        int: Exit code
    """
    # Initialize factory and registry
    # In a real implementation, we would inject actual dependency instances here
    dependencies = {
        "conflict_detector": None, # Placeholder
        "analyzer": None,          # Placeholder
        "strategy_generator": None, # Placeholder
        "repository_ops": None,     # Placeholder
        "security_validator": None  # Placeholder
    }
    
    factory = CommandFactory(dependencies)
    registry = CommandRegistry(factory)

    # Register commands
    registry.register_command(AnalyzeCommand, agent="analyst")
    registry.register_command(ResolveCommand, agent="resolver")
    registry.register_command(ValidateCommand, agent="validator")
    registry.register_command(AnalyzeHistoryCommand, agent="analyst")
    registry.register_command(PlanRebaseCommand, agent="planner")
    registry.register_command(CompareCommand, agent="system")
    registry.register_command(VerifyCommand, agent="system")

    # Create top-level parser
    parser = argparse.ArgumentParser(
        description="EmailIntelligence CLI - Unified modular command system",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add arguments for each registered command
    for command_name, metadata in registry.get_all_commands().items():
        command_instance = registry.get_command(command_name)
        subparser = subparsers.add_parser(
            command_instance.name,
            help=command_instance.description
        )
        command_instance.add_arguments(subparser)

    # Parse arguments
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        return 0

    # Execute command
    try:
        command = registry.get_command(parsed_args.command)
        return await command.execute(parsed_args)
    except Exception as e:
        print(f"Error executing command '{parsed_args.command}': {e}")
        return 1

def main():
    """Main entry point."""
    try:
        exit_code = asyncio.run(run_cli())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
