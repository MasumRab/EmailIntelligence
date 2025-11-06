"""
Task Validation Service for Task Master AI

This service provides validation for task creation and updates, ensuring that
tasks meet quality standards including appropriate testing requirements based
on complexity and branch context.
"""

import re
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum


class TaskComplexity(Enum):
    """Task complexity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BranchType(Enum):
    """Branch type classifications."""
    FEATURE = "feature"
    SCIENTIFIC = "scientific"
    MAIN = "main"
    HOTFIX = "hotfix"


class TaskValidationError(Exception):
    """Exception raised when task validation fails."""
    pass


class TestingRequirements(BaseModel):
    """Model for testing requirements based on task characteristics."""

    min_acceptance_criteria: int = Field(..., description="Minimum number of acceptance criteria required")
    requires_test_strategy: bool = Field(..., description="Whether a test strategy is required")
    requires_performance_tests: bool = Field(..., description="Whether performance tests are required")
    requires_integration_tests: bool = Field(..., description="Whether integration tests are required")
    requires_property_tests: bool = Field(..., description="Whether property-based tests are required")
    min_test_coverage: Optional[float] = Field(None, description="Minimum test coverage percentage required")
    requires_mutation_testing: bool = Field(..., description="Whether mutation testing is required")

    @validator('min_test_coverage')
    def validate_coverage(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Test coverage must be between 0 and 100')
        return v


class TaskValidationService:
    """
    Service for validating task creation and updates.

    This service ensures that tasks meet quality standards and include
    appropriate testing requirements based on their complexity and context.
    """

    def __init__(self):
        """Initialize the task validation service."""
        self.testing_requirements = self._load_testing_requirements()

    def _load_testing_requirements(self) -> Dict[str, Dict[str, TestingRequirements]]:
        """
        Load testing requirements matrix based on complexity and branch type.

        Returns:
            Dict mapping complexity + branch combinations to testing requirements
        """
        return {
            # Feature branches
            f"{TaskComplexity.LOW.value}_{BranchType.FEATURE.value}": TestingRequirements(
                min_acceptance_criteria=2,
                requires_test_strategy=False,
                requires_performance_tests=False,
                requires_integration_tests=False,
                requires_property_tests=False,
                min_test_coverage=70.0,
                requires_mutation_testing=False
            ),
            f"{TaskComplexity.MEDIUM.value}_{BranchType.FEATURE.value}": TestingRequirements(
                min_acceptance_criteria=3,
                requires_test_strategy=True,
                requires_performance_tests=False,
                requires_integration_tests=True,
                requires_property_tests=False,
                min_test_coverage=75.0,
                requires_mutation_testing=False
            ),
            f"{TaskComplexity.HIGH.value}_{BranchType.FEATURE.value}": TestingRequirements(
                min_acceptance_criteria=4,
                requires_test_strategy=True,
                requires_performance_tests=True,
                requires_integration_tests=True,
                requires_property_tests=False,
                min_test_coverage=80.0,
                requires_mutation_testing=False
            ),

            # Scientific branches - higher testing standards
            f"{TaskComplexity.LOW.value}_{BranchType.SCIENTIFIC.value}": TestingRequirements(
                min_acceptance_criteria=3,
                requires_test_strategy=True,
                requires_performance_tests=False,
                requires_integration_tests=True,
                requires_property_tests=True,
                min_test_coverage=80.0,
                requires_mutation_testing=False
            ),
            f"{TaskComplexity.MEDIUM.value}_{BranchType.SCIENTIFIC.value}": TestingRequirements(
                min_acceptance_criteria=4,
                requires_test_strategy=True,
                requires_performance_tests=True,
                requires_integration_tests=True,
                requires_property_tests=True,
                min_test_coverage=85.0,
                requires_mutation_testing=True
            ),
            f"{TaskComplexity.HIGH.value}_{BranchType.SCIENTIFIC.value}": TestingRequirements(
                min_acceptance_criteria=5,
                requires_test_strategy=True,
                requires_performance_tests=True,
                requires_integration_tests=True,
                requires_property_tests=True,
                min_test_coverage=90.0,
                requires_mutation_testing=True
            ),

            # Main branch - strictest requirements
            f"{TaskComplexity.LOW.value}_{BranchType.MAIN.value}": TestingRequirements(
                min_acceptance_criteria=3,
                requires_test_strategy=True,
                requires_performance_tests=False,
                requires_integration_tests=True,
                requires_property_tests=True,
                min_test_coverage=85.0,
                requires_mutation_testing=True
            ),
            f"{TaskComplexity.MEDIUM.value}_{BranchType.MAIN.value}": TestingRequirements(
                min_acceptance_criteria=4,
                requires_test_strategy=True,
                requires_performance_tests=True,
                requires_integration_tests=True,
                requires_property_tests=True,
                min_test_coverage=90.0,
                requires_mutation_testing=True
            ),
            f"{TaskComplexity.HIGH.value}_{BranchType.MAIN.value}": TestingRequirements(
                min_acceptance_criteria=5,
                requires_test_strategy=True,
                requires_performance_tests=True,
                requires_integration_tests=True,
                requires_property_tests=True,
                min_test_coverage=95.0,
                requires_mutation_testing=True
            ),
            f"{TaskComplexity.CRITICAL.value}_{BranchType.MAIN.value}": TestingRequirements(
                min_acceptance_criteria=6,
                requires_test_strategy=True,
                requires_performance_tests=True,
                requires_integration_tests=True,
                requires_property_tests=True,
                min_test_coverage=95.0,
                requires_mutation_testing=True
            ),

            # Hotfix branches - minimal but focused testing
            f"{TaskComplexity.LOW.value}_{BranchType.HOTFIX.value}": TestingRequirements(
                min_acceptance_criteria=2,
                requires_test_strategy=False,
                requires_performance_tests=False,
                requires_integration_tests=True,
                requires_property_tests=False,
                min_test_coverage=80.0,
                requires_mutation_testing=False
            ),
            f"{TaskComplexity.MEDIUM.value}_{BranchType.HOTFIX.value}": TestingRequirements(
                min_acceptance_criteria=3,
                requires_test_strategy=True,
                requires_performance_tests=False,
                requires_integration_tests=True,
                requires_property_tests=False,
                min_test_coverage=85.0,
                requires_mutation_testing=False
            ),
        }

    def validate_task_creation(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a task during creation.

        Args:
            task_data: Task data to validate

        Returns:
            Dict with validation results

        Raises:
            TaskValidationError: If validation fails
        """
        errors = []
        warnings = []

        # Basic field validation
        errors.extend(self._validate_basic_fields(task_data))

        # Complexity and branch validation
        complexity = self._determine_complexity(task_data)
        branch_type = self._determine_branch_type(task_data)

        # Testing requirements validation
        testing_errors = self._validate_testing_requirements(task_data, complexity, branch_type)
        errors.extend(testing_errors)

        # Content quality validation
        content_warnings = self._validate_content_quality(task_data)
        warnings.extend(content_warnings)

        if errors:
            raise TaskValidationError(f"Task validation failed: {'; '.join(errors)}")

        return {
            "valid": True,
            "complexity": complexity.value,
            "branch_type": branch_type.value,
            "warnings": warnings,
            "recommendations": self._generate_recommendations(task_data, complexity, branch_type)
        }

    def _validate_basic_fields(self, task_data: Dict[str, Any]) -> List[str]:
        """Validate basic required fields."""
        errors = []

        required_fields = ["title", "description"]
        for field in required_fields:
            if not task_data.get(field) or not task_data.get(field).strip():
                errors.append(f"Missing or empty required field: {field}")

        # Title length validation
        title = task_data.get("title", "")
        if len(title) < 5:
            errors.append("Title must be at least 5 characters long")
        elif len(title) > 100:
            errors.append("Title must be less than 100 characters long")

        # Description length validation
        description = task_data.get("description", "")
        if len(description) < 20:
            errors.append("Description must be at least 20 characters long")

        return errors

    def _determine_complexity(self, task_data: Dict[str, Any]) -> TaskComplexity:
        """Determine task complexity based on content analysis."""
        title = task_data.get("title", "").lower()
        description = task_data.get("description", "").lower()

        # Keywords indicating high complexity
        high_complexity_keywords = [
            "architect", "refactor", "migration", "integration", "security",
            "performance", "scalability", "distributed", "concurrent"
        ]

        # Keywords indicating critical complexity
        critical_keywords = [
            "breaking", "major", "critical", "production", "infrastructure"
        ]

        text = f"{title} {description}"

        if any(keyword in text for keyword in critical_keywords):
            return TaskComplexity.CRITICAL
        elif any(keyword in text for keyword in high_complexity_keywords):
            return TaskComplexity.HIGH
        elif len(description.split()) > 50:  # Longer descriptions suggest more complexity
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.LOW

    def _determine_branch_type(self, task_data: Dict[str, Any]) -> BranchType:
        """Determine branch type based on task context."""
        # Check if branch is explicitly specified
        branch = task_data.get("branch", "").lower()

        if "scientific" in branch or "feature/scientific" in branch:
            return BranchType.SCIENTIFIC
        elif branch == "main":
            return BranchType.MAIN
        elif "hotfix" in branch:
            return BranchType.HOTFIX
        else:
            return BranchType.FEATURE  # Default

    def _validate_testing_requirements(
        self,
        task_data: Dict[str, Any],
        complexity: TaskComplexity,
        branch_type: BranchType
    ) -> List[str]:
        """Validate testing requirements based on complexity and branch."""
        errors = []

        key = f"{complexity.value}_{branch_type.value}"
        requirements = self.testing_requirements.get(key)

        if not requirements:
            # Fallback to medium feature branch requirements
            requirements = self.testing_requirements.get(f"{TaskComplexity.MEDIUM.value}_{BranchType.FEATURE.value}")

        if requirements:
            # Check acceptance criteria
            acceptance_criteria = task_data.get("acceptance_criteria", [])
            if len(acceptance_criteria) < requirements.min_acceptance_criteria:
                errors.append(
                    f"Task requires at least {requirements.min_acceptance_criteria} "
                    f"acceptance criteria (found {len(acceptance_criteria)})"
                )

            # Check test strategy
            if requirements.requires_test_strategy:
                test_strategy = task_data.get("test_strategy", "").strip()
                if not test_strategy or len(test_strategy) < 10:
                    errors.append("Test strategy is required and must be detailed")

            # Check for specific testing types in test strategy
            test_strategy_lower = task_data.get("test_strategy", "").lower()

            if requirements.requires_performance_tests and "performance" not in test_strategy_lower:
                errors.append("Performance testing must be included in test strategy")

            if requirements.requires_integration_tests and "integration" not in test_strategy_lower:
                errors.append("Integration testing must be included in test strategy")

            if requirements.requires_property_tests and "property" not in test_strategy_lower:
                errors.append("Property-based testing must be included in test strategy")

            if requirements.requires_mutation_testing and "mutation" not in test_strategy_lower:
                errors.append("Mutation testing must be included in test strategy")

        return errors

    def _validate_content_quality(self, task_data: Dict[str, Any]) -> List[str]:
        """Validate content quality and provide warnings."""
        warnings = []

        description = task_data.get("description", "")

        # Check for vague language
        vague_words = ["etc", "things", "stuff", "whatever", "maybe", "probably"]
        found_vague = [word for word in vague_words if word in description.lower()]
        if found_vague:
            warnings.append(f"Consider being more specific - found vague terms: {', '.join(found_vague)}")

        # Check for measurable outcomes
        measurable_indicators = ["should", "must", "will", "can", "able to"]
        has_measurable = any(indicator in description.lower() for indicator in measurable_indicators)
        if not has_measurable:
            warnings.append("Consider adding measurable outcomes or success criteria")

        return warnings

    def _generate_recommendations(
        self,
        task_data: Dict[str, Any],
        complexity: TaskComplexity,
        branch_type: BranchType
    ) -> List[str]:
        """Generate recommendations for task improvement."""
        recommendations = []

        key = f"{complexity.value}_{branch_type.value}"
        requirements = self.testing_requirements.get(key)

        if requirements:
            if requirements.min_test_coverage:
                recommendations.append(
                    f"Aim for {requirements.min_test_coverage}% test coverage"
                )

            if requirements.requires_property_tests:
                recommendations.append(
                    "Consider using property-based testing for edge cases"
                )

            if requirements.requires_performance_tests:
                recommendations.append(
                    "Include performance benchmarks in testing"
                )

        # Complexity-specific recommendations
        if complexity == TaskComplexity.HIGH:
            recommendations.append(
                "Consider breaking this task into smaller subtasks"
            )
        elif complexity == TaskComplexity.CRITICAL:
            recommendations.append(
                "This task requires thorough review and extensive testing"
            )

        return recommendations

    def validate_task_update(self, existing_task: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate task updates.

        Args:
            existing_task: Current task data
            updates: Proposed updates

        Returns:
            Validation results
        """
        # Merge updates for validation
        merged_task = {**existing_task, **updates}
        return self.validate_task_creation(merged_task)


# Global service instance
task_validation_service = TaskValidationService()