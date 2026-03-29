"""
Test Command implementation.

Handles running tests for the EmailIntelligence application.
"""

import logging

from .command_interface import Command

logger = logging.getLogger(__name__)


class TestCommand(Command):
    """
    Command for running tests.

    This command handles:
    - Running unit tests
    - Running integration tests
    - Running end-to-end tests
    - Running performance tests
    - Running security tests
    """

    def get_description(self) -> str:
        return "Run tests for the EmailIntelligence application"

    def validate_args(self) -> bool:
        """Validate command arguments."""
        # Test command arguments are validated by argparse
        return True

    def execute(self) -> int:
        """
        Execute the test command.

        Returns:
            int: Exit code (0 for success, non-zero for failure)
        """
        try:
            from setup.test_stages import handle_test_stage

            logger.info("Running tests...")

            # Execute test stage
            handle_test_stage(self.args)

            logger.info("Tests completed successfully!")
            return 0

        except KeyboardInterrupt:
            logger.info("Tests interrupted by user")
            return 0
        except Exception as e:
            logger.error(f"Test command failed: {e}")
            return 1
