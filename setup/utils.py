"""
Utility functions for the launch system.

This module contains shared utility functions used across the launch system.
"""

import atexit
import logging
import os
import platform
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

# Global paths
ROOT_DIR = Path(__file__).resolve().parent.parent


class ProcessManager:
    """Manager for tracking and cleaning up subprocesses."""

    def __init__(self):
        self.processes: List[subprocess.Popen] = []
        self._shutdown_event = threading.Event()
        atexit.register(self.cleanup)

    def add_process(self, process: subprocess.Popen):
        """Add a process to be managed."""
        self.processes.append(process)

    def cleanup(self):
        """Clean up all managed processes."""
        if self._shutdown_event.is_set():
            return  # Already cleaned up

        logger.info("Performing explicit resource cleanup...")
        self._shutdown_event.set()

        for process in self.processes:
            try:
                if process.poll() is None:  # Process is still running
                    logger.info(f"Terminating process {process.pid}...")
                    process.terminate()

                    # Wait up to 5 seconds for graceful shutdown
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        logger.warning(f"Process {process.pid} did not terminate gracefully, killing...")
                        process.kill()
                        process.wait()
            except Exception as e:
                logger.error(f"Error cleaning up process: {e}")

        self.processes.clear()
        logger.info("Resource cleanup completed.")

    def wait_for_interrupt(self):
        """Wait for keyboard interrupt and cleanup."""
        try:
            while not self._shutdown_event.is_set():
                time.sleep(0.1)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, shutting down...")
            self.cleanup()


# Global process manager instance
process_manager = ProcessManager()


def find_project_root() -> Path:
    """Find the project root directory by looking for key files."""
    current = Path.cwd()

    # Look for project root markers
    root_markers = ["pyproject.toml", "setup.py", "README.md"]

    while current.parent != current:  # Stop at filesystem root
        if any((current / marker).exists() for marker in root_markers):
            return current
        current = current.parent

    # Fallback to current directory
    return Path.cwd()


def is_conda_available() -> bool:
    """Check if conda is available on the system."""
    try:
        result = subprocess.run(
            ["conda", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_conda_env_info():
    """Get information about the current conda environment."""
    try:
        # Check if we're in a conda environment
        env_name = os.environ.get("CONDA_DEFAULT_ENV")
        if env_name:
            logger.info(f"Currently in conda environment: {env_name}")
            return {"env_name": env_name, "active": True}

        # Check conda info
        result = subprocess.run(
            ["conda", "info", "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            import json
            info = json.loads(result.stdout)
            return {
                "active": info.get("active_prefix") is not None,
                "prefix": info.get("active_prefix"),
                "envs": info.get("envs", [])
            }
    except Exception as e:
        logger.debug(f"Could not get conda info: {e}")

    return {"active": False}


def activate_conda_env(env_name: str = None) -> bool:
    """Try to activate a conda environment."""
    if not is_conda_available():
        logger.debug("Conda not available")
        return False

    try:
        # If no env name specified, try to detect
        if not env_name:
            env_info = get_conda_env_info()
            if env_info.get("active"):
                logger.info("Conda environment already active")
                return True

            # Try common environment names
            common_envs = ["emailintelligence", "ei", "venv"]
            for env in common_envs:
                if env in env_info.get("envs", []):
                    env_name = env
                    break

        if env_name:
            logger.info(f"Activating conda environment: {env_name}")
            # Note: This won't actually activate in the current process
            # It's mainly for informational purposes
            os.environ["CONDA_DEFAULT_ENV"] = env_name
            return True
        else:
            logger.debug("No suitable conda environment found")
            return False

    except Exception as e:
        logger.debug(f"Could not activate conda environment: {e}")
        return False


def print_system_info():
    """Print system information for debugging."""
    print("System Information:")
    print(f"  Platform: {platform.platform()}")
    print(f"  Python: {sys.version}")
    print(f"  Executable: {sys.executable}")
    print(f"  Current Directory: {Path.cwd()}")
    print(f"  Project Root: {find_project_root()}")

    # Check for key tools
    tools = ["node", "npm", "conda", "git"]
    print("  Available Tools:")
    for tool in tools:
        try:
            result = subprocess.run([tool, "--version"], capture_output=True, text=True, timeout=2)
            version = result.stdout.strip().split('\n')[0] if result.returncode == 0 else "Not found"
            print(f"    {tool}: {version}")
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            print(f"    {tool}: Not found")

    # Check conda environment
    conda_info = get_conda_env_info()
    if conda_info.get("active"):
        print(f"  Conda Environment: {conda_info.get('env_name', 'Active')}")
    else:
        print("  Conda Environment: None")

    # Check virtual environment
    venv_python = None
    if sys.platform == "win32":
        venv_python = Path(sys.executable).parent.parent / "Scripts" / "python.exe"
    else:
        venv_python = Path(sys.executable).parent.parent / "bin" / "python"

    if venv_python and venv_python.exists():
        print(f"  Virtual Environment: {venv_python.parent.parent}")
    else:
        print("  Virtual Environment: None")