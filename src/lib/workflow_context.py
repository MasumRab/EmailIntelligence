"""
Workflow Context Manager for Guided CLI Workflows.

Manages the state and transitions of interactive developer guides.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class WorkflowState:
    """Represents the current state of a workflow session."""
    guide_name: str
    current_step: str = "start"
    context: Dict[str, Any] = field(default_factory=dict)
    is_completed: bool = False

class WorkflowContextManager:
    """
    Manages the lifecycle and state transitions of guided workflows.
    """
    def __init__(self, guide_name: str):
        self.state = WorkflowState(guide_name=guide_name)

    def get_current_step(self) -> str:
        """Return the ID of the current step."""
        return self.state.current_step

    def update_context(self, data: Dict[str, Any]):
        """Merge new data into the workflow context."""
        self.state.context.update(data)

    def transition_to(self, step_id: str):
        """Move the workflow to a new step."""
        self.state.current_step = step_id

    def complete(self):
        """Mark the workflow as completed."""
        self.state.is_completed = True

    def get_context_value(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from the workflow context."""
        return self.state.context.get(key, default)