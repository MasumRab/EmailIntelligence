"""
<<<<<<< HEAD
Environment management for the launch system.

This module handles virtual environment creation, dependency installation,
and environment setup operations.
=======
Environment setup utilities for EmailIntelligence launcher
>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613
"""

import logging
import os
import platform
<<<<<<< HEAD
import shutil
import subprocess
import sys
import venv
from pathlib import Path
from typing import List

from setup.project_config import get_project_config

logger = logging.getLogger(__name__)

# Global paths
ROOT_DIR = Path(__file__).resolve().parent.parent


def is_wsl():
    """Check if running in WSL environment."""
    try:
        with open("/proc/version", "r") as f:
            content = f.read().lower()
            return "microsoft" in content or "wsl" in content
    except Exception:
        return False


def setup_wsl_environment():
    """Setup WSL-specific environment variables if in WSL."""
=======
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
>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613
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
<<<<<<< HEAD
    """Check WSL-specific requirements and warn if needed."""
=======
    """Check WSL-specific requirements and warn if needed"""
>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613
    if not is_wsl():
        return

    # Check if X11 server is accessible (optional check)
    try:
        result = subprocess.run(["xset", "-q"], capture_output=True, timeout=2)
        if result.returncode != 0:
            logger.warning("X11 server not accessible - GUI applications may not work")
<<<<<<< HEAD
            logger.info("Install VcXsrv, MobaXterm, or similar X11 server on Windows")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass  # Silently ignore X11 check failures


def get_python_executable() -> str:
    """Get the Python executable path from the venv or system."""
    venv_path = ROOT_DIR / "venv"
    if sys.platform == "win32":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"

    if python_exe.exists():
        return str(python_exe)
    # Fallback to system python if venv not found
    return sys.executable


def get_venv_executable(venv_path: Path, executable: str) -> Path:
    """Get the path to an executable within a virtual environment."""
    if sys.platform == "win32":
        return venv_path / "Scripts" / f"{executable}.exe"
    else:
        return venv_path / "bin" / executable


def run_command(cmd: List[str], description: str, **kwargs) -> bool:
    """Run a command with logging and error handling."""
    logger.info(f"{description}: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, **kwargs)
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Command failed: {e}")
        return False


def create_venv(venv_path: Path, recreate: bool = False):
    """Create a Python virtual environment."""
    if venv_path.exists() and recreate:
        logger.info(f"Removing existing virtual environment at {venv_path}")
        shutil.rmtree(venv_path)

    if not venv_path.exists():
        logger.info(f"Creating virtual environment at {venv_path}")
        venv.create(venv_path, with_pip=True)
    else:
        logger.info(f"Virtual environment already exists at {venv_path}")


def install_package_manager(venv_path: Path, manager: str):
    """Install a package manager in the virtual environment."""
    python_exe = get_venv_executable(venv_path, "python")

    if manager == "uv":
        logger.info("Installing uv package manager...")
        run_command([str(python_exe), "-m", "pip", "install", "uv"], "Installing uv")
    elif manager == "poetry":
        logger.info("Installing Poetry package manager...")
        run_command([str(python_exe), "-m", "pip", "install", "poetry"], "Installing Poetry")


def setup_dependencies(venv_path: Path, use_poetry: bool = False):
    """Install Python dependencies using uv or poetry."""
    python_exe = get_venv_executable(venv_path, "python")

    if use_poetry:
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
        # For uv, install if not available
        try:
            subprocess.run([python_exe, "-c", "import uv"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            run_command([python_exe, "-m", "pip", "install", "uv"], "Installing uv")

        run_command(
            [python_exe, "-m", "uv", "pip", "install", "-e", ".[dev]"],
            "Installing dependencies with uv",
            cwd=ROOT_DIR,
        )

        # Install notmuch with version matching system
        install_notmuch_matching_system()

        # Install environment-specific requirements
        install_environment_specific_requirements(str(python_exe))


def install_notmuch_matching_system():
    """Install notmuch with version matching the system."""
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


def install_environment_specific_requirements(python_exe: str):
    """Install environment-specific requirements based on platform and hardware."""
    system = platform.system().lower()
    requirements_files = []

    # Base environment-specific file
    if system == "linux":
        requirements_files.append("requirements-linux.txt")
    elif system == "windows":
        requirements_files.append("requirements-windows.txt")
    elif system == "darwin":  # macOS
        requirements_files.append("requirements-linux.txt")  # Use linux as fallback

    # Hardware-specific file (GPU vs CPU)
    try:
        # Check for CUDA availability (simple check)
        result = subprocess.run(
            [python_exe, "-c", "import torch; print(torch.cuda.is_available())"],
            capture_output=True, text=True, timeout=10
        )
        has_cuda = result.stdout.strip() == "True"
        if has_cuda:
            requirements_files.append("requirements-gpu.txt")
        else:
            requirements_files.append("requirements-cpu.txt")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        # If torch check fails, default to CPU
        logger.info("Could not detect CUDA availability, defaulting to CPU requirements")
        requirements_files.append("requirements-cpu.txt")

    # Install each requirements file if it exists
    for req_file in requirements_files:
        req_path = ROOT_DIR / "setup" / req_file
        if req_path.exists():
            logger.info(f"Installing environment-specific requirements from {req_file}")
            run_command(
                [python_exe, "-m", "pip", "install", "-r", str(req_path)],
                f"Installing {req_file}",
                cwd=ROOT_DIR,
            )
        else:
            logger.debug(f"Environment-specific requirements file {req_file} not found, skipping")


def download_nltk_data(venv_path=None):
    """Download NLTK data required by the application."""
    python_exe = get_python_executable() if venv_path is None else get_venv_executable(venv_path, "python")

    logger.info("Downloading NLTK data...")
    try:
        result = subprocess.run([
            python_exe, "-c",
            "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            logger.info("NLTK data downloaded successfully")
        else:
            logger.warning(f"NLTK download failed: {result.stderr}")
    except Exception as e:
        logger.warning(f"Failed to download NLTK data: {e}")


def handle_setup(args, venv_path):
    """Handle the complete setup process."""
    logger.info("Starting environment setup...")

    if args.use_conda:
=======
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
>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613
        # For Conda, we assume the environment is already set up
        # Could add Conda environment creation here in the future
        logger.info("Using Conda environment - assuming dependencies are already installed")
    else:
        # Use venv
<<<<<<< HEAD
        create_venv(venv_path, args.force_recreate_venv)
        install_package_manager(venv_path, "uv")
        setup_dependencies(venv_path, False)
        if not args.no_download_nltk:
            download_nltk_data(venv_path)

        # Setup Node.js dependencies
        config = get_project_config()

        # Setup frontend dependencies
        frontend_path = config.get_service_path("frontend")
        if frontend_path and frontend_path.exists():
            from setup.services import setup_node_dependencies
            setup_node_dependencies(frontend_path, "Frontend Client")

        # Setup TypeScript backend dependencies
        ts_backend_path = config.get_service_path("typescript_backend")
        if ts_backend_path and ts_backend_path.exists():
            from setup.services import setup_node_dependencies
            setup_node_dependencies(ts_backend_path, "TypeScript Backend")
=======
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
>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613

    logger.info("Setup complete.")


def prepare_environment(args):
<<<<<<< HEAD
    """Prepare the environment for running the application."""
    if not args.no_venv:
        # Try conda first
        from setup.utils import activate_conda_env
        if not activate_conda_env():
            # Fall back to venv setup
            handle_setup(args, ROOT_DIR / "venv")
=======
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
>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613
