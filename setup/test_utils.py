#!/usr/bin/env python3
"""
Unit tests for the utils module.

These tests cover utility functions in setup/utils.py:
- find_project_root
- is_conda_available
- get_conda_env_info
- activate_conda_env
- ProcessManager
"""

import sys
import os
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from setup import utils


class TestFindProjectRoot:
    """Tests for find_project_root function."""

    def test_find_project_root_with_marker(self):
        """Test finding project root with existing marker."""
        with patch.object(Path, 'exists', return_value=True) as mock_exists:
            # Mock Path.cwd to return a test path
            test_path = MagicMock(spec=Path)
            test_path.parent = MagicMock(spec=Path)
            test_path.parent != test_path  # Different to avoid infinite loop
            test_path.__truediv__ = lambda self, other: Path("/project")
            
            with patch('setup.utils.Path.cwd', return_value=test_path):
                with patch('pathlib.Path.exists', return_value=True):
                    # Test that markers are checked
                    root = utils.find_project_root()
                    # Should return a Path object

    def test_find_project_root_fallback(self):
        """Test fallback to current directory."""
        # This tests the fallback behavior
        root = utils.find_project_root()
        assert isinstance(root, Path)


class TestIsCondaAvailable:
    """Tests for is_conda_available function."""

    @patch('setup.utils.subprocess.run')
    def test_is_conda_available_found(self, mock_run):
        """Test when conda is available."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = utils.is_conda_available()
        assert result is True

    @patch('setup.utils.subprocess.run')
    def test_is_conda_available_not_found(self, mock_run):
        """Test when conda is not available."""
        mock_run.side_effect = FileNotFoundError()

        result = utils.is_conda_available()
        assert result is False

    def test_is_conda_available_timeout(self):
        """Test when conda command times out."""
        import subprocess
        with patch('setup.utils.subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("conda", 5)

            result = utils.is_conda_available()
            assert result is False


class TestGetCondaEnvInfo:
    """Tests for get_conda_env_info function."""

    @patch.dict(os.environ, {"CONDA_DEFAULT_ENV": "test_env"})
    def test_get_conda_env_info_active_env(self):
        """Test when conda environment is active."""
        result = utils.get_conda_env_info()
        
        assert result["active"] is True
        assert result["env_name"] == "test_env"

    @patch('setup.utils.subprocess.run')
    @patch.dict(os.environ, {}, clear=False)
    def test_get_conda_env_info_from_conda_info(self, mock_run):
        """Test parsing conda info JSON output."""
        import json
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps({
            "active_prefix": "/home/user/anaconda3/envs/test",
            "envs": ["/home/user/anaconda3/envs/test"]
        })
        mock_run.return_value = mock_result

        result = utils.get_conda_env_info()
        
        assert result["active"] is True
        assert result["prefix"] == "/home/user/anaconda3/envs/test"

    def test_get_conda_env_info_no_env(self):
        """Test when no conda environment is active."""
        mock_result = MagicMock()
        mock_result.returncode = 1  # Exit code 1 means not in conda
        mock_result.stdout = ""
        
        # Force no conda env
        with patch('setup.utils.subprocess.run', return_value=mock_result):
            result = utils.get_conda_env_info()
            # Should return inactive state
            assert result["active"] is False


class TestActivateCondaEnv:
    """Tests for activate_conda_env function."""

    @patch('setup.utils.is_conda_available')
    def test_activate_conda_not_available(self, mock_available):
        """Test when conda is not available."""
        mock_available.return_value = False

        result = utils.activate_conda_env()
        
        assert result is False

    @patch('setup.utils.is_conda_available')
    @patch('setup.utils.get_conda_env_info')
    def test_activate_conda_already_active(self, mock_info, mock_available):
        """Test when conda is already active."""
        mock_available.return_value = True
        mock_info.return_value = {"active": True, "env_name": "existing"}

        result = utils.activate_conda_env()
        
        assert result is True

    @patch('setup.utils.is_conda_available')
    @patch('setup.utils.get_conda_env_info')
    @patch.dict(os.environ, {}, clear=False)
    def test_activate_conda_with_name(self, mock_info, mock_available):
        """Test activating a specific conda environment."""
        mock_available.return_value = True
        mock_info.return_value = {
            "active": False,
            "envs": ["emailintelligence", "test_env"]
        }

        # Ensure not in environment
        if "CONDA_DEFAULT_ENV" in os.environ:
            del os.environ["CONDA_DEFAULT_ENV"]

        result = utils.activate_conda_env("test_env")
        
        assert result is True
        assert os.environ.get("CONDA_DEFAULT_ENV") == "test_env"


class TestProcessManager:
    """Tests for ProcessManager class."""

    def test_process_manager_init(self):
        """Test ProcessManager initialization."""
        pm = utils.ProcessManager()
        
        assert pm.processes == []
        assert pm._shutdown_event is not None

    @patch('setup.utils.atexit')
    def test_process_manager_registers_cleanup(self, mock_atexit):
        """Test ProcessManager registers cleanup on init."""
        pm = utils.ProcessManager()
        mock_atexit.register.assert_called_once_with(pm.cleanup)

    def test_process_manager_add_process(self):
        """Test adding a process."""
        pm = utils.ProcessManager()
        mock_process = MagicMock()
        
        pm.add_process(mock_process)
        
        assert mock_process in pm.processes

    @patch('setup.utils.time.sleep')
    def test_process_manager_wait_for_interrupt(self, mock_sleep):
        """Test waiting for interrupt."""
        pm = utils.ProcessManager()
        
        # Set the shutdown event to break the loop
        pm._shutdown_event.set()
        
        # Should not raise
        pm.wait_for_interrupt()

    def test_process_manager_cleanup_empty(self):
        """Test cleanup with no processes."""
        pm = utils.ProcessManager()
        
        # Should not raise
        pm.cleanup()
        
        assert pm._shutdown_event.is_set()


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])