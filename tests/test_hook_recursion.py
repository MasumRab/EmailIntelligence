"""
Tests for Git hook recursion prevention and infinite loop protection.
"""

import os
import pytest
from pathlib import Path


class TestHookRecursionPrevention:
    """Test that Git hooks prevent infinite loops and recursive calls."""

    def test_post_checkout_recursion_prevention(self):
        """Test that post-checkout hook has recursion prevention."""
        hook_path = Path(".git/hooks/post-checkout")
        assert hook_path.exists(), "post-checkout hook should exist"

        content = hook_path.read_text()

        # Should check for recursion prevention environment variable
        assert "ORCHESTRATION_SYNC_ACTIVE" in content, \
            "post-checkout hook should check for recursion prevention"

        # Should exit early when recursion prevention is active
        assert "exit 0" in content, \
            "post-checkout hook should exit early to prevent recursion"

    def test_hook_recursion_safety_mechanisms(self):
        """Test that hooks performing git operations have safety mechanisms."""
        hooks_to_check = ["post-checkout", "post-merge"]

        for hook_name in hooks_to_check:
            hook_path = Path(f".git/hooks/{hook_name}")
            if hook_path.exists():
                content = hook_path.read_text()

                # Check for recursion prevention mechanisms
                has_recursion_check = (
                    "ORCHESTRATION_SYNC_ACTIVE" in content or
                    "sync operation" in content or
                    "recursive" in content.lower()
                )

                # If hook contains git checkout operations, it must prevent recursion
                if "git checkout" in content:
                    assert has_recursion_check, \
                        f"Hook {hook_name} performs git checkout but lacks recursion prevention"

                # If hook contains git operations, it should have safety checks
                if "git " in content and "checkout" in content:
                    assert has_recursion_check, \
                        f"Hook {hook_name} performs git operations but lacks recursion prevention"

    def test_hook_execution_safety(self):
        """Test that hooks can execute without causing infinite loops."""
        # This test ensures hooks don't recursively call themselves
        hook_path = Path(".git/hooks/post-checkout")

        if hook_path.exists():
            content = hook_path.read_text()

            # Count occurrences of potentially recursive operations
            checkout_count = content.count("git checkout")

            # If there are checkout operations, there must be recursion prevention
            if checkout_count > 0:
                assert "ORCHESTRATION_SYNC_ACTIVE" in content, \
                    f"Hook has {checkout_count} checkout operations but no recursion prevention"

    def test_environment_variable_protection(self):
        """Test that environment variable prevents hook execution."""
        hook_path = Path(".git/hooks/post-checkout")

        if hook_path.exists():
            # Test that hook respects the environment variable
            env_backup = os.environ.get("ORCHESTRATION_SYNC_ACTIVE")

            try:
                # Set the environment variable
                os.environ["ORCHESTRATION_SYNC_ACTIVE"] = "1"

                # Run the hook - it should exit early
                import subprocess
                result = subprocess.run([str(hook_path)], capture_output=True, text=True)

                # Should exit successfully without doing work
                assert result.returncode == 0, "Hook should exit cleanly when recursion prevention is active"

            finally:
                # Restore environment
                if env_backup is not None:
                    os.environ["ORCHESTRATION_SYNC_ACTIVE"] = env_backup
                elif "ORCHESTRATION_SYNC_ACTIVE" in os.environ:
                    del os.environ["ORCHESTRATION_SYNC_ACTIVE"]

    def test_hook_syntax_validation_with_recursion(self):
        """Test that hooks have valid syntax including recursion prevention."""
        import subprocess

        hooks_to_test = ["post-checkout", "post-merge"]

        for hook_name in hooks_to_test:
            hook_path = Path(f".git/hooks/{hook_name}")

            if hook_path.exists() and os.access(hook_path, os.X_OK):
                # Test bash syntax
                result = subprocess.run(["bash", "-n", str(hook_path)],
                                      capture_output=True, text=True)

                assert result.returncode == 0, \
                    f"Hook {hook_name} has syntax errors: {result.stderr}"

                # Additional validation for recursion prevention
                content = hook_path.read_text()
                if "git checkout" in content:
                    assert "ORCHESTRATION_SYNC_ACTIVE" in content, \
                        f"Hook {hook_name} has git checkout but missing recursion prevention"

    def test_worktree_subtree_detection(self):
        """Test that hooks can detect worktree vs subtree setup."""
        hook_path = Path(".git/hooks/post-checkout")

        if hook_path.exists():
            content = hook_path.read_text()

            # Should have worktree/subtree detection logic
            assert "IS_WORKTREE" in content, "Hook should detect worktree setup"
            assert "IS_SUBTREE" in content, "Hook should detect subtree setup"
            assert ".git" in content, "Hook should check .git directory/file for setup detection"

            # Should have warning messages for different setups
            assert "WARNING: Detected WORKTREE setup" in content, "Should warn about worktree detection"
            assert "WARNING: Detected SUBTREE setup" in content, "Should warn about subtree detection"
            assert "Consider using worktrees" in content, "Should suggest worktrees for subtrees"

    def test_conditional_sync_logic(self):
        """Test that hooks have conditional sync logic for different setups."""
        hook_path = Path(".git/hooks/post-checkout")

        if hook_path.exists():
            content = hook_path.read_text()

            # Should have conditional logic for worktree vs subtree
            has_conditional_logic = (
                "IS_WORKTREE" in content and "IS_SUBTREE" in content and
                ("perform_full_sync" in content or "conservative" in content)
            )

            if "git checkout" in content:
                assert has_conditional_logic, \
                    "Hook with git operations should have conditional sync logic for worktree/subtree"

    def test_worktree_safe_operations(self):
        """Test that worktree operations are considered safe."""
        hook_path = Path(".git/hooks/post-checkout")

        if hook_path.exists():
            content = hook_path.read_text()

            # Should indicate worktrees are safe for checkout operations
            if "IS_WORKTREE" in content and "git checkout" in content:
                # Check that worktrees have conditional logic for safe checkout
                # Worktrees should be able to checkout directly without extra conflict checks
                assert "IS_WORKTREE\" == true" in content, "Should have worktree-specific logic"
                assert "Worktrees: safe to checkout directly" in content, "Should indicate worktrees are safe"

                # Subtrees should have conflict checks, worktrees should not
                assert "git status --porcelain" in content, "Should check for conflicts in subtrees"
                assert "has local changes in subtree" in content, "Should warn about subtree conflicts"

    def test_disable_flag_functionality(self):
        """Test that the DISABLE_ORCHESTRATION_CHECKS flag works."""
        hook_path = Path(".git/hooks/post-checkout")

        if hook_path.exists():
            content = hook_path.read_text()

            # Should have disable flag check
            assert "DISABLE_ORCHESTRATION_CHECKS" in content, "Should check for disable flag"
            assert "Orchestration checks disabled" in content, "Should provide disable message"

            # Test that the flag actually works
            import subprocess
            import os

            # Save original env
            original_env = os.environ.get("DISABLE_ORCHESTRATION_CHECKS")

            try:
                # Set the disable flag
                os.environ["DISABLE_ORCHESTRATION_CHECKS"] = "1"

                # Run hook - should exit early with disable message
                result = subprocess.run([str(hook_path)], capture_output=True, text=True)

                # Should exit cleanly without doing sync work
                assert result.returncode == 0, "Hook should exit cleanly when disabled"
                assert "Orchestration checks disabled" in result.stdout, "Should show disable message"

            finally:
                # Restore environment
                if original_env is not None:
                    os.environ["DISABLE_ORCHESTRATION_CHECKS"] = original_env
                elif "DISABLE_ORCHESTRATION_CHECKS" in os.environ:
                    del os.environ["DISABLE_ORCHESTRATION_CHECKS"]

    def test_infinite_loop_prevention_on_branch_switch(self):
        """Test that hook prevents infinite loops when switching branches with orchestration changes."""
        hook_path = Path(".git/hooks/post-checkout")

        if hook_path.exists():
            content = hook_path.read_text()

            # Should have multiple levels of recursion prevention
            assert "ORCHESTRATION_SYNC_ACTIVE" in content, "Should check for sync active flag"

            # Should set the flag before doing git operations
            assert "export ORCHESTRATION_SYNC_ACTIVE=1" in content, "Should set sync active flag"

            # Should check for flag early in the script (within first 15 lines)
            lines = content.split('\n')
            early_checks = lines[:15]  # First 15 lines
            early_check_content = '\n'.join(early_checks)
            assert "ORCHESTRATION_SYNC_ACTIVE" in early_check_content, \
                "Should check recursion flag early in the script"

    def test_git_checkout_operations_are_protected(self):
        """Test that git checkout operations within hooks are protected from recursion."""
        hook_path = Path(".git/hooks/post-checkout")

        if hook_path.exists():
            content = hook_path.read_text()

            # Find all git checkout operations
            checkout_lines = [line for line in content.split('\n') if 'git checkout' in line]

            # Each checkout operation should be protected by the sync flag
            # The flag should be set before any checkout operations occur
            flag_setting_line = None
            for i, line in enumerate(content.split('\n')):
                if 'export ORCHESTRATION_SYNC_ACTIVE=1' in line:
                    flag_setting_line = i
                    break

            assert flag_setting_line is not None, "Should set ORCHESTRATION_SYNC_ACTIVE flag"

            # All git checkout operations should come after the flag is set
            for line in checkout_lines:
                line_index = content.find(line)
                # This is a rough check - in practice we'd need more sophisticated parsing
                assert flag_setting_line < content[:line_index].count('\n'), \
                    f"Git checkout operation '{line.strip()}' should come after sync flag is set"
