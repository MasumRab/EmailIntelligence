"""
Check Command implementation.

Handles orchestration validation and system checks.
"""

import logging
from argparse import Namespace

from .command_interface import Command

logger = logging.getLogger(__name__)


class CheckCommand(Command):
    """
    Command for running orchestration checks.

    This command handles:
    - Checking for critical files
    - Validating the orchestration environment
    - Running system compatibility checks
    """

    def __init__(self, args: Namespace = None):
        """Initialize the check command with arguments."""
        super().__init__(args)
        self.args = args

    def get_description(self) -> str:
        return "Run orchestration checks for the EmailIntelligence application"

    def validate_args(self) -> bool:
        """Validate command arguments."""
        # Check command doesn't take any specific arguments, so always valid
        return True

    def execute(self) -> int:
        """
        Execute the check command.

        Returns:
            int: Exit code (0 for success, non-zero for failure)
        """
        try:
            from setup.validation import (
                validate_orchestration_environment,
                check_critical_files,
            )

            logger.info("Running orchestration checks...")

            # Handle specific check types
            if self.args:
                if hasattr(self.args, "critical_files") and self.args.critical_files:
                    # Check only critical files
                    success = check_critical_files()
                    if success:
                        logger.info("Critical files check passed!")
                        return 0
                    else:
                        logger.error("Critical files check failed")
                        return 1
                elif hasattr(self.args, "env") and self.args.env:
                    # Check orchestration environment
                    success = validate_orchestration_environment()
                    if success:
                        logger.info("Orchestration environment validation passed!")
                        return 0
                    else:
                        logger.error("Orchestration environment validation failed")
                        return 1

            # Default: run all checks
            success = validate_orchestration_environment()

            if success:
                logger.info("Orchestration checks passed successfully!")
                return 0
            else:
                logger.error("Orchestration checks failed")
                return 1

        except KeyboardInterrupt:
            logger.info("Check command interrupted by user")
            return 0
        except Exception as e:
            logger.error(f"Check command failed: {e}")
            return 1
