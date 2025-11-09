"""Integration tests for agent behavior adaptation functionality."""

import pytest
from pathlib import Path
import tempfile
import json

from src.context_control.core import ContextController
from src.context_control.agent import AgentAdapter
from src.context_control.config import ContextControlConfig, init_config
from src.context_control.models import ContextProfile, ProjectConfig


class TestAgentAdaptation:
    """Integration tests for agent behavior adaptation."""

    def test_agent_adapts_to_project_config(self):
        """Test that agents adapt behavior based on project configuration."""
        # Initialize global config
        init_config()

        # Setup project config
        project_config = ProjectConfig(
            project_name="test-python-project",
            project_type="python",
            enable_code_execution=True,
            enable_file_writing=True,
            max_context_length=8192
        )

        # Setup context profile
        profile = ContextProfile(
            id="test-profile",
            name="Test Profile",
            branch_patterns=["main"],
            allowed_files=["*.py"],
            blocked_files=["*.secret"],
            project_config=project_config
        )

        # Setup context controller
        controller = ContextController()

        # Mock the profile loading
        controller._load_all_profiles = lambda: [profile]

        # Create context
        context = controller.get_context_for_branch("main", "test-agent")

        # Create agent adapter
        adapter = AgentAdapter(context)

        # Test adaptations
        assert adapter.can_execute_code() is True
        assert adapter.can_write_files() is True
        assert adapter.get_max_context_length() == 8192
        assert "gpt-4" in adapter.get_preferred_models()  # Default models

    def test_different_projects_different_behavior(self):
        """Test that different project configurations lead to different agent behavior."""
        # Initialize global config
        init_config()

        # Python project
        python_config = ProjectConfig(
            project_name="python-proj",
            project_type="python",
            enable_code_execution=True,
            enable_shell_commands=False
        )

        # Web project
        web_config = ProjectConfig(
            project_name="web-proj",
            project_type="web",
            enable_code_execution=False,
            enable_file_writing=True
        )

        # Create contexts with different project configs
        python_profile = ContextProfile(
            id="python-profile",
            name="Python Profile",
            branch_patterns=["main"],
            project_config=python_config
        )

        web_profile = ContextProfile(
            id="web-profile",
            name="Web Profile",
            branch_patterns=["develop"],
            project_config=web_config
        )

        controller = ContextController()

        # Mock profile loading
        controller._load_all_profiles = lambda: [python_profile, web_profile]

        python_context = controller.get_context_for_branch("main", "agent1")
        web_context = controller.get_context_for_branch("develop", "agent1")

        python_adapter = AgentAdapter(python_context)
        web_adapter = AgentAdapter(web_context)

        # Different behaviors
        assert python_adapter.can_execute_code() is True
        assert web_adapter.can_execute_code() is False

        assert python_adapter.can_write_files() is False  # Default for python
        assert web_adapter.can_write_files() is True

    def test_agent_config_inheritance(self):
        """Test that agent configurations inherit from project settings."""
        # Initialize global config
        init_config()

        project_config = ProjectConfig(
            project_name="inheritance-test",
            project_type="api",
            max_context_length=4096,
            preferred_models=["gpt-4", "claude-3"]
        )

        profile = ContextProfile(
            id="inheritance-profile",
            name="Inheritance Profile",
            branch_patterns=["main"],
            agent_settings={"custom_timeout": 30},  # Agent-specific setting
            project_config=project_config
        )

        controller = ContextController()
        controller._load_all_profiles = lambda: [profile]

        context = controller.get_context_for_branch("main", "test-agent")
        adapter = AgentAdapter(context)

        settings = adapter.get_agent_settings()

        # Should inherit project settings
        assert settings['max_context_length'] == 4096
        assert "gpt-4" in settings['preferred_models']

        # Should include agent-specific settings
        assert settings['custom_timeout'] == 30

    def test_agent_config_override(self):
        """Test that agent-specific settings can override project defaults."""
        # Initialize global config
        init_config()

        project_config = ProjectConfig(
            project_name="override-test",
            project_type="library",
            max_context_length=4096
        )

        profile = ContextProfile(
            id="override-profile",
            name="Override Profile",
            branch_patterns=["main"],
            agent_settings={
                "test-agent": {"max_context_length": 8192}  # Override for specific agent
            },
            project_config=project_config
        )

        controller = ContextController()
        controller._load_all_profiles = lambda: [profile]

        context = controller.get_context_for_branch("main", "test-agent")
        adapter = AgentAdapter(context)

        # Agent-specific setting should override project default
        assert adapter.get_max_context_length() == 8192