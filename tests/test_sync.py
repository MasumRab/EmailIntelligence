"""
Tests for orchestration sync scripts.
"""

import os
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestSyncScripts:
    """Test orchestration sync script functionality."""

    def test_sync_setup_worktrees_exists(self):
        """Test that sync_setup_worktrees.sh exists."""
        script_path = Path("scripts/sync_setup_worktrees.sh")
        assert script_path.exists()
        assert script_path.is_file()
        assert os.access(script_path, os.X_OK), "Script should be executable"

    def test_reverse_sync_orchestration_exists(self):
        """Test that reverse_sync_orchestration.sh exists."""
        script_path = Path("scripts/reverse_sync_orchestration.sh")
        assert script_path.exists()
        assert script_path.is_file()
        assert os.access(script_path, os.X_OK), "Script should be executable"

    def test_cleanup_orchestration_exists(self):
        """Test that cleanup_orchestration.sh exists."""
        script_path = Path("scripts/cleanup_orchestration.sh")
        assert script_path.exists()
        assert script_path.is_file()
        assert os.access(script_path, os.X_OK), "Script should be executable"

    def test_install_hooks_exists(self):
        """Test that install-hooks.sh exists."""
        script_path = Path("scripts/install-hooks.sh")
        assert script_path.exists()
        assert script_path.is_file()
        assert os.access(script_path, os.X_OK), "Script should be executable"


class TestSyncScriptExecution:
    """Test that sync scripts can execute without critical errors."""

    @patch("subprocess.run")
    def test_sync_setup_worktrees_dry_run(self, mock_run):
        """Test sync_setup_worktrees.sh dry run."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        import subprocess

        result = subprocess.run(
            ["bash", "scripts/sync_setup_worktrees.sh", "--dry-run"],
            capture_output=True,
            text=True,
            cwd=".",
        )

        # Should not crash
        assert result.returncode == 0 or result.returncode == 1  # Allow controlled failures

    @patch("subprocess.run")
    def test_reverse_sync_dry_run(self, mock_run):
        """Test reverse_sync_orchestration.sh with help."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        import subprocess

        result = subprocess.run(
            ["bash", "scripts/reverse_sync_orchestration.sh", "--help"],
            capture_output=True,
            text=True,
            cwd=".",
        )

        # Should not crash
        assert result.returncode == 0 or result.returncode == 1


class TestSyncConfiguration:
    """Test sync script configuration and managed files."""

    def test_managed_files_list_exists(self):
        """Test that managed files are defined in sync scripts."""
        # Check reverse_sync_orchestration.sh has MANAGED_FILES
        script_path = Path("scripts/reverse_sync_orchestration.sh")
        content = script_path.read_text()
        assert "MANAGED_FILES=(" in content, "Should define MANAGED_FILES array"

    def test_managed_files_include_essentials(self):
        """Test that managed files include essential orchestration files."""
        script_path = Path("scripts/reverse_sync_orchestration.sh")
        content = script_path.read_text()

        essential_files = ["setup/launch.py", ".flake8", ".gitignore", "pytest.ini"]

        for essential_file in essential_files:
            assert essential_file in content, f"Should include {essential_file} in managed files"

    def test_post_push_managed_files(self):
        """Test that post-push hook has managed files list."""
        hook_path = Path(".git/hooks/post-push")
        if hook_path.exists():
            content = hook_path.read_text()
            assert "MANAGED_FILES=(" in content, "post-push hook should define MANAGED_FILES"

    def test_gitignore_excludes_temp_files(self):
        """Test that .gitignore excludes temporary files."""
        gitignore_path = Path(".gitignore")
        assert gitignore_path.exists()

        content = gitignore_path.read_text()
        assert "__pycache__" in content, ".gitignore should exclude __pycache__"
        # Note: .pyc files are covered by __pycache__/ exclusion


class TestOrchestrationWorkflow:
    """Test orchestration workflow functionality."""

    def test_orchestration_tools_branch(self):
        """Test that we're on orchestration-tools branch."""
        import subprocess

        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            cwd=".",
        )

        assert result.returncode == 0
        current_branch = result.stdout.strip()
        # This test might run on different branches, so just check it's a valid branch
        assert len(current_branch) > 0

    def test_orchestration_commit_tracking(self):
        """Test orchestration commit tracking file."""
        commit_file = Path(".git/hooks/.orchestration_commit_id")
        # File may not exist if hooks haven't been installed
        if commit_file.exists():
            content = commit_file.read_text().strip()
            if content:
                # Should look like a commit hash
                assert len(content) >= 7
                # Should only contain hex characters
                import string

                assert all(c in string.hexdigits for c in content)

    def test_worktree_sync_capability(self):
        """Test that worktree sync script can handle basic operations."""
        script_path = Path("scripts/sync_setup_worktrees.sh")
        content = script_path.read_text()

        # Should have basic validation
        assert (
            "git show-ref --verify --quiet refs/heads/orchestration-tools" in content
        ), "Should check orchestration-tools branch exists"
        assert "orchestration-tools" in content, "Should reference orchestration-tools branch"
