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
from collections import defaultdict

from ..interface import Command


class AnalyzeTasksCommand(Command):
    """
    Command for calculating task complexity and generating execution sequences.

    Provides insights into effort estimation, dependency cycles, and
    hierarchical clustering potential for branch alignment.
    Includes exhaustive automated relationship discovery.
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
        parser.add_argument(
            "--check-cycles",
            action="store_true",
            help="Detect circular dependencies in the task graph"
        )
        parser.add_argument(
            "--execution-order",
            action="store_true",
            help="Generate a valid sequential execution order"
        )
        parser.add_argument(
            "--parallel",
            action="store_true",
            help="Identify potential parallel execution paths"
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

            graph = TaskDependencyGraph(tasks)

            if args.graph:
                self._print_graph(tasks)

            if args.relationships:
                self._analyze_relationships(tasks)

            if args.check_cycles:
                self._handle_cycles(graph)

            if args.execution_order:
                self._handle_execution_order(graph)

            if args.parallel:
                self._handle_parallel_paths(graph)

            return 0
        except Exception as e:
            import traceback
            print(f"Error analyzing tasks: {e}")
            traceback.print_exc()
            return 1

    def _handle_cycles(self, graph: 'TaskDependencyGraph') -> None:
        cycles = graph.detect_cycles()
        if cycles:
            print("\n🚨 CIRCULAR DEPENDENCIES DETECTED")
            for i, cycle in enumerate(cycles):
                print(f"  Cycle {i+1}: {' -> '.join(cycle)}")
        else:
            print("\n✅ No circular dependencies detected.")

    def _handle_execution_order(self, graph: 'TaskDependencyGraph') -> None:
        order = graph.get_execution_order()
        if order:
            print("\n📋 RECOMMENDED EXECUTION ORDER")
            for i, tid in enumerate(order):
                title = graph.task_map[tid].get('title', 'Untitled')
                print(f"  {i+1}. [{tid}] {title}")
        else:
            print("\n❌ Cannot generate execution order due to circular dependencies.")

    def _handle_parallel_paths(self, graph: 'TaskDependencyGraph') -> None:
        paths = graph.get_parallel_paths()
        print("\n⚡ POTENTIAL PARALLEL EXECUTION PATHS")
        for i, path in enumerate(paths):
            print(f"  Path {i+1}: {' -> '.join(path)}")

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

    # --- EXHAUSTIVE RELATIONSHIP DISCOVERY (DNA PORTED) ---

    def _analyze_relationships(self, tasks: List[Dict]) -> None:
        """Deep scan for implicit and parent-child relationships."""
        print("\n🔍 DISCOVERING EXHAUSTIVE RELATIONSHIPS")

        task_map = {str(t['id']): t for t in tasks}
        relationships = {
            'depends_on': defaultdict(list),
            'blocks': defaultdict(list),
            'related_to': defaultdict(list),
            'hierarchy': []
        }

        for task in tasks:
            tid = str(task['id'])

            # 1. Structural Hierarchy (Parent-Child)
            if '.' in tid:
                parent_id = tid.rsplit('.', 1)[0]
                if parent_id in task_map:
                    relationships['hierarchy'].append((tid, parent_id))

            # 2. Content-Based Analysis
            content = self._normalize_text(
                task.get('title', '') + ' ' +
                task.get('description', '') + ' ' +
                task.get('acceptance_criteria', '')
            )

            # Keyword-based extraction
            self._scan_keywords(tid, content, task_map, relationships)

        # Output discovered relationships
        self._print_relationship_report(relationships)

    def _normalize_text(self, text: str) -> str:
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'[^\w\s.]', ' ', text)
        return re.sub(r'\s+', ' ', text).strip()

    def _scan_keywords(self, tid: str, content: str, task_map: Dict, rels: Dict) -> None:
        """Scan content for relationship keywords and task references."""
        patterns = {
            'depends_on': ['after', 'before', 'once', 'requires', 'depends on', 'prerequisite'],
            'blocks': ['blocks', 'prevents', 'stops', 'blocked by'],
            'related_to': ['related to', 'similar to', 'additionally', 'complements']
        }

        for rel_type, keywords in patterns.items():
            for kw in keywords:
                if kw in content:
                    # Find task IDs in context (e.g. "task 1.2" or "task-1.2")
                    matches = re.findall(r'task[-\s](\d+(?:\.\d+)*)', content)
                    for match in matches:
                        if match in task_map and match != tid:
                            if match not in rels[rel_type][tid]:
                                rels[rel_type][tid].append(match)

    def _print_relationship_report(self, rels: Dict) -> None:
        if rels['hierarchy']:
            print("\n  [HIERARCHY]")
            for child, parent in rels['hierarchy']:
                print(f"    • Task {child} is a sub-task of {parent}")

        for rel_type in ['depends_on', 'blocks', 'related_to']:
            if rels[rel_type]:
                print(f"\n  [{rel_type.upper().replace('_', ' ')}]")
                for tid, targets in rels[rel_type].items():
                    print(f"    • Task {tid} -> {', '.join(targets)}")


class TaskDependencyGraph:
    """Helper class for dependency graph analysis."""
    def __init__(self, tasks: List[Dict[str, Any]]):
        self.task_map = {str(t['id']): t for t in tasks}
        self.dependencies = defaultdict(set)
        self.dependents = defaultdict(set)

        for task in tasks:
            tid = str(task['id'])
            deps = task.get("dependencies", [])
            for dep_id in deps:
                dep_id_str = str(dep_id)
                self.dependencies[tid].add(dep_id_str)
                self.dependents[dep_id_str].add(tid)

    def detect_cycles(self) -> List[List[str]]:
        visited = set()
        rec_stack = set()
        cycles = []

        def dfs(node: str, path: List[str]):
            if node in rec_stack:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
            if node in visited:
                return

            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in self.dependents[node]:
                dfs(neighbor, list(path))

            rec_stack.remove(node)

        for tid in self.task_map:
            if tid not in visited:
                dfs(tid, [])
        return cycles

    def get_execution_order(self) -> List[str]:
        # Kahn's algorithm
        in_degree = {tid: len(self.dependencies[tid]) for tid in self.task_map}
        queue = [tid for tid, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            tid = queue.pop(0)
            result.append(tid)
            for dependent in self.dependents[tid]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(result) != len(self.task_map):
            return [] # Cycle detected
        return result

    def get_parallel_paths(self) -> List[List[str]]:
        processed = set()
        paths = []

        # Start with tasks that have no dependencies
        roots = sorted([tid for tid in self.task_map if not self.dependencies[tid]])

        for root in roots:
            if root not in processed:
                path = []
                curr = root
                while curr and curr not in processed:
                    path.append(curr)
                    processed.add(curr)
                    # Simple heuristic: follow first dependent that is now ready
                    next_nodes = sorted([d for d in self.dependents[curr] if d not in processed])
                    curr = next_nodes[0] if next_nodes else None
                if path:
                    paths.append(path)
        return paths
