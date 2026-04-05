"""
Utility functions for EmailIntelligence launcher
"""

import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger("launcher")

# Get root directory (avoid circular import)
ROOT_DIR = Path(__file__).parent.parent


class ProcessManager:
    """Simple process manager to track and cleanup subprocesses."""

    def __init__(self):
        self.processes = []

    def add_process(self, process):
        """Add a process to track."""
        self.processes.append(process)

    def cleanup(self):
        """Terminate all tracked processes."""
        for process in self.processes:
            try:
                if process.poll() is None:  # Process is still running
                    process.terminate()
                    process.wait(timeout=5)
            except Exception as e:
                logger.warning(f"Error terminating process: {e}")
        self.processes.clear()


# Global process manager instance
process_manager = ProcessManager()


def get_python_executable():
    """Get the path to the Python executable to use."""
    # Check if we're in a virtual environment
    venv_python = os.environ.get("VIRTUAL_ENV")
    if venv_python:
        python_exe = Path(venv_python) / "bin" / "python"
        if python_exe.exists():
            return str(python_exe)

    conda_env = os.environ.get("CONDA_DEFAULT_ENV")
    if conda_env:
        # Try to find conda python
        conda_python = Path.home() / "anaconda3" / "envs" / conda_env / "bin" / "python"
        if conda_python.exists():
            return str(conda_python)

    # Fall back to system python
    return sys.executable


def get_venv_executable(venv_path: Path, executable: str) -> Path:
    """Get the path to an executable in a virtual environment."""
    if os.name == "nt":  # Windows
        return venv_path / "Scripts" / f"{executable}.exe"
    else:  # Unix-like
        return venv_path / "bin" / executable


def print_system_info():
    """Print detailed system, Python, and project configuration information."""
    import platform

    print("=== System Information ===")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")

    print("\n=== Project Information ===")
    print(f"Project Root: {ROOT_DIR}")
    print(f"Python Path: {os.environ.get('PYTHONPATH', 'Not set')}")

    print("\n=== Environment Status ===")
    venv_path = ROOT_DIR / "venv"
    if venv_path.exists():
        print(f"Virtual Environment: {venv_path} (exists)")
        python_exe = get_venv_executable(venv_path, "python")
        if python_exe.exists():
            print(f"Venv Python: {python_exe}")
        else:
            print("Venv Python: Not found")
    else:
        print(f"Virtual Environment: {venv_path} (not created)")

    # Check conda availability
    try:
        import subprocess
        result = subprocess.run(["conda", "--version"], capture_output=True, text=True, timeout=2)
        conda_available = result.returncode == 0
    except:
        conda_available = False

    print(f"Conda Available: {conda_available}")
    if conda_available:
        conda_env = os.environ.get("CONDA_DEFAULT_ENV", "None")
        print(f"Current Conda Env: {conda_env}")

    # Check node availability
    try:
        import subprocess
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=2)
        node_available = result.returncode == 0
    except:
        node_available = False

    print(f"Node.js Available: {node_available}")

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
"""
Utility functions for the EmailIntelligence setup system.

This module contains shared utility functions used across the setup system.
"""

import platform
import sys
import os
from pathlib import Path


def print_system_info():
    """Print detailed system, Python, and project configuration information."""
    print("=== System Information ===")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Project Root: {Path(__file__).parent.parent}")
    
    # Check environment variables
    python_path = os.environ.get('PYTHONPATH', 'Not set')
    conda_env = os.environ.get('CONDA_DEFAULT_ENV', 'Not in conda environment')
    
    print(f"Python Path: {python_path}")
    print(f"Conda Environment: {conda_env}")
    
    # Check git information
    try:
        import subprocess
        result = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], 
                              capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        if result.returncode == 0:
            print(f"Git Commit: {result.stdout.strip()}")
        else:
            print("Git: Not in a git repository or git not available")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Git: Not available")
    
    print("=========================")


def process_manager():
    """Basic process management utility function."""
    # This is a placeholder for any process management functionality
    # that might be needed in the future
    return {
        'status': 'active',
        'version': '1.0.0'
    }