#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

This script provides a single, unified way to set up, manage, and run all
components of the EmailIntelligence application, including the Python backend,
Gradio UI, and Node.js services. It supports both modern command-based interface
and legacy arguments for backward compatibility.
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
from pathlib import Path
from typing import List

# --- Infrastructure Core ---
# ROOT_DIR setup as per Runbook
ROOT_DIR = Path(__file__).resolve().parent.parent

# Add project root to sys.path to ensure project-wide modules are always importable
sys.path.insert(0, str(ROOT_DIR))

# Protected Imports as per Runbook
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    load_dotenv = None

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")

# Import project utilities and configuration
from setup.utils import (
    ProcessManager,
    process_manager,
    get_conda_env_info,
    is_conda_available,
    activate_conda_env,
)
from setup.environment import (
    is_wsl,
    setup_wsl_environment as env_setup_wsl,
    check_wsl_requirements,
    get_python_executable,
    get_venv_executable,
)
from setup.validation import (
    check_python_version as val_check_python_version,
    check_for_merge_conflicts,
    check_required_components,
    validate_environment,
    validate_port,
    validate_host,
)
from setup.test_stages import test_stages
from setup.project_config import get_project_config

# Import command pattern components (with error handling for refactors)
try:
    from setup.commands.command_factory import get_command_factory
    from setup.container import get_container, initialize_all_services
    COMMAND_PATTERN_AVAILABLE = True
except ImportError:
    COMMAND_PATTERN_AVAILABLE = False
    get_command_factory = None
    get_container = None
    initialize_all_services = None

# --- Constants ---
PYTHON_MIN_VERSION = (3, 11)
PYTHON_MAX_VERSION = (3, 12)
VENV_DIR = "venv"
CONDA_ENV_NAME = os.getenv("CONDA_ENV_NAME", "base")

# --- Environment Setup Helpers ---

def setup_wsl_environment():
    """Setup WSL-specific environment variables if in WSL"""
    env_setup_wsl()

def check_python_version():
    """Check if the current Python version is compatible."""
    val_check_python_version()

# --- Setup and Execution Logic ---

def run_command(cmd: List[str], description: str, **kwargs) -> bool:
    """Run a command and log its output."""
    logger.info(f"{description}...")
    try:
        proc = subprocess.run(cmd, check=True, text=True, capture_output=True, **kwargs)
        if proc.stdout:
            logger.debug(proc.stdout)
        if proc.stderr:
            logger.warning(proc.stderr)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Failed: {description}")
        if isinstance(e, subprocess.CalledProcessError):
            logger.error(f"Stderr: {e.stderr}")
        return False

def handle_setup(args, venv_path):
    """Handles the complete setup process."""
    from setup.environment import handle_setup as env_handle_setup
    logger.info("Starting environment setup...")
    env_handle_setup(args, venv_path)
    logger.info("Setup complete.")

def prepare_environment(args):
    """Prepares the environment for running the application."""
    from setup.environment import prepare_environment as env_prepare_env
    env_prepare_env(args)

def start_services(args):
    """Starts the required services based on arguments."""
    from setup.services import start_services as env_start_services
    env_start_services(args)

# --- Argument Parsing ---

def _add_common_args(parser):
    """Add common arguments to the parser."""
    parser.add_argument(
        "--loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level.",
    )

def _add_legacy_args(parser):
    """Add legacy arguments for backward compatibility."""
    # Standardizing nomenclature to 'Legacy Component - Maintained for Backward Compatibility'
    parser.add_argument("--setup", action="store_true", help="Set up the environment (Legacy Component - Maintained for Backward Compatibility)")
    parser.add_argument(
        "--stage", choices=["dev", "test"], default="dev", help="Application mode (Legacy Component - Maintained for Backward Compatibility)"
    )
    parser.add_argument(
        "--env-file",
        type=str,
        help="Path to environment file to load.",
    )

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
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")

    # Testing Options
    parser.add_argument(
        "--coverage", action="store_true", help="Generate coverage report when running tests."
    )
    parser.add_argument("--unit", action="store_true", help="Run unit tests.")
    parser.add_argument("--integration", action="store_true", help="Run integration tests.")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests.")
    parser.add_argument("--performance", action="store_true", help="Run performance tests.")
    parser.add_argument("--security", action="store_true", help="Run security tests.")

    # Extensions and Models (from PR #659)
    parser.add_argument("--skip-extensions", action="store_true", help="Skip loading extensions.")
    parser.add_argument("--skip-models", action="store_true", help="Skip downloading models.")

    # Advanced Options
    parser.add_argument(
        "--system-info", action="store_true", help="Print system information then exit."
    )
    parser.add_argument("--share", action="store_true", help="Create a public URL.")
    parser.add_argument("--listen", action="store_true", help="Make the server listen on network.")
    parser.add_argument(
        "--ngrok", type=str, help="Use ngrok to create a tunnel, specify ngrok region."
    )

def _execute_command(command_name: str, args) -> int:
    """Execute a command using the command pattern."""
    if command_name == "check":
        return _execute_check_command(args)

    if COMMAND_PATTERN_AVAILABLE:
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
    else:
        logger.error(f"Command pattern not available and '{command_name}' is not a built-in command")
        return 1

def _execute_check_command(args) -> int:
    """Execute the check command for orchestration validation."""
    logger.info("Running orchestration checks...")
    from setup.validation import check_critical_files, validate_orchestration_environment
    
    success = True
    if getattr(args, 'critical_files', False) or (not getattr(args, 'env', False)):
        if not check_critical_files():
            success = False

    if getattr(args, 'env', False):
        if not validate_orchestration_environment():
            success = False

    if not getattr(args, 'critical_files', False) and not getattr(args, 'env', False):
        if not validate_orchestration_environment():
            success = False

    if success:
        logger.info("All orchestration checks passed!")
        return 0
    else:
        logger.error("Orchestration checks failed!")
        return 1

def _handle_legacy_args(args) -> int:
    """Handle legacy argument parsing (Legacy Component - Maintained for Backward Compatibility)."""
    setup_wsl_environment()
    check_wsl_requirements()

    if not getattr(args, 'skip_python_version_check', False):
        check_python_version()

    if DOTENV_AVAILABLE:
        user_env_file = ROOT_DIR / "launch-user.env"
        if user_env_file.exists():
            load_dotenv(user_env_file)
            logger.info(f"Loaded user environment variables from {user_env_file}")
        
        env_file = getattr(args, 'env_file', None) or ".env"
        if os.path.exists(env_file):
            logger.info(f"Loading environment variables from {env_file}")
            load_dotenv(env_file)

    global CONDA_ENV_NAME
    if getattr(args, 'conda_env', None) and args.conda_env != "base":
        CONDA_ENV_NAME = args.conda_env
        args.use_conda = True

    if not getattr(args, 'skip_prepare', False) and not validate_environment():
        return 1

    try:
        if hasattr(args, 'port'):
            args.port = validate_port(args.port)
        if hasattr(args, 'host'):
            args.host = validate_host(args.host)
        if hasattr(args, "frontend_port"):
            args.frontend_port = validate_port(args.frontend_port)
    except ValueError as e:
        logger.error(f"Input validation failed: {e}")
        return 1

    if getattr(args, 'setup', False):
        venv_path = ROOT_DIR / VENV_DIR
        handle_setup(args, venv_path)
        return 0

    if getattr(args, 'use_conda', False):
        if not is_conda_available():
            logger.error("Conda is not available. Please install Conda or use venv.")
            return 1
        if not get_conda_env_info()["is_active"] and not activate_conda_env(args.conda_env):
            logger.error(f"Failed to activate Conda environment: {args.conda_env}")
            return 1
        elif get_conda_env_info()["is_active"]:
            logger.info(f"Using existing Conda environment: {os.environ.get('CONDA_DEFAULT_ENV')}")

    if not getattr(args, 'skip_prepare', False) and not getattr(args, 'use_conda', False):
        prepare_environment(args)

    if getattr(args, 'system_info', False):
        from setup.utils import print_system_info as utils_print_info
        print_system_info()
        return 0

    if (hasattr(args, "stage") and args.stage == "test") or \
       any(getattr(args, attr, False) for attr in ["unit", "integration", "e2e", "performance", "security", "coverage"]):
        from setup.test_stages import handle_test_stage
        handle_test_stage(args)
        return 0

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

def print_system_info():
    """Print detailed system information (Legacy Component - Maintained for Backward Compatibility)."""
    from setup.utils import print_system_info as utils_print_info
    utils_print_info()

def main():
    """Main entry point for the launcher."""
    parser = argparse.ArgumentParser(
        description="EmailIntelligence Unified Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Add modern subcommands if pattern is available
    if COMMAND_PATTERN_AVAILABLE:
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        setup_parser = subparsers.add_parser("setup", help="Set up the development environment")
        _add_common_args(setup_parser)
        
        run_parser = subparsers.add_parser("run", help="Run the EmailIntelligence application")
        _add_common_args(run_parser)
        run_parser.add_argument("--dev", action="store_true", help="Run in development mode")
        
        test_parser = subparsers.add_parser("test", help="Run tests")
        _add_common_args(test_parser)
        test_parser.add_argument("--unit", action="store_true", help="Run unit tests")
        test_parser.add_argument("--integration", action="store_true", help="Run integration tests")
        test_parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
        test_parser.add_argument("--performance", action="store_true", help="Run performance tests")
        test_parser.add_argument("--security", action="store_true", help="Run security tests")
        test_parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
        
        check_parser = subparsers.add_parser("check", help="Run checks for orchestration environment")
        _add_common_args(check_parser)
        check_parser.add_argument("--critical-files", action="store_true", help="Check for critical orchestration files")
        check_parser.add_argument("--env", action="store_true", help="Check orchestration environment")

    # Always add legacy arguments for backward compatibility
    _add_legacy_args(parser)

    args = parser.parse_args()
    
    if hasattr(args, 'command') and args.command:
        sys.exit(_execute_command(args.command, args))
    else:
        sys.exit(_handle_legacy_args(args))

if __name__ == "__main__":
    main()
