"""
Constitutional Analyzer module.
Orchestrates the checking of code against constitutional rules.
"""

from pathlib import Path
from typing import List, Dict, Any

from src.core.interfaces import IConstitutionalAnalyzer
from src.core.conflict_models import Conflict, AnalysisResult, RiskLevel
from src.utils.logger import get_logger
from .data import RequirementViolation
from .requirement_checker import (
    ErrorHandlingChecker,
    TypeHintChecker,
    DocstringChecker,
    SecurityChecker,
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

    async def analyze(self, conflict: Conflict) -> AnalysisResult:
        """
        Analyze a conflict for constitutional compliance.

        Args:
            conflict: The conflict to analyze

        Returns:
            Analysis result with compliance information
        """
        # Extract code from conflict blocks
        code = ""
        for block in conflict.blocks:
            code += block.incoming_content + "\n"
            code += block.current_content + "\n"

        context = {
            "file_paths": conflict.file_paths,
            "severity": conflict.severity.value if hasattr(conflict, 'severity') else None,
            "conflict_type": conflict.type.value if hasattr(conflict, 'type') else None,
        }

        # Run constitutional compliance analysis
        compliance_result = await self.analyze_constitutional_compliance(code, context)

        # Map compliance result to AnalysisResult
        # Use constitutional_violations from the compliance result
        constitutional_violations = compliance_result.constitutional_violations
        violation_count = len(constitutional_violations)
        
        # Calculate complexity based on violations found
        complexity_score = min(100.0, 30.0 + (violation_count * 10))

        # Determine risk level based on severity
        risk_level = conflict.severity
        if violation_count > 5:
            risk_level = RiskLevel.HIGH
        elif violation_count > 2:
            risk_level = RiskLevel.MEDIUM

        # Determine if auto-resolvable based on violations
        is_auto_resolvable = violation_count < 3

        # Estimate resolution time
        estimated_resolution_time = 10 + (violation_count * 5)

        # Determine recommended strategy
        if violation_count == 0:
            recommended_strategy = "accept_incoming"
        elif violation_count < 3:
            recommended_strategy = "auto_fix"
        else:
            recommended_strategy = "manual_review"

        return AnalysisResult(
            conflict_id=conflict.id,
            complexity_score=complexity_score,
            risk_level=risk_level,
            estimated_resolution_time_minutes=estimated_resolution_time,
            is_auto_resolvable=is_auto_resolvable,
            recommended_strategy_type=recommended_strategy,
            root_cause="Constitutional compliance violations" if violation_count > 0 else "No issues found",
            constitutional_violations=constitutional_violations,
            confidence_score=0.85,
        )

    async def analyze_constitutional_compliance(
        self, code: str, context: Dict[str, Any]
    ) -> AnalysisResult:
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

        compliance_score = (
            1.0 - (failed_checks / total_checks) if total_checks > 0 else 1.0
        )
        # Ensure score is between 0 and 1
        compliance_score = max(0.0, min(1.0, compliance_score))

        # Map to required AnalysisResult fields
        complexity_score = compliance_score * 100
        violation_count = len(violations)
        
        # Determine risk level based on violations
        if violation_count > 5:
            risk_level = RiskLevel.HIGH
        elif violation_count > 2:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        # Determine auto-resolvable
        is_auto_resolvable = violation_count < 3
        
        # Determine recommended strategy
        if violation_count == 0:
            recommended_strategy = "accept_incoming"
        elif violation_count < 3:
            recommended_strategy = "auto_fix"
        else:
            recommended_strategy = "manual_review"
        
        # Estimate resolution time
        estimated_time = 10 + (violation_count * 5)

        analysis_result = AnalysisResult(
            conflict_id=context.get("file_paths", ["unknown"])[0] if context.get("file_paths") else "unknown",
            complexity_score=complexity_score,
            risk_level=risk_level,
            estimated_resolution_time_minutes=estimated_time,
            is_auto_resolvable=is_auto_resolvable,
            recommended_strategy_type=recommended_strategy,
            root_cause="Constitutional compliance check",
            constitutional_violations=[v.description for v in violations],
            confidence_score=compliance_score,
        )

        logger.info(
            f"Constitutional analysis completed with score: {compliance_score:.2f}"
        )
        return analysis_result


class RequirementViolation:
    """
    Represents a violation of a constitutional requirement.
    """

    def __init__(
        self, rule_id: str, description: str, severity: RiskLevel, location: str = None
    ):
        self.rule_id = rule_id
        self.description = description
        self.severity = severity
        self.location = location

    def __str__(self):
        return f"[{self.severity.value}] {self.rule_id}: {self.description}"
