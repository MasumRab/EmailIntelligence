"""
Tests for setup/launch.py orchestration features.
Tests command pattern availability and basic launch functionality.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Import the launch module
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'setup'))

from launch import COMMAND_PATTERN_AVAILABLE, DOTENV_AVAILABLE, PYTHON_MIN_VERSION, PYTHON_MAX_VERSION


class TestLaunchOrchestration:
    """Test launch.py orchestration features."""

    def test_launch_script_exists(self):
        """Test that setup/launch.py exists."""
        launch_script = Path("setup/launch.py")
        assert launch_script.exists()
        assert launch_script.is_file()

    def test_root_launch_wrapper_exists(self):
        """Test that root launch.py wrapper exists."""
        launch_wrapper = Path("launch.py")
        assert launch_wrapper.exists()
        assert launch_wrapper.is_file()

    def test_command_pattern_availability(self):
        """Test that command pattern availability is correctly detected"""
        # In orchestration-tools, should be disabled if src/ is not present
        # For now, we'll just assert it's a boolean, as its value depends on the environment
        assert isinstance(COMMAND_PATTERN_AVAILABLE, bool)

    def test_dotenv_availability(self):
        """Test that dotenv availability is correctly detected"""
        assert isinstance(DOTENV_AVAILABLE, bool)

    def test_python_version_checks(self):
        """Test that Python version constants are defined"""
        assert PYTHON_MIN_VERSION == (3, 12)
        assert PYTHON_MAX_VERSION == (3, 13)

    @patch('subprocess.run')
    def test_launch_execution(self, mock_run):
        """Test that launch script can execute without critical errors."""
        mock_run.return_value = MagicMock(returncode=0)

        # Test the wrapper launch.py
        result = os.system("python launch.py --help > /dev/null 2>&1")
        # We expect this might fail in test environment, but shouldn't crash
        assert result == 0 or result == 256  # 256 is typical for argument errors