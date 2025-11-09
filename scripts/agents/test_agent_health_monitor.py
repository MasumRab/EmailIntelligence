#!/usr/bin/env python3
"""
Test script for agent health monitor
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

from agent_health_monitor import AgentHealthMonitor
from ..task_queue import Agent


def test_agent_health_monitor():
    """Test the agent health monitoring system."""
    print("Testing Agent Health Monitoring System...")

    # Create monitor
    monitor = AgentHealthMonitor()

    # Register some agents
    api_agent = Agent("api-writer", ["api", "general"], 5)
    guide_agent = Agent("guide-writer", ["guide", "general"], 3)
    arch_agent = Agent("architect", ["arch", "general"], 2)

    monitor.register_agent(api_agent)
    monitor.register_agent(guide_agent)
    monitor.register_agent(arch_agent)

    # Send heartbeats
    monitor.send_heartbeat("api-writer")
    monitor.send_heartbeat("guide-writer")
    monitor.send_heartbeat("architect")

    # Update system metrics
    monitor.update_system_metrics("api-writer", 45.0, 60.0)
    monitor.update_system_metrics("guide-writer", 30.0, 55.0)
    monitor.update_system_metrics("architect", 75.0, 80.0)

    # Update task success rates
    monitor.update_task_success_rate("api-writer", 0.95)
    monitor.update_task_success_rate("guide-writer", 0.88)
    monitor.update_task_success_rate("architect", 0.92)

    # Get individual agent health
    api_health = monitor.get_agent_health("api-writer")
    guide_health = monitor.get_agent_health("guide-writer")
    arch_health = monitor.get_agent_health("architect")

    if api_health:
        print(f"API Writer Health Score: {api_health['health_score']:.2f}")
    if guide_health:
        print(f"Guide Writer Health Score: {guide_health['health_score']:.2f}")
    if arch_health:
        print(f"Architect Health Score: {arch_health['health_score']:.2f}")

    # Get system overview
    overview = monitor.get_system_overview()
    print("System Overview:")
    print(f"  Total Agents: {overview['total_agents']}")
    print(f"  Healthy Agents: {overview['healthy_agents']}")
    print(f"  Overall Health: {overview['overall_health']:.2%}")
    print(f"  System CPU: {overview['system_cpu_usage']:.1f}%")
    print(f"  System Memory: {overview['system_memory_usage']:.1f}%")

    # Test alerts
    monitor.update_system_metrics("architect", 85.0, 90.0)  # High usage
    arch_health = monitor.get_agent_health("architect")
    if arch_health and arch_health["recent_alerts"]:
        print(f"Architect has {len(arch_health['recent_alerts'])} recent alerts")

    print("Agent health monitor test completed successfully!")


if __name__ == "__main__":
    test_agent_health_monitor()
