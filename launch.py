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
    --skip-torch-cuda-test      Skip CUDA availability test for PyTorch
    --reinstall-torch           Reinstall PyTorch (useful for CUDA issues)
    --skip-python-version-check Skip Python version check
    --stage {dev,test,staging,prod}  Specify the application stage to run
    --port PORT                 Specify the port to run on (default: 8000)
    --host HOST                 Specify the host to run on (default: 127.0.0.1)
    --api-only                  Run only the API server without the frontend
    --frontend-only             Run only the frontend without the API server
    --debug                     Enable debug mode
    --no-download-nltk          Skip downloading NLTK data
    --skip-prepare              Skip preparation steps
    --skip-extensions           Skip loading extensions
    --no-half                   Disable half-precision for models
    --force-cpu                 Force CPU mode even if GPU is available
    --low-memory                Enable low memory mode
    --share                     Create a public URL
    --listen                    Make the server listen on network
    --ngrok NGROK               Use ngrok to create a tunnel, specify ngrok region
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

import pkg_resources
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")

# Global list to keep track of subprocesses
processes = []
# Global variable to store ngrok tunnel if created
ngrok_tunnel = None


def _handle_sigint(signum, frame):
    logger.info("Received SIGINT/SIGTERM, shutting down...")
    for p in processes:
        if p.poll() is None:  # Check if process is still running
            logger.info(f"Terminating process {p.pid}...")
            p.terminate()
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning(
                    f"Process {p.pid} did not terminate gracefully, killing."
                )
                p.kill()

    global ngrok_tunnel
    if ngrok_tunnel:
        try:
            from pyngrok import ngrok

            logger.info(f"Closing ngrok tunnel: {ngrok_tunnel.public_url} ...")
            ngrok.disconnect(ngrok_tunnel.public_url)
            ngrok.kill()
            logger.info("Ngrok tunnel closed.")
            ngrok_tunnel = None
        except ImportError:
            logger.warning(
                "pyngrok is not installed, cannot manage ngrok tunnel shutdown."
            )
        except Exception as e:
            logger.error(f"Error shutting down ngrok: {e}")

    sys.exit(0)


def _setup_signal_handlers():
    signal.signal(signal.SIGINT, _handle_sigint)
    signal.signal(signal.SIGTERM, _handle_sigint)


# Constants
PYTHON_MIN_VERSION = (3, 11)
PYTHON_MAX_VERSION = (3, 11)
VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"
REQUIREMENTS_VERSIONS_FILE = "requirements_versions.txt"  # New constant
TORCH_CUDA_REQUIRED = False  # Set to True if CUDA is required

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent

# --- Functions migrated from deployment/env_manager.py ---
# These are initially named with _standalone to avoid conflict
# and will be renamed later.

# --- Start of functions that were migrated and renamed ---
# The _standalone suffix is removed from definitions and calls directly.


def check_python_version() -> bool:
    """Check if the Python version is supported."""
    current_version = sys.version_info[:2]
    if current_version < PYTHON_MIN_VERSION:
        logger.error(
            f"Python {'.'.join(map(str, PYTHON_MIN_VERSION))} or higher is required"
        )
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
    if is_venv_available():  # Internal call uses the final name
        if os.name == "nt":  # Windows
            return str(ROOT_DIR / VENV_DIR / "Scripts" / "python.exe")
        else:  # Unix-based systems
            return str(ROOT_DIR / VENV_DIR / "bin" / "python")
    return sys.executable


def install_requirements_from_file(
    requirements_file_path_str: str, update: bool = False
) -> bool:
    """Install or update requirements from a file.
    requirements_file_path_str is relative to ROOT_DIR.
    """
    python = get_python_executable()  # Internal call uses the final name
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
        # Using subprocess.run to capture output for better error reporting (as per previous subtask)
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies from {requirements_path.name}.")
        logger.error(f"pip stdout:\n{e.stdout}")
        logger.error(f"pip stderr:\n{e.stderr}")
        return False


# Alias for backward compatibility or consistent naming if preferred elsewhere
install_dependencies = install_requirements_from_file

# --- End of functions that were migrated and renamed ---

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
        logger.info(
            f"PyTorch CUDA is {'available' if is_available else 'not available'}"
        )
        return is_available
    except subprocess.CalledProcessError:
        logger.warning("Failed to check PyTorch CUDA availability")
        return False


def reinstall_torch() -> bool:
    """Reinstall PyTorch with CUDA support."""
    python = get_python_executable()

    # Uninstall existing PyTorch
    logger.info("Uninstalling existing PyTorch...")
    subprocess.run(
        [python, "-m", "pip", "uninstall", "-y", "torch", "torchvision", "torchaudio"]
    )

    # Install PyTorch with CUDA support
    logger.info("Installing PyTorch with CUDA support...")
    if os.name == "nt":  # Windows
        cmd = f"{python} -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
    else:  # Linux/MacOS
        cmd = f"{python} -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"

    try:
        subprocess.check_call(cmd, shell=True)
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
        if (
            result.stderr
        ):  # NLTK often prints to stderr even on success for some messages
            logger.debug(
                f"NLTK download stderr:\n{result.stderr}"
            )  # Use debug for potentially noisy stderr
        return True
    except subprocess.CalledProcessError as e:
        logger.error("Failed to download NLTK data.")
        if e.stdout:  # Only log if there's actual content
            logger.error(f"NLTK download stdout:\n{e.stdout}")
        if e.stderr:  # Only log if there's actual content
            logger.error(f"NLTK download stderr:\n{e.stderr}")
        return False


# Helper function to get the primary requirements file (factored out in a previous task)
def _get_primary_requirements_file() -> str:
    """Determines the primary requirements file to use.
    Prefers requirements_versions.txt, falls back to requirements.txt.
    Returns the file name string (relative to ROOT_DIR).
    """
    versions_file_path = ROOT_DIR / REQUIREMENTS_VERSIONS_FILE
    if versions_file_path.exists():
        return REQUIREMENTS_VERSIONS_FILE
    else:
        logger.info(
            f"'{REQUIREMENTS_VERSIONS_FILE}' not found, attempting to use '{REQUIREMENTS_FILE}'."
        )
        return REQUIREMENTS_FILE


def prepare_environment(args: argparse.Namespace) -> bool:
    """Prepare the environment for running the application."""
    # Remove Import environment manager
    # from deployment.env_manager import env_manager # This line is removed.

    # Check Python version
    if not args.skip_python_version_check and not check_python_version():
        # This check ensures the current interpreter running launch.py is correct.
        # The interpreter discovery logic in main() should have already handled this.
        logger.error(
            "Initial Python version check failed. This should have been handled by interpreter discovery."
        )
        return False

    # Create virtual environment if needed and install/update dependencies
    if not args.no_venv:
        venv_recreated_this_run = False
        venv_needs_initial_setup = False

        if is_venv_available():
            logger.info(
                f"Virtual environment found at '{ROOT_DIR / VENV_DIR}'. Checking Python version..."
            )

            venv_python_exe_path = ""
            if os.name == "nt":
                venv_python_exe_path = str(
                    ROOT_DIR / VENV_DIR / "Scripts" / "python.exe"
                )
            else:
                venv_python_exe_path = str(ROOT_DIR / VENV_DIR / "bin" / "python")

            if not Path(venv_python_exe_path).exists():
                logger.warning(
                    f"Venv python executable not found at {venv_python_exe_path}. Assuming incompatible or corrupted venv."
                )
                # Treat as incompatible, prompt for re-creation
                try:
                    response = (
                        input(
                            f"WARNING: Could not find Python executable in the existing virtual environment at './{VENV_DIR}'. "
                            f"It might be corrupted. Do you want to delete and recreate it with Python 3.11.x? (yes/no): "
                        )
                        .strip()
                        .lower()
                    )
                except EOFError:
                    response = "no"
                    logger.warning(
                        "Non-interactive session, defaulting to not recreating corrupted venv."
                    )

                if response == "yes":
                    logger.info(
                        f"User approved. Deleting and recreating virtual environment at './{VENV_DIR}'."
                    )
                    try:
                        shutil.rmtree(ROOT_DIR / VENV_DIR)
                        logger.info(
                            f"Successfully deleted existing virtual environment './{VENV_DIR}'."
                        )
                    except OSError as e:
                        logger.error(
                            f"Failed to delete virtual environment './{VENV_DIR}': {e}. Please delete it manually and restart."
                        )
                        return False

                    if not create_venv():
                        logger.error("Failed to recreate virtual environment. Exiting.")
                        return False
                    venv_recreated_this_run = True
                    venv_needs_initial_setup = True
                else:
                    logger.warning(
                        f"User declined or non-interactive. Proceeding with the potentially corrupted virtual environment in './{VENV_DIR}'. "
                        "This may cause errors."
                    )
                    # If we proceed with a corrupted venv, dependency installation might fail or use wrong python.
                    # It's safer to return False if we can't verify its Python.
                    # However, the original subtask said "acceptable to proceed with caution". For now, we'll log and let it try.

            else:  # Venv Python executable found, check its version
                try:
                    result = subprocess.run(
                        [venv_python_exe_path, "--version"],
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=5,
                    )
                    version_output = result.stdout.strip() + result.stderr.strip()

                    # Basic parsing: "Python X.Y.Z"
                    if version_output.startswith("Python "):
                        parts = version_output.split(" ")[1].split(".")
                        if len(parts) >= 2:
                            venv_major = int(parts[0])
                            venv_minor = int(parts[1])

                            target_major, target_minor = PYTHON_MIN_VERSION
                            if not (
                                venv_major == target_major
                                and venv_minor == target_minor
                            ):
                                logger.warning(
                                    f"WARNING: The existing virtual environment at './{VENV_DIR}' was created with Python {venv_major}.{venv_minor}. "
                                    f"This project requires Python {target_major}.{target_minor}."
                                )
                                try:
                                    response = (
                                        input(
                                            "Do you want to delete and recreate the virtual environment with "
                                            f"Python {target_major}.{target_minor}? (yes/no): "
                                        )
                                        .strip()
                                        .lower()
                                    )
                                except EOFError:
                                    response = "no"
                                    logger.warning(
                                        "Non-interactive session, defaulting to not recreating incompatible venv."
                                    )

                                if response == "yes":
                                    logger.info(
                                        f"User approved. Deleting and recreating virtual environment at './{VENV_DIR}'."
                                    )
                                    try:
                                        shutil.rmtree(ROOT_DIR / VENV_DIR)
                                        logger.info(
                                            f"Successfully deleted existing virtual environment './{VENV_DIR}'."
                                        )
                                    except OSError as e:
                                        logger.error(
                                            f"Failed to delete virtual environment './{VENV_DIR}': {e}. Please delete it manually and restart."
                                        )
                                        return False

                                    if (
                                        not create_venv()
                                    ):  # create_venv logs success/failure
                                        logger.error(
                                            "Failed to recreate virtual environment. Exiting."
                                        )
                                        return False
                                    venv_recreated_this_run = True
                                    venv_needs_initial_setup = True
                                else:
                                    logger.warning(
                                        f"User declined or non-interactive. Proceeding with the existing, "
                                        f"potentially incompatible virtual environment (Python {venv_major}.{venv_minor}) in './{VENV_DIR}'."
                                    )
                                    print(
                                        f"WARNING: You chose to proceed with an incompatible Python version ({venv_major}.{venv_minor}) "
                                        f"in the virtual environment './{VENV_DIR}'. This may cause errors or unexpected behavior. "
                                        f"It is strongly recommended to use a Python {target_major}.{target_minor} environment."
                                    )
                            else:
                                logger.info(
                                    f"Existing virtual environment at './{VENV_DIR}' uses compatible Python {venv_major}.{venv_minor}."
                                )
                        else:  # Malformed version string
                            logger.warning(
                                f"Could not parse Python version from venv output: '{version_output}'. Assuming incompatibility and proceeding with caution."
                            )
                    else:  # Does not start with "Python "
                        logger.warning(
                            f"Unrecognized version output from venv Python: '{version_output}'. Assuming incompatibility and proceeding with caution."
                        )

                except subprocess.TimeoutExpired:
                    logger.warning(
                        f"Timeout checking version of venv Python at '{venv_python_exe_path}'. Proceeding with caution."
                    )
                except Exception as e:
                    logger.warning(
                        f"Error checking version of venv Python at '{venv_python_exe_path}': {e}. Proceeding with caution."
                    )

        else:  # No venv found initially
            logger.info(f"Virtual environment not found at './{VENV_DIR}'. Creating...")
            if not create_venv():
                logger.error("Failed to create virtual environment. Exiting.")
                return False
            venv_needs_initial_setup = True  # Mark for dependency installation

        # Install/update dependencies if venv was just created/recreated, or if --update-deps is specified
        if venv_needs_initial_setup:
            primary_req_file = _get_primary_requirements_file()
            logger.info(
                f"Installing base dependencies from {Path(primary_req_file).name} into {'new' if not venv_recreated_this_run else 'recreated'} venv..."
            )
            # Pass update=False because it's a fresh setup of dependencies.
            # args.update_deps is handled below for existing, compatible venvs.
            if not install_dependencies(primary_req_file, update=False):
                logger.error(
                    f"Failed to install base dependencies from {Path(primary_req_file).name}. Exiting."
                )
                return False
        elif (
            args.update_deps
        ):  # Venv existed, was compatible (or user chose to proceed), and user wants to update
            primary_req_file = _get_primary_requirements_file()
            logger.info(
                f"Updating base dependencies from {Path(primary_req_file).name} in existing venv as per --update-deps..."
            )
            if not install_dependencies(
                primary_req_file, update=True
            ):  # Force update True
                logger.error(
                    f"Failed to update base dependencies from {Path(primary_req_file).name}. Exiting."
                )
                return False
        else:  # Venv existed, was compatible (or user chose to proceed), and no --update-deps
            chosen_req_file = (
                _get_primary_requirements_file()
            )  # Log which primary file is considered active
            logger.info(
                f"Compatible virtual environment found (or user chose to proceed with existing). Primary requirements file: {Path(chosen_req_file).name}. Skipping base dependency installation unless --update-deps is used."
            )

        # Handle stage-specific requirements
        # This logic should run if venv was newly set up, or if args.update_deps is true for existing venv
        stage_requirements_file_path_str = (
            None  # Use full path string for install_dependencies
        )
        if args.stage == "dev":
            dev_req_path_obj = ROOT_DIR / "requirements-dev.txt"
            if dev_req_path_obj.exists():
                stage_requirements_file_path_str = "requirements-dev.txt"
        elif args.stage == "test":
            test_req_path_obj = ROOT_DIR / "requirements-test.txt"
            if test_req_path_obj.exists():
                stage_requirements_file_path_str = "requirements-test.txt"

        if stage_requirements_file_path_str:
            # Install stage-specific if:
            # 1. Venv was just set up (fresh install of stage deps)
            # 2. Venv existed and --update-deps was passed (update stage deps)
            # 3. Venv existed, was re-created, and user chose to proceed (fresh install of stage deps)
            # The 'args.update_deps' flag for install_dependencies handles the update part.
            # If venv_needs_initial_setup is true, we want a fresh install (update=False).
            # Otherwise, respect args.update_deps.
            # This logic is a bit subtle. If venv_needs_initial_setup, then primary deps were installed with update=False.
            # Stage deps should also be fresh in that case.
            # If not venv_needs_initial_setup, then primary deps were updated based on args.update_deps.
            # Stage deps should follow the same update flag.

            install_stage_deps_update_flag = args.update_deps
            if (
                venv_needs_initial_setup
            ):  # If we did a fresh install of base, do fresh for stage too
                install_stage_deps_update_flag = False
                logger.info(
                    f"Installing stage-specific requirements for '{args.stage}' from {Path(stage_requirements_file_path_str).name} into {'new' if not venv_recreated_this_run else 'recreated'} venv..."
                )
            elif (
                args.update_deps
            ):  # Only log about updating if not a fresh setup and update_deps is true
                logger.info(
                    f"Updating stage-specific requirements for '{args.stage}' from {Path(stage_requirements_file_path_str).name} as per --update-deps..."
                )
            else:  # No initial setup, no update_deps, so skip stage-specific unless they were missing
                logger.info(
                    f"Skipping stage-specific requirements for '{args.stage}' from {Path(stage_requirements_file_path_str).name} unless missing or --update-deps is used."
                )

            # The install_dependencies function itself is idempotent if packages are already there and update=False
            # So, it's generally safe to call it. The update flag controls upgrade behavior.
            if (
                venv_needs_initial_setup or args.update_deps
            ):  # Only proceed if new/recreated or updating
                if not install_dependencies(
                    stage_requirements_file_path_str,
                    update=install_stage_deps_update_flag,
                ):
                    logger.error(
                        f"Failed to install/update stage-specific dependencies from {Path(stage_requirements_file_path_str).name}. Exiting."
                    )
                    return False
            # If not venv_needs_initial_setup AND not args.update_deps, we can log that we are skipping.
            # This is covered by the logger.info above.

    # Check PyTorch CUDA
    if TORCH_CUDA_REQUIRED and not args.skip_torch_cuda_test:
        if not check_torch_cuda():
            if args.reinstall_torch:
                logger.info(
                    "PyTorch CUDA not found. Reinstalling PyTorch with CUDA support as requested."
                )
                if not reinstall_torch():
                    logger.error(
                        "Failed to reinstall PyTorch with CUDA. Please check manually."
                    )
            else:
                logger.warning(
                    "PyTorch CUDA is not available. Use --reinstall-torch to attempt reinstallation, or --skip-torch-cuda-test to ignore."
                )

    # Download NLTK data
    if not args.no_download_nltk:
        if not download_nltk_data():
            return False

    python_executable = get_python_executable()  # Get python executable for managers

    # Load extensions if not skipped
    if not args.skip_extensions:
        from deployment.extensions import extensions_manager

        extensions_manager.set_python_executable(
            python_executable
        )  # Set python executable
        if not extensions_manager.load_extensions():
            logger.error("Failed to load one or more extensions.")
            return False
        if not extensions_manager.initialize_extensions():
            logger.error("Failed to initialize one or more extensions.")
            return False

    # Download models if needed
    if not args.skip_models:
        from deployment.models import models_manager

        logger.info(f"DEBUG: args.skip_models is False. Checking models...")
        current_models = models_manager.list_models()
        logger.info(f"DEBUG: models_manager.list_models() returned: {current_models}")
        # models_manager does not require python_executable to be set explicitly for now
        if not current_models:  # If "models" dir was truly empty initially
            if args.stage == "dev":
                logger.info(
                    "Development stage: Skipping download of default models. Placeholders will be used/created."
                )
            elif (
                not models_manager.download_default_models()
            ):  # Original logic for non-dev stages
                logger.error("Failed to download default models.")
                # Logged error, but will proceed to create_placeholder_nlp_models anyway

        # Always attempt to create/verify NLP placeholders if models are not skipped
        logger.info("Ensuring NLP placeholder models exist...")
        if not models_manager.create_placeholder_nlp_models():
            logger.warning(
                "Failed to create/verify some placeholder NLP models. NLP functionality might be limited."
            )

    return True


def start_backend(
    args: argparse.Namespace, python_executable: str
) -> Optional[subprocess.Popen]:
    """Starts the backend server."""
    actual_host = "0.0.0.0" if args.listen else args.host
    logger.info(f"Starting backend server on {actual_host}:{args.port}...")

    cmd = [
        python_executable,
        "-m",
        "uvicorn",
        "server.python_backend.main:app",  # Assuming this is the correct path to your ASGI app
        "--host",
        actual_host,  # Use actual_host here
        "--port",
        str(args.port),
    ]

    if args.debug:  # For local development, --reload is often useful
        cmd.append("--log-level=debug")
        cmd.append("--reload")  # Add reload for development

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)
    # Determine NODE_ENV based on stage, default to development
    env["NODE_ENV"] = "development" if args.stage == "dev" else args.stage
    env["DEBUG"] = str(args.debug)

    try:
        # Log the command with the actual host
        log_cmd = cmd[:]
        if args.listen:  # For logging, show the original intention if --listen was used
            log_cmd[log_cmd.index(actual_host)] = (
                f"{args.host} (via --listen on 0.0.0.0)"
            )
        logger.info(f"Running backend command: {' '.join(log_cmd)}")
        process = subprocess.Popen(cmd, env=env)
        processes.append(process)  # Add to global list
        logger.info(
            f"Backend server started with PID {process.pid} on {actual_host}:{args.port}."
        )
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


def start_frontend(args: argparse.Namespace) -> Optional[subprocess.Popen]:
    """Starts the frontend development server."""
    logger.info(f"Starting frontend server on {args.host}:{args.frontend_port}...")

    # Check for Node.js
    try:
        subprocess.check_call(
            ["node", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error(
            "Node.js is not installed or not found in PATH. Cannot start frontend."
        )
        return None

    client_dir = ROOT_DIR / "client"
    client_pkg_json = client_dir / "package.json"

    if client_pkg_json.exists():
        npm_executable_path = shutil.which("npm")
        if npm_executable_path is None:
            logger.error(
                f"The 'npm' command was not found in your system's PATH. "
                f"Please ensure Node.js and npm are correctly installed and that the npm installation directory is added to your PATH environment variable. "
                f"Attempted to find 'npm' for the client in: {client_dir}"
            )
            # Potentially return None here if npm is essential and not found,
            # or let it proceed to fail at the npm install line, which will now be more informed.
            # For now, let's log and let it try, as the original code attempts to continue.
            # If we want to stop it here, uncomment the next line:
            # return None
        else:
            logger.info(f"Found 'npm' executable at: {npm_executable_path}")

        logger.info(f"Found package.json in {client_dir}. Running npm install...")
        try:
            # Use subprocess.run to wait for completion and check for errors
            install_result = subprocess.run(
                ["npm", "install"],
                cwd=client_dir,
                capture_output=True,
                text=True,
                check=False,  # check=False to handle errors manually
            )
            if install_result.returncode != 0:
                logger.error(
                    f"Failed to install frontend dependencies in {client_dir}."
                )
                logger.error(f"npm stdout:\n{install_result.stdout}")
                logger.error(f"npm stderr:\n{install_result.stderr}")
                # Optionally, decide if this is a fatal error for frontend launch
                # For now, log and attempt to continue, Vite might still run if some deps are missing but core is there.
            else:
                logger.info(
                    f"Frontend dependencies installed successfully in {client_dir}."
                )
        except Exception as e:
            logger.error(f"Error running npm install in {client_dir}: {e}")
            # Decide how to handle this, for now, attempt to continue
    else:
        logger.warning(
            f"No package.json found in {client_dir}. Skipping npm install for frontend."
        )
        # This would likely lead to `npm run dev` failing, but the check is here.

    cmd = [
        "npm",
        "run",
        "dev",
        "--",
        "--host",
        args.host,
        "--port",
        str(args.frontend_port),
    ]

    env = os.environ.copy()
    env["VITE_API_URL"] = f"http://{args.host}:{args.port}"  # Backend URL for Vite
    env["NODE_ENV"] = "development"  # Or args.stage if relevant for frontend build

    try:
        logger.info(
            f"Running frontend command: {' '.join(cmd)} in {str(ROOT_DIR / 'client')}"
        )
        process = subprocess.Popen(cmd, cwd=str(ROOT_DIR / "client"), env=env)
        processes.append(process)  # Add to global list
        logger.info(f"Frontend server started with PID {process.pid}.")
        return process
    except FileNotFoundError:
        logger.error(
            "Error: 'npm' not found. Please ensure Node.js and npm are installed and in your PATH."
        )
        return None
    except Exception as e:
        logger.error(f"Failed to start frontend server: {e}")
        return None


def run_application(args: argparse.Namespace) -> int:
    """Run the application with the specified arguments."""
    python_executable = get_python_executable()
    backend_process = None
    frontend_process = None
    global ngrok_tunnel  # To store the ngrok tunnel object

    if args.share:
        try:
            from pyngrok import conf, ngrok

            logger.info("Starting ngrok tunnel...")
            if args.ngrok_region:
                logger.info(f"Using ngrok region: {args.ngrok_region}")
                # Pyngrok uses a config object or can be set via ngrok config file
                # For direct region setting if available via conf object:
                ngrok_conf = conf.PyngrokConfig(region=args.ngrok_region)
                conf.set_default(ngrok_conf)
                # Alternatively, ensure user has ngrok configured with region if above doesn't work as expected

            # Assuming backend port (args.port) is the one to share
            ngrok_tunnel = ngrok.connect(args.port)
            logger.info(
                f"Ngrok tunnel established. Public URL: {ngrok_tunnel.public_url}"
            )
            logger.info(
                "Note: If you have a free ngrok account, you might be limited to one tunnel at a time."
            )
            logger.info(
                "Ensure your ngrok authtoken is configured if you face issues: ngrok authtoken <YOUR_AUTHTOKEN>"
            )

        except ImportError:
            logger.error(
                "pyngrok is not installed. Please run 'pip install pyngrok' to use the --share feature."
            )
            logger.warning("--share feature disabled.")
        except Exception as e:  # Catch other ngrok errors (auth, connection, etc.)
            logger.error(f"Failed to start ngrok tunnel: {e}")
            logger.warning("--share feature might not be working as expected.")
            if ngrok_tunnel:  # If tunnel object exists but failed later
                try:
                    ngrok.disconnect(ngrok_tunnel.public_url)
                    ngrok.kill()
                except:
                    pass
                ngrok_tunnel = None

    # Load custom .env file if specified
    # Note: The env dict from original code is not directly used by Popen here.
    # Environment variables for Popen are set directly in start_backend/start_frontend.
    # Custom .env file will override any values from the default .env file
    if args.env_file:
        env_file_path = ROOT_DIR / args.env_file
        if env_file_path.exists():
            logger.info(
                f"Loading environment variables from custom .env file: {env_file_path}"
            )
            load_dotenv(dotenv_path=env_file_path, override=True)
        else:
            logger.warning(
                f"Specified env file {args.env_file} not found at {env_file_path}"
            )

    if args.api_only:
        logger.info("Running in API only mode.")
        backend_process = start_backend(args, python_executable)
        if backend_process:
            backend_process.wait()  # Wait for backend to finish or be interrupted
        else:
            logger.error("Failed to start backend server in API only mode.")
            return 1
    elif args.frontend_only:
        logger.info("Running in Frontend only mode.")
        # Note: Frontend usually needs API URL. User must ensure API is running elsewhere or configured.
        if not args.api_url:  # Or some other check if frontend can run without live API
            logger.warning(
                "Frontend only mode: VITE_API_URL might not be correctly set if backend is not running or --api-url is not provided."
            )
        frontend_process = start_frontend(args)
        if frontend_process:
            frontend_process.wait()
        else:
            logger.error("Failed to start frontend server in frontend only mode.")
            return 1
    elif args.stage == "dev" or not args.stage:  # Default to local development mode
        logger.info("Running in local development mode (backend and frontend).")
        unexpected_exit = False
        backend_process = start_backend(args, python_executable)
        frontend_process = start_frontend(args)

        if backend_process:
            logger.info(f"Backend accessible at http://{args.host}:{args.port}")
        else:
            logger.error("Backend server failed to start.")
            if frontend_process and frontend_process.poll() is None:
                frontend_process.terminate()  # Stop frontend if backend failed
            return 1  # Critical failure

        if frontend_process:
            logger.info(
                f"Frontend accessible at http://{args.host}:{args.frontend_port}"
            )
        else:
            logger.error("Frontend server failed to start.")
            if backend_process and backend_process.poll() is None:
                backend_process.terminate()  # Stop backend if frontend failed
            return 1  # Critical failure

        if backend_process and frontend_process:
            logger.info("Backend and Frontend started. Press Ctrl+C to stop.")
            try:
                # Keep main thread alive until SIGINT, which is handled by _handle_sigint
                while True:
                    # Check if either process has exited unexpectedly
                    if backend_process.poll() is not None:
                        logger.error(
                            f"Backend process {backend_process.pid} exited unexpectedly."
                        )
                        unexpected_exit = True
                        if frontend_process.poll() is None:
                            logger.info(
                                f"Terminating frontend process {frontend_process.pid}..."
                            )
                            frontend_process.terminate()
                        break
                    if frontend_process.poll() is not None:
                        logger.error(
                            f"Frontend process {frontend_process.pid} exited unexpectedly."
                        )
                        unexpected_exit = True
                        if backend_process.poll() is None:
                            logger.info(
                                f"Terminating backend process {backend_process.pid}..."
                            )
                            backend_process.terminate()
                        break
                    time.sleep(1)
            except (
                KeyboardInterrupt
            ):  # This should ideally be caught by the SIGINT handler
                logger.info(
                    "KeyboardInterrupt in run_application. Signal handler should take over."
                )
                pass  # Signal handler will manage shutdown
            except Exception as e:
                logger.error(
                    f"An unexpected error occurred in run_application main loop: {e}"
                )
            finally:
                # Ensure processes are terminated if loop exits for other reasons
                # _handle_sigint should manage this, but as a fallback:
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

        elif backend_process:  # Only backend started and frontend failed earlier
            logger.info("Only backend process is running. Waiting for it to complete.")
            backend_process.wait()
            # If backend exits with an error code, it might be an unexpected exit
            if backend_process.returncode != 0:
                logger.error(
                    f"Backend process exited with code: {backend_process.returncode}"
                )
                return 1
        # (No case for only frontend, as backend failure would terminate it)

    elif args.stage == "test":
        logger.info("Running application in 'test' stage (executing tests)...")
        logger.info(
            f"Executing default test suite for '--stage {args.stage}'. Specific test flags (e.g., --unit, --integration) were not provided."
        )
        from deployment.test_stages import \
            test_stages  # Moved import here for locality

        test_run_success = True  # Assume success initially

        # Run unit tests by default
        if hasattr(test_stages, "run_unit_tests"):
            logger.info("Running unit tests (default for --stage test)...")
            if not test_stages.run_unit_tests(args.coverage, args.debug):
                test_run_success = False
                logger.error("Unit tests failed.")
        else:
            logger.warning(
                "test_stages.run_unit_tests not found, cannot run unit tests."
            )
            # Consider if this should be a failure for the 'test' stage
            # test_run_success = False

        # Run integration tests by default
        if hasattr(test_stages, "run_integration_tests"):
            logger.info("Running integration tests (default for --stage test)...")
            if not test_stages.run_integration_tests(args.coverage, args.debug):
                test_run_success = False
                logger.error("Integration tests failed.")
        else:
            logger.warning(
                "test_stages.run_integration_tests not found, cannot run integration tests."
            )
            # Consider if this should be a failure for the 'test' stage
            # test_run_success = False

        logger.info(
            f"Default test suite execution finished. Success: {test_run_success}"
        )
        return 0 if test_run_success else 1

    return 0  # Assuming success if processes managed by signal handler or exited cleanly for other stages


def _print_system_info():
    """Prints detailed system information."""
    print("\n--- System Information ---")
    print(
        f"Operating System: {platform.system()} {platform.release()} ({platform.version()})"
    )
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
    # Check if PyTorch is installed before trying to import or run check_torch_cuda
    # This avoids ModuleNotFoundError if torch isn't even in the environment.
    # A more robust check might involve trying to import torch.
    try:
        # Attempt a lightweight check first using pkg_resources if available,
        # or directly try importing torch if that's preferred.
        # For simplicity, directly call check_torch_cuda and let it handle import errors if any.
        # However, check_torch_cuda itself calls get_python_executable and runs a subprocess.
        python_exec = get_python_executable()
        torch_version_proc = subprocess.run(
            [python_exec, "-c", "import torch; print(torch.__version__)"],
            capture_output=True,
            text=True,
        )
        if torch_version_proc.returncode == 0:
            print(f"PyTorch Version: {torch_version_proc.stdout.strip()}")
            check_torch_cuda()  # This will print CUDA availability
        else:
            print(
                "PyTorch Version: Not installed or importable with current Python executable."
            )
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
        print(
            f"Used RAM: {virtual_mem.used / (1024**3):.2f} GB ({virtual_mem.percent}%)"
        )
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
        "--skip-torch-cuda-test",
        action="store_true",
        help="Skip CUDA availability test for PyTorch",
    )
    parser.add_argument(
        "--reinstall-torch",
        action="store_true",
        help="Reinstall PyTorch (useful for CUDA issues)",
    )
    parser.add_argument(
        "--skip-python-version-check",
        action="store_true",
        help="Skip Python version check",
    )
    parser.add_argument(
        "--no-download-nltk", action="store_true", help="Skip downloading NLTK data"
    )
    parser.add_argument(
        "--skip-prepare", action="store_true", help="Skip preparation steps"
    )

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
        "--frontend-port",
        type=int,
        default=5173,
        help="Specify the frontend port to run on (default: 5173)",
    )
    parser.add_argument(
        "--api-url", type=str, help="Specify the API URL for the frontend"
    )
    parser.add_argument(
        "--api-only",
        action="store_true",
        help="Run only the API server without the frontend",
    )
    parser.add_argument(
        "--frontend-only",
        action="store_true",
        help="Run only the frontend without the API server",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    # Testing options
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Generate coverage report when running tests",
    )
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument(
        "--integration", action="store_true", help="Run integration tests"
    )
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    parser.add_argument(
        "--performance", action="store_true", help="Run performance tests"
    )
    parser.add_argument("--security", action="store_true", help="Run security tests")

    # Extensions and models
    parser.add_argument(
        "--skip-extensions", action="store_true", help="Skip loading extensions"
    )
    parser.add_argument(
        "--skip-models", action="store_true", help="Skip downloading models"
    )
    parser.add_argument(
        "--install-extension",
        type=str,
        help="Install an extension from a Git repository",
    )
    parser.add_argument(
        "--uninstall-extension", type=str, help="Uninstall an extension"
    )
    parser.add_argument("--update-extension", type=str, help="Update an extension")
    parser.add_argument(
        "--list-extensions", action="store_true", help="List all extensions"
    )
    parser.add_argument(
        "--create-extension", type=str, help="Create a new extension template"
    )

    # Model options
    parser.add_argument(
        "--download-model", type=str, help="Download a model from a URL"
    )
    parser.add_argument(
        "--model-name", type=str, help="Specify the model name for download"
    )
    parser.add_argument("--list-models", action="store_true", help="List all models")
    parser.add_argument("--delete-model", type=str, help="Delete a model")

    # Advanced options
    parser.add_argument(
        "--no-half", action="store_true", help="Disable half-precision for models"
    )
    parser.add_argument(
        "--force-cpu",
        action="store_true",
        help="Force CPU mode even if GPU is available",
    )
    parser.add_argument(
        "--low-memory", action="store_true", help="Enable low memory mode"
    )
    parser.add_argument(
        "--system-info", action="store_true", help="Print system information"
    )

    # Networking options
    parser.add_argument(
        "--share", action="store_true", help="Create a public URL using ngrok"
    )
    parser.add_argument(
        "--listen",
        action="store_true",
        help="Make the backend server listen on 0.0.0.0",
    )
    parser.add_argument(
        "--ngrok-region",
        type=str,
        help="Specify ngrok region (e.g., us, eu, ap, au, sa, jp, in). Used with --share.",
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

    # Python interpreter discovery and re-execution logic
    # Goal: Ensure launch.py runs with Python 3.11.x
    if os.environ.get("LAUNCHER_REEXEC_GUARD") != "1":
        current_major, current_minor = sys.version_info[:2]
        target_major, target_minor = (
            PYTHON_MIN_VERSION  # Assuming PYTHON_MIN_VERSION is (3, 11)
        )

        if not (current_major == target_major and current_minor == target_minor):
            logger.info(
                f"Current Python is {current_major}.{current_minor}. "
                f"Launcher requires Python {target_major}.{target_minor}. Attempting to find and re-execute."
            )

            candidate_interpreters = []
            if platform.system() == "Windows":
                candidate_interpreters = [
                    ["py", "-3.11"],  # Python Launcher for Windows
                    ["python3.11"],
                    ["python"],  # General python, check version
                ]
            else:  # Linux/macOS
                candidate_interpreters = [
                    ["python3.11"],
                    ["python3"],  # General python3, check version
                ]

            found_interpreter_path = None
            for candidate_parts in candidate_interpreters:
                exe_name = candidate_parts[0]
                version_check_args = candidate_parts[1:]  # Args for "py -3.11"

                potential_path = shutil.which(exe_name)
                if potential_path:
                    cmd_to_check = [potential_path] + version_check_args + ["--version"]
                    try:
                        # Ensure PATH is inherited by subprocess, especially for `py` on Windows
                        env = os.environ.copy()
                        result = subprocess.run(
                            cmd_to_check,
                            capture_output=True,
                            text=True,
                            check=False,
                            env=env,
                            timeout=5,
                        )

                        # Python version can be in stdout or stderr
                        version_output = result.stdout.strip() + result.stderr.strip()

                        # Example outputs: "Python 3.11.5" or "Python 3.11.0rc1"
                        if f"Python {target_major}.{target_minor}" in version_output:
                            logger.info(
                                f"Found compatible Python {target_major}.{target_minor} interpreter: {potential_path} (version output: {version_output})"
                            )
                            found_interpreter_path = potential_path
                            break
                        else:
                            logger.debug(
                                f"Candidate {potential_path} (from {exe_name}) is not Python {target_major}.{target_minor}. Output: {version_output}"
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
                logger.info(
                    f"Re-executing launcher with interpreter: {found_interpreter_path}"
                )
                new_env = os.environ.copy()
                new_env["LAUNCHER_REEXEC_GUARD"] = "1"

                # On Windows, os.execve is not ideal for .exe files if they are not true executables (e.g. py.exe might be tricky).
                # subprocess.Popen might be more robust for re-launching, then sys.exit.
                # However, the requirement is to use os.execve.
                try:
                    # sys.argv[0] should be launch.py. If it's an absolute path, use it.
                    # If not, it might be relative, which is fine for execve's second arg.
                    script_path = sys.argv[0]
                    if not os.path.isabs(script_path) and shutil.which(script_path):
                        # If sys.argv[0] is just "launch.py", make it absolute if possible,
                        # assuming it's in PATH or CWD. For robustness, ensure it's discoverable.
                        # A safer bet is to use __file__ from the script's context.
                        script_path = str(Path(__file__).resolve())

                    args_for_exec = [found_interpreter_path, script_path] + sys.argv[1:]
                    os.execve(found_interpreter_path, args_for_exec, new_env)
                    # os.execve does not return if successful
                except Exception as e:
                    logger.error(
                        f"Failed to re-execute with {found_interpreter_path}: {e}"
                    )
                    # Fall through to the error below if execve fails critically

            # If loop completes or execve fails before replacing the process
            logger.error(
                f"Python {target_major}.{target_minor} is required, but a compatible version was not found "
                f"on your system after searching common paths (candidates: {[c[0] for c in candidate_interpreters]}). "
                f"Please install Python {target_major}.{target_minor}, ensure it's in your PATH, "
                f"or run {Path(__file__).name} using a Python {target_major}.{target_minor} interpreter directly."
            )
            sys.exit(1)
        # If current version is already the target, and guard is not set, it implies first direct run with correct version.
        # No specific log needed here, it will just proceed.

    elif os.environ.get("LAUNCHER_REEXEC_GUARD") == "1":
        logger.info(
            f"Launcher re-executed with Python {sys.version_info.major}.{sys.version_info.minor} "
            f"(Guard was set). Skipping further Python version discovery."
        )
        # Optionally, unset the guard if it's not needed by child processes spawned by this script itself.
        # For now, keep it, as it doesn't harm.
        # del os.environ["LAUNCHER_REEXEC_GUARD"]

    _setup_signal_handlers()  # Setup signal handlers at the beginning
    # Parse arguments
    args = parse_arguments()

    # Configure logging level based on command line argument
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        # This should not happen due to choices in argparse, but good practice to check
        raise ValueError(f"Invalid log level: {args.loglevel}")

    # Reconfigure the root logger. Using force=True (Python 3.8+) to allow this.
    # This will affect all loggers unless they have had their level set explicitly.
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        force=True,
    )
    # Ensure our main launcher logger also adheres to this level.
    # (basicConfig sets root, getLogger then inherits or can be set specifically)
    logger.setLevel(numeric_level)
    # Other loggers (e.g., from libraries) will also use this level unless configured otherwise.

    logger.info(f"Launcher log level set to: {args.loglevel}")

    # Load default .env file if it exists
    default_env_file = ROOT_DIR / ".env"
    if default_env_file.exists():
        logger.info(
            f"Loading environment variables from default .env file: {default_env_file}"
        )
        load_dotenv(dotenv_path=default_env_file, override=True)

    # Handle special commands

    # System information
    if args.system_info:
        _print_system_info()
        return 0

    # Extensions management
    # Ensure python_executable is set for extensions_manager if any extension command is run
    # This is a bit repetitive but ensures it's set if --skip-prepare was used.
    # A more elegant solution might involve a global setup for managers.
    if (
        args.list_extensions
        or args.install_extension
        or args.uninstall_extension
        or args.update_extension
        or args.create_extension
    ):
        from deployment.extensions import extensions_manager

        if (
            not extensions_manager.python_executable
            or extensions_manager.python_executable == sys.executable
        ):  # Check if it needs setting
            # This check is to avoid overriding if already set by prepare_environment
            # to a venv python. If it's None or system python, and we are in venv, update it.
            current_launcher_python_exec = get_python_executable()
            if extensions_manager.python_executable != current_launcher_python_exec:
                extensions_manager.set_python_executable(current_launcher_python_exec)
                logger.debug(
                    f"Set python_executable for extensions_manager in main() to: {current_launcher_python_exec}"
                )

    if args.list_extensions:
        from deployment.extensions import extensions_manager

        # load_extensions might be needed if prepare_environment was skipped
        # However, list_extensions in its current form doesn't strictly need them loaded,
        # it lists based on discovery. If it were to list *loaded* extensions, this would change.
        # For now, assuming list_extensions can operate without full load_extensions() if needed.
        # extensions_manager.load_extensions() # Potentially add this if list shows *active* extensions
        extensions = extensions_manager.list_extensions()

        print(f"Found {len(extensions)} extensions:")
        for extension in extensions:
            print(
                f"  {extension['name']} - {'Enabled' if extension['enabled'] else 'Disabled'}"
            )
            print(f"    Path: {extension['path']}")
            print(f"    Loaded: {extension['loaded']}")
            print(
                f"    Description: {extension['metadata'].get('description', 'No description')}"
            )
            print()

        return 0

    if args.install_extension:
        from deployment.extensions import extensions_manager

        # Ensure prepare_environment or equivalent setup for venv has run if installing.
        if not args.skip_prepare:  # If prepare_environment ran, venv should be ready.
            pass  # Dependencies should be in venv.
        else:  # If skipping prepare, user is responsible for environment.
            logger.warning(
                "Skipping prepare_environment. Ensure correct Python environment for extension installation."
            )
        success = extensions_manager.install_extension(args.install_extension)
        return 0 if success else 1

    if args.uninstall_extension:
        from deployment.extensions import extensions_manager

        success = extensions_manager.uninstall_extension(args.uninstall_extension)
        return 0 if success else 1

    if args.update_extension:
        from deployment.extensions import extensions_manager

        # Similar to install, ensure environment is appropriate.
        if not args.skip_prepare:
            pass
        else:
            logger.warning(
                "Skipping prepare_environment. Ensure correct Python environment for extension update."
            )
        success = extensions_manager.update_extension(args.update_extension)
        return 0 if success else 1

    if args.create_extension:
        from deployment.extensions import extensions_manager

        success = extensions_manager.create_extension_template(args.create_extension)
        return 0 if success else 1

    # Models management
    if args.list_models:
        from deployment.models import models_manager

        models = models_manager.list_models()

        print(f"Found {len(models)} models:")
        for model in models:
            print(f"  {model}")

            # Print the model configuration if available
            config = models_manager.get_model_config(model)
            if config:
                print(f"    Configuration:")
                for key, value in config.items():
                    print(f"      {key}: {value}")

            print()

        return 0

    if args.download_model and args.model_name:
        from deployment.models import models_manager

        success = models_manager.download_model(args.download_model, args.model_name)
        return 0 if success else 1

    if args.delete_model:
        from deployment.models import models_manager

        success = models_manager.delete_model(args.delete_model)
        return 0 if success else 1

    # Testing options
    # This block handles specific test flags. If any are true, tests run and program exits.
    # If --stage test is specified WITHOUT these specific flags, it will be handled in run_application.
    if args.unit or args.integration or args.e2e or args.performance or args.security:
        logger.info("Specific test flags detected. Running requested tests...")
        from deployment.test_stages import \
            test_stages  # Import here as it's specific to this block

        test_run_success = True

        if args.unit:
            logger.info("Running unit tests...")
            test_run_success = (
                test_stages.run_unit_tests(args.coverage, args.debug)
                and test_run_success
            )

        if args.integration:
            logger.info("Running integration tests...")
            test_run_success = (
                test_stages.run_integration_tests(args.coverage, args.debug)
                and test_run_success
            )

        if args.e2e:
            logger.info("Running e2e tests...")
            test_run_success = (
                test_stages.run_e2e_tests(True, args.debug) and test_run_success
            )

        if args.performance:
            logger.info("Running performance tests...")
            test_run_success = (
                test_stages.run_performance_tests(60, 10, args.debug)
                and test_run_success
            )

        if args.security:
            logger.info("Running security tests...")
            test_run_success = (
                test_stages.run_security_tests(
                    f"http://{args.host}:{args.port}", args.debug
                )
                and test_run_success
            )

        logger.info(f"Test execution finished. Success: {test_run_success}")
        return 0 if test_run_success else 1

    # If --stage is 'test' but no specific test flags were given, run_application will handle it.
    # For other stages or default 'dev' stage, proceed to prepare environment and run application.

    # Prepare environment
    if not args.skip_prepare and not prepare_environment(args):
        return 1

    # Run application
    return run_application(args)


if __name__ == "__main__":
    sys.exit(main())
