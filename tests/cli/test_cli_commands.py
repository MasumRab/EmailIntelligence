"""Tests for CLI command system."""

import pytest
from argparse import Namespace
from unittest.mock import MagicMock

from src.cli.commands.interface import Command
from src.cli.commands.factory import CommandFactory
from src.cli.commands.registry import CommandRegistry
from src.cli.commands.analyze_command import AnalyzeCommand
from src.cli.commands.resolve_command import ResolveCommand
from src.cli.commands.validate_command import ValidateCommand
from src.cli.commands.analyze_history_command import AnalyzeHistoryCommand
from src.cli.commands.plan_rebase_command import PlanRebaseCommand
from src.cli.commands.integration import (
    create_default_dependencies,
    create_command_factory,
    create_registry,
    get_command_dispatcher,
    add_modular_arguments,
    setup_modular_cli,
    handle_modular_command,
)


class TestCommandInterface:
    """Test the Command abstract base class."""

    def test_command_is_abstract(self):
        """Test that Command cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Command()


class TestCommandFactory:
    """Test the CommandFactory class."""

    def test_factory_initialization(self):
        """Test factory can be initialized without dependencies."""
        factory = CommandFactory()
        assert factory is not None
        assert factory._dependencies == {}

    def test_factory_with_dependencies(self):
        """Test factory can be initialized with custom dependencies."""
        deps = {"test_dep": MagicMock()}
        factory = CommandFactory(deps)
        assert factory._dependencies == deps

    def test_register_command(self):
        """Test registering a command class."""
        factory = CommandFactory()

        class TestCommand(Command):
            @property
            def name(self):
                return "test"

            @property
            def description(self):
                return "Test command"

            def add_arguments(self, parser):
                pass

            async def execute(self, args):
                return 0

            def get_dependencies(self):
                return {}

        factory.register_command(TestCommand)
        assert factory.has_command("test")

    def test_create_command(self):
        """Test creating a command instance."""
        factory = CommandFactory()

        class TestCommand(Command):
            @property
            def name(self):
                return "test"

            @property
            def description(self):
                return "Test command"

            def add_arguments(self, parser):
                pass

            async def execute(self, args):
                return 0

            def get_dependencies(self):
                return {}

        factory.register_command(TestCommand)
        command = factory.create_command("test")
        assert isinstance(command, TestCommand)

    def test_create_command_not_found(self):
        """Test creating a non-existent command returns None."""
        factory = CommandFactory()
        command = factory.create_command("nonexistent")
        assert command is None

    def test_get_available_commands(self):
        """Test getting all available commands."""
        factory = CommandFactory()

        class TestCommand(Command):
            @property
            def name(self):
                return "test"

            @property
            def description(self):
                return "Test command"

            def add_arguments(self, parser):
                pass

            async def execute(self, args):
                return 0

            def get_dependencies(self):
                return {}

        factory.register_command(TestCommand)
        commands = factory.get_available_commands()
        assert "test" in commands
        assert commands["test"] == "Test command"

    def test_has_command(self):
        """Test checking if a command exists."""
        factory = CommandFactory()

        class TestCommand(Command):
            @property
            def name(self):
                return "test"

            @property
            def description(self):
                return "Test command"

            def add_arguments(self, parser):
                pass

            async def execute(self, args):
                return 0

            def get_dependencies(self):
                return {}

        factory.register_command(TestCommand)
        assert factory.has_command("test")
        assert not factory.has_command("nonexistent")

    def test_command_dependency_injection(self):
        """Test that dependencies are injected into commands."""

        class TestCommand(Command):
            @property
            def name(self):
                return "test"

            @property
            def description(self):
                return "Test command"

            def add_arguments(self, parser):
                pass

            async def execute(self, args):
                return 0

            def get_dependencies(self):
                return {"my_dep": str}

            def set_dependencies(self, deps):
                self.deps = deps

        deps = {"my_dep": "test_value"}
        factory = CommandFactory(deps)
        factory.register_command(TestCommand)

        command = factory.create_command("test")
        assert hasattr(command, "deps")
        assert command.deps.get("my_dep") == "test_value"


class TestCommandRegistry:
    """Test the CommandRegistry class."""

    def test_registry_initialization(self):
        """Test registry can be initialized with a factory."""
        factory = CommandFactory()
        registry = CommandRegistry(factory)
        assert registry._factory is factory

    def test_register_command(self):
        """Test registering a command with the registry."""
        factory = CommandFactory()
        registry = CommandRegistry(factory)

        class TestCommand(Command):
            @property
            def name(self):
                return "test"

            @property
            def description(self):
                return "Test command"

            def add_arguments(self, parser):
                pass

            async def execute(self, args):
                return 0

            def get_dependencies(self):
                return {}

        registry.register_command(TestCommand, "test-agent")
        assert registry.has_command("test")

    def test_get_command(self):
        """Test getting a command from the registry."""
        factory = CommandFactory()
        registry = CommandRegistry(factory)

        class TestCommand(Command):
            @property
            def name(self):
                return "test"

            @property
            def description(self):
                return "Test command"

            def add_arguments(self, parser):
                pass

            async def execute(self, args):
                return 0

            def get_dependencies(self):
                return {}

        registry.register_command(TestCommand)
        command = registry.get_command("test")
        assert isinstance(command, TestCommand)

    def test_get_command_not_found(self):
        """Test getting a non-existent command raises error."""
        factory = CommandFactory()
        registry = CommandRegistry(factory)

        with pytest.raises(ValueError, match="not registered"):
            registry.get_command("nonexistent")

    def test_get_agent_for_command(self):
        """Test getting the agent assigned to a command."""
        factory = CommandFactory()
        registry = CommandRegistry(factory)

        class TestCommand(Command):
            @property
            def name(self):
                return "test"

            @property
            def description(self):
                return "Test command"

            def add_arguments(self, parser):
                pass

            async def execute(self, args):
                return 0

            def get_dependencies(self):
                return {}

        registry.register_command(TestCommand, "my-agent")
        assert registry.get_agent_for_command("test") == "my-agent"

    def test_get_agent_for_unknown_command(self):
        """Test getting agent for unknown command returns 'system'."""
        factory = CommandFactory()
        registry = CommandRegistry(factory)
        assert registry.get_agent_for_command("unknown") == "system"

    def test_get_commands_by_agent(self):
        """Test getting all commands for a specific agent."""
        factory = CommandFactory()
        registry = CommandRegistry(factory)

        class TestCommand1(Command):
            @property
            def name(self):
                return "test1"

            @property
            def description(self):
                return "Test 1"

            def add_arguments(self, parser):
                pass

            async def execute(self, args):
                return 0

            def get_dependencies(self):
                return {}

        class TestCommand2(Command):
            @property
            def name(self):
                return "test2"

            @property
            def description(self):
                return "Test 2"

            def add_arguments(self, parser):
                pass

            async def execute(self, args):
                return 0

            def get_dependencies(self):
                return {}

        registry.register_command(TestCommand1, "agent-1")
        registry.register_command(TestCommand2, "agent-1")

        commands = registry.get_commands_by_agent("agent-1")
        assert "test1" in commands
        assert "test2" in commands

    def test_get_all_commands(self):
        """Test getting metadata for all commands."""
        factory = CommandFactory()
        registry = CommandRegistry(factory)

        class TestCommand(Command):
            @property
            def name(self):
                return "test"

            @property
            def description(self):
                return "Test command"

            def add_arguments(self, parser):
                pass

            async def execute(self, args):
                return 0

            def get_dependencies(self):
                return {}

        registry.register_command(TestCommand, "test-agent")
        all_commands = registry.get_all_commands()
        assert "test" in all_commands
        assert all_commands["test"]["description"] == "Test command"
        assert all_commands["test"]["agent"] == "test-agent"

    def test_get_available_commands(self):
        """Test getting all available commands with descriptions."""
        factory = CommandFactory()
        registry = CommandRegistry(factory)

        class TestCommand(Command):
            @property
            def name(self):
                return "test"

            @property
            def description(self):
                return "Test command"

            def add_arguments(self, parser):
                pass

            async def execute(self, args):
                return 0

            def get_dependencies(self):
                return {}

        registry.register_command(TestCommand)
        commands = registry.get_available_commands()
        assert "test" in commands

    def test_get_registry_status(self):
        """Test getting comprehensive registry status."""
        factory = CommandFactory()
        registry = CommandRegistry(factory)

        class TestCommand(Command):
            @property
            def name(self):
                return "test"

            @property
            def description(self):
                return "Test command"

            def add_arguments(self, parser):
                pass

            async def execute(self, args):
                return 0

            def get_dependencies(self):
                return {}

        registry.register_command(TestCommand, "agent-1")
        status = registry.get_registry_status()
        assert status["total_commands"] == 1
        assert "agent-1" in status["agents"]


class TestAnalyzeCommand:
    """Test the AnalyzeCommand class."""

    def test_command_properties(self):
        """Test command name and description."""
        cmd = AnalyzeCommand()
        assert cmd.name == "analyze"
        assert cmd.description == "Analyze repository conflicts between branches"

    def test_get_dependencies(self):
        """Test getting command dependencies."""
        cmd = AnalyzeCommand()
        deps = cmd.get_dependencies()
        assert "conflict_detector" in deps
        assert "analyzer" in deps
        assert "strategy_generator" in deps
        assert "repository_ops" in deps

    def test_set_dependencies(self):
        """Test setting command dependencies."""
        cmd = AnalyzeCommand()
        deps = {
            "conflict_detector": MagicMock(),
            "analyzer": MagicMock(),
            "strategy_generator": MagicMock(),
            "repository_ops": MagicMock(),
        }
        cmd.set_dependencies(deps)
        assert cmd._detector is deps["conflict_detector"]
        assert cmd._analyzer is deps["analyzer"]

    @pytest.mark.asyncio
    async def test_execute_nonexistent_repo(self):
        """Test execute fails for non-existent repository."""
        cmd = AnalyzeCommand()
        args = Namespace(repo_path="/nonexistent/path", pr_id=None, base_branch="main", head_branch=None)
        result = await cmd.execute(args)
        assert result == 1


class TestResolveCommand:
    """Test the ResolveCommand class."""

    def test_command_properties(self):
        """Test command name and description."""
        cmd = ResolveCommand()
        assert cmd.name == "resolve"
        assert cmd.description == "Resolve a specific conflict using a strategy"

    def test_get_dependencies(self):
        """Test getting command dependencies."""
        cmd = ResolveCommand()
        deps = cmd.get_dependencies()
        assert "resolver" in deps
        assert "validator" in deps

    @pytest.mark.asyncio
    async def test_execute_success(self):
        """Test successful resolve execution."""
        cmd = ResolveCommand()
        args = Namespace(conflict_id="test-conflict", strategy_id="test-strategy")
        result = await cmd.execute(args)
        assert result == 0


class TestValidateCommand:
    """Test the ValidateCommand class."""

    def test_command_properties(self):
        """Test command name and description."""
        cmd = ValidateCommand()
        assert cmd.name == "validate"
        assert cmd.description == "Run validation checks on the codebase"

    def test_get_dependencies(self):
        """Test getting command dependencies."""
        cmd = ValidateCommand()
        deps = cmd.get_dependencies()
        assert "validator" in deps

    @pytest.mark.asyncio
    async def test_execute_no_validator(self):
        """Test execute with no validator set."""
        cmd = ValidateCommand()
        args = Namespace()
        result = await cmd.execute(args)
        # Should fail because validator is None
        assert result == 1


class TestAnalyzeHistoryCommand:
    """Test the AnalyzeHistoryCommand class."""

    def test_command_properties(self):
        """Test command name and description."""
        cmd = AnalyzeHistoryCommand()
        assert cmd.name == "analyze-history"
        assert cmd.description == "Analyze git commit history and patterns"

    def test_get_dependencies(self):
        """Test getting command dependencies."""
        cmd = AnalyzeHistoryCommand()
        deps = cmd.get_dependencies()
        assert "history" in deps
        assert "classifier" in deps


class TestPlanRebaseCommand:
    """Test the PlanRebaseCommand class."""

    def test_command_properties(self):
        """Test command name and description."""
        cmd = PlanRebaseCommand()
        assert cmd.name == "plan-rebase"
        assert cmd.description == "Generate optimal rebase plan for a branch"

    def test_get_dependencies(self):
        """Test getting command dependencies."""
        cmd = PlanRebaseCommand()
        deps = cmd.get_dependencies()
        assert "history" in deps
        assert "classifier" in deps
        assert "planner" in deps


class TestIntegration:
    """Test CLI integration functions."""

    def test_create_default_dependencies(self):
        """Test creating default dependencies."""
        deps = create_default_dependencies()
        # Should have keys but many will be None due to import errors
        assert isinstance(deps, dict)

    def test_create_command_factory(self):
        """Test creating command factory."""
        factory = create_command_factory()
        assert factory is not None
        assert isinstance(factory, CommandFactory)

    def test_create_command_factory_with_deps(self):
        """Test creating command factory with custom deps."""
        custom_deps = {"custom": MagicMock()}
        factory = create_command_factory(custom_deps)
        assert factory._dependencies.get("custom") is custom_deps["custom"]

    def test_create_registry(self):
        """Test creating command registry."""
        registry = create_registry()
        assert registry is not None
        assert isinstance(registry, CommandRegistry)

    def test_get_command_dispatcher(self):
        """Test getting command dispatcher."""
        dispatcher = get_command_dispatcher()
        assert callable(dispatcher)

    def test_add_modular_arguments(self):
        """Test adding modular arguments to subparsers."""
        # Create a mock subparsers object
        mock_subparsers = MagicMock()
        mock_parser = MagicMock()
        mock_subparsers.add_parser.return_value = mock_parser

        result = add_modular_arguments(mock_subparsers)
        assert isinstance(result, dict)

    def test_setup_modular_cli(self):
        """Test setting up modular CLI."""
        mock_parser = MagicMock()
        mock_subparsers = MagicMock()
        mock_parser.add_subparsers.return_value = mock_subparsers

        modular_subparsers, legacy_parser = setup_modular_cli(mock_parser)
        assert modular_subparsers is not None
        assert legacy_parser is not None

    def test_handle_modular_command_no_command(self):
        """Test handling modular command with no command set."""
        args = Namespace(modular_command=None)
        result = handle_modular_command(args)
        assert result == 0

    def test_handle_modular_command_with_dispatcher(self):
        """Test handling modular command with custom dispatcher."""
        args = Namespace(modular_command="test")
        mock_dispatcher = MagicMock(return_value=0)
        result = handle_modular_command(args, dispatcher=mock_dispatcher)
        mock_dispatcher.assert_called_once()