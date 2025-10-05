#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

<<<<<<< HEAD
This script provides a single, unified way to set up, manage, and run all
components of the EmailIntelligence application, including the Python backend,
Gradio UI, and Node.js services. It uses 'uv' for Python dependency management
based on pyproject.toml.

Usage:
    python launch.py [arguments]
=======
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
>>>>>>> origin/feature/git-history-analysis-report
"""

import argparse
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
from typing import List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")

# --- Global state ---
processes = []
ROOT_DIR = Path(__file__).resolve().parent

# --- Constants ---
PYTHON_MIN_VERSION = (3, 12)
PYTHON_MAX_VERSION = (3, 12)
VENV_DIR = "venv"


# --- Signal Handling ---
def _handle_sigint(signum, frame):
<<<<<<< HEAD
    logger.info("Received SIGINT/SIGTERM, shutting down all services...")
    for p in processes:
        if p.poll() is None:
=======
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
>>>>>>> origin/feature/git-history-analysis-report
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


<<<<<<< HEAD
# --- Environment & Tooling ---
def get_venv_python_path() -> Path:
    """Get the path to the venv python executable."""
    venv_path = ROOT_DIR / VENV_DIR
    if os.name == "nt":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"


def get_python_executable() -> str:
    """Get the Python executable path, preferring the venv."""
    if (ROOT_DIR / VENV_DIR).exists():
        return str(get_venv_python_path())
    return sys.executable


def run_command(cmd: List[str], description: str, cwd: Optional[Path] = None, shell=False) -> bool:
    """Run a command with verbose logging."""
    logger.info(description)
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd or ROOT_DIR,
            check=True,
=======
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
>>>>>>> origin/feature/git-history-analysis-report
            capture_output=True,
            text=True,
            shell=(os.name == 'nt' and 'npm' in cmd),
        )
        # Always log stdout for visibility, especially for debugging setup steps.
        if proc.stdout:
            logger.info(f"stdout from '{' '.join(cmd)}':\n{proc.stdout}")
        if proc.stderr:
            logger.warning(f"stderr from '{' '.join(cmd)}':\n{proc.stderr}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed: {description}")
        logger.error(f"stdout:\n{e.stdout}")
        logger.error(f"stderr:\n{e.stderr}")
        return False


<<<<<<< HEAD
# --- Python Environment Management ---
def create_venv() -> bool:
    """Create a Python virtual environment."""
    if (ROOT_DIR / VENV_DIR).exists():
        logger.info("Virtual environment already exists.")
        return True
    logger.info(f"Creating virtual environment at '{ROOT_DIR / VENV_DIR}'...")
    return run_command(
        [sys.executable, "-m", "venv", VENV_DIR],
        "Creating Python virtual environment",
    )


def install_uv_in_venv(python_executable: str) -> bool:
    """Install or upgrade 'uv' in the virtual environment."""
    return run_command(
        [python_executable, "-m", "pip", "install", "-U", "uv"],
        "Installing/updating 'uv' in venv",
    )


def install_python_dependencies(python_executable: str, args: argparse.Namespace) -> bool:
    """Install Python dependencies using uv from pyproject.toml."""
    if not install_uv_in_venv(python_executable):
=======
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
>>>>>>> origin/feature/git-history-analysis-report
        return False

    # Use --active to ensure uv respects the created venv, not a default .venv
    cmd = [python_executable, "-m", "uv", "sync", "--active"]
    desc = "Syncing Python dependencies from pyproject.toml"

<<<<<<< HEAD
    if args.stage in ["dev", "test"]:
        cmd.append("--all-extras")
        desc += " (with dev extras)"
    if args.update_deps:
        cmd.append("--reinstall")
        desc += " (force reinstall)"

    return run_command(cmd, desc)
=======
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
>>>>>>> origin/feature/git-history-analysis-report


def download_nltk_data(python_executable: str) -> bool:
    """Download required NLTK data."""
    nltk_script = (
        "import nltk; "
        "[nltk.download(d, quiet=True) for d in ['punkt', 'stopwords', 'wordnet', 'vader_lexicon', 'averaged_perceptron_tagger', 'brown']]"
    )
    return run_command(
        [python_executable, "-c", nltk_script], "Downloading NLTK data"
    )


# --- Node.js Environment Management ---
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
    desc = f"{'Updating' if update else 'Installing'} Node.js dependencies for '{directory}/'"
    return run_command(cmd, desc, cwd=ROOT_DIR / directory, shell=(os.name == "nt"))


# --- Service Management ---
def start_service(
    cmd: List[str], log_name: str, cwd: Optional[Path] = None
) -> Optional[subprocess.Popen]:
    """Start a subprocess and add it to the global list."""
    logger.info(f"Starting {log_name}...")
    try:
        # Use shell=True only when necessary (e.g., for npm on Windows)
        is_windows_npm = "npm" in cmd and os.name == "nt"
        p = subprocess.Popen(cmd, cwd=cwd or ROOT_DIR, shell=is_windows_npm)
        processes.append(p)
        logger.info(f"{log_name} started with PID {p.pid}.")
        return p
    except Exception as e:
        logger.error(f"Failed to start {log_name}: {e}")
        return None


# --- Main Application Logic ---
def prepare_environment(args: argparse.Namespace) -> bool:
    """Prepare the full application environment."""
    # 0. Clean venv if requested
    if not args.no_venv and args.force_recreate_venv:
        venv_path = ROOT_DIR / VENV_DIR
        if venv_path.exists():
            logger.info(f"Force-recreating venv: Deleting existing directory at '{venv_path}'...")
            try:
                shutil.rmtree(venv_path)
            except OSError as e:
                logger.error(f"Failed to delete venv: {e}. Please remove it manually.")
                return False

    # 1. Setup Python venv and dependencies
    if not args.no_venv:
        if not create_venv():
            return False
        python_executable = str(get_venv_python_path())
        if not install_python_dependencies(python_executable, args):
            return False
        # Download NLTK data immediately after Python deps are installed
        if not args.no_download_nltk:
            if not download_nltk_data(python_executable):
                return False
    else:
        python_executable = sys.executable
        # If not using venv, still need to handle NLTK download
        if not args.no_download_nltk:
            logger.warning("Running NLTK download with system python. This may fail if nltk is not installed globally.")
            if not download_nltk_data(python_executable):
                return False

    # 2. Install Node.js dependencies
    if not args.no_client:
        if not install_nodejs_dependencies("client", args.update_deps):
            return False

    return True


<<<<<<< HEAD
=======
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


>>>>>>> origin/feature/git-history-analysis-report
def run_application(args: argparse.Namespace) -> int:
    """Run the selected application components."""
    python_executable = get_python_executable()
    services_started = []

<<<<<<< HEAD
    # Start Python Backend (FastAPI)
    if not args.no_backend:
        actual_host = "0.0.0.0" if args.listen else args.host
        cmd = [
            python_executable, "-m", "uvicorn", "backend.python_backend.main:app",
            "--host", actual_host, "--port", str(args.port),
        ]
        if args.debug:
            cmd.append("--reload")
        services_started.append(start_service(cmd, "Python Backend"))

    # Start Gradio UI
    if not args.no_ui:
        cmd = [python_executable, "backend/python_backend/gradio_app.py", "--host", args.host]
        if args.gradio_port:
            cmd.extend(["--port", str(args.gradio_port)])
        if args.share:
            cmd.append("--share")
        services_started.append(start_service(cmd, "Gradio UI"))

    # Start Node.js Frontend (Vite)
    if not args.no_client:
        services_started.append(
            start_service(["npm", "run", "dev"], "Node.js Frontend", cwd=ROOT_DIR / "client")
        )

    if not any(services_started):
        logger.error("No services were selected to run. Use --help to see options.")
        return 1

    logger.info("All selected services started. Press Ctrl+C to stop.")
    try:
        while True:
            for p in processes:
                if p.poll() is not None:
                    logger.error(f"Service with PID {p.pid} exited unexpectedly.")
                    return 1
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received in main loop. Shutting down.")
    finally:
        _handle_sigint(None, None)
=======
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
>>>>>>> origin/feature/git-history-analysis-report

    return 0


<<<<<<< HEAD
def find_compatible_python_interpreter() -> Optional[str]:
    """Find a compatible Python interpreter on the system."""
    logger.info(f"Searching for a Python {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}+ interpreter...")
    candidates = ["python3.12", "python3", "python"]
    for candidate in candidates:
        path = shutil.which(candidate)
        if path:
            try:
                result = subprocess.run(
                    [path, "--version"], capture_output=True, text=True, check=True
                )
                version_str = result.stdout.strip().split(" ")[1]
                version_tuple = tuple(map(int, version_str.split(".")[:2]))
                if PYTHON_MIN_VERSION <= version_tuple <= PYTHON_MAX_VERSION:
                    logger.info(f"Found compatible interpreter: {path} (version {version_str})")
                    return path
            except Exception as e:
                logger.debug(f"Could not use interpreter '{path}': {e}")
    return None


def re_execute_with_compatible_python(interpreter_path: str):
    """Re-execute the launcher with a different Python interpreter."""
    logger.info(f"Re-executing launcher with: {interpreter_path}")
    os.environ["LAUNCHER_REEXEC_GUARD"] = "1"
    os.execv(interpreter_path, [interpreter_path, *sys.argv])


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="EmailIntelligence Unified Launcher",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # --- Setup Arguments ---
    setup = parser.add_argument_group("Setup Arguments")
    setup.add_argument("--setup", action="store_true", help="Run environment setup and exit.")
    setup.add_argument("--update-deps", action="store_true", help="Update all dependencies.")
    setup.add_argument("--no-venv", action="store_true", help="Do not create or use a Python venv.")
    setup.add_argument("--force-recreate-venv", action="store_true", help="Delete and recreate the venv before setup.")
    setup.add_argument("--no-download-nltk", action="store_true", help="Skip downloading NLTK data.")

    # --- Service Selection ---
    selection = parser.add_argument_group("Service Selection")
    selection.add_argument("--no-backend", action="store_true", help="Do not start the Python backend.")
    selection.add_argument("--no-ui", action="store_true", help="Do not start the Gradio UI.")
    selection.add_argument("--no-client", action="store_true", help="Do not start the Node.js frontend.")

    # --- Configuration ---
    config = parser.add_argument_group("Configuration")
    config.add_argument("--stage", choices=["dev", "test"], default="dev", help="Application stage.")
    config.add_argument("--port", type=int, default=8000, help="Port for the Python backend.")
    config.add_argument("--gradio-port", type=int, help="Port for the Gradio UI (defaults to 7860).")
    config.add_argument("--host", default="127.0.0.1", help="Host address for servers.")
    config.add_argument("--listen", action="store_true", help="Listen on 0.0.0.0 (overrides --host).")
    config.add_argument("--share", action="store_true", help="Create a public Gradio sharing link.")
    config.add_argument("--debug", action="store_true", help="Enable debug/reload mode for services.")
    config.add_argument("--env-file", help="Path to a custom .env file to load.")

=======
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
>>>>>>> origin/feature/git-history-analysis-report
    return parser.parse_args()


def main() -> int:
<<<<<<< HEAD
    """Main entry point."""
    # Ensure launcher is running with a compatible Python
    if os.environ.get("LAUNCHER_REEXEC_GUARD") != "1":
        current_version = sys.version_info[:2]
        if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
            interpreter = find_compatible_python_interpreter()
            if interpreter:
                re_execute_with_compatible_python(interpreter)
            else:
                logger.error(f"Python {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]} is required but not found.")
                return 1
=======
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
>>>>>>> origin/feature/git-history-analysis-report

    _setup_signal_handlers()
    args = parse_arguments()

    if args.env_file:
        try:
            from dotenv import load_dotenv
            if Path(args.env_file).exists():
                logger.info(f"Loading environment variables from {args.env_file}")
                load_dotenv(dotenv_path=args.env_file, override=True)
            else:
                logger.warning(f"Specified --env-file '{args.env_file}' not found.")
        except ImportError:
            logger.warning("python-dotenv not installed, cannot load .env file. Skipping.")

<<<<<<< HEAD
    if not prepare_environment(args):
        logger.error("Environment setup failed. Aborting.")
=======
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
>>>>>>> origin/feature/git-history-analysis-report
        return 1

    if args.setup:
        logger.info("Environment setup complete. Exiting as requested by --setup flag.")
        return 0

    return run_application(args)


if __name__ == "__main__":
    sys.exit(main())