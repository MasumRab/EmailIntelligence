from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class ConflictType(str, Enum):
    CONTENT = "content"
    BINARY = "binary"
    MODIFY_DELETE = "modify/delete"

class HunkModel(BaseModel):
    """Represents a diff hunk."""
    header: str
    lines: List[str]

class ConflictModel(BaseModel):
    """Represents a file conflict."""
    path: str
    type: ConflictType
    oid_base: Optional[str]
    oid_ours: Optional[str]
    oid_theirs: Optional[str]
    hunks: List[HunkModel] = []
