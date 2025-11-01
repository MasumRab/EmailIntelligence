"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Version 1 API routes for email operations
Following the new architectural patterns with service layer and API versioning
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Request

from backend.python_backend.dependencies import get_email_service
from backend.python_backend.exceptions import EmailNotFoundException
from backend.python_backend.models import EmailCreate, EmailResponse, EmailUpdate
from backend.python_backend.performance_monitor import log_performance
from backend.python_backend.services.email_service import EmailService

logger = logging.getLogger(__name__)

# Create router with API version prefix
router = APIRouter(prefix="/v1")


@router.get("/emails", response_model=EmailResponse)
@log_performance(operation="get_emails_v1")
async def get_emails_v1(
    request: Request,
    limit: int = 50,
    offset: int = 0,
    category_id: Optional[int] = None,
    is_unread: Optional[bool] = None,
    search: Optional[str] = None,
    email_service: EmailService = Depends(get_email_service),
):
    """
    Retrieves a list of emails with optional filtering, pagination, and search.

    Args:
        request: The incoming request object.
        limit: Number of emails to return (default 50)
        offset: Number of emails to skip (for pagination)
        category_id: Optional category ID to filter emails
        is_unread: Optional flag to filter unread emails
        search: Optional search term to filter emails by subject, content, or sender
        email_service: Email service dependency.

    Returns:
        A paginated list of emails that match the filtering criteria.
    """
    if search:
        # Use search functionality if search term is provided
        result = await email_service.search_emails(search, limit)
    else:
        # Use get_all_emails with filters
        result = await email_service.get_all_emails(limit, offset, category_id, is_unread)

    if result.success:
        return result
    else:
        # If there was an error, return the error response
        raise EmailNotFoundException(message_id=None, email_id=None)  # This is just a placeholder


@router.get("/emails/{email_id}", response_model=EmailResponse)
@log_performance(operation="get_email_v1")
async def get_email_v1(
    request: Request, email_id: int, email_service: EmailService = Depends(get_email_service)
):
    """
    Retrieves a specific email by its unique ID.

    Args:
        request: The incoming request object.
        email_id: The ID of the email to retrieve.
        email_service: Email service dependency.

    Returns:
        The email object if found.

    Raises:
        EmailNotFoundException: If the email is not found.
    """
    result = await email_service.get_email_by_id(email_id)

    if result.success:
        # Create a successful response using BaseResponse structure
        response = EmailResponse(**result.data)
        return response
    else:
        # Raise appropriate exception if not found
        raise EmailNotFoundException(email_id=email_id)


@router.post("/emails", response_model=EmailResponse)
@log_performance(operation="create_email_v1")
async def create_email_v1(
    request: Request,
    email: EmailCreate,
    background_tasks: BackgroundTasks,
    email_service: EmailService = Depends(get_email_service),
):
    """
    Create a new email.

    Args:
        request: The incoming request object.
        email: The email data to create.
        background_tasks: FastAPI background tasks.
        email_service: Email service dependency.

    Returns:
        The created email object.
    """
    # Convert EmailCreate to dict for service layer
    email_data = email.model_dump()

    result = await email_service.create_email(email_data)

    if result.success:
        # Create a successful response using BaseResponse structure
        response = EmailResponse(**result.data)
        return response
    else:
        # Handle error case - in a complete implementation, we'd have specific error handling
        from fastapi import HTTPException

        raise HTTPException(status_code=500, detail=result.error)


@router.put("/emails/{email_id}", response_model=EmailResponse)
@log_performance(operation="update_email_v1")
async def update_email_v1(
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
        email_service: Email service dependency.

    Returns:
        The updated email object.

    Raises:
        EmailNotFoundException: If the email is not found.
    """
    # Convert EmailUpdate to dict for service layer, excluding unset values
    update_data = email_update.model_dump(exclude_unset=True)

    result = await email_service.update_email(email_id, update_data)

    if result.success:
        # Create a successful response using BaseResponse structure
        response = EmailResponse(**result.data)
        return response
    else:
        # Raise appropriate exception if not found
        raise EmailNotFoundException(email_id=email_id)
