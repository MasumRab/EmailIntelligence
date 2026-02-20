from typing import List, Optional
from pydantic import BaseModel
from src.core.base import Action

class ExecutionPlan(BaseModel):
    """Ordered list of actions to execute."""
    actions: List[Action]
    rollback_on_failure: bool = True
