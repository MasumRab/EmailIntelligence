#!/usr/bin/env python3
"""
EmailIntelligence Launcher

This script provides a unified way to launch the EmailIntelligence application
with automatic environment setup, dependency management, and configuration.
It's inspired by the approach used in projects like Stable Diffusion WebUI.

Usage:
    python launch.py [arguments]

Arguments:
    --help                      Show this help message
    --no-venv                   Don't create or use a virtual environment
    --update-deps               Update dependencies before launching
    --skip-python-version-check Skip Python version check
    --stage {dev,test,staging,prod}  Specify the application stage to run
    --port PORT                 Specify the port to run on (default: 8000)
    --host HOST                 Specify the host to run on (default: 127.0.0.1)
    --api-only                  Run only the API server without the frontend
    --frontend-only             Run only the frontend without the API server
    --debug                     Enable debug mode
    --no-download-nltk          Skip downloading NLTK data
    --skip-prepare              Skip preparation steps
    --no-half                   Disable half-precision for models
    --force-cpu                 Force CPU mode even if GPU is available
    --low-memory                Enable low memory mode
    --listen                    Make the server listen on network
    --env-file FILE             Specify a custom .env file
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
from dotenv import load_dotenv

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
    """Check if the Python version is supported."""
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
    """Check if a virtual environment is available."""
    venv_path = ROOT_DIR / VENV_DIR
    if os.name == "nt":  # Windows
        return venv_path.exists() and (venv_path / "Scripts" / "python.exe").exists()
    else:  # Unix-based systems
        return venv_path.exists() and (venv_path / "bin" / "python").exists()


def create_venv() -> bool:
    """Create a virtual environment."""
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
    """Get the Python executable path."""
    if is_venv_available():
        if os.name == "nt":  # Windows
            return str(ROOT_DIR / VENV_DIR / "Scripts" / "python.exe")
        else:  # Unix-based systems
            return str(ROOT_DIR / VENV_DIR / "bin" / "python")
    return sys.executable


def install_requirements_from_file(requirements_file_path_str: str, update: bool = False) -> bool:
    """Install or update requirements from a file.
    requirements_file_path_str is relative to ROOT_DIR.
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
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
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
    """Download NLTK data."""
    python = get_python_executable()

    logger.info("Downloading NLTK data...")
    cmd = [
        python,
        "-c",
        "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True); nltk.download('vader_lexicon', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True); nltk.download('brown', quiet=True); print('NLTK data download initiated.')",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info("NLTK data download process completed.")
        if result.stdout:
            logger.debug(f"NLTK download stdout:\n{result.stdout}")
        if result.stderr:
            logger.debug(
                f"NLTK download stderr:\n{result.stderr}"
            )
        return True
    except subprocess.CalledProcessError as e:
        logger.error("Failed to download NLTK data.")
        if e.stdout:
            logger.error(f"NLTK download stdout:\n{e.stdout}")
        if e.stderr:
            logger.error(f"NLTK download stderr:\n{e.stderr}")
        return False


def _get_primary_requirements_file() -> str:
    """Determines the primary requirements file to use."""
    versions_file_path = ROOT_DIR / REQUIREMENTS_VERSIONS_FILE
    if versions_file_path.exists():
        return REQUIREMENTS_VERSIONS_FILE
    else:
        logger.info(
            f"'{REQUIREMENTS_VERSIONS_FILE}' not found, attempting to use '{REQUIREMENTS_FILE}'."
        )
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
    """Run the application with the specified arguments."""
    python_executable = get_python_executable()
    backend_process = None
    gradio_process = None

    if args.env_file:
        env_file_path = ROOT_DIR / args.env_file
        if env_file_path.exists():
            logger.info(f"Loading environment variables from custom .env file: {env_file_path}")
            load_dotenv(dotenv_path=env_file_path, override=True)
        else:
            logger.warning(f"Specified env file {args.env_file} not found at {env_file_path}")

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

        if backend_process:
            logger.info(f"Backend accessible at http://{args.host}:{args.port}")
        else:
            logger.error("Backend server failed to start.")
            if gradio_process and gradio_process.poll() is None:
                gradio_process.terminate()
            return 1

        if gradio_process:
            gradio_port_info = f":{args.gradio_port}" if args.gradio_port else " on default port (e.g. 7860)"
            logger.info(f"Gradio UI starting at http://{args.host}{gradio_port_info}. Check console for exact URL.")
        else:
            logger.error("Gradio UI failed to start.")
            if backend_process and backend_process.poll() is None:
                backend_process.terminate()
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
                logger.info("KeyboardInterrupt in run_application. Signal handler should take over.")
                pass
            except Exception as e:
                logger.error(f"An unexpected error occurred in run_application main loop: {e}")
            finally:
                for p in [backend_process, gradio_process]:
                    if p and p.poll() is None:
                        p.terminate()
                        try:
                            p.wait(timeout=1)
                        except subprocess.TimeoutExpired:
                            p.kill()
            if unexpected_exit:
                logger.error("One or more services exited unexpectedly.")
                return 1
    elif args.stage == "test":
        logger.info("Running application in 'test' stage (executing tests)...")
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
            logger.warning("test_stages.run_integration_tests not found, cannot run integration tests.")
        logger.info(f"Default test suite execution finished. Success: {test_run_success}")
        return 0 if test_run_success else 1

    return 0


def _print_system_info():
    """Prints detailed system information."""
    print("\n--- System Information ---")
    print(f"Operating System: {platform.system()} {platform.release()} ({platform.version()})")
    print(f"Processor: {platform.processor()}")
    try:
        print(f"CPU Cores: {os.cpu_count()}")
    except NotImplementedError:
        print("CPU Cores: Not available")

    print(f"\n--- Python Environment ---")
    print(f"Python Version: {sys.version.splitlines()[0]}")
    print(f"System Python Executable: {sys.executable}")
    print(f"Launcher's Perceived Python Executable: {get_python_executable()}")
    print(f"Project Root Directory (ROOT_DIR): {ROOT_DIR}")
    print(f"Virtual Environment Directory (VENV_DIR): {ROOT_DIR / VENV_DIR}")
    print(f"Venv Active (according to launcher): {is_venv_available()}")

    print("\n--- Requirements Files ---")
    for req_file_name in [
        REQUIREMENTS_FILE,
        REQUIREMENTS_VERSIONS_FILE,
        "requirements-dev.txt",
        "requirements-test.txt",
    ]:
        req_file_path = ROOT_DIR / req_file_name
        status = "Found" if req_file_path.exists() else "Not Found"
        print(f"{req_file_name}: {status} at {req_file_path}")

    print("\n--- PyTorch Information ---")
    try:
        python_exec = get_python_executable()
        torch_version_proc = subprocess.run(
            [python_exec, "-c", "import torch; print(torch.__version__)"],
            capture_output=True,
            text=True,
        )
        if torch_version_proc.returncode == 0:
            print(f"PyTorch Version: {torch_version_proc.stdout.strip()}")
            # check_torch_cuda() # This function was removed
        else:
            print("PyTorch Version: Not installed or importable with current Python executable.")
            logger.debug(f"Failed to get PyTorch version: {torch_version_proc.stderr}")
    except Exception as e:
        print(f"PyTorch Information: Error checking PyTorch - {e}")

    print("\n--- Memory Information ---")
    try:
        import psutil

        virtual_mem = psutil.virtual_memory()
        swap_mem = psutil.swap_memory()
        print(f"Total RAM: {virtual_mem.total / (1024**3):.2f} GB")
        print(f"Available RAM: {virtual_mem.available / (1024**3):.2f} GB")
        print(f"Used RAM: {virtual_mem.used / (1024**3):.2f} GB ({virtual_mem.percent}%)")
        print(f"Total Swap: {swap_mem.total / (1024**3):.2f} GB")
        print(f"Used Swap: {swap_mem.used / (1024**3):.2f} GB ({swap_mem.percent}%)")
    except ImportError:
        print(
            "Memory Information: `psutil` module not found. Install with `pip install psutil` for detailed memory stats."
        )
    except Exception as e:
        print(f"Memory Information: Error getting memory info - {e}")

    print("\n--- End of System Information ---")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="EmailIntelligence Launcher")

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
    parser.add_argument("--share", action="store_true", help="Enable Gradio sharing link")

    # Testing options
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Generate coverage report when running tests",
    )
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--security", action="store_true", help="Run security tests")

    # Advanced options
    parser.add_argument("--no-half", action="store_true", help="Disable half-precision for models")
    parser.add_argument(
        "--force-cpu",
        action="store_true",
        help="Force CPU mode even if GPU is available",
    )
    parser.add_argument("--low-memory", action="store_true", help="Enable low memory mode")
    parser.add_argument("--system-info", action="store_true", help="Print system information")

    # Networking options
    parser.add_argument(
        "--listen",
        action="store_true",
        help="Make the backend server listen on 0.0.0.0",
    )

    # UI and Execution options
    parser.add_argument(
        "--theme",
        type=str,
        default="system",
        help="UI theme (e.g., light, dark, system). For future use.",
    )
    parser.add_argument(
        "--allow-code",
        action="store_true",
        help="Allow execution of custom code from extensions (for future use).",
    )
    parser.add_argument(
        "--loglevel",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level for the launcher and application.",
    )

    # Environment configuration
    parser.add_argument("--env-file", type=str, help="Specify a custom .env file")

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    if os.environ.get("LAUNCHER_REEXEC_GUARD") != "1":
        current_major, current_minor = sys.version_info[:2]
        target_major, target_minor = PYTHON_MIN_VERSION

        current_version = (current_major, current_minor)
        if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
            logger.info(
                f"Current Python is {current_major}.{current_minor}. "
                f"Launcher requires Python {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]} to {PYTHON_MAX_VERSION[0]}.{PYTHON_MAX_VERSION[1]}. Attempting to find and re-execute."
            )

            candidate_interpreters = []
            if platform.system() == "Windows":
                candidate_interpreters = [
                    ["py", "-3.12"],
                    ["py", "-3.11"],
                    ["python3.12"],
                    ["python3.11"],
                    ["python"],
                ]
            else:
                candidate_interpreters = [
                    ["python3.12"],
                    ["python3.11"],
                    ["python3"],
                ]

            found_interpreter_path = None
            for candidate_parts in candidate_interpreters:
                exe_name = candidate_parts[0]
                version_check_args = candidate_parts[1:]

                potential_path = shutil.which(exe_name)
                if potential_path:
                    cmd_to_check = [potential_path] + version_check_args + ["--version"]
                    try:
                        env = os.environ.copy()
                        result = subprocess.run(
                            cmd_to_check,
                            capture_output=True,
                            text=True,
                            check=False,
                            env=env,
                            timeout=5,
                        )

                        version_output = result.stdout.strip() + result.stderr.strip()

                        compatible = False
                        for major in range(PYTHON_MIN_VERSION[0], PYTHON_MAX_VERSION[0] + 1):
                            for minor in range(PYTHON_MIN_VERSION[1] if major == PYTHON_MIN_VERSION[0] else 0, 
                                             PYTHON_MAX_VERSION[1] + 1 if major == PYTHON_MAX_VERSION[0] else 100):
                                if f"Python {major}.{minor}" in version_output:
                                    logger.info(
                                        f"Found compatible Python {major}.{minor} interpreter: {potential_path} (version output: {version_output})"
                                    )
                                    found_interpreter_path = potential_path
                                    compatible = True
                                    break
                            if compatible:
                                break
                        
                        if compatible:
                            break
                        else:
                            logger.debug(
                                f"Candidate {potential_path} (from {exe_name}) is not in supported Python version range. Output: {version_output}"
                            )
                    except subprocess.TimeoutExpired:
                        logger.warning(
                            f"Timeout checking version of interpreter candidate: {potential_path} (from {exe_name})"
                        )
                    except Exception as e:
                        logger.warning(
                            f"Error checking version of interpreter candidate: {potential_path} (from {exe_name}): {e}"
                        )

            if found_interpreter_path:
                logger.info(f"Re-executing launcher with interpreter: {found_interpreter_path}")
                new_env = os.environ.copy()
                new_env["LAUNCHER_REEXEC_GUARD"] = "1"

                try:
                    script_path = str(Path(__file__).resolve())
                    args_for_exec = [found_interpreter_path, script_path] + sys.argv[1:]
                    os.execve(found_interpreter_path, args_for_exec, new_env)
                except Exception as e:
                    logger.error(f"Failed to re-execute with {found_interpreter_path}: {e}")

            logger.error(
                f"Python {target_major}.{target_minor} is required, but a compatible version was not found "
                f"on your system after searching common paths (candidates: {[c[0] for c in candidate_interpreters]}). "
                f"Please install Python {target_major}.{target_minor}, ensure it's in your PATH, "
                f"or run {Path(__file__).name} using a Python {target_major}.{target_minor} interpreter directly."
            )
            sys.exit(1)

    elif os.environ.get("LAUNCHER_REEXEC_GUARD") == "1":
        logger.info(
            f"Launcher re-executed with Python {sys.version_info.major}.{sys.version_info.minor} "
            f"(Guard was set). Skipping further Python version discovery."
        )

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

    if args.unit or args.integration or args.e2e or args.performance or args.security:
        logger.info("Specific test flags detected. Running requested tests...")
        from deployment.test_stages import test_stages

        test_run_success = True

        if args.unit:
            logger.info("Running unit tests...")
            test_run_success = (
                test_stages.run_unit_tests(args.coverage, args.debug) and test_run_success
            )

        if args.integration:
            logger.info("Running integration tests...")
            test_run_success = (
                test_stages.run_integration_tests(args.coverage, args.debug) and test_run_success
            )

        if args.e2e:
            logger.info("Running e2e tests...")
            test_run_success = test_stages.run_e2e_tests(True, args.debug) and test_run_success

        if args.performance:
            logger.info("Running performance tests...")
            test_run_success = (
                test_stages.run_performance_tests(60, 10, args.debug) and test_run_success
            )

        if args.security:
            logger.info("Running security tests...")
            test_run_success = (
                test_stages.run_security_tests(f"http://{args.host}:{args.port}", args.debug)
                and test_run_success
            )

        logger.info(f"Test execution finished. Success: {test_run_success}")
        return 0 if test_run_success else 1

    if not args.skip_prepare and not prepare_environment(args):
        return 1

    return run_application(args)


if __name__ == "__main__":
    sys.exit(main())