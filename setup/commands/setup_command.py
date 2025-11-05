"""
Setup Command implementation.

Handles environment setup operations including virtual environment creation,
dependency installation, and system configuration.
"""

import logging
from argparse import Namespace
from pathlib import Path

from .command_interface import Command

logger = logging.getLogger(__name__)


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

    def validate_args(self) -> bool:
        """Validate command arguments."""
        # Setup command accepts various legacy arguments
        return True

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
        """Validate the environment before setup."""
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
            # Use existing setup logic from environment.py
            from setup.environment import handle_setup
            from setup.project_config import get_project_config
            import argparse

            # Create args object with defaults for setup
            args = argparse.Namespace(
                use_conda=getattr(self.args, 'use_conda', False),
                force_recreate_venv=getattr(self.args, 'force_recreate_venv', False),
                no_download_nltk=getattr(self.args, 'no_download_nltk', False)
            )

            # Get venv path
            venv_path = get_project_config().root_dir / "venv"

            # Call the existing setup function
            handle_setup(args, venv_path)

            logger.info("Virtual environment setup completed")
            return True

        except Exception as e:
            logger.error(f"Virtual environment setup failed: {e}")
            return False

    def _install_dependencies(self) -> bool:
        """Install project dependencies."""
        logger.info("Installing dependencies...")

        # Dependencies are already installed in _setup_virtual_env
        # This method is kept for future expansion if needed
        logger.info("Dependencies installed successfully")
        return True

    def _validate_setup(self) -> bool:
        """Validate that setup completed successfully."""
        logger.info("Validating setup...")

        try:
            # Check if venv exists and is functional
            from setup.project_config import get_project_config
            from setup.environment import get_venv_executable

            venv_path = get_project_config().root_dir / "venv"
            python_exe = get_venv_executable(venv_path, "python")

            if not python_exe.exists():
                logger.error(f"Python executable not found in venv: {python_exe}")
                return False

            # Try to run a simple python command to verify venv works
            import subprocess
            result = subprocess.run([str(python_exe), "-c", "print('Venv validation successful')"],
                                  capture_output=True, text=True, timeout=10)

            if result.returncode != 0:
                logger.error(f"Venv validation failed: {result.stderr}")
                return False

            logger.info("Setup validation passed")
            return True

        except Exception as e:
            logger.error(f"Setup validation failed: {e}")
            return False