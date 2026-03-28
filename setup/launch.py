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
    check_python_version,
    check_for_merge_conflicts,
    check_required_components,
    validate_environment,
)
from setup.services import get_python_executable
from setup.environment import setup_wsl_environment, check_wsl_requirements, is_wsl

# Import test stages

# Standard library imports
import os
import platform
import shutil
import subprocess
import sys
import venv
from pathlib import Path
from typing import List

# Import project configuration
from setup.project_config import get_project_config

# Import command pattern components (with error handling for refactors)
try:
    from setup.commands.command_factory import get_command_factory
    from setup.container import get_container, initialize_all_services
except ImportError:
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

# --- Constants ---
PYTHON_MIN_VERSION = (3, 12)
PYTHON_MAX_VERSION = (3, 13)
VENV_DIR = "venv"
CONDA_ENV_NAME = os.getenv("CONDA_ENV_NAME", "base")
USER_ENV_FILE = "launch-user.env"


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


def _check_paths(paths, root):
    """Check which paths don't exist and return the missing ones."""
    return [p for p in paths if not (root / p).exists()]


def _log_missing(missing, label):
    """Log missing paths with a given label."""
    if missing:
        logger.error(f"Missing critical {label}:")
        for path in missing:
            logger.error(f"  - {path}")


def check_critical_files() -> bool:  # noqa: PLR0912
    """Check for critical files that must exist in the orchestration-tools branch."""
    critical_files = [
        "scripts/install-hooks.sh",
        "scripts/cleanup_orchestration.sh",
        "scripts/sync_setup_worktrees.sh",
        "scripts/reverse_sync_orchestration.sh",
        "scripts/hooks/pre-commit",
        "scripts/hooks/post-commit",
        "scripts/hooks/post-commit-setup-sync",
        "scripts/hooks/post-merge",
        "scripts/hooks/post-checkout",
        "scripts/hooks/post-push",
        "scripts/lib/common.sh",
        "scripts/lib/error_handling.sh",
        "scripts/lib/git_utils.sh",
        "scripts/lib/logging.sh",
        "scripts/lib/validation.sh",
        "setup/launch.py",
        "setup/pyproject.toml",
        "setup/requirements.txt",
        "setup/requirements-dev.txt",
        "setup/setup_environment_system.sh",
        "setup/setup_environment_wsl.sh",
        "setup/setup_python.sh",
        ".flake8",
        ".pylintrc",
        ".gitignore",
        ".gitattributes",
        "launch.py",
        "deployment/deploy.py",
        "deployment/test_stages.py",
        "deployment/docker-compose.yml",
    ]
    critical_dirs = [
        "scripts/",
        "scripts/hooks/",
        "scripts/lib/",
        "setup/",
        "deployment/",
        "docs/",
    ]
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

    missing_files = _check_paths(critical_files + orchestration_docs, ROOT_DIR)
    missing_dirs = _check_paths(critical_dirs, ROOT_DIR)

    if missing_files or missing_dirs:
        _log_missing(missing_files, "files")
        _log_missing(missing_dirs, "directories")
        logger.error(
            "Please restore these critical files for proper orchestration functionality."
        )
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


def setup_dependencies(_venv_path=None, _use_poetry=False):
    """Set up dependencies in a virtual environment.

    Args:
        venv_path: Path to the virtual environment (currently unused, reserved for future use).
        use_poetry: Whether to use poetry for dependency management.
    """
    python_exe = get_python_executable()

    if use_poetry:
        # Ensure pip is up-to-date before installing other packages
        run_command(
            [python_exe, "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip"
        )
        # For poetry, we need to install it first if not available
        try:
            subprocess.run(
                [python_exe, "-c", "import poetry"], check=True, capture_output=True
            )
        except subprocess.CalledProcessError:
            run_command(
                [python_exe, "-m", "pip", "install", "poetry"], "Installing Poetry"
            )

        run_command(
            [python_exe, "-m", "poetry", "install", "--with", "dev"],
            "Installing dependencies with Poetry",
            cwd=ROOT_DIR,
        )
    else:
        # Ensure pip is up-to-date before installing other packages
        run_command(
            [python_exe, "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip"
        )
        # For uv, install if not available
        try:
            subprocess.run(
                [python_exe, "-c", "import uv"], check=True, capture_output=True
            )
        except subprocess.CalledProcessError:
            run_command([python_exe, "-m", "pip", "install", "uv"], "Installing uv")

        run_command(
            [
                python_exe,
                "-m",
                "uv",
                "pip",
                "install",
                "-e",
                ".[dev]",
                "--exclude",
                "notmuch",
            ],
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


def download_nltk_data(_venv_path=None):
    """Download NLTK data packages.

    Args:
        venv_path: Path to virtual environment (unused, reserved for future use).
    """
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
        [python_exe, "-c", nltk_download_script],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
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
