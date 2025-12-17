#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

This script provides a unified entry point for setting up and running the EmailIntelligence application.
It supports both legacy arguments for backward compatibility and modern command-based interface.

Features:
- Environment setup with virtual environment management
- Service startup (backend, frontend, TypeScript server, Gradio UI)
- Test execution with multiple test types
- Orchestration validation checks
- System information display
- Cross-platform support (Linux, macOS, Windows, WSL)
"""

# Import launch system modules
from setup.validation import (
    check_python_version, check_for_merge_conflicts, check_required_components,
    validate_environment, validate_port, validate_host
)
from setup.services import (
    start_services, start_backend, start_node_service, start_gradio_ui, validate_services
)
from setup.environment import (
    handle_setup, prepare_environment, setup_wsl_environment, check_wsl_requirements
)
from setup.utils import print_system_info, process_manager

# Import test stages
from setup.test_stages import test_stages

# Standard library imports
import argparse
import atexit
import os
import platform
import shutil
import subprocess
import sys
import threading
import time
import venv
from pathlib import Path
from typing import List

# Import project configuration
from setup.project_config import get_project_config

# Import command pattern components (with error handling for refactors)
try:
    from setup.commands.command_factory import get_command_factory
    from setup.container import get_container, initialize_all_services
except ImportError as e:
    # Command pattern not available, will use legacy mode
    get_command_factory = None
    get_container = None
    initialize_all_services = None

try:
    from dotenv import load_dotenv

    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    load_dotenv = None  # Will be loaded later if needed

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")


# --- Global state ---
ROOT_DIR = get_project_config().root_dir

# Import process manager from utils
from setup.utils import process_manager

# --- Constants ---
PYTHON_MIN_VERSION = (3, 12)
PYTHON_MAX_VERSION = (3, 13)
VENV_DIR = "venv"
CONDA_ENV_NAME = os.getenv("CONDA_ENV_NAME", "base")




def setup_wsl_environment():
    """Setup WSL-specific environment variables if in WSL"""
    if not is_wsl():
        return

    # Set display for GUI applications
    if "DISPLAY" not in os.environ:
        os.environ["DISPLAY"] = ":0"

    # Set matplotlib backend for WSL
    os.environ["MPLBACKEND"] = "Agg"

    # Optimize for WSL performance
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ["PYTHONUNBUFFERED"] = "1"

    # Set OpenGL for WSL
    os.environ["LIBGL_ALWAYS_INDIRECT"] = "1"

    logger.info("🐧 WSL environment detected - applied optimizations")


def check_wsl_requirements():
    """Check WSL-specific requirements and warn if needed"""
    if not is_wsl():
        return

    # Check if X11 server is accessible (optional check)
    try:
        result = subprocess.run(["xset", "-q"], capture_output=True, timeout=2)
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
        logger.error(
            f"Python version {platform.python_version()} is not compatible. "
            f"Please use Python version {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]} "
            f"to {PYTHON_MAX_VERSION[0]}.{PYTHON_MAX_VERSION[1]}."
        )
        sys.exit(1)
    logger.info(f"Python version {platform.python_version()} is compatible.")


# --- Environment Validation ---
# check_for_merge_conflicts is imported from setup.validation


def check_required_components() -> bool:
    """Check for required components and configurations."""
    issues = []

    # Check Python version
    current_version = sys.version_info[:2]
    if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
        issues.append(
            f"Python version {current_version} is not compatible. Required: {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}-{PYTHON_MAX_VERSION[0]}.{PYTHON_MAX_VERSION[1]}"
        )

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


def check_critical_files() -> bool:
    """Check for critical files that must exist in the orchestration-tools branch."""
    # Critical files that are essential for orchestration
    critical_files = [
        # Core orchestration scripts
        "scripts/install-hooks.sh",
        "scripts/cleanup_orchestration.sh",
        "scripts/sync_setup_worktrees.sh",
        "scripts/reverse_sync_orchestration.sh",
        
        # Git hooks
        "scripts/hooks/pre-commit",
        "scripts/hooks/post-commit",
        "scripts/hooks/post-commit-setup-sync",
        "scripts/hooks/post-merge",
        "scripts/hooks/post-checkout",
        "scripts/hooks/post-push",
        
        # Shared libraries
        "scripts/lib/common.sh",
        "scripts/lib/error_handling.sh",
        "scripts/lib/git_utils.sh",
        "scripts/lib/logging.sh",
        "scripts/lib/validation.sh",
        
        # Setup files
        "setup/launch.py",
        "setup/pyproject.toml",
        "setup/requirements.txt",
        "setup/requirements-dev.txt",
        "setup/setup_environment_system.sh",
        "setup/setup_environment_wsl.sh",
        "setup/setup_python.sh",
        
        # Configuration files
        ".flake8",
        ".pylintrc",
        ".gitignore",
        ".gitattributes",
        
        # Root wrapper
        "launch.py",
        
        # Deployment files
        "deployment/deploy.py",
        "deployment/test_stages.py",
        "deployment/docker-compose.yml",
    ]
    
    # Critical directories that must exist
    critical_directories = [
        "scripts/",
        "scripts/hooks/",
        "scripts/lib/",
        "setup/",
        "deployment/",
        "docs/",
    ]
    
    # Orchestration documentation files
    orchestration_docs = [
        "docs/orchestration_summary.md",
        "docs/orchestration_validation_tests.md",
        "docs/orchestration_hook_management.md",
        "docs/orchestration_branch_scope.md",
        "docs/env_management.md",
        "docs/git_workflow_plan.md",
        "docs/current_orchestration_docs/",
        "docs/guides/",
    ]
    
    missing_files = []
    missing_dirs = []
    
    # Check for missing critical files
    for file_path in critical_files:
        full_path = ROOT_DIR / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    # Check for missing critical directories
    for dir_path in critical_directories:
        full_path = ROOT_DIR / dir_path
        if not full_path.exists():
            missing_dirs.append(dir_path)
    
    # Check for missing orchestration documentation
    for doc_path in orchestration_docs:
        full_path = ROOT_DIR / doc_path
        if not full_path.exists():
            missing_files.append(doc_path)
    
    if missing_files or missing_dirs:
        if missing_files:
            logger.error("Missing critical files:")
            for file_path in missing_files:
                logger.error(f"  - {file_path}")
        if missing_dirs:
            logger.error("Missing critical directories:")
            for dir_path in missing_dirs:
                logger.error(f"  - {dir_path}")
        logger.error("Please restore these critical files for proper orchestration functionality.")
        return False
    
    logger.info("All critical files are present.")
    return True


def validate_orchestration_environment() -> bool:
    """Run comprehensive validation for the orchestration-tools branch."""
    logger.info("Running orchestration environment validation...")
    
    # Check for merge conflicts first
    if not check_for_merge_conflicts():
        return False
    
    # Check critical files
    if not check_critical_files():
        return False
    
    logger.info("Orchestration environment validation passed.")
    return True


# --- Input Validation ---













    if not is_conda_available():
        if env_name:
            logger.warning(f"Conda not available, cannot activate environment '{env_name}'. Please install Conda.")
        else:
            logger.debug("Conda not available, skipping environment activation.")
        return False

    conda_info = get_conda_env_info()
    if conda_info["is_active"]:
        if conda_info["env_name"] == env_name:
            logger.info(f"Already in specified conda environment: {conda_info['env_name']}")
            return True
        else:
            logger.warning(
                f"Currently in conda environment '{conda_info['env_name']}', "
                f"but '{env_name}' was requested. "
                f"Please activate '{env_name}' manually before running the script."
            )
            return False









# --- Helper Functions ---
def get_venv_executable(venv_path: Path, executable: str) -> Path:
    """Get the path to a specific executable in the virtual environment."""
    scripts_dir = "Scripts" if platform.system() == "Windows" else "bin"
    return (
        venv_path
        / scripts_dir
        / (f"{executable}.exe" if platform.system() == "Windows" else executable)
    )


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
    run_command([python_exe, "-m", "pip", "install", manager], f"Installing {manager}")


def setup_dependencies(venv_path: Path, use_poetry: bool = False):
    python_exe = get_python_executable()

    if use_poetry:
        # Ensure pip is up-to-date before installing other packages
        run_command([python_exe, "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip")
        # For poetry, we need to install it first if not available
        try:
            subprocess.run([python_exe, "-c", "import poetry"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            run_command([python_exe, "-m", "pip", "install", "poetry"], "Installing Poetry")

        run_command(
            [python_exe, "-m", "poetry", "install", "--with", "dev"],
            "Installing dependencies with Poetry",
            cwd=ROOT_DIR,
        )
    else:
        # Ensure pip is up-to-date before installing other packages
        run_command([python_exe, "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip")
        # For uv, install if not available
        try:
            subprocess.run([python_exe, "-c", "import uv"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            run_command([python_exe, "-m", "pip", "install", "uv"], "Installing uv")

        run_command(
            [python_exe, "-m", "uv", "pip", "install", "-e", ".[dev]", "--exclude", "notmuch"],
            "Installing dependencies with uv (excluding notmuch)",
            cwd=ROOT_DIR,
        )

        # Install notmuch with version matching system
        install_notmuch_matching_system()


def install_notmuch_matching_system():
    try:
        result = subprocess.run(
            ["notmuch", "--version"], capture_output=True, text=True, check=True
        )
        version_line = result.stdout.strip()
        # Parse version, e.g., "notmuch 0.38.3"
        version = version_line.split()[1]
        major_minor = ".".join(version.split(".")[:2])  # e.g., 0.38
        python_exe = get_python_executable()
        run_command(
            [python_exe, "-m", "pip", "install", f"notmuch=={major_minor}"],
            f"Installing notmuch {major_minor} to match system",
        )
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
        [python_exe, "-c", textblob_download_script],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        timeout=120,
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
    pkg_json_path = ROOT_DIR / "backend" / "server-ts" / "package.json"
    if not pkg_json_path.exists():
        logger.debug(
            "No package.json in 'backend/server-ts/', skipping TypeScript backend server startup."
        )
        return None

    # Install Node.js dependencies if node_modules doesn't exist
    node_modules_path = ROOT_DIR / "backend" / "server-ts" / "node_modules"
    if not node_modules_path.exists():
        logger.info("Installing TypeScript server dependencies...")


# --- Service Startup Functions ---
def start_backend(host: str, port: int, debug: bool = False):
    python_exe = get_python_executable()
    cmd = [
        python_exe,
        "-m",
        "uvicorn",
        "src.main:create_app",
        "--factory",
        "--host",
        host,
        "--port",
        str(port),
    ]
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
        logger.warning(
            f"package.json not found for {service_name}, skipping dependency installation."
        )
        return
    logger.info(f"Installing npm dependencies for {service_name}...")
    run_command(["npm", "install"], f"Installing {service_name} dependencies", cwd=service_path)


def start_gradio_ui(host, port, share, debug):
    logger.info("Starting Gradio UI...")
    python_exe = get_python_executable()
    cmd = [python_exe, "-m", "src.main"]  # Assuming Gradio is launched from main
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
        results.append(
            test_stages.run_security_tests(
                target_url=f"http://{args.host}:{args.port}", debug=args.debug
            )
        )

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

    print("\n=== Project Information ===")
    print(f"Project Root: {ROOT_DIR}")
    print(f"Python Path: {os.environ.get('PYTHONPATH', 'Not set')}")

    print("\n=== Environment Status ===")
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
        conda_env = os.environ.get("CONDA_DEFAULT_ENV", "None")
        print(f"Current Conda Env: {conda_env}")

    node_available = check_node_npm_installed()
    print(f"Node.js/npm Available: {node_available}")

    print("\n=== Configuration Files ===")
    config_files = [
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
        "package.json",
        "launch-user.env",
        ".env",
    ]
    for cf in config_files:
        exists = (ROOT_DIR / cf).exists()
        print(f"{cf}: {'Found' if exists else 'Not found'}")


def main():
    # Initialize services if command pattern is available
    if COMMAND_PATTERN_AVAILABLE and initialize_all_services and get_container:
        initialize_all_services(get_container())

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="EmailIntelligence Unified Launcher")

    # Add subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Set up the development environment")
    _add_common_args(setup_parser)

    # Run command
    run_parser = subparsers.add_parser("run", help="Run the EmailIntelligence application")
    _add_common_args(run_parser)
    run_parser.add_argument("--dev", action="store_true", help="Run in development mode")

    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests")
    _add_common_args(test_parser)
    test_parser.add_argument("--unit", action="store_true", help="Run unit tests")
    test_parser.add_argument("--integration", action="store_true", help="Run integration tests")
    test_parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    test_parser.add_argument("--performance", action="store_true", help="Run performance tests")
    test_parser.add_argument("--security", action="store_true", help="Run security tests")
    test_parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    test_parser.add_argument(
        "--continue-on-error", action="store_true", help="Continue running tests even if some fail"
    )

    # Check command for orchestration-tools branch
    check_parser = subparsers.add_parser("check", help="Run checks for orchestration environment")
    _add_common_args(check_parser)
    check_parser.add_argument("--critical-files", action="store_true", help="Check for critical orchestration files")
    check_parser.add_argument("--env", action="store_true", help="Check orchestration environment")

    # Legacy argument parsing for backward compatibility
    parser.add_argument("--setup", action="store_true", help="Set up the environment (legacy)")
    parser.add_argument(
        "--stage", choices=["dev", "test"], default="dev", help="Application mode (legacy)"
    )

    # Environment Setup
    parser.add_argument(
        "--force-recreate-venv", action="store_true", help="Force recreation of the venv."
    )

    parser.add_argument(
        "--use-conda", action="store_true", help="Use Conda environment instead of venv."
    )
    parser.add_argument(
        "--conda-env",
        type=str,
        default="base",
        help="Conda environment name to use (default: base).",
    )
    parser.add_argument(
        "--no-venv", action="store_true", help="Don't create or use a virtual environment."
    )
    parser.add_argument(
        "--update-deps", action="store_true", help="Update dependencies before launching."
    )
    parser.add_argument(
        "--skip-torch-cuda-test",
        action="store_true",
        help="Skip CUDA availability test for PyTorch.",
    )
    parser.add_argument("--reinstall-torch", action="store_true", help="Reinstall PyTorch.")
    parser.add_argument(
        "--skip-python-version-check", action="store_true", help="Skip Python version check."
    )
    parser.add_argument(
        "--no-download-nltk", action="store_true", help="Skip downloading NLTK data."
    )
    parser.add_argument(
        "--skip-prepare", action="store_true", help="Skip all environment preparation steps."
    )
    parser.add_argument(
        "--loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level.",
    )

    # Application Stage

    # Server Configuration
    parser.add_argument("--port", type=int, default=8000, help="Specify the port to run on.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Specify the host to run on.")
    parser.add_argument(
        "--frontend-port", type=int, default=5173, help="Specify the frontend port to run on."
    )
    parser.add_argument("--api-url", type=str, help="Specify the API URL for the frontend.")
    parser.add_argument(
        "--api-only", action="store_true", help="Run only the API server without the frontend."
    )
    parser.add_argument(
        "--frontend-only", action="store_true", help="Run only the frontend without the API server."
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")

    args = parser.parse_args()

    # Handle command pattern vs legacy arguments
    if args.command:
        # Use command pattern
        return _execute_command(args.command, args)
    else:
        # Handle legacy arguments
        return _handle_legacy_args(args)


def _add_common_args(parser):
    """Add common arguments to subcommand parsers."""
    parser.add_argument(
        "--loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level.",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")


def _add_legacy_args(parser):
    """Add legacy arguments for backward compatibility."""
    # Environment Setup
    parser.add_argument(
        "--force-recreate-venv", action="store_true", help="Force recreation of the venv."
    )
    parser.add_argument(
        "--use-conda", action="store_true", help="Use Conda environment instead of venv."
    )
    parser.add_argument(
        "--conda-env",
        type=str,
        default="base",
        help="Conda environment name to use (default: base).",
    )
    parser.add_argument(
        "--no-venv", action="store_true", help="Don't create or use a virtual environment."
    )
    parser.add_argument(
        "--update-deps", action="store_true", help="Update dependencies before launching."
    )
    parser.add_argument(
        "--skip-torch-cuda-test",
        action="store_true",
        help="Skip CUDA availability test for PyTorch.",
    )
    parser.add_argument("--reinstall-torch", action="store_true", help="Reinstall PyTorch.")
    parser.add_argument(
        "--skip-python-version-check", action="store_true", help="Skip Python version check."
    )
    parser.add_argument(
        "--no-download-nltk", action="store_true", help="Skip downloading NLTK data."
    )
    parser.add_argument(
        "--skip-prepare", action="store_true", help="Skip all environment preparation steps."
    )

    # Application Configuration
    parser.add_argument("--port", type=int, default=8000, help="Specify the port to run on.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Specify the host to run on.")
    parser.add_argument(
        "--frontend-port", type=int, default=5173, help="Specify the frontend port to run on."
    )
    parser.add_argument("--api-url", type=str, help="Specify the API URL for the frontend.")
    parser.add_argument(
        "--api-only", action="store_true", help="Run only the API server without the frontend."
    )
    parser.add_argument(
        "--frontend-only", action="store_true", help="Run only the frontend without the API server."
    )

    # Testing Options
    parser.add_argument(
        "--coverage", action="store_true", help="Generate coverage report when running tests."
    )
    parser.add_argument("--unit", action="store_true", help="Run unit tests.")
    parser.add_argument("--integration", action="store_true", help="Run integration tests.")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests.")
    parser.add_argument("--performance", action="store_true", help="Run performance tests.")
    parser.add_argument("--security", action="store_true", help="Run security tests.")

    # Extensions and Models
    parser.add_argument("--skip-extensions", action="store_true", help="Skip loading extensions.")
    parser.add_argument("--skip-models", action="store_true", help="Skip downloading models.")

    # Advanced Options
    parser.add_argument(
        "--system-info", action="store_true", help="Print system information then exit."
    )
    parser.add_argument("--env-file", type=str, help="Specify environment file to load.")
    parser.add_argument("--share", action="store_true", help="Create a public URL.")
    parser.add_argument("--listen", action="store_true", help="Make the server listen on network.")
    parser.add_argument(
        "--ngrok", type=str, help="Use ngrok to create a tunnel, specify ngrok region."
    )


def main():
    # Check for common setup issues before proceeding
    _check_setup_warnings()

    # Initialize services (only if core modules are available)
    if initialize_all_services and get_container:
        initialize_all_services(get_container())

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="EmailIntelligence Unified Launcher")

    # Add subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Set up the development environment")
    _add_common_args(setup_parser)

    # Run command
    run_parser = subparsers.add_parser("run", help="Run the EmailIntelligence application")
    _add_common_args(run_parser)
    run_parser.add_argument("--dev", action="store_true", help="Run in development mode")

    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests")
    _add_common_args(test_parser)
    test_parser.add_argument("--unit", action="store_true", help="Run unit tests")
    test_parser.add_argument("--integration", action="store_true", help="Run integration tests")
    test_parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    test_parser.add_argument("--performance", action="store_true", help="Run performance tests")
    test_parser.add_argument("--security", action="store_true", help="Run security tests")
    test_parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    test_parser.add_argument(
        "--continue-on-error", action="store_true", help="Continue running tests even if some fail"
    )

    # Legacy argument parsing for backward compatibility
    parser.add_argument("--setup", action="store_true", help="Set up the environment (legacy)")
    parser.add_argument(
        "--stage", choices=["dev", "test"], default="dev", help="Application mode (legacy)"
    )

    # Add all legacy arguments for backward compatibility
    _add_legacy_args(parser)

    args = parser.parse_args()

    # Handle command pattern vs legacy arguments
    if args.command:
        # Use command pattern
        return _execute_command(args.command, args)
    else:
        # Handle legacy arguments
        return _handle_legacy_args(args)


def _execute_command(command_name: str, args) -> int:
    """Execute a command using the command pattern."""
    # Handle check command directly in orchestration-tools branch
    if command_name == "check":
        return _execute_check_command(args)
    
    # For other commands, use command pattern if available
    if COMMAND_PATTERN_AVAILABLE:
        factory = get_command_factory()
        command = factory.create_command(command_name, args)

        if command is None:
            logger.error(f"Unknown command: {command_name}")
            return 1

        try:
            return command.execute()
        finally:
            command.cleanup()
    else:
        logger.error(f"Command pattern not available and '{command_name}' is not a built-in command")
        return 1


def _execute_check_command(args) -> int:
    """Execute the check command for orchestration validation."""
    logger.info("Running orchestration checks...")
    
    success = True
    
    # Run critical files check if requested
    if args.critical_files or (not args.env):
        if not check_critical_files():
            success = False
    
    # Run environment validation if requested
    if args.env:
        if not validate_orchestration_environment():
            success = False
    
    # If no specific check was requested, run all checks
    if not args.critical_files and not args.env:
        if not validate_orchestration_environment():
            success = False
    
    if success:
        logger.info("All orchestration checks passed!")
        return 0
    else:
        logger.error("Orchestration checks failed!")
        return 1


def _handle_legacy_args(args) -> int:
    """Handle legacy argument parsing for backward compatibility."""
    # Setup WSL environment if applicable (early setup)
    from setup.environment import setup_wsl_environment, check_wsl_requirements
    setup_wsl_environment()
    check_wsl_requirements()

    if not args.skip_python_version_check:
        check_python_version()

    logging.getLogger().setLevel(getattr(args, 'loglevel', 'INFO'))

    if DOTENV_AVAILABLE:
        # Load user customizations from launch-user.env if it exists
        user_env_file = ROOT_DIR / "launch-user.env"
        if user_env_file.exists():
            load_dotenv(user_env_file)
            logger.info(f"Loaded user environment variables from {user_env_file}")
        else:
            logger.debug(f"User env file not found: {user_env_file}")

        # Load environment file if specified
        env_file = args.env_file or ".env"
        if os.path.exists(env_file):
            logger.info(f"Loading environment variables from {env_file}")
            load_dotenv(env_file)

    # Set conda environment name if specified
    global CONDA_ENV_NAME
    if args.conda_env and args.conda_env != "base":  # Only if explicitly set to non-default
        CONDA_ENV_NAME = args.conda_env
        args.use_conda = True  # Set flag when conda env is specified
        # args.use_conda remains as set by command line argument

    # Check for system info first (doesn't need validation)
    if args.system_info:
        print_system_info()
        return 0

    # Validate environment if not skipping preparation
    if not args.skip_prepare and not validate_environment():
        return 1

    # Validate input arguments
    try:
        args.port = validate_port(args.port)
        args.host = validate_host(args.host)
        if hasattr(args, "frontend_port"):
            args.frontend_port = validate_port(args.frontend_port)
    except ValueError as e:
        logger.error(f"Input validation failed: {e}")
        return 1

    if args.setup:
        venv_path = ROOT_DIR / VENV_DIR
        handle_setup(args, venv_path)
        return 0

    # Handle Conda environment if requested
    from setup.environment import is_conda_available, get_conda_env_info, activate_conda_env
    if args.use_conda:
        if not is_conda_available():
            logger.error("Conda is not available. Please install Conda or use venv.")
            return 1
        if not get_conda_env_info()["is_active"] and not activate_conda_env(args.conda_env):
            logger.error(f"Failed to activate Conda environment: {args.conda_env}")
            return 1
        elif get_conda_env_info()["is_active"]:
            logger.info(f"Using existing Conda environment: {os.environ.get('CONDA_DEFAULT_ENV')}")

    if not args.skip_prepare and not args.use_conda:
        prepare_environment(args)

    if args.system_info:
        print("DEBUG: system_info flag detected")
        print_system_info()
        return 0

    # Handle test stage
    if hasattr(args, "stage") and args.stage == "test":
        from setup.test_stages import handle_test_stage
        handle_test_stage(args)
        return 0

    # Handle unit/integration test flags
    if (
        getattr(args, "unit", False)
        or getattr(args, "integration", False)
        or getattr(args, "coverage", False)
    ):
        from setup.test_stages import handle_test_stage
        handle_test_stage(args)
        return 0

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

    return 0


def _check_setup_warnings():
    """Check for common setup issues and warn users."""
    import sys
    from pathlib import Path

    # Check if using system Python
    python_path = Path(sys.executable)
    system_indicators = [
        python_path == Path("/usr/bin/python"),
        python_path == Path("/usr/bin/python3"),
        str(python_path).startswith("/usr/"),
        str(python_path).startswith("/usr/local/"),
    ]

    if any(system_indicators):
        logger.warning("⚠️  You're using system Python. This may cause permission errors with pip.")
        logger.info("💡  Run 'python launch.py setup' to create a virtual environment")
        logger.info("   Then use: source venv/bin/activate")

    # Check if venv exists but not activated
    venv_path = ROOT_DIR / "venv" / "bin" / "python"
    if venv_path.exists() and python_path != venv_path:
        logger.info("💡  Virtual environment exists. Activate it with: source venv/bin/activate")


if __name__ == "__main__":
    main()
