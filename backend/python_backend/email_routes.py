import json
import logging
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request

from .dependencies import get_email_service, get_workflow_engine
from .exceptions import DatabaseError, EmailNotFoundException
from .models import EmailCreate, EmailResponse, EmailUpdate
from .performance_monitor import log_performance
from .services.email_service import EmailService
from .utils import create_log_data
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
    email_service: EmailService = Depends(get_email_service),
):
    """
    Retrieves a list of emails, with optional filtering by category and search term.
    """
    try:
        if search:
            result = await email_service.search_emails(search, limit)
        else:
            result = await email_service.get_all_emails(limit, offset, category_id, is_unread)

        if result.success:
            return result.data
        else:
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


@router.get("/api/emails/{email_id}", response_model=EmailResponse)
@log_performance(operation="get_email")
async def get_email(
    request: Request, 
    email_id: int, 
    email_service: EmailService = Depends(get_email_service)
):
    """
    Retrieves a specific email by its unique ID.
    """
    try:
        result = await email_service.get_email_by_id(email_id)
        if result.success and result.data:
            return EmailResponse(**result.data)
        else:
            raise EmailNotFoundException(email_id=email_id)
    except EmailNotFoundException:
        raise
    except Exception as e:
        log_data = create_log_data(
            message=f"Unhandled error fetching email id {email_id}",
            request_url=request.url,
            error_type=type(e).__name__,
            error_detail=str(e),
        )
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Failed to fetch email due to an unexpected error.")


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
        processed_data = await workflow_engine.run_workflow(email.model_dump())
        result = await email_service.create_email(processed_data)
        
        if result.success and result.data:
            return EmailResponse(**result.data)
        else:
            raise HTTPException(status_code=500, detail=result.error)
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
    email_service: EmailService = Depends(get_email_service),
):
    """
    Updates an existing email by its ID.
    """
    try:
        update_data = email_update.model_dump(exclude_unset=True)
        result = await email_service.update_email(email_id, update_data)
        
        if result.success and result.data:
            return EmailResponse(**result.data)
        else:
            raise EmailNotFoundException(email_id=email_id)
    except EmailNotFoundException:
        raise
    except Exception as e:
        log_data = create_log_data(
            message=f"Unhandled error updating email id {email_id}",
            request_url=request.url,
            error_type=type(e).__name__,
            error_detail=str(e),
        )
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Failed to update email due to an unexpected error.")
