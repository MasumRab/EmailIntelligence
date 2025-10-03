"""
A simple launcher script for the EmailIntelligence application.

This script provides a basic entry point for starting the application. It sets
up logging and handles system signals for graceful shutdown.
"""
import logging
import signal
import sys


def main():
    """
    The main entry point for the application.

    This function initializes basic logging and imports and runs the main
    application logic.
    """
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting EmailIntelligence...")

    try:
        # Import and run your main application logic here
        import main  # Replace with your actual entry point

        main.run()  # Replace with your actual run method
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)


def handle_exit(signum, frame):
    """
    Handles SIGINT and SIGTERM signals for graceful shutdown.

    Args:
        signum: The signal number.
        frame: The current stack frame.
    """
    logging.info("Shutting down EmailIntelligence gracefully...")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    main()