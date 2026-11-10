#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

This script provides a single, unified way to set up, manage, and run all
components of the EmailIntelligence application. It supports both legacy
arguments for backward compatibility and a modern command-based interface.

Features:
- Environment setup with virtual environment/conda management
- Service startup (FastAPI backend, Gradio UI, Node.js services)
- Test execution across multiple stages
- Orchestration validation and system health checks
- Cross-platform support
"""

import argparse
import atexit
import logging
import os
import platform
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to sys.path for imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import launch system modules
from scripts.automation.setup.validation import (
    check_python_version, check_for_merge_conflicts, check_required_components,
    validate_environment, validate_port, validate_host
)
from scripts.automation.setup.services import (
    start_services, start_backend, start_node_service, start_gradio_ui, validate_services
)
from scripts.automation.setup.environment import (
    handle_setup, prepare_environment, setup_wsl_environment, check_wsl_requirements,
    is_conda_available, get_conda_env_info, activate_conda_env
)
from scripts.automation.setup.utils import print_system_info, process_manager, find_project_root, get_python_executable

# Import project configuration
from scripts.automation.setup.project_config import get_project_config

# Import test stages
try:
    from scripts.automation.setup.test_stages import test_stages
except ImportError:
    # Fallback to deployment location
    try:
        from deployment.test_stages import test_stages
    except ImportError:
        test_stages = None

# Import command pattern components
try:
    from scripts.automation.setup.commands.command_factory import get_command_factory
    from scripts.automation.setup.container import get_container, initialize_all_services
    COMMAND_PATTERN_AVAILABLE = True
except ImportError:
    COMMAND_PATTERN_AVAILABLE = False
    get_command_factory = None
    get_container = None
    initialize_all_services = None

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

ROOT_DIR = get_project_config().root_dir
VENV_DIR = "venv"
CONDA_ENV_NAME = os.getenv("CONDA_ENV_NAME", "base")


def check_critical_files() -> bool:
    """Check for critical files required for the application."""
    config = get_project_config()
    critical_files = config.get_critical_files()
    
    missing_files = []
    for file_path in critical_files:
        full_path = ROOT_DIR / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        logger.error("Missing critical files:")
        for file_path in missing_files:
            logger.error(f"  - {file_path}")
        return False
    
    logger.info("All critical files are present.")
    return True


def validate_orchestration_environment() -> bool:
    """Run comprehensive validation for the orchestration environment."""
    logger.info("Running orchestration environment validation...")
    
    if not check_for_merge_conflicts():
        return False
    
    if not check_critical_files():
        return False
    
    logger.info("Orchestration environment validation passed.")
    return True


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
    parser.add_argument("--setup", action="store_true", help="Run environment setup.")
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
        "--skip-python-version-check", action="store_true", help="Skip Python version check."
    )
    parser.add_argument(
        "--no-download-nltk", action="store_true", help="Skip downloading NLTK data."
    )
    parser.add_argument(
        "--skip-prepare", action="store_true", help="Skip all environment preparation steps."
    )
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
    parser.add_argument(
        "--coverage", action="store_true", help="Generate coverage report when running tests."
    )
    parser.add_argument("--unit", action="store_true", help="Run unit tests.")
    parser.add_argument("--integration", action="store_true", help="Run integration tests.")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests.")
    parser.add_argument("--performance", action="store_true", help="Run performance tests.")
    parser.add_argument("--security", action="store_true", help="Run security tests.")
    parser.add_argument(
        "--system-info", action="store_true", help="Print system information then exit."
    )
    parser.add_argument("--share", action="store_true", help="Create a public URL.")
    parser.add_argument("--env-file", type=str, help="Specify environment file to load.")


def _execute_command(command_name: str, args) -> int:
    """Execute a command using the command pattern or built-in handlers."""
    if command_name == "check":
        return _execute_check_command(args)
    
    if COMMAND_PATTERN_AVAILABLE:
        factory = get_command_factory()
        command = factory.create_command(command_name, args)
        if command:
            try:
                return command.execute()
            finally:
                command.cleanup()
    
    logger.error(f"Command '{command_name}' is not supported in this mode.")
    return 1


def _execute_check_command(args) -> int:
    """Execute the check command for orchestration validation."""
    logger.info("Running orchestration checks...")
    success = True
    
    if getattr(args, 'critical_files', False) or (not getattr(args, 'env', False)):
        if not check_critical_files():
            success = False
    
    if getattr(args, 'env', False):
        if not validate_orchestration_environment():
            success = False
            
    return 0 if success else 1


def _handle_legacy_args(args) -> int:
    """Handle legacy argument parsing for backward compatibility."""
    setup_wsl_environment()
    check_wsl_requirements()

    if not getattr(args, 'skip_python_version_check', False):
        if not check_python_version():
            return 1

    logging.getLogger().setLevel(getattr(args, 'loglevel', 'INFO'))

    if DOTENV_AVAILABLE:
        user_env_file = ROOT_DIR / "launch-user.env"
        if user_env_file.exists():
            load_dotenv(user_env_file)
        
        env_file = getattr(args, 'env_file', None) or ".env"
        if os.path.exists(env_file):
            load_dotenv(env_file)

    if getattr(args, 'system_info', False):
        print_system_info()
        return 0

    if not getattr(args, 'skip_prepare', False) and not validate_environment():
        return 1

    if getattr(args, 'setup', False):
        handle_setup(args, ROOT_DIR / VENV_DIR)
        return 0

    if getattr(args, 'use_conda', False):
        if not is_conda_available():
            logger.error("Conda not available.")
            return 1
        if not activate_conda_env(getattr(args, 'conda_env', 'base')):
            return 1

    if not getattr(args, 'skip_prepare', False):
        prepare_environment(args)

    # Handle tests
    test_flags = ['unit', 'integration', 'e2e', 'performance', 'security']
    if any(getattr(args, flag, False) for flag in test_flags) or (hasattr(args, 'stage') and args.stage == 'test'):
        from scripts.automation.setup.test_stages import handle_test_stage
        handle_test_stage(args)
        return 0

    # Start services
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
    python_path = Path(sys.executable)
    if "/usr/bin/" in str(python_path) or "/usr/local/bin/" in str(python_path):
        logger.warning("⚠️  You're using system Python. This may cause permission errors.")
        logger.info("💡  Run 'python launch.py setup' to create a virtual environment.")


def main():
    _check_setup_warnings()

    if COMMAND_PATTERN_AVAILABLE and initialize_all_services and get_container:
        initialize_all_services(get_container())

    parser = argparse.ArgumentParser(description="EmailIntelligence Unified Launcher")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Setup subcommand
    setup_parser = subparsers.add_parser("setup", help="Set up the environment")
    _add_common_args(setup_parser)
    setup_parser.add_argument("--force-recreate-venv", action="store_true")

    # Run subcommand
    run_parser = subparsers.add_parser("run", help="Run the application")
    _add_common_args(run_parser)
    run_parser.add_argument("--dev", action="store_true")

    # Check subcommand
    check_parser = subparsers.add_parser("check", help="Run orchestration checks")
    _add_common_args(check_parser)
    check_parser.add_argument("--critical-files", action="store_true")
    check_parser.add_argument("--env", action="store_true")

    # Legacy support
    _add_legacy_args(parser)

    args = parser.parse_args()

    if args.command:
        return _execute_command(args.command, args)
    else:
        return _handle_legacy_args(args)


if __name__ == "__main__":
    sys.exit(main())
