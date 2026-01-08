"""
Integration tests for CLI command system
"""

import pytest
from src.cli.commands.integration import (
    create_registry,
    create_command_factory,
    create_default_dependencies,
    get_command_dispatcher,
)


class TestCommandIntegration:
    """Integration tests for command system."""

    def test_create_default_dependencies(self):
        """Test that default dependencies function runs without error."""
        deps = create_default_dependencies()
        assert isinstance(deps, dict)

    def test_create_command_factory(self):
        """Test factory creation."""
        factory = create_command_factory()
        assert factory is not None

    def test_create_registry(self):
        """Test registry creation and command registration."""
        registry = create_registry()
        assert registry is not None

        # Check all commands are registered
        assert registry.has_command("analyze")
        assert registry.has_command("resolve")
        assert registry.has_command("validate")
        assert registry.has_command("analyze-history")
        assert registry.has_command("plan-rebase")

    def test_registry_agent_assignments(self):
        """Test that commands are assigned to correct agents."""
        registry = create_registry()

        assert registry.get_agent_for_command("analyze") == "agent-2"
        assert registry.get_agent_for_command("resolve") == "agent-3"
        assert registry.get_agent_for_command("validate") == "agent-4"
        assert registry.get_agent_for_command("analyze-history") == "agent-5"
        assert registry.get_agent_for_command("plan-rebase") == "agent-5"

    def test_get_available_commands(self):
        """Test getting all available commands."""
        registry = create_registry()
        commands = registry.get_available_commands()

        assert isinstance(commands, dict)
        assert "analyze" in commands
        assert "resolve" in commands
        assert "validate" in commands
        assert "analyze-history" in commands
        assert "plan-rebase" in commands

    def test_command_creation(self):
        """Test that commands can be created via registry."""
        registry = create_registry()

        analyze_cmd = registry.get_command("analyze")
        assert analyze_cmd is not None
        assert analyze_cmd.name == "analyze"

        validate_cmd = registry.get_command("validate")
        assert validate_cmd is not None
        assert validate_cmd.name == "validate"

    def test_get_command_invalid_name(self):
        """Test error when requesting non-existent command."""
        registry = create_registry()

        with pytest.raises(ValueError):
            registry.get_command("nonexistent")

    def test_get_commands_by_agent(self):
        """Test filtering commands by agent."""
        registry = create_registry()

        agent2_commands = registry.get_commands_by_agent("agent-2")
        assert "analyze" in agent2_commands
        assert len(agent2_commands) == 1

        agent5_commands = registry.get_commands_by_agent("agent-5")
        assert "analyze-history" in agent5_commands
        assert "plan-rebase" in agent5_commands
        assert len(agent5_commands) == 2

    def test_get_registry_status(self):
        """Test registry status reporting."""
        registry = create_registry()
        status = registry.get_registry_status()

        assert status["total_commands"] == 5
        assert "agent-2" in status["agents"]
        assert "agent-3" in status["agents"]
        assert "agent-4" in status["agents"]
        assert "agent-5" in status["agents"]
        assert status["agent_counts"]["agent-2"] == 1
        assert status["agent_counts"]["agent-5"] == 2

    def test_get_all_commands_metadata(self):
        """Test getting full command metadata."""
        registry = create_registry()
        metadata = registry.get_all_commands()

        assert isinstance(metadata, dict)
        assert "analyze" in metadata
        assert metadata["analyze"]["agent"] == "agent-2"
        assert metadata["analyze"]["class"] == "AnalyzeCommand"

    def test_dispatcher_function(self):
        """Test dispatcher function creation."""
        registry = create_registry()
        dispatcher = get_command_dispatcher(registry)

        assert callable(dispatcher)
