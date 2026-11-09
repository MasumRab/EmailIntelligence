#!/usr/bin/env python3
"""
Task Completion Rate Tracking
Monitor and analyze task completion patterns.
"""

import time
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, deque
from datetime import datetime, timedelta
import statistics


@dataclass
class TaskCompletionRecord:
    task_id: str
    agent_id: str
    task_type: str
    start_time: float
    end_time: float
    duration: float
    success: bool
    error_message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class TaskCompletionTracker:
    def __init__(self, tracking_file: Path = None, max_history: int = 10000):
        self.tracking_file = tracking_file or Path(".task_completion_tracking.json")
        self.max_history = max_history
        self.completion_records: deque = deque(maxlen=max_history)
        self.agent_task_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.task_type_stats: Dict[str, Dict[str, List]] = defaultdict(lambda: defaultdict(list))
        self._lock = threading.RLock()
        self.load_tracking_data()

    def record_task_completion(self, record: TaskCompletionRecord):
        """Record a task completion."""
        with self._lock:
            self.completion_records.append(record)

            # Update agent task counts
            if record.success:
                self.agent_task_counts[record.agent_id]['successful'] += 1
            else:
                self.agent_task_counts[record.agent_id]['failed'] += 1

            # Update task type statistics
            self.task_type_stats[record.task_type]['durations'].append(record.duration)
            self.task_type_stats[record.task_type]['successes'].append(1 if record.success else 0)

            self._save_tracking_data()

    def get_completion_rate(self, agent_id: str = None, task_type: str = None,
                          time_window_hours: int = 24) -> float:
        """Get completion rate for agent, task type, or overall."""
        with self._lock:
            cutoff_time = time.time() - (time_window_hours * 3600)
            relevant_records = [
                record for record in self.completion_records
                if record.end_time >= cutoff_time and
                (agent_id is None or record.agent_id == agent_id) and
                (task_type is None or record.task_type == task_type)
            ]

            if not relevant_records:
                return 0.0

            successful = sum(1 for record in relevant_records if record.success)
            return successful / len(relevant_records) * 100

    def get_average_completion_time(self, agent_id: str = None, task_type: str = None,
                                  time_window_hours: int = 24) -> float:
        """Get average completion time for agent, task type, or overall."""
        with self._lock:
            cutoff_time = time.time() - (time_window_hours * 3600)
            relevant_records = [
                record for record in self.completion_records
                if record.end_time >= cutoff_time and record.success and
                (agent_id is None or record.agent_id == agent_id) and
                (task_type is None or record.task_type == task_type)
            ]

            if not relevant_records:
                return 0.0

            return statistics.mean(record.duration for record in relevant_records)

    def get_completion_trends(self, agent_id: str = None, task_type: str = None,
                            time_windows: List[int] = None) -> List[Tuple[int, float]]:
        """Get completion rate trends over different time windows."""
        if time_windows is None:
            time_windows = [1, 6, 12, 24, 168]  # 1h, 6h, 12h, 24h, 168h (1 week)

        trends = []
        for window in time_windows:
            rate = self.get_completion_rate(agent_id, task_type, window)
            trends.append((window, rate))

        return trends

    def get_agent_performance_report(self, agent_id: str,
                                   time_window_hours: int = 24) -> Dict[str, Any]:
        """Get detailed performance report for an agent."""
        with self._lock:
            successful = self.agent_task_counts[agent_id]['successful']
            failed = self.agent_task_counts[agent_id]['failed']
            total = successful + failed

            completion_rate = (successful / total * 100) if total > 0 else 0.0
            avg_time = self.get_average_completion_time(agent_id, time_window_hours=time_window_hours)

            # Get trends (without time_window_hours parameter)
            trends = self.get_completion_trends(agent_id)

            return {
                'agent_id': agent_id,
                'time_window_hours': time_window_hours,
                'total_tasks': total,
                'successful_tasks': successful,
                'failed_tasks': failed,
                'completion_rate': completion_rate,
                'average_completion_time': avg_time,
                'trends': trends
            }

    def get_task_type_performance_report(self, task_type: str,
                                       time_window_hours: int = 24) -> Dict[str, Any]:
        """Get detailed performance report for a task type."""
        with self._lock:
            completion_rate = self.get_completion_rate(task_type=task_type,
                                                     time_window_hours=time_window_hours)
            avg_time = self.get_average_completion_time(task_type=task_type,
                                                      time_window_hours=time_window_hours)

            # Get duration statistics
            durations = self.task_type_stats[task_type]['durations'][-1000:]  # Last 1000 samples
            if durations:
                duration_stats = {
                    'mean': statistics.mean(durations),
                    'median': statistics.median(durations),
                    'stdev': statistics.stdev(durations) if len(durations) > 1 else 0.0,
                    'min': min(durations),
                    'max': max(durations)
                }
            else:
                duration_stats = {}

            # Success rate statistics
            successes = self.task_type_stats[task_type]['successes'][-1000:]  # Last 1000 samples
            if successes:
                success_rate_stats = {
                    'mean': statistics.mean(successes) * 100,
                    'stdev': statistics.stdev(successes) * 100 if len(successes) > 1 else 0.0
                }
            else:
                success_rate_stats = {}

            return {
                'task_type': task_type,
                'time_window_hours': time_window_hours,
                'completion_rate': completion_rate,
                'average_completion_time': avg_time,
                'duration_statistics': duration_stats,
                'success_rate_statistics': success_rate_stats,
                'sample_count': len(durations)
            }

    def get_system_performance_report(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Get overall system performance report."""
        with self._lock:
            completion_rate = self.get_completion_rate(time_window_hours=time_window_hours)
            avg_time = self.get_average_completion_time(time_window_hours=time_window_hours)

            # Get agent performance summary
            agent_reports = {}
            for agent_id in self.agent_task_counts.keys():
                agent_reports[agent_id] = self.get_agent_performance_report(
                    agent_id, time_window_hours)

            # Get task type performance summary
            task_type_reports = {}
            for task_type in self.task_type_stats.keys():
                task_type_reports[task_type] = self.get_task_type_performance_report(
                    task_type, time_window_hours)

            return {
                'time_window_hours': time_window_hours,
                'overall_completion_rate': completion_rate,
                'average_completion_time': avg_time,
                'agent_performance': agent_reports,
                'task_type_performance': task_type_reports,
                'total_tasks_tracked': len(self.completion_records)
            }

    def get_underperforming_agents(self, threshold_rate: float = 80.0,
                                 time_window_hours: int = 24) -> List[Dict[str, Any]]:
        """Get list of agents with completion rates below threshold."""
        underperforming = []

        with self._lock:
            for agent_id in self.agent_task_counts.keys():
                rate = self.get_completion_rate(agent_id, time_window_hours=time_window_hours)
                if rate < threshold_rate:
                    report = self.get_agent_performance_report(agent_id, time_window_hours)
                    underperforming.append(report)

        return underperforming

    def get_performance_alerts(self, completion_rate_threshold: float = 80.0,
                             time_window_hours: int = 24) -> List[Dict[str, Any]]:
        """Get performance alerts for underperforming agents or task types."""
        alerts = []

        # Check agents
        underperforming_agents = self.get_underperforming_agents(
            completion_rate_threshold, time_window_hours)

        for agent_report in underperforming_agents:
            alerts.append({
                'type': 'agent_underperforming',
                'agent_id': agent_report['agent_id'],
                'completion_rate': agent_report['completion_rate'],
                'message': f"Agent {agent_report['agent_id']} completion rate "
                          f"({agent_report['completion_rate']:.1f}%) is below threshold "
                          f"({completion_rate_threshold}%)"
            })

        # Check task types
        with self._lock:
            for task_type in self.task_type_stats.keys():
                rate = self.get_completion_rate(task_type=task_type,
                                              time_window_hours=time_window_hours)
                if rate < completion_rate_threshold:
                    alerts.append({
                        'type': 'task_type_underperforming',
                        'task_type': task_type,
                        'completion_rate': rate,
                        'message': f"Task type '{task_type}' completion rate "
                                  f"({rate:.1f}%) is below threshold "
                                  f"({completion_rate_threshold}%)"
                    })

        return alerts

    def _save_tracking_data(self):
        """Save tracking data to file."""
        try:
            data = {
                'timestamp': time.time(),
                'completion_records': [
                    {
                        'task_id': record.task_id,
                        'agent_id': record.agent_id,
                        'task_type': record.task_type,
                        'start_time': record.start_time,
                        'end_time': record.end_time,
                        'duration': record.duration,
                        'success': record.success,
                        'error_message': record.error_message,
                        'metadata': record.metadata
                    }
                    for record in self.completion_records
                ],
                'agent_task_counts': dict(self.agent_task_counts),
                'task_type_stats': {
                    task_type: dict(stats)
                    for task_type, stats in self.task_type_stats.items()
                }
            }

            with open(self.tracking_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving tracking data: {e}")

    def load_tracking_data(self):
        """Load tracking data from file."""
        try:
            if not self.tracking_file.exists():
                return

            with open(self.tracking_file, 'r') as f:
                data = json.load(f)

            # Restore completion records
            self.completion_records.clear()
            for record_data in data.get('completion_records', []):
                record = TaskCompletionRecord(
                    task_id=record_data['task_id'],
                    agent_id=record_data['agent_id'],
                    task_type=record_data['task_type'],
                    start_time=record_data['start_time'],
                    end_time=record_data['end_time'],
                    duration=record_data['duration'],
                    success=record_data['success'],
                    error_message=record_data.get('error_message', ''),
                    metadata=record_data.get('metadata', {})
                )
                self.completion_records.append(record)

            # Restore agent task counts
            self.agent_task_counts.clear()
            for agent_id, counts in data.get('agent_task_counts', {}).items():
                self.agent_task_counts[agent_id] = defaultdict(int, counts)

            # Restore task type stats
            self.task_type_stats.clear()
            for task_type, stats in data.get('task_type_stats', {}).items():
                self.task_type_stats[task_type] = defaultdict(list, stats)

        except Exception as e:
            print(f"Error loading tracking data: {e}")


class TaskCompletionDashboard:
    def __init__(self, tracker: TaskCompletionTracker):
        self.tracker = tracker

    def display_agent_performance(self, agent_id: str):
        """Display performance report for an agent."""
        report = self.tracker.get_agent_performance_report(agent_id)

        print(f"\nAgent Performance Report - {agent_id}")
        print("=" * 45)
        print(f"Time Window: {report['time_window_hours']} hours")
        print(f"Total Tasks: {report['total_tasks']}")
        print(f"Successful: {report['successful_tasks']}")
        print(f"Failed: {report['failed_tasks']}")
        print(f"Completion Rate: {report['completion_rate']:.1f}%")
        print(f"Avg Completion Time: {report['average_completion_time']:.2f}s")

        print("\nTrends:")
        for window, rate in report['trends']:
            print(f"  {window}h: {rate:.1f}%")

    def display_task_type_performance(self, task_type: str):
        """Display performance report for a task type."""
        report = self.tracker.get_task_type_performance_report(task_type)

        print(f"\nTask Type Performance Report - {task_type}")
        print("=" * 45)
        print(f"Time Window: {report['time_window_hours']} hours")
        print(f"Completion Rate: {report['completion_rate']:.1f}%")
        print(f"Avg Completion Time: {report['average_completion_time']:.2f}s")
        print(f"Sample Count: {report['sample_count']}")

        if 'duration_statistics' in report and report['duration_statistics']:
            stats = report['duration_statistics']
            print(f"\nDuration Statistics:")
            print(f"  Mean: {stats['mean']:.2f}s")
            print(f"  Median: {stats['median']:.2f}s")
            print(f"  Std Dev: {stats['stdev']:.2f}s")

    def display_system_performance(self):
        """Display overall system performance."""
        report = self.tracker.get_system_performance_report()

        print(f"\nSystem Performance Report")
        print("=" * 30)
        print(f"Time Window: {report['time_window_hours']} hours")
        print(f"Overall Completion Rate: {report['overall_completion_rate']:.1f}%")
        print(f"Avg Completion Time: {report['average_completion_time']:.2f}s")
        print(f"Total Tasks Tracked: {report['total_tasks_tracked']}")

    def display_performance_alerts(self, threshold: float = 80.0):
        """Display performance alerts."""
        alerts = self.tracker.get_performance_alerts(threshold)

        if not alerts:
            print(f"\nNo performance alerts (threshold: {threshold}%)")
            return

        print(f"\nPerformance Alerts (threshold: {threshold}%)")
        print("=" * 40)
        for alert in alerts:
            print(f"⚠️  {alert['message']}")


def main():
    # Example usage
    print("Task Completion Rate Tracking System")
    print("=" * 40)

    # Create tracker and dashboard
    tracker = TaskCompletionTracker()
    dashboard = TaskCompletionDashboard(tracker)

    print("Task completion tracking system initialized")
    print("System ready to monitor and analyze task completion patterns")

    # Example of what the workflow would look like:
    print("\nExample workflow:")
    print("  1. Record task completion events")
    print("  2. Track completion rates by agent and task type")
    print("  3. Generate performance reports")
    print("  4. Identify underperforming agents or task types")
    print("  5. Generate alerts for performance issues")


if __name__ == "__main__":
    main()
