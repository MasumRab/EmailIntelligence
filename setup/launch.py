#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

This module provides a unified entry point for setting up the development
environment, running tests, and launching services for the EmailIntelligence
application.
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
import venv
from pathlib import Path
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")

# Global paths
ROOT_DIR = Path(__file__).resolve().parent.parent

# Add project root to sys.path for module imports
sys.path.insert(0, str(ROOT_DIR))

# Import utilities from the setup package
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

# Try to import dotenv
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    load_dotenv = None

# --- Global state ---
# --- Constants ---
PYTHON_MIN_VERSION = (3, 11)
PYTHON_MAX_VERSION = (3, 12)
VENV_DIR = "venv"
CONDA_ENV_NAME = os.getenv("CONDA_ENV_NAME", "base")


# --- WSL Environment Functions ---
def setup_wsl_environment():
    """Setup WSL-specific environment variables if in WSL"""
    env_setup_wsl()


# --- Python Version Checking ---
def check_python_version():
    """Check if the current Python version is compatible."""
    val_check_python_version()


# --- Environment Validation ---
def check_required_components() -> bool:
    """Check for required components and configurations."""
    return check_required_components()


# --- Helper Functions ---
def get_venv_executable_path(venv_path: Path, executable: str) -> Path:
    """Get the path to a specific executable in the virtual environment."""
    return get_venv_executable(venv_path, executable)


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


# --- Setup Functions ---
def create_venv(venv_path: Path, recreate: bool = False):
    """Create a virtual environment."""
    from setup.environment import create_venv as env_create_venv
    env_create_venv(venv_path, recreate)


def install_package_manager(venv_path: Path, manager: str):
    """Install a package manager in the venv."""
    from setup.environment import install_package_manager as env_install_pm
    env_install_pm(venv_path, manager)


def setup_dependencies(venv_path: Path, use_poetry: bool = False):
    """Set up dependencies using the package manager."""
    from setup.environment import setup_dependencies as env_setup_deps
    env_setup_deps(venv_path, use_poetry)


def install_notmuch_matching_system():
    """Install notmuch matching system version."""
    from setup.environment import install_notmuch_matching_system as env_install_notmuch
    env_install_notmuch()


def download_nltk_data(venv_path=None):
    """Download NLTK data required by the application."""
    from setup.environment import download_nltk_data as env_download_nltk
    env_download_nltk(venv_path)


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


def setup_node_dependencies(service_path: Path, service_name: str):
    """Install npm dependencies for a Node.js service."""
    if not (service_path / "package.json").exists():
        logger.warning(
            f"package.json not found for {service_name}, skipping dependency installation."
        )
        return
    logger.info(f"Installing npm dependencies for {service_name}...")
    run_command(["npm", "install"], f"Installing {service_name} dependencies", cwd=service_path)


def install_nodejs_dependencies(directory: str, update: bool = False) -> bool:
    """Install Node.js dependencies in a given directory."""
    pkg_json_path = ROOT_DIR / directory / "package.json"
    if not pkg_json_path.exists():
        logger.debug(f"No package.json in '{directory}/', skipping npm install.")
        return True

    if not check_node_npm_installed():
        return False

    cmd = ["npm", "update" if update else "install"]
    desc = f"{'Updating' if update else 'Installing'} Node.js dependencies for '{directory}/'"
    return run_command(cmd, desc, cwd=ROOT_DIR / directory, shell=(os.name == "nt"))


def start_client():
    """Start the Node.js frontend."""
    logger.info("Starting Node.js frontend...")
    if not install_nodejs_dependencies("client"):
        return None


def start_server_ts():
    """Start the TypeScript backend server."""
    logger.info("Starting TypeScript backend server...")
    if not shutil.which("npm"):
        logger.warning("npm not found. Skipping TypeScript backend server startup.")
        return None

    pkg_json_path = ROOT_DIR / "backend" / "server-ts" / "package.json"
    if not pkg_json_path.exists():
        logger.debug(
            "No package.json in 'backend/server-ts/', skipping TypeScript backend server startup."
        )
        return None


# --- Service Startup Functions ---
def start_backend(host: str, port: int, debug: bool = False):
    """Start the Python backend server."""
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


def start_gradio_ui(host, port, share, debug):
    """Start the Gradio UI."""
    logger.info("Starting Gradio UI...")
    python_exe = get_python_executable()
    cmd = [python_exe, "-m", "src.main"]
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
        logger.info("Using Conda environment - assuming dependencies are already installed")
    else:
        create_venv(venv_path, args.force_recreate_venv)
        install_package_manager(venv_path, "uv")
        setup_dependencies(venv_path, False)
        if not args.no_download_nltk:
            download_nltk_data(venv_path)

        setup_node_dependencies(ROOT_DIR / "client", "Frontend Client")
        setup_node_dependencies(ROOT_DIR / "backend" / "server-ts", "TypeScript Backend")
    logger.info("Setup complete.")


def prepare_environment(args):
    """Prepares the environment for running the application."""
    if not args.no_venv:
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
        python_exe = get_venv_executable_path(venv_path, "python")
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
    """Add common arguments to the parser."""
    parser.add_argument(
        "--loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level.",
    )


def _add_legacy_args(parser):
    """Add legacy arguments - Maintained for Backward Compatibility."""
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
    parser.add_argument("--share", action="store_true", help="Create a public URL.")

    # Testing Options
    parser.add_argument(
        "--coverage", action="store_true", help="Generate coverage report when running tests."
    )
    parser.add_argument("--unit", action="store_true", help="Run unit tests.")
    parser.add_argument("--integration", action="store_true", help="Run integration tests.")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests.")
    parser.add_argument("--performance", action="store_true", help="Run performance tests.")
    parser.add_argument("--security", action="store_true", help="Run security tests.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")

    # Advanced Options
    parser.add_argument(
        "--system-info", action="store_true", help="Print system information then exit."
    )
    parser.add_argument("--listen", action="store_true", help="Make the server listen on network.")
    parser.add_argument(
        "--ngrok", type=str, help="Use ngrok to create a tunnel, specify ngrok region."
    )


def _handle_legacy_args(args) -> int:
    """Handle legacy argument parsing - Maintained for Backward Compatibility."""
    setup_wsl_environment()
    check_wsl_requirements()

    if not args.skip_python_version_check:
        check_python_version()

    if DOTENV_AVAILABLE:
        user_env_file = ROOT_DIR / "launch-user.env"
        if user_env_file.exists():
            load_dotenv(user_env_file)
            logger.info(f"Loaded user environment variables from {user_env_file}")
        else:
            logger.debug(f"User env file not found: {user_env_file}")

        env_file = args.env_file or ".env"
        if os.path.exists(env_file):
            logger.info(f"Loading environment variables from {env_file}")
            load_dotenv(env_file)

    global CONDA_ENV_NAME
    if args.conda_env and args.conda_env != "base":
        CONDA_ENV_NAME = args.conda_env
        args.use_conda = True

    if not args.skip_prepare and not validate_environment():
        return 1

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
        print_system_info()
        return 0

    if hasattr(args, "stage") and args.stage == "test":
        handle_test_stage(args)
        return 0

    if (
        getattr(args, "unit", False)
        or getattr(args, "integration", False)
        or getattr(args, "coverage", False)
    ):
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


def main():
    """Main entry point for the launcher."""
    parser = argparse.ArgumentParser(
        description="EmailIntelligence Unified Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    _add_legacy_args(parser)

    args = parser.parse_args()
    sys.exit(_handle_legacy_args(args))


if __name__ == "__main__":
    main()
