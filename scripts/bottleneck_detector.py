#!/usr/bin/env python3
"""
Automated Bottleneck Detection
Automatically identify and alert on workflow bottlenecks.
"""

import time
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict, deque
import statistics
from datetime import datetime


@dataclass
class WorkflowStep:
    step_id: str
    step_name: str
    start_time: float
    end_time: float = 0.0
    duration: float = 0.0
    status: str = "running"  # "running", "completed", "failed"
    agent_id: str = ""
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BottleneckAlert:
    alert_id: str
    alert_type: str  # "long_running_step", "queue_backlog", "resource_contention", "dependency_block"
    severity: str  # "low", "medium", "high", "critical"
    description: str
    affected_steps: List[str]
    affected_agents: List[str]
    timestamp: float
    resolution_suggestion: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class BottleneckDetector:
    def __init__(self, detection_file: Path = None, max_history: int = 1000):
        self.detection_file = detection_file or Path(".bottleneck_detection.json")
        self.max_history = max_history
        self.workflow_steps: Dict[str, WorkflowStep] = {}
        self.bottleneck_alerts: deque = deque(maxlen=max_history)
        self.step_durations: Dict[str, List[float]] = defaultdict(list)
        self.agent_workloads: Dict[str, int] = defaultdict(int)
        self.step_queue_sizes: Dict[str, List[int]] = defaultdict(list)
        self._lock = threading.RLock()
        self.load_detection_data()

    def start_workflow_step(
        self,
        step_id: str,
        step_name: str,
        agent_id: str = "",
        dependencies: List[str] = None,
        metadata: Dict[str, Any] = None,
    ) -> WorkflowStep:
        """Start tracking a workflow step."""
        if dependencies is None:
            dependencies = []
        if metadata is None:
            metadata = {}

        step = WorkflowStep(
            step_id=step_id,
            step_name=step_name,
            start_time=time.time(),
            agent_id=agent_id,
            dependencies=dependencies,
            metadata=metadata,
        )

        with self._lock:
            self.workflow_steps[step_id] = step
            self.agent_workloads[agent_id] += 1
            self._save_detection_data()

        return step

    def complete_workflow_step(
        self, step_id: str, success: bool = True, error_message: str = ""
    ) -> Optional[WorkflowStep]:
        """Mark a workflow step as completed."""
        with self._lock:
            if step_id not in self.workflow_steps:
                return None

            step = self.workflow_steps[step_id]
            step.end_time = time.time()
            step.duration = step.end_time - step.start_time
            step.status = "completed" if success else "failed"
            if not success:
                step.metadata["error_message"] = error_message

            # Update step durations for historical analysis
            self.step_durations[step.step_name].append(step.duration)

            # Update agent workload
            if step.agent_id in self.agent_workloads:
                self.agent_workloads[step.agent_id] -= 1
                if self.agent_workloads[step.agent_id] < 0:
                    self.agent_workloads[step.agent_id] = 0

            self._save_detection_data()
            return step

    def get_step_duration_stats(self, step_name: str) -> Dict[str, float]:
        """Get duration statistics for a step type."""
        with self._lock:
            durations = self.step_durations.get(step_name, [])
            if not durations:
                return {}

            return {
                "count": len(durations),
                "mean": statistics.mean(durations),
                "median": statistics.median(durations),
                "stdev": statistics.stdev(durations) if len(durations) > 1 else 0.0,
                "min": min(durations),
                "max": max(durations),
                "percentile_95": self._percentile(durations, 95),
                "percentile_99": self._percentile(durations, 99),
            }

    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile of a list of numbers."""
        if not data:
            return 0.0

        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)

        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower = sorted_data[int(index)]
            upper = sorted_data[min(int(index) + 1, len(sorted_data) - 1)]
            return lower + (upper - lower) * (index - int(index))

    def detect_long_running_steps(
        self, duration_threshold_percentile: float = 95, min_duration: float = 60.0
    ) -> List[BottleneckAlert]:
        """Detect steps that are taking longer than expected."""
        alerts = []

        with self._lock:
            # Get currently running steps
            running_steps = [
                step
                for step in self.workflow_steps.values()
                if step.status == "running"
            ]

            for step in running_steps:
                current_duration = time.time() - step.start_time

                # Check if step is taking too long
                stats = self.get_step_duration_stats(step.step_name)
                if stats:
                    # Use either the percentile threshold or minimum duration, whichever is higher
                    threshold = max(
                        stats.get("percentile_95", min_duration), min_duration
                    )

                    if current_duration > threshold:
                        alert = BottleneckAlert(
                            alert_id=f"long_running_{step.step_id}",
                            alert_type="long_running_step",
                            severity="high"
                            if current_duration > threshold * 2
                            else "medium",
                            description=f"Step '{step.step_name}' (ID: {step.step_id}) "
                            f"has been running for {current_duration:.1f}s, "
                            f"exceeding threshold of {threshold:.1f}s",
                            affected_steps=[step.step_id],
                            affected_agents=[step.agent_id],
                            timestamp=time.time(),
                            resolution_suggestion=f"Check if step '{step.step_name}' "
                            f"is stuck or needs optimization",
                        )
                        alerts.append(alert)
                elif current_duration > min_duration:
                    # No historical data, but step is taking a long time
                    alert = BottleneckAlert(
                        alert_id=f"long_running_{step.step_id}",
                        alert_type="long_running_step",
                        severity="medium",
                        description=f"Step '{step.step_name}' (ID: {step.step_id}) "
                        f"has been running for {current_duration:.1f}s "
                        f"with no historical data for comparison",
                        affected_steps=[step.step_id],
                        affected_agents=[step.agent_id],
                        timestamp=time.time(),
                        resolution_suggestion=f"Check if step '{step.step_name}' "
                        f"is functioning correctly",
                    )
                    alerts.append(alert)

        return alerts

    def detect_queue_backlogs(
        self, backlog_threshold: int = 10
    ) -> List[BottleneckAlert]:
        """Detect steps with large queue backlogs."""
        alerts = []

        with self._lock:
            # For this simplified implementation, we'll check agent workloads
            # In a real system, this would check actual queue sizes
            overloaded_agents = [
                agent_id
                for agent_id, workload in self.agent_workloads.items()
                if workload > backlog_threshold
            ]

            if overloaded_agents:
                alert = BottleneckAlert(
                    alert_id=f"queue_backlog_{int(time.time())}",
                    alert_type="queue_backlog",
                    severity="high"
                    if any(
                        w > backlog_threshold * 2 for w in self.agent_workloads.values()
                    )
                    else "medium",
                    description=f"Agents {overloaded_agents} have high workloads "
                    f"(>{backlog_threshold} tasks)",
                    affected_steps=[],
                    affected_agents=overloaded_agents,
                    timestamp=time.time(),
                    resolution_suggestion="Consider adding more agents or redistributing workload",
                )
                alerts.append(alert)

        return alerts

    def detect_resource_contention(
        self, resource_threshold: float = 80.0
    ) -> List[BottleneckAlert]:
        """Detect resource contention issues (placeholder implementation)."""
        # In a real implementation, this would check actual system resources
        # For now, we'll create a placeholder that could be extended
        alerts = []

        # This is a simplified check - in reality, you'd monitor actual CPU, memory, disk, network
        with self._lock:
            high_duration_steps = []
            for step_name, durations in self.step_durations.items():
                if durations and len(durations) > 5:  # Need sufficient data
                    recent_durations = durations[-10:]  # Last 10 durations
                    avg_recent = statistics.mean(recent_durations)
                    stats = self.get_step_duration_stats(step_name)
                    historical_avg = stats.get("mean", 0)

                    # If recent durations are significantly higher than historical average
                    if historical_avg > 0 and avg_recent > historical_avg * 1.5:
                        high_duration_steps.append(step_name)

            if high_duration_steps:
                alert = BottleneckAlert(
                    alert_id=f"resource_contention_{int(time.time())}",
                    alert_type="resource_contention",
                    severity="medium",
                    description=f"Steps {high_duration_steps} showing increased durations, "
                    f"possibly due to resource contention",
                    affected_steps=high_duration_steps,
                    affected_agents=[],
                    timestamp=time.time(),
                    resolution_suggestion="Check system resources (CPU, memory, disk I/O) and "
                    "consider resource allocation optimization",
                )
                alerts.append(alert)

        return alerts

    def detect_dependency_blocks(self) -> List[BottleneckAlert]:
        """Detect steps blocked by dependencies."""
        alerts = []

        with self._lock:
            # Find steps that are waiting for dependencies
            blocked_steps = []
            for step in self.workflow_steps.values():
                if step.status == "running" and step.dependencies:
                    # Check if dependencies are completed
                    unmet_dependencies = [
                        dep_id
                        for dep_id in step.dependencies
                        if dep_id not in self.workflow_steps
                        or self.workflow_steps[dep_id].status
                        not in ["completed", "failed"]
                    ]

                    if unmet_dependencies:
                        # Check how long we've been waiting
                        wait_time = time.time() - step.start_time
                        if wait_time > 300:  # 5 minutes
                            blocked_steps.append((step, unmet_dependencies, wait_time))

            if blocked_steps:
                affected_step_ids = [step.step_id for step, _, _ in blocked_steps]
                affected_agent_ids = [step.agent_id for step, _, _ in blocked_steps]

                alert = BottleneckAlert(
                    alert_id=f"dependency_block_{int(time.time())}",
                    alert_type="dependency_block",
                    severity="high",
                    description=f"{len(blocked_steps)} steps blocked by unmet dependencies "
                    f"for over 5 minutes",
                    affected_steps=affected_step_ids,
                    affected_agents=affected_agent_ids,
                    timestamp=time.time(),
                    resolution_suggestion="Check dependency chain and ensure upstream steps "
                    "are progressing or failed appropriately",
                )
                alerts.append(alert)

        return alerts

    def detect_all_bottlenecks(
        self,
        duration_threshold_percentile: float = 95,
        min_duration: float = 60.0,
        backlog_threshold: int = 10,
        resource_threshold: float = 80.0,
    ) -> List[BottleneckAlert]:
        """Detect all types of bottlenecks."""
        all_alerts = []

        # Detect different types of bottlenecks
        all_alerts.extend(
            self.detect_long_running_steps(duration_threshold_percentile, min_duration)
        )
        all_alerts.extend(self.detect_queue_backlogs(backlog_threshold))
        all_alerts.extend(self.detect_resource_contention(resource_threshold))
        all_alerts.extend(self.detect_dependency_blocks())

        return all_alerts

    def add_bottleneck_alert(self, alert: BottleneckAlert):
        """Add a bottleneck alert to the history."""
        with self._lock:
            self.bottleneck_alerts.append(alert)
            self._save_detection_data()

    def get_recent_alerts(self, hours: int = 24) -> List[BottleneckAlert]:
        """Get recent bottleneck alerts."""
        cutoff_time = time.time() - (hours * 3600)

        with self._lock:
            return [
                alert
                for alert in self.bottleneck_alerts
                if alert.timestamp >= cutoff_time
            ]

    def get_alerts_by_type(self, alert_type: str) -> List[BottleneckAlert]:
        """Get bottleneck alerts by type."""
        with self._lock:
            return [
                alert
                for alert in self.bottleneck_alerts
                if alert.alert_type == alert_type
            ]

    def get_alerts_by_severity(self, severity: str) -> List[BottleneckAlert]:
        """Get bottleneck alerts by severity."""
        with self._lock:
            return [
                alert for alert in self.bottleneck_alerts if alert.severity == severity
            ]

    def get_bottleneck_summary(self) -> Dict[str, Any]:
        """Get a summary of current bottleneck detection status."""
        with self._lock:
            running_steps = [
                step
                for step in self.workflow_steps.values()
                if step.status == "running"
            ]

            completed_steps = [
                step
                for step in self.workflow_steps.values()
                if step.status == "completed"
            ]

            failed_steps = [
                step for step in self.workflow_steps.values() if step.status == "failed"
            ]

            # Get recent alerts
            recent_alerts = self.get_recent_alerts(1)  # Last hour

            return {
                "timestamp": time.time(),
                "total_steps": len(self.workflow_steps),
                "running_steps": len(running_steps),
                "completed_steps": len(completed_steps),
                "failed_steps": len(failed_steps),
                "active_agents": len(
                    [a for a, w in self.agent_workloads.items() if w > 0]
                ),
                "total_agents": len(self.agent_workloads),
                "recent_alerts": len(recent_alerts),
                "alerts_by_severity": {
                    "critical": len(self.get_alerts_by_severity("critical")),
                    "high": len(self.get_alerts_by_severity("high")),
                    "medium": len(self.get_alerts_by_severity("medium")),
                    "low": len(self.get_alerts_by_severity("low")),
                },
                "alerts_by_type": {
                    "long_running_step": len(
                        self.get_alerts_by_type("long_running_step")
                    ),
                    "queue_backlog": len(self.get_alerts_by_type("queue_backlog")),
                    "resource_contention": len(
                        self.get_alerts_by_type("resource_contention")
                    ),
                    "dependency_block": len(
                        self.get_alerts_by_type("dependency_block")
                    ),
                },
            }

    def _save_detection_data(self):
        """Save detection data to file."""
        try:
            data = {
                "timestamp": time.time(),
                "workflow_steps": {
                    step_id: {
                        "step_id": step.step_id,
                        "step_name": step.step_name,
                        "start_time": step.start_time,
                        "end_time": step.end_time,
                        "duration": step.duration,
                        "status": step.status,
                        "agent_id": step.agent_id,
                        "dependencies": step.dependencies,
                        "metadata": step.metadata,
                    }
                    for step_id, step in self.workflow_steps.items()
                },
                "bottleneck_alerts": [
                    {
                        "alert_id": alert.alert_id,
                        "alert_type": alert.alert_type,
                        "severity": alert.severity,
                        "description": alert.description,
                        "affected_steps": alert.affected_steps,
                        "affected_agents": alert.affected_agents,
                        "timestamp": alert.timestamp,
                        "resolution_suggestion": alert.resolution_suggestion,
                        "metadata": alert.metadata,
                    }
                    for alert in self.bottleneck_alerts
                ],
                "step_durations": {
                    step_name: durations
                    for step_name, durations in self.step_durations.items()
                },
                "agent_workloads": dict(self.agent_workloads),
            }

            with open(self.detection_file, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving detection data: {e}")

    def load_detection_data(self):
        """Load detection data from file."""
        try:
            if not self.detection_file.exists():
                return

            with open(self.detection_file, "r") as f:
                data = json.load(f)

            # Restore workflow steps
            self.workflow_steps.clear()
            for step_id, step_data in data.get("workflow_steps", {}).items():
                step = WorkflowStep(
                    step_id=step_data["step_id"],
                    step_name=step_data["step_name"],
                    start_time=step_data["start_time"],
                    end_time=step_data["end_time"],
                    duration=step_data["duration"],
                    status=step_data["status"],
                    agent_id=step_data["agent_id"],
                    dependencies=step_data["dependencies"],
                    metadata=step_data["metadata"],
                )
                self.workflow_steps[step_id] = step

            # Restore bottleneck alerts
            self.bottleneck_alerts.clear()
            for alert_data in data.get("bottleneck_alerts", []):
                alert = BottleneckAlert(
                    alert_id=alert_data["alert_id"],
                    alert_type=alert_data["alert_type"],
                    severity=alert_data["severity"],
                    description=alert_data["description"],
                    affected_steps=alert_data["affected_steps"],
                    affected_agents=alert_data["affected_agents"],
                    timestamp=alert_data["timestamp"],
                    resolution_suggestion=alert_data.get("resolution_suggestion", ""),
                    metadata=alert_data.get("metadata", {}),
                )
                self.bottleneck_alerts.append(alert)

            # Restore step durations
            self.step_durations.clear()
            for step_name, durations in data.get("step_durations", {}).items():
                self.step_durations[step_name] = durations

            # Restore agent workloads
            self.agent_workloads.clear()
            for agent_id, workload in data.get("agent_workloads", {}).items():
                self.agent_workloads[agent_id] = workload

        except Exception as e:
            print(f"Error loading detection data: {e}")


class BottleneckDashboard:
    def __init__(self, detector: BottleneckDetector):
        self.detector = detector

    def display_bottleneck_summary(self):
        """Display bottleneck detection summary."""
        summary = self.detector.get_bottleneck_summary()

        print("\nBottleneck Detection Summary")
        print("=" * 35)
        print(f"Total Steps: {summary['total_steps']}")
        print(f"Running Steps: {summary['running_steps']}")
        print(f"Completed Steps: {summary['completed_steps']}")
        print(f"Failed Steps: {summary['failed_steps']}")
        print(f"Active Agents: {summary['active_agents']}/{summary['total_agents']}")
        print(f"Recent Alerts (1h): {summary['recent_alerts']}")

        print("\nAlerts by Severity:")
        for severity, count in summary["alerts_by_severity"].items():
            print(f"  {severity.capitalize()}: {count}")

        print("\nAlerts by Type:")
        for alert_type, count in summary["alerts_by_type"].items():
            print(f"  {alert_type.replace('_', ' ').title()}: {count}")

    def display_recent_alerts(self, hours: int = 1):
        """Display recent bottleneck alerts."""
        alerts = self.detector.get_recent_alerts(hours)

        if not alerts:
            print(f"\nNo recent alerts (last {hours} hour(s))")
            return

        print(f"\nRecent Bottleneck Alerts (last {hours} hour(s))")
        print("=" * 50)
        for alert in sorted(alerts, key=lambda x: x.timestamp, reverse=True):
            timestamp = datetime.fromtimestamp(alert.timestamp).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            print(f"\n[{timestamp}] {alert.severity.upper()}: {alert.description}")
            if alert.resolution_suggestion:
                print(f"  Suggestion: {alert.resolution_suggestion}")

    def display_detailed_analysis(self):
        """Display detailed bottleneck analysis."""
        print("\nDetailed Bottleneck Analysis")
        print("=" * 30)

        # Check for all types of bottlenecks
        alerts = self.detector.detect_all_bottlenecks()

        if not alerts:
            print("No active bottlenecks detected")
            return

        print(f"Detected {len(alerts)} active bottlenecks:")
        for alert in alerts:
            print(
                f"\n⚠️  [{alert.severity.upper()}] {alert.alert_type.replace('_', ' ').title()}"
            )
            print(f"   {alert.description}")
            if alert.affected_steps:
                print(f"   Affected Steps: {', '.join(alert.affected_steps)}")
            if alert.affected_agents:
                print(f"   Affected Agents: {', '.join(alert.affected_agents)}")
            if alert.resolution_suggestion:
                print(f"   Suggestion: {alert.resolution_suggestion}")


def main():
    # Example usage
    print("Automated Bottleneck Detection System")
    print("=" * 40)

    # Create detector and dashboard
    detector = BottleneckDetector()
    dashboard = BottleneckDashboard(detector)

    print("Bottleneck detection system initialized")
    print("System ready to automatically identify and alert on workflow bottlenecks")

    # Example of what the workflow would look like:
    print("\nExample workflow:")
    print("  1. Track workflow steps as they start and complete")
    print("  2. Analyze step durations and patterns")
    print("  3. Detect various types of bottlenecks")
    print("  4. Generate alerts for performance issues")
    print("  5. Provide resolution suggestions")


if __name__ == "__main__":
    main()
