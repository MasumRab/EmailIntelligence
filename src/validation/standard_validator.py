"""
Standard Validator for Constitutional Compliance and Feature Preservation

Provides standard validation including constitutional compliance checking
and feature preservation analysis for resolution quality assurance.

Features:
- Constitutional compliance validation
- Feature preservation analysis
- Standard quality gates
- Structured validation reporting
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import structlog

from ..resolution.constitutional_engine import ConstitutionalEngine
from ..resolution.types import ResolutionStrategy, ResolutionStep
from .quick_validator import QuickValidator, ValidationLevel, ValidationStatus

logger = structlog.get_logger()


@dataclass
class StandardValidationResult:
    """Result of standard validation"""

    status: ValidationStatus
    overall_score: float
    validation_time: float
    constitutional_score: float
    feature_preservation_score: float
    compliance_issues: List[Dict[str, Any]]
    preservation_issues: List[Dict[str, Any]]
    quality_gates: Dict[str, Any]
    recommendations: List[str]
    readiness_assessment: str


class StandardValidator:
    """
    Standard validation with constitutional compliance and feature preservation

    Provides balanced validation suitable for most resolution scenarios
    with moderate computational overhead and comprehensive quality assessment.
    """

    def __init__(self):
        """Initialize standard validator"""
        self.quick_validator = QuickValidator()
        self.constitutional_engine = ConstitutionalEngine()

        self.validation_stats = {
            "total_validations": 0,
            "compliance_pass_rate": 0.0,
            "preservation_pass_rate": 0.0,
            "average_constitutional_score": 0.0,
            "average_preservation_score": 0.0,
        }

        # Quality gates for standard validation
        self.quality_gates = {
            "constitutional_compliance": {
                "threshold": 0.7,
                "description": "Constitutional compliance minimum threshold",
            },
            "feature_preservation": {"threshold": 0.8, "description": "Feature preservation minimum threshold"},
            "overall_quality": {"threshold": 0.75, "description": "Overall quality minimum threshold"},
        }

        logger.info("Standard validator initialized")

    async def validate_standard_resolution(
        self,
        conflict_data,
        resolution_strategy: ResolutionStrategy,
        specification_data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> StandardValidationResult:
        """
        Perform standard validation including constitutional compliance

        Args:
            conflict_data: Conflict information to validate
            resolution_strategy: Resolution strategy to validate
            specification_data: Optional specification data for enhanced validation
            **kwargs: Additional validation context

        Returns:
            StandardValidationResult with validation results
        """
        import time

        start_time = time.time()
        self.validation_stats["total_validations"] += 1

        try:
            logger.debug("Starting standard validation", conflict_type=type(conflict_data).__name__)

            # Step 1: Basic validation (inherit from QuickValidator)
            basic_result = await self.quick_validator.validate_basic_resolution(
                conflict_data, resolution_strategy, **kwargs
            )

            # Step 2: Constitutional compliance validation
            constitutional_result = await self._validate_constitutional_compliance(
                resolution_strategy, specification_data
            )

            # Step 3: Feature preservation analysis
            preservation_result = await self._analyze_feature_preservation(
                conflict_data, resolution_strategy, specification_data
            )

            # Step 4: Calculate comprehensive scores
            constitutional_score = constitutional_result.get("score", 0.0)
            preservation_score = preservation_result.get("score", 0.0)
            overall_score = (constitutional_score + preservation_score + basic_result.overall_score) / 3

            # Step 5: Quality gate assessment
            quality_gates = self._assess_quality_gates(constitutional_score, preservation_score, overall_score)

            # Step 6: Identify issues and generate recommendations
            compliance_issues = constitutional_result.get("issues", [])
            preservation_issues = preservation_result.get("issues", [])
            all_recommendations = self._generate_standard_recommendations(
                constitutional_result, preservation_result, quality_gates
            )

            # Step 7: Assess readiness
            readiness_assessment = self._assess_standard_readiness(
                constitutional_score, preservation_score, quality_gates
            )

            # Calculate validation time
            validation_time = time.time() - start_time

            # Update statistics
            self._update_standard_stats(constitutional_score, preservation_score)

            result = StandardValidationResult(
                status=ValidationStatus.PASS if overall_score >= 0.75 else ValidationStatus.WARNING,
                overall_score=overall_score,
                validation_time=validation_time,
                constitutional_score=constitutional_score,
                feature_preservation_score=preservation_score,
                compliance_issues=compliance_issues,
                preservation_issues=preservation_issues,
                quality_gates=quality_gates,
                recommendations=all_recommendations,
                readiness_assessment=readiness_assessment,
            )

            logger.info(
                "Standard validation completed",
                constitutional_score=constitutional_score,
                preservation_score=preservation_score,
                overall_score=overall_score,
                readiness=readiness_assessment,
                validation_time=validation_time,
            )

            return result

        except Exception as e:
            logger.error("Standard validation failed", error=str(e))

            return StandardValidationResult(
                status=ValidationStatus.ERROR,
                overall_score=0.0,
                validation_time=time.time() - start_time,
                constitutional_score=0.0,
                feature_preservation_score=0.0,
                compliance_issues=[{"type": "validation_error", "message": str(e)}],
                preservation_issues=[],
                quality_gates={},
                recommendations=["Fix validation errors and retry"],
                readiness_assessment="needs_major_review",
            )

    async def _validate_constitutional_compliance(
        self, resolution_strategy: ResolutionStrategy, specification_data: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Validate constitutional compliance"""

        issues = []
        score_components = []

        try:
            # Step 1: Check strategy against constitutional rules
            if hasattr(resolution_strategy, "constitutional_compliant"):
                if resolution_strategy.constitutional_compliant:
                    score_components.append(0.9)
                else:
                    score_components.append(0.3)
                    issues.append(
                        {
                            "type": "constitutional_non_compliance",
                            "severity": "critical",
                            "description": "Resolution strategy marked as non-constitutional",
                        }
                    )
            else:
                score_components.append(0.7)  # Neutral score for missing information

            # Step 2: Validate strategy steps against constitutional requirements
            if resolution_strategy.steps:
                step_compliance_score = self._validate_steps_compliance(resolution_strategy.steps)
                score_components.append(step_compliance_score)

                if step_compliance_score < 0.7:
                    issues.append(
                        {
                            "type": "step_compliance_issues",
                            "severity": "major",
                            "description": "Some resolution steps may violate constitutional requirements",
                        }
                    )

            # Step 3: Check rollback strategy compliance
            if resolution_strategy.rollback_strategy:
                rollback_compliance = self._validate_rollback_compliance(resolution_strategy.rollback_strategy)
                score_components.append(rollback_compliance)

                if rollback_compliance < 0.6:
                    issues.append(
                        {
                            "type": "rollback_compliance_issues",
                            "severity": "major",
                            "description": "Rollback strategy may not meet constitutional standards",
                        }
                    )

            # Step 4: Validate against specification if available
            if specification_data:
                spec_compliance = await self._validate_specification_compliance(resolution_strategy, specification_data)
                score_components.append(spec_compliance)

            # Calculate overall constitutional score
            constitutional_score = sum(score_components) / len(score_components) if score_components else 0.5

            return {
                "score": constitutional_score,
                "issues": issues,
                "components": {
                    "strategy_compliance": score_components[0] if score_components else 0.5,
                    "step_compliance": score_components[1] if len(score_components) > 1 else 0.5,
                    "rollback_compliance": score_components[2] if len(score_components) > 2 else 0.5,
                    "specification_compliance": score_components[3] if len(score_components) > 3 else 0.5,
                },
            }

        except Exception as e:
            logger.error("Constitutional compliance validation failed", error=str(e))
            return {
                "score": 0.0,
                "issues": [{"type": "validation_error", "message": f"Constitutional validation failed: {str(e)}"}],
            }

    def _validate_steps_compliance(self, steps: List[ResolutionStep]) -> float:
        """Validate resolution steps against constitutional requirements"""

        if not steps:
            return 0.5  # Neutral score for no steps

        compliance_scores = []

        for step in steps:
            step_score = 0.5  # Base score

            # Check if step has validation steps (constitutional requirement)
            if step.validation_steps and len(step.validation_steps) > 0:
                step_score += 0.2

            # Check if step has reasonable time estimate
            if hasattr(step, "estimated_time") and step.estimated_time > 0:
                step_score += 0.1

            # Check if step can rollback (constitutional safety requirement)
            if hasattr(step, "can_rollback") and step.can_rollback:
                step_score += 0.2

            compliance_scores.append(min(1.0, step_score))

        return sum(compliance_scores) / len(compliance_scores)

    def _validate_rollback_compliance(self, rollback_strategy: str) -> float:
        """Validate rollback strategy compliance"""

        if not rollback_strategy:
            return 0.3  # Low score for no rollback strategy

        compliance_score = 0.5  # Base score

        # Check for specific rollback mechanisms
        rollback_keywords = {
            "git": 0.2,  # Git-based rollback
            "checkpoint": 0.15,  # Checkpoint-based rollback
            "branch": 0.1,  # Branch-based rollback
            "revert": 0.15,  # Revert-based rollback
            "backup": 0.1,  # Backup-based rollback
        }

        rollback_strategy_lower = rollback_strategy.lower()
        for keyword, bonus in rollback_keywords.items():
            if keyword in rollback_strategy_lower:
                compliance_score += bonus

        return min(1.0, compliance_score)

    async def _validate_specification_compliance(
        self, resolution_strategy: ResolutionStrategy, specification_data: Dict[str, Any]
    ) -> float:
        """Validate strategy against specification requirements"""

        try:
            compliance_score = 0.5  # Base score

            # Check specification completeness
            if "template_content" in specification_data:
                compliance_score += 0.1

            # Check constitutional validation results
            if "constitutional_validation" in specification_data:
                compliance_score += 0.2

                const_validation = specification_data["constitutional_validation"]
                if isinstance(const_validation, dict):
                    compliance_score += const_validation.get("overall_score", 0.0) * 0.1

            # Check quality recommendations compliance
            if "quality_recommendations" in specification_data:
                compliance_score += 0.1

            return min(1.0, compliance_score)

        except Exception as e:
            logger.error("Specification compliance validation failed", error=str(e))
            return 0.3

    async def _analyze_feature_preservation(
        self, conflict_data, resolution_strategy: ResolutionStrategy, specification_data: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze feature preservation in resolution strategy"""

        issues = []
        preservation_indicators = []

        try:
            # Step 1: Check for feature preservation in strategy
            if hasattr(resolution_strategy, "enhancement_preservation"):
                enhancement_preservation = resolution_strategy.enhancement_preservation
                if enhancement_preservation and len(enhancement_preservation) > 0:
                    preservation_indicators.append(0.8)

                    # Analyze preservation quality
                    for preservation in enhancement_preservation:
                        if hasattr(preservation, "preservation_score"):
                            preservation_indicators.append(preservation.preservation_score)
                        else:
                            preservation_indicators.append(0.6)  # Default for missing score
                else:
                    preservation_indicators.append(0.3)  # Low score for no enhancement preservation
            else:
                preservation_indicators.append(0.5)  # Neutral for missing information

            # Step 2: Check for feature preservation in validation steps
            preservation_validation_steps = 0
            for step in resolution_strategy.steps:
                if step.validation_steps:
                    validation_text = " ".join(step.validation_steps).lower()
                    if any(
                        keyword in validation_text
                        for keyword in ["feature", "functionality", "preservation", "enhancement"]
                    ):
                        preservation_validation_steps += 1

            if preservation_validation_steps > 0:
                preservation_indicators.append(
                    min(1.0, preservation_validation_steps / len(resolution_strategy.steps) * 0.7 + 0.3)
                )
            else:
                preservation_indicators.append(0.2)  # Low score for no preservation validation

            # Step 3: Check rollback strategy for feature preservation
            if resolution_strategy.rollback_strategy:
                rollback_lower = resolution_strategy.rollback_strategy.lower()
                if any(keyword in rollback_lower for keyword in ["feature", "enhancement", "functionality"]):
                    preservation_indicators.append(0.7)
                else:
                    preservation_indicators.append(0.4)
            else:
                preservation_indicators.append(0.2)

            # Step 4: Check strategy confidence for feature preservation quality
            if hasattr(resolution_strategy, "confidence"):
                confidence_score = resolution_strategy.confidence
                if confidence_score > 0.8:
                    preservation_indicators.append(0.8)
                elif confidence_score > 0.6:
                    preservation_indicators.append(0.6)
                else:
                    preservation_indicators.append(0.4)

            # Calculate overall preservation score
            preservation_score = sum(preservation_indicators) / len(preservation_indicators)

            # Identify preservation issues
            if preservation_score < 0.7:
                issues.append(
                    {
                        "type": "low_feature_preservation",
                        "severity": "major",
                        "description": "Resolution strategy may not adequately preserve features",
                    }
                )

            if (
                not hasattr(resolution_strategy, "enhancement_preservation")
                or not resolution_strategy.enhancement_preservation
            ):
                issues.append(
                    {
                        "type": "missing_preservation_analysis",
                        "severity": "minor",
                        "description": "No explicit feature preservation analysis found",
                    }
                )

            return {
                "score": preservation_score,
                "issues": issues,
                "indicators": {
                    "enhancement_preservation": preservation_indicators[0] if preservation_indicators else 0.5,
                    "validation_steps": preservation_indicators[1] if len(preservation_indicators) > 1 else 0.5,
                    "rollback_strategy": preservation_indicators[2] if len(preservation_indicators) > 2 else 0.5,
                    "strategy_confidence": preservation_indicators[3] if len(preservation_indicators) > 3 else 0.5,
                },
            }

        except Exception as e:
            logger.error("Feature preservation analysis failed", error=str(e))
            return {
                "score": 0.0,
                "issues": [{"type": "analysis_error", "message": f"Feature preservation analysis failed: {str(e)}"}],
            }

    def _assess_quality_gates(
        self, constitutional_score: float, preservation_score: float, overall_score: float
    ) -> Dict[str, Any]:
        """Assess quality gate compliance"""

        quality_gates = {}

        # Check constitutional compliance gate
        constitutional_gate = {
            "name": "constitutional_compliance",
            "threshold": self.quality_gates["constitutional_compliance"]["threshold"],
            "score": constitutional_score,
            "passed": constitutional_score >= self.quality_gates["constitutional_compliance"]["threshold"],
        }
        quality_gates["constitutional_compliance"] = constitutional_gate

        # Check feature preservation gate
        preservation_gate = {
            "name": "feature_preservation",
            "threshold": self.quality_gates["feature_preservation"]["threshold"],
            "score": preservation_score,
            "passed": preservation_score >= self.quality_gates["feature_preservation"]["threshold"],
        }
        quality_gates["feature_preservation"] = preservation_gate

        # Check overall quality gate
        overall_gate = {
            "name": "overall_quality",
            "threshold": self.quality_gates["overall_quality"]["threshold"],
            "score": overall_score,
            "passed": overall_score >= self.quality_gates["overall_quality"]["threshold"],
        }
        quality_gates["overall_quality"] = overall_gate

        # Calculate overall gate compliance
        gate_compliance = sum(1 for gate in quality_gates.values() if gate["passed"]) / len(quality_gates)
        quality_gates["overall_compliance"] = gate_compliance

        return quality_gates

    def _generate_standard_recommendations(
        self, constitutional_result: Dict[str, Any], preservation_result: Dict[str, Any], quality_gates: Dict[str, Any]
    ) -> List[str]:
        """Generate standard-level recommendations"""

        recommendations = []

        # Constitutional recommendations
        if not quality_gates.get("constitutional_compliance", {}).get("passed", False):
            recommendations.append("Address constitutional compliance issues before proceeding")
            recommendations.append("Review resolution strategy against organizational constitutional rules")

        # Feature preservation recommendations
        if not quality_gates.get("feature_preservation", {}).get("passed", False):
            recommendations.append("Enhance feature preservation strategy")
            recommendations.append("Include specific preservation validation steps")

        # Quality recommendations
        if not quality_gates.get("overall_quality", {}).get("passed", False):
            recommendations.append("Improve overall resolution quality")
            recommendations.append("Consider standard validation improvements")

        # Specific issue recommendations
        for issue in constitutional_result.get("issues", []):
            if issue.get("type") == "constitutional_non_compliance":
                recommendations.append("Review and modify strategy to meet constitutional requirements")
            elif issue.get("type") == "step_compliance_issues":
                recommendations.append("Add validation steps to resolution strategy")

        for issue in preservation_result.get("issues", []):
            if issue.get("type") == "low_feature_preservation":
                recommendations.append("Develop comprehensive feature preservation analysis")
            elif issue.get("type") == "missing_preservation_analysis":
                recommendations.append("Include explicit feature preservation validation")

        return recommendations

    def _assess_standard_readiness(
        self, constitutional_score: float, preservation_score: float, quality_gates: Dict[str, Any]
    ) -> str:
        """Assess readiness for standard validation level"""

        passed_gates = quality_gates.get("overall_compliance", 0.0)

        if constitutional_score >= 0.8 and preservation_score >= 0.8 and passed_gates >= 0.8:
            return "ready_for_implementation"
        elif constitutional_score >= 0.7 and preservation_score >= 0.7 and passed_gates >= 0.6:
            return "needs_minor_improvements"
        elif constitutional_score >= 0.6 and preservation_score >= 0.6:
            return "needs_focused_improvements"
        else:
            return "requires_comprehensive_revision"

    def _update_standard_stats(self, constitutional_score: float, preservation_score: float):
        """Update standard validation statistics"""

        total = self.validation_stats["total_validations"]

        # Update average scores
        current_const_avg = self.validation_stats["average_constitutional_score"]
        current_preserv_avg = self.validation_stats["average_preservation_score"]

        self.validation_stats["average_constitutional_score"] = (
            current_const_avg * (total - 1) + constitutional_score
        ) / total
        self.validation_stats["average_preservation_score"] = (
            current_preserv_avg * (total - 1) + preservation_score
        ) / total

        # Update pass rates
        if constitutional_score >= self.quality_gates["constitutional_compliance"]["threshold"]:
            current_pass_rate = self.validation_stats["compliance_pass_rate"]
            self.validation_stats["compliance_pass_rate"] = (current_pass_rate * (total - 1) + 1) / total
        else:
            current_pass_rate = self.validation_stats["compliance_pass_rate"]
            self.validation_stats["compliance_pass_rate"] = (current_pass_rate * (total - 1)) / total

        if preservation_score >= self.quality_gates["feature_preservation"]["threshold"]:
            current_pass_rate = self.validation_stats["preservation_pass_rate"]
            self.validation_stats["preservation_pass_rate"] = (current_pass_rate * (total - 1) + 1) / total
        else:
            current_pass_rate = self.validation_stats["preservation_pass_rate"]
            self.validation_stats["preservation_pass_rate"] = (current_pass_rate * (total - 1)) / total

    def get_standard_validation_statistics(self) -> Dict[str, Any]:
        """Get standard validation statistics"""

        return {
            **self.validation_stats,
            "validation_level": ValidationLevel.STANDARD.value,
            "quality_gates": self.quality_gates,
        }
