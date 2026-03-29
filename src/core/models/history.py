from typing import List, Optional
from pydantic import BaseModel

class CommitNode(BaseModel):
    """Represents a commit in the DAG."""
    oid: str
    parents: List[str]
    message: str
    author: str
    timestamp: int
    is_merge: bool = False

class HistoryPlan(BaseModel):
    """A topologically sorted list of commits."""
    commits: List[CommitNode]
    base_oid: str
    target_oid: str
