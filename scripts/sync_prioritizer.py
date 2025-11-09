#!/usr/bin/env python3
"""
Sync Prioritization
Prioritize urgent syncs over routine updates.
"""

import time
import heapq
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from pathlib import Path


class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4


class SyncType(Enum):
    ROUTINE = "routine"
    URGENT = "urgent"
    MANUAL = "manual"
    BACKGROUND = "background"


@dataclass
class SyncTask:
    task_id: str
    worker_id: str
    priority: Priority
    sync_type: SyncType
    files: List[str]
    created_at: float
    deadline: Optional[float] = None
    dependencies: List[str] = field(default_factory=list)
    estimated_duration: float = 0.0  # in seconds

    def __lt__(self, other):
        # For priority queue ordering: lower priority value = higher priority
        # If priorities are equal, earlier creation time = higher priority
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        return self.created_at < other.created_at


class PrioritySyncQueue:
    def __init__(self):
        self.task_queue: List[SyncTask] = []
        self.completed_tasks: Set[str] = set()
        self.failed_tasks: Set[str] = set()
        self.active_tasks: Set[str] = set()
        self.task_history: List[Dict] = []

    def add_task(self, task: SyncTask):
        """Add a sync task to the priority queue."""
        heapq.heappush(self.task_queue, task)

    def get_next_task(self) -> Optional[SyncTask]:
        """Get the next highest priority task."""
        if not self.task_queue:
            return None

        # Remove completed/failed tasks from queue
        while self.task_queue and (
            self.task_queue[0].task_id in self.completed_tasks
            or self.task_queue[0].task_id in self.failed_tasks
        ):
            heapq.heappop(self.task_queue)

        if self.task_queue:
            return heapq.heappop(self.task_queue)
        return None

    def mark_task_completed(self, task_id: str, duration: float = 0.0):
        """Mark a task as completed."""
        self.completed_tasks.add(task_id)
        self.active_tasks.discard(task_id)

        # Add to history
        self.task_history.append(
            {
                "task_id": task_id,
                "status": "completed",
                "completed_at": time.time(),
                "duration": duration,
            }
        )

    def mark_task_failed(self, task_id: str, error: str = ""):
        """Mark a task as failed."""
        self.failed_tasks.add(task_id)
        self.active_tasks.discard(task_id)

        # Add to history
        self.task_history.append(
            {
                "task_id": task_id,
                "status": "failed",
                "failed_at": time.time(),
                "error": error,
            }
        )

    def mark_task_active(self, task_id: str):
        """Mark a task as currently being processed."""
        self.active_tasks.add(task_id)

    def get_queue_stats(self) -> Dict:
        """Get statistics about the queue."""
        pending_count = len(
            [
                t
                for t in self.task_queue
                if t.task_id not in self.completed_tasks
                and t.task_id not in self.failed_tasks
            ]
        )

        return {
            "pending_tasks": pending_count,
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
            "total_history": len(self.task_history),
        }


class SyncPrioritizer:
    def __init__(self):
        self.priority_queue = PrioritySyncQueue()
        self.worker_load: Dict[str, int] = {}  # worker_id -> current_load
        self.max_worker_load = 3  # Max concurrent tasks per worker

    def create_sync_task(
        self, worker_id: str, files: List[str], sync_reason: str = "routine"
    ) -> SyncTask:
        """Create a sync task with appropriate priority based on context."""
        priority = self._determine_priority(sync_reason, files)
        sync_type = self._determine_sync_type(sync_reason)
        estimated_duration = self._estimate_sync_duration(files)

        task_id = f"sync_{worker_id}_{int(time.time())}"

        task = SyncTask(
            task_id=task_id,
            worker_id=worker_id,
            priority=priority,
            sync_type=sync_type,
            files=files,
            created_at=time.time(),
            estimated_duration=estimated_duration,
        )

        # Set deadline for critical tasks
        if priority == Priority.CRITICAL:
            task.deadline = time.time() + 300  # 5 minutes

        return task

    def _determine_priority(self, sync_reason: str, files: List[str]) -> Priority:
        """Determine priority based on sync reason and file types."""
        # Critical priority for urgent changes
        if "urgent" in sync_reason.lower() or "critical" in sync_reason.lower():
            return Priority.CRITICAL

        # High priority for important file types
        important_extensions = {".md", ".py", ".json", ".yml", ".yaml"}
        important_files = [
            f for f in files if Path(f).suffix.lower() in important_extensions
        ]

        if important_files and len(important_files) / len(files) > 0.5:
            return Priority.HIGH

        # High priority for API or configuration files
        for file_path in files:
            if any(
                keyword in file_path.lower()
                for keyword in ["api", "config", "settings"]
            ):
                return Priority.HIGH

        # Normal priority for routine syncs
        if "routine" in sync_reason.lower():
            return Priority.NORMAL

        # Low priority for background maintenance
        if "background" in sync_reason.lower() or "maintenance" in sync_reason.lower():
            return Priority.LOW

        # Default to normal priority
        return Priority.NORMAL

    def _determine_sync_type(self, sync_reason: str) -> SyncType:
        """Determine sync type based on reason."""
        if "urgent" in sync_reason.lower() or "immediate" in sync_reason.lower():
            return SyncType.URGENT
        elif "manual" in sync_reason.lower() or "user" in sync_reason.lower():
            return SyncType.MANUAL
        elif (
            "background" in sync_reason.lower() or "maintenance" in sync_reason.lower()
        ):
            return SyncType.BACKGROUND
        else:
            return SyncType.ROUTINE

    def _estimate_sync_duration(self, files: List[str]) -> float:
        """Estimate sync duration based on number and size of files."""
        # Simple estimation: 0.1 seconds per file + 0.01 seconds per KB
        base_time = len(files) * 0.1

        # In a real implementation, we would check actual file sizes
        # For now, we'll estimate based on file count
        size_time = len(files) * 0.05  # Assume average 50KB per file

        return base_time + size_time

    def prioritize_task(self, task: SyncTask):
        """Add a task to the priority queue."""
        self.priority_queue.add_task(task)

    def get_next_task_for_worker(self, worker_id: str) -> Optional[SyncTask]:
        """Get the next task appropriate for a specific worker."""
        # Check if worker is overloaded
        if self.worker_load.get(worker_id, 0) >= self.max_worker_load:
            return None

        # Get next task from priority queue
        task = self.priority_queue.get_next_task()
        return task

    def assign_task_to_worker(self, task: SyncTask, worker_id: str) -> bool:
        """Assign a task to a worker."""
        # Update worker load
        current_load = self.worker_load.get(worker_id, 0)
        self.worker_load[worker_id] = current_load + 1

        # Mark task as active
        self.priority_queue.mark_task_active(task.task_id)

        return True

    def complete_task(self, task_id: str, worker_id: str, duration: float = 0.0):
        """Mark a task as completed and update worker load."""
        self.priority_queue.mark_task_completed(task_id, duration)

        # Update worker load
        current_load = self.worker_load.get(worker_id, 0)
        self.worker_load[worker_id] = max(0, current_load - 1)

    def fail_task(self, task_id: str, worker_id: str, error: str = ""):
        """Mark a task as failed and update worker load."""
        self.priority_queue.mark_task_failed(task_id, error)

        # Update worker load
        current_load = self.worker_load.get(worker_id, 0)
        self.worker_load[worker_id] = max(0, current_load - 1)

    def get_worker_load(self, worker_id: str) -> int:
        """Get current load for a worker."""
        return self.worker_load.get(worker_id, 0)

    def get_system_load(self) -> Dict:
        """Get overall system load statistics."""
        total_workers = len(self.worker_load)
        total_load = sum(self.worker_load.values())
        avg_load = total_load / total_workers if total_workers > 0 else 0

        queue_stats = self.priority_queue.get_queue_stats()

        return {
            "total_workers": total_workers,
            "total_active_tasks": total_load,
            "average_load_per_worker": avg_load,
            "queue_stats": queue_stats,
        }

    def get_priority_distribution(self) -> Dict:
        """Get distribution of tasks by priority."""
        priority_counts = {p.name: 0 for p in Priority}

        # Count tasks in queue
        for task in self.priority_queue.task_queue:
            if (
                task.task_id not in self.priority_queue.completed_tasks
                and task.task_id not in self.priority_queue.failed_tasks
            ):
                priority_counts[task.priority.name] += 1

        return priority_counts


def main():
    # Example usage
    print("Sync Prioritization System")
    print("=" * 25)

    # Create prioritizer
    prioritizer = SyncPrioritizer()

    # Create some sample tasks
    task1 = prioritizer.create_sync_task(
        "worker1", ["docs/api.md", "docs/guide.md"], "urgent"
    )
    task2 = prioritizer.create_sync_task("worker2", ["docs/changelog.md"], "routine")
    task3 = prioritizer.create_sync_task(
        "worker3", ["config/settings.json"], "critical"
    )

    # Add tasks to priority queue
    prioritizer.prioritize_task(task1)
    prioritizer.prioritize_task(task2)
    prioritizer.prioritize_task(task3)

    # Show priority distribution
    priority_dist = prioritizer.get_priority_distribution()
    print(f"Priority distribution: {priority_dist}")

    print("Sync prioritization system initialized")
    print("System ready to prioritize urgent syncs over routine updates")


if __name__ == "__main__":
    main()
