"""
Models for constitutional analysis.
"""

from enum import Enum
try:
    from ...core.conflict_models import RiskLevel
except ImportError:
    # Fallback if not available in the expected location
    class RiskLevel(Enum):
        NONE = "none"
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
        CRITICAL = "critical"

class RequirementViolation:
    """
    Represents a violation of a constitutional requirement.
    """
    
    def __init__(self, rule_id: str, description: str, severity: RiskLevel, location: str = None):
        self.rule_id = rule_id
        self.description = description
        self.severity = severity
        self.location = location

    def __str__(self):
        return f"[{self.severity.value}] {self.rule_id}: {self.description}"
