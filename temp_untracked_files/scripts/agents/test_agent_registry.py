#!/usr/bin/env python3
"""
Test script for agent capability registry
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from agent_registry import AgentCapabilityRegistry
from ..task_queue import Agent

def test_agent_registry():
    """Test the agent capability registry."""
    print("Testing Agent Capability Registry...")
    
    # Create registry
    registry = AgentCapabilityRegistry()
    
    # Register some capabilities
    registry.register_capability("api", "API documentation writing", "documentation")
    registry.register_capability("guide", "User guide writing", "documentation")
    registry.register_capability("arch", "Architecture documentation", "documentation")
    
    # Create test agents
    api_agent = Agent("api-writer", ["api", "general"], 5)
    guide_agent = Agent("guide-writer", ["guide", "general"], 3)
    
    # Register agents
    registry.register_agent(api_agent)
    registry.register_agent(guide_agent)
    
    # Test matching
    api_agents = registry.get_agents_with_capability("api")
    print(f"Agents with API capability: {[a.agent_name for a in api_agents]}")
    
    guide_agents = registry.get_agents_with_capability("guide")
    print(f"Agents with Guide capability: {[a.agent_name for a in guide_agents]}")
    
    # Test registry stats
    stats = registry.get_registry_stats()
    print(f"Registry stats: {stats}")
    
    print("Agent registry test completed successfully!")

if __name__ == "__main__":
    test_agent_registry()