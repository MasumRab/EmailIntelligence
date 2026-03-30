"""
Test script for command pattern implementation.

This script demonstrates and tests the command pattern implementation.
"""

import argparse
import logging
import sys
from pathlib import Path

# Add the setup directory to the path so we can import the commands
sys.path.insert(0, str(Path(__file__).parent))

from commands.command_factory import get_command_factory
from container import get_container, initialize_all_services

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_command_creation():
    """Test command creation through the factory."""
    logger.info("Testing command creation...")

    factory = get_command_factory()

    # Test available commands
    commands = factory.get_available_commands()
    logger.info(f"Available commands: {commands}")

    # Test creating each command
    for cmd_name in commands:
        try:
            # Create a simple args object for testing
            args = argparse.Namespace()
            command = factory.create_command(cmd_name, args)
            if command:
                logger.info(f"Successfully created {cmd_name} command")
                logger.info(f"Description: {command.get_description()}")
            else:
                logger.error(f"Failed to create {cmd_name} command")
        except Exception as e:
            logger.error(f"Error creating {cmd_name} command: {e}")


def test_command_execution():
    """Test command execution."""
    logger.info("Testing command execution...")

    factory = get_command_factory()

    # Test creating and getting description for each command
    for cmd_name in factory.get_available_commands():
        try:
            command = factory.create_command(cmd_name, argparse.Namespace())
            if command:
                description = factory.get_command_description(cmd_name)
                logger.info(f"{cmd_name}: {description}")
            else:
                logger.error(f"Failed to create {cmd_name} command for description test")
        except Exception as e:
            logger.error(f"Error testing {cmd_name} command: {e}")


def main():
    """Main test function."""
    logger.info("Starting command pattern tests...")

    # Initialize services
    container = get_container()
    initialize_all_services(container)

    # Run tests
    test_command_creation()
    test_command_execution()

    logger.info("Command pattern tests completed.")


if __name__ == "__main__":
    main()