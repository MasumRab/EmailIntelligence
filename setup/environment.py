"""
Environment setup utilities for EmailIntelligence launcher
"""

import logging
import os
import platform
import subprocess
from pathlib import Path

logger = logging.getLogger("launcher")

# Get root directory (avoid circular import)
ROOT_DIR = Path(__file__).parent.parent

# Constants
VENV_DIR = "venv"
CONDA_ENV_NAME = os.getenv("CONDA_ENV_NAME", "base")


def is_wsl():
    """Check if running in Windows Subsystem for Linux."""
    return "microsoft" in platform.uname().release.lower() or "wsl" in platform.uname().release.lower()


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
    except (subprocess.TimeoutExpired, FileNotFoundError):
        logger.warning("X11 server check failed - GUI applications may not work")


def is_conda_available():
    """Check if conda is available."""
    try:
        result = subprocess.run(["conda", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_conda_env_info():
    """Get information about the current conda environment."""
    try:
        result = subprocess.run(["conda", "info", "--envs"], capture_output=True, text=True)
        return result.stdout
    except Exception:
        return "Conda environment info not available"


def activate_conda_env():
    """Try to activate the conda environment."""
    if not is_conda_available():
        return False

    try:
        # This is tricky in a subprocess - we'd need to source the conda script
        # For now, just check if we're already in the right environment
        current_env = os.environ.get("CONDA_DEFAULT_ENV", "")
        if current_env == CONDA_ENV_NAME:
            logger.info(f"Already in conda environment: {current_env}")
            return True
        else:
            logger.info(f"Conda environment {CONDA_ENV_NAME} not active")
            return False
    except Exception as e:
        logger.warning(f"Could not check conda environment: {e}")
        return False


def handle_setup(args, venv_path):
    """Handles the complete setup process."""
    logger.info("Starting environment setup...")

    if getattr(args, 'use_conda', False):
        # For Conda, we assume the environment is already set up
        # Could add Conda environment creation here in the future
        logger.info("Using Conda environment - assuming dependencies are already installed")
    else:
        # Use venv
        try:
            from setup.launch import create_venv, install_package_manager, setup_dependencies, download_nltk_data
            create_venv(venv_path, getattr(args, 'force_recreate_venv', False))
            install_package_manager(venv_path, "uv")
            setup_dependencies(venv_path, False)
            if not getattr(args, 'no_download_nltk', False):
                download_nltk_data(venv_path)
        except ImportError:
            logger.warning("Some setup functions not available yet")

        # Setup Node.js dependencies
        try:
            from setup.launch import setup_node_dependencies
            setup_node_dependencies(ROOT_DIR / "client", "Frontend Client")
            setup_node_dependencies(ROOT_DIR / "backend" / "server-ts", "TypeScript Backend")
        except ImportError:
            logger.warning("Node setup functions not available yet")

    logger.info("Setup complete.")


def prepare_environment(args):
    """Prepares the environment for running the application."""
    if not getattr(args, 'no_venv', False):
        # Try conda first
        if not activate_conda_env():
            venv_path = ROOT_DIR / VENV_DIR
            try:
                from setup.launch import create_venv
                create_venv(venv_path)
            except ImportError:
                logger.warning("create_venv function not available yet")

        if getattr(args, 'update_deps', False):
            try:
                from setup.launch import setup_dependencies
                setup_dependencies(ROOT_DIR / VENV_DIR, False)
            except ImportError:
                logger.warning("setup_dependencies function not available yet")

    if not getattr(args, 'no_download_nltk', False):
        try:
            from setup.launch import download_nltk_data
            download_nltk_data()
        except ImportError:
            logger.warning("download_nltk_data function not available yet")