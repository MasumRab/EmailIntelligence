"""
Violation types for constitutional analysis.
"""

from typing import List
from src.core.conflict_models import RiskLevel
from dataclasses import dataclass


@dataclass
class RequirementViolation:
    """Represents a constitutional requirement violation."""
    rule_id: str
    description: str
    severity: RiskLevel
    line_number: int = 0
    file_path: str = ""
    snippet: str = ""
