"""Unit and integration tests for the context control module."""

import pytest
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from context_control import (
    init_config,
    ContextController,
    ContextValidator,
    detect_branch,
    get_current_branch,
    is_git_repository,
    ContextProfile,
    AgentContext,
    ContextValidationResult
)
from context_control.exceptions import ContextNotFoundError, ContextValidationError


class TestContextControl:
    """Test suite for context control functionality."""

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Set up test environment."""
        # Initialize config for each test
        init_config()

    def test_config_initialization(self):
        """Test that configuration initializes properly."""
        from context_control.config import get_current_config
        config = get_current_config()
        assert config is not None
        assert hasattr(config, 'log_level')
        assert hasattr(config, 'profiles_dir')

    def test_branch_detection(self):
        """Test branch detection functionality."""
        branch = detect_branch()
        assert isinstance(branch, str)
        assert len(branch) > 0

        # Test current branch function
        current_branch = get_current_branch()
        assert isinstance(current_branch, str)
        assert current_branch == branch

    def test_git_repository_detection(self):
        """Test git repository detection."""
        is_git = is_git_repository()
        assert isinstance(is_git, bool)
        # Should be True since we're in a git repo
        assert is_git is True

    def test_context_controller_creation(self):
        """Test ContextController can be created."""
        controller = ContextController()
        assert controller is not None
        assert hasattr(controller, 'get_context_for_branch')

    def test_context_retrieval_scientific_branch(self):
        """Test context retrieval for scientific branch."""
        controller = ContextController()
        context = controller.get_context_for_branch('scientific')

        assert isinstance(context, AgentContext)
        assert context.profile_id == 'scientific'
        assert context.agent_id == 'default'

    def test_context_retrieval_main_branch(self):
        """Test context retrieval for main branch."""
        controller = ContextController()
        context = controller.get_context_for_branch('main')

        assert isinstance(context, AgentContext)
        assert context.profile_id == 'main'
        assert context.agent_id == 'default'

    def test_context_caching(self):
        """Test that contexts are cached properly."""
        controller = ContextController()

        # First call
        context1 = controller.get_context_for_branch('scientific')
        # Second call should return cached version
        context2 = controller.get_context_for_branch('scientific')

        assert context1 is context2  # Same object from cache

    def test_invalid_branch_raises_error(self):
        """Test that invalid branch raises ContextNotFoundError."""
        controller = ContextController()

        with pytest.raises(ContextNotFoundError):
            controller.get_context_for_branch('nonexistent-branch')

    def test_context_validator_creation(self):
        """Test ContextValidator can be created."""
        validator = ContextValidator()
        assert validator is not None

    def test_context_profile_loading(self):
        """Test that context profiles load correctly."""
        from context_control.storage import ProfileStorage

        storage = ProfileStorage()
        profiles = storage.load_all_profiles()

        assert len(profiles) >= 2  # Should have at least scientific and main

        # Check scientific profile
        scientific_profile = next((p for p in profiles if p.id == 'scientific'), None)
        assert scientific_profile is not None
        assert 'scientific' in scientific_profile.branch_patterns

        # Check main profile
        main_profile = next((p for p in profiles if p.id == 'main'), None)
        assert main_profile is not None
        assert 'main' in main_profile.branch_patterns

    def test_agent_context_creation(self):
        """Test AgentContext creation with different parameters."""
        controller = ContextController()

        # Test with custom agent_id
        context = controller.get_context_for_branch('scientific', agent_id='test-agent')
        assert context.agent_id == 'test-agent'
        assert context.profile_id == 'scientific'

    @pytest.mark.integration
    def test_full_context_workflow(self):
        """Integration test for full context workflow."""
        # Detect current branch
        branch = detect_branch()

        # Create controller
        controller = ContextController()

        # Get context
        context = controller.get_context_for_branch(branch)

        # Validate context has required attributes
        assert hasattr(context, 'profile_id')
        assert hasattr(context, 'agent_id')
        assert hasattr(context, 'accessible_files')
        assert hasattr(context, 'restricted_files')
        assert hasattr(context, 'agent_settings')

        # Test context validator
        validator = ContextValidator()
        # Basic validation - should not raise errors
        assert validator is not None


if __name__ == '__main__':
    pytest.main([__file__])