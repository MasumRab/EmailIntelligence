"""
Constitutional Analyzer module.
Orchestrates the checking of code against constitutional rules.
"""

from pathlib import Path
from typing import List, Dict, Any

from ...core.interfaces import IConstitutionalAnalyzer
from ...core.models import Conflict, AnalysisResult, RiskLevel
from ...utils.logger import get_logger
from .requirement_checker import (
    ErrorHandlingChecker,
    TypeHintChecker,
    DocstringChecker,
    SecurityChecker,
    RequirementViolation,
)

logger = get_logger(__name__)


class ConstitutionalAnalyzer(IConstitutionalAnalyzer):
    """
    Analyzes code compliance with constitutional rules.
    """

    def __init__(self, rules_path: Path = None):
        self.rules_path = rules_path or Path("constitutions")
        self.checkers = [
            ErrorHandlingChecker(),
            TypeHintChecker(),
            DocstringChecker(),
            SecurityChecker(),
        ]

    async def analyze(self, conflict: Conflict, context: Dict[str, Any] = None) -> AnalysisResult:
        """
        Analyze a conflict against constitutional rules.
        """
        logger.info("Starting constitutional analysis", conflict_id=conflict.id)

        violations = []

        # Analyze each file in the conflict
        for block in conflict.blocks:
            # Analyze incoming content (the proposed change)
            file_violations = self._analyze_code(block.incoming_content, block.file_path)
            violations.extend(file_violations)

        # Calculate scores and risk
        complexity_score = self._calculate_complexity(conflict)
        risk_level = self._assess_risk(violations, complexity_score)

        return AnalysisResult(
            conflict_id=conflict.id,
            complexity_score=complexity_score,
            risk_level=risk_level,
            estimated_resolution_time_minutes=self._estimate_time(
                complexity_score, len(violations)
            ),
            is_auto_resolvable=len(violations) == 0 and complexity_score < 50,
            recommended_strategy_type="automated" if len(violations) == 0 else "manual",
            root_cause="Constitutional Analysis",
            constitutional_violations=[v.description for v in violations],
            confidence_score=0.9,
        )

    async def validate_code_change(self, code: str, rules: List[str] = None) -> Dict[str, Any]:
        """
        Validate a specific code snippet against rules.
        """
        violations = self._analyze_code(code, "snippet")

        if rules:
            violations = [v for v in violations if v.rule_id in rules]

        return {
            "valid": len(violations) == 0,
            "violations": [v.__dict__ for v in violations],
        }

    def _analyze_code(self, code: str, file_path: str) -> List[RequirementViolation]:
        """Run all checkers on the code."""
        violations = []
        for checker in self.checkers:
            try:
                checker_violations = checker.check(code, file_path)
                violations.extend(checker_violations)
            except Exception as e:
                logger.error("Checker failed", checker=checker.__class__.__name__, error=str(e))
        return violations

    def _calculate_complexity(self, conflict: Conflict) -> float:
        """Calculate complexity score (0-100)."""
        # specialized logic would go here (e.g. cyclomatic complexity)
        # for now, simple heuristic based on lines of code
        total_lines = sum(len(b.incoming_content.splitlines()) for b in conflict.blocks)
        return min(total_lines * 1.5, 100.0)

    def _assess_risk(self, violations: List[RequirementViolation], complexity: float) -> RiskLevel:
        """Assess risk level based on violations and complexity."""
        if any(v.severity == "critical" for v in violations):
            return RiskLevel.CRITICAL
        if complexity > 80 or any(v.severity == "major" for v in violations):
            return RiskLevel.HIGH
        if complexity > 40:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def _estimate_time(self, complexity: float, violation_count: int) -> int:
        """Estimate resolution time in minutes."""
        base_time = 5  # minutes
        return int(base_time + (complexity * 0.5) + (violation_count * 10))
