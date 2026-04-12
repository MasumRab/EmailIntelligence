#!/usr/bin/env python3
"""
Load Balancer for Documentation Tasks
Implements automatic task distribution based on agent capabilities and performance history.
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from task_queue import TaskRouter, Agent, Task, TaskQueue, Priority, TaskStatus


class LoadBalancer:
    def __init__(self, router: TaskRouter):
        self.router = router
        self.performance_history = {}
        self.agent_registry = {}
        
    def register_agent(self, agent: Agent):
        """Register an agent with the load balancer."""
        self.agent_registry[agent.name] = agent
        self.performance_history[agent.name] = []
        
    def update_agent_performance(self, agent_name: str, task_completion_time: int, success: bool = True):
        """Update performance history for an agent."""
        if agent_name in self.performance_history:
            self.performance_history[agent_name].append({
                'timestamp': datetime.now().isoformat(),
                'completion_time': task_completion_time,
                'success': success
            })
            
            # Keep only last 100 entries
            if len(self.performance_history[agent_name]) > 100:
                self.performance_history[agent_name] = self.performance_history[agent_name][-100:]
    
    def get_agent_efficiency(self, agent_name: str) -> float:
        """Calculate agent efficiency based on performance history."""
        if agent_name not in self.performance_history:
            return 1.0  # Default efficiency
            
        history = self.performance_history[agent_name]
        if not history:
            return 1.0
            
        # Calculate success rate
        successful_tasks = len([h for h in history if h['success']])
        success_rate = successful_tasks / len(history)
        
        # Calculate average completion time (lower is better)
        completion_times = [h['completion_time'] for h in history if h['success']]
        if not completion_times:
            return success_rate
            
        avg_time = sum(completion_times) / len(completion_times)
        # Normalize time (assuming 30 minutes is baseline)
        time_efficiency = min(1.0, 30 / avg_time) if avg_time > 0 else 1.0
        
        # Combined efficiency score
        efficiency = (success_rate * 0.7) + (time_efficiency * 0.3)
        return efficiency
    
    def balance_load(self):
        """Distribute tasks evenly across available agents."""
        # Get all pending tasks
        pending_tasks = []
        for queue in self.router.queues.values():
            pending_tasks.extend([t for t in queue.tasks if t.status == TaskStatus.PENDING])
        
        if not pending_tasks:
            return
            
        # Sort tasks by priority
        pending_tasks.sort(key=lambda t: t.priority.value)
        
        # Distribute tasks based on agent efficiency and capacity
        for task in pending_tasks:
            best_agent = self._find_best_agent_for_task(task)
            if best_agent:
                self._assign_task_to_agent(task, best_agent)
    
    def find_best_agent_for_task(self, task: Task) -> Optional[Agent]:
        """Find the best agent for a specific task."""
        suitable_agents = []
        
        # Find agents that can handle this task type
        for agent in self.router.agents:
            if agent.can_handle_task(task) and agent.has_capacity():
                suitable_agents.append(agent)
        
        if not suitable_agents:
            return None
            
        # Rank agents by efficiency and current load
        ranked_agents = []
        for agent in suitable_agents:
            efficiency = self.get_agent_efficiency(agent.name)
            # Prefer agents with lower current load
            load_factor = 1.0 - (agent.current_load / agent.max_concurrent_tasks)
            score = (efficiency * 0.7) + (load_factor * 0.3)
            ranked_agents.append((agent, score))
        
        # Sort by score (highest first)
        ranked_agents.sort(key=lambda x: x[1], reverse=True)
        return ranked_agents[0][0] if ranked_agents else None
    
    def assign_task_to_agent(self, task: Task, agent: Agent):
        """Assign a task to an agent through the router."""
        # Find the queue that contains this task
        for queue in self.router.queues.values():
            if task in queue.tasks:
                queue.mark_task_assigned(task, agent.name)
                agent.assign_task(task)
                break
    
    def get_load_balancing_stats(self) -> Dict:
        """Get load balancing statistics."""
        stats = {
            'total_agents': len(self.router.agents),
            'active_agents': len([a for a in self.router.agents if a.current_load > 0]),
            'agent_efficiencies': {},
            'load_distribution': {}
        }
        
        for agent in self.router.agents:
            stats['agent_efficiencies'][agent.name] = self.get_agent_efficiency(agent.name)
            stats['load_distribution'][agent.name] = {
                'current_load': agent.current_load,
                'max_capacity': agent.max_concurrent_tasks,
                'utilization': agent.get_utilization_rate()
            }
            
        return stats
    
    def scale_agents(self, target_utilization: float = 0.85):
        """Dynamically scale agents based on current load."""
        # This is a simplified version - in a real system, this would
        # interact with a resource manager to add/remove agents
        current_utilization = self._get_average_utilization()
        
        if current_utilization > target_utilization * 1.2:
            # System is overloaded - would add more agents
            return "scale_up"
        elif current_utilization < target_utilization * 0.8:
            # System is underloaded - could remove agents
            return "scale_down"
        else:
            return "stable"
    
    def _get_average_utilization(self) -> float:
        """Calculate average agent utilization."""
        if not self.router.agents:
            return 0.0
            
        total_utilization = sum(agent.get_utilization_rate() for agent in self.router.agents)
        return total_utilization / len(self.router.agents)


def main():
    # Create task router
    router = TaskRouter()
    
    # Create queues
    router.add_queue(TaskQueue('api_docs'))
    router.add_queue(TaskQueue('user_guides'))
    router.add_queue(TaskQueue('architecture'))
    router.add_queue(TaskQueue('general'))
    
    # Create agents
    api_agent = Agent('api-writer', ['api', 'general'], 5)
    guide_agent = Agent('guide-writer', ['guide', 'general'], 3)
    arch_agent = Agent('architect', ['arch', 'general'], 2)
    
    # Add agents to router
    router.add_agent(api_agent)
    router.add_agent(guide_agent)
    router.add_agent(arch_agent)
    
    # Create load balancer
    load_balancer = LoadBalancer(router)
    load_balancer.register_agent(api_agent)
    load_balancer.register_agent(guide_agent)
    load_balancer.register_agent(arch_agent)
    
    # Example usage would go here
    
    print("Load balancer initialized")
    stats = load_balancer.get_load_balancing_stats()
    print(f"Agent efficiencies: {stats['agent_efficiencies']}")
    print(f"Load distribution: {stats['load_distribution']}")


if __name__ == "__main__":
    main()