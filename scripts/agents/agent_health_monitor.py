#!/usr/bin/env python3
"""
Agent Health Monitoring
Implements health checks and automatic failover for agent failures.
"""

import psutil
import time
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ..task_queue import Agent


class AgentHealthMetrics:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.cpu_usage: List[float] = []
        self.memory_usage: List[float] = []
        self.task_success_rate: List[float] = []
        self.heartbeat_timestamps: List[str] = []
        self.last_check = datetime.now().isoformat()
        self.is_healthy = True
        self.alerts: List[Dict] = []
        
    def add_heartbeat(self):
        """Record a heartbeat from the agent."""
        self.heartbeat_timestamps.append(datetime.now().isoformat())
        
        # Keep only last 100 heartbeats
        if len(self.heartbeat_timestamps) > 100:
            self.heartbeat_timestamps = self.heartbeat_timestamps[-100:]
            
    def add_system_metrics(self, cpu_percent: float, memory_percent: float):
        """Add system resource metrics."""
        self.cpu_usage.append(cpu_percent)
        self.memory_usage.append(memory_percent)
        
        # Keep only last 100 measurements
        if len(self.cpu_usage) > 100:
            self.cpu_usage = self.cpu_usage[-100:]
        if len(self.memory_usage) > 100:
            self.memory_usage = self.memory_usage[-100:]
            
    def add_task_success_rate(self, success_rate: float):
        """Add task success rate metric."""
        self.task_success_rate.append(success_rate)
        
        # Keep only last 100 measurements
        if len(self.task_success_rate) > 100:
            self.task_success_rate = self.task_success_rate[-100:]
            
    def get_health_score(self) -> float:
        """Calculate overall health score (0.0 to 1.0)."""
        if not self.cpu_usage or not self.memory_usage or not self.task_success_rate:
            return 1.0  # Assume healthy if no data
            
        # CPU usage factor (prefer < 80%)
        avg_cpu = sum(self.cpu_usage) / len(self.cpu_usage)
        cpu_score = max(0.0, 1.0 - (avg_cpu / 100.0))
        
        # Memory usage factor (prefer < 85%)
        avg_memory = sum(self.memory_usage) / len(self.memory_usage)
        memory_score = max(0.0, 1.0 - (avg_memory / 100.0))
        
        # Task success rate factor (prefer > 90%)
        avg_success = sum(self.task_success_rate) / len(self.task_success_rate)
        success_score = avg_success
        
        # Heartbeat factor (check if recent heartbeat)
        if self.heartbeat_timestamps:
            last_heartbeat = datetime.fromisoformat(self.heartbeat_timestamps[-1])
            time_since_heartbeat = datetime.now() - last_heartbeat
            # Prefer heartbeats within last 5 minutes
            heartbeat_score = max(0.0, 1.0 - (time_since_heartbeat.total_seconds() / 300.0))
        else:
            heartbeat_score = 0.0
            
        # Weighted average
        health_score = (
            cpu_score * 0.25 +
            memory_score * 0.25 +
            success_score * 0.35 +
            heartbeat_score * 0.15
        )
        
        return max(0.0, min(1.0, health_score))  # Clamp between 0 and 1
        
    def is_failing(self) -> bool:
        """Check if agent is failing based on health score."""
        return self.get_health_score() < 0.3  # Threshold for failure
        
    def needs_attention(self) -> bool:
        """Check if agent needs attention based on health score."""
        return self.get_health_score() < 0.7  # Threshold for attention
        
    def add_alert(self, alert_type: str, message: str, severity: str = "warning"):
        """Add an alert for this agent."""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'message': message,
            'severity': severity
        }
        self.alerts.append(alert)
        
        # Keep only last 50 alerts
        if len(self.alerts) > 50:
            self.alerts = self.alerts[-50:]
            
    def get_recent_alerts(self, hours: int = 24) -> List[Dict]:
        """Get recent alerts within specified hours."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_alerts = []
        
        for alert in self.alerts:
            alert_time = datetime.fromisoformat(alert['timestamp'])
            if alert_time > cutoff_time:
                recent_alerts.append(alert)
                
        return recent_alerts


class AgentHealthMonitor:
    def __init__(self, metrics_file: Optional[Path] = None):
        self.metrics_file = metrics_file or Path("agent_health_metrics.json")
        self.agent_metrics: Dict[str, AgentHealthMetrics] = {}
        self.agents: List[Agent] = []
        self.alert_thresholds = {
            'cpu_usage': 80.0,      # % CPU usage
            'memory_usage': 85.0,   # % Memory usage
            'success_rate': 0.85,   # 85% success rate
            'heartbeat_timeout': 300  # 5 minutes in seconds
        }
        self._load_metrics()
        
    def _load_metrics(self):
        """Load metrics from file."""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    data = json.load(f)
                    for agent_name, metrics_data in data.items():
                        metrics = AgentHealthMetrics(agent_name)
                        metrics.cpu_usage = metrics_data.get('cpu_usage', [])
                        metrics.memory_usage = metrics_data.get('memory_usage', [])
                        metrics.task_success_rate = metrics_data.get('task_success_rate', [])
                        metrics.heartbeat_timestamps = metrics_data.get('heartbeat_timestamps', [])
                        metrics.alerts = metrics_data.get('alerts', [])
                        metrics.last_check = metrics_data.get('last_check', datetime.now().isoformat())
                        self.agent_metrics[agent_name] = metrics
            except Exception as e:
                print(f"Error loading metrics: {e}")
                
    def _save_metrics(self):
        """Save metrics to file."""
        try:
            data = {}
            for agent_name, metrics in self.agent_metrics.items():
                data[agent_name] = {
                    'cpu_usage': metrics.cpu_usage,
                    'memory_usage': metrics.memory_usage,
                    'task_success_rate': metrics.task_success_rate,
                    'heartbeat_timestamps': metrics.heartbeat_timestamps,
                    'alerts': metrics.alerts,
                    'last_check': metrics.last_check
                }
            with open(self.metrics_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving metrics: {e}")
            
    def register_agent(self, agent: Agent):
        """Register an agent for health monitoring."""
        if agent.name not in self.agent_metrics:
            self.agent_metrics[agent.name] = AgentHealthMetrics(agent.name)
        if agent not in self.agents:
            self.agents.append(agent)
            
    def send_heartbeat(self, agent_name: str):
        """Record a heartbeat from an agent."""
        if agent_name in self.agent_metrics:
            self.agent_metrics[agent_name].add_heartbeat()
            self._save_metrics()
            
    def update_system_metrics(self, agent_name: str, cpu_percent: float, memory_percent: float):
        """Update system metrics for an agent."""
        if agent_name in self.agent_metrics:
            self.agent_metrics[agent_name].add_system_metrics(cpu_percent, memory_percent)
            self._check_thresholds(agent_name, cpu_percent, memory_percent)
            self._save_metrics()
            
    def update_task_success_rate(self, agent_name: str, success_rate: float):
        """Update task success rate for an agent."""
        if agent_name in self.agent_metrics:
            self.agent_metrics[agent_name].add_task_success_rate(success_rate)
            self._check_success_rate_threshold(agent_name, success_rate)
            self._save_metrics()
            
    def _check_thresholds(self, agent_name: str, cpu_percent: float, memory_percent: float):
        """Check if metrics exceed thresholds and generate alerts."""
        metrics = self.agent_metrics[agent_name]
        
        if cpu_percent > self.alert_thresholds['cpu_usage']:
            metrics.add_alert(
                'high_cpu',
                f'CPU usage is {cpu_percent:.1f}%, exceeding threshold of {self.alert_thresholds["cpu_usage"]}%'
            )
            
        if memory_percent > self.alert_thresholds['memory_usage']:
            metrics.add_alert(
                'high_memory',
                f'Memory usage is {memory_percent:.1f}%, exceeding threshold of {self.alert_thresholds["memory_usage"]}%'
            )
            
    def _check_success_rate_threshold(self, agent_name: str, success_rate: float):
        """Check if success rate falls below threshold."""
        if success_rate < self.alert_thresholds['success_rate']:
            metrics = self.agent_metrics[agent_name]
            metrics.add_alert(
                'low_success_rate',
                f'Task success rate is {success_rate:.2%}, below threshold of {self.alert_thresholds["success_rate"]:.2%}'
            )
            
    def check_heartbeat_timeout(self):
        """Check for agents that haven't sent heartbeats recently."""
        timeout_seconds = self.alert_thresholds['heartbeat_timeout']
        current_time = datetime.now()
        
        for agent_name, metrics in self.agent_metrics.items():
            if metrics.heartbeat_timestamps:
                last_heartbeat = datetime.fromisoformat(metrics.heartbeat_timestamps[-1])
                time_since_heartbeat = (current_time - last_heartbeat).total_seconds()
                
                if time_since_heartbeat > timeout_seconds:
                    metrics.add_alert(
                        'heartbeat_timeout',
                        f'No heartbeat received for {time_since_heartbeat:.0f} seconds, exceeding timeout of {timeout_seconds} seconds',
                        'critical'
                    )
                    
    def get_agent_health(self, agent_name: str) -> Optional[Dict]:
        """Get health information for a specific agent."""
        if agent_name not in self.agent_metrics:
            return None
            
        metrics = self.agent_metrics[agent_name]
        return {
            'agent_name': agent_name,
            'health_score': metrics.get_health_score(),
            'is_healthy': metrics.get_health_score() >= 0.7,
            'is_failing': metrics.is_failing(),
            'needs_attention': metrics.needs_attention(),
            'cpu_usage': metrics.cpu_usage[-1] if metrics.cpu_usage else None,
            'memory_usage': metrics.memory_usage[-1] if metrics.memory_usage else None,
            'success_rate': metrics.task_success_rate[-1] if metrics.task_success_rate else None,
            'recent_alerts': metrics.get_recent_alerts(24)
        }
        
    def get_all_agents_health(self) -> Dict:
        """Get health information for all agents."""
        health_data = {}
        for agent_name in self.agent_metrics.keys():
            health_data[agent_name] = self.get_agent_health(agent_name)
        return health_data
        
    def get_system_overview(self) -> Dict:
        """Get overall system health overview."""
        health_data = self.get_all_agents_health()
        
        total_agents = len(health_data)
        healthy_agents = len([h for h in health_data.values() if h and h['is_healthy']])
        failing_agents = len([h for h in health_data.values() if h and h['is_failing']])
        attention_agents = len([h for h in health_data.values() if h and h['needs_attention']])
        
        # Get system metrics
        system_cpu = psutil.cpu_percent()
        system_memory = psutil.virtual_memory().percent
        
        return {
            'total_agents': total_agents,
            'healthy_agents': healthy_agents,
            'failing_agents': failing_agents,
            'attention_agents': attention_agents,
            'system_cpu_usage': system_cpu,
            'system_memory_usage': system_memory,
            'overall_health': healthy_agents / total_agents if total_agents > 0 else 1.0
        }
        
    def get_failing_agents(self) -> List[str]:
        """Get list of failing agents that need failover."""
        failing_agents = []
        for agent_name, metrics in self.agent_metrics.items():
            if metrics.is_failing():
                failing_agents.append(agent_name)
        return failing_agents
        
    def trigger_failover(self, failing_agent_name: str) -> bool:
        """Trigger failover for a failing agent."""
        # In a real implementation, this would:
        # 1. Reassign tasks from failing agent to healthy agents
        # 2. Alert system administrators
        # 3. Potentially restart the agent
        # 4. Log the failover event
        
        print(f"Failover triggered for agent: {failing_agent_name}")
        
        # Add alert
        if failing_agent_name in self.agent_metrics:
            self.agent_metrics[failing_agent_name].add_alert(
                'failover_triggered',
                f'Automatic failover initiated for agent {failing_agent_name}',
                'critical'
            )
            self._save_metrics()
            
        return True


def main():
    # Example usage
    monitor = AgentHealthMonitor()
    
    # Register some agents
    api_agent = Agent("api-writer", ["api", "general"], 5)
    guide_agent = Agent("guide-writer", ["guide", "general"], 3)
    
    monitor.register_agent(api_agent)
    monitor.register_agent(guide_agent)
    
    # Send some heartbeats
    monitor.send_heartbeat("api-writer")
    monitor.send_heartbeat("guide-writer")
    
    # Update system metrics
    monitor.update_system_metrics("api-writer", 45.0, 60.0)
    monitor.update_system_metrics("guide-writer", 30.0, 55.0)
    
    # Update task success rates
    monitor.update_task_success_rate("api-writer", 0.95)
    monitor.update_task_success_rate("guide-writer", 0.88)
    
    # Get health status
    api_health = monitor.get_agent_health("api-writer")
    print(f"API Writer Health: {api_health}")
    
    # Get system overview
    overview = monitor.get_system_overview()
    print(f"System Overview: {overview}")
    
    print("Agent health monitoring system initialized")


if __name__ == "__main__":
    main()