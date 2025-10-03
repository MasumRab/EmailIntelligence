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


class VenvStatus(Enum):
    """Represents the status of the virtual environment."""
    OK = auto()
    MISSING = auto()
    CORRUPTED = auto()
    INCOMPATIBLE = auto()


def _get_venv_status() -> Tuple[VenvStatus, Optional[str]]:
    """Checks the status of the virtual environment."""
    if not is_venv_available():
        return VenvStatus.MISSING, None

    venv_python_exe_path = ""
    if os.name == "nt":
        venv_python_exe_path = str(ROOT_DIR / VENV_DIR / "Scripts" / "python.exe")
    else:
        venv_python_exe_path = str(ROOT_DIR / VENV_DIR / "bin" / "python")

    if not Path(venv_python_exe_path).exists():
        return VenvStatus.CORRUPTED, None

    try:
        result = subprocess.run(
            [venv_python_exe_path, "--version"],
            capture_output=True, text=True, check=False, timeout=5
        )
        version_output = result.stdout.strip() + result.stderr.strip()
        if version_output.startswith("Python "):
            parts = version_output.split(" ")[1].split(".")
            if len(parts) >= 2:
                venv_major, venv_minor = int(parts[0]), int(parts[1])
                venv_version = (venv_major, venv_minor)
                if not (PYTHON_MIN_VERSION <= venv_version <= PYTHON_MAX_VERSION):
                    return VenvStatus.INCOMPATIBLE, venv_python_exe_path
                return VenvStatus.OK, venv_python_exe_path
    except (subprocess.TimeoutExpired, ValueError, IndexError) as e:
        logger.warning(f"Could not determine venv Python version: {e}")

    return VenvStatus.CORRUPTED, None


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


# Original functions are now fully replaced.
# The aliasing and del operations for _standalone versions are no longer needed.


def check_torch_cuda() -> bool:
    """Check if PyTorch with CUDA is available."""
    python = get_python_executable()

    try:
        result = subprocess.run(
            [python, "-c", "import torch; print(torch.cuda.is_available())"],
            capture_output=True,
            text=True,
            check=True,
        )
        is_available = result.stdout.strip() == "True"
        logger.info(f"PyTorch CUDA is {'available' if is_available else 'not available'}")
        return is_available
    except subprocess.CalledProcessError:
        logger.warning("Failed to check PyTorch CUDA availability")
        return False


def reinstall_torch() -> bool:
    """Reinstall PyTorch with CUDA support."""
    python = get_python_executable()

    # Uninstall existing PyTorch
    logger.info("Uninstalling existing PyTorch...")
    subprocess.run([python, "-m", "pip", "uninstall", "-y", "torch", "torchvision", "torchaudio"])

    # Install PyTorch with CUDA support
    logger.info("Installing PyTorch with CUDA support...")
    cmd = [
        python,
        "-m",
        "pip",
        "install",
        "torch",
        "torchvision",
        "torchaudio",
        "--index-url",
        "https://download.pytorch.org/whl/cu118",
    ]

    try:
        subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to reinstall PyTorch: {e}")
        return False


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


def _recreate_venv() -> bool:
    """Deletes and recreates the virtual environment. Returns True on success."""
    logger.info(f"Deleting and recreating virtual environment at './{VENV_DIR}'.")
    try:
        shutil.rmtree(ROOT_DIR / VENV_DIR)
        logger.info(f"Successfully deleted existing virtual environment './{VENV_DIR}'.")
    except OSError as e:
        logger.error(f"Failed to delete virtual environment './{VENV_DIR}': {e}. Please delete it manually and restart.")
        return False

    if not create_venv():
        logger.error("Failed to recreate virtual environment. Exiting.")
        return False
    return True


def prepare_environment(args: argparse.Namespace) -> bool:
    """Prepare the environment for running the application."""
    if not args.skip_python_version_check and not check_python_version():
        return False

    if args.no_venv:
        if not args.no_download_nltk and not download_nltk_data():
            return False
        return True

    venv_needs_initial_setup = False
    status, _ = _get_venv_status()

    if status == VenvStatus.MISSING:
        logger.info(f"Virtual environment not found at './{VENV_DIR}'. Creating...")
        if not create_venv():
            return False
        venv_needs_initial_setup = True
    elif status in (VenvStatus.CORRUPTED, VenvStatus.INCOMPATIBLE):
        issue = "corrupted" if status == VenvStatus.CORRUPTED else "incompatible"
        logger.warning(f"The existing virtual environment at './{VENV_DIR}' is {issue}.")

        response = ""
        if args.force_recreate_venv or os.environ.get("CI"):
            response = "yes"
            logger.warning(f"CI environment or --force-recreate-venv flag detected, automatically recreating {issue} venv.")
        else:
            try:
                prompt_message = (
                    f"Do you want to delete and recreate the {issue} virtual environment? (yes/no): "
                )
                response = input(prompt_message).strip().lower()
            except EOFError:
                response = "no"
                logger.warning("Non-interactive session, defaulting to not recreating venv.")

        if response == "yes":
            if not _recreate_venv():
                return False
            venv_needs_initial_setup = True
        else:
            logger.warning(f"Proceeding with the existing, potentially {issue} virtual environment.")

    # Install/update dependencies
    if venv_needs_initial_setup or args.update_deps:
        primary_req_file = _get_primary_requirements_file()
        update_flag = args.update_deps and not venv_needs_initial_setup

        logger.info(f"{'Updating' if update_flag else 'Installing'} base dependencies from {primary_req_file}...")
        if not install_dependencies(primary_req_file, update=update_flag):
            return False

        stage_req_file = f"requirements-{args.stage}.txt"
        if (ROOT_DIR / stage_req_file).exists():
            logger.info(f"{'Updating' if update_flag else 'Installing'} stage-specific dependencies from {stage_req_file}...")
            if not install_dependencies(stage_req_file, update=update_flag):
                return False
    else:
        logger.info("Virtual environment is OK. Skipping dependency installation unless --update-deps is used.")

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

    gradio_script_path = ROOT_DIR / "backend" / "python_backend" / "gradio_app.py"
    if not gradio_script_path.exists():
        logger.error(f"Gradio UI script not found at: {gradio_script_path}")
        return None

    cmd = [
        python_executable,
        str(gradio_script_path),
        "--host",
        args.host,
    ]

    # Add port if specified, Gradio has its own default port (7860)
    if args.gradio_port:
        cmd.extend(["--port", str(args.gradio_port)])
    if hasattr(args, 'debug') and args.debug:
        cmd.append("--debug")
    if hasattr(args, 'share') and args.share:
        cmd.append("--share")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)

    try:
        logger.info(f"Running Gradio UI command: {' '.join(cmd)}")
        process = subprocess.Popen(cmd, env=env)
        processes.append(process)
        logger.info(f"Gradio UI started with PID {process.pid}.")
        return process
    except Exception as e:
        logger.error(f"Failed to start Gradio UI: {e}")
        return None


def run_application(args: argparse.Namespace) -> int:
    """Run the application with the specified arguments."""
    from dotenv import load_dotenv
    python_executable = get_python_executable()
    backend_process = None
    gradio_process = None

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
        else:
            logger.error("Failed to start backend server in API only mode.")
            return 1
    elif args.frontend_only:
        logger.info("Running in Frontend only mode.")
        if not args.api_url:
            logger.warning(
                "Frontend only mode: VITE_API_URL might not be correctly set if backend is not running or --api-url is not provided."
            )
        frontend_process = start_frontend(args)
        if frontend_process:
            frontend_process.wait()
        else:
            logger.error("Failed to start Gradio UI in UI only mode.")
            return 1
    elif args.stage == "dev" or not args.stage:
        logger.info("Running in local development mode (backend and frontend).")
        unexpected_exit = False
        backend_process = start_backend(args, python_executable)
        gradio_process = start_gradio_ui(args, python_executable)

        if backend_process:
            logger.info(f"Backend accessible at http://{args.host}:{args.port}")
        else:
            logger.error("Backend server failed to start.")
            if frontend_process and frontend_process.poll() is None:
                frontend_process.terminate()
            return 1

    if not backend_process or not gradio_process:
        logger.error("Failed to start one or more application components.")
        return 1

        if backend_process and gradio_process:
            logger.info("Backend and Gradio UI started. Press Ctrl+C to stop.")
            try:
                while True:
                    if backend_process.poll() is not None:
                        logger.error(f"Backend process {backend_process.pid} exited unexpectedly.")
                        unexpected_exit = True
                        if gradio_process.poll() is None:
                            logger.info(f"Terminating Gradio UI process {gradio_process.pid}...")
                            gradio_process.terminate()
                        break
                    if gradio_process.poll() is not None:
                        logger.error(f"Gradio UI process {gradio_process.pid} exited unexpectedly.")
                        unexpected_exit = True
                        if backend_process.poll() is None:
                            logger.info(f"Terminating backend process {backend_process.pid}...")
                            backend_process.terminate()
                        break
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info(
                    "KeyboardInterrupt in run_application. Signal handler should take over."
                )
                pass
            except Exception as e:
                logger.error(f"An unexpected error occurred in run_application main loop: {e}")
            finally:
                for p in [backend_process, frontend_process]:
                    if p and p.poll() is None:
                        p.terminate()
                        try:
                            p.wait(timeout=1)
                        except subprocess.TimeoutExpired:
                            p.kill()
            if unexpected_exit:
                logger.error("One or more services exited unexpectedly.")
                return 1

        elif backend_process:
            logger.info("Only backend process is running. Waiting for it to complete.")
            backend_process.wait()
            if backend_process.returncode != 0:
                logger.error(f"Backend process exited with code: {backend_process.returncode}")
                return 1

    elif args.stage == "test":
        logger.info("Running application in 'test' stage (executing tests)...")
        logger.info(
            f"Executing default test suite for '--stage {args.stage}'. Specific test flags (e.g., --unit, --integration) were not provided."
        )
        from deployment.test_stages import test_stages

        test_run_success = True

        if hasattr(test_stages, "run_unit_tests"):
            logger.info("Running unit tests (default for --stage test)...")
            if not test_stages.run_unit_tests(args.coverage, args.debug):
                test_run_success = False
                logger.error("Unit tests failed.")
        else:
            logger.warning("test_stages.run_unit_tests not found, cannot run unit tests.")

        if hasattr(test_stages, "run_integration_tests"):
            logger.info("Running integration tests (default for --stage test)...")
            if not test_stages.run_integration_tests(args.coverage, args.debug):
                test_run_success = False
                logger.error("Integration tests failed.")
        else:
            logger.warning(
                "test_stages.run_integration_tests not found, cannot run integration tests."
            )

        logger.info(f"Default test suite execution finished. Success: {test_run_success}")
        return 0 if test_run_success else 1

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

    # Environment setup arguments
    parser.add_argument(
        "--no-venv",
        action="store_true",
        help="Don't create or use a virtual environment",
    )
    parser.add_argument(
        "--update-deps",
        action="store_true",
        help="Update dependencies before launching",
    )
    parser.add_argument(
        "--skip-python-version-check",
        action="store_true",
        help="Skip Python version check",
    )
    parser.add_argument(
        "--force-recreate-venv",
        action="store_true",
        help="Force deletion and recreation of the virtual environment if it's corrupted or incompatible.",
    )
    parser.add_argument(
        "--no-download-nltk", action="store_true", help="Skip downloading NLTK data"
    )
    parser.add_argument("--skip-prepare", action="store_true", help="Skip preparation steps")

    # Application stage
    parser.add_argument(
        "--stage",
        choices=["dev", "test"],
        default="dev",
        help="Specify the application mode ('dev' for running, 'test' for running tests).",
    )

    # Server configuration
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Specify the port to run on (default: 8000)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Specify the host to run on (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--gradio-port",
        type=int,
        default=None,
        help="Specify the port for the Gradio UI (default: 7860 or next available)",
    )
    parser.add_argument("--api-url", type=str, help="Specify the API URL for the frontend")
    parser.add_argument(
        "--api-only",
        action="store_true",
        help="Run only the API server without the Gradio UI",
    )
    parser.add_argument(
        "--ui-only",
        action="store_true",
        help="Run only the Gradio UI without the API server",
    )
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

    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {args.loglevel}")

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        force=True,
    )
    logger.setLevel(numeric_level)
    logger.info(f"Launcher log level set to: {args.loglevel}")

    default_env_file = ROOT_DIR / ".env"
    if default_env_file.exists():
        logger.info(f"Loading environment variables from default .env file: {default_env_file}")
        load_dotenv(dotenv_path=default_env_file, override=True)

    if args.system_info:
        _print_system_info()
        return 0

    if not prepare_environment(args):
        return 1

    from dotenv import load_dotenv
    default_env_file = ROOT_DIR / ".env"
    if default_env_file.exists():
        logger.info(f"Loading environment variables from default .env file: {default_env_file}")
        load_dotenv(dotenv_path=default_env_file, override=True)

    if args.setup:
        logger.info("Environment setup complete. Exiting as requested by --setup flag.")
        return 0

    return run_application(args)


if __name__ == "__main__":
    sys.exit(main())