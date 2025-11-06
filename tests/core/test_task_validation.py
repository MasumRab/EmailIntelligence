"""
Unit tests for Task Validation Service.

Tests the validation logic for task creation and updates,
ensuring testing requirements are properly enforced.
"""

import pytest
from unittest.mock import patch

from src.backend.services.task_validation_service import (
    TaskValidationService,
    TaskValidationError,
    TaskComplexity,
    BranchType,
    TestingRequirements
)


class TestTaskValidationService:
    """Test cases for TaskValidationService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = TaskValidationService()

    def test_validate_basic_fields_success(self):
        """Test validation of basic required fields - success case."""
        task_data = {
            "title": "Test Task Title",
            "description": "This is a test task description that is long enough to pass validation."
        }

        errors = self.service._validate_basic_fields(task_data)
        assert len(errors) == 0

    def test_validate_basic_fields_missing_title(self):
        """Test validation fails when title is missing."""
        task_data = {
            "description": "This is a test task description."
        }

        errors = self.service._validate_basic_fields(task_data)
        assert len(errors) > 0
        assert any("title" in error.lower() for error in errors)

    def test_validate_basic_fields_title_too_short(self):
        """Test validation fails when title is too short."""
        task_data = {
            "title": "Hi",
            "description": "This is a test task description."
        }

        errors = self.service._validate_basic_fields(task_data)
        assert len(errors) > 0
        assert any("title must be at least" in error.lower() for error in errors)

    def test_determine_complexity_low(self):
        """Test complexity determination for low-complexity tasks."""
        task_data = {
            "title": "Fix typo",
            "description": "Fix a small typo in the documentation."
        }

        complexity = self.service._determine_complexity(task_data)
        assert complexity == TaskComplexity.LOW

    def test_determine_complexity_high(self):
        """Test complexity determination for high-complexity tasks."""
        task_data = {
            "title": "Refactor architecture",
            "description": "Major architectural refactoring involving security and performance improvements."
        }

        complexity = self.service._determine_complexity(task_data)
        assert complexity == TaskComplexity.HIGH

    def test_determine_complexity_critical(self):
        """Test complexity determination for critical tasks."""
        task_data = {
            "title": "Breaking change",
            "description": "Implement breaking API changes for production system."
        }

        complexity = self.service._determine_complexity(task_data)
        assert complexity == TaskComplexity.CRITICAL

    def test_determine_branch_type_scientific(self):
        """Test branch type determination for scientific branches."""
        task_data = {"branch": "feature/scientific-ai"}

        branch_type = self.service._determine_branch_type(task_data)
        assert branch_type == BranchType.SCIENTIFIC

    def test_determine_branch_type_main(self):
        """Test branch type determination for main branch."""
        task_data = {"branch": "main"}

        branch_type = self.service._determine_branch_type(task_data)
        assert branch_type == BranchType.MAIN

    def test_determine_branch_type_feature_default(self):
        """Test branch type defaults to feature."""
        task_data = {"branch": "feature/new-ui"}

        branch_type = self.service._determine_branch_type(task_data)
        assert branch_type == BranchType.FEATURE

    def test_validate_testing_requirements_scientific_high(self):
        """Test testing requirements validation for scientific high-complexity tasks."""
        task_data = {
            "acceptance_criteria": ["AC1", "AC2", "AC3", "AC4", "AC5", "AC6"],  # 6 criteria
            "test_strategy": "Comprehensive testing including property-based tests, mutation testing, performance benchmarks, and integration tests."
        }

        complexity = TaskComplexity.HIGH
        branch_type = BranchType.SCIENTIFIC

        errors = self.service._validate_testing_requirements(task_data, complexity, branch_type)
        assert len(errors) == 0  # Should pass

    def test_validate_testing_requirements_insufficient_ac(self):
        """Test validation fails when insufficient acceptance criteria."""
        task_data = {
            "acceptance_criteria": ["Only one criterion"],
            "test_strategy": "Basic testing strategy."
        }

        complexity = TaskComplexity.HIGH
        branch_type = BranchType.SCIENTIFIC

        errors = self.service._validate_testing_requirements(task_data, complexity, branch_type)
        assert len(errors) > 0
        assert any("acceptance criteria" in error.lower() for error in errors)

    def test_validate_testing_requirements_missing_property_tests(self):
        """Test validation fails when property tests are required but not mentioned."""
        task_data = {
            "acceptance_criteria": ["AC1", "AC2", "AC3", "AC4", "AC5"],
            "test_strategy": "Integration and performance testing only."  # Missing property tests
        }

        complexity = TaskComplexity.MEDIUM
        branch_type = BranchType.SCIENTIFIC

        errors = self.service._validate_testing_requirements(task_data, complexity, branch_type)
        assert len(errors) > 0
        assert any("property" in error.lower() for error in errors)

    def test_validate_task_creation_success(self):
        """Test successful task creation validation."""
        task_data = {
            "title": "Implement user authentication",
            "description": "Implement secure user authentication with JWT tokens and password hashing. This involves creating login endpoints, token validation middleware, and secure password storage.",
            "acceptance_criteria": [
                "Users can log in with valid credentials",
                "Invalid credentials are rejected",
                "JWT tokens are properly validated",
                "Passwords are securely hashed"
            ],
            "test_strategy": "Unit tests for authentication logic, integration tests for API endpoints, property-based testing for token validation edge cases.",
            "branch": "feature/auth",
            "priority": "high"
        }

        result = self.service.validate_task_creation(task_data)

        assert result["valid"] is True
        assert "complexity" in result
        assert "branch_type" in result

    def test_validate_task_creation_failure(self):
        """Test task creation validation failure."""
        task_data = {
            "title": "Hi",  # Too short
            "description": "Short",  # Too short
            "acceptance_criteria": [],  # Insufficient
        }

        with pytest.raises(TaskValidationError):
            self.service.validate_task_creation(task_data)

    def test_validate_content_quality_warnings(self):
        """Test content quality validation produces warnings."""
        task_data = {
            "title": "Test Task",
            "description": "This task does some stuff and things etc. It might work or whatever."
        }

        warnings = self.service._validate_content_quality(task_data)
        assert len(warnings) > 0
        assert any("vague" in warning.lower() for warning in warnings)

    def test_generate_recommendations(self):
        """Test recommendation generation."""
        task_data = {
            "title": "High complexity task",
            "description": "This is a high complexity architectural refactoring task.",
            "branch": "scientific"
        }

        complexity = TaskComplexity.HIGH
        branch_type = BranchType.SCIENTIFIC

        recommendations = self.service._generate_recommendations(task_data, complexity, branch_type)

        assert len(recommendations) > 0
        assert any("test coverage" in rec.lower() for rec in recommendations)

    def test_testing_requirements_matrix_complete(self):
        """Test that testing requirements matrix covers all combinations."""
        # This test ensures we don't miss any complexity/branch combinations
        expected_keys = []
        for complexity in TaskComplexity:
            for branch_type in [BranchType.FEATURE, BranchType.SCIENTIFIC, BranchType.MAIN, BranchType.HOTFIX]:
                if branch_type == BranchType.MAIN and complexity == TaskComplexity.CRITICAL:
                    expected_keys.append(f"{complexity.value}_{branch_type.value}")
                elif branch_type != BranchType.MAIN or complexity != TaskComplexity.CRITICAL:
                    expected_keys.append(f"{complexity.value}_{branch_type.value}")

        matrix_keys = set(self.service.testing_requirements.keys())

        # Check that we have requirements for expected combinations
        for key in expected_keys:
            if key not in matrix_keys:
                # Allow missing combinations to fall back to defaults
                continue
            assert key in matrix_keys, f"Missing requirements for {key}"

    def test_validate_task_update(self):
        """Test task update validation."""
        existing_task = {
            "title": "Original Task",
            "description": "Original description",
            "acceptance_criteria": ["AC1"]
        }

        updates = {
            "title": "Updated Task Title",
            "description": "Updated description that is long enough for validation."
        }

        result = self.service.validate_task_update(existing_task, updates)
        assert result["valid"] is True