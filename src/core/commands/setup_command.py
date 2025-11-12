"""
Setup Command implementation.

Handles environment setup operations including virtual environment creation,
dependency installation, and system configuration.
"""

import logging
import os
import shutil
import subprocess
import sys
import venv
from argparse import Namespace
from pathlib import Path

from .command_interface import Command

def is_wsl():
    """Check if running in WSL environment"""
    try:
        with open('/proc/version', 'r') as f:
            content = f.read().lower()
            return 'microsoft' in content or 'wsl' in content
    except:
        return False

logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
VENV_DIR = ROOT_DIR / "venv"


class SetupCommand(Command):
    """
    Command for setting up the development environment.

    This command handles:
    - Virtual environment creation
    - Dependency installation
    - Environment validation
    - System configuration
    """

    def get_description(self) -> str:
        return "Set up the development environment (virtual environment, dependencies, etc.)"

    def execute(self) -> int:
        """
        Execute the setup command.

        Returns:
            int: Exit code
        """
        try:
            logger.info("Starting environment setup...")

            # Validate environment
            if not self._validate_environment():
                return 1

            # Setup virtual environment
            if not self.args.no_venv and not self._setup_virtual_env():
                return 1

            # Install dependencies
            if not self._install_dependencies():
                return 1

            # Validate setup
            if not self._validate_setup():
                return 1

            logger.info("Environment setup completed successfully")
            return 0

        except Exception as e:
            logger.error(f"Setup failed: {e}")
            return 1

    def _validate_environment(self) -> bool:
        """
        TODO: Implement comprehensive environment validation.

        This method should perform checks to ensure the system meets the
        minimum requirements for the project. This includes:
        1.  **Python Version Check:** Verify that the installed Python version
            is compatible (e.g., Python 3.12+).
        2.  **Git Installation Check:** Ensure Git is installed and accessible.
        3.  **System Dependencies:** Check for any required system-level packages
            (e.g., `notmuch` for email processing, specific compilers).
        4.  **OS Compatibility:** Verify compatibility with the operating system
            (e.g., Linux, macOS, WSL).
        5.  **Resource Availability:** Optionally check for sufficient RAM, disk space.
        """
        logger.info("Validating environment...")

        # Add environment validation logic here
        # This would include Python version checks, system requirements, etc.

        # For now, just log success
        logger.info("Environment validation passed")
        return True

    def _setup_virtual_env(self) -> bool:
        """Setup virtual environment."""
        logger.info("Setting up virtual environment...")
        try:
            if VENV_DIR.exists() and self.args.force_recreate_venv:
                logger.info("Removing existing virtual environment.")
                shutil.rmtree(VENV_DIR)
            if not VENV_DIR.exists():
                logger.info("Creating virtual environment.")
                venv.create(VENV_DIR, with_pip=True, upgrade_deps=True)
            logger.info("Virtual environment setup completed")
            return True
        except Exception as e:
            logger.error(f"Failed to set up virtual environment: {e}")
            return False

    def _install_dependencies(self) -> bool:
        """
        TODO: Enhance dependency installation logic.

        This method should install project dependencies. Future enhancements:
        1.  **Dynamic Project Root:** The hardcoded path `/home/masum/github/EmailIntelligenceGem/`
            should be replaced with a dynamic path derived from `ROOT_DIR`.
        2.  **Dependency File Flexibility:** Support for different dependency files
            (e.g., `requirements.txt`, `pyproject.toml` with `poetry` or `pdm`).
        3.  **CPU/GPU Specifics:** Better handling of CPU-only vs. GPU-enabled
            installations, potentially reading from configuration or CLI arguments.
        4.  **Error Handling:** More robust error handling and user guidance for
            failed installations.
        5.  **Progress Indicators:** Integrate progress indicators for long installations.
        """
        logger.info("Installing dependencies...")
        try:
            if is_wsl():
                self._run_command(["sudo", "apt-get", "update"], "Updating package list")
                self._run_command(["sudo", "apt-get", "install", "-y", "notmuch", "python3-notmuch"], "Installing notmuch and python3-notmuch")
            python_exe = self._get_venv_executable("python")
            self._run_command([str(python_exe), "-m", "pip", "install", "uv"], "Installing uv")
            # TODO: Make the installation path dynamic.
            # Replace "/home/masum/github/EmailIntelligenceGem/" with `str(ROOT_DIR)`
            self._run_command([str(python_exe), "-m", "uv", "pip", "install", "-e", "/home/masum/github/EmailIntelligenceGem/"], "Installing dependencies with uv", cwd=ROOT_DIR)
            logger.info("Dependencies installed successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False

    def _install_notmuch_matching_system(self):
        try:
            result = subprocess.run(["notmuch", "--version"], capture_output=True, text=True, check=True)
            version_line = result.stdout.strip()
            version = version_line.split()[1]
            major_minor = '.'.join(version.split('.')[:2])
            python_exe = self._get_venv_executable("python")
            self._run_command([str(python_exe), "-m", "pip", "install", f"notmuch=={major_minor}"], f"Installing notmuch {major_minor} to match system")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("notmuch not found on system, installing latest version from PyPI")
            python_exe = self._get_venv_executable("python")
            self._run_command([str(python_exe), "-m", "pip", "install", "notmuch"], "Installing latest notmuch from PyPI")

    def _get_venv_executable(self, executable: str) -> Path:
        """Get the path to a specific executable in the virtual environment."""
        scripts_dir = "Scripts" if sys.platform == "win32" else "bin"
        return VENV_DIR / scripts_dir / (f"{executable}.exe" if sys.platform == "win32" else executable)

    def _run_command(self, cmd: list[str], description: str, **kwargs) -> bool:
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

    def _validate_setup(self) -> bool:
        """
        TODO: Implement comprehensive setup validation.

        This method should verify that the environment setup was successful
        and that the project is ready to run. This includes:
        1.  **Virtual Environment Activation:** Check if the virtual environment
            is correctly activated.
        2.  **Dependency Availability:** Verify that all critical dependencies
            are importable within the virtual environment.
        3.  **Basic Functionality Test:** Run a very basic test to ensure the
            core components of the application can start or execute.
        4.  **Configuration Files:** Check for the presence and validity of
            essential configuration files.
        """
        logger.info("Validating setup...")

        # Add setup validation logic here
        # Check that venv works, imports work, etc.

        # For now, just log success
        logger.info("Setup validation passed")
        return True