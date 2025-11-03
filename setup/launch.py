#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

This script provides a single, unified way to set up, manage, and run all
components of the EmailIntelligence application, including the Python backend,
Gradio UI, and Node.js services. It uses 'uv' for Python dependency management
based on pyproject.toml.

Usage:
    python launch.py [command] [arguments]

Commands:
    setup    Set up the environment (virtual environment, dependencies, etc.)
    run      Run the EmailIntelligence application
    test     Run tests with optional coverage reporting

For backward compatibility, the old argument style is still supported.
"""

import argparse
import asyncio
import atexit
import logging
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import time
import threading
import venv
from pathlib import Path
from typing import List, Optional

# Add project root to sys.path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import new modular components
from src.core.commands.command_factory import get_command_factory
from src.core.container import initialize_services, initialize_all_services, cleanup_all_services

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    load_dotenv = None  # Will be loaded later if needed

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")


# --- Global state ---
def find_project_root() -> Path:
    """Find the project root directory by looking for key files."""
    current = Path(__file__).resolve().parent
    if (current / "pyproject.toml").exists() and current.name != "setup":
        return current
    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    return current


ROOT_DIR = find_project_root()

class ProcessManager:
    """Manages child processes for the application."""
    def __init__(self):
        self.processes = []
        self.lock = threading.Lock()  # Add lock for thread safety

    def add_process(self, process):
        with self.lock:
            self.processes.append(process)

    def cleanup(self):
        logger.info("Performing explicit resource cleanup...")
        # Create a copy of the list to avoid modifying while iterating
        with self.lock:
            processes_copy = self.processes[:]

        for p in processes_copy:
            if p.poll() is None:
                logger.info(f"Terminating process {p.pid}...")
                p.terminate()
                try:
                    p.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    logger.warning(f"Process {p.pid} did not terminate gracefully, killing.")
                    p.kill()
        logger.info("Resource cleanup completed.")

    def shutdown(self):
        logger.info("Received shutdown signal, cleaning up processes...")
        self.cleanup()
        sys.exit(0)

process_manager = ProcessManager()
atexit.register(process_manager.cleanup)

# --- Constants ---
PYTHON_MIN_VERSION = (3, 12)
PYTHON_MAX_VERSION = (3, 13)
VENV_DIR = "venv"
CONDA_ENV_NAME = os.getenv("CONDA_ENV_NAME", "base")

# --- WSL Support ---
def is_wsl():
    """Check if running in WSL environment"""
    try:
        with open('/proc/version', 'r') as f:
            content = f.read().lower()
            return 'microsoft' in content or 'wsl' in content
    except:
        return False

def setup_wsl_environment():
    """Setup WSL-specific environment variables if in WSL"""
    if not is_wsl():
        return

    # Set display for GUI applications
    if 'DISPLAY' not in os.environ:
        os.environ['DISPLAY'] = ':0'

    # Set matplotlib backend for WSL
    os.environ['MPLBACKEND'] = 'Agg'

    # Optimize for WSL performance
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    os.environ['PYTHONUNBUFFERED'] = '1'

    # Set OpenGL for WSL
    os.environ['LIBGL_ALWAYS_INDIRECT'] = '1'

    logger.info("🐧 WSL environment detected - applied optimizations")

def check_wsl_requirements():
    """Check WSL-specific requirements and warn if needed"""
    if not is_wsl():
        return

    # Check if X11 server is accessible (optional check)
    try:
        result = subprocess.run(['xset', '-q'],
                              capture_output=True,
                              timeout=2)
        if result.returncode != 0:
            logger.warning("X11 server not accessible - GUI applications may not work")
            logger.info("Install VcXsrv, MobaXterm, or similar X11 server on Windows")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass  # Silently ignore X11 check failures

# --- Python Version Checking ---
def check_python_version():
    """Check if the current Python version is compatible."""
    current_version = sys.version_info[:2]
    if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
        logger.error(f"Python version {platform.python_version()} is not compatible.")
        sys.exit(1)
    logger.info(f"Python version {platform.python_version()} is compatible.")

# --- Environment Validation ---
def check_for_merge_conflicts() -> bool:
    """Check for unresolved merge conflict markers in critical files."""
    conflict_markers = ["<<<<<<< ", "======= ", ">>>>>>> "]
    critical_files = [
        "backend/python_backend/main.py",
        "backend/python_nlp/nlp_engine.py",
        "backend/python_backend/database.py",
        "backend/python_backend/email_routes.py",
        "backend/python_backend/category_routes.py",
        "backend/python_backend/gmail_routes.py",
        "backend/python_backend/filter_routes.py",
        "backend/python_backend/action_routes.py",
        "backend/python_backend/dashboard_routes.py",
        "backend/python_backend/workflow_routes.py",
        "backend/python_backend/performance_monitor.py",
        "backend/python_nlp/gmail_integration.py",
        "backend/python_nlp/gmail_service.py",
        "backend/python_nlp/smart_filters.py",
        "backend/python_nlp/smart_retrieval.py",
        "backend/python_nlp/ai_training.py",
        "README.md",
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
    ]

    conflicts_found = False
    for file_path in critical_files:
        full_path = ROOT_DIR / file_path
        if full_path.exists():
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    for marker in conflict_markers:
                        if marker in content:
                            logger.error(
                                f"Unresolved merge conflict detected in {file_path} with marker: {marker.strip()}"
                            )
                            conflicts_found = True
            except Exception as e:
                logger.warning(f"Could not check {file_path} for conflicts: {e}")

    if conflicts_found:
        logger.error("Please resolve all merge conflicts before proceeding.")
        return False

    logger.info("No unresolved merge conflicts detected in critical files.")
    return True


def check_required_components() -> bool:
    """Check for required components and configurations."""
    issues = []

    # Check Python version
    current_version = sys.version_info[:2]
    if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
        issues.append(f"Python version {current_version} is not compatible. Required: {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}-{PYTHON_MAX_VERSION[0]}.{PYTHON_MAX_VERSION[1]}")

    # Check key directories
    required_dirs = ["backend", "client", "shared", "tests"]
    for dir_name in required_dirs:
        if not (ROOT_DIR / dir_name).exists():
            issues.append(f"Required directory '{dir_name}' is missing.")

    # Check key files
    required_files = ["pyproject.toml", "README.md", "requirements.txt"]
    for file_name in required_files:
        if not (ROOT_DIR / file_name).exists():
            issues.append(f"Required file '{file_name}' is missing.")

    # Check AI models directory
    models_dir = ROOT_DIR / "models"
    if not models_dir.exists():
        logger.warning("AI models directory not found. Creating it...")
        try:
            models_dir.mkdir(parents=True, exist_ok=True)
            logger.info("AI models directory created successfully.")
        except Exception as e:
            logger.error(f"Failed to create models directory: {e}")
            issues.append("Failed to create models directory")

    if issues:
        for issue in issues:
            logger.error(issue)
        return False

    logger.info("All required components are present.")
    return True


def validate_environment() -> bool:
    """Run comprehensive environment validation."""
    logger.info("Running environment validation...")

    if not check_for_merge_conflicts():
        return False

    if not check_required_components():
        return False

    logger.info("Environment validation passed.")
    return True


# --- Input Validation ---
def validate_port(port: int) -> int:
    """Validate port number is within valid range."""
    if not 1 <= port <= 65535:
        raise ValueError(f"Invalid port: {port}. Port must be between 1 and 65535.")
    return port


def validate_host(host: str) -> str:
    """Validate host name/address format."""
    import re

    if not re.match(r"^[a-zA-Z0-9.-]+$", host):
        raise ValueError(f"Invalid host: {host}")
    return host


# --- Conda Environment Support ---
def is_conda_available() -> bool:
    """Check if conda is available on the system."""
    try:
        result = subprocess.run(
            ["conda", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_conda_env_info():
    """Get information about the current conda environment."""
    env_vars = os.environ
    conda_default_env = env_vars.get("CONDA_DEFAULT_ENV")
    conda_prefix = env_vars.get("CONDA_PREFIX")

    return {
        "is_active": conda_default_env is not None,
        "env_name": conda_default_env,
        "prefix": conda_prefix,
        "python_exe": env_vars.get("CONDA_PREFIX", "") + "/python" if conda_prefix else None
    }


def activate_conda_env(env_name: str = None) -> bool:
    """Activate a conda environment."""
    env_name = env_name or CONDA_ENV_NAME

    # Validate environment name to prevent command injection
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+$', env_name):
        logger.error(f"Invalid conda environment name: {env_name}. Only alphanumeric characters, hyphens, and underscores are allowed.")
        return False

    if not is_conda_available():
        logger.debug("Conda not available, skipping environment activation.")
        return False

    conda_info = get_conda_env_info()
    if conda_info["is_active"]:
        logger.info(f"Already in conda environment: {conda_info['env_name']}")
        return True

    # Check if the requested environment exists
    try:
        result = subprocess.run(
            ["conda", "info", "--envs"],
            capture_output=True,
            text=True,
            check=True
        )
        envs = result.stdout.strip().split('\n')
        env_names = [line.split()[0] for line in envs if line.strip() and not line.startswith('#')]
        if env_name not in env_names:
            logger.warning(f"Conda environment '{env_name}' not found.")
            return False
    except subprocess.CalledProcessError as e:
        logger.warning(f"Failed to list conda environments: {e}")
        return False

    logger.info(f"Will use conda environment: {env_name}")
    # We don't actually activate the environment here since subprocess.run
    # cannot persist environment changes. Instead, we rely on get_python_executable()
    # to find the correct Python executable for the environment.
    return True


def get_python_executable() -> str:
    """Get the appropriate Python executable (conda > venv > system)."""
    # Check if we're in a conda environment
    conda_info = get_conda_env_info()
    if conda_info["is_active"] and conda_info["python_exe"]:
        python_exe = conda_info["python_exe"]
        if platform.system() == "Windows":
            python_exe += ".exe"
        if os.path.exists(python_exe):
            logger.info(f"Using conda Python: {python_exe}")
            return python_exe

    # Check for venv
    venv_path = ROOT_DIR / VENV_DIR
    if venv_path.exists():
        python_exe = get_venv_executable(venv_path, "python")
        if python_exe.exists():
            logger.info(f"Using venv Python: {python_exe}")
            return str(python_exe)

    # Fall back to system Python
    logger.info("Using system Python")
    return sys.executable

# --- Helper Functions ---
def get_venv_executable(venv_path: Path, executable: str) -> Path:
    """Get the path to a specific executable in the virtual environment."""
    scripts_dir = "Scripts" if platform.system() == "Windows" else "bin"
    return venv_path / scripts_dir / (f"{executable}.exe" if platform.system() == "Windows" else executable)

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
    if venv_path.exists() and recreate:
        logger.info("Removing existing virtual environment.")
        shutil.rmtree(venv_path)
    if not venv_path.exists():
        logger.info("Creating virtual environment.")
        venv.create(venv_path, with_pip=True, upgrade_deps=True)

def install_package_manager(venv_path: Path, manager: str):
    python_exe = get_venv_executable(venv_path, "python")
    run_command([str(python_exe), "-m", "pip", "install", manager], f"Installing {manager}")

def setup_dependencies(venv_path: Path, use_poetry: bool = False):
    python_exe = get_python_executable()

    if use_poetry:
        # For poetry, we need to install it first if not available
        try:
            subprocess.run([python_exe, "-c", "import poetry"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            run_command([python_exe, "-m", "pip", "install", "poetry"], "Installing Poetry")

        run_command([python_exe, "-m", "poetry", "install", "--with", "dev"], "Installing dependencies with Poetry", cwd=ROOT_DIR)
    else:
        # For uv, install if not available
        try:
            subprocess.run([python_exe, "-c", "import uv"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            run_command([python_exe, "-m", "pip", "install", "uv"], "Installing uv")

        run_command([python_exe, "-m", "uv", "pip", "install", "-e", ".[dev]", "--exclude", "notmuch"], "Installing dependencies with uv (excluding notmuch)", cwd=ROOT_DIR)

        # Install notmuch with version matching system
        install_notmuch_matching_system()

def install_notmuch_matching_system():
    try:
        result = subprocess.run(["notmuch", "--version"], capture_output=True, text=True, check=True)
        version_line = result.stdout.strip()
        # Parse version, e.g., "notmuch 0.38.3"
        version = version_line.split()[1]
        major_minor = '.'.join(version.split('.')[:2])  # e.g., 0.38
        python_exe = get_python_executable()
        run_command([python_exe, "-m", "pip", "install", f"notmuch=={major_minor}"], f"Installing notmuch {major_minor} to match system")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("notmuch not found on system, skipping version-specific install")

def download_nltk_data(venv_path=None):
    python_exe = get_python_executable()

    # Updated NLTK download script with better error handling and more packages
    nltk_download_script = """
try:
    import nltk
    # Download essential NLTK packages
    packages = ['punkt', 'punkt_tab', 'stopwords', 'wordnet', 'averaged_perceptron_tagger', 'vader_lexicon', 'omw-1.4']
    for package in packages:
        try:
            nltk.download(package, quiet=True)
            print(f"Downloaded NLTK package: {package}")
        except Exception as e:
            print(f"Failed to download {package}: {e}")
    print("NLTK data download completed.")
except ImportError:
    print("NLTK not available, skipping download.")
except Exception as e:
    print(f"NLTK download failed: {e}")
"""

    logger.info("Downloading NLTK data...")
    result = subprocess.run(
        [python_exe, "-c", nltk_download_script], cwd=ROOT_DIR, capture_output=True, text=True
    )
    if result.returncode != 0:
        logger.error(f"Failed to download NLTK data: {result.stderr}")
        # This might fail in some environments but it's not critical for basic operation
        logger.warning("NLTK data download failed, but continuing setup...")
    else:
        logger.info("NLTK data downloaded successfully.")

    # Download TextBlob corpora with improved error handling
    textblob_download_script = """
try:
    from textblob import download_corpora
    download_corpora()
    print("TextBlob corpora download completed.")
except ImportError:
    print("TextBlob not available, skipping corpora download.")
except Exception as e:
    print(f"TextBlob corpora download failed: {e}")
"""

    logger.info("Downloading TextBlob corpora...")
    result = subprocess.run(
        [python_exe, "-c", textblob_download_script], cwd=ROOT_DIR, capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        logger.warning(f"TextBlob corpora download failed: {result.stderr}")
        logger.warning("Continuing setup without TextBlob corpora...")
    else:
        logger.info("TextBlob corpora downloaded successfully.")


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

    # Install Node.js dependencies if node_modules doesn't exist
    node_modules_path = ROOT_DIR / "client" / "node_modules"
    if not node_modules_path.exists():
        logger.info("Installing Node.js dependencies...")


def start_server_ts():
    """Start the TypeScript backend server."""
    logger.info("Starting TypeScript backend server...")
    # Check if npm is available
    if not shutil.which("npm"):
        logger.warning("npm not found. Skipping TypeScript backend server startup.")
        return None

    # Check if package.json exists
    pkg_json_path = ROOT_DIR / "server" / "package.json"
    if not pkg_json_path.exists():
        logger.debug("No package.json in 'server/', skipping TypeScript backend server startup.")
        return None

    # Install Node.js dependencies if node_modules doesn't exist
    node_modules_path = ROOT_DIR / "server" / "node_modules"
    if not node_modules_path.exists():
        logger.info("Installing TypeScript server dependencies...")

# --- Service Startup Functions ---
def start_backend(host: str, port: int, debug: bool = False):
    """Start the backend service."""
    # Validate inputs to prevent command injection
    try:
        # Allow localhost, 127.0.0.1, or valid IP addresses
        if host not in ["localhost", "127.0.0.1", "0.0.0.0"]:
            import ipaddress
            ipaddress.ip_address(host)  # Validates IP format
        if not (1 <= port <= 65535):
            raise ValueError("Port out of range")
    except ValueError as e:
        logger.error(f"Invalid host or port: {e}")
        return

python_exe = get_python_executable()
cmd = [python_exe, "-m", "uvicorn", "src.main:create_app", "--factory", "--host", host, "--port", str(port)]
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

def setup_node_dependencies(service_path: Path, service_name: str):
    """Install npm dependencies for a Node.js service."""
    if not (service_path / "package.json").exists():
        logger.warning(f"package.json not found for {service_name}, skipping dependency installation.")
        return
    logger.info(f"Installing npm dependencies for {service_name}...")
    run_command(["npm", "install"], f"Installing {service_name} dependencies", cwd=service_path)

def start_gradio_ui(host, port, share, debug):
    logger.info("Starting Gradio UI...")
    python_exe = get_python_executable()
    cmd = [python_exe, "-m", "src.main"] # Assuming Gradio is launched from main
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
    # For Conda, we assume the environment is already set up
        # Could add Conda environment creation here in the future
        logger.info("Using Conda environment - assuming dependencies are already installed")
    else:
        # Use venv
        create_venv(venv_path, args.force_recreate_venv)
        install_package_manager(venv_path, "uv")
        setup_dependencies(venv_path, False)
        if not args.no_download_nltk:
            download_nltk_data(venv_path)

        # Setup Node.js dependencies
        setup_node_dependencies(ROOT_DIR / "client", "Frontend Client")
        setup_node_dependencies(ROOT_DIR / "backend" / "server-ts", "TypeScript Backend")
    logger.info("Setup complete.")

def prepare_environment(args):
    """Prepares the environment for running the application."""
    if not args.no_venv:
        # Try conda first
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
        results.append(test_stages.run_security_tests(target_url=f"http://{args.host}:{args.port}", debug=args.debug))

    # If no specific test type is selected, run a default set (e.g., unit and integration)
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
    import platform
    import sys

    print("=== System Information ===")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")

    print("\\n=== Project Information ===")
    print(f"Project Root: {ROOT_DIR}")
    print(f"Python Path: {os.environ.get('PYTHONPATH', 'Not set')}")

    print("\\n=== Environment Status ===")
    venv_path = ROOT_DIR / VENV_DIR
    if venv_path.exists():
        print(f"Virtual Environment: {venv_path} (exists)")
        python_exe = get_venv_executable(venv_path, "python")
        if python_exe.exists():
            print(f"Venv Python: {python_exe}")
        else:
            print("Venv Python: Not found")
    else:
        print(f"Virtual Environment: {venv_path} (not created)")

    conda_available = is_conda_available()
    print(f"Conda Available: {conda_available}")
    if conda_available:
        conda_env = os.environ.get('CONDA_DEFAULT_ENV', 'None')
        print(f"Current Conda Env: {conda_env}")

    node_available = check_node_npm_installed()
    print(f"Node.js/npm Available: {node_available}")

    print("\\n=== Configuration Files ===")
    config_files = [
        "pyproject.toml", "requirements.txt", "requirements-dev.txt",
        "package.json", "launch-user.env", ".env"
    ]
    for cf in config_files:
        exists = (ROOT_DIR / cf).exists()
        print(f"{cf}: {'Found' if exists else 'Not found'}")

async def main_async():
    """Main entry point with async support for new Command pattern."""
    # Initialize services
    initialize_services()

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="EmailIntelligence Unified Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch.py setup                    # Set up environment
  python launch.py run                      # Run all services
  python launch.py test --coverage          # Run tests with coverage
  python launch.py --setup                  # Legacy setup mode
  python launch.py --port 8001              # Legacy run mode
        """
    )

    # Add subcommands for new Command pattern
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Set up the environment')
    setup_parser.add_argument('--recreate-venv', action='store_true', help='Recreate virtual environment')
    setup_parser.add_argument('--use-poetry', action='store_true', help='Use Poetry instead of uv/pip')
    setup_parser.add_argument('--skip-nltk', action='store_true', help='Skip NLTK data download')

    # Run command
    run_parser = subparsers.add_parser('run', help='Run the application')
    run_parser.add_argument('--backend-only', action='store_true', help='Run only backend')
    run_parser.add_argument('--ui-only', action='store_true', help='Run only UI')
    run_parser.add_argument('--api-only', action='store_true', help='Run only API')
    run_parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    run_parser.add_argument('--backend-port', type=int, default=8000, help='Backend port')
    run_parser.add_argument('--gradio-port', type=int, default=7860, help='Gradio UI port')
    run_parser.add_argument('--node-port', type=int, default=3000, help='Node.js API port')
    run_parser.add_argument('--no-health-check', action='store_true', help='Disable health monitoring')
    run_parser.add_argument('--detach', action='store_true', help='Run in background')

    # Test command
    test_parser = subparsers.add_parser('test', help='Run tests')
    test_parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    test_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    test_parser.add_argument('--fail-fast', '-x', action='store_true', help='Stop on first failure')
    test_parser.add_argument('--pattern', '-k', help='Run tests matching pattern')

    # Legacy arguments for backward compatibility
    parser.add_argument("--setup", action="store_true", help="Run environment setup (legacy).")
    parser.add_argument("--force-recreate-venv", action="store_true", help="Force recreation of the venv (legacy).")
    parser.add_argument("--use-conda", action="store_true", help="Use Conda environment instead of venv (legacy).")
    parser.add_argument("--conda-env", type=str, default="base", help="Conda environment name (legacy).")
    parser.add_argument("--no-venv", action="store_true", help="Don't create or use a virtual environment (legacy).")
    parser.add_argument("--update-deps", action="store_true", help="Update dependencies before launching (legacy).")
    parser.add_argument("--skip-torch-cuda-test", action="store_true", help="Skip CUDA availability test (legacy).")
    parser.add_argument("--reinstall-torch", action="store_true", help="Reinstall PyTorch (legacy).")
    parser.add_argument("--skip-python-version-check", action="store_true", help="Skip Python version check (legacy).")
    parser.add_argument("--no-download-nltk", action="store_true", help="Skip downloading NLTK data (legacy).")
    parser.add_argument("--skip-prepare", action="store_true", help="Skip all environment preparation steps (legacy).")
    parser.add_argument("--loglevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO', help="Set the logging level.")
    parser.add_argument("--stage", choices=['dev', 'test'], default='dev', help="Specify the application mode (legacy).")
    parser.add_argument("--port", type=int, default=8000, help="Specify the port to run on (legacy).")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Specify the host to run on (legacy).")
    parser.add_argument("--frontend-port", type=int, default=5173, help="Specify the frontend port (legacy).")
    parser.add_argument("--api-url", type=str, help="Specify the API URL for the frontend (legacy).")
    parser.add_argument("--api-only", action="store_true", help="Run only the API server (legacy).")
    parser.add_argument("--frontend-only", action="store_true", help="Run only the frontend (legacy).")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode (legacy).")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report (legacy).")
    parser.add_argument("--unit", action="store_true", help="Run unit tests (legacy).")
    parser.add_argument("--integration", action="store_true", help="Run integration tests (legacy).")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests (legacy).")
    parser.add_argument("--performance", action="store_true", help="Run performance tests (legacy).")
    parser.add_argument("--security", action="store_true", help="Run security tests (legacy).")
    parser.add_argument("--system-info", action="store_true", help="Print system information (legacy).")

    args = parser.parse_args()

    # Setup basic environment
    setup_wsl_environment()
    check_wsl_requirements()

    if not args.skip_python_version_check:
        check_python_version()

    logging.getLogger().setLevel(args.loglevel)

    # Load environment variables
    if DOTENV_AVAILABLE:
        user_env_file = ROOT_DIR / "launch-user.env"
        if user_env_file.exists():
            load_dotenv(user_env_file)
            logger.info(f"Loaded user environment variables from {user_env_file}")

        env_file = getattr(args, 'env_file', None) or ".env"
        if os.path.exists(env_file):
            load_dotenv(env_file)

    # Determine which execution path to take
    if args.command:
        # New Command pattern path
        await execute_command(args.command, args)
    else:
        # Legacy backward compatibility path
        await execute_legacy_mode(args)


async def execute_command(command_name: str, args):
    """Execute a command using the new Command pattern."""
    try:
        # Initialize all services
        await initialize_all_services()

        # Get command factory and create command
        factory = get_command_factory()
        command = factory.create_command(command_name, args)

        if not command:
            logger.error(f"Unknown command: {command_name}")
            logger.info("Available commands:")
            for name, cls in factory.get_available_commands().items():
                logger.info(f"  {name}: {cls().description}")
            sys.exit(1)

        # Execute command
        result = await command.execute()

        # Handle result
        if result.success:
            if result.data:
                logger.info(f"Command completed: {result.message}")
            else:
                logger.info(result.message)
        else:
            logger.error(f"Command failed: {result.message}")
            sys.exit(result.exit_code)

    except Exception as e:
        logger.error(f"Command execution failed: {e}")
        sys.exit(1)
    finally:
        await cleanup_all_services()


async def execute_legacy_mode(args):
    """Execute in legacy mode for backward compatibility."""
    logger.info("Running in legacy compatibility mode")

    # Setup WSL environment if applicable (early setup)
    setup_wsl_environment()
    check_wsl_requirements()

    if not args.skip_python_version_check:
        check_python_version()

    logging.getLogger().setLevel(args.loglevel)

    # Validate environment if not skipping preparation
    if not args.skip_prepare and not validate_environment():
        sys.exit(1)

    # Validate input arguments
    try:
        args.port = validate_port(args.port)
        args.host = validate_host(args.host)
        if hasattr(args, 'frontend_port'):
            args.frontend_port = validate_port(args.frontend_port)
    except ValueError as e:
        logger.error(f"Input validation failed: {e}")
        sys.exit(1)

    if args.setup:
        venv_path = ROOT_DIR / VENV_DIR
        handle_setup(args, venv_path)
        return

    # Handle Conda environment if requested
    if args.use_conda:
        if not is_conda_available():
            logger.error("Conda is not available. Please install Conda or use venv.")
            sys.exit(1)
        if not get_conda_env_info()["is_active"] and not activate_conda_env(args.conda_env):
            logger.error(f"Failed to activate Conda environment: {args.conda_env}")
            sys.exit(1)
        elif get_conda_env_info()["is_active"]:
            logger.info(f"Using existing Conda environment: {os.environ.get('CONDA_DEFAULT_ENV')}")

    if not args.skip_prepare and not args.use_conda:
        prepare_environment(args)

    if args.system_info:
        print_system_info()
        return

    # Stage-specific logic
    if args.stage == 'test':
        handle_test_stage(args)
        return

    # Service startup logic
    start_services(args)

    logger.info("All services started. Press Ctrl+C to shut down.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutdown signal received.")
    finally:
        process_manager.cleanup()


def main():
    """Main entry point - wraps async main for compatibility."""
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
