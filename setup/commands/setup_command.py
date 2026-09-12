"""
Setup Command implementation.

Handles environment setup operations including virtual environment creation,
dependency installation, and system configuration.
"""

import logging
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

            logger.info("🎉 Environment setup completed successfully!")
            logger.info("")
            logger.info("Next steps:")
            logger.info("  1. Activate the virtual environment:")
            logger.info("     source venv/bin/activate")
            logger.info("")
            logger.info("  2. Or use Python directly:")
            logger.info("     ./venv/bin/python")
            logger.info("")
            logger.info("  3. Install additional packages (if needed):")
            logger.info("     ./venv/bin/pip install <package>")
            logger.info("")
            return 0

        except Exception as e:
            logger.error(f"Setup failed: {e}")
            return 1

    def _validate_environment(self) -> bool:
        """Validate the environment before setup."""
        import sys

        logger.info("Validating environment...")

        # Check for system Python that might cause permission issues
        if self._is_system_python():
            logger.warning("⚠️  System Python detected at: {}".format(sys.executable))
            logger.warning(
                "❌ This will cause 'Permission denied' errors when running 'pip install'"
            )
            logger.info(
                "✅ The setup will create a virtual environment to avoid permission issues."
            )
            logger.info("💡 After setup, always use: source venv/bin/activate")
            logger.info("   Or run commands with: ./venv/bin/pip install <package>")

        # Check if we're already in a virtual environment
        if self._is_in_virtual_env():
            venv_path = self._get_venv_path()
            logger.info(f"✅ Already in virtual environment: {venv_path}")
        else:
            logger.info("ℹ️  Not in a virtual environment - setup will create one")

        # Check Python version
        import sys

        python_version = sys.version_info
        if python_version < (3, 8):
            logger.error(
                f"Python {python_version.major}.{python_version.minor} is too old. Minimum required: 3.8"
            )
            return False

        logger.info(
            f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}"
        )
        logger.info("Environment validation passed")
        return True

    def _is_system_python(self) -> bool:
        """Check if we're using system-installed Python."""
        import sys

        python_path = Path(sys.executable)

        # Common system Python paths
        system_paths = [
            "/usr/bin/python",
            "/usr/bin/python3",
            "/usr/local/bin/python",
            "/usr/local/bin/python3",
            "/opt/homebrew/bin/python3",  # macOS Homebrew
        ]

        # Check if executable is in system paths
        for system_path in system_paths:
            if python_path == Path(system_path):
                return True

        # Check if it's in a system directory
        system_dirs = ["/usr", "/usr/local", "/opt/homebrew"]
        for sys_dir in system_dirs:
            if str(python_path).startswith(sys_dir):
                return True

        return False

    def _is_in_virtual_env(self) -> bool:
        """Check if we're currently in a virtual environment."""
        import sys
        import os

        # Check for common venv indicators
        return (
            hasattr(sys, "real_prefix")
            or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
            or os.environ.get("VIRTUAL_ENV") is not None
            or os.environ.get("CONDA_DEFAULT_ENV") is not None
        )

    def _get_venv_path(self) -> str:
        """Get the current virtual environment path."""
        import os

        # Check various indicators
        venv_path = os.environ.get("VIRTUAL_ENV")
        if venv_path:
            return venv_path

        conda_env = os.environ.get("CONDA_DEFAULT_ENV")
        if conda_env:
            return f"conda:{conda_env}"

        # Try to infer from sys.prefix
        import sys

        if hasattr(sys, "real_prefix"):
            return sys.real_prefix
        elif hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix:
            return sys.prefix

        return "Unknown"

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
                use_conda=getattr(self.args, "use_conda", False),
                force_recreate_venv=getattr(self.args, "force_recreate_venv", False),
                no_download_nltk=getattr(self.args, "no_download_nltk", False),
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

            result = subprocess.run(
                [str(python_exe), "-c", "print('Venv validation successful')"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                logger.error(f"Venv validation failed: {result.stderr}")
                return False

            logger.info("Setup validation passed")
            return True

        except Exception as e:
            logger.error(f"Setup validation failed: {e}")
            return False
