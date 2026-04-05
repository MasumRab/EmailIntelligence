"""
Command routing for the EmailIntelligence launcher.

This module handles the routing between command pattern and legacy argument handling,
providing a clean interface for executing different launcher operations.
"""

import logging
from typing import Any

from setup.launch import (
    COMMAND_PATTERN_AVAILABLE,
    _check_setup_warnings,
    _execute_command,
    _handle_legacy_args,
    get_command_factory,
)

logger = logging.getLogger(__name__)


class Launcher:
    """Main launcher class that handles command routing and execution."""

    def __init__(self):
        """Initialize the launcher."""
        self._initialized = False

    def _initialize_services(self) -> None:
        """Initialize services if available."""
        if self._initialized:
            return

        # Initialize services (only if core modules are available)
        if COMMAND_PATTERN_AVAILABLE:
            try:
                from setup.container import get_container, initialize_all_services
                if initialize_all_services and get_container:
                    initialize_all_services(get_container())
                    logger.debug("Services initialized successfully")
            except ImportError:
                logger.debug("Service initialization not available")

        self._initialized = True

    def run(self, args: Any) -> int:
        """
        Run the launcher with the given arguments.

        Args:
            args: Parsed command line arguments

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            # Check for common setup issues before proceeding
            _check_setup_warnings()

            # Initialize services
            self._initialize_services()

            # Handle command pattern vs legacy arguments
            if args.command:
                # Use command pattern
                logger.debug(f"Routing to command pattern: {args.command}")
                return _execute_command(args.command, args)
            else:
                # Handle legacy arguments
                logger.debug("Routing to legacy argument handling")
                return _handle_legacy_args(args)

        except Exception as e:
            logger.error(f"Launcher execution failed: {e}")
            return 1


def create_launcher() -> Launcher:
    """Create and return a new launcher instance."""
    return Launcher()