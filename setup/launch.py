import sys
import os
import time
import logging
import argparse
from setup.project_config import get_project_config

# Import from setup modules
from setup.environment import (
    prepare_environment,
    handle_setup,
)
from setup.validation import (
    validate_environment,
    validate_port,
    validate_host,
    check_critical_files,
    validate_orchestration_environment,
    check_python_version,
)
from setup.utils import print_system_info
from setup.container import get_container, initialize_all_services
from setup.utils import process_manager
# TODO: The function 'start_services' appears to be missing from the codebase.
# from setup.services import start_services
from setup.commands import COMMAND_PATTERN_AVAILABLE, get_command_factory

# Try to import dotenv related variables and functions
try:
    from dotenv import load_dotenv

    DOTENV_AVAILABLE = True
except ImportError:
    load_dotenv = None
    DOTENV_AVAILABLE = False

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

logger = logging.getLogger(__name__)

ROOT_DIR = get_project_config().root_dir
VENV_DIR = "venv"


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
        "--force-recreate-venv",
        action="store_true",
        help="Force recreation of the venv.",
    )
    parser.add_argument(
        "--use-conda",
        action="store_true",
        help="Use Conda environment instead of venv.",
    )
    parser.add_argument(
        "--conda-env",
        type=str,
        default="base",
        help="Conda environment name to use (default: base).",
    )
    parser.add_argument(
        "--no-venv",
        action="store_true",
        help="Don't create or use a virtual environment.",
    )
    parser.add_argument(
        "--update-deps",
        action="store_true",
        help="Update dependencies before launching.",
    )
    parser.add_argument(
        "--skip-torch-cuda-test",
        action="store_true",
        help="Skip CUDA availability test for PyTorch.",
    )
    parser.add_argument(
        "--reinstall-torch", action="store_true", help="Reinstall PyTorch."
    )
    parser.add_argument(
        "--skip-python-version-check",
        action="store_true",
        help="Skip Python version check.",
    )
    parser.add_argument(
        "--no-download-nltk", action="store_true", help="Skip downloading NLTK data."
    )
    parser.add_argument(
        "--skip-prepare",
        action="store_true",
        help="Skip all environment preparation steps.",
    )

    # Application Configuration
    parser.add_argument(
        "--port", type=int, default=8000, help="Specify the port to run on."
    )
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Specify the host to run on."
    )
    parser.add_argument(
        "--frontend-port",
        type=int,
        default=5173,
        help="Specify the frontend port to run on.",
    )
    parser.add_argument(
        "--api-url", type=str, help="Specify the API URL for the frontend."
    )
    parser.add_argument(
        "--api-only",
        action="store_true",
        help="Run only the API server without the frontend.",
    )
    parser.add_argument(
        "--frontend-only",
        action="store_true",
        help="Run only the frontend without the API server.",
    )
    parser.add_argument("--env-file", type=str, help="Specify a custom .env file.")

    # Testing Options
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Generate coverage report when running tests.",
    )
    parser.add_argument("--unit", action="store_true", help="Run unit tests.")
    parser.add_argument(
        "--integration", action="store_true", help="Run integration tests."
    )
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests.")
    parser.add_argument(
        "--performance", action="store_true", help="Run performance tests."
    )
    parser.add_argument("--security", action="store_true", help="Run security tests.")

    # Extensions and Models
    parser.add_argument(
        "--skip-extensions", action="store_true", help="Skip loading extensions."
    )
    parser.add_argument(
        "--skip-models", action="store_true", help="Skip downloading models."
    )

    # Advanced Options
    parser.add_argument(
        "--system-info", action="store_true", help="Print system information then exit."
    )
    parser.add_argument("--share", action="store_true", help="Create a public URL.")
    parser.add_argument(
        "--listen", action="store_true", help="Make the server listen on network."
    )
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
    setup_parser = subparsers.add_parser(
        "setup", help="Set up the development environment"
    )
    _add_common_args(setup_parser)

    # Run command
    run_parser = subparsers.add_parser(
        "run", help="Run the EmailIntelligence application"
    )
    _add_common_args(run_parser)
    run_parser.add_argument(
        "--dev", action="store_true", help="Run in development mode"
    )

    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests")
    _add_common_args(test_parser)

    # Guide-dev command
    guide_dev_parser = subparsers.add_parser(
        "guide-dev", help="Interactive guide for daily development tasks (e.g., choosing a branch)."
    )
    _add_common_args(guide_dev_parser)

    # Guide-pr command
    guide_pr_parser = subparsers.add_parser(
        "guide-pr", help="Interactive guide for merging branches (e.g., choosing a merge strategy)."
    )
    _add_common_args(guide_pr_parser)

    test_parser.add_argument("--unit", action="store_true", help="Run unit tests")
    test_parser.add_argument(
        "--integration", action="store_true", help="Run integration tests"
    )
    test_parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    test_parser.add_argument(
        "--performance", action="store_true", help="Run performance tests"
    )
    test_parser.add_argument(
        "--security", action="store_true", help="Run security tests"
    )
    test_parser.add_argument(
        "--coverage", action="store_true", help="Generate coverage report"
    )
    test_parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue running tests even if some fail",
    )

    # Legacy argument parsing for backward compatibility
    parser.add_argument(
        "--setup", action="store_true", help="Set up the environment (legacy)"
    )
    parser.add_argument(
        "--stage",
        choices=["dev", "test"],
        default="dev",
        help="Application mode (legacy)",
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
    # Handle check command directly in orchestration-tools branch
    if command_name == "check":
        return _execute_check_command(args)

    # For other commands, use command pattern if available
    if COMMAND_PATTERN_AVAILABLE:
        factory = get_command_factory()
        command = factory.create_command(command_name, args)

        if command is None:
            logger.error(f"Unknown command: {command_name}")
            return 1

        try:
            return command.execute()
        finally:
            command.cleanup()
    else:
        logger.error(
            f"Command pattern not available and '{command_name}' is not a built-in command"
        )
        return 1


def _execute_check_command(args) -> int:
    """Execute the check command for orchestration validation."""
    logger.info("Running orchestration checks...")

    success = True

    # Run critical files check if requested
    if args.critical_files or (not args.env):
        if not check_critical_files():
            success = False

    # Run environment validation if requested
    if args.env:
        if not validate_orchestration_environment():
            success = False

    # If no specific check was requested, run all checks
    if not args.critical_files and not args.env:
        if not validate_orchestration_environment():
            success = False

    if success:
        logger.info("All orchestration checks passed!")
        return 0
    else:
        logger.error("Orchestration checks failed!")
        return 1


def _handle_legacy_args(args) -> int:
    """Handle legacy argument parsing for backward compatibility."""
    # Setup WSL environment if applicable (early setup)
    from setup.environment import setup_wsl_environment, check_wsl_requirements

    setup_wsl_environment()
    check_wsl_requirements()

    if not args.skip_python_version_check:
        check_python_version()

    logging.getLogger().setLevel(getattr(args, "loglevel", "INFO"))

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
    if (
        args.conda_env and args.conda_env != "base"
    ):  # Only if explicitly set to non-default
        CONDA_ENV_NAME = args.conda_env
        args.use_conda = True  # Set flag when conda env is specified
        # args.use_conda remains as set by command line argument

    # Check for system info first (doesn't need validation)
    if args.system_info:
        print_system_info()
        return 0

    # Validate environment if not skipping preparation
    # This includes checks for Python version, merge conflicts, required components,
    # and NLTK compatibility.
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
    from setup.environment import (
        is_conda_available,
        get_conda_env_info,
        activate_conda_env,
    )

    if args.use_conda:
        if not is_conda_available():
            logger.error("Conda is not available. Please install Conda or use venv.")
            return 1
        if not get_conda_env_info()["is_active"] and not activate_conda_env(
            args.conda_env
        ):
            logger.error(f"Failed to activate Conda environment: {args.conda_env}")
            return 1
        elif get_conda_env_info()["is_active"]:
            logger.info(
                f"Using existing Conda environment: {os.environ.get('CONDA_DEFAULT_ENV')}"
            )

    if not args.skip_prepare and not args.use_conda:
        prepare_environment(args)

    if args.system_info:
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
    # TODO: Restore this call once the 'start_services' function is found/restored.
    # start_services(args)

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
        logger.warning(
            "⚠️  You're using system Python. This may cause permission errors with pip."
        )
        logger.info("💡  Run 'python launch.py setup' to create a virtual environment")
        logger.info("   Then use: source venv/bin/activate")

    # Check if venv exists but not activated
    venv_path = ROOT_DIR / "venv" / "bin" / "python"
    if venv_path.exists() and python_path != venv_path:
        logger.info(
            "💡  Virtual environment exists. Activate it with: source venv/bin/activate"
        )


if __name__ == "__main__":
    main()
