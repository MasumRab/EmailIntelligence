"""
Analyze Tasks Command Module

Implements complexity analysis and dependency graphing for project tasks.
Ported from .taskmaster/scripts/task_complexity_analyzer.py with RelationshipBuilder DNA.
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
    Includes automated relationship discovery.
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
        parser.add_argument(
            "--relationships", 
            action="store_true", 
            help="Deep scan for implicit and parent-child relationships"
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

            if args.relationships:
                self._analyze_relationships(tasks)
                
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

    # --- Relationship Discovery Logic (Ported DNA) ---

    def _analyze_relationships(self, tasks: List[Dict]) -> None:
        """Ported logic to find implicit links and hierarchies."""
        print("\n🔍 DISCOVERING IMPLICIT RELATIONSHIPS")
        
        task_map = {str(t['id']): t for t in tasks}
        
        for task in tasks:
            tid = str(task['id'])
            content = (task.get('title', '') + ' ' + task.get('description', '')).lower()
            
            # 1. Parent-Child Discovery
            if '.' in tid:
                parent_parts = tid.rsplit('.', 1)
                if len(parent_parts) > 0:
                    parent_id = parent_parts[0]
                    if parent_id in task_map:
                        print(f"  - Hierarchy: Task {tid} is a sub-task of {parent_id}")

            # 2. Keyword-based Dependency Scan
            keywords = ['depends on', 'requires', 'after', 'prerequisite']
            for kw in keywords:
                if kw in content:
                    # Look for ID-like patterns near keyword
                    refs = re.findall(r'task[-\s](\d+(?:\.\d+)*)', content)
                    for ref in refs:
                        if ref in task_map and ref != tid:
                            print(f"  - Implicit Link: {tid} -> {ref} (Reason: '{kw}')")
