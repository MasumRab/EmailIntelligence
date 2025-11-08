#!/usr/bin/env python3
"""
Automated Maintenance Task Scheduling
Create automated scheduling for routine documentation maintenance.
"""

import time
import json
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from collections import defaultdict
import uuid


@dataclass
class MaintenanceTask:
    task_id: str
    task_type: str  # "link_check", "content_update", "format_check", "security_check", etc.
    document_id: str
    description: str
    scheduled_time: float
    status: str = "pending"  # "pending", "in_progress", "completed", "failed", "cancelled"
    priority: str = "normal"  # "low", "normal", "high", "critical"
    assigned_agents: List[str] = field(default_factory=list)
    start_time: float = 0.0
    end_time: float = 0.0
    result: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MaintenanceSchedule:
    schedule_id: str
    name: str
    description: str
    task_type: str
    schedule_pattern: str  # "daily", "weekly", "monthly", "custom", etc.
    next_run_time: float
    last_run_time: float = 0.0
    enabled: bool = True
    task_params: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MaintenanceAgent:
    agent_id: str
    capabilities: List[str]  # List of task types the agent can handle
    max_concurrent_tasks: int = 5
    status: str = "active"  # "active", "inactive", "maintenance"
    current_task_count: int = 0
    last_heartbeat: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MaintenanceResult:
    result_id: str
    task_id: str
    agent_id: str
    status: str  # "success", "partial_success", "failed"
    findings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class MaintenanceScheduler:
    def __init__(self, scheduler_file: Path = None):
        self.scheduler_file = scheduler_file or Path(".maintenance_scheduler.json")
        self.maintenance_tasks: Dict[str, MaintenanceTask] = {}
        self.maintenance_schedules: Dict[str, MaintenanceSchedule] = {}
        self.maintenance_agents: Dict[str, MaintenanceAgent] = {}
        self.maintenance_results: Dict[str, MaintenanceResult] = {}
        self.task_queue: List[str] = []  # Queue of task IDs
        self.completed_tasks: List[str] = []  # Completed task IDs
        self.failed_tasks: List[str] = []  # Failed task IDs
        self._lock = threading.RLock()
        self.scheduler_thread: Optional[threading.Thread] = None
        self.scheduler_active = False
        self.task_execution_callbacks: Dict[str, Callable] = {}
        self.load_scheduler_data()

    def register_task_callback(self, task_type: str, callback: Callable):
        """Register a callback function for a specific task type."""
        with self._lock:
            self.task_execution_callbacks[task_type] = callback

    def register_agent(self, agent: MaintenanceAgent) -> bool:
        """Register a maintenance agent."""
        with self._lock:
            self.maintenance_agents[agent.agent_id] = agent
            self._save_scheduler_data()
            return True

    def create_maintenance_task(self, task_type: str, document_id: str, description: str,
                              priority: str = "normal", assigned_agents: List[str] = None,
                              metadata: Dict[str, Any] = None) -> str:
        """Create a new maintenance task."""
        if assigned_agents is None:
            assigned_agents = []
        if metadata is None:
            metadata = {}

        task_id = str(uuid.uuid4())

        with self._lock:
            task = MaintenanceTask(
                task_id=task_id,
                task_type=task_type,
                document_id=document_id,
                description=description,
                scheduled_time=time.time(),  # Schedule for immediate execution
                priority=priority,
                assigned_agents=assigned_agents,
                metadata=metadata
            )

            self.maintenance_tasks[task_id] = task

            # If no specific agents assigned, assign based on capabilities
            if not assigned_agents:
                available_agents = self._find_available_agents(task_type)
                task.assigned_agents = available_agents[:1]  # Assign first available agent

            # Add to queue
            self.task_queue.append(task_id)

            self._save_scheduler_data()

            return task_id

    def create_recurring_schedule(self, name: str, description: str, task_type: str,
                                schedule_pattern: str, task_params: Dict[str, Any] = None) -> str:
        """Create a recurring maintenance schedule."""
        if task_params is None:
            task_params = {}

        schedule_id = str(uuid.uuid4())

        # Calculate next run time based on pattern
        next_run = self._calculate_next_run_time(schedule_pattern)

        with self._lock:
            schedule = MaintenanceSchedule(
                schedule_id=schedule_id,
                name=name,
                description=description,
                task_type=task_type,
                schedule_pattern=schedule_pattern,
                next_run_time=next_run,
                task_params=task_params
            )

            self.maintenance_schedules[schedule_id] = schedule
            self._save_scheduler_data()

            return schedule_id

    def _calculate_next_run_time(self, schedule_pattern: str) -> float:
        """Calculate the next run time based on the schedule pattern."""
        now = time.time()

        if schedule_pattern == "hourly":
            return now + 3600  # 1 hour
        elif schedule_pattern == "daily":
            return now + 86400  # 24 hours
        elif schedule_pattern == "weekly":
            return now + (7 * 86400)  # 7 days
        elif schedule_pattern == "monthly":
            return now + (30 * 86400)  # 30 days
        else:
            # Default to daily for unknown patterns
            return now + 86400

    def _find_available_agents(self, task_type: str) -> List[str]:
        """Find agents that can handle a specific task type."""
        available_agents = []

        with self._lock:
            for agent_id, agent in self.maintenance_agents.items():
                if (agent.status == "active" and
                    task_type in agent.capabilities and
                    agent.current_task_count < agent.max_concurrent_tasks):
                    available_agents.append(agent_id)

        return available_agents

    def execute_next_task(self) -> bool:
        """Execute the next task in the queue."""
        with self._lock:
            if not self.task_queue:
                return False

            # Find highest priority task
            task_id = self._find_highest_priority_task()
            if not task_id:
                return False

            task = self.maintenance_tasks[task_id]

            # Find an available agent
            if not task.assigned_agents:
                available_agents = self._find_available_agents(task.task_type)
                if not available_agents:
                    return False  # No available agents
                task.assigned_agents = [available_agents[0]]

            agent_id = task.assigned_agents[0]
            agent = self.maintenance_agents[agent_id]

            # Update task status
            task.status = "in_progress"
            task.start_time = time.time()

            # Update agent task count
            agent.current_task_count += 1

        # Execute task outside the lock to avoid blocking
        success = self._execute_task(task_id)

        return success

    def _find_highest_priority_task(self) -> Optional[str]:
        """Find the highest priority task in the queue."""
        with self._lock:
            # Sort tasks by priority (critical > high > normal > low)
            priority_order = {"critical": 4, "high": 3, "normal": 2, "low": 1}

            # Get tasks from queue that are still pending
            pending_tasks = [
                task_id for task_id in self.task_queue
                if task_id in self.maintenance_tasks and self.maintenance_tasks[task_id].status == "pending"
            ]

            if not pending_tasks:
                return None

            # Find highest priority task
            highest_priority_task = max(
                pending_tasks,
                key=lambda tid: priority_order.get(self.maintenance_tasks[tid].priority, 0)
            )

            return highest_priority_task

    def _execute_task(self, task_id: str) -> bool:
        """Execute a specific task."""
        with self._lock:
            if task_id not in self.maintenance_tasks:
                return False

            task = self.maintenance_tasks[task_id]
            task_type = task.task_type

        # Get the callback for this task type
        callback = self.task_execution_callbacks.get(task_type)
        if not callback:
            # No callback registered, create a dummy result
            with self._lock:
                result_id = str(uuid.uuid4())
                result = MaintenanceResult(
                    result_id=result_id,
                    task_id=task_id,
                    agent_id=task.assigned_agents[0] if task.assigned_agents else "unknown",
                    status="failed",
                    findings=[f"No callback registered for task type: {task_type}"],
                    suggestions=[f"Register a callback for task type: {task_type}"]
                )
                self.maintenance_results[result_id] = result
                task.status = "failed"
            return False

        try:
            # Execute the task callback
            result_data = callback(task)

            with self._lock:
                # Create result
                result_id = str(uuid.uuid4())
                result = MaintenanceResult(
                    result_id=result_id,
                    task_id=task_id,
                    agent_id=task.assigned_agents[0] if task.assigned_agents else "unknown",
                    status="success",
                    findings=result_data.get("findings", []),
                    suggestions=result_data.get("suggestions", []),
                    execution_time=time.time() - task.start_time,
                    metadata=result_data.get("metadata", {})
                )
                self.maintenance_results[result_id] = result

                # Update task status
                task.status = "completed"
                task.end_time = time.time()

                # Update agent
                if task.assigned_agents:
                    agent = self.maintenance_agents.get(task.assigned_agents[0])
                    if agent:
                        agent.current_task_count -= 1

                # Move from queue to completed
                if task_id in self.task_queue:
                    self.task_queue.remove(task_id)
                self.completed_tasks.append(task_id)

                self._save_scheduler_data()

            return True

        except Exception as e:
            with self._lock:
                # Create failure result
                result_id = str(uuid.uuid4())
                result = MaintenanceResult(
                    result_id=result_id,
                    task_id=task_id,
                    agent_id=task.assigned_agents[0] if task.assigned_agents else "unknown",
                    status="failed",
                    findings=[f"Task execution failed: {str(e)}"],
                    suggestions=["Check task implementation and inputs"]
                )
                self.maintenance_results[result_id] = result

                task.status = "failed"
                task.end_time = time.time()

                # Update agent
                if task.assigned_agents:
                    agent = self.maintenance_agents.get(task.assigned_agents[0])
                    if agent:
                        agent.current_task_count -= 1

                # Move from queue to failed
                if task_id in self.task_queue:
                    self.task_queue.remove(task_id)
                self.failed_tasks.append(task_id)

                self._save_scheduler_data()

            return False

    def start_scheduler(self):
        """Start the maintenance scheduler in a background thread."""
        if self.scheduler_active:
            return

        self.scheduler_active = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()

    def stop_scheduler(self):
        """Stop the maintenance scheduler."""
        self.scheduler_active = False
        if self.scheduler_thread:
            self.scheduler_thread.join()

    def _scheduler_loop(self):
        """Main scheduler loop."""
        while self.scheduler_active:
            try:
                # Check for recurring schedules that need to run
                self._check_schedules()

                # Execute next available task
                while self.task_queue and self.scheduler_active:
                    if not self.execute_next_task():
                        break  # No more tasks or no available agents
                    time.sleep(0.1)  # Small delay between tasks

                time.sleep(1)  # Check every second

            except Exception as e:
                print(f"Error in scheduler loop: {e}")
                time.sleep(1)

    def _check_schedules(self):
        """Check if any scheduled tasks need to run."""
        now = time.time()

        with self._lock:
            for schedule_id, schedule in self.maintenance_schedules.items():
                if (schedule.enabled and
                    schedule.next_run_time <= now and
                    schedule.last_run_time < schedule.next_run_time):

                    # Create a new maintenance task based on the schedule
                    task_id = self.create_maintenance_task(
                        task_type=schedule.task_type,
                        document_id=schedule.task_params.get("document_id", "*"),  # All documents if not specified
                        description=f"Scheduled task: {schedule.name}",
                        priority=schedule.task_params.get("priority", "normal"),
                        metadata={
                            "source_schedule": schedule_id,
                            "scheduled_params": schedule.task_params
                        }
                    )

                    # Update schedule for next run
                    schedule.last_run_time = now
                    schedule.next_run_time = self._calculate_next_run_time(schedule.schedule_pattern)

                    self._save_scheduler_data()

    def get_task_status(self, task_id: str) -> Optional[MaintenanceTask]:
        """Get the status of a specific task."""
        with self._lock:
            return self.maintenance_tasks.get(task_id)

    def get_agent_status(self, agent_id: str) -> Optional[MaintenanceAgent]:
        """Get the status of a specific agent."""
        with self._lock:
            return self.maintenance_agents.get(agent_id)

    def get_task_results(self, task_id: str) -> List[MaintenanceResult]:
        """Get results for a specific task."""
        with self._lock:
            return [
                result for result in self.maintenance_results.values()
                if result.task_id == task_id
            ]

    def get_schedule_status(self, schedule_id: str) -> Optional[MaintenanceSchedule]:
        """Get the status of a specific schedule."""
        with self._lock:
            return self.maintenance_schedules.get(schedule_id)

    def get_scheduler_statistics(self) -> Dict[str, Any]:
        """Get scheduler statistics."""
        with self._lock:
            return {
                'total_agents': len(self.maintenance_agents),
                'active_agents': len([a for a in self.maintenance_agents.values() if a.status == "active"]),
                'total_tasks': len(self.maintenance_tasks),
                'pending_tasks': len([t for t in self.maintenance_tasks.values() if t.status == "pending"]),
                'in_progress_tasks': len([t for t in self.maintenance_tasks.values() if t.status == "in_progress"]),
                'completed_tasks': len([t for t in self.maintenance_tasks.values() if t.status == "completed"]),
                'failed_tasks': len([t for t in self.maintenance_tasks.values() if t.status == "failed"]),
                'task_queue_length': len(self.task_queue),
                'total_schedules': len(self.maintenance_schedules),
                'enabled_schedules': len([s for s in self.maintenance_schedules.values() if s.enabled])
            }

    def _save_scheduler_data(self):
        """Save scheduler data to file."""
        try:
            data = {
                'timestamp': time.time(),
                'maintenance_tasks': {
                    task_id: {
                        'task_id': task.task_id,
                        'task_type': task.task_type,
                        'document_id': task.document_id,
                        'description': task.description,
                        'scheduled_time': task.scheduled_time,
                        'status': task.status,
                        'priority': task.priority,
                        'assigned_agents': task.assigned_agents,
                        'start_time': task.start_time,
                        'end_time': task.end_time,
                        'result': task.result,
                        'metadata': task.metadata
                    }
                    for task_id, task in self.maintenance_tasks.items()
                },
                'maintenance_schedules': {
                    schedule_id: {
                        'schedule_id': schedule.schedule_id,
                        'name': schedule.name,
                        'description': schedule.description,
                        'task_type': schedule.task_type,
                        'schedule_pattern': schedule.schedule_pattern,
                        'next_run_time': schedule.next_run_time,
                        'last_run_time': schedule.last_run_time,
                        'enabled': schedule.enabled,
                        'task_params': schedule.task_params,
                        'metadata': schedule.metadata
                    }
                    for schedule_id, schedule in self.maintenance_schedules.items()
                },
                'maintenance_agents': {
                    agent_id: {
                        'agent_id': agent.agent_id,
                        'capabilities': agent.capabilities,
                        'max_concurrent_tasks': agent.max_concurrent_tasks,
                        'status': agent.status,
                        'current_task_count': agent.current_task_count,
                        'last_heartbeat': agent.last_heartbeat,
                        'metadata': agent.metadata
                    }
                    for agent_id, agent in self.maintenance_agents.items()
                },
                'maintenance_results': {
                    result_id: {
                        'result_id': result.result_id,
                        'task_id': result.task_id,
                        'agent_id': result.agent_id,
                        'status': result.status,
                        'findings': result.findings,
                        'suggestions': result.suggestions,
                        'execution_time': result.execution_time,
                        'metadata': result.metadata
                    }
                    for result_id, result in self.maintenance_results.items()
                },
                'task_queue': self.task_queue[:],
                'completed_tasks': self.completed_tasks[:],
                'failed_tasks': self.failed_tasks[:]
            }

            with open(self.scheduler_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving scheduler data: {e}")

    def load_scheduler_data(self):
        """Load scheduler data from file."""
        try:
            if not self.scheduler_file.exists():
                return

            with open(self.scheduler_file, 'r') as f:
                data = json.load(f)

            # Restore maintenance tasks
            self.maintenance_tasks.clear()
            for task_id, task_data in data.get('maintenance_tasks', {}).items():
                task = MaintenanceTask(
                    task_id=task_data['task_id'],
                    task_type=task_data['task_type'],
                    document_id=task_data['document_id'],
                    description=task_data['description'],
                    scheduled_time=task_data['scheduled_time'],
                    status=task_data.get('status', 'pending'),
                    priority=task_data.get('priority', 'normal'),
                    assigned_agents=task_data.get('assigned_agents', []),
                    start_time=task_data.get('start_time', 0.0),
                    end_time=task_data.get('end_time', 0.0),
                    result=task_data.get('result', ''),
                    metadata=task_data.get('metadata', {})
                )
                self.maintenance_tasks[task_id] = task

            # Restore schedules
            self.maintenance_schedules.clear()
            for schedule_id, schedule_data in data.get('maintenance_schedules', {}).items():
                schedule = MaintenanceSchedule(
                    schedule_id=schedule_data['schedule_id'],
                    name=schedule_data['name'],
                    description=schedule_data['description'],
                    task_type=schedule_data['task_type'],
                    schedule_pattern=schedule_data['schedule_pattern'],
                    next_run_time=schedule_data['next_run_time'],
                    last_run_time=schedule_data.get('last_run_time', 0.0),
                    enabled=schedule_data.get('enabled', True),
                    task_params=schedule_data.get('task_params', {}),
                    metadata=schedule_data.get('metadata', {})
                )
                self.maintenance_schedules[schedule_id] = schedule

            # Restore agents
            self.maintenance_agents.clear()
            for agent_id, agent_data in data.get('maintenance_agents', {}).items():
                agent = MaintenanceAgent(
                    agent_id=agent_data['agent_id'],
                    capabilities=agent_data['capabilities'],
                    max_concurrent_tasks=agent_data.get('max_concurrent_tasks', 5),
                    status=agent_data.get('status', 'active'),
                    current_task_count=agent_data.get('current_task_count', 0),
                    last_heartbeat=agent_data.get('last_heartbeat', 0.0),
                    metadata=agent_data.get('metadata', {})
                )
                self.maintenance_agents[agent_id] = agent

            # Restore results
            self.maintenance_results.clear()
            for result_id, result_data in data.get('maintenance_results', {}).items():
                result = MaintenanceResult(
                    result_id=result_data['result_id'],
                    task_id=result_data['task_id'],
                    agent_id=result_data['agent_id'],
                    status=result_data['status'],
                    findings=result_data.get('findings', []),
                    suggestions=result_data.get('suggestions', []),
                    execution_time=result_data.get('execution_time', 0.0),
                    metadata=result_data.get('metadata', {})
                )
                self.maintenance_results[result_id] = result

            # Restore queues
            self.task_queue = data.get('task_queue', [])
            self.completed_tasks = data.get('completed_tasks', [])
            self.failed_tasks = data.get('failed_tasks', [])

        except Exception as e:
            print(f"Error loading scheduler data: {e}")


class MaintenanceDashboard:
    def __init__(self, scheduler: MaintenanceScheduler):
        self.scheduler = scheduler

    def display_scheduler_status(self):
        """Display overall scheduler status."""
        stats = self.scheduler.get_scheduler_statistics()

        print(f"\nMaintenance Scheduler Status")
        print("=" * 29)
        print(f"Total Agents: {stats['total_agents']}")
        print(f"Active Agents: {stats['active_agents']}")
        print(f"Total Tasks: {stats['total_tasks']}")
        print(f"Pending Tasks: {stats['pending_tasks']}")
        print(f"In Progress: {stats['in_progress_tasks']}")
        print(f"Completed: {stats['completed_tasks']}")
        print(f"Failed: {stats['failed_tasks']}")
        print(f"Task Queue: {stats['task_queue_length']}")
        print(f"Total Schedules: {stats['total_schedules']}")
        print(f"Enabled Schedules: {stats['enabled_schedules']}")

    def display_agents(self):
        """Display all maintenance agents."""
        agents = self.scheduler.maintenance_agents

        print(f"\nMaintenance Agents")
        print("=" * 17)

        if not agents:
            print("No agents registered")
            return

        for agent_id, agent in agents.items():
            print(f"\nAgent: {agent_id}")
            print(f"  Status: {agent.status}")
            print(f"  Capabilities: {', '.join(agent.capabilities)}")
            print(f"  Max Concurrent Tasks: {agent.max_concurrent_tasks}")
            print(f"  Current Task Count: {agent.current_task_count}")

    def display_schedules(self):
        """Display all maintenance schedules."""
        schedules = self.scheduler.maintenance_schedules

        print(f"\nMaintenance Schedules")
        print("=" * 22)

        if not schedules:
            print("No schedules defined")
            return

        for schedule_id, schedule in schedules.items():
            next_run = datetime.fromtimestamp(schedule.next_run_time).strftime('%Y-%m-%d %H:%M:%S')
            last_run = datetime.fromtimestamp(schedule.last_run_time).strftime('%Y-%m-%d %H:%M:%S') if schedule.last_run_time > 0 else "Never"

            print(f"\nSchedule: {schedule.name}")
            print(f"  ID: {schedule_id}")
            print(f"  Task Type: {schedule.task_type}")
            print(f"  Pattern: {schedule.schedule_pattern}")
            print(f"  Enabled: {schedule.enabled}")
            print(f"  Next Run: {next_run}")
            print(f"  Last Run: {last_run}")

    def display_pending_tasks(self):
        """Display all pending maintenance tasks."""
        tasks = self.scheduler.maintenance_tasks
        queue = self.scheduler.task_queue

        print(f"\nPending Tasks")
        print("=" * 13)

        if not queue:
            print("No pending tasks")
            return

        for task_id in queue:
            if task_id in tasks:
                task = tasks[task_id]
                scheduled_time = datetime.fromtimestamp(task.scheduled_time).strftime('%Y-%m-%d %H:%M:%S')
                print(f"\nTask: {task.description}")
                print(f"  ID: {task.task_id}")
                print(f"  Type: {task.task_type}")
                print(f"  Document: {task.document_id}")
                print(f"  Priority: {task.priority}")
                print(f"  Scheduled: {scheduled_time}")

    def display_task_results(self, task_id: str):
        """Display results for a specific task."""
        results = self.scheduler.get_task_results(task_id)

        print(f"\nTask Results - {task_id}")
        print("=" * 22)

        if not results:
            print("No results found")
            return

        for result in results:
            print(f"\nResult: {result.status}")
            print(f"  Agent: {result.agent_id}")
            print(f"  Execution Time: {result.execution_time:.2f}s")

            if result.findings:
                print(f"  Findings: {', '.join(result.findings)}")

            if result.suggestions:
                print(f"  Suggestions: {', '.join(result.suggestions)}")


def main():
    # Example usage
    print("Automated Maintenance Task Scheduling")
    print("=" * 38)

    # Create scheduler and dashboard
    scheduler = MaintenanceScheduler()
    dashboard = MaintenanceDashboard(scheduler)

    print("Maintenance scheduling system initialized")
    print("System ready for automated documentation maintenance")

    # Example of what the workflow would look like:
    print("\nExample workflow:")
    print("  1. Register maintenance agents with capabilities")
    print("  2. Create recurring schedules for routine tasks")
    print("  3. Submit ad-hoc maintenance tasks")
    print("  4. Monitor task execution and results")
    print("  5. Generate maintenance reports and statistics")


if __name__ == "__main__":
    main()