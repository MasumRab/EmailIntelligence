#!/usr/bin/env python3
"""
EmailIntelligence CLI - Unified Entry Point

This is the main entry point for the modular CLI architecture.
It coordinates service initialization, dependency injection, and command dispatch.
"""

import argparse
import asyncio
import sys
import logging
from typing import List, Optional

from .commands import (
    CommandFactory,
    CommandRegistry
)
from .commands.integration import get_command_registry, create_default_dependencies
from .services.nlp import NLPService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_cli(args: Optional[List[str]] = None) -> int:
    """
    Run the unified CLI with explicit dependency management.
    """
    # 1. Initialize Core Services
    dependencies = create_default_dependencies()
    
    # 2. Setup Modular Architecture
    factory = CommandFactory(dependencies)
    registry = get_command_registry(factory)

    # 3. Create CLI Parser
    parser = argparse.ArgumentParser(
        description="EmailIntelligence CLI - Unified modular command system",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 4. Register Command Arguments
    for command_name, _ in registry.get_all_commands().items():
        command_instance = registry.get_command(command_name)
        subparser = subparsers.add_parser(
            command_instance.name,
            help=command_instance.description
        )
        command_instance.add_arguments(subparser)

    # 5. Parse and Dispatch
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        return 0

    try:
        command = registry.get_command(parsed_args.command)
        return await command.execute(parsed_args)
    except Exception as e:
        logger.error(f"Error executing command '{parsed_args.command}': {e}")
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
