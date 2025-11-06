"""
CI/CD Integration Service for Task Master AI

This service handles communication between CI/CD pipelines and the Task Master system,
providing automated testing validation and status updates for task completion workflows.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class TestResult(BaseModel):
    """Model for test execution results."""
    total_tests: int = Field(..., description="Total number of tests executed")
    passed_tests: int = Field(..., description="Number of tests that passed")
    failed_tests: int = Field(..., description="Number of tests that failed")
    skipped_tests: int = Field(..., description="Number of tests that were skipped")
    coverage_percentage: Optional[float] = Field(None, description="Code coverage percentage")
    test_duration: Optional[float] = Field(None, description="Test execution duration in seconds")

    # Advanced testing metrics (scientific branch)
    property_tests_run: Optional[int] = Field(None, description="Number of property-based tests executed")
    mutation_score: Optional[float] = Field(None, description="Mutation testing score (0-100)")
    performance_baseline: Optional[Dict[str, float]] = Field(None, description="Performance benchmark baselines")
    flaky_tests_detected: Optional[int] = Field(None, description="Number of potentially flaky tests detected")
    integration_tests_passed: Optional[int] = Field(None, description="Number of integration tests passed")


class CIStatus(BaseModel):
    """Model for CI/CD pipeline status."""
    status: str = Field(..., description="CI status: 'success', 'failure', 'pending', 'running'")
    branch: str = Field(..., description="Git branch name")
    commit_sha: str = Field(..., description="Git commit SHA")
    pr_number: Optional[int] = Field(None, description="Pull request number if applicable")
    test_results: Optional[TestResult] = Field(None, description="Test execution results")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Status timestamp")


class CICDService:
    """
    Service for handling CI/CD integration with Task Master AI.

    This service provides methods to:
    - Receive and process CI/CD status updates
    - Validate test results against task requirements
    - Update task status based on CI/CD outcomes
    - Provide branch-specific validation rules
    """

    def __init__(self, task_master_api_url: str = "http://localhost:8000/api"):
        """
        Initialize the CI/CD service.

        Args:
            task_master_api_url: Base URL for Task Master API
        """
        self.task_master_api_url = task_master_api_url
        self.client = httpx.AsyncClient(timeout=30.0)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def process_ci_status(self, ci_status: CIStatus) -> Dict[str, Any]:
        """
        Process a CI/CD status update and update relevant tasks.

        Args:
            ci_status: CI/CD status information

        Returns:
            Dict containing processing results
        """
        logger.info(f"Processing CI status for branch {ci_status.branch}, commit {ci_status.commit_sha}")

        # Find tasks associated with this branch/commit
        associated_tasks = await self._find_associated_tasks(ci_status)

        results = {
            "processed_tasks": [],
            "validation_results": [],
            "errors": []
        }

        for task in associated_tasks:
            try:
                validation_result = await self._validate_task_completion(task, ci_status)
                results["processed_tasks"].append(task["id"])
                results["validation_results"].append(validation_result)

                # Update task status if validation passes
                if validation_result["status"] == "passed":
                    await self._update_task_status(task["id"], "completed", validation_result)

            except Exception as e:
                logger.error(f"Error processing task {task['id']}: {e}")
                results["errors"].append(f"Task {task['id']}: {str(e)}")

        return results

    async def _find_associated_tasks(self, ci_status: CIStatus) -> list:
        """
        Find tasks associated with the CI status.

        For now, this is a placeholder that would query Task Master API
        to find tasks linked to the branch or PR.
        """
        # TODO: Implement actual task lookup via Task Master API
        # This would query tasks by branch name or PR number

        # Placeholder: return mock tasks for demonstration
        return [
            {
                "id": "example-task-1",
                "branch": ci_status.branch,
                "required_coverage": 80.0,
                "required_test_types": ["unit", "integration"]
            }
        ]

    async def _validate_task_completion(self, task: Dict[str, Any], ci_status: CIStatus) -> Dict[str, Any]:
        """
        Validate if a task meets completion criteria based on CI results.

        Args:
            task: Task information
            ci_status: CI/CD status

        Returns:
            Dict with validation results
        """
        validation = {
            "task_id": task["id"],
            "status": "pending",
            "checks": [],
            "errors": [],
            "branch": ci_status.branch
        }

        # Check CI status
        if ci_status.status != "success":
            validation["errors"].append(f"CI status is {ci_status.status}, expected success")
            return validation

        # Get branch-specific validation rules
        branch_rules = self.get_branch_validation_rules(ci_status.branch)
        validation["branch_rules"] = branch_rules

        # Check test results if available
        if ci_status.test_results:
            test_result = ci_status.test_results

            # Check test pass rate
            if test_result.failed_tests > 0:
                validation["errors"].append(f"{test_result.failed_tests} tests failed")
            else:
                validation["checks"].append("All tests passed")

            # Check coverage against branch-specific requirements
            required_coverage = branch_rules.get("min_coverage", task.get("required_coverage", 0))
            if test_result.coverage_percentage is not None:
                if test_result.coverage_percentage >= required_coverage:
                    validation["checks"].append(f"Coverage {test_result.coverage_percentage:.1f}% meets requirement {required_coverage}%")
                else:
                    validation["errors"].append(f"Coverage {test_result.coverage_percentage:.1f}% below requirement {required_coverage}%")

            # Branch-specific validations with advanced testing requirements
        if ci_status.branch.startswith("feature/scientific-") or ci_status.branch == "scientific":
            validation["checks"].append("Scientific branch validation applied")

            # Scientific-specific test requirements
            if branch_rules.get("require_scientific_tests"):
                validation["checks"].append("Scientific-specific tests executed")

            # Property-based testing validation
            if branch_rules.get("require_property_tests"):
                if test_result.property_tests_run and test_result.property_tests_run > 0:
                    validation["checks"].append(f"Property-based tests executed: {test_result.property_tests_run}")
                else:
                    validation["errors"].append("Property-based tests required but not executed")

            # Mutation testing validation
            if branch_rules.get("require_mutation_testing"):
                min_score = branch_rules.get("min_mutation_score", 0)
                if test_result.mutation_score is not None:
                    if test_result.mutation_score >= min_score:
                        validation["checks"].append(f"Mutation score {test_result.mutation_score:.1f}% meets requirement {min_score}%")
                    else:
                        validation["errors"].append(f"Mutation score {test_result.mutation_score:.1f}% below requirement {min_score}%")
                else:
                    validation["errors"].append("Mutation testing required but not executed")

            # Performance testing validation
            if branch_rules.get("require_performance_tests"):
                if test_result.performance_baseline:
                    validation["checks"].append("Performance benchmarks executed")
                else:
                    validation["errors"].append("Performance testing required but not executed")

            # Additional scientific-specific checks
            for check in branch_rules.get("additional_checks", []):
                validation["checks"].append(f"Scientific check: {check}")

        elif ci_status.branch.startswith("feature/"):
            validation["checks"].append("Feature branch validation applied")
            for check in branch_rules.get("additional_checks", []):
                validation["checks"].append(f"Feature check: {check}")

        elif ci_status.branch == "main":
            validation["checks"].append("Main branch validation applied")

            # Strict main branch requirements
            if branch_rules.get("require_property_tests"):
                if not (test_result.property_tests_run and test_result.property_tests_run > 0):
                    validation["errors"].append("Property-based tests required for main branch")

            if branch_rules.get("require_mutation_testing"):
                min_score = branch_rules.get("min_mutation_score", 0)
                if not (test_result.mutation_score and test_result.mutation_score >= min_score):
                    validation["errors"].append(f"Mutation testing with score >= {min_score}% required for main branch")

            for check in branch_rules.get("additional_checks", []):
                validation["checks"].append(f"Main branch check: {check}")

        # Validate task-branch association
        task_branch = task.get("branch")
        if task_branch and task_branch != ci_status.branch:
            validation["errors"].append(f"Task branch mismatch: task expects '{task_branch}', CI reports '{ci_status.branch}'")

        # Determine overall status
        if not validation["errors"]:
            validation["status"] = "passed"
        else:
            validation["status"] = "failed"

        return validation

    async def _update_task_status(self, task_id: str, status: str, validation_result: Dict[str, Any]):
        """
        Update task status in Task Master.

        Args:
            task_id: Task identifier
            status: New status
            validation_result: Validation details
        """
        # TODO: Implement actual Task Master API call
        logger.info(f"Would update task {task_id} to status {status} with validation: {validation_result}")

        # Placeholder for API call
        # await self.client.post(
        #     f"{self.task_master_api_url}/tasks/{task_id}/status",
        #     json={"status": status, "validation": validation_result}
        # )

    def get_branch_validation_rules(self, branch: str) -> Dict[str, Any]:
        """
        Get validation rules specific to a branch.

        Args:
            branch: Branch name

        Returns:
            Dict with validation rules
        """
        rules = {
            "min_coverage": 80.0,
            "require_scientific_tests": False,
            "require_property_tests": False,
            "require_mutation_testing": False,
            "require_performance_tests": False,
            "min_mutation_score": 0.0,
            "additional_checks": []
        }

        # Scientific branch specific rules - advanced testing requirements
        if branch.startswith("feature/scientific-") or branch == "scientific":
            rules.update({
                "min_coverage": 85.0,
                "require_scientific_tests": True,
                "require_property_tests": True,
                "require_mutation_testing": True,
                "require_performance_tests": True,
                "min_mutation_score": 75.0,
                "additional_checks": [
                    "data_platform_tests",
                    "scientific_validation",
                    "property_based_tests",
                    "mutation_testing",
                    "performance_regression_tests",
                    "integration_test_suites"
                ]
            })

        # Feature branch rules - moderate testing requirements
        elif branch.startswith("feature/"):
            rules.update({
                "min_coverage": 75.0,
                "require_property_tests": False,
                "require_mutation_testing": False,
                "require_performance_tests": False,
                "additional_checks": ["feature_integration_tests"]
            })

        # Main branch - strict testing requirements
        elif branch == "main":
            rules.update({
                "min_coverage": 90.0,
                "require_property_tests": True,
                "require_mutation_testing": True,
                "require_performance_tests": True,
                "min_mutation_score": 80.0,
                "additional_checks": [
                    "comprehensive_integration_tests",
                    "performance_regression_tests",
                    "security_tests",
                    "mutation_testing"
                ]
            })

        return rules


# Global service instance
ci_cd_service = CICDService()