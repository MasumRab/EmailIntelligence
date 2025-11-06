"""
CI/CD Integration API Routes

Provides endpoints for CI/CD pipeline integration with Task Master AI,
enabling automated testing validation and status updates.
"""

import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from datetime import datetime

from ..services.ci_cd_service import ci_cd_service, CIStatus, TestResult

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ci-cd", tags=["ci-cd"])


class CIStatusRequest(BaseModel):
    """Request model for CI status updates."""
    status: str = Field(..., description="CI status: 'success', 'failure', 'pending', 'running'")
    branch: str = Field(..., description="Git branch name")
    commit_sha: str = Field(..., description="Git commit SHA")
    pr_number: Optional[int] = Field(None, description="Pull request number if applicable")
    test_results: Optional[Dict[str, Any]] = Field(None, description="Test execution results")
    repository: str = Field(..., description="Repository name")
    workflow_run_id: Optional[str] = Field(None, description="CI workflow run ID")


@router.post("/status", summary="Update CI/CD Status")
async def update_ci_status(
    status_request: CIStatusRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Receive and process CI/CD status updates from GitHub Actions or other CI systems.

    This endpoint allows CI/CD pipelines to report their status and test results,
    which are then used to validate task completion requirements.
    """
    try:
        logger.info(f"Received CI status update for branch {status_request.branch}")

        # Convert request to CIStatus model
        test_results = None
        if status_request.test_results:
            test_results = TestResult(**status_request.test_results)

        ci_status = CIStatus(
            status=status_request.status,
            branch=status_request.branch,
            commit_sha=status_request.commit_sha,
            pr_number=status_request.pr_number,
            test_results=test_results
        )

        # Process in background to avoid blocking CI pipeline
        background_tasks.add_task(ci_cd_service.process_ci_status, ci_status)

        return {
            "message": "CI status update received and queued for processing",
            "branch": status_request.branch,
            "commit_sha": status_request.commit_sha,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Error processing CI status update: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process CI status: {str(e)}")


@router.get("/validation-rules/{branch}", summary="Get Branch Validation Rules")
async def get_branch_validation_rules(branch: str) -> Dict[str, Any]:
    """
    Get validation rules for a specific branch.

    Returns the testing and validation requirements that apply to tasks
    associated with the specified branch.
    """
    try:
        rules = ci_cd_service.get_branch_validation_rules(branch)
        return {
            "branch": branch,
            "validation_rules": rules
        }
    except Exception as e:
        logger.error(f"Error getting validation rules for branch {branch}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get validation rules: {str(e)}")


@router.post("/webhook/github", summary="GitHub Webhook Handler")
async def github_webhook_handler(
    payload: Dict[str, Any],
    background_tasks: BackgroundTasks,
    x_github_event: str = None
) -> Dict[str, Any]:
    """
    Handle GitHub webhooks for CI/CD status updates.

    Processes workflow_run and check_run events to update task validation status.
    """
    try:
        if x_github_event == "workflow_run":
            return await _handle_workflow_run(payload, background_tasks)
        elif x_github_event == "check_run":
            return await _handle_check_run(payload, background_tasks)
        else:
            return {"message": f"Unhandled event type: {x_github_event}"}

    except Exception as e:
        logger.error(f"Error processing GitHub webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process webhook: {str(e)}")


async def _handle_workflow_run(payload: Dict[str, Any], background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """Handle GitHub workflow_run webhook events."""
    workflow_run = payload.get("workflow_run", {})

    # Extract relevant information
    status = workflow_run.get("status", "unknown")  # completed, in_progress, etc.
    conclusion = workflow_run.get("conclusion")  # success, failure, etc.

    # Map GitHub status to our CI status
    if status == "completed":
        ci_status = conclusion if conclusion else "unknown"
    else:
        ci_status = "running" if status == "in_progress" else "pending"

    branch = workflow_run.get("head_branch", "")
    commit_sha = workflow_run.get("head_sha", "")
    pr_number = None

    # Check if this is from a PR
    if "pull_requests" in payload and payload["pull_requests"]:
        pr_number = payload["pull_requests"][0].get("number")

    # Create CI status update
    ci_status_obj = CIStatus(
        status=ci_status,
        branch=branch,
        commit_sha=commit_sha,
        pr_number=pr_number
    )

    # Process in background
    background_tasks.add_task(ci_cd_service.process_ci_status, ci_status_obj)

    return {
        "message": "GitHub workflow_run event processed",
        "workflow": workflow_run.get("name"),
        "status": ci_status,
        "branch": branch
    }


async def _handle_check_run(payload: Dict[str, Any], background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """Handle GitHub check_run webhook events."""
    check_run = payload.get("check_run", {})

    # Extract information from check run
    status = check_run.get("status")  # completed, in_progress
    conclusion = check_run.get("conclusion")  # success, failure, etc.

    if status == "completed":
        ci_status = conclusion if conclusion else "unknown"
    else:
        ci_status = "running"

    # Get branch and commit info
    commit_sha = check_run.get("head_sha", "")
    branch = ""

    # Try to get branch from pull request if available
    if "pull_requests" in payload and payload["pull_requests"]:
        pr = payload["pull_requests"][0]
        branch = pr.get("head", {}).get("ref", "")

    ci_status_obj = CIStatus(
        status=ci_status,
        branch=branch,
        commit_sha=commit_sha
    )

    # Process in background
    background_tasks.add_task(ci_cd_service.process_ci_status, ci_status_obj)

    return {
        "message": "GitHub check_run event processed",
        "check_name": check_run.get("name"),
        "status": ci_status
    }