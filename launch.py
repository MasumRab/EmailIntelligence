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

import os
import sys
import platform
import subprocess
import argparse
import shutil
import venv
import logging
import json
import time
import signal
import pkg_resources
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")

# Global list to keep track of subprocesses
processes = []
# Global variable to store ngrok tunnel if created
ngrok_tunnel = None

def _handle_sigint(signum, frame):
    logger.info("Received SIGINT/SIGTERM, shutting down...")
    for p in processes:
        if p.poll() is None: # Check if process is still running
            logger.info(f"Terminating process {p.pid}...")
            p.terminate()
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning(f"Process {p.pid} did not terminate gracefully, killing.")
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
            logger.warning("pyngrok is not installed, cannot manage ngrok tunnel shutdown.")
        except Exception as e:
            logger.error(f"Error shutting down ngrok: {e}")

    sys.exit(0)

def _setup_signal_handlers():
    signal.signal(signal.SIGINT, _handle_sigint)
    signal.signal(signal.SIGTERM, _handle_sigint)

# Constants
PYTHON_MIN_VERSION = (3, 8)
PYTHON_MAX_VERSION = (3, 11)
VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"
REQUIREMENTS_VERSIONS_FILE = "requirements_versions.txt" # New constant
TORCH_CUDA_REQUIRED = False  # Set to True if CUDA is required

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent

# --- Functions migrated from deployment/env_manager.py ---
# These are initially named with _standalone to avoid conflict
# and will be renamed later.

def check_python_version_standalone() -> bool:
    """Check if the Python version is supported."""
    current_version = sys.version_info[:2]
    if current_version < PYTHON_MIN_VERSION:
        logger.error(f"Python {'.'.join(map(str, PYTHON_MIN_VERSION))} or higher is required")
        return False
    if current_version > PYTHON_MAX_VERSION:
        logger.warning(f"Python {'.'.join(map(str, current_version))} is not officially supported. "
                      f"Recommended version is {'.'.join(map(str, PYTHON_MAX_VERSION))} or lower.")
    return True

def is_venv_available_standalone() -> bool:
    """Check if a virtual environment is available."""
    venv_path = ROOT_DIR / VENV_DIR # Uses ROOT_DIR from launch.py
    if os.name == 'nt':  # Windows
        return venv_path.exists() and (venv_path / "Scripts" / "python.exe").exists()
    else:  # Unix-based systems
        return venv_path.exists() and (venv_path / "bin" / "python").exists()

def create_venv_standalone() -> bool:
    """Create a virtual environment."""
    venv_path = ROOT_DIR / VENV_DIR # Uses ROOT_DIR from launch.py
    if venv_path.exists(): # Check existence using the path
        logger.info(f"Virtual environment already exists at {venv_path}")
        return True
    
    logger.info(f"Creating virtual environment at {venv_path}")
    try:
        venv.create(venv_path, with_pip=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create virtual environment: {e}")
        return False

def get_python_executable_standalone() -> str:
    """Get the Python executable path."""
    if is_venv_available_standalone(): # Calls the standalone version
        if os.name == 'nt':  # Windows
            return str(ROOT_DIR / VENV_DIR / "Scripts" / "python.exe")
        else:  # Unix-based systems
            return str(ROOT_DIR / VENV_DIR / "bin" / "python")
    return sys.executable

def install_requirements_from_file(requirements_file_path_str: str, update: bool = False) -> bool:
    """Install or update requirements from a file.
    requirements_file_path_str is relative to ROOT_DIR.
    """
    python = get_python_executable_standalone() # Calls the standalone version
    # Ensure requirements_file_path_str is interpreted relative to ROOT_DIR
    requirements_path = ROOT_DIR / requirements_file_path_str
    
    if not requirements_path.exists():
        logger.error(f"Requirements file not found at {requirements_path}")
        return False
    
    cmd = [python, "-m", "pip", "install"]
    if update:
        cmd.append("--upgrade")
    cmd.extend(["-r", str(requirements_path)])
    
    logger.info(f"{'Updating' if update else 'Installing'} dependencies from {requirements_path.name}...")
    try:
        subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        return False

# --- End of migrated functions ---

# Comment out original functions
# def check_python_version() -> bool:
#     """Check if the Python version is supported."""
#     current_version = sys.version_info[:2]
#     if current_version < PYTHON_MIN_VERSION:
#         logger.error(f"Python {'.'.join(map(str, PYTHON_MIN_VERSION))} or higher is required")
#         return False
#     if current_version > PYTHON_MAX_VERSION:
#         logger.warning(f"Python {'.'.join(map(str, current_version))} is not officially supported. "
#                       f"Recommended version is {'.'.join(map(str, PYTHON_MAX_VERSION))} or lower.")
#     return True
#
# def is_venv_available() -> bool:
#     """Check if a virtual environment is available."""
#     venv_path = ROOT_DIR / VENV_DIR
#     return venv_path.exists() and (venv_path / "Scripts" / "python.exe").exists() if os.name == 'nt' else \
#            (venv_path / "bin" / "python").exists()
#
# def create_venv() -> bool:
#     """Create a virtual environment."""
#     venv_path = ROOT_DIR / VENV_DIR
#     if venv_path.exists():
#         logger.info(f"Virtual environment already exists at {venv_path}")
#         return True
#
#     logger.info(f"Creating virtual environment at {venv_path}")
#     try:
#         venv.create(venv_path, with_pip=True)
#         return True
#     except Exception as e:
#         logger.error(f"Failed to create virtual environment: {e}")
#         return False
#
# def get_python_executable() -> str:
#     """Get the Python executable path."""
#     if is_venv_available(): # This would now call the new is_venv_available
#         if os.name == 'nt':
#             return str(ROOT_DIR / VENV_DIR / "Scripts" / "python.exe")
#         else:
#             return str(ROOT_DIR / VENV_DIR / "bin" / "python")
#     return sys.executable
#
# def install_dependencies(update: bool = False) -> bool:
#     """Install or update dependencies."""
#     python = get_python_executable() # This would now call the new get_python_executable
#     requirements_path = ROOT_DIR / REQUIREMENTS_FILE # Default requirements file
#
#     if not requirements_path.exists():
#         logger.error(f"Requirements file not found at {requirements_path}")
#         return False
#
#     cmd = [python, "-m", "pip", "install"]
#     if update:
#         cmd.append("--upgrade")
#     cmd.extend(["-r", str(requirements_path)])
#
#     logger.info(f"{'Updating' if update else 'Installing'} dependencies...")
#     try:
#         subprocess.check_call(cmd)
#         return True
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Failed to install dependencies: {e}")
#         return False

# Rename standalone functions to take over the original names
check_python_version = check_python_version_standalone
is_venv_available = is_venv_available_standalone
create_venv = create_venv_standalone
get_python_executable = get_python_executable_standalone

# The new function for installing requirements was install_requirements_from_file.
# We want launch.py's main dependency installer to be this.
# The original install_dependencies took only 'update'. The new one takes 'requirements_file_path_str' and 'update'.
# We will alias install_dependencies to install_requirements_from_file.
# The call sites of install_dependencies will need to be updated if they don't pass the requirements file path.
# For now, let's make install_dependencies the more capable function.
install_dependencies = install_requirements_from_file


# Adjust get_python_executable to ensure it calls the new is_venv_available (already done by renaming)
# No change needed here as get_python_executable_standalone already called is_venv_available_standalone

# Adjust install_dependencies (which is now install_requirements_from_file)
# to ensure it calls the new get_python_executable (already done by renaming)
# No change needed here as install_requirements_from_file already called get_python_executable_standalone

# Clean up the _standalone aliases from global scope if they are no longer needed
del check_python_version_standalone
del is_venv_available_standalone
del create_venv_standalone
del get_python_executable_standalone
# del install_requirements_from_file # install_dependencies is now an alias to this

def check_torch_cuda() -> bool:
    """Check if PyTorch with CUDA is available."""
    python = get_python_executable()
    
    try:
        result = subprocess.run(
            [python, "-c", "import torch; print(torch.cuda.is_available())"],
            capture_output=True,
            text=True,
            check=True
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
    if os.name == 'nt':  # Windows
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
    try:
        subprocess.check_call([
            python, "-c", 
            "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
        ])
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to download NLTK data: {e}")
        return False

def prepare_environment(args: argparse.Namespace) -> bool:
    """Prepare the environment for running the application."""
    # Remove Import environment manager
    # from deployment.env_manager import env_manager # This line is removed.
    
    # Check Python version
    if not args.skip_python_version_check and not check_python_version(): # Use local function
        return False
    
    # Create virtual environment if needed and install/update dependencies
    if not args.no_venv:
        if not is_venv_available(): # Use local function
            logger.info("Virtual environment not found. Creating...")
            if not create_venv(): # Use local function
                logger.error("Failed to create virtual environment. Exiting.")
                return False
            # Install/update dependencies after creating venv
            primary_req_file_to_install = REQUIREMENTS_VERSIONS_FILE
            if not (ROOT_DIR / primary_req_file_to_install).exists():
                logger.info(f"{REQUIREMENTS_VERSIONS_FILE} not found, falling back to {REQUIREMENTS_FILE}.")
                primary_req_file_to_install = REQUIREMENTS_FILE

            logger.info(f"Installing base dependencies from {primary_req_file_to_install} into new venv...")
            if not install_dependencies(primary_req_file_to_install, args.update_deps):
                logger.error(f"Failed to install base dependencies from {primary_req_file_to_install} in new venv. Exiting.")
                return False
        elif args.update_deps: # If venv exists, only update if requested
            primary_req_file_to_update = REQUIREMENTS_VERSIONS_FILE
            if not (ROOT_DIR / primary_req_file_to_update).exists():
                logger.info(f"{REQUIREMENTS_VERSIONS_FILE} not found, falling back to {REQUIREMENTS_FILE} for update check.")
                primary_req_file_to_update = REQUIREMENTS_FILE

            logger.info(f"Updating base dependencies from {primary_req_file_to_update} in existing venv...")
            if not install_dependencies(primary_req_file_to_update, True): # Force update True
                logger.error(f"Failed to update base dependencies from {primary_req_file_to_update}. Exiting.")
                return False
        else:
            # Even if not updating, log which primary file is considered active or would be used.
            chosen_req_file = REQUIREMENTS_VERSIONS_FILE if (ROOT_DIR / REQUIREMENTS_VERSIONS_FILE).exists() else REQUIREMENTS_FILE
            logger.info(f"Virtual environment found. Primary requirements file: {chosen_req_file}. Skipping dependency installation unless --update-deps is used.")

        # Handle stage-specific requirements after base requirements
        # This replaces the logic from env_manager.setup_environment_for_stage()
        stage_requirements_file = None
        if args.stage == "dev":
            # Assuming DEV_REQUIREMENTS_FILE would be defined, let's use a string literal for now
            # Or better, define it as a constant if it's standard
            dev_req_path = ROOT_DIR / "requirements-dev.txt"
            if dev_req_path.exists():
                stage_requirements_file = "requirements-dev.txt"
        elif args.stage == "test":
            # Assuming TEST_REQUIREMENTS_FILE would be defined
            test_req_path = ROOT_DIR / "requirements-test.txt"
            if test_req_path.exists():
                stage_requirements_file = "requirements-test.txt"

        if stage_requirements_file:
            logger.info(f"Installing stage-specific requirements for '{args.stage}' stage from {stage_requirements_file}...")
            if not install_dependencies(stage_requirements_file, args.update_deps): # Use local function
                logger.error(f"Failed to install stage-specific dependencies from {stage_requirements_file}. Exiting.")
                return False
    
    # Check PyTorch CUDA
    if TORCH_CUDA_REQUIRED and not args.skip_torch_cuda_test:
        # Removed: system_info = env_manager.get_system_info()
        if not check_torch_cuda(): # This function uses local get_python_executable
            if args.reinstall_torch:
                logger.info("PyTorch CUDA not found. Reinstalling PyTorch with CUDA support as requested.")
                # Removed: env_manager.uninstall_package and env_manager.install_package calls
                if not reinstall_torch(): # Use local function
                    logger.error("Failed to reinstall PyTorch with CUDA. Please check manually.")
                    # Depending on how critical this is, you might return False.
            else:
                logger.warning("PyTorch CUDA is not available. Use --reinstall-torch to attempt reinstallation, or --skip-torch-cuda-test to ignore.")
    
    # Download NLTK data
    if not args.no_download_nltk:
        # Removed: python = env_manager.get_python_executable()
        if not download_nltk_data(): # This function uses local get_python_executable
            # Error is logged within download_nltk_data
            return False
    
    # Load extensions if not skipped
    if not args.skip_extensions:
        from deployment.extensions import extensions_manager
        extensions_manager.load_extensions()
        extensions_manager.initialize_extensions()
    
    # Download models if needed
    if not args.skip_models:
        from deployment.models import models_manager
        if not models_manager.list_models():
            logger.info("No models found. Downloading default models...")
            models_manager.download_default_models()
    
    return True

def start_backend(args: argparse.Namespace, python_executable: str) -> Optional[subprocess.Popen]:
    """Starts the backend server."""
    actual_host = "0.0.0.0" if args.listen else args.host
    logger.info(f"Starting backend server on {actual_host}:{args.port}...")

    cmd = [
        python_executable,
        "-m", "uvicorn",
        "server.python_backend.main:app", # Assuming this is the correct path to your ASGI app
        "--host", actual_host, # Use actual_host here
        "--port", str(args.port)
    ]

    if args.debug: # For local development, --reload is often useful
        cmd.append("--log-level=debug")
        cmd.append("--reload") # Add reload for development

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)
    # Determine NODE_ENV based on stage, default to development
    env["NODE_ENV"] = "development" if args.stage == "dev" else args.stage
    env["DEBUG"] = str(args.debug)

    try:
        # Log the command with the actual host
        log_cmd = cmd[:]
        if args.listen: # For logging, show the original intention if --listen was used
            log_cmd[log_cmd.index(actual_host)] = f"{args.host} (via --listen on 0.0.0.0)"
        logger.info(f"Running backend command: {' '.join(log_cmd)}")
        process = subprocess.Popen(cmd, env=env)
        processes.append(process) # Add to global list
        logger.info(f"Backend server started with PID {process.pid} on {actual_host}:{args.port}.")
        return process
    except FileNotFoundError:
        logger.error(f"Error: Python executable not found at {python_executable} or uvicorn not installed in the venv.")
        logger.error("Please ensure your virtual environment is active and has 'uvicorn' and other backend dependencies installed.")
        return None
    except Exception as e:
        logger.error(f"Failed to start backend server: {e}")
        return None

def start_frontend(args: argparse.Namespace) -> Optional[subprocess.Popen]:
    """Starts the frontend development server."""
    logger.info(f"Starting frontend server on {args.host}:{args.frontend_port}...")

    # Check for Node.js
    try:
        subprocess.check_call(["node", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Node.js is not installed or not found in PATH. Cannot start frontend.")
        return None

    cmd = [
        "npm", "run", "dev", "--",
        "--host", args.host,
        "--port", str(args.frontend_port)
    ]

    env = os.environ.copy()
    env["VITE_API_URL"] = f"http://{args.host}:{args.port}" # Backend URL for Vite
    env["NODE_ENV"] = "development" # Or args.stage if relevant for frontend build

    try:
        logger.info(f"Running frontend command: {' '.join(cmd)} in {str(ROOT_DIR / 'client')}")
        process = subprocess.Popen(cmd, cwd=str(ROOT_DIR / "client"), env=env)
        processes.append(process) # Add to global list
        logger.info(f"Frontend server started with PID {process.pid}.")
        return process
    except FileNotFoundError:
        logger.error("Error: 'npm' not found. Please ensure Node.js and npm are installed and in your PATH.")
        return None
    except Exception as e:
        logger.error(f"Failed to start frontend server: {e}")
        return None

def run_application(args: argparse.Namespace) -> int:
    """Run the application with the specified arguments."""
    python_executable = get_python_executable()
    backend_process = None
    frontend_process = None
    global ngrok_tunnel # To store the ngrok tunnel object

    if args.share:
        try:
            from pyngrok import ngrok, conf
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
            logger.info(f"Ngrok tunnel established. Public URL: {ngrok_tunnel.public_url}")
            logger.info("Note: If you have a free ngrok account, you might be limited to one tunnel at a time.")
            logger.info("Ensure your ngrok authtoken is configured if you face issues: ngrok authtoken <YOUR_AUTHTOKEN>")

        except ImportError:
            logger.error("pyngrok is not installed. Please run 'pip install pyngrok' to use the --share feature.")
            logger.warning("--share feature disabled.")
        except Exception as e: # Catch other ngrok errors (auth, connection, etc.)
            logger.error(f"Failed to start ngrok tunnel: {e}")
            logger.warning("--share feature might not be working as expected.")
            if ngrok_tunnel: # If tunnel object exists but failed later
                try: ngrok.disconnect(ngrok_tunnel.public_url); ngrok.kill()
                except: pass
                ngrok_tunnel = None


    # Load .env file if specified
    # Note: The env dict from original code is not directly used by Popen here.
    # Environment variables for Popen are set directly in start_backend/start_frontend.
    # If args.env_file is meant to globally affect os.environ, that should be handled earlier,
    # possibly in main() before prepare_environment or run_application.
    # For now, this specific 'env' dict isn't used further in this refactored version.
    if args.env_file:
        env_file_path = ROOT_DIR / args.env_file
        if env_file_path.exists():
            logger.info(f"Loading environment variables from {env_file_path}")
            from dotenv import load_dotenv # Consider adding to imports if not there
            load_dotenv(dotenv_path=env_file_path, override=True)
        else:
            logger.warning(f"Specified env file {args.env_file} not found at {env_file_path}")

    if args.api_only:
        logger.info("Running in API only mode.")
        backend_process = start_backend(args, python_executable)
        if backend_process:
            backend_process.wait() # Wait for backend to finish or be interrupted
        else:
            logger.error("Failed to start backend server in API only mode.")
            return 1
    elif args.frontend_only:
        logger.info("Running in Frontend only mode.")
        # Note: Frontend usually needs API URL. User must ensure API is running elsewhere or configured.
        if not args.api_url: # Or some other check if frontend can run without live API
             logger.warning("Frontend only mode: VITE_API_URL might not be correctly set if backend is not running or --api-url is not provided.")
        frontend_process = start_frontend(args)
        if frontend_process:
            frontend_process.wait()
        else:
            logger.error("Failed to start frontend server in frontend only mode.")
            return 1
    elif args.stage == "dev" or not args.stage: # Default to local development mode
        logger.info("Running in local development mode (backend and frontend).")
        backend_process = start_backend(args, python_executable)
        frontend_process = start_frontend(args)

        if backend_process:
            logger.info(f"Backend accessible at http://{args.host}:{args.port}")
        else:
            logger.error("Backend server failed to start.")
            if frontend_process and frontend_process.poll() is None:
                frontend_process.terminate() # Stop frontend if backend failed
            return 1 # Critical failure

        if frontend_process:
            logger.info(f"Frontend accessible at http://{args.host}:{args.frontend_port}")
        else:
            logger.error("Frontend server failed to start.")
            if backend_process and backend_process.poll() is None:
                backend_process.terminate() # Stop backend if frontend failed
            return 1 # Critical failure

        if backend_process and frontend_process:
            logger.info("Backend and Frontend started. Press Ctrl+C to stop.")
            try:
                # Keep main thread alive until SIGINT, which is handled by _handle_sigint
                while True:
                    # Check if either process has exited unexpectedly
                    if backend_process.poll() is not None:
                        logger.error(f"Backend process {backend_process.pid} exited unexpectedly.")
                        if frontend_process.poll() is None:
                            logger.info(f"Terminating frontend process {frontend_process.pid}...")
                            frontend_process.terminate()
                        break
                    if frontend_process.poll() is not None:
                        logger.error(f"Frontend process {frontend_process.pid} exited unexpectedly.")
                        if backend_process.poll() is None:
                            logger.info(f"Terminating backend process {backend_process.pid}...")
                            backend_process.terminate()
                        break
                    time.sleep(1)
            except KeyboardInterrupt: # This should ideally be caught by the SIGINT handler
                logger.info("KeyboardInterrupt in run_application. Signal handler should take over.")
                pass # Signal handler will manage shutdown
            except Exception as e:
                logger.error(f"An unexpected error occurred in run_application main loop: {e}")
            finally:
                # Ensure processes are terminated if loop exits for other reasons
                # _handle_sigint should manage this, but as a fallback:
                for p in [backend_process, frontend_process]:
                    if p and p.poll() is None:
                        p.terminate()
                        try: p.wait(timeout=1)
                        except subprocess.TimeoutExpired: p.kill()

        elif backend_process: # Only backend started and frontend failed earlier
            logger.info("Only backend process is running. Waiting for it to complete.")
            backend_process.wait()
        # (No case for only frontend, as backend failure would terminate it)

    elif args.stage == "test":
        logger.info("Running application in 'test' stage (executing tests)...")
        # This section replicates the test execution logic from main() when specific test args are given.
        # If --stage test is used, it implies running all relevant tests.
        from deployment.test_stages import test_stages # Moved import here

        test_success = True
        # Determine which tests to run. If --stage test is given, maybe run all?
        # Or expect other flags like --unit, --integration to be combined.
        # For now, let's assume if --stage test is set, it runs a default suite (e.g., unit and integration).
        # If specific flags like --unit are also given, the logic in main() before run_application would handle it.
        # This part is for when ONLY --stage test is the primary command.

        # If specific test arguments (like --unit, --integration) are NOT provided,
        # then --stage test could imply a default set of tests.
        # However, the current structure in main() already checks for --unit, --integration etc.
        # before calling run_application.
        # So, if run_application is called with args.stage == "test", it means those specific
        # test flags were NOT set.
        # This part of the code might be simplified if --stage test implies specific test runs
        # that are not covered by the --unit, --integration args directly in main().

        # Let's refine this: if --stage test is specified, it should run a comprehensive suite.
        # The existing logic in main() for --unit etc. handles specific test runs.
        # If neither --unit nor other specific test flags are given, but --stage test is,
        # then we run a default set.

        if not (args.unit or args.integration or args.e2e or args.performance or args.security):
            logger.info("No specific test types provided with --stage test. Running unit and integration tests by default.")
            if hasattr(test_stages, 'run_unit_tests'):
                 test_success = test_stages.run_unit_tests(args.coverage, args.debug) and test_success
            else:
                logger.warning("test_stages.run_unit_tests not found.")
            if hasattr(test_stages, 'run_integration_tests'):
                test_success = test_stages.run_integration_tests(args.coverage, args.debug) and test_success
            else:
                logger.warning("test_stages.run_integration_tests not found.")
            # Add other default tests if needed
        else:
            # If specific flags like --unit were passed, they would be handled by the block in main().
            # This path (args.stage == "test" inside run_application) would ideally not be hit
            # if those flags caused an early exit in main().
            # However, to be safe, we can state that specific test flags should be used, or rely on the default above.
            logger.info("Specific test flags (--unit, --integration, etc.) were likely handled before run_application.")
            logger.info("If you see this, it means --stage test was passed alongside other specific test flags OR those specific test flags were not handled in main().")
            # Fallback to the default set if somehow specific flags didn't trigger tests in main()
            if hasattr(test_stages, 'run_unit_tests'):
                 test_success = test_stages.run_unit_tests(args.coverage, args.debug) and test_success
            if hasattr(test_stages, 'run_integration_tests'):
                test_success = test_stages.run_integration_tests(args.coverage, args.debug) and test_success

        return 0 if test_success else 1
    # Staging and Prod are no longer valid choices here as per argparser modification.
    # else:
    #    logger.error(f"Unknown or unsupported stage for direct execution: {args.stage}")
    #    return 1

    return 0 # Assuming success if processes managed by signal handler or exited cleanly

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="EmailIntelligence Launcher")
    
    # Environment setup arguments
    parser.add_argument("--no-venv", action="store_true", help="Don't create or use a virtual environment")
    parser.add_argument("--update-deps", action="store_true", help="Update dependencies before launching")
    parser.add_argument("--skip-torch-cuda-test", action="store_true", help="Skip CUDA availability test for PyTorch")
    parser.add_argument("--reinstall-torch", action="store_true", help="Reinstall PyTorch (useful for CUDA issues)")
    parser.add_argument("--skip-python-version-check", action="store_true", help="Skip Python version check")
    parser.add_argument("--no-download-nltk", action="store_true", help="Skip downloading NLTK data")
    parser.add_argument("--skip-prepare", action="store_true", help="Skip preparation steps")
    
    # Application stage
    parser.add_argument("--stage", choices=["dev", "test"], default="dev",
                        help="Specify the application mode ('dev' for running, 'test' for running tests).")
    
    # Server configuration
    parser.add_argument("--port", type=int, default=8000, help="Specify the port to run on (default: 8000)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Specify the host to run on (default: 127.0.0.1)")
    parser.add_argument("--frontend-port", type=int, default=5173, help="Specify the frontend port to run on (default: 5173)")
    parser.add_argument("--api-url", type=str, help="Specify the API URL for the frontend")
    parser.add_argument("--api-only", action="store_true", help="Run only the API server without the frontend")
    parser.add_argument("--frontend-only", action="store_true", help="Run only the frontend without the API server")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    # Testing options
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report when running tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--security", action="store_true", help="Run security tests")
    
    # Extensions and models
    parser.add_argument("--skip-extensions", action="store_true", help="Skip loading extensions")
    parser.add_argument("--skip-models", action="store_true", help="Skip downloading models")
    parser.add_argument("--install-extension", type=str, help="Install an extension from a Git repository")
    parser.add_argument("--uninstall-extension", type=str, help="Uninstall an extension")
    parser.add_argument("--update-extension", type=str, help="Update an extension")
    parser.add_argument("--list-extensions", action="store_true", help="List all extensions")
    parser.add_argument("--create-extension", type=str, help="Create a new extension template")
    
    # Model options
    parser.add_argument("--download-model", type=str, help="Download a model from a URL")
    parser.add_argument("--model-name", type=str, help="Specify the model name for download")
    parser.add_argument("--list-models", action="store_true", help="List all models")
    parser.add_argument("--delete-model", type=str, help="Delete a model")
    
    # Advanced options
    parser.add_argument("--no-half", action="store_true", help="Disable half-precision for models")
    parser.add_argument("--force-cpu", action="store_true", help="Force CPU mode even if GPU is available")
    parser.add_argument("--low-memory", action="store_true", help="Enable low memory mode")
    parser.add_argument("--system-info", action="store_true", help="Print system information")
    
    # Networking options
    parser.add_argument("--share", action="store_true", help="Create a public URL using ngrok")
    parser.add_argument("--listen", action="store_true", help="Make the backend server listen on 0.0.0.0")
    parser.add_argument("--ngrok-region", type=str, help="Specify ngrok region (e.g., us, eu, ap, au, sa, jp, in). Used with --share.")

    # UI and Execution options
    parser.add_argument("--theme", type=str, default="system", help="UI theme (e.g., light, dark, system). For future use.")
    parser.add_argument("--allow-code", action="store_true", help="Allow execution of custom code from extensions (for future use).")
    parser.add_argument("--loglevel", type=str, default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Set the logging level for the launcher and application.")

    # Environment configuration
    parser.add_argument("--env-file", type=str, help="Specify a custom .env file")
    
    return parser.parse_args()

def main() -> int:
    """Main entry point."""
    _setup_signal_handlers() # Setup signal handlers at the beginning
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
        force=True
    )
    # Ensure our main launcher logger also adheres to this level.
    # (basicConfig sets root, getLogger then inherits or can be set specifically)
    logger.setLevel(numeric_level)
    # Other loggers (e.g., from libraries) will also use this level unless configured otherwise.

    logger.info(f"Launcher log level set to: {args.loglevel}")

    # Handle special commands
    
    # System information
    if args.system_info:
        # from deployment.env_manager import env_manager # Removed this import
        # env_manager.print_system_info() # Removed this call
        logger.info("The --system-info option is temporarily disabled as part of refactoring.")
        print("System information display is temporarily disabled.")
        return 0
    
    # Extensions management
    if args.list_extensions:
        from deployment.extensions import extensions_manager
        extensions_manager.load_extensions()
        extensions = extensions_manager.list_extensions()
        
        print(f"Found {len(extensions)} extensions:")
        for extension in extensions:
            print(f"  {extension['name']} - {'Enabled' if extension['enabled'] else 'Disabled'}")
            print(f"    Path: {extension['path']}")
            print(f"    Loaded: {extension['loaded']}")
            print(f"    Description: {extension['metadata'].get('description', 'No description')}")
            print()
        
        return 0
    
    if args.install_extension:
        from deployment.extensions import extensions_manager
        success = extensions_manager.install_extension(args.install_extension)
        return 0 if success else 1
    
    if args.uninstall_extension:
        from deployment.extensions import extensions_manager
        success = extensions_manager.uninstall_extension(args.uninstall_extension)
        return 0 if success else 1
    
    if args.update_extension:
        from deployment.extensions import extensions_manager
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
        from deployment.test_stages import test_stages # Import here as it's specific to this block
        
        test_run_success = True
        
        if args.unit:
            logger.info("Running unit tests...")
            test_run_success = test_stages.run_unit_tests(args.coverage, args.debug) and test_run_success
        
        if args.integration:
            logger.info("Running integration tests...")
            test_run_success = test_stages.run_integration_tests(args.coverage, args.debug) and test_run_success
        
        if args.e2e:
            logger.info("Running e2e tests...")
            test_run_success = test_stages.run_e2e_tests(True, args.debug) and test_run_success
        
        if args.performance:
            logger.info("Running performance tests...")
            test_run_success = test_stages.run_performance_tests(60, 10, args.debug) and test_run_success
        
        if args.security:
            logger.info("Running security tests...")
            test_run_success = test_stages.run_security_tests(f"http://{args.host}:{args.port}", args.debug) and test_run_success
        
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