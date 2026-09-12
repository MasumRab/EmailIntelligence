#!/usr/bin/env python3
"""
Resource Utilization Monitoring
Track system resources used by parallel agents.
"""

import psutil
import time
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, deque
import statistics
from datetime import datetime, timedelta


@dataclass
class ResourceSnapshot:
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_available: int  # bytes
    disk_io_read: int  # bytes
    disk_io_write: int  # bytes
    network_io_sent: int  # bytes
    network_io_recv: int  # bytes
    process_count: int
    load_average: Tuple[float, float, float]  # 1, 5, 15 minute load averages


@dataclass
class ProcessResourceUsage:
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    memory_rss: int  # bytes
    memory_vms: int  # bytes
    create_time: float
    status: str
    username: str
    cmdline: List[str]


@dataclass
class ResourceAlert:
    alert_id: str
    resource_type: str  # "cpu", "memory", "disk", "network", "process"
    severity: str  # "low", "medium", "high", "critical"
    description: str
    current_value: float
    threshold_value: float
    timestamp: float
    affected_processes: List[int] = field(default_factory=list)
    resolution_suggestion: str = ""


class ResourceMonitor:
    def __init__(self, monitoring_file: Path = None, max_history: int = 1000):
        self.monitoring_file = monitoring_file or Path(".resource_monitoring.json")
        self.max_history = max_history
        self.system_resources: deque = deque(maxlen=max_history)
        self.process_resources: Dict[int, deque] = defaultdict(lambda: deque(maxlen=max_history))
        self._lock = threading.RLock()
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_interval = 5.0  # seconds
        self.load_monitoring()

    def start_monitoring(self, interval: float = 5.0):
        """Start resource monitoring in a background thread."""
        if self.monitoring_active:
            return

        self.monitoring_interval = interval
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()

    def stop_monitoring(self):
        """Stop resource monitoring."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join()

    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                self._collect_system_resources()
                self._collect_process_resources()
                time.sleep(self.monitoring_interval)
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(self.monitoring_interval)

    def _collect_system_resources(self):
        """Collect system-level resource usage."""
        try:
            # Get system resources
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk_io = psutil.disk_io_counters()
            network_io = psutil.net_io_counters()
            process_count = len(psutil.pids())
            load_average = psutil.getloadavg() if hasattr(psutil, 'getloadavg') else (0.0, 0.0, 0.0)

            snapshot = ResourceSnapshot(
                timestamp=time.time(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_available=memory.available,
                disk_io_read=disk_io.read_bytes if disk_io else 0,
                disk_io_write=disk_io.write_bytes if disk_io else 0,
                network_io_sent=network_io.bytes_sent if network_io else 0,
                network_io_recv=network_io.bytes_recv if network_io else 0,
                process_count=process_count,
                load_average=load_average
            )

            with self._lock:
                self.system_resources.append(snapshot)
                self._save_monitoring_data()

        except Exception as e:
            print(f"Error collecting system resources: {e}")

    def _collect_process_resources(self):
        """Collect process-level resource usage."""
        try:
            # Get all running processes
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent',
                                           'memory_info', 'create_time', 'status', 'username',
                                           'cmdline']):
                try:
                    # Skip system processes
                    if proc.info['pid'] <= 1:
                        continue

                    # Get process info
                    pid = proc.info['pid']
                    name = proc.info['name'] or "unknown"
                    cpu_percent = proc.info['cpu_percent'] or 0.0
                    memory_percent = proc.info['memory_percent'] or 0.0

                    memory_info = proc.info['memory_info']
                    memory_rss = memory_info.rss if memory_info else 0
                    memory_vms = memory_info.vms if memory_info else 0

                    create_time = proc.info['create_time'] or 0.0
                    status = proc.info['status'] or "unknown"
                    username = proc.info['username'] or "unknown"
                    cmdline = proc.info['cmdline'] or []

                    process_usage = ProcessResourceUsage(
                        pid=pid,
                        name=name,
                        cpu_percent=cpu_percent,
                        memory_percent=memory_percent,
                        memory_rss=memory_rss,
                        memory_vms=memory_vms,
                        create_time=create_time,
                        status=status,
                        username=username,
                        cmdline=cmdline
                    )

                    with self._lock:
                        self.process_resources[pid].append(process_usage)

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Process may have terminated or we don't have access
                    continue

            with self._lock:
                self._save_monitoring_data()

        except Exception as e:
            print(f"Error collecting process resources: {e}")

    def get_system_resource_history(self, hours: int = 1) -> List[ResourceSnapshot]:
        """Get system resource history for the specified time period."""
        cutoff_time = time.time() - (hours * 3600)

        with self._lock:
            return [
                snapshot for snapshot in self.system_resources
                if snapshot.timestamp >= cutoff_time
            ]

    def get_process_resource_history(self, pid: int, hours: int = 1) -> List[ProcessResourceUsage]:
        """Get process resource history for the specified time period."""
        cutoff_time = time.time() - (hours * 3600)

        with self._lock:
            if pid not in self.process_resources:
                return []

            return [
                usage for usage in self.process_resources[pid]
                if usage.create_time >= cutoff_time or usage.timestamp >= cutoff_time
            ]

    def get_top_processes_by_resource(self, resource_type: str = "cpu",
                                    limit: int = 10) -> List[ProcessResourceUsage]:
        """Get top processes by resource usage."""
        with self._lock:
            # Get the most recent resource usage for each process
            latest_usage = {}
            for pid, usage_history in self.process_resources.items():
                if usage_history:
                    latest_usage[pid] = usage_history[-1]

            # Sort by resource usage
            if resource_type == "cpu":
                sorted_processes = sorted(
                    latest_usage.values(),
                    key=lambda x: x.cpu_percent,
                    reverse=True
                )
            elif resource_type == "memory":
                sorted_processes = sorted(
                    latest_usage.values(),
                    key=lambda x: x.memory_percent,
                    reverse=True
                )
            else:
                sorted_processes = list(latest_usage.values())

            return sorted_processes[:limit]

    def get_system_resource_stats(self, hours: int = 1) -> Dict[str, Any]:
        """Get system resource statistics for the specified time period."""
        history = self.get_system_resource_history(hours)

        if not history:
            return {}

        # Calculate statistics
        cpu_percentages = [s.cpu_percent for s in history]
        memory_percentages = [s.memory_percent for s in history]
        process_counts = [s.process_count for s in history]

        return {
            'time_window_hours': hours,
            'sample_count': len(history),
            'cpu': {
                'mean': statistics.mean(cpu_percentages),
                'median': statistics.median(cpu_percentages),
                'stdev': statistics.stdev(cpu_percentages) if len(cpu_percentages) > 1 else 0.0,
                'min': min(cpu_percentages),
                'max': max(cpu_percentages),
                'percentile_95': self._percentile(cpu_percentages, 95),
                'percentile_99': self._percentile(cpu_percentages, 99)
            },
            'memory': {
                'mean': statistics.mean(memory_percentages),
                'median': statistics.median(memory_percentages),
                'stdev': statistics.stdev(memory_percentages) if len(memory_percentages) > 1 else 0.0,
                'min': min(memory_percentages),
                'max': max(memory_percentages),
                'percentile_95': self._percentile(memory_percentages, 95),
                'percentile_99': self._percentile(memory_percentages, 99)
            },
            'processes': {
                'mean': statistics.mean(process_counts),
                'median': statistics.median(process_counts),
                'min': min(process_counts),
                'max': max(process_counts)
            }
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

    def detect_resource_alerts(self, cpu_threshold: float = 80.0,
                             memory_threshold: float = 85.0,
                             process_threshold: int = 500) -> List[ResourceAlert]:
        """Detect resource utilization alerts."""
        alerts = []

        with self._lock:
            if not self.system_resources:
                return alerts

            # Get latest system resource snapshot
            latest = self.system_resources[-1]

            # Check CPU usage
            if latest.cpu_percent > cpu_threshold:
                severity = "critical" if latest.cpu_percent > cpu_threshold * 1.2 else "high"
                alert = ResourceAlert(
                    alert_id=f"cpu_overload_{int(latest.timestamp)}",
                    resource_type="cpu",
                    severity=severity,
                    description=f"CPU usage is {latest.cpu_percent:.1f}%, exceeding threshold of {cpu_threshold}%",
                    current_value=latest.cpu_percent,
                    threshold_value=cpu_threshold,
                    timestamp=latest.timestamp,
                    resolution_suggestion="Check for CPU-intensive processes and consider scaling or optimization"
                )
                alerts.append(alert)

            # Check memory usage
            if latest.memory_percent > memory_threshold:
                severity = "critical" if latest.memory_percent > memory_threshold * 1.1 else "high"
                alert = ResourceAlert(
                    alert_id=f"memory_overload_{int(latest.timestamp)}",
                    resource_type="memory",
                    severity=severity,
                    description=f"Memory usage is {latest.memory_percent:.1f}%, exceeding threshold of {memory_threshold}%",
                    current_value=latest.memory_percent,
                    threshold_value=memory_threshold,
                    timestamp=latest.timestamp,
                    resolution_suggestion="Check for memory leaks and consider adding more RAM or optimizing memory usage"
                )
                alerts.append(alert)

            # Check process count
            if latest.process_count > process_threshold:
                severity = "high" if latest.process_count > process_threshold * 1.5 else "medium"
                alert = ResourceAlert(
                    alert_id=f"process_overload_{int(latest.timestamp)}",
                    resource_type="process",
                    severity=severity,
                    description=f"Process count is {latest.process_count}, exceeding threshold of {process_threshold}",
                    current_value=latest.process_count,
                    threshold_value=process_threshold,
                    timestamp=latest.timestamp,
                    resolution_suggestion="Check for process leaks and consider process management optimization"
                )
                alerts.append(alert)

        return alerts

    def get_resource_utilization_summary(self) -> Dict[str, Any]:
        """Get a summary of current resource utilization."""
        with self._lock:
            if not self.system_resources:
                return {}

            latest = self.system_resources[-1]

            # Get recent alerts
            recent_alerts = self.detect_resource_alerts()

            # Get top processes
            top_cpu_processes = self.get_top_processes_by_resource("cpu", 5)
            top_memory_processes = self.get_top_processes_by_resource("memory", 5)

            return {
                'timestamp': latest.timestamp,
                'system_resources': {
                    'cpu_percent': latest.cpu_percent,
                    'memory_percent': latest.memory_percent,
                    'memory_available_gb': latest.memory_available / (1024**3),
                    'process_count': latest.process_count,
                    'load_average': latest.load_average
                },
                'top_processes': {
                    'cpu': [
                        {
                            'pid': p.pid,
                            'name': p.name,
                            'cpu_percent': p.cpu_percent,
                            'memory_percent': p.memory_percent
                        }
                        for p in top_cpu_processes
                    ],
                    'memory': [
                        {
                            'pid': p.pid,
                            'name': p.name,
                            'cpu_percent': p.cpu_percent,
                            'memory_percent': p.memory_percent,
                            'memory_rss_mb': p.memory_rss / (1024**2)
                        }
                        for p in top_memory_processes
                    ]
                },
                'recent_alerts': len(recent_alerts),
                'alerts_by_severity': {
                    'critical': len([a for a in recent_alerts if a.severity == 'critical']),
                    'high': len([a for a in recent_alerts if a.severity == 'high']),
                    'medium': len([a for a in recent_alerts if a.severity == 'medium']),
                    'low': len([a for a in recent_alerts if a.severity == 'low'])
                }
            }

    def _save_monitoring_data(self):
        """Save monitoring data to file."""
        try:
            data = {
                'timestamp': time.time(),
                'system_resources': [
                    {
                        'timestamp': s.timestamp,
                        'cpu_percent': s.cpu_percent,
                        'memory_percent': s.memory_percent,
                        'memory_available': s.memory_available,
                        'disk_io_read': s.disk_io_read,
                        'disk_io_write': s.disk_io_write,
                        'network_io_sent': s.network_io_sent,
                        'network_io_recv': s.network_io_recv,
                        'process_count': s.process_count,
                        'load_average': s.load_average
                    }
                    for s in self.system_resources
                ],
                'process_resources': {}
            }

            # Save process resources (only latest snapshot for each process to save space)
            with self._lock:
                for pid, usage_history in self.process_resources.items():
                    if usage_history:
                        latest_usage = usage_history[-1]
                        data['process_resources'][pid] = {
                            'pid': latest_usage.pid,
                            'name': latest_usage.name,
                            'cpu_percent': latest_usage.cpu_percent,
                            'memory_percent': latest_usage.memory_percent,
                            'memory_rss': latest_usage.memory_rss,
                            'memory_vms': latest_usage.memory_vms,
                            'create_time': latest_usage.create_time,
                            'status': latest_usage.status,
                            'username': latest_usage.username,
                            'cmdline': latest_usage.cmdline,
                            'timestamp': time.time()  # Add timestamp for cleanup
                        }

            with open(self.monitoring_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving monitoring data: {e}")

    def load_monitoring(self):
        """Load monitoring data from file."""
        try:
            if not self.monitoring_file.exists():
                return

            with open(self.monitoring_file, 'r') as f:
                data = json.load(f)

            # Restore system resources
            self.system_resources.clear()
            for snapshot_data in data.get('system_resources', []):
                snapshot = ResourceSnapshot(
                    timestamp=snapshot_data['timestamp'],
                    cpu_percent=snapshot_data['cpu_percent'],
                    memory_percent=snapshot_data['memory_percent'],
                    memory_available=snapshot_data['memory_available'],
                    disk_io_read=snapshot_data['disk_io_read'],
                    disk_io_write=snapshot_data['disk_io_write'],
                    network_io_sent=snapshot_data['network_io_sent'],
                    network_io_recv=snapshot_data['network_io_recv'],
                    process_count=snapshot_data['process_count'],
                    load_average=snapshot_data['load_average']
                )
                self.system_resources.append(snapshot)

            # Restore process resources
            self.process_resources.clear()
            for pid_str, usage_data in data.get('process_resources', {}).items():
                pid = int(pid_str)
                usage = ProcessResourceUsage(
                    pid=usage_data['pid'],
                    name=usage_data['name'],
                    cpu_percent=usage_data['cpu_percent'],
                    memory_percent=usage_data['memory_percent'],
                    memory_rss=usage_data['memory_rss'],
                    memory_vms=usage_data['memory_vms'],
                    create_time=usage_data['create_time'],
                    status=usage_data['status'],
                    username=usage_data['username'],
                    cmdline=usage_data['cmdline']
                )

                # Create a deque with the single entry
                usage_deque = deque([usage], maxlen=self.max_history)
                self.process_resources[pid] = usage_deque

        except Exception as e:
            print(f"Error loading monitoring data: {e}")


class ResourceDashboard:
    def __init__(self, monitor: ResourceMonitor):
        self.monitor = monitor

    def display_resource_summary(self):
        """Display resource utilization summary."""
        summary = self.monitor.get_resource_utilization_summary()

        if not summary:
            print("No resource data available")
            return

        timestamp = datetime.fromtimestamp(summary['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        print(f"\nResource Utilization Summary - {timestamp}")
        print("=" * 50)

        sys_resources = summary['system_resources']
        print(f"CPU Usage: {sys_resources['cpu_percent']:.1f}%")
        print(f"Memory Usage: {sys_resources['memory_percent']:.1f}%")
        print(f"Available Memory: {sys_resources['memory_available_gb']:.2f} GB")
        print(f"Process Count: {sys_resources['process_count']}")
        print(f"Load Average: {sys_resources['load_average'][0]:.2f} (1m), "
              f"{sys_resources['load_average'][1]:.2f} (5m), "
              f"{sys_resources['load_average'][2]:.2f} (15m)")

        print(f"\nRecent Alerts: {summary['recent_alerts']}")
        for severity, count in summary['alerts_by_severity'].items():
            if count > 0:
                print(f"  {severity.capitalize()}: {count}")

        print("\nTop CPU Processes:")
        for proc in summary['top_processes']['cpu'][:3]:
            print(f"  PID {proc['pid']} ({proc['name']}): {proc['cpu_percent']:.1f}% CPU")

        print("\nTop Memory Processes:")
        for proc in summary['top_processes']['memory'][:3]:
            print(f"  PID {proc['pid']} ({proc['name']}): {proc['memory_percent']:.1f}% Memory "
                  f"({proc['memory_rss_mb']:.1f} MB RSS)")

    def display_resource_alerts(self):
        """Display resource utilization alerts."""
        alerts = self.monitor.detect_resource_alerts()

        if not alerts:
            print("\nNo resource alerts")
            return

        print(f"\nResource Alerts ({len(alerts)} total)")
        print("=" * 30)

        for alert in sorted(alerts, key=lambda x: x.timestamp, reverse=True):
            timestamp = datetime.fromtimestamp(alert.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n[{timestamp}] {alert.severity.upper()}: {alert.description}")
            if alert.resolution_suggestion:
                print(f"  Suggestion: {alert.resolution_suggestion}")

    def display_resource_trends(self, hours: int = 1):
        """Display resource utilization trends."""
        stats = self.monitor.get_system_resource_stats(hours)

        if not stats:
            print(f"\nNo resource data available for the last {hours} hour(s)")
            return

        print(f"\nResource Trends (Last {hours} hour(s))")
        print("=" * 40)

        cpu_stats = stats['cpu']
        print(f"CPU Usage:")
        print(f"  Mean: {cpu_stats['mean']:.1f}%")
        print(f"  Median: {cpu_stats['median']:.1f}%")
        print(f"  Min: {cpu_stats['min']:.1f}%")
        print(f"  Max: {cpu_stats['max']:.1f}%")
        print(f"  95th Percentile: {cpu_stats['percentile_95']:.1f}%")

        memory_stats = stats['memory']
        print(f"\nMemory Usage:")
        print(f"  Mean: {memory_stats['mean']:.1f}%")
        print(f"  Median: {memory_stats['median']:.1f}%")
        print(f"  Min: {memory_stats['min']:.1f}%")
        print(f"  Max: {memory_stats['max']:.1f}%")
        print(f"  95th Percentile: {memory_stats['percentile_95']:.1f}%")


def main():
    # Example usage
    print("Resource Utilization Monitoring System")
    print("=" * 42)

    # Create monitor and dashboard
    monitor = ResourceMonitor()
    dashboard = ResourceDashboard(monitor)

    print("Resource monitoring system initialized")
    print("System ready to track system resources used by parallel agents")

    # Example of what the workflow would look like:
    print("\nExample workflow:")
    print("  1. Monitor system and process resources in real-time")
    print("  2. Track resource usage patterns and trends")
    print("  3. Detect resource overutilization")
    print("  4. Generate alerts for performance issues")
    print("  5. Provide optimization suggestions")


if __name__ == "__main__":
    main()
