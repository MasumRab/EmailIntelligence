#!/usr/bin/env python3
"""
Real-time Agent Performance Metrics
Track agent performance in real-time for optimization.
"""

import psutil
import time
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import deque, defaultdict


@dataclass
class AgentPerformanceMetrics:
    agent_id: str
    timestamp: float
    tasks_completed: int = 0
    success_rate: float = 0.0
    average_task_time: float = 0.0
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    disk_io_read: int = 0
    disk_io_write: int = 0
    network_io_sent: int = 0
    network_io_recv: int = 0
    custom_metrics: Dict[str, Any] = field(default_factory=dict)


class PerformanceSnapshot:
    def __init__(self):
        self.timestamp = time.time()
        self.process = psutil.Process()
        self.system_cpu = psutil.cpu_percent(interval=0.1)
        self.system_memory = psutil.virtual_memory()
        self.disk_io = psutil.disk_io_counters()
        self.network_io = psutil.net_io_counters()

    def get_process_metrics(self) -> Dict[str, Any]:
        """Get metrics for the current process."""
        try:
            with self.process.oneshot():
                return {
                    "cpu_percent": self.process.cpu_percent(),
                    "memory_percent": self.process.memory_percent(),
                    "memory_info": self.process.memory_info(),
                    "io_counters": self.process.io_counters()
                    if hasattr(self.process, "io_counters")
                    else None,
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {}


class RealTimePerformanceMonitor:
    def __init__(self, metrics_file: Path = None, max_history: int = 1000):
        self.metrics_file = metrics_file or Path(".agent_performance_metrics.json")
        self.max_history = max_history
        self.agent_metrics: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=max_history)
        )
        self.system_metrics: deque = deque(maxlen=max_history)
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_interval = 5.0  # seconds
        self._lock = threading.RLock()

    def start_monitoring(self, interval: float = 5.0):
        """Start real-time monitoring in a background thread."""
        if self.monitoring_active:
            return

        self.monitoring_interval = interval
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitor_loop, daemon=True
        )
        self.monitoring_thread.start()

    def stop_monitoring(self):
        """Stop real-time monitoring."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join()

    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                self._collect_system_metrics()
                time.sleep(self.monitoring_interval)
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(self.monitoring_interval)

    def _collect_system_metrics(self):
        """Collect system-level metrics."""
        try:
            snapshot = PerformanceSnapshot()
            system_metrics = {
                "timestamp": snapshot.timestamp,
                "cpu_percent": snapshot.system_cpu,
                "memory_percent": snapshot.system_memory.percent,
                "disk_io_read": snapshot.disk_io.read_bytes,
                "disk_io_write": snapshot.disk_io.write_bytes,
                "network_io_sent": snapshot.network_io.bytes_sent,
                "network_io_recv": snapshot.network_io.bytes_recv,
            }

            with self._lock:
                self.system_metrics.append(system_metrics)
                self._save_metrics()

        except Exception as e:
            print(f"Error collecting system metrics: {e}")

    def record_agent_metrics(self, agent_id: str, metrics: AgentPerformanceMetrics):
        """Record metrics for a specific agent."""
        with self._lock:
            self.agent_metrics[agent_id].append(metrics)
            self._save_metrics()

    def get_agent_metrics(
        self, agent_id: str, limit: int = 100
    ) -> List[AgentPerformanceMetrics]:
        """Get recent metrics for an agent."""
        with self._lock:
            metrics = list(self.agent_metrics[agent_id])
            return metrics[-limit:] if len(metrics) > limit else metrics

    def get_all_agent_metrics(self) -> Dict[str, List[AgentPerformanceMetrics]]:
        """Get metrics for all agents."""
        with self._lock:
            return {
                agent_id: list(metrics)
                for agent_id, metrics in self.agent_metrics.items()
            }

    def get_system_metrics(self, limit: int = 100) -> List[Dict]:
        """Get recent system metrics."""
        with self._lock:
            metrics = list(self.system_metrics)
            return metrics[-limit:] if len(metrics) > limit else metrics

    def get_agent_performance_summary(
        self, agent_id: str, window_hours: int = 1
    ) -> Dict[str, Any]:
        """Get performance summary for an agent over a time window."""
        with self._lock:
            metrics = self.get_agent_metrics(agent_id)
            if not metrics:
                return {}

            # Filter metrics within time window
            cutoff_time = time.time() - (window_hours * 3600)
            recent_metrics = [m for m in metrics if m.timestamp >= cutoff_time]

            if not recent_metrics:
                return {}

            # Calculate summary statistics
            total_tasks = sum(m.tasks_completed for m in recent_metrics)
            avg_success_rate = sum(m.success_rate for m in recent_metrics) / len(
                recent_metrics
            )
            avg_task_time = sum(m.average_task_time for m in recent_metrics) / len(
                recent_metrics
            )

            # Resource usage stats
            avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
            avg_memory = sum(m.memory_percent for m in recent_metrics) / len(
                recent_metrics
            )

            return {
                "agent_id": agent_id,
                "time_window_hours": window_hours,
                "total_tasks_completed": total_tasks,
                "average_success_rate": avg_success_rate,
                "average_task_time": avg_task_time,
                "average_cpu_percent": avg_cpu,
                "average_memory_percent": avg_memory,
                "sample_count": len(recent_metrics),
            }

    def get_system_performance_summary(self, window_hours: int = 1) -> Dict[str, Any]:
        """Get system performance summary over a time window."""
        with self._lock:
            metrics = self.get_system_metrics()
            if not metrics:
                return {}

            # Filter metrics within time window
            cutoff_time = time.time() - (window_hours * 3600)
            recent_metrics = [m for m in metrics if m["timestamp"] >= cutoff_time]

            if not recent_metrics:
                return {}

            # Calculate summary statistics
            avg_cpu = sum(m["cpu_percent"] for m in recent_metrics) / len(
                recent_metrics
            )
            avg_memory = sum(m["memory_percent"] for m in recent_metrics) / len(
                recent_metrics
            )

            return {
                "time_window_hours": window_hours,
                "average_system_cpu": avg_cpu,
                "average_system_memory": avg_memory,
                "sample_count": len(recent_metrics),
            }

    def _save_metrics(self):
        """Save metrics to file."""
        try:
            data = {
                "timestamp": time.time(),
                "agent_metrics": {},
                "system_metrics": list(self.system_metrics),
            }

            # Convert agent metrics to serializable format
            for agent_id, metrics in self.agent_metrics.items():
                data["agent_metrics"][agent_id] = [
                    {
                        "agent_id": m.agent_id,
                        "timestamp": m.timestamp,
                        "tasks_completed": m.tasks_completed,
                        "success_rate": m.success_rate,
                        "average_task_time": m.average_task_time,
                        "cpu_percent": m.cpu_percent,
                        "memory_percent": m.memory_percent,
                        "disk_io_read": m.disk_io_read,
                        "disk_io_write": m.disk_io_write,
                        "network_io_sent": m.network_io_sent,
                        "network_io_recv": m.network_io_recv,
                        "custom_metrics": m.custom_metrics,
                    }
                    for m in metrics
                ]

            with open(self.metrics_file, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving metrics: {e}")

    def load_metrics(self):
        """Load metrics from file."""
        try:
            if not self.metrics_file.exists():
                return

            with open(self.metrics_file, "r") as f:
                data = json.load(f)

            # Restore system metrics
            self.system_metrics.clear()
            for metric in data.get("system_metrics", []):
                self.system_metrics.append(metric)

            # Restore agent metrics
            self.agent_metrics.clear()
            for agent_id, metrics in data.get("agent_metrics", {}).items():
                agent_deque = deque(maxlen=self.max_history)
                for metric_data in metrics:
                    metric = AgentPerformanceMetrics(
                        agent_id=metric_data["agent_id"],
                        timestamp=metric_data["timestamp"],
                        tasks_completed=metric_data["tasks_completed"],
                        success_rate=metric_data["success_rate"],
                        average_task_time=metric_data["average_task_time"],
                        cpu_percent=metric_data["cpu_percent"],
                        memory_percent=metric_data["memory_percent"],
                        disk_io_read=metric_data["disk_io_read"],
                        disk_io_write=metric_data["disk_io_write"],
                        network_io_sent=metric_data["network_io_sent"],
                        network_io_recv=metric_data["network_io_recv"],
                        custom_metrics=metric_data.get("custom_metrics", {}),
                    )
                    agent_deque.append(metric)
                self.agent_metrics[agent_id] = agent_deque

        except Exception as e:
            print(f"Error loading metrics: {e}")


class AgentPerformanceDashboard:
    def __init__(self, monitor: RealTimePerformanceMonitor):
        self.monitor = monitor

    def display_agent_status(self, agent_id: str):
        """Display current status for an agent."""
        summary = self.monitor.get_agent_performance_summary(agent_id, window_hours=1)
        if not summary:
            print(f"No metrics available for agent {agent_id}")
            return

        print(f"\nAgent Performance Dashboard - {agent_id}")
        print("=" * 50)
        print(f"Tasks Completed (1h): {summary['total_tasks_completed']}")
        print(f"Success Rate: {summary['average_success_rate']:.1f}%")
        print(f"Avg Task Time: {summary['average_task_time']:.2f}s")
        print(f"CPU Usage: {summary['average_cpu_percent']:.1f}%")
        print(f"Memory Usage: {summary['average_memory_percent']:.1f}%")

    def display_system_status(self):
        """Display current system status."""
        summary = self.monitor.get_system_performance_summary(window_hours=1)
        if not summary:
            print("No system metrics available")
            return

        print("\nSystem Performance Dashboard")
        print("=" * 30)
        print(f"System CPU: {summary['average_system_cpu']:.1f}%")
        print(f"System Memory: {summary['average_system_memory']:.1f}%")

    def display_all_agents(self):
        """Display status for all agents."""
        print("\nAll Agents Performance Dashboard")
        print("=" * 40)

        agent_metrics = self.monitor.get_all_agent_metrics()
        if not agent_metrics:
            print("No agent metrics available")
            return

        for agent_id, metrics in agent_metrics.items():
            if metrics:
                latest = metrics[-1]
                print(f"\n{agent_id}:")
                print(f"  Tasks: {latest.tasks_completed}")
                print(f"  Success: {latest.success_rate:.1f}%")
                print(f"  Avg Time: {latest.average_task_time:.2f}s")
                print(f"  CPU: {latest.cpu_percent:.1f}%")
                print(f"  Memory: {latest.memory_percent:.1f}%")


def main():
    # Example usage
    print("Real-time Agent Performance Metrics System")
    print("=" * 45)

    # Create monitor and dashboard
    monitor = RealTimePerformanceMonitor()
    dashboard = AgentPerformanceDashboard(monitor)

    print("Performance monitoring system initialized")
    print("System ready to track agent performance in real-time")

    # Example of what the workflow would look like:
    print("\nExample workflow:")
    print("  1. Start real-time monitoring")
    print("  2. Record metrics for each agent")
    print("  3. Display performance dashboard")
    print("  4. Track historical performance trends")


if __name__ == "__main__":
    main()
