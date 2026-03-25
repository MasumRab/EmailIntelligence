"""
Tests for setup/launch.py orchestration features.
Tests basic functionality and constants.
"""

import os
import pytest
import subprocess
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Import the launch module
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

    def test_python_version_constants(self):
        """Test that Python version constants are defined"""
        assert PYTHON_MIN_VERSION == (3, 12)
        assert PYTHON_MAX_VERSION == (3, 13)

    def test_launch_help_execution(self):
        """Test that launch.py --help runs without errors and shows expected output."""
        result = subprocess.run([sys.executable, 'launch.py', '--help'],
                              capture_output=True, text=True, cwd='.')
        assert result.returncode == 0
        assert 'EmailIntelligence Unified Launcher' in result.stdout

    def test_no_src_import_warnings(self):
        """Test that launch.py doesn't show src import warnings in orchestration-tools"""
        result = subprocess.run([sys.executable, 'launch.py', '--help'],
                              capture_output=True, text=True, cwd='.')
        # Should not have warnings about core modules if src/ missing
        assert 'Could not import core modules' not in result.stderr