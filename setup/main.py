#!/usr/bin/env python3
"""
EmailIntelligence Main Entry Point

This module serves as the main entry point for the EmailIntelligence launcher system.
It provides a clean, modular interface to the launcher functionality.
"""

import sys
import logging
from pathlib import Path

# Add the project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from setup.routing import create_launcher
from setup.args import parse_arguments
from setup.validation import check_python_version

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main() -> int:
    """
    Main entry point for the EmailIntelligence launcher.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        # Basic validation
        check_python_version()

        # Parse command line arguments
        args = parse_arguments()

        # Create and run launcher
        launcher = create_launcher()
        return launcher.run(args)

    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())