from typing import List
from src.core.git.plumbing import GitPlumbing
from src.core.models.git import ConflictModel

class ConflictDetector:
    """Orchestrates in-memory conflict detection."""
    
    def __init__(self, plumbing: GitPlumbing):
        self.plumbing = plumbing

    def detect(self, base: str, head: str) -> List[ConflictModel]:
        raw_output = self.plumbing.merge_tree(base, head)
        return self.plumbing.parse_merge_tree(raw_output)
