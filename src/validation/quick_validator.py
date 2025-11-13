"""
Quick Validator for Basic Conflict Resolution

Provides basic validation for conflict resolution processes
with minimal overhead and quick feedback.

Features:
- Basic conflict resolution validation
- Quick assessment of resolution quality
- Minimal validation overhead
- Fast feedback for iterative development
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import structlog

from ..resolution.types import (
    ResolutionStrategy,
)

logger = structlog.get_logger()


class ValidationLevel(Enum):
    """Validation levels"""

    QUICK = "quick"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"


class ValidationStatus(Enum):
    """Validation status levels"""

    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"
    ERROR = "error"


@dataclass
class QuickValidationResult:
    """Result of quick validation"""

    status: ValidationStatus
    overall_score: float
    validation_time: float
    basic_checks: Dict[str, Any]
    quick_issues: List[str]
    recommendations: List[str]
    resolution_readiness: str  # ready, needs_minor_fixes, needs_major_review


@dataclass
class BasicCheck:
    """Basic validation check"""

    name: str
    description: str
    weight: float
    threshold: float


class QuickValidator:
    """
    Quick validation for basic conflict resolution

    Provides fast validation with minimal computational overhead
    suitable for iterative development and quick feedback cycles.
    """

    def __init__(self):
        """Initialize quick validator"""
        self.validation_stats = {
            "total_validations": 0,
            "pass_rate": 0.0,
            "average_validation_time": 0.0,
            "common_issues": {},
        }

        # Define basic checks with minimal computational cost
        self.basic_checks = [
            BasicCheck(
                name="conflict_identification",
                description="Conflict properly identified and classified",
                weight=0.3,
                threshold=0.8,
            ),
            BasicCheck(
                name="basic_resolution_plan",
                description="Resolution plan exists and is structured",
                weight=0.25,
                threshold=0.7,
            ),
            BasicCheck(
                name="essential_validation",
                description="Essential validation steps included",
                weight=0.25,
                threshold=0.6,
            ),
            BasicCheck(
                name="rollback_feasibility", description="Rollback strategy is defined", weight=0.2, threshold=0.5
            ),
        ]

        logger.info("Quick validator initialized")

    async def validate_basic_resolution(
        self, conflict_data, resolution_strategy: Optional[ResolutionStrategy] = None, **kwargs
    ) -> QuickValidationResult:
        """
        Perform quick validation on basic conflict resolution

        Args:
            conflict_data: Conflict information to validate
            resolution_strategy: Optional resolution strategy
            **kwargs: Additional validation context

        Returns:
            QuickValidationResult with validation results
        """
        import time

        start_time = time.time()
        self.validation_stats["total_validations"] += 1

        try:
            logger.debug("Starting quick validation", conflict_type=type(conflict_data).__name__)

            # Perform basic checks
            check_results = await self._perform_basic_checks(conflict_data, resolution_strategy, **kwargs)

            # Calculate overall score
            overall_score = self._calculate_quick_score(check_results)

            # Identify quick issues
            quick_issues = self._identify_quick_issues(check_results)

            # Generate recommendations
            recommendations = self._generate_quick_recommendations(check_results, quick_issues)

            # Determine resolution readiness
            resolution_readiness = self._assess_resolution_readiness(overall_score, quick_issues)

            # Calculate validation time
            validation_time = time.time() - start_time

            # Update statistics
            self._update_validation_stats(ValidationStatus.PASS if overall_score >= 0.7 else ValidationStatus.WARNING)

            result = QuickValidationResult(
                status=ValidationStatus.PASS if overall_score >= 0.7 else ValidationStatus.WARNING,
                overall_score=overall_score,
                validation_time=validation_time,
                basic_checks=check_results,
                quick_issues=quick_issues,
                recommendations=recommendations,
                resolution_readiness=resolution_readiness,
            )

            logger.info(
                "Quick validation completed",
                score=overall_score,
                status=result.status.value,
                readiness=resolution_readiness,
                validation_time=validation_time,
            )

            return result

        except Exception as e:
            logger.error("Quick validation failed", error=str(e))

            # Return error result
            return QuickValidationResult(
                status=ValidationStatus.ERROR,
                overall_score=0.0,
                validation_time=time.time() - start_time,
                basic_checks={},
                quick_issues=[f"Validation failed: {str(e)}"],
                recommendations=["Fix validation errors and retry"],
                resolution_readiness="needs_major_review",
            )

    async def _perform_basic_checks(
        self, conflict_data, resolution_strategy: Optional[ResolutionStrategy], **kwargs
    ) -> Dict[str, Any]:
        """Perform basic validation checks"""

        check_results = {}

        # Check 1: Conflict Identification
        check_results["conflict_identification"] = await self._check_conflict_identification(conflict_data)

        # Check 2: Basic Resolution Plan
        check_results["basic_resolution_plan"] = await self._check_resolution_plan(conflict_data, resolution_strategy)

        # Check 3: Essential Validation
        check_results["essential_validation"] = await self._check_essential_validation(
            conflict_data, resolution_strategy
        )

        # Check 4: Rollback Feasibility
        check_results["rollback_feasibility"] = await self._check_rollback_feasibility(resolution_strategy)

        return check_results

    async def _check_conflict_identification(self, conflict_data) -> Dict[str, Any]:
        """Check if conflict is properly identified"""

        score = 0.0
        details = {}

        # Check if conflict data has basic required fields
        required_fields = ["conflict_type", "file_paths", "branches"]

        for field in required_fields:
            if hasattr(conflict_data, field):
                field_value = getattr(conflict_data, field)
                if field_value:
                    score += 0.25
                details[field] = {"present": bool(field_value), "value": field_value}

        # Check conflict type classification
        if hasattr(conflict_data, "conflict_type"):
            conflict_type = getattr(conflict_data, "conflict_type")
            if conflict_type in ["content", "structural", "architectural", "dependency", "semantic"]:
                score += 0.15
                details["conflict_type_classified"] = True
                details["conflict_type"] = conflict_type
            else:
                details["conflict_type_classified"] = False
                details["conflict_type"] = conflict_type

        return {"score": min(1.0, score), "passed": score >= 0.8, "details": details}

    async def _check_resolution_plan(
        self, conflict_data, resolution_strategy: Optional[ResolutionStrategy]
    ) -> Dict[str, Any]:
        """Check basic resolution plan existence and structure"""

        score = 0.0
        details = {}

        # Check if resolution strategy exists
        if resolution_strategy:
            score += 0.4
            details["strategy_exists"] = True

            # Check strategy basic structure
            if resolution_strategy.steps and len(resolution_strategy.steps) > 0:
                score += 0.3
                details["has_steps"] = True
                details["step_count"] = len(resolution_strategy.steps)
            else:
                details["has_steps"] = False

            # Check strategy description
            if resolution_strategy.description:
                score += 0.2
                details["has_description"] = True
            else:
                details["has_description"] = False

            # Check confidence score
            if hasattr(resolution_strategy, "confidence") and resolution_strategy.confidence > 0:
                score += 0.1
                details["confidence"] = resolution_strategy.confidence
        else:
            details["strategy_exists"] = False

        # Check if conflict has estimated resolution time
        if hasattr(conflict_data, "estimated_resolution_time"):
            score += 0.1
            details["has_time_estimate"] = True
            details["estimated_time"] = getattr(conflict_data, "estimated_resolution_time")
        else:
            details["has_time_estimate"] = False

        return {"score": min(1.0, score), "passed": score >= 0.7, "details": details}

    async def _check_essential_validation(
        self, conflict_data, resolution_strategy: Optional[ResolutionStrategy]
    ) -> Dict[str, Any]:
        """Check for essential validation steps"""

        score = 0.0
        details = {}

        # Check for basic validation steps in strategy
        if resolution_strategy and resolution_strategy.steps:
            validation_steps = 0

            for step in resolution_strategy.steps:
                if step.validation_steps:
                    validation_steps += len(step.validation_steps)

            if validation_steps > 0:
                score += 0.4
                details["validation_steps"] = validation_steps

            # Check for testing validation
            testing_steps = sum(
                1
                for step in resolution_strategy.steps
                if step.validation_steps and any("test" in validation.lower() for validation in step.validation_steps)
            )

            if testing_steps > 0:
                score += 0.3
                details["testing_steps"] = testing_steps

            # Check for code review validation
            review_steps = sum(
                1
                for step in resolution_strategy.steps
                if step.validation_steps and any("review" in validation.lower() for validation in step.validation_steps)
            )

            if review_steps > 0:
                score += 0.2
                details["review_steps"] = review_steps

        # Check if conflict has complexity score (indicating analysis)
        if hasattr(conflict_data, "complexity_score"):
            score += 0.1
            details["has_complexity_analysis"] = True
            details["complexity_score"] = getattr(conflict_data, "complexity_score")
        else:
            details["has_complexity_analysis"] = False

        return {"score": min(1.0, score), "passed": score >= 0.6, "details": details}

    async def _check_rollback_feasibility(self, resolution_strategy: Optional[ResolutionStrategy]) -> Dict[str, Any]:
        """Check rollback strategy feasibility"""

        score = 0.0
        details = {}

        if resolution_strategy:
            # Check if rollback strategy is defined
            if resolution_strategy.rollback_strategy:
                score += 0.5
                details["rollback_defined"] = True
                details["rollback_strategy"] = resolution_strategy.rollback_strategy
            else:
                details["rollback_defined"] = False

            # Check if steps can rollback
            rollbackable_steps = sum(
                1 for step in resolution_strategy.steps if hasattr(step, "can_rollback") and step.can_rollback
            )

            if rollbackable_steps > 0:
                score += 0.3
                details["rollbackable_steps"] = rollbackable_steps

            # Check if strategy has approval requirements (indicating caution)
            if hasattr(resolution_strategy, "requires_approval") and resolution_strategy.requires_approval:
                score += 0.2
                details["requires_approval"] = True
            else:
                details["requires_approval"] = False
        else:
            details["rollback_defined"] = False
            details["rollbackable_steps"] = 0

        return {"score": min(1.0, score), "passed": score >= 0.5, "details": details}

    def _calculate_quick_score(self, check_results: Dict[str, Any]) -> float:
        """Calculate overall quick validation score"""

        total_weighted_score = 0.0
        total_weight = 0.0

        for check in self.basic_checks:
            if check.name in check_results:
                result = check_results[check.name]
                weighted_score = result["score"] * check.weight
                total_weighted_score += weighted_score
                total_weight += check.weight

        if total_weight > 0:
            return total_weighted_score / total_weight
        else:
            return 0.0

    def _identify_quick_issues(self, check_results: Dict[str, Any]) -> List[str]:
        """Identify quick validation issues"""

        issues = []

        for check_name, result in check_results.items():
            if not result["passed"]:
                check_obj = next((c for c in self.basic_checks if c.name == check_name), None)
                if check_obj:
                    issues.append(f"{check_obj.description} - Score: {result['score']:.2f}")

        return issues

    def _generate_quick_recommendations(self, check_results: Dict[str, Any], issues: List[str]) -> List[str]:
        """Generate quick recommendations for improvement"""

        recommendations = []

        # Based on failing checks, provide specific recommendations
        if not check_results.get("conflict_identification", {}).get("passed", False):
            recommendations.append("Ensure conflict data includes proper classification and affected files")

        if not check_results.get("basic_resolution_plan", {}).get("passed", False):
            recommendations.append("Create a structured resolution strategy with clear steps")

        if not check_results.get("essential_validation", {}).get("passed", False):
            recommendations.append("Include essential validation steps like testing and code review")

        if not check_results.get("rollback_feasibility", {}).get("passed", False):
            recommendations.append("Define rollback strategy for safe resolution execution")

        # General recommendations
        if len(issues) > 2:
            recommendations.append("Consider more detailed resolution planning")

        return recommendations

    def _assess_resolution_readiness(self, overall_score: float, issues: List[str]) -> str:
        """Assess resolution readiness"""

        if overall_score >= 0.8 and len(issues) <= 1:
            return "ready"
        elif overall_score >= 0.6 and len(issues) <= 3:
            return "needs_minor_fixes"
        else:
            return "needs_major_review"

    def _update_validation_stats(self, status: ValidationStatus):
        """Update validation statistics"""

        # Update pass rate (simplified)
        current_pass_rate = self.validation_stats["pass_rate"]
        total_validations = self.validation_stats["total_validations"]

        if status in [ValidationStatus.PASS, ValidationStatus.WARNING]:
            # Assuming warning also counts as acceptable for quick validation
            new_pass_rate = (current_pass_rate * (total_validations - 1) + 1) / total_validations
        else:
            new_pass_rate = (current_pass_rate * (total_validations - 1)) / total_validations

        self.validation_stats["pass_rate"] = new_pass_rate

    def get_validation_statistics(self) -> Dict[str, Any]:
        """Get quick validation statistics"""

        return {
            **self.validation_stats,
            "validation_level": ValidationLevel.QUICK.value,
            "check_count": len(self.basic_checks),
        }

    async def validate_batch_resolutions(
        self, conflicts: List[Any], strategies: List[Optional[ResolutionStrategy]] = None
    ) -> List[QuickValidationResult]:
        """Validate multiple resolutions in batch for efficiency"""

        if strategies is None:
            strategies = [None] * len(conflicts)

        results = []

        for i, (conflict, strategy) in enumerate(zip(conflicts, strategies)):
            try:
                result = await self.validate_basic_resolution(conflict, strategy)
                results.append(result)
            except Exception as e:
                logger.error("Batch validation failed for item", item_index=i, error=str(e))

                # Add error result
                results.append(
                    QuickValidationResult(
                        status=ValidationStatus.ERROR,
                        overall_score=0.0,
                        validation_time=0.0,
                        basic_checks={},
                        quick_issues=[f"Validation error: {str(e)}"],
                        recommendations=["Fix validation error"],
                        resolution_readiness="needs_major_review",
                    )
                )

        return results

    def get_performance_metrics(self) -> Dict[str, float]:
        """Get quick validation performance metrics"""

        total_validations = self.validation_stats["total_validations"]

        if total_validations > 0:
            avg_time = self.validation_stats["average_validation_time"]
            return {
                "average_validation_time": avg_time,
                "validations_per_second": 1.0 / avg_time if avg_time > 0 else 0.0,
                "throughput_rate": total_validations,
            }
        else:
            return {"average_validation_time": 0.0, "validations_per_second": 0.0, "throughput_rate": 0}
