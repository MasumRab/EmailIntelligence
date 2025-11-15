import argparse
import logging
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

from setup.environment import (
    check_python_version,
    create_venv,
    get_python_executable,
    get_venv_executable,
    install_package_manager,
    setup_dependencies,
    download_nltk_data,
    validate_environment,
    validate_port,
    validate_host,
    is_conda_available,
    activate_conda_env,
    get_conda_env_info,
)
from setup.process_manager import ProcessManager
from setup.project_config import get_project_config
from setup import test_stages

# --- Constants ---
ROOT_DIR = get_project_config().root_dir
VENV_DIR = "venv"
DOTENV_AVAILABLE = find_dotenv()

# --- Global Variables ---
process_manager = ProcessManager()
CONDA_ENV_NAME = "emailintelligence"  # Default Conda environment name

# --- Dynamic Imports for Command Pattern (if available) ---
COMMAND_PATTERN_AVAILABLE = False
try:
    from src.command_pattern import get_command_factory, initialize_all_services, get_container

    COMMAND_PATTERN_AVAILABLE = True
except ImportError:
    logging.warning("Command pattern modules not found. Running in legacy mode.")


# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# --- Helper Functions ---
def run_command(
    cmd: list,
    description: str,
    cwd: Path = ROOT_DIR,
    shell: bool = False,
    capture_output: bool = False,
    text: bool = False,
    timeout: int = None,
) -> bool:
    """Run a shell command and log its output."""
    logger.info(f"{description}...")
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=shell,
            capture_output=capture_output,
            text=text,
            timeout=timeout,
            check=True,
        )
        if capture_output:
            logger.debug(result.stdout)
        logger.info(f"{description} completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"{description} failed: {e}")
        if capture_output:
            logger.error(f"Stdout: {e.stdout}")
            logger.error(f"Stderr: {e.stderr}")
        return False
    except subprocess.TimeoutExpired as e:
        logger.error(f"{description} timed out: {e}")
        if capture_output:
            logger.error(f"Stdout: {e.stdout}")
            logger.error(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        logger.error(f"Command not found: {cmd[0]}. Please ensure it is installed and in your PATH.")
        return False


def download_nltk_data(venv_path: Path = None):
    """Download NLTK data if not already present."""
    nltk_data_path = Path.home() / "nltk_data"
    if nltk_data_path.exists():
        logger.info("NLTK data already exists.")
        return

    logger.info("Downloading NLTK data (punkt, averaged_perceptron_tagger, stopwords, wordnet, omw-1.4)...")
    python_exe = get_python_executable(venv_path)
    download_script = """
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    nltk.download('punkt')
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except nltk.downloader.DownloadError:
    nltk.download('averaged_perceptron_tagger')
try:
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except nltk.downloader.DownloadError:
    nltk.download('wordnet')
try:
    nltk.data.find('corpora/omw-1.4')
except nltk.downloader.DownloadError:
    nltk.download('omw-1.4')
print("NLTK data download completed.")
"""
    result = subprocess.run(
        [python_exe, "-c", download_script],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        logger.warning(f"NLTK data download failed: {result.stderr}")
        logger.warning("Continuing setup without NLTK data...")
    else:
        logger.info("NLTK data downloaded successfully.")


def check_uvicorn_installed() -> bool:
    """Check if uvicorn is installed."""
    python_exe = get_python_executable()
    try:
        result = subprocess.run(
            [python_exe, "-c", "import uvicorn"], capture_output=True, text=True
        )
        if result.returncode == 0:
            logger.info("uvicorn is available.")
            return True
        else:
            logger.error("uvicorn is not installed.")
            return False
    except FileNotFoundError:
        logger.error("Python executable not found.")
        return False

def check_node_npm_installed() -> bool:
    """Check if Node.js and npm are installed and available."""
    if not shutil.which("node"):
        logger.error("Node.js is not installed. Please install it to continue.")
        return False
    if not shutil.which("npm"):
        logger.error("npm is not installed. Please install it to continue.")
        return False
    return True

def install_nodejs_dependencies(directory: str, update: bool = False) -> bool:
    """Install Node.js dependencies in a given directory."""
    pkg_json_path = ROOT_DIR / directory / "package.json"
    if not pkg_json_path.exists():
        logger.debug(f"No package.json in '{directory}/', skipping npm install.")
        return True

    if not check_node_npm_installed():
        return False

    cmd = ["npm", "update" if update else "install"]
    desc = f"{('Updating' if update else 'Installing')} Node.js dependencies for '{directory}/'"
    return run_command(cmd, desc, cwd=ROOT_DIR / directory, shell=(os.name == "nt"))

def start_client():
    """Start the Node.js frontend."""
    logger.info("Starting Node.js frontend...")
    if not install_nodejs_dependencies("client"):
        return None

    # Install Node.js dependencies if node_modules doesn't exist
    node_modules_path = ROOT_DIR / "client" / "node_modules"
    if not node_modules_path.exists():
        logger.info("Installing Node.js dependencies...")

def start_server_ts():
    """Start the TypeScript backend server."""
    logger.info("Starting TypeScript backend server...")
    # Check if npm is available
    if not shutil.which("npm"):
        logger.warning("npm not found. Skipping TypeScript backend server startup.")
        return None

    # Check if package.json exists
    pkg_json_path = ROOT_DIR / "backend" / "server-ts" / "package.json"
    if not pkg_json_path.exists():
        logger.debug(
            "No package.json in 'backend/server-ts/', skipping TypeScript backend server startup."
        )
        return None

    # Install Node.js dependencies if node_modules doesn't exist
    node_modules_path = ROOT_DIR / "backend" / "server-ts" / "node_modules"
    if not node_modules_path.exists():
        logger.info("Installing TypeScript server dependencies...")


# --- Service Startup Functions ---
def start_backend(host: str, port: int, debug: bool = False):
    python_exe = get_python_executable()
    cmd = [
        python_exe,
        "-m",
        "uvicorn",
        "src.main:create_app",
        "--factory",
        "--host",
        host,
        "--port",
        str(port),
    ]
    if debug:
        cmd.append("--reload")
    logger.info(f"Starting backend on {host}:{port}")
    process = subprocess.Popen(cmd, cwd=ROOT_DIR)
    process_manager.add_process(process)

def start_node_service(service_path: Path, service_name: str, port: int, api_url: str):
    """Start a Node.js service."""
    if not service_path.exists():
        logger.warning(f"{service_name} path not found at {service_path}, skipping.")
        return
    logger.info(f"Starting {service_name} on port {port}...")
    env = os.environ.copy()
    env["PORT"] = str(port)
    env["VITE_API_URL"] = api_url
    process = subprocess.Popen(["npm", "start"], cwd=service_path, env=env)
    process_manager.add_process(process)

def setup_node_dependencies(service_path: Path, service_name: str):
    """Install npm dependencies for a Node.js service."""
    if not (service_path / "package.json").exists():
        logger.warning(
            f"package.json not found for {service_name}, skipping dependency installation."
        )
        return
    logger.info(f"Installing npm dependencies for {service_name}...")
    run_command(["npm", "install"], f"Installing {service_name} dependencies", cwd=service_path)

def start_gradio_ui(host, port, share, debug):
    logger.info("Starting Gradio UI...")
    python_exe = get_python_executable()
    cmd = [python_exe, "-m", "src.main"]  # Assuming Gradio is launched from main
    if share:
        cmd.append("--share")
    if debug:
        cmd.append("--debug")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)
    process = subprocess.Popen(cmd, cwd=ROOT_DIR, env=env)
    process_manager.add_process(process)

def handle_setup(args, venv_path):
    """Handles the complete setup process."""
    logger.info("Starting environment setup...")

    if args.use_conda:
        # For Conda, we assume the environment is already set up
        # Could add Conda environment creation here in the future
        logger.info("Using Conda environment - assuming dependencies are already installed")
    else:
        # Use venv
        create_venv(venv_path, args.force_recreate_venv)
        install_package_manager(venv_path, "uv")
        setup_dependencies(venv_path, False)
        if not args.no_download_nltk:
            download_nltk_data(venv_path)

        # Setup Node.js dependencies
        setup_node_dependencies(ROOT_DIR / "client", "Frontend Client")
        setup_node_dependencies(ROOT_DIR / "backend" / "server-ts", "TypeScript Backend")
    logger.info("Setup complete.")

def prepare_environment(args):
    """Prepares the environment for running the application."""
    if not args.no_venv:
        # Try conda first
        if not activate_conda_env():
            venv_path = ROOT_DIR / VENV_DIR
            create_venv(venv_path)
        if args.update_deps:
            setup_dependencies(ROOT_DIR / VENV_DIR, False)
    if not args.no_download_nltk:
        download_nltk_data()

def start_services(args):
    """Starts the required services based on arguments."""
    api_url = args.api_url or f"http://{args.host}:{args.port}"

    if not args.frontend_only:
        start_backend(args.host, args.port, args.debug)
        start_node_service(ROOT_DIR / "backend" / "server-ts", "TypeScript Backend", 8001, api_url)

    if not args.api_only:
        start_gradio_ui(args.host, 7860, args.share, args.debug)
        start_node_service(ROOT_DIR / "client", "Frontend Client", args.frontend_port, api_url)

def handle_test_stage(args):
    """Handles the test stage execution."""
    logger.info("Starting test stage...")
    results = []
    if args.unit:
        results.append(test_stages.run_unit_tests(args.coverage, args.debug))
    if args.integration:
        results.append(test_stages.run_integration_tests(args.coverage, args.debug))
    if args.e2e:
        results.append(test_stages.run_e2e_tests(headless=not args.debug, debug=args.debug))
    if args.performance:
        results.append(test_stages.run_performance_tests(duration=300, users=10, debug=args.debug))
    if args.security:
        results.append(
            test_stages.run_security_tests(
                target_url=f"http://{args.host}:{args.port}", debug=args.debug
            )
        )

    # If no specific test type is selected, run a default set (e.g., unit and integration)
    if not any([args.unit, args.integration, args.e2e, args.performance, args.security]):
        logger.info("No specific test type selected, running unit and integration tests.")
        results.append(test_stages.run_unit_tests(args.coverage, args.debug))
        results.append(test_stages.run_integration_tests(args.coverage, args.debug))

    if all(results):
        logger.info("All tests passed successfully.")
        sys.exit(0)
    else:
        logger.error("Some tests failed.")
        sys.exit(1)

def print_system_info():
    """Print detailed system, Python, and project configuration information."""
    import platform
    import sys

    print("=== System Information ===")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")

    print("\n=== Project Information ===")
    print(f"Project Root: {ROOT_DIR}")
    print(f"Python Path: {os.environ.get('PYTHONPATH', 'Not set')}")

    print("\n=== Environment Status ===")
    venv_path = ROOT_DIR / VENV_DIR
    if venv_path.exists():
        print(f"Virtual Environment: {venv_path} (exists)")
        python_exe = get_venv_executable(venv_path, "python")
        if python_exe.exists():
            print(f"Venv Python: {python_exe}")
        else:
            print("Venv Python: Not found")
    else:
        print(f"Virtual Environment: {venv_path} (not created)")

    conda_available = is_conda_available()
    print(f"Conda Available: {conda_available}")
    if conda_available:
        conda_env = os.environ.get("CONDA_DEFAULT_ENV", "None")
        print(f"Current Conda Env: {conda_env}")

    node_available = check_node_npm_installed()
    print(f"Node.js/npm Available: {node_available}")

    print("\n=== Configuration Files ===")
    config_files = [
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
        "package.json",
        "launch-user.env",
        ".env",
    ]
    for cf in config_files:
        exists = (ROOT_DIR / cf).exists()
        print(f"{cf}: {'Found' if exists else 'Not found'}")

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
    parser.add_argument("--env-file", type=str, help="Specify environment file to load.")
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
    if COMMAND_PATTERN_AVAILABLE and initialize_all_services and get_container:
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

    # Check command for orchestration-tools branch
    check_parser = subparsers.add_parser("check", help="Run checks for orchestration environment")
    _add_common_args(check_parser)
    check_parser.add_argument("--critical-files", action="store_true", help="Check for critical orchestration files")
    check_parser.add_argument("--env", action="store_true", help="Check orchestration environment")

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
        args.conda_env and args.conda_env != "base"  # Only if explicitly set to non-default
    ):
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