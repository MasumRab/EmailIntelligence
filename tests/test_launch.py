"""
Tests for setup/launch.py orchestration features.
Tests basic functionality and constants.
"""

import os
import pytest
import subprocess
import sys
from pathlib import Path


class TestLaunchOrchestration:
    """Test orchestration-specific features of launch.py"""

    def test_launch_script_exists(self):
        """Test that launch.py script exists"""
        launch_path = Path("setup/launch.py")
        assert launch_path.exists()

    def test_launch_help_runs(self):
        """Test that launch.py --help runs without errors"""
        result = subprocess.run([sys.executable, 'setup/launch.py', '--help'],
                              capture_output=True, text=True, cwd='.')
        assert result.returncode == 0
        assert 'EmailIntelligence Unified Launcher' in result.stdout

    def test_no_src_import_warnings(self):
        """Test that launch.py doesn't show src import warnings in orchestration-tools"""
        result = subprocess.run([sys.executable, 'setup/launch.py', '--help'],
                              capture_output=True, text=True, cwd='.')
        # Should not have warnings about core modules if src/ missing
        assert 'Could not import core modules' not in result.stderr

    def test_python_version_constants(self):
        """Test that Python version constants are in the file"""
        launch_content = Path("setup/launch.py").read_text()
        assert 'PYTHON_MIN_VERSION = (3, 12)' in launch_content
        assert 'PYTHON_MAX_VERSION = (3, 13)' in launch_content
