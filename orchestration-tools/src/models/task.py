from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Task(BaseModel):
    """
    Represents a task in the orchestration system
    """
    id: str  # Unique identifier for the task
    name: str  # Name of the task
    description: str  # Description of the task
    goal_ids: List[str] = []  # List of goal IDs this task is related to
    status: str = "PENDING"  # Status of the task (PENDING, IN_PROGRESS, COMPLETED)
    created_at: datetime = datetime.now()  # Time when task was created
    updated_at: datetime = datetime.now()  # Time when task was last updated
    assigned_to: Optional[str] = None  # User assigned to this task