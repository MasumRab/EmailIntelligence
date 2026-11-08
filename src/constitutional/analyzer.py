"""
Constitutional Analyzer module.
Orchestrates the checking of code against constitutional rules.
"""

from pathlib import Path
from typing import List, Dict, Any

from ..core.interfaces import IConstitutionalAnalyzer
from ..core.conflict_models import Conflict, AnalysisResult, RiskLevel
from ..utils.logger import get_logger
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
    Analyzes code against constitutional rules and requirements.
    """

    def __init__(self, constitution_file: str = None):
        self.constitution_file = constitution_file
        self.checkers = [
            ErrorHandlingChecker(),
            TypeHintChecker(),
            DocstringChecker(),
            SecurityChecker(),
        ]

    async def analyze_constitutional_compliance(self, code: str, context: Dict[str, Any]) -> AnalysisResult:
        """
        Analyze code for constitutional compliance.

        Args:
            code: The code to analyze
            context: Additional context for the analysis

        Returns:
            Analysis result with compliance information
        """
        logger.info(f"Starting constitutional analysis for code of length {len(code)}")
        
        violations = []
        recommendations = []
        details = {}
        
        # Run all checkers
        for checker in self.checkers:
            checker_violations = checker.check(code)
            violations.extend(checker_violations)
            
            # Generate recommendations based on violations
            for violation in checker_violations:
                recommendations.append(f"Fix: {violation.description}")
        
        # Calculate compliance score
        total_checks = len(self.checkers) * 10  # Assuming each checker runs 10 checks
        failed_checks = len(violations)
        
        compliance_score = 1.0 - (failed_checks / total_checks) if total_checks > 0 else 1.0
        # Ensure score is between 0 and 1
        compliance_score = max(0.0, min(1.0, compliance_score))
        
        analysis_result = AnalysisResult(
            compliance_score=compliance_score,
            violations=[v.description for v in violations],
            recommendations=recommendations,
            details=details
        )
        
        logger.info(f"Constitutional analysis completed with score: {compliance_score:.2f}")
        return analysis_result


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