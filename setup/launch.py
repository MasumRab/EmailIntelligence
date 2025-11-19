"""
Core execution functions for the EmailIntelligence launcher.

This module contains the core command execution and legacy argument handling logic.
It is used by the modular launcher system (main.py, args.py, routing.py).
"""

import logging
from setup.project_config import get_project_config

# Import command pattern components (with error handling for refactors)
try:
    from setup.commands.command_factory import get_command_factory
except ImportError:
    # Command pattern not available, will use legacy mode
    get_command_factory = None

# Define COMMAND_PATTERN_AVAILABLE at module level
COMMAND_PATTERN_AVAILABLE = get_command_factory is not None

# Try to import dotenv related variables and functions
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    load_dotenv = None
    DOTENV_AVAILABLE = False

logger = logging.getLogger(__name__)

ROOT_DIR = get_project_config().root_dir
VENV_DIR = "venv"






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
    if getattr(args, 'critical_files', False) or (not getattr(args, 'env', False)):
        if not check_critical_files():
            success = False

    # Run environment validation if requested
    if getattr(args, 'env', False):
        if not validate_environment():
            success = False

    # If no specific check was requested, run all checks
    if not getattr(args, 'critical_files', False) and not getattr(args, 'env', False):
        if not check_critical_files() or not validate_environment():
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


def start_services(args):
    """Start the required services based on arguments."""
    from setup.services import start_backend, start_node_service, start_gradio_ui

    api_url = args.api_url or f"http://{args.host}:{args.port}"

    if not args.frontend_only:
        start_backend(args.host, args.port, args.debug)
        start_node_service(ROOT_DIR / "backend" / "server-ts", "TypeScript Backend", 8001, api_url)

    if not args.api_only:
        start_gradio_ui(args.host, 7860, args.share, args.debug)
        start_node_service(ROOT_DIR / "client", "Frontend Client", args.frontend_port, api_url)


def check_critical_files() -> bool:
    """Check for critical files that must exist in the orchestration-tools branch."""
    # Critical files that are essential for orchestration
    critical_files = [
        # Core orchestration scripts
        "scripts/install-hooks.sh",
        "scripts/cleanup_orchestration.sh",
        "scripts/sync_setup_worktrees.sh",
        "scripts/reverse_sync_orchestration.sh",

        # Git hooks
        "scripts/hooks/pre-commit",
        "scripts/hooks/post-commit",
        "scripts/hooks/post-commit-setup-sync",
        "scripts/hooks/post-merge",
        "scripts/hooks/post-checkout",
        "scripts/hooks/post-push",

        # Shared libraries
        "scripts/lib/common.sh",
        "scripts/lib/error_handling.sh",
        "scripts/lib/git_utils.sh",
        "scripts/lib/logging.sh",
        "scripts/lib/validation.sh",

        # Setup files
        "setup/launch.py",
        "setup/pyproject.toml",
        "setup/requirements.txt",
        "setup/requirements-dev.txt",

        # Root wrapper
        "launch.py",
    ]

    missing_files = []

    # Check for missing critical files
    for file_path in critical_files:
        full_path = ROOT_DIR / file_path
        if not full_path.exists():
            missing_files.append(file_path)

    if missing_files:
        logger.error("Missing critical files:")
        for file_path in missing_files:
            logger.error(f"  - {file_path}")
        logger.error("Please restore these critical files for proper orchestration functionality.")
        return False

    logger.info("All critical files are present.")
    return True


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


