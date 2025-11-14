"""
Tests for Git hook functionality in orchestration-tools.
"""

import os
import pytest
from pathlib import Path


class TestGitHooks:
    """Test Git hooks installation and functionality"""

    def test_hooks_directory_exists(self):
        """Test that .git/hooks directory exists"""
        hooks_dir = Path(".git/hooks")
        assert hooks_dir.exists()
        assert hooks_dir.is_dir()

    def test_required_hooks_exist(self):
        """Test that required orchestration hooks are installed"""
        required_hooks = ['pre-commit', 'post-commit', 'post-merge', 'post-checkout', 'post-push']
        hooks_dir = Path(".git/hooks")

        for hook in required_hooks:
            hook_path = hooks_dir / hook
            assert hook_path.exists(), f"Hook {hook} not found"
            assert os.access(hook_path, os.X_OK), f"Hook {hook} not executable"

    def test_hook_scripts_reference_install_hooks(self):
        """Test that hook scripts reference install-hooks.sh"""
        hooks_dir = Path(".git/hooks")
        post_merge_hook = hooks_dir / "post-merge"

        if post_merge_hook.exists():
            content = post_merge_hook.read_text()
            assert "install-hooks.sh" in content, "post-merge should reference install-hooks.sh"

    def test_install_hooks_script_exists(self):
        """Test that install-hooks.sh script exists and is executable"""
        script_path = Path("scripts/install-hooks.sh")
        assert script_path.exists()
        assert os.access(script_path, os.X_OK)

"""
Tests for Git hook functionality in orchestration-tools.
"""

import os
import pytest
from pathlib import Path


class TestGitHooks:
    """Test Git hook installation and functionality."""

    def test_hook_directory_exists(self):
        """Test that .git/hooks directory exists."""
        hooks_dir = Path(".git/hooks")
        assert hooks_dir.exists()
        assert hooks_dir.is_dir()

    def test_required_hooks_exist(self):
        """Test that required hooks are installed."""
        required_hooks = ["pre-commit", "post-commit", "post-merge", "post-checkout", "post-push"]
        hooks_dir = Path(".git/hooks")

        for hook in required_hooks:
            hook_path = hooks_dir / hook
            assert hook_path.exists(), f"Hook {hook} should exist"
            assert os.access(hook_path, os.X_OK), f"Hook {hook} should be executable"

    def test_install_hooks_script_exists(self):
        """Test that install-hooks.sh script exists and is executable."""
        script_path = Path("scripts/install-hooks.sh")
        assert script_path.exists()
        assert os.access(script_path, os.X_OK)

    def test_hooks_reference_install_script(self):
        """Test that hooks properly reference orchestration scripts."""
        hooks_dir = Path(".git/hooks")

        # Check post-merge hook has orchestration functionality
        post_merge_hook = hooks_dir / "post-merge"
        if post_merge_hook.exists():
            content = post_merge_hook.read_text()
            assert "orchestration-tools" in content, "post-merge should reference orchestration-tools branch"

    def test_hook_orchestration_commit_tracking(self):
        """Test that hook orchestration commit tracking works."""
        commit_id_file = Path(".git/hooks/.orchestration_commit_id")
        # This file may or may not exist depending on installation state
        # Just check it doesn't contain invalid content if it exists
        if commit_id_file.exists():
            content = commit_id_file.read_text().strip()
            if content:
                # Should be a valid git commit hash
                assert len(content) >= 7, "Commit ID should be at least 7 characters"


class TestHookValidation:
    """Test hook validation functionality."""

    def test_hook_syntax_validation(self):
        """Test that installed hooks have valid bash syntax."""
        import subprocess
        hooks_dir = Path(".git/hooks")

        for hook_file in hooks_dir.glob("*"):
            if hook_file.is_file() and os.access(hook_file, os.X_OK):
                # Skip sample files and non-shell scripts
                if "sample" in hook_file.name or hook_file.suffix in [".py", ".js"]:
                    continue

                # Test bash syntax
                result = subprocess.run(["bash", "-n", str(hook_file)],
                                      capture_output=True, text=True)
                assert result.returncode == 0, f"Hook {hook_file.name} has syntax errors: {result.stderr}"

    def test_hook_permissions(self):
        """Test that hooks have correct permissions."""
        hooks_dir = Path(".git/hooks")

        for hook_file in hooks_dir.glob("*"):
            if (hook_file.is_file() and
            not hook_file.name.endswith(".sample") and
            not hook_file.name.startswith(".") and  # Exclude data files like .orchestration_commit_id
                hook_file.name in ["pre-commit", "post-commit", "post-merge", "post-checkout", "post-push"]):
                # Should be executable
                assert os.access(hook_file, os.X_OK), f"Hook {hook_file.name} should be executable"
