import json
import logging
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request

from src.backend.node_engine.workflow_engine import WorkflowEngine
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
from .workflow_engine import WorkflowEngine

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/emails", response_model=List[EmailResponse])
@log_performance(operation="get_emails")
async def get_emails(
    request: Request,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    is_unread: Optional[bool] = None,
    current_user: str = Depends(get_current_active_user),
    email_service: EmailService = Depends(get_email_service),
):
    """
    Retrieves a list of emails, with optional filtering by category and search term.

    Args:
        request: The incoming request object.
        category_id: An optional category ID to filter emails.
        search: An optional search term to filter emails by subject, content, or sender.
        current_user: The authenticated user making the request.

    Returns:
        A list of emails that match the filtering criteria.

    Raises:
        HTTPException: If a database error occurs or if there's a validation error.
    """
    try:
        if search:
            result = await email_service.search_emails(search, limit)
        else:
            result = await email_service.get_emails(category_id, limit, offset, is_unread)
        return [EmailResponse(**email) for email in result]
    except Exception as e:
        logger.error(f"Failed to get emails: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve emails")


@router.get("/api/emails/{email_id}", response_model=EmailResponse)  # Changed to EmailResponse
@log_performance(operation="get_email")
async def get_email_by_id(
    email_id: int,
    request: Request,
    current_user: str = Depends(get_current_active_user),
    email_service: EmailService = Depends(get_email_service),
):
    """
    Retrieves a specific email by its unique ID.

    Args:
        request: The incoming request object.
        email_id: The ID of the email to retrieve.
        current_user: The authenticated user making the request.

    Returns:
        The email object if found.

    Raises:
        HTTPException: If the email is not found, or if a database or validation error occurs.
    """
    try:
        email = await email_service.get_email_by_id(email_id)
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        return EmailResponse(**email)
    except Exception as e:
        logger.error(f"Failed to get emails: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve emails")
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
    email_service: EmailService = Depends(get_email_service),
    workflow_engine: WorkflowEngine = Depends(get_workflow_engine),
):
    """Create new email with AI analysis using the active workflow.

    Requires authentication.
    """
    try:
        # Run the active workflow to process the email data
        processed_data = await workflow_engine.run_workflow(email.model_dump())
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


@router.put("/api/emails/{email_id}", response_model=EmailResponse)  # Changed to EmailResponse
@log_performance(operation="update_email")
async def update_email(
    request: Request,
    email_id: int,
    email_update: EmailUpdate,
    current_user: str = Depends(get_current_active_user),
    email_service: EmailService = Depends(get_email_service),
):
    """
    Updates an existing email by its ID.

    Args:
        request: The incoming request object.
        email_id: The ID of the email to update.
        email_update: The email data to update.
        current_user: The authenticated user making the request.

    Returns:
        The updated email object.

    Raises:
        HTTPException: If the email is not found, or if a database or validation error occurs.
    """
    try:
        updated_email = await email_service.update_email(email_id, email_update)
        if not updated_email:
            raise HTTPException(status_code=404, detail="Email not found")
        return EmailResponse(**updated_email)
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
        raise DatabaseError(detail="Failed to update email due to an unexpected error.")
