"""
Analyze Tasks Command Module

Implements complexity analysis and dependency graphing for project tasks.
Ported from .taskmaster/scripts/task_complexity_analyzer.py.
"""

import json
import re
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List

from ..interface import Command


class AnalyzeTasksCommand(Command):
    """
    Command for calculating task complexity and generating execution sequences.
    
    Provides insights into effort estimation, dependency cycles, and 
    hierarchical clustering potential for branch alignment.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "task-analyze"

    @property
    def description(self) -> str:
        return "Analyze task complexity and dependency graphs"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--file", 
            default="tasks/tasks.json", 
            help="Path to tasks.json file"
        )
        parser.add_argument(
            "--graph", 
            action="store_true", 
            help="Generate a textual dependency graph"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {
            "security_validator": "SecurityValidator"
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Set command dependencies."""
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        """Execute the task-analyze command."""
        tasks_file = Path(args.file)

        # Security validation
        if self._security_validator:
            is_safe, error = self._security_validator.validate_path_security(str(tasks_file.absolute()))
            if not is_safe:
                print(f"Error: Security violation for path '{tasks_file}': {error}")
                return 1

        if not tasks_file.exists():
            print(f"Error: Tasks file '{tasks_file}' not found.")
            return 1

        try:
            with open(tasks_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            tasks = data.get("master", {}).get("tasks", []) if "master" in data else data.get("tasks", [])
            
            if not tasks:
                print("No tasks found to analyze.")
                return 0

            print(f"📊 Analyzing {len(tasks)} tasks...")
            
            for task in tasks:
                complexity = self._calculate_complexity(task)
                print(f"Task {task['id']}: Complexity {complexity}/10 - {task['title']}")

            if args.graph:
                self._print_graph(tasks)
                
            return 0
        except Exception as e:
            print(f"Error analyzing tasks: {e}")
            return 1

    def _calculate_complexity(self, task: Dict[str, Any]) -> int:
        """Calculate complexity score (regex logic)."""
        details = task.get('details', '') or task.get('description', '')
        match = re.search(r'complexity:\s*(\d+)', details, re.IGNORECASE)
        return int(match.group(1)) if match else 5

    def _print_graph(self, tasks: List[Dict[str, Any]]) -> None:
        """Print a simple dependency graph."""
        print("\n⛓️  DEPENDENCY GRAPH")
        for task in tasks:
            deps = task.get("dependencies", [])
            if deps:
                print(f"  [{task['id']}] depends on -> {', '.join(map(str, deps))}")
            else:
                print(f"  [{task['id']}] (No dependencies)")
