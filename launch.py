#!/usr/bin/env python3
"""
EmailIntelligence Launcher

This script provides a unified way to launch the EmailIntelligence application,
automating environment setup, dependency management, and process execution.
It ensures that the application runs in a consistent environment, whether for
development, testing, or production.

Key Features:
-   **Python Version Discovery**: Automatically detects a compatible Python
    interpreter (3.11-3.12) and re-executes itself if necessary.
-   **Virtual Environment Management**: Creates and manages a local Python
    virtual environment in `./venv` to isolate dependencies.
-   **Dependency Installation**: Installs required Python packages from
    `requirements.txt` and stage-specific files (e.g., `requirements-dev.txt`).
-   **NLTK Data Download**: Ensures necessary NLTK data models are downloaded.
-   **Component Execution**: Starts the backend FastAPI server and the frontend
    Vite development server as separate processes.
-   **Graceful Shutdown**: Handles SIGINT/SIGTERM signals to terminate all
    spawned processes gracefully.

Usage:
    python launch.py [arguments]

Arguments can be viewed by running:
    python launch.py --help
"""

import argparse
import json
import logging
import os
import platform
import shutil
import signal
import subprocess
import sys
import time
import venv
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")

# Global list to keep track of subprocesses
processes = []


def _handle_sigint(signum, frame):
    """
    Handles SIGINT and SIGTERM signals for graceful shutdown.

    Terminates all child processes tracked in the global `processes` list.

    Args:
        signum: The signal number.
        frame: The current stack frame.
    """
    logger.info("Received SIGINT/SIGTERM, shutting down...")
    for p in processes:
        if p.poll() is None:  # Check if process is still running
            logger.info(f"Terminating process {p.pid}...")
            p.terminate()
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning(f"Process {p.pid} did not terminate gracefully, killing.")
                p.kill()
    sys.exit(0)


def _setup_signal_handlers():
    """Sets up signal handlers for SIGINT and SIGTERM."""
    signal.signal(signal.SIGINT, _handle_sigint)
    signal.signal(signal.SIGTERM, _handle_sigint)


# Constants
PYTHON_MIN_VERSION = (3, 11)
PYTHON_MAX_VERSION = (3, 12)
VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"
REQUIREMENTS_VERSIONS_FILE = "requirements_versions.txt"

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent


def check_python_version() -> bool:
    """
    Checks if the current Python version is within the supported range.

    Returns:
        True if the version is supported, False otherwise.
    """
    current_version = sys.version_info[:2]
    if current_version < PYTHON_MIN_VERSION:
        logger.error(f"Python {'.'.join(map(str, PYTHON_MIN_VERSION))} or higher is required")
        return False
    if current_version > PYTHON_MAX_VERSION:
        logger.warning(
            f"Python {'.'.join(map(str, current_version))} is not officially supported. "
            f"Recommended version is {'.'.join(map(str, PYTHON_MAX_VERSION))} or lower."
        )
    return True


def is_venv_available() -> bool:
    """
    Checks if a virtual environment is available and properly configured.

    Returns:
        True if a virtual environment exists and contains a Python executable.
    """
    venv_path = ROOT_DIR / VENV_DIR
    if os.name == "nt":  # Windows
        return venv_path.exists() and (venv_path / "Scripts" / "python.exe").exists()
    else:  # Unix-based systems
        return venv_path.exists() and (venv_path / "bin" / "python").exists()


def create_venv() -> bool:
    """
    Creates a new virtual environment.

    Returns:
        True if the virtual environment was created successfully, False otherwise.
    """
    venv_path = ROOT_DIR / VENV_DIR
    if venv_path.exists():
        logger.info(f"Virtual environment already exists at {venv_path}")
        return True

    logger.info(f"Creating virtual environment at {venv_path}")
    try:
        venv.create(venv_path, with_pip=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create virtual environment: {e}")
        return False


def get_python_executable() -> str:
    """
    Gets the path to the appropriate Python executable.

    Returns the path to the virtual environment's Python executable if it exists,
    otherwise returns the path to the system's Python executable.

    Returns:
        The path to the Python executable.
    """
    if is_venv_available():
        if os.name == "nt":  # Windows
            return str(ROOT_DIR / VENV_DIR / "Scripts" / "python.exe")
        else:  # Unix-based systems
            return str(ROOT_DIR / VENV_DIR / "bin" / "python")
    return sys.executable


def install_requirements_from_file(requirements_file_path_str: str, update: bool = False) -> bool:
    """
    Installs or updates Python packages from a requirements file.

    Args:
        requirements_file_path_str: The path to the requirements file, relative to the project root.
        update: If True, upgrades existing packages.

    Returns:
        True if installation was successful, False otherwise.
    """
    python = get_python_executable()
    requirements_path = ROOT_DIR / requirements_file_path_str

    if not requirements_path.exists():
        logger.error(f"Requirements file not found at {requirements_path}")
        return False

    cmd = [python, "-m", "pip", "install"]
    if update:
        cmd.append("--upgrade")
    cmd.extend(["-r", str(requirements_path)])

    logger.info(
        f"{'Updating' if update else 'Installing'} dependencies from {requirements_path.name}..."
    )
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies from {requirements_path.name}.")
        logger.error(f"pip stdout:\n{e.stdout}")
        logger.error(f"pip stderr:\n{e.stderr}")
        return False


install_dependencies = install_requirements_from_file


def download_nltk_data() -> bool:
    """
    Downloads necessary NLTK data models.

    Returns:
        True if the download process completes successfully, False otherwise.
    """
    python = get_python_executable()

    logger.info("Downloading NLTK data...")
    cmd = [
        python,
        "-c",
        "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True);",
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info("NLTK data download process completed.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error("Failed to download NLTK data.")
        logger.error(f"NLTK download stderr:\n{e.stderr}")
        return False


def _get_primary_requirements_file() -> str:
    """
    Determines the primary requirements file to use.

    Prioritizes `requirements_versions.txt` if it exists, otherwise falls back
    to `requirements.txt`.

    Returns:
        The name of the requirements file to use.
    """
    if (ROOT_DIR / REQUIREMENTS_VERSIONS_FILE).exists():
        return REQUIREMENTS_VERSIONS_FILE
    else:
        logger.info(f"'{REQUIREMENTS_VERSIONS_FILE}' not found, using '{REQUIREMENTS_FILE}'.")
        return REQUIREMENTS_FILE


def prepare_environment(args: argparse.Namespace) -> bool:
    """
    Prepares the full application environment.

    This includes checking the Python version, creating/validating the virtual
    environment, and installing all necessary dependencies.

    Args:
        args: The parsed command-line arguments.

    Returns:
        True if the environment is successfully prepared, False otherwise.
    """
    if not args.skip_python_version_check and not check_python_version():
        return False

    if not args.no_venv:
        if not is_venv_available():
            logger.info(f"Virtual environment not found at './{VENV_DIR}'. Creating...")
            if not create_venv():
                return False
            # Install dependencies after creating venv
            if not install_dependencies(_get_primary_requirements_file()):
                return False
        elif args.update_deps:
            if not install_dependencies(_get_primary_requirements_file(), update=True):
                return False

    if not args.no_download_nltk:
        if not download_nltk_data():
            return False

    return True


def start_backend(args: argparse.Namespace, python_executable: str) -> Optional[subprocess.Popen]:
    """
    Starts the backend FastAPI server.

    Args:
        args: The parsed command-line arguments.
        python_executable: The path to the Python executable to use.

    Returns:
        A `subprocess.Popen` object for the running server, or None on failure.
    """
    actual_host = "0.0.0.0" if args.listen else args.host
    logger.info(f"Starting backend server on {actual_host}:{args.port}...")
    cmd = [python_executable, "-m", "uvicorn", "backend.python_backend.main:app", "--host", actual_host, "--port", str(args.port)]
    if args.debug:
        cmd.append("--reload")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)
    try:
        process = subprocess.Popen(cmd, env=env)
        processes.append(process)
        return process
    except Exception as e:
        logger.error(f"Failed to start backend server: {e}")
        return None


def start_gradio_ui(args: argparse.Namespace, python_executable: str) -> Optional[subprocess.Popen]:
    """
    Starts the Gradio UI server, ensuring frontend dependencies are installed.

    Args:
        args: The parsed command-line arguments.
        python_executable: The path to the Python executable to use.

    Returns:
        A `subprocess.Popen` object for the running server, or None on failure.
    """
    logger.info("Starting Gradio UI...")

    try:
        subprocess.check_call(["node", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Node.js is not installed or not found in PATH. Cannot start frontend.")
        return None

    client_dir = ROOT_DIR / "client"
    if (client_dir / "package.json").exists():
        npm_executable = shutil.which("npm")
        if not npm_executable:
            logger.error(
                f"The 'npm' command was not found in your system's PATH. "
                f"Please ensure Node.js and npm are correctly installed and that the npm installation directory is added to your PATH environment variable. "
                f"Attempted to find 'npm' for the client in: {client_dir}"
            )
            return None

        logger.info(f"Found package.json in {client_dir}. Running npm install...")
        try:
            install_result = subprocess.run(
                [npm_executable, "install"], cwd=client_dir, capture_output=True, text=True, check=False
            )
            if install_result.returncode != 0:
                logger.error(f"Failed to install frontend dependencies in {client_dir}.")
                logger.error(f"npm stdout:\n{install_result.stdout}")
                logger.error(f"npm stderr:\n{install_result.stderr}")
                return None
        except Exception as e:
            logger.error(f"Error running npm install in {client_dir}: {e}")
            return None

    gradio_script_path = ROOT_DIR / "backend" / "python_backend" / "gradio_app.py"
    cmd = [python_executable, str(gradio_script_path)]
    if hasattr(args, 'gradio_port') and args.gradio_port:
        cmd.extend(["--port", str(args.gradio_port)])
    if hasattr(args, 'debug') and args.debug:
        cmd.append("--debug")
    if hasattr(args, 'share') and args.share:
        cmd.append("--share")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)

    try:
        process = subprocess.Popen(cmd, env=env)
        processes.append(process)
        return process
    except Exception as e:
        logger.error(f"Failed to start Gradio UI: {e}")
        return None


def run_application(args: argparse.Namespace) -> int:
    """
    Runs the application components based on the provided arguments.

    Args:
        args: The parsed command-line arguments.

    Returns:
        An exit code (0 for success, 1 for failure).
    """
    python_executable = get_python_executable()
    if args.api_only:
        backend_process = start_backend(args, python_executable)
        if backend_process:
            backend_process.wait()
        return 0 if backend_process else 1

    backend_process = start_backend(args, python_executable)
    gradio_process = start_gradio_ui(args, python_executable)

    if not backend_process or not gradio_process:
        logger.error("Failed to start one or more application components.")
        return 1

    logger.info("Backend and Gradio UI started. Press Ctrl+C to stop.")
    try:
        while True:
            if backend_process.poll() is not None or gradio_process.poll() is not None:
                logger.error("A service exited unexpectedly.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Graceful shutdown initiated by user.")
    finally:
        _handle_sigint(None, None)
    return 0


def _print_system_info():
    """Prints detailed system and environment information for debugging."""
    print("\n--- System Information ---")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print(f"Project Root: {ROOT_DIR}")
    print(f"Venv Active: {is_venv_available()}")
    print(f"Python Executable: {get_python_executable()}")
    print("--- End System Information ---")


def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments for the launcher.

    Returns:
        An `argparse.Namespace` object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="EmailIntelligence Launcher")
    parser.add_argument("--no-venv", action="store_true", help="Don't use a virtual environment")
    parser.add_argument("--update-deps", action="store_true", help="Update dependencies")
    parser.add_argument("--skip-python-version-check", action="store_true", help="Skip Python version check")
    parser.add_argument("--stage", choices=["dev", "test"], default="dev", help="Application stage")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    parser.add_argument("--host", default="127.0.0.1", help="Server host")
    parser.add_argument("--api-only", action="store_true", help="Run only the API server")
    parser.add_argument("--frontend-only", action="store_true", help="Run only the frontend")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--no-download-nltk", action="store_true", help="Skip NLTK data download")
    parser.add_argument("--system-info", action="store_true", help="Print system information")
    return parser.parse_args()


def main() -> int:
    """
    Main entry point for the launcher script.

    It handles Python version discovery, argument parsing, environment setup,
    and application execution.

    Returns:
        An exit code (0 for success, 1 for failure).
    """
    if os.environ.get("LAUNCHER_REEXEC_GUARD") != "1":
        current_major, current_minor = sys.version_info[:2]
        if not (PYTHON_MIN_VERSION <= (current_major, current_minor) <= PYTHON_MAX_VERSION):
            logger.info("Incompatible Python version. Searching for a compatible one...")
            for py_cmd in [f"python{v[0]}.{v[1]}" for v in [PYTHON_MIN_VERSION, PYTHON_MAX_VERSION]] + ["python3"]:
                if found_path := shutil.which(py_cmd):
                    logger.info(f"Found compatible Python at {found_path}. Re-executing...")
                    os.environ["LAUNCHER_REEXEC_GUARD"] = "1"
                    os.execve(found_path, [found_path, __file__] + sys.argv[1:], os.environ)
            logger.error("Could not find a compatible Python version.")
            return 1

    _setup_signal_handlers()
    args = parse_arguments()

    if args.system_info:
        _print_system_info()
        return 0

    if not prepare_environment(args):
        return 1

    return run_application(args)


if __name__ == "__main__":
    sys.exit(main())