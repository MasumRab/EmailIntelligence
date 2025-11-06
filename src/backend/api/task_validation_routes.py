"""
Task Validation API Routes

Provides endpoints for task validation during creation and updates,
ensuring tasks meet quality standards and testing requirements.
"""

import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field

from ..services.task_validation_service import task_validation_service, TaskValidationError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/task-validation", tags=["task-validation"])


class TaskValidationRequest(BaseModel):
    """Request model for task validation."""
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    acceptance_criteria: list = Field(default_factory=list, description="List of acceptance criteria")
    test_strategy: str = Field("", description="Test strategy description")
    branch: str = Field("", description="Target branch name")
    priority: str = Field("medium", description="Task priority")
    dependencies: list = Field(default_factory=list, description="Task dependencies")


class TaskValidationResponse(BaseModel):
    """Response model for task validation."""
    valid: bool = Field(..., description="Whether the task is valid")
    complexity: str = Field("", description="Determined task complexity")
    branch_type: str = Field("", description="Determined branch type")
    warnings: list = Field(default_factory=list, description="Validation warnings")
    recommendations: list = Field(default_factory=list, description="Improvement recommendations")
    errors: list = Field(default_factory=list, description="Validation errors")


@router.post("/validate-creation", response_model=TaskValidationResponse)
async def validate_task_creation(
    request: TaskValidationRequest
) -> TaskValidationResponse:
    """
    Validate a task during creation.

    This endpoint checks that the task meets quality standards and includes
    appropriate testing requirements based on its complexity and branch context.
    """
    try:
        logger.info(f"Validating task creation: {request.title}")

        # Convert request to dict for validation service
        task_data = {
            "title": request.title,
            "description": request.description,
            "acceptance_criteria": request.acceptance_criteria,
            "test_strategy": request.test_strategy,
            "branch": request.branch,
            "priority": request.priority,
            "dependencies": request.dependencies
        }

        # Validate the task
        result = task_validation_service.validate_task_creation(task_data)

        return TaskValidationResponse(
            valid=result["valid"],
            complexity=result["complexity"],
            branch_type=result["branch_type"],
            warnings=result["warnings"],
            recommendations=result["recommendations"],
            errors=[]
        )

    except TaskValidationError as e:
        logger.warning(f"Task validation failed: {e}")
        return TaskValidationResponse(
            valid=False,
            complexity="",
            branch_type="",
            warnings=[],
            recommendations=[],
            errors=[str(e)]
        )

    except Exception as e:
        logger.error(f"Unexpected error during task validation: {e}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@router.post("/validate-update", response_model=TaskValidationResponse)
async def validate_task_update(
    task_id: str,
    current_task: Dict[str, Any] = Body(..., description="Current task data"),
    updates: Dict[str, Any] = Body(..., description="Proposed updates")
) -> TaskValidationResponse:
    """
    Validate task updates.

    This endpoint validates proposed changes to ensure they maintain
    task quality standards.
    """
    try:
        logger.info(f"Validating task update for task {task_id}")

        # Validate the update
        result = task_validation_service.validate_task_update(current_task, updates)

        return TaskValidationResponse(
            valid=result["valid"],
            complexity=result["complexity"],
            branch_type=result["branch_type"],
            warnings=result["warnings"],
            recommendations=result["recommendations"],
            errors=[]
        )

    except TaskValidationError as e:
        logger.warning(f"Task update validation failed: {e}")
        return TaskValidationResponse(
            valid=False,
            complexity="",
            branch_type="",
            warnings=[],
            recommendations=[],
            errors=[str(e)]
        )

    except Exception as e:
        logger.error(f"Unexpected error during task update validation: {e}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@router.get("/requirements/{complexity}/{branch_type}")
async def get_testing_requirements(
    complexity: str,
    branch_type: str
) -> Dict[str, Any]:
    """
    Get testing requirements for a specific complexity and branch type.

    This endpoint provides the testing standards that apply to tasks
    of the specified complexity targeting the given branch type.
    """
    try:
        # Get requirements from the service
        key = f"{complexity}_{branch_type}"
        requirements = task_validation_service.testing_requirements.get(key)

        if not requirements:
            raise HTTPException(
                status_code=404,
                detail=f"No requirements found for complexity '{complexity}' and branch type '{branch_type}'"
            )

        return {
            "complexity": complexity,
            "branch_type": branch_type,
            "requirements": requirements.dict()
        }

    except Exception as e:
        logger.error(f"Error getting testing requirements: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get requirements: {str(e)}")


@router.get("/complexity-hints")
async def get_complexity_hints() -> Dict[str, Any]:
    """
    Get hints for determining task complexity.

    This endpoint provides guidance on how task complexity is determined
    and examples of different complexity levels.
    """
    return {
        "complexity_levels": {
            "low": {
                "description": "Simple tasks with minimal impact",
                "examples": ["Add a comment", "Fix a typo", "Update documentation"],
                "indicators": ["Short description", "No architectural changes", "Minimal testing needed"]
            },
            "medium": {
                "description": "Tasks requiring careful implementation",
                "examples": ["Add a new feature", "Refactor a function", "Update dependencies"],
                "indicators": ["Moderate description length", "Some testing required", "May affect other components"]
            },
            "high": {
                "description": "Complex tasks with significant impact",
                "examples": ["Major refactoring", "Architecture changes", "Security enhancements"],
                "indicators": ["Long description", "Architectural keywords", "Extensive testing required"]
            },
            "critical": {
                "description": "High-risk tasks affecting production systems",
                "examples": ["Database migrations", "Breaking API changes", "Infrastructure updates"],
                "indicators": ["Critical keywords", "Production impact", "Requires extensive validation"]
            }
        },
        "branch_types": {
            "feature": "Standard feature development branches",
            "scientific": "Research and advanced feature branches with higher testing standards",
            "main": "Production branch with strictest requirements",
            "hotfix": "Emergency fixes with focused testing"
        }
    }