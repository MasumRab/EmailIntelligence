"""
Agent Workflow Integration Module

This module provides integration between different agents in the Email Intelligence system.
It handles the coordination and communication between various specialized agents
in the workflow.
"""

from typing import Dict, Any, Optional, List
import logging
from dataclasses import dataclass
from enum import Enum, auto

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Enumeration of different agent types in the system."""
    PROCESSING = auto()
    ANALYSIS = auto()
    VALIDATION = auto()
    ORCHESTRATION = auto()


@dataclass
class WorkflowContext:
    """Context object passed between agents during workflow execution."""
    data: Dict[str, Any]
    metadata: Dict[str, Any] = None
    errors: List[Dict[str, str]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.errors is None:
            self.errors = []
    
    def add_error(self, source: str, message: str) -> None:
        """Add an error to the context.
        
        Args:
            source: The source of the error (e.g., agent name)
            message: Error message
        """
        self.errors.append({"source": source, "message": message})
    
    def has_errors(self) -> bool:
        """Check if there are any errors in the context."""
        return len(self.errors) > 0


class Agent:
    """Base class for all agents in the system."""
    
    def __init__(self, agent_type: AgentType, name: str):
        """Initialize the agent.
        
        Args:
            agent_type: Type of the agent
            name: Unique name for the agent
        """
        self.agent_type = agent_type
        self.name = name
        self.next_agents = []
    
    def process(self, context: WorkflowContext) -> WorkflowContext:
        """Process the workflow context.
        
        Args:
            context: The current workflow context
            
        Returns:
            Updated workflow context
        """
        raise NotImplementedError("Subclasses must implement process()")
    
    def add_next_agent(self, agent: 'Agent') -> None:
        """Add the next agent in the workflow.
        
        Args:
            agent: The next agent to execute
        """
        self.next_agents.append(agent)
    
    def execute_workflow(self, context: WorkflowContext) -> WorkflowContext:
        """Execute this agent and all subsequent agents in the workflow.
        
        Args:
            context: The workflow context
            
        Returns:
            The final workflow context after all agents have executed
        """
        logger.info(f"Executing agent: {self.name}")
        
        try:
            # Process the current agent
            context = self.process(context)
            
            # If there are no errors, continue with next agents
            if not context.has_errors() and self.next_agents:
                for next_agent in self.next_agents:
                    context = next_agent.execute_workflow(context)
                    
        except Exception as e:
            logger.error(f"Error in agent {self.name}: {str(e)}", exc_info=True)
            context.add_error(self.name, f"Processing error: {str(e)}")
        
        return context


class WorkflowOrchestrator:
    """Orchestrates the execution of agents in a workflow."""
    
    def __init__(self):
        self.entry_point: Optional[Agent] = None
        self.agents = {}
    
    def add_agent(self, agent: Agent) -> None:
        """Add an agent to the workflow.
        
        Args:
            agent: The agent to add
        """
        self.agents[agent.name] = agent
        
        # If this is the first agent, set it as the entry point
        if len(self.agents) == 1:
            self.entry_point = agent
    
    def connect_agents(self, from_agent_name: str, to_agent_name: str) -> None:
        """Connect two agents in the workflow.
        
        Args:
            from_agent_name: Name of the source agent
            to_agent_name: Name of the target agent
            
        Raises:
            ValueError: If either agent is not found
        """
        if from_agent_name not in self.agents or to_agent_name not in self.agents:
            raise ValueError("One or both agents not found in the workflow")
            
        self.agents[from_agent_name].add_next_agent(self.agents[to_agent_name])
    
    def execute_workflow(self, initial_data: Dict[str, Any] = None) -> WorkflowContext:
        """Execute the workflow.
        
        Args:
            initial_data: Initial data for the workflow context
            
        Returns:
            The final workflow context after execution
            
        Raises:
            RuntimeError: If no agents are defined in the workflow
        """
        if not self.agents or not self.entry_point:
            raise RuntimeError("No agents defined in the workflow")
        
        context = WorkflowContext(data=initial_data or {})
        return self.entry_point.execute_workflow(context)


def create_default_workflow() -> WorkflowOrchestrator:
    """Create a default workflow with common agents.
    
    Returns:
        A configured workflow orchestrator
    """
    orchestrator = WorkflowOrchestrator()
    
    # Create agents
    # Example: processing_agent = ProcessingAgent("email_processor")
    # orchestrator.add_agent(processing_agent)
    
    # Connect agents
    # Example: orchestrator.connect_agents("email_processor", "analysis_agent")
    
    return orchestrator


def main():
    """Main function to demonstrate workflow execution."""
    # Create and configure the workflow
    workflow = create_default_workflow()
    
    # Example initial data
    initial_data = {
        "input_file": "emails.json",
        "output_dir": "results",
        "config": {
            "max_retries": 3,
            "timeout": 60
        }
    }
    
    # Execute the workflow
    result = workflow.execute_workflow(initial_data)
    
    # Process results
    if result.has_errors():
        logger.error("Workflow completed with errors:")
        for error in result.errors:
            logger.error(f"{error['source']}: {error['message']}")
    else:
        logger.info("Workflow completed successfully")
        logger.info(f"Results: {result.data}")


if __name__ == "__main__":
    main()
