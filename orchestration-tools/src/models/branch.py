from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class BranchType(str):
    FEATURE = "feature"
    SCIENTIFIC = "scientific"
    MAIN = "main"
    RELEASE = "release"


class Branch(BaseModel):
    """
    Represents Git branches being validated
    """
    name: str  # Name of the branch
    type: BranchType  # Type of branch (feature, scientific, main, release)
    created_at: datetime = datetime.now()  # Time when branch was created
    last_updated: datetime = datetime.now()  # Time of last update
    linked_pull_requests: List[str] = []  # Associated pull requests
    verification_history: List[str] = []  # History of verification results for this branch