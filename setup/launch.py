#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

This script provides a single, unified way to set up, manage, and run all
components of the EmailIntelligence application, including the Python backend,
Gradio UI, and Node.js services. It uses 'uv' for Python dependency management
based on pyproject.toml.

Usage:
    python launch.py [arguments]
"""

import argparse
import atexit
import logging
import os
import platform
import shutil
import subprocess
import sys
import time
import threading
import venv
from pathlib import Path
from typing import List

# Add project root to sys.path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import project configuration
from setup.project_config import get_project_config

# Import launch system modules
from setup.validation import (
    check_python_version, check_for_merge_conflicts, check_required_components,
    validate_environment, validate_port, validate_host
)
from setup.services import (
    start_services, start_backend, start_node_service, start_gradio_ui, validate_services
)
from setup.environment import (
    handle_setup, prepare_environment, setup_wsl_environment, check_wsl_requirements
)
from setup.utils import print_system_info, process_manager

# Import test stages
from setup.test_stages import test_stages

# Import command pattern components (with error handling for refactors)
try:
    from src.core.commands.command_factory import get_command_factory
    from src.core.container import get_container, initialize_all_services
    COMMAND_PATTERN_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Could not import core modules: {e}. Some features may be unavailable.")
    get_command_factory = None
    get_container = None
    initialize_all_services = None
    COMMAND_PATTERN_AVAILABLE = False

try:
    from dotenv import load_dotenv

    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    load_dotenv = None  # Will be loaded later if needed

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")


# --- Global state ---
ROOT_DIR = get_project_config().root_dir

# Import process manager from utils
from setup.utils import process_manager

# --- Constants ---
PYTHON_MIN_VERSION = (3, 12)
PYTHON_MAX_VERSION = (3, 13)
VENV_DIR = "venv"
CONDA_ENV_NAME = os.getenv("CONDA_ENV_NAME", "base")





# --- Input Validation ---























def _add_common_args(parser):
    """Add common arguments to subcommand parsers."""
    parser.add_argument(
        "--loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level.",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")


def _add_legacy_args(parser):
    """Add legacy arguments for backward compatibility."""
    # Environment Setup
    parser.add_argument(
        "--force-recreate-venv", action="store_true", help="Force recreation of the venv."
    )
    parser.add_argument(
        "--use-conda", action="store_true", help="Use Conda environment instead of venv."
    )
    parser.add_argument(
        "--conda-env",
        type=str,
        default="base",
        help="Conda environment name to use (default: base).",
    )
    parser.add_argument(
        "--no-venv", action="store_true", help="Don't create or use a virtual environment."
    )
    parser.add_argument(
        "--update-deps", action="store_true", help="Update dependencies before launching."
    )
    parser.add_argument(
        "--skip-torch-cuda-test",
        action="store_true",
        help="Skip CUDA availability test for PyTorch.",
    )
    parser.add_argument("--reinstall-torch", action="store_true", help="Reinstall PyTorch.")
    parser.add_argument(
        "--skip-python-version-check", action="store_true", help="Skip Python version check."
    )
    parser.add_argument(
        "--no-download-nltk", action="store_true", help="Skip downloading NLTK data."
    )
    parser.add_argument(
        "--skip-prepare", action="store_true", help="Skip all environment preparation steps."
    )

    # Application Configuration
    parser.add_argument("--port", type=int, default=8000, help="Specify the port to run on.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Specify the host to run on.")
    parser.add_argument(
        "--frontend-port", type=int, default=5173, help="Specify the frontend port to run on."
    )
    parser.add_argument("--api-url", type=str, help="Specify the API URL for the frontend.")
    parser.add_argument(
        "--api-only", action="store_true", help="Run only the API server without the frontend."
    )
    parser.add_argument(
        "--frontend-only", action="store_true", help="Run only the frontend without the API server."
    )

    # Testing Options
    parser.add_argument(
        "--coverage", action="store_true", help="Generate coverage report when running tests."
    )
    parser.add_argument("--unit", action="store_true", help="Run unit tests.")
    parser.add_argument("--integration", action="store_true", help="Run integration tests.")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests.")
    parser.add_argument("--performance", action="store_true", help="Run performance tests.")
    parser.add_argument("--security", action="store_true", help="Run security tests.")

    # Extensions and Models
    parser.add_argument("--skip-extensions", action="store_true", help="Skip loading extensions.")
    parser.add_argument("--skip-models", action="store_true", help="Skip downloading models.")

    # Advanced Options
    parser.add_argument(
        "--system-info", action="store_true", help="Print system information then exit."
    )
    parser.add_argument("--env-file", type=str, help="Specify environment file to load.")
    parser.add_argument("--share", action="store_true", help="Create a public URL.")
    parser.add_argument("--listen", action="store_true", help="Make the server listen on network.")
    parser.add_argument(
        "--ngrok", type=str, help="Use ngrok to create a tunnel, specify ngrok region."
    )


def main():
    # Check for common setup issues before proceeding
    _check_setup_warnings()

    # Initialize services (only if core modules are available)
    if initialize_all_services and get_container:
        initialize_all_services(get_container())

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="EmailIntelligence Unified Launcher")

    # Add subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Set up the development environment")
    _add_common_args(setup_parser)

    # Run command
    run_parser = subparsers.add_parser("run", help="Run the EmailIntelligence application")
    _add_common_args(run_parser)
    run_parser.add_argument("--dev", action="store_true", help="Run in development mode")

    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests")
    _add_common_args(test_parser)
    test_parser.add_argument("--unit", action="store_true", help="Run unit tests")
    test_parser.add_argument("--integration", action="store_true", help="Run integration tests")
    test_parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    test_parser.add_argument("--performance", action="store_true", help="Run performance tests")
    test_parser.add_argument("--security", action="store_true", help="Run security tests")
    test_parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    test_parser.add_argument(
        "--continue-on-error", action="store_true", help="Continue running tests even if some fail"
    )

    # Legacy argument parsing for backward compatibility
    parser.add_argument("--setup", action="store_true", help="Set up the environment (legacy)")
    parser.add_argument(
        "--stage", choices=["dev", "test"], default="dev", help="Application mode (legacy)"
    )

    # Add all legacy arguments for backward compatibility
    _add_legacy_args(parser)

    args = parser.parse_args()

    # Handle command pattern vs legacy arguments
    if args.command:
        # Use command pattern
        return _execute_command(args.command, args)
    else:
        # Handle legacy arguments
        return _handle_legacy_args(args)


def _execute_command(command_name: str, args) -> int:
    """Execute a command using the command pattern."""
    factory = get_command_factory()
    command = factory.create_command(command_name, args)

    if command is None:
        logger.error(f"Unknown command: {command_name}")
        return 1

    try:
        return command.execute()
    finally:
        command.cleanup()


def _handle_legacy_args(args) -> int:
    """Handle legacy argument parsing for backward compatibility."""
    # Setup WSL environment if applicable (early setup)
    from setup.environment import setup_wsl_environment, check_wsl_requirements
    setup_wsl_environment()
    check_wsl_requirements()

    if not args.skip_python_version_check:
        check_python_version()

    logging.getLogger().setLevel(getattr(args, 'loglevel', 'INFO'))

    if DOTENV_AVAILABLE:
        # Load user customizations from launch-user.env if it exists
        user_env_file = ROOT_DIR / "launch-user.env"
        if user_env_file.exists():
            load_dotenv(user_env_file)
            logger.info(f"Loaded user environment variables from {user_env_file}")
        else:
            logger.debug(f"User env file not found: {user_env_file}")

        # Load environment file if specified
        env_file = args.env_file or ".env"
        if os.path.exists(env_file):
            logger.info(f"Loading environment variables from {env_file}")
            load_dotenv(env_file)

    # Set conda environment name if specified
    global CONDA_ENV_NAME
    if args.conda_env and args.conda_env != "base":  # Only if explicitly set to non-default
        CONDA_ENV_NAME = args.conda_env
        args.use_conda = True  # Set flag when conda env is specified
        # args.use_conda remains as set by command line argument

    # Check for system info first (doesn't need validation)
    if args.system_info:
        print_system_info()
        return 0

    # Validate environment if not skipping preparation
    if not args.skip_prepare and not validate_environment():
        return 1

    # Validate input arguments
    try:
        args.port = validate_port(args.port)
        args.host = validate_host(args.host)
        if hasattr(args, "frontend_port"):
            args.frontend_port = validate_port(args.frontend_port)
    except ValueError as e:
        logger.error(f"Input validation failed: {e}")
        return 1

    if args.setup:
        venv_path = ROOT_DIR / VENV_DIR
        handle_setup(args, venv_path)
        return 0

    # Handle Conda environment if requested
    from setup.environment import is_conda_available, get_conda_env_info, activate_conda_env
    if args.use_conda:
        if not is_conda_available():
            logger.error("Conda is not available. Please install Conda or use venv.")
            return 1
        if not get_conda_env_info()["is_active"] and not activate_conda_env(args.conda_env):
            logger.error(f"Failed to activate Conda environment: {args.conda_env}")
            return 1
        elif get_conda_env_info()["is_active"]:
            logger.info(f"Using existing Conda environment: {os.environ.get('CONDA_DEFAULT_ENV')}")

    if not args.skip_prepare and not args.use_conda:
        prepare_environment(args)

    if args.system_info:
        print("DEBUG: system_info flag detected")
        print_system_info()
        return 0

    # Handle test stage
    if hasattr(args, "stage") and args.stage == "test":
        from setup.test_stages import handle_test_stage
        handle_test_stage(args)
        return 0

    # Handle unit/integration test flags
    if (
        getattr(args, "unit", False)
        or getattr(args, "integration", False)
        or getattr(args, "coverage", False)
    ):
        from setup.test_stages import handle_test_stage
        handle_test_stage(args)
        return 0

    # Service startup logic
    start_services(args)

    logger.info("All services started. Press Ctrl+C to shut down.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutdown signal received.")
    finally:
        process_manager.cleanup()

    return 0


def _check_setup_warnings():
    """Check for common setup issues and warn users."""
    import sys
    from pathlib import Path

    # Check if using system Python
    python_path = Path(sys.executable)
    system_indicators = [
        python_path == Path("/usr/bin/python"),
        python_path == Path("/usr/bin/python3"),
        str(python_path).startswith("/usr/"),
        str(python_path).startswith("/usr/local/"),
    ]

    if any(system_indicators):
        logger.warning("⚠️  You're using system Python. This may cause permission errors with pip.")
        logger.info("💡  Run 'python launch.py setup' to create a virtual environment")
        logger.info("   Then use: source venv/bin/activate")

    # Check if venv exists but not activated
    venv_path = ROOT_DIR / "venv" / "bin" / "python"
    if venv_path.exists() and python_path != venv_path:
        logger.info("💡  Virtual environment exists. Activate it with: source venv/bin/activate")


if __name__ == "__main__":
    main()
