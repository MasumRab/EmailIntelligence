from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class LogicEngine(ABC):
    """Base class for all core logic engines (Git, Analysis, etc)."""
    
    @abstractmethod
    def validate(self, context: Dict[str, Any]) -> bool:
        """Verify inputs before execution."""
        pass

class Action(BaseModel):
    """Represents a single atomic operation."""
    id: str
    description: str
    command: str
    rollback_command: Optional[str] = None
    
class ExecutionContext(BaseModel):
    """Runtime context for logic engines."""
    dry_run: bool = False
    repo_root: str
