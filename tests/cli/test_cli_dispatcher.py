"""Tests for the unified CLI dispatcher.

Before ``src/cli/main.py`` and ``src/cli/commands/__init__.py`` existed, every
command module under ``src/cli/commands/`` began with ``from ..interface import
Command`` and raised ``ModuleNotFoundError`` on import, so none of the 17
commands could be reached. These tests fail against that tree.

The async entry point is driven with ``asyncio.run`` rather than a pytest
async plugin, so the file runs under the plain pytest install.
"""

import asyncio
from argparse import Namespace

from src.cli.commands import Command, CommandFactory
from src.cli.main import COMMANDS, build_parser, build_registry, run_cli


def _command_class(name: str):
    return next(command for command, _agent in COMMANDS if command.__name__ == name)


def test_every_registered_command_is_a_command_subclass():
    for command_class, _agent in COMMANDS:
        assert issubclass(command_class, Command), command_class


def test_registry_registers_all_seventeen_commands():
    registry = build_registry()
    registered = registry.get_all_commands()
    assert len(registered) == len(COMMANDS) == 17
    assert len(set(registered)) == 17, "duplicate command names"


def test_each_command_name_is_unique_and_non_empty():
    names = [command_class().name for command_class, _agent in COMMANDS]
    assert all(names)
    assert len(names) == len(set(names))


def test_parser_builds_a_subparser_per_command():
    parser = build_parser(build_registry())
    assert parser.parse_args(["task-list"]).command == "task-list"


def test_factory_injects_declared_dependencies():
    class _Sentinel:
        pass

    sentinel = _Sentinel()
    factory = CommandFactory({"security_validator": sentinel})
    factory.register_command(_command_class("TaskmasterCommand"))
    command = factory.create_command("task-generate")
    assert command is not None
    assert getattr(command, "_security_validator", None) is sentinel


def test_unknown_dependency_resolves_to_none_rather_than_raising():
    factory = CommandFactory()
    factory.register_command(_command_class("AnalyzeCommand"))
    assert factory.create_command("git-analyze") is not None


def test_run_cli_without_a_command_prints_help_and_returns_zero(capsys):
    assert asyncio.run(run_cli([])) == 0
    assert "Available commands" in capsys.readouterr().out


def test_run_cli_executes_the_selected_command():
    assert asyncio.run(run_cli(["task-list"])) == 0


def test_registry_round_trips_agent_assignments():
    registry = build_registry()
    assert registry.get_agent_for_command("git-analyze") == "analyst"
    assert "git-analyze" in registry.get_commands_by_agent("analyst")


def test_parser_returns_a_namespace_with_parsed_arguments():
    """A guard against the dispatcher handing a dict where a Namespace is expected."""
    parser = build_parser(build_registry())
    parsed = parser.parse_args(["logic-compare", "a.py"])
    assert isinstance(parsed, Namespace)
    assert parsed.scripts == ["a.py"]
