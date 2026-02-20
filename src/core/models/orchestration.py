from enum import Enum
from typing import Dict, Any, Optional, List
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class WorkflowType(str, Enum):
    REBASE = "rebase"
    ANALYZE = "analyze"
    SYNC = "sync"

class SessionStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class Session(BaseModel):
    """Tracks state of a long-running workflow."""
    id: UUID = Field(default_factory=uuid4)
    workflow: WorkflowType
    status: SessionStatus
    step_index: int = 0
    context: Dict[str, Any] = {}
    updated_at: datetime = Field(default_factory=datetime.now)

class SyncReport(BaseModel):
    diverged_files: List[str]
    up_to_date: bool
