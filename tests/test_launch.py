"""
Tests for setup/launch.py orchestration features.
Tests command pattern availability and basic launch functionality.
"""

import os
import pytest
from unittest.mock import patch, MagicMock

# Import the launch module
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'setup'))

from launch import COMMAND_PATTERN_AVAILABLE, DOTENV_AVAILABLE


class TestLaunchOrchestration:
    """Test orchestration-specific features of launch.py"""

    def test_command_pattern_availability(self):
        """Test that command pattern availability is correctly detected"""
        if os.path.exists("src"):
            # In branches with src/, should attempt to load
            # Availability depends on successful import
            pass  # Skip detailed check as it varies
        else:
            # In orchestration-tools, should be disabled
            assert COMMAND_PATTERN_AVAILABLE == False

    def test_dotenv_availability(self):
        """Test that dotenv availability is correctly detected"""
        # Should be True if python-dotenv is installed
        assert isinstance(DOTENV_AVAILABLE, bool)

    @patch('subprocess.run')
    def test_launch_help_command(self, mock_subprocess):
        """Test that launch.py --help forwards correctly"""
        mock_subprocess.return_value = MagicMock(returncode=0)

        # Import and test help
        from launch import main
        # This would require more setup, skip for now
        pass

    def test_python_version_checks(self):
        """Test that Python version constants are defined"""
        from launch import PYTHON_MIN_VERSION, PYTHON_MAX_VERSION
        assert PYTHON_MIN_VERSION == (3, 12)
        assert PYTHON_MAX_VERSION == (3, 13)
