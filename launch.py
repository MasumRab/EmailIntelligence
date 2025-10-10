#!/usr/bin/env python3
"""
EmailIntelligence Launcher

This script provides a unified way to launch the EmailIntelligence application,
automating environment setup, dependency management, and process execution.
It ensures that the application runs in a consistent environment, whether for
development, testing, or production.
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
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from enum import Enum, auto

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError

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
    """
    logger.info("Received SIGINT/SIGTERM, shutting down...")
    for p in processes:
        if p.poll() is None:
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
ROOT_DIR = Path(__file__).resolve().parent

def check_python_version() -> bool:
    """
    Checks if the current Python version is within the supported range.
    """
    current_version = sys.version_info[:2]
    if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
        logger.error(f"Python version {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}-{PYTHON_MAX_VERSION[0]}.{PYTHON_MAX_VERSION[1]} is required. You are using {platform.python_version()}")
        return False
    return True

def get_python_executable() -> str:
    """
    Gets the path to the Python executable from the poetry environment.
    """
    try:
        result = subprocess.run(["poetry", "env", "info", "-p"], capture_output=True, text=True, check=True)
        venv_path = result.stdout.strip()
        if os.name == "nt":
            return os.path.join(venv_path, "Scripts", "python.exe")
        else:
            return os.path.join(venv_path, "bin", "python")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("Could not determine poetry environment. Falling back to system python.")
        return sys.executable

def download_nltk_data() -> bool:
    """
    Downloads necessary NLTK data models.
    """
    python = get_python_executable()
    logger.info("Downloading NLTK data...")
    cmd = [python, "-c", "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True);"]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info("NLTK data download process completed.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to download NLTK data: {e.stderr}")
        return False

def prepare_environment(args: argparse.Namespace) -> bool:
    """
    Prepares the environment for running the application.
    """
    if not args.skip_python_version_check and not check_python_version():
        return False

    try:
        result = subprocess.run(["poetry", "env", "info", "-p"], capture_output=True, text=True, check=True)
        if not os.path.exists(result.stdout.strip()):
            logger.error("Poetry environment not found. Please run 'poetry install' first.")
            return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Poetry is not installed or not in the system's PATH. Please run 'poetry install'.")
        return False

    if args.update_deps:
        logger.info("Updating dependencies with poetry...")
        try:
            subprocess.run(["poetry", "install"], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("Failed to update dependencies with poetry. Please run 'poetry install' manually.")
            return False

    if not args.no_download_nltk:
        if not download_nltk_data():
            return False

    logger.info("Checking for Playwright browsers...")
    try:
        subprocess.run(["poetry", "run", "playwright", "install"], check=True, capture_output=True, text=True)
        logger.info("Playwright browsers are installed.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Failed to install Playwright browsers. Please run 'poetry run playwright install' manually. Error: {e.stderr}")
        return False

    return True

def start_backend(args: argparse.Namespace, python_executable: str) -> Optional[subprocess.Popen]:
    """
    Starts the backend FastAPI server.
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
    Starts the Gradio UI server.
    """
    logger.info("Starting Gradio UI...")
    gradio_script_path = ROOT_DIR / "backend" / "python_backend" / "gradio_app.py"
    if not gradio_script_path.exists():
        logger.error(f"Gradio UI script not found at: {gradio_script_path}")
        return None

    cmd = [python_executable, str(gradio_script_path), "--host", args.host]
    if args.gradio_port:
        cmd.extend(["--port", str(args.gradio_port)])
    if args.share:
        cmd.append("--share")
    if args.debug:
        cmd.append("--debug")

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
    Run the application with the specified arguments.
    """
    python_executable = get_python_executable()

    if args.stage == "test":
        logger.info("Running tests...")
        cmd = ["poetry", "run", "pytest"]
        if args.coverage:
            cmd.extend(["--cov=.", "--cov-report=term-missing"])
        result = subprocess.run(cmd)
        return result.returncode

    backend_process = None
    gradio_process = None

    if not args.ui_only:
        backend_process = start_backend(args, python_executable)
        if not backend_process:
            return 1

    if not args.api_only:
        gradio_process = start_gradio_ui(args, python_executable)
        if not gradio_process:
            if backend_process:
                backend_process.terminate()
            return 1

    try:
        if backend_process and gradio_process:
            logger.info("Backend and Gradio UI started. Press Ctrl+C to stop.")
            backend_process.wait()
            gradio_process.wait()
        elif backend_process:
            backend_process.wait()
        elif gradio_process:
            gradio_process.wait()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Shutting down...")
    finally:
        for p in processes:
            if p.poll() is None:
                p.terminate()
    return 0

def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments for the launcher."""
    parser = argparse.ArgumentParser(description="EmailIntelligence Launcher Script")

    # Environment setup arguments
    env_group = parser.add_argument_group("Environment Setup")
    env_group.add_argument("--update-deps", action="store_true", help="Update dependencies before launching")
    env_group.add_argument("--skip-python-version-check", action="store_true", help="Skip Python version check")
    env_group.add_argument("--no-download-nltk", action="store_true", help="Skip downloading NLTK data")
    env_group.add_argument("--skip-prepare", action="store_true", help="Skip all preparation steps")
    env_group.add_argument("--setup", action="store_true", help="Run environment setup only, then exit")

    # Application stage
    stage_group = parser.add_argument_group("Application Stage")
    stage_group.add_argument("--stage", choices=["dev", "test"], default="dev", help="Specify the application mode")

    # Server configuration
    server_group = parser.add_argument_group("Server Configuration")
    server_group.add_argument("--port", type=int, default=8000, help="Port for the backend server")
    server_group.add_argument("--host", type=str, default="127.0.0.1", help="Host for the backend server")
    server_group.add_argument("--listen", action="store_true", help="Listen on 0.0.0.0")
    server_group.add_argument("--gradio-port", type=int, default=None, help="Port for the Gradio UI")
    server_group.add_argument("--api-only", action="store_true", help="Run only the API server")
    server_group.add_argument("--ui-only", action="store_true", help="Run only the Gradio UI")
    server_group.add_argument("--debug", action="store_true", help="Enable debug mode (e.g., --reload for uvicorn)")
    server_group.add_argument("--share", action="store_true", help="Create a public link for the Gradio UI")

    # Testing
    test_group = parser.add_argument_group("Testing")
    test_group.add_argument("--coverage", action="store_true", help="Generate code coverage report")

    # Miscellaneous
    misc_group = parser.add_argument_group("Miscellaneous")
    misc_group.add_argument("--system-info", action="store_true", help="Print system information and exit")
    misc_group.add_argument("--loglevel", type=str, default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging level")

    return parser.parse_args()

def main() -> int:
    """
    Main entry point for the launcher script.
    """
    if os.environ.get("LAUNCHER_REEXEC_GUARD") != "1":
        current_major, current_minor = sys.version_info[:2]
        if not (PYTHON_MIN_VERSION <= (current_major, current_minor) <= PYTHON_MAX_VERSION):
            logger.info("Incompatible Python version. Searching for a compatible one...")
            for py_cmd in [f"python{v[0]}.{v[1]}" for v in [PYTHON_MAX_VERSION, PYTHON_MIN_VERSION]] + ["python3"]:
                if found_path := shutil.which(py_cmd):
                    logger.info(f"Found compatible Python at {found_path}. Re-executing...")
                    os.environ["LAUNCHER_REEXEC_GUARD"] = "1"
                    os.execve(found_path, [found_path, __file__] + sys.argv[1:], os.environ)
            logger.error("Could not find a compatible Python version.")
            return 1

    _setup_signal_handlers()
    args = parse_arguments()

    if not args.skip_prepare:
        if not prepare_environment(args):
            return 1

    python_executable = get_python_executable()
    if sys.executable != python_executable and os.environ.get("VENV_REEXEC_GUARD") != "1":
        logger.info(f"Re-executing with virtual environment python: {python_executable}")
        os.environ["VENV_REEXEC_GUARD"] = "1"
        os.execve(python_executable, [python_executable] + sys.argv, os.environ)

    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        logger.warning("python-dotenv not found. Skipping .env file loading.")

    return run_application(args)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logger.error(f"An unexpected error occurred in main: {e}", exc_info=True)
        sys.exit(1)