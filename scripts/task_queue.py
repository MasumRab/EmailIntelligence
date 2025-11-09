#!/usr/bin/env python3
"""
Task Queue System with Smart Routing
Implements independent task queues with smart routing based on agent capabilities.
"""

from typing import List, Dict, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4


class TaskStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    id: str
    title: str
    description: str
    type: str
    estimated_time: int  # in minutes
    priority: Priority
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    dependencies: List[str] = None
    created_at: str = None
    assigned_at: Optional[str] = None
    completed_at: Optional[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if isinstance(self.priority, str):
            self.priority = Priority[self.priority.upper()]
        if isinstance(self.status, str):
            self.status = TaskStatus[self.status.upper()]


class Agent:
    def __init__(
        self, name: str, capabilities: List[str], max_concurrent_tasks: int = 3
    ):
        self.name = name
        self.capabilities = capabilities
        self.max_concurrent_tasks = max_concurrent_tasks
        self.current_load = 0
        self.performance_history = []
        self.last_heartbeat = datetime.now()

    def can_handle_task(self, task: Task) -> bool:
        """Check if agent can handle a specific task type."""
        return task.type in self.capabilities or "general" in self.capabilities

    def has_capacity(self) -> bool:
        """Check if agent has capacity for more tasks."""
        return self.current_load < self.max_concurrent_tasks

    def assign_task(self, task: Task) -> bool:
        """Assign a task to this agent."""
        if self.can_handle_task(task) and self.has_capacity():
            self.current_load += 1
            self.last_heartbeat = datetime.now()
            return True
        return False

    def complete_task(self):
        """Mark a task as completed by this agent."""
        if self.current_load > 0:
            self.current_load -= 1
            self.performance_history.append(
                {
                    "completed_at": datetime.now().isoformat(),
                    "task_time": 10,  # Placeholder
                }
            )

    def get_utilization_rate(self) -> float:
        """Get agent utilization rate."""
        return self.current_load / self.max_concurrent_tasks


class TaskQueue:
    def __init__(self, name: str):
        self.name = name
        self.tasks: List[Task] = []
        self.completed_tasks: List[Task] = []

    def add_task(self, task: Task):
        """Add a task to the queue."""
        self.tasks.append(task)

    def get_next_task(self, agent: Agent) -> Optional[Task]:
        """Get the next suitable task for an agent."""
        # Sort tasks by priority and dependencies
        sorted_tasks = sorted(
            self.tasks,
            key=lambda t: (
                t.priority.value,
                len(
                    [d for d in t.dependencies if not self._is_dependency_completed(d)]
                ),
            ),
        )

        for task in sorted_tasks:
            if (
                task.status == TaskStatus.PENDING
                and agent.can_handle_task(task)
                and self._are_dependencies_met(task)
            ):
                return task
        return None

    def _is_dependency_completed(self, task_id: str) -> bool:
        """Check if a dependency task is completed."""
        for task in self.completed_tasks:
            if task.id == task_id:
                return True
        return False

    def _are_dependencies_met(self, task: Task) -> bool:
        """Check if all dependencies for a task are met."""
        for dep_id in task.dependencies:
            if not self._is_dependency_completed(dep_id):
                return False
        return True

    def mark_task_assigned(self, task: Task, agent_name: str):
        """Mark a task as assigned to an agent."""
        task.status = TaskStatus.ASSIGNED
        task.assigned_agent = agent_name
        task.assigned_at = datetime.now().isoformat()

    def mark_task_completed(self, task: Task):
        """Mark a task as completed."""
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now().isoformat()
        self.tasks.remove(task)
        self.completed_tasks.append(task)


class TaskRouter:
    def __init__(self):
        self.queues: Dict[str, TaskQueue] = {}
        self.agents: List[Agent] = []

    def add_queue(self, queue: TaskQueue):
        """Add a task queue."""
        self.queues[queue.name] = queue

    def add_agent(self, agent: Agent):
        """Add an agent."""
        self.agents.append(agent)

    def route_task(self, task: Task) -> bool:
        """Route a task to the appropriate queue."""
        # Determine queue based on task type
        if task.type.startswith("api"):
            queue_name = "api_docs"
        elif task.type.startswith("guide"):
            queue_name = "user_guides"
        elif task.type.startswith("arch"):
            queue_name = "architecture"
        else:
            queue_name = "general"

        if queue_name in self.queues:
            self.queues[queue_name].add_task(task)
            return True
        return False

    def assign_tasks(self):
        """Assign tasks to available agents."""
        for agent in self.agents:
            if agent.has_capacity():
                # Find a suitable task for this agent
                task = self._find_task_for_agent(agent)
                if task:
                    self._assign_task_to_agent(task, agent)

    def _find_task_for_agent(self, agent: Agent) -> Optional[Task]:
        """Find the best task for an agent."""
        # Check each queue for tasks the agent can handle
        for queue in self.queues.values():
            task = queue.get_next_task(agent)
            if task:
                return task
        return None

    def _assign_task_to_agent(self, task: Task, agent: Agent):
        """Assign a task to an agent."""
        # Find the queue that contains this task
        for queue in self.queues.values():
            if task in queue.tasks:
                queue.mark_task_assigned(task, agent.name)
                agent.assign_task(task)
                break

    def get_queue_stats(self) -> Dict:
        """Get statistics for all queues."""
        stats = {}
        for name, queue in self.queues.items():
            stats[name] = {
                "pending": len(
                    [t for t in queue.tasks if t.status == TaskStatus.PENDING]
                ),
                "assigned": len(
                    [t for t in queue.tasks if t.status == TaskStatus.ASSIGNED]
                ),
                "in_progress": len(
                    [t for t in queue.tasks if t.status == TaskStatus.IN_PROGRESS]
                ),
                "completed": len(queue.completed_tasks),
            }
        return stats

    def get_agent_stats(self) -> Dict:
        """Get statistics for all agents."""
        stats = {}
        for agent in self.agents:
            stats[agent.name] = {
                "utilization": agent.get_utilization_rate(),
                "current_load": agent.current_load,
                "max_capacity": agent.max_concurrent_tasks,
                "capabilities": agent.capabilities,
            }
        return stats


def main():
    # Create task router
    router = TaskRouter()

    # Create queues
    router.add_queue(TaskQueue("api_docs"))
    router.add_queue(TaskQueue("user_guides"))
    router.add_queue(TaskQueue("architecture"))
    router.add_queue(TaskQueue("general"))

    # Create agents
    router.add_agent(Agent("api-writer", ["api", "general"], 5))
    router.add_agent(Agent("guide-writer", ["guide", "general"], 3))
    router.add_agent(Agent("architect", ["arch", "general"], 2))

    # Example usage would go here

    print("Task queue system initialized")
    print(f"Queues: {list(router.queues.keys())}")
    print(f"Agents: {[a.name for a in router.agents]}")


if __name__ == "__main__":
    main()
