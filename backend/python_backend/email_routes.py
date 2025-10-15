import json
import logging
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request

from ..python_nlp.smart_filters import SmartFilterManager  # Corrected import
from .ai_engine import AdvancedAIEngine
from .database import DatabaseManager, get_db
from .dependencies import get_ai_engine, get_filter_manager, get_workflow_engine, get_email_service
from backend.node_engine.workflow_engine import WorkflowEngine
from .exceptions import AIAnalysisError, DatabaseError, EmailNotFoundException
from .models import EmailResponse
from .models import EmailCreate, EmailUpdate
from .performance_monitor import log_performance
from .utils import create_log_data, handle_pydantic_validation
from .services.email_service import EmailService

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
    email_service: EmailService = Depends(get_email_service),
):
    """
    Retrieves a list of emails, with optional filtering by category and search term.

    Args:
        request: The incoming request object.
        category_id: An optional category ID to filter emails.
        search: An optional search term to filter emails by subject, content, or sender.
        limit: Number of emails to return (default 50)
        offset: Number of emails to skip (for pagination)
        is_unread: Optional flag to filter unread emails
        email_service: The email service dependency.

    Returns:
        A list of emails that match the filtering criteria.

    Raises:
        HTTPException: If a database error occurs or if there's a validation error.
    """
    try:
        if search:
            result = await email_service.search_emails(search, limit)
        else:
            result = await email_service.get_all_emails(limit, offset, category_id, is_unread)

        if result.success:
            return result.data
        else:
            # Handle error case
            raise HTTPException(status_code=500, detail=result.error)
    except HTTPException:
        raise
    except Exception as e:
        log_data = create_log_data(
            message="Unhandled error in get_emails",
            request_url=request.url,
            error_type=type(e).__name__,
            error_detail=str(e),
        )
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Failed to fetch emails due to an unexpected error.")


@router.get("/api/emails/{email_id}", response_model=EmailResponse)  # Changed to EmailResponse
@log_performance(operation="get_email")
async def get_email(
    request: Request, email_id: int, email_service: EmailService = Depends(get_email_service)
):
    """
    Retrieves a specific email by its unique ID.

    Args:
        request: The incoming request object.
        email_id: The ID of the email to retrieve.
        email_service: The email service dependency.

    Returns:
        The email object if found.

    Raises:
        HTTPException: If the email is not found, or if a database or validation error occurs.
    """
    try:
        result = await email_service.get_email_by_id(email_id)
        if result.success:
            return EmailResponse(**result.data)
        else:
            # Raise appropriate exception if not found
            raise EmailNotFoundException(email_id=email_id)
    except EmailNotFoundException:
        raise
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
    email_service: EmailService = Depends(get_email_service),
    workflow_engine: WorkflowEngine = Depends(get_workflow_engine),
):
    """Create new email with AI analysis using the active workflow."""
    try:
        # Run the default workflow to process the email data
        # TODO: Implement proper workflow selection
        from backend.node_engine.workflow_manager import workflow_manager

        default_workflow = workflow_manager.create_sample_workflow()
        execution_context = await workflow_engine.execute_workflow(
            default_workflow, {"email_data": email.model_dump()}
        )
        processed_data = execution_context.outputs.get("processed_email", email.model_dump())

        # Add email through service layer
        result = await email_service.create_email(processed_data)

        if result.success:
            return EmailResponse(**result.data)
        else:
            # Handle error case
            raise HTTPException(status_code=500, detail=result.error)
    except Exception as e:
        log_data = create_log_data(
            message="Unhandled error in create_email",
            request_url=request.url,
            error_type=type(e).__name__,
            error_detail=str(e),
        )
        logger.error(json.dumps(log_data))
        raise AIAnalysisError(detail="Failed to create email due to an unexpected error.")


@router.put("/api/emails/{email_id}", response_model=EmailResponse)  # Changed to EmailResponse
@log_performance(operation="update_email")
async def update_email(
    request: Request,
    email_id: int,
    email_update: EmailUpdate,
    email_service: EmailService = Depends(get_email_service),
):
    """
    Updates an existing email by its ID.

    Args:
        request: The incoming request object.
        email_id: The ID of the email to update.
        email_update: The email data to update.
        email_service: The email service dependency.

    Returns:
        The updated email object.

    Raises:
        HTTPException: If the email is not found, or if a database or validation error occurs.
    """
    try:
        # Convert EmailUpdate to dict for service layer, excluding unset values
        update_data = email_update.model_dump(exclude_unset=True)

        result = await email_service.update_email(email_id, update_data)

        if result.success:
            return EmailResponse(**result.data)
        else:
            # Raise appropriate exception if not found
            raise EmailNotFoundException(email_id=email_id)
    except EmailNotFoundException:
        raise
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
