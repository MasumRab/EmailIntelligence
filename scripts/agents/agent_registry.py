#!/usr/bin/env python3
"""
Agent Capability Registry
Tracks and manages agent skills for optimal task assignment.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from ..task_queue import Agent


class Capability:
    def __init__(self, name: str, description: str, category: str):
        self.name = name
        self.description = description
        self.category = category
        self.created_at = datetime.now().isoformat()


class AgentProfile:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.capabilities: List[str] = []
        self.skills: Dict[str, int] = {}  # skill_name: proficiency_level (1-10)
        self.certifications: List[str] = []
        self.training_completed: List[Dict] = []
        self.performance_metrics: Dict = {
            'tasks_completed': 0,
            'success_rate': 0.0,
            'avg_completion_time': 0.0,
            'quality_score': 0.0
        }
        self.last_updated = datetime.now().isoformat()
        
    def add_capability(self, capability: str):
        """Add a capability to the agent."""
        if capability not in self.capabilities:
            self.capabilities.append(capability)
            self.last_updated = datetime.now().isoformat()
            
    def add_skill(self, skill_name: str, proficiency_level: int):
        """Add or update a skill proficiency level."""
        self.skills[skill_name] = max(1, min(10, proficiency_level))
        self.last_updated = datetime.now().isoformat()
        
    def add_certification(self, certification: str):
        """Add a certification to the agent."""
        if certification not in self.certifications:
            self.certifications.append(certification)
            self.last_updated = datetime.now().isoformat()
            
    def add_training(self, training_name: str, completion_date: str, score: float = None):
        """Add completed training to the agent's record."""
        training_record = {
            'training_name': training_name,
            'completion_date': completion_date,
            'score': score,
            'timestamp': datetime.now().isoformat()
        }
        self.training_completed.append(training_record)
        self.last_updated = datetime.now().isoformat()
        
    def update_performance(self, tasks_completed: int = 0, success_rate: float = None, 
                          avg_completion_time: float = None, quality_score: float = None):
        """Update performance metrics."""
        if tasks_completed > 0:
            self.performance_metrics['tasks_completed'] += tasks_completed
            
        if success_rate is not None:
            # Calculate weighted average
            current_tasks = self.performance_metrics['tasks_completed']
            current_rate = self.performance_metrics['success_rate']
            self.performance_metrics['success_rate'] = (
                (current_rate * current_tasks + success_rate * tasks_completed) / 
                (current_tasks + tasks_completed)
            ) if (current_tasks + tasks_completed) > 0 else success_rate
            
        if avg_completion_time is not None:
            current_time = self.performance_metrics['avg_completion_time']
            self.performance_metrics['avg_completion_time'] = (
                (current_time * current_tasks + avg_completion_time * tasks_completed) / 
                (current_tasks + tasks_completed)
            ) if (current_tasks + tasks_completed) > 0 else avg_completion_time
            
        if quality_score is not None:
            current_quality = self.performance_metrics['quality_score']
            self.performance_metrics['quality_score'] = (
                (current_quality * current_tasks + quality_score * tasks_completed) / 
                (current_tasks + tasks_completed)
            ) if (current_tasks + tasks_completed) > 0 else quality_score
            
        self.last_updated = datetime.now().isoformat()


class AgentCapabilityRegistry:
    def __init__(self, registry_file: Path = None):
        self.registry_file = registry_file or Path("agent_registry.json")
        self.agents: Dict[str, AgentProfile] = {}
        self.capabilities: Dict[str, Capability] = {}
        self.load_registry()
        
    def register_agent(self, agent: Agent) -> AgentProfile:
        """Register an agent in the registry."""
        if agent.name not in self.agents:
            profile = AgentProfile(agent.name)
            # Add capabilities from agent
            for capability in agent.capabilities:
                profile.add_capability(capability)
            self.agents[agent.name] = profile
            self.save_registry()
        return self.agents[agent.name]
        
    def register_capability(self, name: str, description: str, category: str) -> Capability:
        """Register a new capability type."""
        if name not in self.capabilities:
            capability = Capability(name, description, category)
            self.capabilities[name] = capability
            self.save_registry()
        return self.capabilities[name]
        
    def get_agent_profile(self, agent_name: str) -> Optional[AgentProfile]:
        """Get an agent's profile."""
        return self.agents.get(agent_name)
        
    def get_agents_with_capability(self, capability: str) -> List[AgentProfile]:
        """Get all agents with a specific capability."""
        return [profile for profile in self.agents.values() 
                if capability in profile.capabilities]
                
    def get_agents_with_skill(self, skill_name: str, min_proficiency: int = 1) -> List[AgentProfile]:
        """Get all agents with a specific skill above minimum proficiency."""
        return [profile for profile in self.agents.values() 
                if profile.skills.get(skill_name, 0) >= min_proficiency]
                
    def match_agent_to_task(self, task_type: str, required_skills: List[str] = None) -> List[AgentProfile]:
        """Find agents that match a task type and required skills."""
        matched_agents = []
        
        # First, try to match by task type/capability
        for profile in self.agents.values():
            if task_type in profile.capabilities:
                # Check required skills if specified
                if required_skills:
                    has_all_skills = True
                    for skill in required_skills:
                        if skill not in profile.skills or profile.skills[skill] < 1:
                            has_all_skills = False
                            break
                    if has_all_skills:
                        matched_agents.append(profile)
                else:
                    matched_agents.append(profile)
                    
        return matched_agents
        
    def update_agent_performance(self, agent_name: str, **kwargs):
        """Update an agent's performance metrics."""
        profile = self.get_agent_profile(agent_name)
        if profile:
            profile.update_performance(**kwargs)
            self.save_registry()
            
    def add_agent_training(self, agent_name: str, training_name: str, completion_date: str, score: float = None):
        """Add training to an agent's record."""
        profile = self.get_agent_profile(agent_name)
        if profile:
            profile.add_training(training_name, completion_date, score)
            self.save_registry()
            
    def save_registry(self):
        """Save the registry to file."""
        data = {
            'agents': {},
            'capabilities': {}
        }
        
        # Serialize agents
        for name, profile in self.agents.items():
            data['agents'][name] = {
                'agent_name': profile.agent_name,
                'capabilities': profile.capabilities,
                'skills': profile.skills,
                'certifications': profile.certifications,
                'training_completed': profile.training_completed,
                'performance_metrics': profile.performance_metrics,
                'last_updated': profile.last_updated
            }
            
        # Serialize capabilities
        for name, capability in self.capabilities.items():
            data['capabilities'][name] = {
                'name': capability.name,
                'description': capability.description,
                'category': capability.category,
                'created_at': capability.created_at
            }
            
        with open(self.registry_file, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load_registry(self):
        """Load the registry from file."""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r') as f:
                    data = json.load(f)
                    
                # Deserialize agents
                for name, agent_data in data.get('agents', {}).items():
                    profile = AgentProfile(agent_data['agent_name'])
                    profile.capabilities = agent_data.get('capabilities', [])
                    profile.skills = agent_data.get('skills', {})
                    profile.certifications = agent_data.get('certifications', [])
                    profile.training_completed = agent_data.get('training_completed', [])
                    profile.performance_metrics = agent_data.get('performance_metrics', {
                        'tasks_completed': 0,
                        'success_rate': 0.0,
                        'avg_completion_time': 0.0,
                        'quality_score': 0.0
                    })
                    profile.last_updated = agent_data.get('last_updated', datetime.now().isoformat())
                    self.agents[name] = profile
                    
                # Deserialize capabilities
                for name, cap_data in data.get('capabilities', {}).items():
                    capability = Capability(
                        cap_data['name'],
                        cap_data['description'],
                        cap_data['category']
                    )
                    capability.created_at = cap_data.get('created_at', datetime.now().isoformat())
                    self.capabilities[name] = capability
                    
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading registry: {e}")
                
    def get_registry_stats(self) -> Dict:
        """Get statistics about the registry."""
        return {
            'total_agents': len(self.agents),
            'total_capabilities': len(self.capabilities),
            'agents_by_capability': {
                cap: len(self.get_agents_with_capability(cap)) 
                for cap in self.capabilities.keys()
            },
            'recently_updated': [
                profile.agent_name 
                for profile in self.agents.values() 
                if datetime.fromisoformat(profile.last_updated) > datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            ]
        }


def main():
    # Example usage
    registry = AgentCapabilityRegistry()
    
    # Register some capabilities
    registry.register_capability("api", "API documentation writing", "documentation")
    registry.register_capability("guide", "User guide writing", "documentation")
    registry.register_capability("arch", "Architecture documentation", "documentation")
    registry.register_capability("markdown", "Markdown formatting", "formatting")
    registry.register_capability("diagrams", "Creating diagrams", "visual")
    
    print("Agent capability registry initialized")
    print(f"Registered capabilities: {list(registry.capabilities.keys())}")


if __name__ == "__main__":
    main()