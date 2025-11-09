"""Integration tests for context loading functionality."""

import pytest
from pathlib import Path
import tempfile
import json
from unittest.mock import patch, MagicMock

from src.context_control.core import ContextController
from src.context_control.models import ContextProfile, AgentContext
from src.context_control.config import ContextControlConfig
from src.context_control.exceptions import ContextNotFoundError


class TestContextLoading:
    """Integration tests for context loading."""

    def test_load_context_for_branch_with_profile(self):
        """Test loading context profile for a specific branch."""
        # Create a temporary profiles directory
        with tempfile.TemporaryDirectory() as temp_dir:
            profiles_dir = Path(temp_dir) / "profiles"
            profiles_dir.mkdir()

            # Create a test profile
            profile_data = {
                "id": "test-profile",
                "name": "Test Profile",
                "description": "A test profile",
                "branch_patterns": ["main", "master"],
                "allowed_files": ["*.py", "*.md"],
                "blocked_files": ["*.secret"],
                "agent_settings": {"max_tokens": 1000}
            }

            profile_file = profiles_dir / "test-profile.json"
            with open(profile_file, 'w') as f:
                json.dump(profile_data, f)

            # Create config
            config = ContextControlConfig(profiles_dir=profiles_dir)

            # Create controller
            controller = ContextController(config)

            # Test loading context
            context = controller.get_context_for_branch("main", "test-agent")

            assert context.profile_id == "test-profile"
            assert context.agent_id == "test-agent"
            assert context.environment_type == "production"
            assert "*.py" in context.accessible_files
            assert "*.secret" in context.restricted_files

    def test_context_not_found_for_unknown_branch(self):
        """Test that unknown branches raise ContextNotFoundError."""
        with tempfile.TemporaryDirectory() as temp_dir:
            profiles_dir = Path(temp_dir) / "profiles"
            profiles_dir.mkdir()

            config = ContextControlConfig(profiles_dir=profiles_dir)
            controller = ContextController(config)

            with pytest.raises(ContextNotFoundError):
                controller.get_context_for_branch("unknown-branch", "test-agent")

    @patch('src.context_control.environment.detect_branch')
    def test_context_caching(self, mock_detect_branch):
        """Test that contexts are cached for performance."""
        mock_detect_branch.return_value = "main"

        with tempfile.TemporaryDirectory() as temp_dir:
            profiles_dir = Path(temp_dir) / "profiles"
            profiles_dir.mkdir()

            # Create a test profile
            profile_data = {
                "id": "cached-profile",
                "name": "Cached Profile",
                "branch_patterns": ["main"],
                "allowed_files": ["*.py"],
                "blocked_files": []
            }

            profile_file = profiles_dir / "cached-profile.json"
            with open(profile_file, 'w') as f:
                json.dump(profile_data, f)

            config = ContextControlConfig(profiles_dir=profiles_dir)
            controller = ContextController(config)

            # First call should load from file
            context1 = controller.get_context_for_branch("main", "agent1")

            # Second call should use cache
            context2 = controller.get_context_for_branch("main", "agent1")

            # Should be the same object (from cache)
            assert context1 is context2

            # Different agent should create new context
            context3 = controller.get_context_for_branch("main", "agent2")
            assert context3 is not context1
            assert context3.agent_id == "agent2"

    def test_context_validation(self):
        """Test that loaded contexts are validated."""
        with tempfile.TemporaryDirectory() as temp_dir:
            profiles_dir = Path(temp_dir) / "profiles"
            profiles_dir.mkdir()

            # Create a test profile
            profile_data = {
                "id": "validation-profile",
                "name": "Validation Profile",
                "branch_patterns": ["test"],
                "allowed_files": ["*.py"],
                "blocked_files": ["secret.txt"]
            }

            profile_file = profiles_dir / "validation-profile.json"
            with open(profile_file, 'w') as f:
                json.dump(profile_data, f)

            config = ContextControlConfig(profiles_dir=profiles_dir)
            controller = ContextController(config)

            context = controller.get_context_for_branch("test", "test-agent")

            # Validate the context
            result = controller.validate_context(context)

            assert result.is_valid
            assert len(result.errors) == 0