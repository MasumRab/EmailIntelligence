#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

This script provides a single, unified way to set up, manage, and run all
components of the EmailIntelligence application, including the Python backend,
Gradio UI, and Node.js services. It uses 'uv' for Python dependency management
based on pyproject.toml.

Usage:
    python launch.py [arguments]
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
    """
    Handles SIGINT and SIGTERM signals for graceful shutdown.

    Terminates all child processes tracked in the global `processes` list.

    Args:
        signum: The signal number.
        frame: The current stack frame.
    """
    logger.info("Received SIGINT/SIGTERM, shutting down...")
    for p in processes:
        if p.poll() is None:
            logger.info(f"Terminating process {p.pid}...")
            p.terminate()
            try:
                p.wait(timeout=5)  # Wait up to 5 seconds for graceful shutdown
            except subprocess.TimeoutExpired:
                logger.warning(f"Process {p.pid} did not terminate gracefully, killing it...")
                p.kill()
    logger.info("All services shut down.")
    sys.exit(0)


# Setup signal handlers
signal.signal(signal.SIGINT, _handle_sigint)
signal.signal(signal.SIGTERM, _handle_sigint)


def check_python_version():
    """Check if the current Python version is compatible."""
    current_version = sys.version_info[:2]
    if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
        logger.error(
            f"Python version {current_version} is not compatible. "
            f"Required: >={'.'.join(map(str, PYTHON_MIN_VERSION))}, "
            f"<={'.'.join(map(str, PYTHON_MAX_VERSION))}"
        )
<<<<<<< HEAD
        sys.exit(1)
    logger.info(f"Python version {sys.version} is compatible.")


def create_venv(venv_path: Path, recreate: bool = False):
    """Create or recreate the virtual environment."""
    if venv_path.exists() and recreate:
        logger.info(f"Removing existing virtual environment at {venv_path}")
        shutil.rmtree(venv_path)
=======
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
        return False

    # Use --active to ensure uv respects the created venv, not a default .venv
    cmd = [python_executable, "-m", "uv", "sync", "--active"]
    desc = "Syncing Python dependencies from pyproject.toml"

    if args.stage in ["dev", "test"]:
        cmd.append("--all-extras")
        desc += " (with dev extras)"
    if args.update_deps:
        cmd.append("--reinstall")
        desc += " (force reinstall)"

    return run_command(cmd, desc)


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
<<<<<<< HEAD
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
=======
            venv_needs_initial_setup = True

        if venv_needs_initial_setup:
            primary_req_file = _get_primary_requirements_file()
            logger.info(
                f"Installing base dependencies from {Path(primary_req_file).name} into {'new' if not venv_recreated_this_run else 'recreated'} venv..."
            )
            if not install_dependencies(primary_req_file, update=False):
                logger.error(
                    f"Failed to install base dependencies from {Path(primary_req_file).name}. Exiting."
                )
                return False
        elif args.update_deps:
            primary_req_file = _get_primary_requirements_file()
            logger.info(
                f"Updating base dependencies from {Path(primary_req_file).name} in existing venv as per --update-deps..."
            )
            if not install_dependencies(primary_req_file, update=True):
                logger.error(
                    f"Failed to update base dependencies from {Path(primary_req_file).name}. Exiting."
                )
                return False
        else:
            chosen_req_file = _get_primary_requirements_file()
            logger.info(
                f"Compatible virtual environment found (or user chose to proceed with existing). Primary requirements file: {Path(chosen_req_file).name}. Skipping base dependency installation unless --update-deps is used."
            )

        stage_requirements_file_path_str = None
        if args.stage == "dev":
            dev_req_path_obj = ROOT_DIR / "requirements-dev.txt"
            if dev_req_path_obj.exists():
                stage_requirements_file_path_str = "requirements-dev.txt"
        elif args.stage == "test":
            test_req_path_obj = ROOT_DIR / "requirements-test.txt"
            if test_req_path_obj.exists():
                stage_requirements_file_path_str = "requirements-test.txt"

        if stage_requirements_file_path_str:
            install_stage_deps_update_flag = args.update_deps
            if venv_needs_initial_setup:
                install_stage_deps_update_flag = False
                logger.info(
                    f"Installing stage-specific requirements for '{args.stage}' from {Path(stage_requirements_file_path_str).name} into {'new' if not venv_recreated_this_run else 'recreated'} venv..."
                )
            elif args.update_deps:
                logger.info(
                    f"Updating stage-specific requirements for '{args.stage}' from {Path(stage_requirements_file_path_str).name} as per --update-deps..."
                )
            else:
                logger.info(
                    f"Skipping stage-specific requirements for '{args.stage}' from {Path(stage_requirements_file_path_str).name} unless missing or --update-deps is used."
                )

            if venv_needs_initial_setup or args.update_deps:
                if not install_dependencies(
                    stage_requirements_file_path_str,
                    update=install_stage_deps_update_flag,
                ):
                    logger.error(
                        f"Failed to install/update stage-specific dependencies from {Path(stage_requirements_file_path_str).name}. Exiting."
                    )
                    return False

    if not args.no_download_nltk:
        if not download_nltk_data():
>>>>>>> origin/main
            return False

    return True


<<<<<<< HEAD
=======
def start_backend(args: argparse.Namespace, python_executable: str) -> Optional[subprocess.Popen]:
    """Starts the backend server."""
    actual_host = "0.0.0.0" if args.listen else args.host
    logger.info(f"Starting backend server on {actual_host}:{args.port}...")

    cmd = [
        python_executable,
        "-m",
        "uvicorn",
        "backend.python_backend.main:app",
        "--host",
        actual_host,
        "--port",
        str(args.port),
    ]

    if args.debug:
        cmd.append("--log-level=debug")
        cmd.append("--reload")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)
    env["NODE_ENV"] = "development" if args.stage == "dev" else args.stage
    env["DEBUG"] = str(args.debug)

    try:
        log_cmd = cmd[:]
        if args.listen:
            log_cmd[log_cmd.index(actual_host)] = f"{args.host} (via --listen on 0.0.0.0)"
        logger.info(f"Running backend command: {' '.join(log_cmd)}")
        process = subprocess.Popen(cmd, env=env)
        processes.append(process)
        logger.info(f"Backend server started with PID {process.pid} on {actual_host}:{args.port}.")
        return process
    except FileNotFoundError:
        logger.error(
            f"Error: Python executable not found at {python_executable} or uvicorn not installed in the venv."
        )
        logger.error(
            "Please ensure your virtual environment is active and has 'uvicorn' and other backend dependencies installed."
        )
        return None
    except Exception as e:
        logger.error(f"Failed to start backend server: {e}")
        return None


def start_gradio_ui(args: argparse.Namespace, python_executable: str) -> Optional[subprocess.Popen]:
    """Starts the Gradio UI server."""
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

    if args.debug:
        cmd.append("--debug")

    if args.share:
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


>>>>>>> origin/main
def run_application(args: argparse.Namespace) -> int:
    """Run the selected application components."""
    python_executable = get_python_executable()
    services_started = []
>>>>>>> origin/feat/modular-ai-platform

    if not venv_path.exists():
        logger.info(f"Creating virtual environment at {venv_path}")
        venv.create(venv_path, with_pip=True)
    else:
        logger.info(f"Virtual environment already exists at {venv_path}")

<<<<<<< HEAD
=======
<<<<<<< HEAD
    # Start Gradio UI
    if not args.no_ui:
        cmd = [python_executable, "backend/python_backend/gradio_app.py", "--host", args.host]
        if args.gradio_port:
            cmd.extend(["--port", str(args.gradio_port)])
        if args.share:
            cmd.append("--share")
        services_started.append(start_service(cmd, "Gradio UI"))
=======
    if args.api_only:
        logger.info("Running in API only mode.")
        backend_process = start_backend(args, python_executable)
        if backend_process:
            backend_process.wait()
        else:
            logger.error("Failed to start backend server in API only mode.")
            return 1
    elif args.ui_only:
        logger.info("Running in UI only mode.")
        gradio_process = start_gradio_ui(args, python_executable)
        if gradio_process:
            gradio_process.wait()
        else:
            logger.error("Failed to start Gradio UI in UI only mode.")
            return 1
    elif args.stage == "dev" or not args.stage:
        logger.info("Running in local development mode (backend and Gradio UI).")
        unexpected_exit = False
        backend_process = start_backend(args, python_executable)
        gradio_process = start_gradio_ui(args, python_executable)
>>>>>>> origin/main
>>>>>>> origin/feat/modular-ai-platform

def install_uv(venv_path: Path):
    """Install uv package manager in the virtual environment."""
    venv_python = venv_path / "Scripts" / "python.exe" if platform.system() == "Windows" else venv_path / "bin" / "python"
    if not venv_python.exists():
        logger.error(f"Python executable not found at {venv_python}")
        sys.exit(1)

    logger.info("Installing uv package manager...")
    result = subprocess.run(
        [str(venv_python), "-m", "pip", "install", "uv"],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        logger.error(f"Failed to install uv: {result.stderr}")
        sys.exit(1)
    logger.info("uv installed successfully.")


def setup_dependencies(venv_path: Path, update: bool = False):
    """Install project dependencies using uv."""
    venv_python = venv_path / "Scripts" / "python.exe" if platform.system() == "Windows" else venv_path / "bin" / "python"
    venv_uv = venv_path / "Scripts" / "uv.exe" if platform.system() == "Windows" else venv_path / "bin" / "uv"

    cmd = [str(venv_uv), "sync"]
    if update:
        cmd.extend(["--upgrade"])
    
    logger.info("Installing project dependencies...")
    result = subprocess.run(
        cmd,
        cwd=ROOT_DIR,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        logger.error(f"Failed to install dependencies: {result.stderr}")
        sys.exit(1)
    logger.info("Dependencies installed successfully.")


def download_nltk_data(venv_path: Path):
    """Download required NLTK data."""
    venv_python = venv_path / "Scripts" / "python.exe" if platform.system() == "Windows" else venv_path / "bin" / "python"

    nltk_download_script = """
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
print("NLTK data download completed.")
"""

    logger.info("Downloading NLTK data...")
    result = subprocess.run(
        [str(venv_python), "-c", nltk_download_script],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        logger.error(f"Failed to download NLTK data: {result.stderr}")
        # This might fail in some environments but it's not critical for basic operation
        logger.warning("NLTK data download failed, but continuing setup...")
    else:
        logger.info("NLTK data downloaded successfully.")


def start_backend(venv_path: Path, host: str, port: int, debug: bool = False):
    """Start the Python FastAPI backend."""
    venv_python = venv_path / "Scripts" / "python.exe" if platform.system() == "Windows" else venv_path / "bin" / "python"
    backend_path = ROOT_DIR / "backend" / "python_backend" / "main.py"

    cmd = [str(venv_python), str(backend_path)]
    if debug:
        cmd.extend(["--reload", "--host", host, "--port", str(port)])
    else:
        # For production, we might want to use uvicorn directly
        cmd = [str(venv_python), "-m", "uvicorn", "backend.python_backend.main:app", "--host", host, "--port", str(port)]

    logger.info(f"Starting Python backend on {host}:{port}")
    process = subprocess.Popen(cmd, cwd=ROOT_DIR)
    processes.append(process)
    return process


def start_gradio_ui(venv_path: Path, host: str, port: Optional[int] = None, debug: bool = False, share: bool = False):
    """Start the Gradio UI."""
    venv_python = venv_path / "Scripts" / "python.exe" if platform.system() == "Windows" else venv_path / "bin" / "python"
    gradio_path = ROOT_DIR / "backend" / "python_backend" / "gradio_app.py"

    cmd = [str(venv_python), str(gradio_path)]
    if share:
        cmd.append("--share")  # Enable public sharing
    if port:
        # Gradio doesn't take port as a command line param directly, 
        # we'd need to modify the app to accept it
        logger.info(f"Starting Gradio UI (on default or next available port)")
    else:
        logger.info("Starting Gradio UI on default port")

    process = subprocess.Popen(cmd, cwd=ROOT_DIR)
    processes.append(process)
    return process


def start_client():
    """Start the Node.js frontend."""
    logger.info("Starting Node.js frontend...")
    # Check if npm is available
    if not shutil.which("npm"):
        logger.error("npm is not available in PATH. Please install Node.js.")
        sys.exit(1)

    # Install Node.js dependencies if node_modules doesn't exist
    node_modules_path = ROOT_DIR / "client" / "node_modules"
    if not node_modules_path.exists():
        logger.info("Installing Node.js dependencies...")
        result = subprocess.run(
            ["npm", "install"],
            cwd=ROOT_DIR / "client",
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"Failed to install Node.js dependencies: {result.stderr}")
            sys.exit(1)
        logger.info("Node.js dependencies installed.")

    # Start the React frontend
    process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=ROOT_DIR / "client"
    )
    processes.append(process)
    return process


def start_server_ts():
    """Start the TypeScript backend server."""
    logger.info("Starting TypeScript backend server...")
    # Check if npm is available
    if not shutil.which("npm"):
        logger.error("npm is not available in PATH. Please install Node.js.")
        sys.exit(1)

    # Install Node.js dependencies if node_modules doesn't exist
    node_modules_path = ROOT_DIR / "server" / "node_modules"
    if not node_modules_path.exists():
        logger.info("Installing TypeScript server dependencies...")
        result = subprocess.run(
            ["npm", "install"],
            cwd=ROOT_DIR / "server",
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"Failed to install TypeScript server dependencies: {result.stderr}")
            sys.exit(1)
        logger.info("TypeScript server dependencies installed.")

    # Start the TypeScript backend
    process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=ROOT_DIR / "server"
    )
    processes.append(process)
    return process


def wait_for_processes():
    """Wait for all processes to complete."""
    try:
        while True:
            time.sleep(1)
            # Check if any process has terminated unexpectedly
            for i, process in enumerate(processes[:]):
                if process.poll() is not None:
                    logger.warning(f"Process {process.pid} terminated with code {process.returncode}")
                    processes.remove(process)
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
        _handle_sigint(None, None)


def main():
    parser = argparse.ArgumentParser(description="EmailIntelligence Unified Launcher")
    
    # Setup arguments
    parser.add_argument("--setup", action="store_true", help="Run environment setup and exit.")
    parser.add_argument("--update-deps", action="store_true", help="Update all dependencies.")
    parser.add_argument("--no-venv", action="store_true", help="Do not create or use a Python venv.")
    parser.add_argument("--force-recreate-venv", action="store_true", help="Delete and recreate the venv before setup.")
    parser.add_argument("--no-download-nltk", action="store_true", help="Skip downloading NLTK data.")
    
    # Service selection
    parser.add_argument("--no-backend", action="store_true", help="Do not start the Python backend.")
    parser.add_argument("--no-ui", action="store_true", help="Do not start the Gradio UI.")
    parser.add_argument("--no-client", action="store_true", help="Do not start the Node.js frontend.")
    
    # Configuration
    parser.add_argument("--stage", choices=["dev", "test"], default="dev", help="Application stage.")
    parser.add_argument("--port", type=int, default=8000, help="Port for the Python backend.")
    parser.add_argument("--gradio-port", type=int, help="Port for the Gradio UI (defaults to 7860).")
    parser.add_argument("--host", default="127.0.0.1", help="Host address for servers.")
    parser.add_argument("--listen", action="store_true", help="Listen on 0.0.0.0 (overrides --host).")
    parser.add_argument("--share", action="store_true", help="Create a public Gradio sharing link.")
    parser.add_argument("--debug", action="store_true", help="Enable debug/reload mode for services.")
    parser.add_argument("--env-file", help="Path to a custom .env file to load.")
    
    args = parser.parse_args()

<<<<<<< HEAD
    # Use 0.0.0.0 if --listen is specified
    host = "0.0.0.0" if args.listen else args.host
=======
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

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    # Ensure launcher is running with a compatible Python
    if os.environ.get("LAUNCHER_REEXEC_GUARD") != "1":
<<<<<<< HEAD
        current_version = sys.version_info[:2]
        if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
            interpreter = find_compatible_python_interpreter()
            if interpreter:
                re_execute_with_compatible_python(interpreter)
            else:
                logger.error(f"Python {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]} is required but not found.")
                return 1
=======
        interpreter = find_compatible_python_interpreter()
        if interpreter:
            re_execute_with_compatible_python(interpreter)
        else:
            target_major, target_minor = PYTHON_MIN_VERSION
            logger.error(
                f"Python {target_major}.{target_minor} is required, but not found. "
                "Please install it or run with a compatible interpreter."
            )
            sys.exit(1)

    elif os.environ.get("LAUNCHER_REEXEC_GUARD") == "1":
        logger.info(
            f"Launcher re-executed with Python {sys.version_info.major}.{sys.version_info.minor}"
        )
>>>>>>> origin/main

    _setup_signal_handlers()
    args = parse_arguments()
>>>>>>> origin/feat/modular-ai-platform

    # Set environment file if specified
    if args.env_file:
        env_path = Path(args.env_file)
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
            logger.info(f"Loaded environment variables from {env_path}")
        else:
            logger.error(f"Environment file not found: {env_path}")
            sys.exit(1)

    # Check Python version
    check_python_version()

    # Determine venv path
    venv_path = ROOT_DIR / VENV_DIR

    # Setup mode
    if args.setup or args.update_deps:
        if not args.no_venv:
            create_venv(venv_path, args.force_recreate_venv)
            install_uv(venv_path)
            setup_dependencies(venv_path, args.update_deps)
        
        if not args.no_download_nltk:
            download_nltk_data(venv_path)
        
        logger.info("Setup completed successfully.")
        return

    # If not in setup mode, ensure venv exists (unless --no-venv is specified)
    if not args.no_venv and not venv_path.exists():
        logger.error(f"Virtual environment does not exist at {venv_path}. Please run with --setup first.")
        sys.exit(1)

    # Start services
    if not args.no_backend:
        start_backend(venv_path, host, args.port, args.debug)
        time.sleep(2)  # Brief pause to let backend start

    if not args.no_ui:
        start_gradio_ui(venv_path, host, args.gradio_port, args.debug, args.share)

    if not args.no_client:
        # Note: The client and server-ts might require additional parameters or configuration
        start_client()
        start_server_ts()

    logger.info("All selected services started. Press Ctrl+C to shut down.")
    wait_for_processes()


if __name__ == "__main__":
    sys.exit(main())