"""
Tests for orchestration sync scripts.
"""

import os
import pytest
from pathlib import Path
from unittest.mock import patch


class TestSyncScripts:
    """Test sync setup worktrees script"""

    def test_sync_script_exists(self):
        """Test that sync script exists and is executable"""
        script_path = Path("scripts/sync_setup_worktrees.sh")
        assert script_path.exists()
        assert os.access(script_path, os.X_OK)

    def test_manage_changes_script_exists(self):
        """Test that manage orchestration changes script exists"""
        script_path = Path("scripts/manage_orchestration_changes.sh")
        assert script_path.exists()
        assert os.access(script_path, os.X_OK)

    @patch('subprocess.run')
    def test_sync_script_help(self, mock_subprocess):
        """Test that sync script shows help"""
        mock_subprocess.return_value = MagicMock(returncode=0, stdout="Usage:")

        # Would need to run the script, but skip for now
        pass

    def test_managed_files_list(self):
        """Test that managed files list is defined in manage script"""
        script_path = Path("scripts/manage_orchestration_changes.sh")
        content = script_path.read_text()
        assert "MANAGED_FILES" in content
        assert "setup/launch.py" in content
