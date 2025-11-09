#!/usr/bin/env python3
"""
Event-Driven Task Assignment System
Replaces polling with event-driven system for immediate task assignment.
"""

from typing import List, Dict, Optional, Callable
from datetime import datetime
from task_queue import TaskRouter, Agent, Task, TaskStatus
from load_balancer import LoadBalancer


class EventType:
    TASK_COMPLETED = "task_completed"
    AGENT_AVAILABLE = "agent_available"
    TASK_FAILED = "task_failed"
    AGENT_UNAVAILABLE = "agent_unavailable"


class Event:
    def __init__(self, event_type: str, data: Dict, timestamp: str = None):
        self.type = event_type
        self.data = data
        self.timestamp = timestamp or datetime.now().isoformat()


class EventManager:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        self.event_queue: List[Event] = []

    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to an event type."""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def emit(self, event: Event):
        """Emit an event to all subscribers."""
        self.event_queue.append(event)
        self._process_event(event)

    def _process_event(self, event: Event):
        """Process an event by calling all subscribers."""
        if event.type in self.listeners:
            for callback in self.listeners[event.type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Error in event callback: {e}")

    def process_events(self):
        """Process all queued events."""
        while self.event_queue:
            event = self.event_queue.pop(0)
            self._process_event(event)


class EventDrivenTaskAssigner:
    def __init__(self, router: TaskRouter, load_balancer: LoadBalancer):
        self.router = router
        self.load_balancer = load_balancer
        self.event_manager = EventManager()
        self._setup_event_handlers()

    def _setup_event_handlers(self):
        """Set up event handlers for task assignment."""
        self.event_manager.subscribe(EventType.TASK_COMPLETED, self._on_task_completed)
        self.event_manager.subscribe(
            EventType.AGENT_AVAILABLE, self._on_agent_available
        )
        self.event_manager.subscribe(EventType.TASK_FAILED, self._on_task_failed)

    def _on_task_completed(self, event: Event):
        """Handle task completion event."""
        task_id = event.data.get("task_id")
        agent_name = event.data.get("agent_name")
        completion_time = event.data.get("completion_time", 0)

        # Update agent performance
        if agent_name:
            self.load_balancer.update_agent_performance(agent_name, completion_time)

        # Find next task for the agent
        agent = self._get_agent_by_name(agent_name)
        if agent:
            self._assign_next_task_to_agent(agent)

    def _on_agent_available(self, event: Event):
        """Handle agent availability event."""
        agent_name = event.data.get("agent_name")
        agent = self._get_agent_by_name(agent_name)
        if agent:
            self._assign_next_task_to_agent(agent)

    def _on_task_failed(self, event: Event):
        """Handle task failure event."""
        task_id = event.data.get("task_id")
        agent_name = event.data.get("agent_name")
        error = event.data.get("error", "Unknown error")

        # Log failure and potentially reassign task
        print(f"Task {task_id} failed on agent {agent_name}: {error}")

        # Find the task and potentially reassign it
        task = self._find_task_by_id(task_id)
        if task:
            self._reassign_failed_task(task)

    def _get_agent_by_name(self, agent_name: str) -> Optional[Agent]:
        """Get agent by name."""
        for agent in self.router.agents:
            if agent.name == agent_name:
                return agent
        return None

    def _find_task_by_id(self, task_id: str) -> Optional[Task]:
        """Find task by ID."""
        for queue in self.router.queues.values():
            for task in queue.tasks:
                if task.id == task_id:
                    return task
        return None

    def _assign_next_task_to_agent(self, agent: Agent):
        """Assign the next suitable task to an agent."""
        # Find the next suitable task for the agent
        task = self.load_balancer.find_best_agent_for_task(
            agent
        )  # This needs to be public
        if task:
            self.load_balancer.assign_task_to_agent(task, agent)

    def _reassign_failed_task(self, task: Task):
        """Reassign a failed task."""
        # Reset task status
        task.status = TaskStatus.PENDING
        task.assigned_agent = None
        task.assigned_at = None

        # Try to assign to a different agent
        best_agent = self.load_balancer.find_best_agent_for_task(task)
        if best_agent:
            self.load_balancer.assign_task_to_agent(task, best_agent)
        else:
            print(f"No suitable agent found for failed task {task.id}")

    def emit_task_completed(self, task_id: str, agent_name: str, completion_time: int):
        """Emit a task completed event."""
        event = Event(
            EventType.TASK_COMPLETED,
            {
                "task_id": task_id,
                "agent_name": agent_name,
                "completion_time": completion_time,
            },
        )
        self.event_manager.emit(event)

    def emit_agent_available(self, agent_name: str):
        """Emit an agent available event."""
        event = Event(EventType.AGENT_AVAILABLE, {"agent_name": agent_name})
        self.event_manager.emit(event)

    def emit_task_failed(self, task_id: str, agent_name: str, error: str):
        """Emit a task failed event."""
        event = Event(
            EventType.TASK_FAILED,
            {"task_id": task_id, "agent_name": agent_name, "error": error},
        )
        self.event_manager.emit(event)

    def process_pending_events(self):
        """Process any pending events."""
        self.event_manager.process_events()


def main():
    # This would integrate with the existing router and load balancer
    print("Event-driven task assignment system initialized")
    print("Event system ready for task assignment without polling")


if __name__ == "__main__":
    main()
