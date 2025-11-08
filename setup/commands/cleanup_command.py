"""
Cleanup Command implementation.

Handles manual cleanup of resources and processes.
"""

import logging
from argparse import Namespace

from .command_interface import Command

logger = logging.getLogger(__name__)


class CleanupCommand(Command):
    """
    Command for performing manual cleanup operations.

    This command handles:
    - Terminating managed processes
    - Cleaning up resources
    - Removing temporary files
    """

    def get_description(self) -> str:
        return "Perform manual cleanup of resources and processes"

    def validate_args(self) -> bool:
        """Validate command arguments."""
        # Cleanup command doesn't have specific validation requirements
        return True

    def execute(self) -> int:
        """
        Execute the cleanup command.

        Returns:
            int: Exit code (0 for success, non-zero for failure)
        """
        try:
            from setup.utils import process_manager
            logger.info("Starting manual cleanup...")

            # Perform process cleanup
            process_manager.cleanup()

            logger.info("Manual cleanup completed successfully!")
            return 0

        except KeyboardInterrupt:
            logger.info("Cleanup interrupted by user")
            return 0
        except Exception as e:
            logger.error(f"Cleanup command failed: {e}")
            return 1

    def cleanup(self) -> None:
        """
        Cleanup method for this command.
        In this case, cleanup has already been done in execute.
        """
        pass