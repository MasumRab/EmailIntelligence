"""
Refactored Version 1 API routes for email operations
Following modern architectural patterns with improved service layer integration
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Request, HTTPException

from ...core.models import EmailResponse, EmailCreate, EmailUpdate
from ...core.services.email_service import EmailService, get_email_service
from ...core.exceptions import EmailNotFoundException, BaseAppException
from ...core.performance_monitor import log_performance

logger = logging.getLogger(__name__)

# Create router with API version prefix
router = APIRouter(prefix="/api/v1")


@router.get("/emails", response_model=List[EmailResponse])
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
        limit: Number of emails to return (default 50, max 1000)
        offset: Number of emails to skip (for pagination)
        category_id: Optional category ID to filter emails
        is_unread: Optional flag to filter unread emails
        search: Optional search term to filter emails by subject, content, or sender
        email_service: Email service dependency.

    Returns:
        A paginated list of emails that match the filtering criteria.

    Raises:
        HTTPException: If there's an error processing the request.
    """
    try:
        if search:
            # Use search functionality if search term is provided
            result = await email_service.search_emails(search, limit)
        else:
            # Use get_all_emails with filters
            result = await email_service.get_all_emails(
                limit=limit, 
                offset=offset, 
                category_id=category_id, 
                is_unread=is_unread
            )

        if result.success:
            return result.data
        else:
            # Handle service error
            raise HTTPException(
                status_code=400 if result.error_code == "INVALID_INPUT" else 500,
                detail=result.error or result.message
            )
            
    except EmailNotFoundException:
        raise HTTPException(status_code=404, detail="Email not found")
    except BaseAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_emails_v1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/emails/{email_id}", response_model=EmailResponse)
@log_performance(operation="get_email_v1")
async def get_email_v1(
    request: Request, 
    email_id: int, 
    email_service: EmailService = Depends(get_email_service)
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
        HTTPException: If the email is not found or there's an error.
    """
    try:
        result = await email_service.get_email_by_id(email_id)

        if result.success:
            return result.data
        else:
            # Handle service error
            if result.error_code == "EMAIL_NOT_FOUND":
                raise HTTPException(status_code=404, detail="Email not found")
            else:
                raise HTTPException(
                    status_code=400 if result.error_code == "INVALID_INPUT" else 500,
                    detail=result.error or result.message
                )
                
    except EmailNotFoundException:
        raise HTTPException(status_code=404, detail="Email not found")
    except BaseAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_email_v1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


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

    Raises:
        HTTPException: If there's an error creating the email.
    """
    try:
        result = await email_service.create_email(email)

        if result.success:
            return result.data
        else:
            # Handle service error
            raise HTTPException(
                status_code=400 if result.error_code == "INVALID_INPUT" else 500,
                detail=result.error or result.message
            )
            
    except BaseAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in create_email_v1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


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
        HTTPException: If the email is not found or there's an error.
    """
    try:
        result = await email_service.update_email(email_id, email_update)

        if result.success:
            return result.data
        else:
            # Handle service error
            if result.error_code == "EMAIL_NOT_FOUND":
                raise HTTPException(status_code=404, detail="Email not found")
            else:
                raise HTTPException(
                    status_code=400 if result.error_code == "INVALID_INPUT" else 500,
                    detail=result.error or result.message
                )
                
    except EmailNotFoundException:
        raise HTTPException(status_code=404, detail="Email not found")
    except BaseAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in update_email_v1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/emails/{email_id}")
@log_performance(operation="delete_email_v1")
async def delete_email_v1(
    request: Request,
    email_id: int,
    email_service: EmailService = Depends(get_email_service),
):
    """
    Deletes an email by its ID.

    Args:
        request: The incoming request object.
        email_id: The ID of the email to delete.
        email_service: Email service dependency.

    Returns:
        A success message.

    Raises:
        HTTPException: If the email is not found or there's an error.
    """
    try:
        result = await email_service.delete_email(email_id)

        if result.success:
            return {"message": result.message}
        else:
            # Handle service error
            if result.error_code == "EMAIL_NOT_FOUND":
                raise HTTPException(status_code=404, detail="Email not found")
            else:
                raise HTTPException(
                    status_code=400 if result.error_code == "INVALID_INPUT" else 500,
                    detail=result.error or result.message
                )
                
    except EmailNotFoundException:
        raise HTTPException(status_code=404, detail="Email not found")
    except BaseAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in delete_email_v1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/emails/search/{search_term}", response_model=List[EmailResponse])
@log_performance(operation="search_emails_v1")
async def search_emails_v1(
    request: Request,
    search_term: str,
    limit: int = 50,
    email_service: EmailService = Depends(get_email_service),
):
    """
    Search emails by term.

    Args:
        request: The incoming request object.
        search_term: Term to search for in emails.
        limit: Maximum number of results to return.
        email_service: Email service dependency.

    Returns:
        A list of emails matching the search term.

    Raises:
        HTTPException: If there's an error processing the request.
    """
    try:
        result = await email_service.search_emails(search_term, limit)

        if result.success:
            return result.data
        else:
            # Handle service error
            raise HTTPException(
                status_code=400 if result.error_code == "INVALID_INPUT" else 500,
                detail=result.error or result.message
            )
            
    except BaseAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in search_emails_v1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/emails/category/{category_id}", response_model=List[EmailResponse])
@log_performance(operation="get_emails_by_category_v1")
async def get_emails_by_category_v1(
    request: Request,
    category_id: int,
    limit: int = 50,
    offset: int = 0,
    email_service: EmailService = Depends(get_email_service),
):
    """
    Get emails by category.

    Args:
        request: The incoming request object.
        category_id: Category ID to filter by.
        limit: Number of emails to return.
        offset: Number of emails to skip.
        email_service: Email service dependency.

    Returns:
        A list of emails in the specified category.

    Raises:
        HTTPException: If there's an error processing the request.
    """
    try:
        result = await email_service.get_emails_by_category(category_id, limit, offset)

        if result.success:
            return result.data
        else:
            # Handle service error
            if result.error_code == "EMAIL_NOT_FOUND":
                raise HTTPException(status_code=404, detail="No emails found for category")
            else:
                raise HTTPException(
                    status_code=400 if result.error_code == "INVALID_INPUT" else 500,
                    detail=result.error or result.message
                )
                
    except BaseAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_emails_by_category_v1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/emails/stats")
@log_performance(operation="get_email_stats_v1")
async def get_email_stats_v1(
    request: Request,
    email_service: EmailService = Depends(get_email_service),
):
    """
    Get email statistics.

    Args:
        request: The incoming request object.
        email_service: Email service dependency.

    Returns:
        Email statistics and analytics.

    Raises:
        HTTPException: If there's an error processing the request.
    """
    try:
        result = await email_service.get_statistics()

        if result.success:
            return result.data
        else:
            # Handle service error
            raise HTTPException(
                status_code=400 if result.error_code == "INVALID_INPUT" else 500,
                detail=result.error or result.message
            )
            
    except BaseAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_email_stats_v1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")