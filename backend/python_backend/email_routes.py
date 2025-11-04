import json
import logging
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request

from backend.node_engine.workflow_engine import WorkflowEngine
from src.core.auth import get_current_active_user

from ..python_nlp.smart_filters import SmartFilterManager  # Corrected import
from .ai_engine import AdvancedAIEngine
from .database import DatabaseManager, get_db
from .dependencies import get_ai_engine, get_email_service, get_filter_manager, get_workflow_engine
from .exceptions import AIAnalysisError, DatabaseError, EmailNotFoundException
from .models import EmailCreate, EmailResponse, EmailUpdate
from .performance_monitor import log_performance
from .services.email_service import EmailService
from .utils import create_log_data, handle_pydantic_validation

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/emails", response_model=List[EmailResponse])
@log_performance(operation="get_emails")
async def get_emails(
    request: Request,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    is_unread: Optional[bool] = None,
    current_user: str = Depends(get_current_active_user),
    email_repo: EmailRepository = Depends(get_email_repository),
):
    """
    Retrieves a list of emails, with optional filtering by category and search term.
    Requires authentication.

    Args:
        request: The incoming request object.
        category_id: An optional category ID to filter emails.
        search: An optional search term to filter emails by subject, content, or sender.
        is_unread: An optional flag to filter unread emails.
        email_repo: The email repository dependency.

    Returns:
        A list of emails that match the filtering criteria.

    Raises:
        HTTPException: If a database error occurs or if there's a validation error.
    """
    try:
        if search:
            emails = await email_repo.search_emails(search)
            if category_id is not None:
                emails = [email for email in emails if email.get("category_id") == category_id]
        else:
            emails = await email_repo.get_emails(category_id=category_id, is_unread=is_unread)

        try:
            return [EmailResponse(**email) for email in emails]
        except Exception as e_outer:
            logger.error(f"Validation error for emails: {e_outer}", exc_info=True)
            raise HTTPException(status_code=500, detail="Data validation error")
    except Exception as e:
        logger.error(f"Failed to get emails: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve emails")


@router.get("/api/emails/{email_id}", response_model=EmailResponse)
@log_performance(operation="get_email")
async def get_email(
    request: Request,
    email_id: int,
    current_user: str = Depends(get_current_active_user),
    email_repo: EmailRepository = Depends(get_email_repository),
):
    """
    Retrieves a specific email by its unique ID.
    Requires authentication.

    Args:
        request: The incoming request object.
        email_id: The ID of the email to retrieve.
        email_repo: The email repository dependency.

    Returns:
        The email object if found.

    Raises:
        HTTPException: If the email is not found, or if a database or validation error occurs.
    """
    try:
        email = await email_repo.get_email_by_id(email_id)
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        try:
            return EmailResponse(**email)
        except Exception as e:
            logger.error(f"Validation error for email {email_id}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Data validation error")
    except HTTPException:
        raise
    except Exception as e:
        log_data = {
            "message": f"Unhandled error fetching email id {email_id}",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to fetch email")


@router.post("/api/emails", response_model=EmailResponse)
@log_performance(operation="create_email")
async def create_email(
    request: Request,
    email: EmailCreate,
    background_tasks: BackgroundTasks,
    current_user: str = Depends(get_current_active_user),
    email_repo: EmailRepository = Depends(get_email_repository),
    workflow_engine: WorkflowEngine = Depends(get_workflow_engine),
):
    """Create new email with AI analysis using the active workflow.
    Requires authentication."""
    try:
        # Run the active workflow to process the email data
        processed_data = await workflow_engine.run_workflow(email.model_dump())

        # Create the email in the database with the processed data
        created_email_dict = await email_repo.create_email(processed_data)

        try:
            return EmailResponse(**created_email_dict)
        except Exception as e_outer:
            logger.error(f"Validation error for created email: {e_outer}", exc_info=True)
            raise HTTPException(status_code=500, detail="Data validation error")
    except Exception as e:
        log_data = create_log_data(
            message="Unhandled error in create_email",
            request_url=request.url,
            error_type=type(e).__name__,
            error_detail=str(e),
        )
        logger.error(json.dumps(log_data))
        raise HTTPException(
            status_code=500, detail="Failed to create email due to an unexpected error."
        )


@router.put("/api/emails/{email_id}", response_model=EmailResponse)
@log_performance(operation="update_email")
async def update_email(
    request: Request,
    email_id: int,
    email_update: EmailUpdate,
    current_user: str = Depends(get_current_active_user),
    email_repo: EmailRepository = Depends(get_email_repository),
):
    """
    Updates an existing email by its ID.
    Requires authentication.

    Args:
        request: The incoming request object.
        email_id: The ID of the email to update.
        email_update: The email data to update.
        email_repo: The email repository dependency.

    Returns:
        The updated email object.

    Raises:
        HTTPException: If the email is not found, or if a database or validation error occurs.
    """
    try:
        updated_email_dict = await email_repo.update_email(
            email_id, email_update.model_dump(exclude_unset=True)
        )
        if not updated_email_dict:
            raise HTTPException(status_code=404, detail="Email not found")
        try:
            return EmailResponse(**updated_email_dict)
        except Exception as e_outer:
            logger.error(f"Validation error for updated email {email_id}: {e_outer}", exc_info=True)
            raise HTTPException(status_code=500, detail="Data validation error")
    except HTTPException:
        raise
    except Exception as e:
        log_data = {
            "message": f"Unhandled error updating email id {email_id}",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to update email due to an unexpected error.")
