from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Goal(BaseModel):
    """
    Represents a goal in the orchestration system
    """
    id: str  # Unique identifier for the goal
    name: str  # Name of the goal
    description: str  # Description of the goal
    created_at: datetime = datetime.now()  # Time when goal was created
    updated_at: datetime = datetime.now()  # Time when goal was last updated
    related_tasks: List[str] = []  # List of task IDs related to this goal