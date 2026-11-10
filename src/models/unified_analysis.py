from datetime import datetime
from typing import List, Dict, Any, Optional

class ActionNarrative:
    """
    A synthesized description of a single commit's intent and actions.
    This is the building block for reports.
    """
    def __init__(self, commit_hexsha: str, author_name: str, authored_date: int,
                 commit_message: str, synthesized_narrative: str,
                 is_consistent: bool, discrepancy_notes: str):
        self.commit_hexsha = commit_hexsha
        self.author_name = author_name
        self.authored_date = authored_date
        self.commit_message = commit_message
        self.synthesized_narrative = synthesized_narrative
        self.is_consistent = is_consistent
        self.discrepancy_notes = discrepancy_notes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "commit_hexsha": self.commit_hexsha,
            "author_name": self.author_name,
            "authored_date": self.authored_date,
            "commit_message": self.commit_message,
            "synthesized_narrative": self.synthesized_narrative,
            "is_consistent": self.is_consistent,
            "discrepancy_notes": self.discrepancy_notes,
        }

class IntentReport:
    """
    A collection of ActionNarrative objects for all commits in a branch,
    representing the total intended change before a merge or rebase.
    """
    def __init__(self, branch_name: str, generated_at: datetime,
                 commit_narratives: List[ActionNarrative]):
        self.branch_name = branch_name
        self.generated_at = generated_at
        self.commit_narratives = commit_narratives

    def to_dict(self) -> Dict[str, Any]:
        return {
            "branch_name": self.branch_name,
            "generated_at": self.generated_at.isoformat(),
            "commit_narratives": [narrative.to_dict() for narrative in self.commit_narratives],
        }

class VerificationResult:
    """
    The output of the verification process, indicating consistency or listing discrepancies
    between an IntentReport and the final merged state.
    """
    def __init__(self, branch_name: str, verified_at: datetime,
                 is_fully_consistent: bool, missing_changes: List[Dict[str, Any]],
                 unexpected_changes: List[Dict[str, Any]]):
        self.branch_name = branch_name
        self.verified_at = verified_at
        self.is_fully_consistent = is_fully_consistent
        self.missing_changes = missing_changes
        self.unexpected_changes = unexpected_changes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "branch_name": self.branch_name,
            "verified_at": self.verified_at.isoformat(),
            "is_fully_consistent": self.is_fully_consistent,
            "missing_changes": self.missing_changes,
            "unexpected_changes": self.unexpected_changes,
        }
