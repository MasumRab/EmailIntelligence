#!/usr/bin/env python3
"""
Task Dependency Resolution
Create system to handle task dependencies in parallel workflows.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Set
from datetime import datetime
from task_queue import Task


class TaskDependencyGraph:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}  # task_id -> Task
        self.dependencies: Dict[str, Set[str]] = {}  # task_id -> set of dependent task_ids
        self.dependents: Dict[str, Set[str]] = {}  # task_id -> set of task_ids that depend on it
        self.completed_tasks: Set[str] = set()
        self.in_progress_tasks: Set[str] = set()
        
    def add_task(self, task: Task):
        """Add a task to the dependency graph."""
        self.tasks[task.id] = task
        if task.id not in self.dependencies:
            self.dependencies[task.id] = set()
        if task.id not in self.dependents:
            self.dependents[task.id] = set()
            
        # Add explicit dependencies from task object
        for dep_id in task.dependencies:
            self.add_dependency(task.id, dep_id)
            
    def add_dependency(self, task_id: str, dependency_id: str):
        """Add a dependency relationship: task_id depends on dependency_id."""
        if task_id not in self.dependencies:
            self.dependencies[task_id] = set()
        if dependency_id not in self.dependents:
            self.dependents[dependency_id] = set()
            
        self.dependencies[task_id].add(dependency_id)
        self.dependents[dependency_id].add(task_id)
        
    def remove_dependency(self, task_id: str, dependency_id: str):
        """Remove a dependency relationship."""
        if task_id in self.dependencies and dependency_id in self.dependencies[task_id]:
            self.dependencies[task_id].remove(dependency_id)
        if dependency_id in self.dependents and task_id in self.dependents[dependency_id]:
            self.dependents[dependency_id].remove(task_id)
            
    def get_task_dependencies(self, task_id: str) -> Set[str]:
        """Get all dependencies for a task."""
        return self.dependencies.get(task_id, set()).copy()
        
    def get_task_dependents(self, task_id: str) -> Set[str]:
        """Get all tasks that depend on this task."""
        return self.dependents.get(task_id, set()).copy()
        
    def is_task_ready(self, task_id: str) -> bool:
        """Check if a task is ready to be executed (all dependencies completed)."""
        if task_id not in self.tasks:
            return False
            
        # Task is ready if all its dependencies are completed
        task_dependencies = self.dependencies.get(task_id, set())
        return task_dependencies.issubset(self.completed_tasks)
        
    def get_ready_tasks(self) -> List[Task]:
        """Get all tasks that are ready to be executed."""
        ready_tasks = []
        for task_id, task in self.tasks.items():
            if (task_id not in self.completed_tasks and 
                task_id not in self.in_progress_tasks and 
                self.is_task_ready(task_id)):
                ready_tasks.append(task)
        return ready_tasks
        
    def get_blocked_tasks(self) -> List[Task]:
        """Get all tasks that are blocked by uncompleted dependencies."""
        blocked_tasks = []
        for task_id, task in self.tasks.items():
            if (task_id not in self.completed_tasks and 
                task_id not in self.in_progress_tasks and 
                not self.is_task_ready(task_id)):
                blocked_tasks.append(task)
        return blocked_tasks
        
    def mark_task_in_progress(self, task_id: str):
        """Mark a task as in progress."""
        if task_id in self.tasks and task_id not in self.completed_tasks:
            self.in_progress_tasks.add(task_id)
            
    def mark_task_completed(self, task_id: str):
        """Mark a task as completed."""
        if task_id in self.tasks:
            self.completed_tasks.add(task_id)
            self.in_progress_tasks.discard(task_id)
            
    def mark_task_failed(self, task_id: str):
        """Mark a task as failed (remove from in progress)."""
        self.in_progress_tasks.discard(task_id)
        # Don't add to completed tasks - it failed
        
    def get_task_status(self, task_id: str) -> str:
        """Get the status of a task."""
        if task_id in self.completed_tasks:
            return "completed"
        elif task_id in self.in_progress_tasks:
            return "in_progress"
        elif self.is_task_ready(task_id):
            return "ready"
        else:
            return "blocked"
            
    def get_all_dependencies(self, task_id: str) -> Set[str]:
        """Get all direct and indirect dependencies for a task."""
        all_deps = set()
        to_process = list(self.dependencies.get(task_id, set()))
        
        while to_process:
            dep_id = to_process.pop()
            if dep_id not in all_deps:
                all_deps.add(dep_id)
                # Add indirect dependencies
                to_process.extend(self.dependencies.get(dep_id, set()))
                
        return all_deps
        
    def detect_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependencies in the graph."""
        visited = set()
        rec_stack = set()
        cycles = []
        
        def dfs(node: str, path: List[str]):
            if node in rec_stack:
                # Found a cycle
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
                
            if node in visited:
                return
                
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            # Visit dependents
            for dependent in self.dependents.get(node, set()):
                dfs(dependent, path[:])  # Pass a copy of the path
                
            rec_stack.remove(node)
            
        for task_id in self.tasks:
            if task_id not in visited:
                dfs(task_id, [])
                
        return cycles
        
    def get_parallel_execution_paths(self) -> List[List[str]]:
        """Identify parallel execution paths in the dependency graph."""
        # This is a simplified approach - in a real system, this would be more complex
        paths = []
        processed = set()
        
        # Start with tasks that have no dependencies
        independent_tasks = [
            task_id for task_id in self.tasks 
            if not self.dependencies.get(task_id, set())
        ]
        
        # For each independent task, trace its execution path
        for start_task in independent_tasks:
            if start_task not in processed:
                path = self._trace_execution_path(start_task, processed)
                if path:
                    paths.append(path)
                    
        return paths
        
    def _trace_execution_path(self, start_task: str, processed: Set[str]) -> List[str]:
        """Trace an execution path starting from a task."""
        path = [start_task]
        processed.add(start_task)
        current_task = start_task
        
        # Follow the chain of dependents
        while True:
            dependents = list(self.dependents.get(current_task, set()))
            # Filter out already processed tasks
            dependents = [d for d in dependents if d not in processed]
            
            if not dependents:
                break
                
            # For simplicity, pick the first dependent
            # In a real system, this would consider task priorities, etc.
            next_task = dependents[0]
            path.append(next_task)
            processed.add(next_task)
            current_task = next_task
            
        return path
        
    def get_execution_order(self) -> List[str]:
        """Get a valid execution order for all tasks (topological sort)."""
        # Kahn's algorithm for topological sorting
        in_degree = {}
        for task_id in self.tasks:
            in_degree[task_id] = len(self.dependencies.get(task_id, set()))
            
        queue = [task_id for task_id, degree in in_degree.items() if degree == 0]
        result = []
        
        while queue:
            task_id = queue.pop(0)
            result.append(task_id)
            
            # Reduce in-degree for all dependents
            for dependent in self.dependents.get(task_id, set()):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
                    
        # Check for circular dependencies
        if len(result) != len(self.tasks):
            raise ValueError("Circular dependency detected in task graph")
            
        return result
        
    def visualize_graph(self) -> str:
        """Create a simple text visualization of the dependency graph."""
        lines = ["Task Dependency Graph:"]
        lines.append("=" * 30)
        
        # Show tasks and their dependencies
        for task_id in sorted(self.tasks.keys()):
            task = self.tasks[task_id]
            status = self.get_task_status(task_id)
            deps = list(self.dependencies.get(task_id, set()))
            
            lines.append(f"{task_id} [{status}]")
            if deps:
                for dep in deps:
                    lines.append(f"  └── depends on: {dep}")
            else:
                lines.append("  └── no dependencies")
                
        # Show circular dependencies if any
        cycles = self.detect_circular_dependencies()
        if cycles:
            lines.append("\nCircular Dependencies Detected:")
            for i, cycle in enumerate(cycles):
                lines.append(f"  Cycle {i+1}: {' -> '.join(cycle)}")
                
        return "\n".join(lines)
        
    def get_statistics(self) -> Dict:
        """Get statistics about the dependency graph."""
        total_tasks = len(self.tasks)
        completed_tasks = len(self.completed_tasks)
        in_progress_tasks = len(self.in_progress_tasks)
        ready_tasks = len(self.get_ready_tasks())
        blocked_tasks = len(self.get_blocked_tasks())
        
        cycles = self.detect_circular_dependencies()
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress_tasks,
            'ready_tasks': ready_tasks,
            'blocked_tasks': blocked_tasks,
            'circular_dependencies': len(cycles),
            'parallel_paths': len(self.get_parallel_execution_paths()),
            'completion_percentage': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }


def main():
    # Example usage
    graph = TaskDependencyGraph()
    
    # Create some sample tasks
    from task_queue import Task, Priority, TaskStatus
    
    task1 = Task(
        id="task-1",
        title="Create API documentation outline",
        description="Create outline for API documentation",
        type="api",
        estimated_time=10,
        priority=Priority.NORMAL
    )
    
    task2 = Task(
        id="task-2",
        title="Write API endpoint descriptions",
        description="Write detailed descriptions for each API endpoint",
        type="api",
        estimated_time=30,
        priority=Priority.NORMAL,
        dependencies=["task-1"]
    )
    
    task3 = Task(
        id="task-3",
        title="Create API examples",
        description="Create code examples for API usage",
        type="api",
        estimated_time=20,
        priority=Priority.NORMAL,
        dependencies=["task-1"]
    )
    
    task4 = Task(
        id="task-4",
        title="Review API documentation",
        description="Review and finalize API documentation",
        type="api",
        estimated_time=15,
        priority=Priority.NORMAL,
        dependencies=["task-2", "task-3"]
    )
    
    # Add tasks to graph
    for task in [task1, task2, task3, task4]:
        graph.add_task(task)
        
    # Display graph
    print(graph.visualize_graph())
    
    # Get ready tasks
    ready_tasks = graph.get_ready_tasks()
    print(f"\nReady tasks: {[t.id for t in ready_tasks]}")
    
    # Get execution order
    try:
        execution_order = graph.get_execution_order()
        print(f"\nExecution order: {execution_order}")
    except ValueError as e:
        print(f"\nError: {e}")
        
    # Get statistics
    stats = graph.get_statistics()
    print(f"\nStatistics: {stats}")
    
    print("Task dependency resolution system initialized")


if __name__ == "__main__":
    main()