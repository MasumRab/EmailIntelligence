"""
List Tasks Command Module

Implements a command for listing and filtering tasks from tasks.json.
Ported from .taskmaster/scripts/list_tasks.py.
"""

import json
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict

from ..interface import Command


class ListTasksCommand(Command):
    """
    Command for listing tasks from the unified tasks.json.

    Provides filtering capabilities by status, priority, and visibility of subtasks.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "task-list"

    @property
    def description(self) -> str:
        return "List and filter project tasks"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--status", help="Filter by status (pending, in-progress, done)"
        )
        parser.add_argument("--priority", help="Filter by priority (high, medium, low)")
        parser.add_argument(
            "--show-subtasks", action="store_true", help="Show subtask details"
        )
        parser.add_argument(
            "--file",
            default=".taskmaster/tasks/tasks.json",
            help="Path to tasks.json file",
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {"security_validator": "SecurityValidator"}

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Set command dependencies."""
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        """Execute the task-list command."""
        tasks_file = Path(args.file)

        # Security validation
        if self._security_validator:
            is_safe, error = self._security_validator.validate_path_security(
                str(tasks_file.absolute())
            )
            if not is_safe:
                print(f"Error: Security violation for path '{tasks_file}': {error}")
                return 1

        if not tasks_file.exists():
            print(f"Error: Tasks file '{tasks_file}' not found.")
            return 1

        try:
            with open(tasks_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Handle different JSON formats (master key or direct list)
            tasks = (
                data.get("master", {}).get("tasks", [])
                if "master" in data
                else data.get("tasks", [])
            )

            if not tasks:
                print("No tasks found.")
                return 0

            # Filter
            if args.status:
                tasks = [t for t in tasks if t.get("status") == args.status]
            if args.priority:
                tasks = [t for t in tasks if t.get("priority") == args.priority]

            print(f"📋 Found {len(tasks)} tasks:\n")

            for task in tasks:
                self._print_task(task, args.show_subtasks)

            return 0
        except Exception as e:
            print(f"Error reading tasks: {e}")
            return 1

    def _print_task(self, task: Dict[str, Any], show_subtasks: bool) -> None:
        """Format and print a single task."""
        status_icon = "✅" if task.get("status") in ["done", "completed"] else "⏳"
        print(f"{status_icon} [{task['id']}] {task['title']}")
        print(f"   Priority: {task.get('priority', 'medium')}")

        if show_subtasks and "subtasks" in task and task["subtasks"]:
            print(f"   Subtasks ({len(task['subtasks'])}):")
            for sub in task["subtasks"]:
                sub_status = (
                    "ok" if sub.get("status") in ["done", "completed"] else ".."
                )
                print(f"     - [{sub_status}] {sub['id']}: {sub['title']}")
        print()
