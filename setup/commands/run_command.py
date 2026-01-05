"""
Run Command implementation.

Handles the execution of the EmailIntelligence application.
"""

import logging

from .command_interface import Command

logger = logging.getLogger(__name__)


class RunCommand(Command):
    """
    Command for running the EmailIntelligence application.

    This command handles:
    - Starting the backend server
    - Starting the frontend client
    - Starting the TypeScript backend
    - Starting the Gradio UI
    """

    def get_description(self) -> str:
        return "Run the EmailIntelligence application"

    def validate_args(self) -> bool:
        """Validate command arguments."""
        # Basic validation for host and port
        if hasattr(self.args, "host") and self.args.host:
            host = self.args.host
            if not isinstance(host, str) or len(host) == 0:
                logger.error("Host must be a non-empty string")
                return False

        if hasattr(self.args, "port") and self.args.port:
            port = self.args.port
            if not isinstance(port, int) or not (1 <= port <= 65535):
                logger.error(f"Port must be an integer between 1 and 65535, got {port}")
                return False

        return True

    def execute(self) -> int:
        """
        Execute the run command.

        Returns:
            int: Exit code (0 for success, non-zero for failure)
        """
        try:
            from setup.services import start_services, validate_services
            from setup.launch import prepare_environment

            logger.info("Starting EmailIntelligence application...")

            # Prepare the environment
            prepare_environment(self.args)

            # Validate available services
            available_services = validate_services()
            logger.info(f"Available services: {list(available_services.keys())}")

            # Start the required services
            start_services(self.args)

            logger.info("EmailIntelligence application started successfully!")
            logger.info("Application is now running. Press Ctrl+C to stop.")

            # Keep the process running
            import time

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Application interrupted by user")
                return 0

        except KeyboardInterrupt:
            logger.info("Run command interrupted by user")
            return 0
        except Exception as e:
            logger.error(f"Run command failed: {e}")
            return 1
