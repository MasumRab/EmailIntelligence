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
