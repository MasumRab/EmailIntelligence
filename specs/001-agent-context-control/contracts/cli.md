# CLI Contracts: Agent Context Control

**Date**: 2025-11-10 | **API Contracts**: specs/001-agent-context-control/contracts/api.md

## Overview

This document specifies the command-line interface contracts for the Agent Context Control system. The CLI provides comprehensive management capabilities for context profiles and system operations.

## Command Structure

### Base Command Interface

```python
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from argparse import ArgumentParser, Namespace

class CLICommand(ABC):
    """Base class for all CLI commands."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Command name."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Command description."""
        ...

    @abstractmethod
    def add_arguments(self, parser: ArgumentParser) -> None:
        """
        Add command-specific arguments to parser.

        Args:
            parser: Argument parser to extend
        """
        ...

    @abstractmethod
    def execute(self, args: Namespace) -> int:
        """
        Execute the command.

        Args:
            args: Parsed command arguments

        Returns:
            int: Exit code (0 for success, non-zero for errors)
        """
        ...

    def format_output(self, data: Any, format: str = "text") -> str:
        """
        Format command output.

        Args:
            data: Data to format
            format: Output format (text, json, yaml)

        Returns:
            str: Formatted output
        """
        if format == "json":
            import json
            return json.dumps(data, indent=2, default=str)
        elif format == "yaml":
            try:
                import yaml
                return yaml.dump(data, default_flow_style=False)
            except ImportError:
                return json.dumps(data, indent=2, default=str)
        else:
            return str(data)
```

## Core Commands

### Init Command

Initialize context control in a project.

```python
class InitCommand(CLICommand):
    """Initialize context control in current directory."""

    @property
    def name(self) -> str:
        return "init"

    @property
    def description(self) -> str:
        return "Initialize context control in current directory"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--context-dir",
            default=".agent-context",
            help="Directory for context profiles"
        )
        parser.add_argument(
            "--encrypt",
            action="store_true",
            help="Enable encryption for sensitive data"
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing configuration"
        )

    def execute(self, args: Namespace) -> int:
        """Initialize context control."""
        try:
            # Create context directory
            context_dir = Path(args.context_dir)
            context_dir.mkdir(parents=True, exist_ok=args.force)

            # Create default configuration
            config = ContextControlConfig(
                context_dir=context_dir,
                encryption_enabled=args.encrypt
            )

            # Save configuration
            config_path = Path(".context-control.yaml")
            with open(config_path, 'w') as f:
                import yaml
                yaml.dump(config.dict(), f)

            # Create example context
            self._create_example_context(context_dir)

            print(f"✓ Context control initialized in {context_dir}")
            print(f"✓ Configuration saved to {config_path}")
            print("\nNext steps:")
            print("1. Edit context profiles in .agent-context/")
            print("2. Run 'context-control create' to add more contexts")
            print("3. Run 'context-control current' to test detection")

            return 0

        except Exception as e:
            print(f"✗ Initialization failed: {e}")
            return 1

    def _create_example_context(self, context_dir: Path) -> None:
        """Create example context profile."""
        example_profile = ContextProfile(
            context_id="main-development",
            branch="main",
            environment="development",
            agent_config={
                "max_concurrent_tasks": 3,
                "timeout_seconds": 60
            },
            feature_flags={
                "debug_mode": True
            }
        )

        profile_path = context_dir / "main-development.json"
        with open(profile_path, 'w') as f:
            import json
            json.dump(example_profile.dict(), f, indent=2)
```

### Current Command

Show current context information.

```python
class CurrentCommand(CLICommand):
    """Show current context information."""

    @property
    def name(self) -> str:
        return "current"

    @property
    def description(self) -> str:
        return "Show current context information"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--format",
            choices=["text", "json", "yaml"],
            default="text",
            help="Output format"
        )
        parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            help="Show detailed information"
        )

    def execute(self, args: Namespace) -> int:
        """Show current context."""
        try:
            controller = self._get_controller()
            context = controller.get_context()

            if args.format == "text":
                self._print_text_context(context, args.verbose)
            else:
                output = self.format_output(context.dict(), args.format)
                print(output)

            return 0

        except Exception as e:
            print(f"✗ Failed to get current context: {e}")
            return 1

    def _print_text_context(self, context: AgentContext, verbose: bool) -> None:
        """Print context in human-readable format."""
        print(f"Context ID: {context.context_id}")
        print(f"Environment: {context.environment}")
        print(f"Max Tasks: {context.max_concurrent_tasks}")
        print(f"Timeout: {context.timeout_seconds}s")
        print(f"Memory Limit: {context.memory_limit_mb}MB")

        if context.feature_flags:
            print("\nFeature Flags:")
            for flag, enabled in context.feature_flags.items():
                status = "✓" if enabled else "✗"
                print(f"  {status} {flag}")

        if verbose:
            print(f"\nCreated: {context.created_at}")
            if context.branch_info:
                print("\nBranch Info:")
                for key, value in context.branch_info.items():
                    print(f"  {key}: {value}")

    def _get_controller(self) -> ContextController:
        """Get configured context controller."""
        # Implementation would load from configuration
        return DefaultContextController()
```

### List Command

List all available contexts.

```python
class ListCommand(CLICommand):
    """List all available context profiles."""

    @property
    def name(self) -> str:
        return "list"

    @property
    def description(self) -> str:
        return "List all available context profiles"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--format",
            choices=["text", "json", "yaml"],
            default="text",
            help="Output format"
        )
        parser.add_argument(
            "--current",
            action="store_true",
            help="Highlight current context"
        )
        parser.add_argument(
            "--filter",
            help="Filter contexts by environment (e.g., development,production)"
        )

    def execute(self, args: Namespace) -> int:
        """List all contexts."""
        try:
            controller = self._get_controller()
            contexts = controller.list_contexts()

            # Apply filters
            if args.filter:
                environments = args.filter.split(",")
                contexts = {
                    cid: profile
                    for cid, profile in contexts.items()
                    if profile.environment in environments
                }

            # Get current context for highlighting
            current_id = None
            if args.current:
                try:
                    current_context = controller.get_context()
                    current_id = current_context.context_id
                except Exception:
                    pass  # Ignore errors when getting current context

            if args.format == "text":
                self._print_text_contexts(contexts, current_id)
            else:
                output = self.format_output(contexts, args.format)
                print(output)

            return 0

        except Exception as e:
            print(f"✗ Failed to list contexts: {e}")
            return 1

    def _print_text_contexts(
        self,
        contexts: Dict[str, ContextProfile],
        current_id: Optional[str]
    ) -> None:
        """Print contexts in table format."""
        if not contexts:
            print("No context profiles found.")
            return

        print(f"Found {len(contexts)} context profile(s):")
        print()

        # Header
        print("<15")
        print("-" * 60)

        # Rows
        for context_id, profile in contexts.items():
            marker = "→" if context_id == current_id else " "
            print("<15")

    def _get_controller(self) -> ContextController:
        """Get configured context controller."""
        return DefaultContextController()
```

### Create Command

Create a new context profile.

```python
class CreateCommand(CLICommand):
    """Create a new context profile."""

    @property
    def name(self) -> str:
        return "create"

    @property
    def description(self) -> str:
        return "Create a new context profile"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--interactive", "-i",
            action="store_true",
            help="Interactive mode"
        )
        parser.add_argument(
            "--template",
            choices=["development", "staging", "production", "ci"],
            help="Use template for environment"
        )
        parser.add_argument(
            "--branch",
            help="Branch name for context"
        )
        parser.add_argument(
            "--environment",
            choices=["development", "staging", "production", "ci"],
            help="Environment type"
        )
        parser.add_argument(
            "--output", "-o",
            help="Output file path (default: auto-generated)"
        )

    def execute(self, args: Namespace) -> int:
        """Create new context profile."""
        try:
            if args.interactive:
                profile = self._create_interactive()
            elif args.template:
                profile = self._create_from_template(args.template, args.branch)
            else:
                profile = self._create_manual(args)

            # Validate profile
            controller = self._get_controller()
            validation = controller.validator.validate_profile(profile)
            if not validation.is_valid:
                print("✗ Context validation failed:")
                for error in validation.errors:
                    print(f"  - {error.message}")
                return 1

            # Save profile
            storage = controller.storage
            storage.save_context(profile)

            print(f"✓ Created context profile: {profile.context_id}")
            print(f"  File: {controller.context_dir}/{profile.context_id}.json")

            return 0

        except Exception as e:
            print(f"✗ Failed to create context: {e}")
            return 1

    def _create_interactive(self) -> ContextProfile:
        """Create profile through interactive prompts."""
        print("Creating new context profile interactively...")
        print()

        context_id = input("Context ID: ").strip()
        branch = input("Branch name: ").strip()
        environment = self._prompt_environment()

        # Agent config
        print("\nAgent Configuration:")
        max_tasks = int(input("Max concurrent tasks (default 5): ") or "5")
        timeout = int(input("Timeout seconds (default 300): ") or "300")
        memory = int(input("Memory limit MB (default 1024): ") or "1024")

        # Feature flags
        feature_flags = {}
        if input("\nAdd feature flags? (y/N): ").lower().startswith('y'):
            while True:
                flag = input("Feature flag (empty to finish): ").strip()
                if not flag:
                    break
                enabled = input(f"Enable {flag}? (y/N): ").lower().startswith('y')
                feature_flags[flag] = enabled

        return ContextProfile(
            context_id=context_id,
            branch=branch,
            environment=environment,
            agent_config={
                "max_concurrent_tasks": max_tasks,
                "timeout_seconds": timeout,
                "memory_limit_mb": memory
            },
            feature_flags=feature_flags
        )

    def _create_from_template(self, template: str, branch: Optional[str]) -> ContextProfile:
        """Create profile from template."""
        templates = {
            "development": {
                "environment": "development",
                "agent_config": {"max_concurrent_tasks": 3, "timeout_seconds": 60},
                "feature_flags": {"debug_mode": True, "performance_monitoring": False}
            },
            "staging": {
                "environment": "staging",
                "agent_config": {"max_concurrent_tasks": 5, "timeout_seconds": 120},
                "feature_flags": {"debug_mode": False, "performance_monitoring": True}
            },
            "production": {
                "environment": "production",
                "agent_config": {"max_concurrent_tasks": 10, "timeout_seconds": 300},
                "feature_flags": {"debug_mode": False, "performance_monitoring": True}
            },
            "ci": {
                "environment": "ci",
                "agent_config": {"max_concurrent_tasks": 1, "timeout_seconds": 600},
                "feature_flags": {"debug_mode": False, "performance_monitoring": True}
            }
        }

        config = templates[template]
        context_id = f"{branch or 'unknown'}-{template}"

        return ContextProfile(
            context_id=context_id,
            branch=branch or "unknown",
            environment=config["environment"],
            agent_config=config["agent_config"],
            feature_flags=config["feature_flags"]
        )

    def _create_manual(self, args: Namespace) -> ContextProfile:
        """Create profile from command arguments."""
        if not args.branch or not args.environment:
            raise ValueError("--branch and --environment required for manual creation")

        context_id = f"{args.branch}-{args.environment}"

        return ContextProfile(
            context_id=context_id,
            branch=args.branch,
            environment=args.environment
        )

    def _prompt_environment(self) -> str:
        """Prompt for environment selection."""
        environments = ["development", "staging", "production", "ci"]
        print("\nEnvironment:")
        for i, env in enumerate(environments, 1):
            print(f"  {i}. {env}")

        while True:
            try:
                choice = int(input("Select environment (1-4): "))
                if 1 <= choice <= len(environments):
                    return environments[choice - 1]
            except ValueError:
                pass
            print("Invalid choice. Please select 1-4.")

    def _get_controller(self) -> ContextController:
        """Get configured context controller."""
        return DefaultContextController()
```

### Validate Command

Validate context profiles.

```python
class ValidateCommand(CLICommand):
    """Validate context profiles."""

    @property
    def name(self) -> str:
        return "validate"

    @property
    def description(self) -> str:
        return "Validate context profiles"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "files",
            nargs="*",
            help="Specific files to validate (default: all)"
        )
        parser.add_argument(
            "--format",
            choices=["text", "json", "yaml"],
            default="text",
            help="Output format"
        )
        parser.add_argument(
            "--strict",
            action="store_true",
            help="Fail on warnings"
        )

    def execute(self, args: Namespace) -> int:
        """Validate context profiles."""
        try:
            controller = self._get_controller()
            validator = controller.validator

            results = {}

            if args.files:
                # Validate specific files
                for file_path in args.files:
                    profile = self._load_profile_from_file(file_path)
                    result = validator.validate_profile(profile)
                    results[file_path] = result
            else:
                # Validate all contexts
                contexts = controller.list_contexts()
                for context_id, profile in contexts.items():
                    result = validator.validate_profile(profile)
                    results[context_id] = result

            # Check for failures
            has_errors = any(not result.is_valid for result in results.values())
            has_warnings = any(result.warnings for result in results.values())

            if args.format == "text":
                self._print_validation_results(results, has_errors, has_warnings)
            else:
                output = self.format_output(results, args.format)
                print(output)

            # Return appropriate exit code
            if has_errors or (args.strict and has_warnings):
                return 1
            return 0

        except Exception as e:
            print(f"✗ Validation failed: {e}")
            return 1

    def _print_validation_results(
        self,
        results: Dict[str, ContextValidationResult],
        has_errors: bool,
        has_warnings: bool
    ) -> None:
        """Print validation results in human-readable format."""
        total = len(results)
        valid = sum(1 for r in results.values() if r.is_valid)
        invalid = total - valid

        print(f"Validated {total} context profile(s)")
        print(f"✓ Valid: {valid}")
        if invalid > 0:
            print(f"✗ Invalid: {invalid}")
        if has_warnings:
            print(f"⚠ Warnings: {sum(len(r.warnings) for r in results.values())}")

        print()

        for name, result in results.items():
            if result.is_valid and not result.warnings:
                print(f"✓ {name}")
            elif result.is_valid and result.warnings:
                print(f"⚠ {name}")
                for warning in result.warnings:
                    print(f"  - Warning: {warning}")
            else:
                print(f"✗ {name}")
                for error in result.errors:
                    print(f"  - Error: {error.message}")

    def _load_profile_from_file(self, file_path: str) -> ContextProfile:
        """Load profile from file path."""
        import json
        with open(file_path, 'r') as f:
            data = json.load(f)
        return ContextProfile(**data)

    def _get_controller(self) -> ContextController:
        """Get configured context controller."""
        return DefaultContextController()
```

## Main CLI Application

### ContextControlCLI

Main CLI application class.

```python
import sys
from argparse import ArgumentParser
from typing import List

from .commands import (
    InitCommand, CurrentCommand, ListCommand,
    CreateCommand, ValidateCommand
)

class ContextControlCLI:
    """Main CLI application for context control."""

    def __init__(self):
        """Initialize CLI with all commands."""
        self.commands = {
            "init": InitCommand(),
            "current": CurrentCommand(),
            "list": ListCommand(),
            "create": CreateCommand(),
            "validate": ValidateCommand(),
        }

    def main(self, args: Optional[List[str]] = None) -> int:
        """
        Main CLI entry point.

        Args:
            args: Command line arguments (default: sys.argv[1:])

        Returns:
            int: Exit code
        """
        if args is None:
            args = sys.argv[1:]

        parser = ArgumentParser(
            prog="context-control",
            description="Agent Context Control CLI"
        )

        parser.add_argument(
            "--version",
            action="version",
            version="%(prog)s 1.0.0"
        )

        parser.add_argument(
            "--config",
            help="Path to configuration file"
        )

        # Add subcommands
        subparsers = parser.add_subparsers(
            dest="command",
            help="Available commands"
        )

        for name, command in self.commands.items():
            subparser = subparsers.add_parser(
                name,
                help=command.description
            )
            command.add_arguments(subparser)

        # Parse arguments
        parsed_args = parser.parse_args(args)

        if not parsed_args.command:
            parser.print_help()
            return 0

        # Execute command
        command = self.commands[parsed_args.command]
        try:
            return command.execute(parsed_args)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            return 130
        except Exception as e:
            print(f"Unexpected error: {e}")
            return 1

# CLI entry point
def main():
    """CLI entry point."""
    cli = ContextControlCLI()
    sys.exit(cli.main())
```

## Error Handling

### CLI Error Classes

```python
class CLIError(Exception):
    """Base CLI error."""

    def __init__(self, message: str, exit_code: int = 1):
        super().__init__(message)
        self.exit_code = exit_code

class CommandNotFoundError(CLIError):
    """Command not found error."""
    pass

class ValidationError(CLIError):
    """Validation error."""
    pass

class FileOperationError(CLIError):
    """File operation error."""
    pass
```

## Testing Contracts

### CLI Testing Utilities

```python
import tempfile
from pathlib import Path
from typing import List

class CLITestHarness:
    """Test harness for CLI commands."""

    def __init__(self):
        """Initialize test harness."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.original_cwd = Path.cwd()

    def setup(self):
        """Set up test environment."""
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        # cd to temp directory
        import os
        os.chdir(self.temp_dir)

    def teardown(self):
        """Clean up test environment."""
        import os
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def run_cli(self, args: List[str]) -> tuple[int, str, str]:
        """
        Run CLI command and capture output.

        Args:
            args: CLI arguments

        Returns:
            tuple: (exit_code, stdout, stderr)
        """
        from io import StringIO
        import sys

        # Capture stdout and stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        stdout_capture = StringIO()
        stderr_capture = StringIO()

        try:
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture

            cli = ContextControlCLI()
            exit_code = cli.main(args)

        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        return exit_code, stdout_capture.getvalue(), stderr_capture.getvalue()
```

This completes the CLI contracts specification. The CLI provides comprehensive management capabilities while maintaining clear separation of concerns and robust error handling.