#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

This script provides a single, unified way to set up, manage, and run all
components of the EmailIntelligence application. It supports both a modern
command-based interface and legacy arguments for backward compatibility.

Features:
- Environment setup (venv/conda)
- Service management (Backend, Frontend, Gradio)
- Multi-stage testing
- Orchestration validation
"""

import os
import sys
import platform
import shutil
import subprocess
import time
import atexit
import logging
from pathlib import Path
from typing import List, Optional

# --- 1. Infrastructure Core ---
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# --- 2. Protected & Deferred Imports ---
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

# Import utilities (unstable modules should be deferred inside functions)
try:
    from setup.utils import process_manager, print_system_info
    from setup.project_config import get_project_config
    from setup.validation import validate_environment, check_for_merge_conflicts
    from setup.test_stages import test_stages
    from setup.services import start_services
    from setup.environment import handle_setup, prepare_environment
except ImportError:
    # Fallback or deferred imports will handle this
    process_manager = None
    print_system_info = None

# Command pattern components
try:
    from setup.commands.command_factory import get_command_factory
    from setup.container import get_container, initialize_all_services
    COMMAND_PATTERN_AVAILABLE = True
except ImportError:
    COMMAND_PATTERN_AVAILABLE = False

# --- 3. Configuration & Constants ---
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")

PYTHON_MIN_VERSION = (3, 11)
PYTHON_MAX_VERSION = (3, 13)
VENV_DIR = "venv"
CONDA_ENV_NAME = os.getenv("CONDA_ENV_NAME", "base")

# --- 4. Helper Functions ---

def check_python_version():
    """Check if the current Python version is compatible."""
    current_version = sys.version_info[:2]
    if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
        logger.error(
            f"Python version {platform.python_version()} is not compatible. "
            f"Please use Python {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]} to {PYTHON_MAX_VERSION[0]}.{PYTHON_MAX_VERSION[1]}"
        )
        sys.exit(1)

def _check_setup_warnings():
    """Check for common setup issues and warn users."""
    python_path = Path(sys.executable)
    if "/usr/bin/python" in str(python_path) or "/usr/local/bin/python" in str(python_path):
        logger.warning("⚠️  You're using system Python. This may cause permission errors.")
        logger.info("💡  Run 'python setup/launch.py setup' to create a virtual environment")

def _execute_command(command_name: str, args) -> int:
    """Execute a command using the command pattern."""
    if not COMMAND_PATTERN_AVAILABLE:
        logger.error(f"Command pattern not available for '{command_name}'")
        return 1
    
    factory = get_command_factory()
    command = factory.create_command(command_name, args)

    if command is None:
        logger.error(f"Unknown command: {command_name}")
        return 1

    try:
        return command.execute()
    finally:
        if hasattr(command, 'cleanup'):
            command.cleanup()

# --- 5. Argument Parsing & Dispatching ---

def _add_common_args(parser):
    """Add common arguments to the parser."""
    parser.add_argument(
        "--loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level.",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")

def _add_legacy_args(parser):
    """Add all flags to ensure backward compatibility as per Runbook."""
    # Environment & Setup
    parser.add_argument("--setup", action="store_true", help="Set up the environment (Legacy Component - Maintained for Backward Compatibility)")
    parser.add_argument("--stage", choices=["dev", "test"], default="dev", help="Application mode (Legacy Component - Maintained for Backward Compatibility)")
    parser.add_argument("--force-recreate-venv", action="store_true", help="Force recreation of the venv.")
    parser.add_argument("--use-conda", action="store_true", help="Use Conda environment instead of venv.")
    parser.add_argument("--conda-env", type=str, default="base", help="Conda environment name to use.")
    parser.add_argument("--no-venv", action="store_true", help="Don't use a virtual environment.")
    parser.add_argument("--update-deps", action="store_true", help="Update dependencies before launching.")
    parser.add_argument("--no-download-nltk", action="store_true", help="Skip downloading NLTK data.")
    parser.add_argument("--skip-python-version-check", action="store_true", help="Skip version check.")
    
    # Server Config
    parser.add_argument("--port", type=int, default=8000, help="Backend port.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Backend host.")
    parser.add_argument("--frontend-port", type=int, default=5173, help="Frontend port.")
    parser.add_argument("--api-url", type=str, help="API URL for frontend.")
    parser.add_argument("--api-only", action="store_true", help="Run only API server.")
    parser.add_argument("--frontend-only", action="store_true", help="Run only frontend.")
    
    # Testing
    parser.add_argument("--unit", action="store_true", help="Run unit tests.")
    parser.add_argument("--integration", action="store_true", help="Run integration tests.")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests.")
    parser.add_argument("--performance", action="store_true", help="Run performance tests.")
    parser.add_argument("--security", action="store_true", help="Run security tests.")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report.")
    
    # Advanced
    parser.add_argument("--system-info", action="store_true", help="Print system information.")
    parser.add_argument("--env-file", type=str, help="Specify environment file to load.")
    parser.add_argument("--listen", action="store_true", help="Listen on network.")
    parser.add_argument("--share", action="store_true", help="Create a public URL.")

def _handle_legacy_args(args) -> int:
    """Primary dispatcher for legacy argument support."""
    # 1. Environment Overrides
    if DOTENV_AVAILABLE:
        user_env = ROOT_DIR / "launch-user.env"
        if user_env.exists():
            load_dotenv(user_env)
        env_file = args.env_file or ".env"
        if os.path.exists(env_file):
            load_dotenv(env_file)

    # 2. System Info
    if args.system_info:
        from setup.utils import print_system_info
        print_system_info()
        return 0

    # 3. Validation
    if not args.skip_python_version_check:
        check_python_version()
    
    if not validate_environment():
        return 1

    # 4. Setup
    if args.setup:
        from setup.environment import handle_setup
        handle_setup(args, ROOT_DIR / VENV_DIR)
        return 0

    # 5. Tests
    if args.unit or args.integration or args.e2e or args.stage == "test":
        from setup.test_stages import handle_test_stage
        handle_test_stage(args)
        return 0

    # 6. Services
    from setup.services import start_services
    start_services(args)

    logger.info("All services started. Press Ctrl+C to shut down.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutdown signal received.")
    finally:
        if process_manager:
            process_manager.cleanup()
    
    return 0

def main():
    """Main entry point."""
    _check_setup_warnings()

    if COMMAND_PATTERN_AVAILABLE and initialize_all_services and get_container:
        initialize_all_services(get_container())

    parser = argparse.ArgumentParser(description="EmailIntelligence Unified Launcher")
    _add_common_args(parser)

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: setup
    setup_parser = subparsers.add_parser("setup", help="Set up environment")
    _add_common_args(setup_parser)
    _add_legacy_args(setup_parser)

    # Command: run
    run_parser = subparsers.add_parser("run", help="Run application")
    _add_common_args(run_parser)
    _add_legacy_args(run_parser)
    run_parser.add_argument("--dev", action="store_true", help="Run in development mode")

    # Command: test
    test_parser = subparsers.add_parser("test", help="Run tests")
    _add_common_args(test_parser)
    _add_legacy_args(test_parser)

    # Add legacy args to top level for backward compatibility
    _add_legacy_args(parser)

    args = parser.parse_args()

    # Dispatch
    if args.command:
        return _execute_command(args.command, args)
    else:
        return _handle_legacy_args(args)

if __name__ == "__main__":
    sys.exit(main())
