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
    logger.info("Received SIGINT/SIGTERM, shutting down all services...")
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
    signal.signal(signal.SIGINT, _handle_sigint)
    signal.signal(signal.SIGTERM, _handle_sigint)


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
            if not download_nltk_data():
                return False
            return False

    return True



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

def run_application(args: argparse.Namespace) -> int:
    """Run the selected application components."""
    python_executable = get_python_executable()
    services_started = []

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

    return 0


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

    if not prepare_environment(args):
        logger.error("Environment setup failed. Aborting.")
        return 1

    if args.setup:
        logger.info("Environment setup complete. Exiting as requested by --setup flag.")
        return 0

    return run_application(args)


if __name__ == "__main__":
    sys.exit(main())