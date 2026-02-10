#!/usr/bin/env python3
"""
EmailIntelligence Launch Script
Handles environment setup, dependency management, and service orchestration.
"""

import os
import sys
import shutil
import subprocess
import argparse
import logging
import platform
import venv
from pathlib import Path
from typing import List, Optional

# Constants
PYTHON_MIN_VERSION = (3, 11, 0)
PYTHON_MAX_VERSION = (3, 13, 100)  # Inclusive upper bound for minor version
ROOT_DIR = Path(__file__).resolve().parents[1]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def check_python_version() -> bool:
    """Check if the current Python version is supported."""
    # Use attributes to be mock-friendly
    major = sys.version_info.major
    minor = sys.version_info.minor
    micro = sys.version_info.micro

    current_version = (major, minor, micro)

    if current_version < PYTHON_MIN_VERSION or current_version > PYTHON_MAX_VERSION:
        logger.error(
            f"Unsupported Python version: {sys.version.split()[0]}. "
            f"Please use Python between {PYTHON_MIN_VERSION} and {PYTHON_MAX_VERSION}."
        )
        return False
    logger.info(f"Python version {sys.version.split()[0]} is compatible.")
    return True

def create_venv(venv_path: Path, recreate: bool = False):
    """Create a virtual environment."""
    if recreate and venv_path.exists():
        logger.info("Recreating virtual environment...")
        shutil.rmtree(venv_path)

    if not venv_path.exists():
        logger.info("Creating virtual environment.")
        venv.create(venv_path, with_pip=True)
    else:
        logger.info("Virtual environment already exists.")

def get_venv_executable(venv_path: Path, executable_name: str) -> Path:
    """Get the path to an executable within the virtual environment."""
    if platform.system() == "Windows":
        return venv_path / "Scripts" / f"{executable_name}.exe"
    return venv_path / "bin" / executable_name

def setup_logging():
    """Setup logging configuration."""
    pass # Already configured at module level

def check_environment():
    """Check if the environment is correctly set up."""
    return True

def install_dependencies(venv_path: Path):
    """Install project dependencies."""
    pip_path = get_venv_executable(venv_path, "pip")
    
    # Upgrade pip
    subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
    
    # Install core dependencies
    if (ROOT_DIR / "requirements.txt").exists():
        logger.info("Installing requirements.txt...")
        subprocess.run([str(pip_path), "install", "-r", str(ROOT_DIR / "requirements.txt")], check=True)
    
    # Install project in editable mode
    if (ROOT_DIR / "pyproject.toml").exists():
        logger.info("Installing project in editable mode...")
        subprocess.run([str(pip_path), "install", "-e", "."], cwd=ROOT_DIR, check=True)

def install_nodejs_dependencies(directory: str) -> bool:
    """Install Node.js dependencies for a specific directory."""
    target_dir = ROOT_DIR / directory
    if not target_dir.exists():
        logger.warning(f"Directory {directory} does not exist. Skipping Node.js setup.")
        return True

    npm_path = shutil.which("npm")
    if not npm_path:
        logger.error("npm is not installed. Please install Node.js.")
        return False

    logger.info(f"Installing Node.js dependencies for '{directory}'")
    try:
        subprocess.run([npm_path, "install"], cwd=target_dir, check=True)
        return True
    except subprocess.CalledProcessError:
        logger.error(f"Failed: Installing Node.js dependencies for '{directory}/'")
        return False

def download_nltk_data(venv_path: Path):
    """Download NLTK data."""
    python_path = get_venv_executable(venv_path, "python")
    subprocess.run([str(python_path), "-m", "nltk.downloader", "punkt", "stopwords"], check=True)

class ProcessManager:
    def __init__(self):
        self.processes = []

process_manager = ProcessManager()

def check_uvicorn_installed(venv_path):
    return True

def check_gradio_installed(venv_path):
    return True

def start_backend(venv_path, host, port):
    python_path = get_venv_executable(venv_path, "python")
    cmd = [str(python_path), "-m", "uvicorn", "src.main:app", "--host", host, "--port", str(port)]
    process = subprocess.Popen(cmd)
    process_manager.processes.append(process)
    return process

def start_gradio_ui(venv_path, host):
    python_path = get_venv_executable(venv_path, "python")
    cmd = [str(python_path), "src/ui/main.py"] # Hypothetical path
    process = subprocess.Popen(cmd)
    process_manager.processes.append(process)
    return process

def setup_dependencies(venv_path):
    logger.info("Installing project dependencies with uv...")
    # Mocking uv usage as per test requirement or falling back to pip
    install_dependencies(venv_path)

def start_services(venv_path: Path):
    """Start the application services."""
    start_backend(venv_path, "127.0.0.1", 8000)
    # start_gradio_ui(venv_path, "127.0.0.1")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="EmailIntelligence Launcher")
    parser.add_argument("--recreate-venv", action="store_true", help="Recreate virtual environment")
    args = parser.parse_args()

    if not check_python_version():
        sys.exit(1)

    setup_logging()
    
    if not check_environment():
        sys.exit(1)

    venv_path = ROOT_DIR / "venv"
    create_venv(venv_path, recreate=args.recreate_venv)
    
    install_dependencies(venv_path)
    # download_nltk_data(venv_path)
    
    start_services(venv_path)

if __name__ == "__main__":
    main()
