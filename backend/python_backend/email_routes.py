import json
import logging
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request

from ..python_nlp.smart_filters import SmartFilterManager  # Corrected import
from .ai_engine import AdvancedAIEngine
from .database import DatabaseManager, get_db
from .dependencies import get_ai_engine, get_filter_manager, get_workflow_engine, get_email_service
from .workflow_engine import WorkflowEngine
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
<<<<<<< HEAD
        limit: Number of emails to return (default 50)
        offset: Number of emails to skip (for pagination)
        is_unread: Optional flag to filter unread emails
        email_service: The email service dependency.
=======
        db: The database manager dependency.
>>>>>>> main

    Returns:
        A list of emails that match the filtering criteria.

    Raises:
        HTTPException: If a database error occurs or if there's a validation error.
    """
    try:
        if search:
            result = await email_service.search_emails(search, limit)
        else:
<<<<<<< HEAD
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
=======
            emails = await db.get_all_emails()
        try:
            return [EmailResponse(**email) for email in emails]
        except Exception as e_outer:
            logger.error(
                "Outer exception during get_emails Pydantic validation: "
                f"{type(e_outer)} - {repr(e_outer)}"
            )
            if hasattr(e_outer, "errors"):  # For pydantic.ValidationError
                logger.error(f"Pydantic errors: {e_outer.errors()}")
            raise  # Re-raise for FastAPI to handle
    except Exception as db_err:
        log_data = create_log_data(
            message="Database operation failed while fetching emails",
            request_url=request.url,
            error_type=type(db_err).__name__,
            error_detail=str(db_err),
            pgcode=None,
        )
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Database service unavailable.")
    except Exception as e:
        log_data = {
            "message": "Unhandled error in get_emails",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to fetch emails")
>>>>>>> main


@router.get("/api/emails/{email_id}", response_model=EmailResponse)  # Changed to EmailResponse
@log_performance(operation="get_email")
<<<<<<< HEAD
async def get_email(
    request: Request, 
    email_id: int, 
    email_service: EmailService = Depends(get_email_service)
):
=======
async def get_email(request: Request, email_id: int, db: DatabaseManager = Depends(get_db)):
>>>>>>> main
    """
    Retrieves a specific email by its unique ID.

    Args:
        request: The incoming request object.
        email_id: The ID of the email to retrieve.
<<<<<<< HEAD
        email_service: The email service dependency.
=======
        db: The database manager dependency.
>>>>>>> main

    Returns:
        The email object if found.

    Raises:
        HTTPException: If the email is not found, or if a database or validation error occurs.
    """
    try:
<<<<<<< HEAD
        result = await email_service.get_email_by_id(email_id)
        if result.success:
            return EmailResponse(**result.data)
        else:
            # Raise appropriate exception if not found
            raise EmailNotFoundException(email_id=email_id)
    except EmailNotFoundException:
        raise
=======
        email = await db.get_email_by_id(email_id)
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        try:
            return EmailResponse(**email)
        except Exception as e_outer:
            logger.error(
                "Outer exception during get_email Pydantic validation: "
                f"{type(e_outer)} - {repr(e_outer)}"
            )
            if hasattr(e_outer, "errors"):  # For pydantic.ValidationError
                logger.error(f"Pydantic errors: {e_outer.errors()}")
            raise  # Re-raise for FastAPI to handle
>>>>>>> main
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
        # Run the active workflow to process the email data
        processed_data = await workflow_engine.run_workflow(email.model_dump())
<<<<<<< HEAD
        
        # Add email through service layer
        result = await email_service.create_email(processed_data)
        
        if result.success:
            return EmailResponse(**result.data)
        else:
            # Handle error case
            raise HTTPException(status_code=500, detail=result.error)
=======

        # Create the email in the database with the processed data
        created_email_dict = await db.create_email(processed_data)

        try:
            return EmailResponse(**created_email_dict)
        except Exception as e_outer:
            logger.error(
                "Outer exception during create_email Pydantic validation: "
                f"{type(e_outer)} - {repr(e_outer)}"
            )
            if hasattr(e_outer, "errors"):  # For pydantic.ValidationError
                logger.error(f"Pydantic errors: {e_outer.errors()}")
            raise  # Re-raise for FastAPI to handle
    except Exception as db_err:
        log_data = create_log_data(
            message="Database operation failed while creating email",
            request_url=request.url,
            error_type=type(db_err).__name__,
            error_detail=str(db_err),
            pgcode=None,
        )
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Database service unavailable.")
>>>>>>> main
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
    email_service: EmailService = Depends(get_email_service),
):
    """
    Updates an existing email by its ID.

    Args:
        request: The incoming request object.
        email_id: The ID of the email to update.
        email_update: The email data to update.
<<<<<<< HEAD
        email_service: The email service dependency.
=======
        db: The database manager dependency.
>>>>>>> main

    Returns:
        The updated email object.

    Raises:
        HTTPException: If the email is not found, or if a database or validation error occurs.
    """
    try:
<<<<<<< HEAD
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
=======
        updated_email_dict = await db.update_email(
            email_id, email_update.model_dump(exclude_unset=True)
        )
        if not updated_email_dict:
            raise HTTPException(status_code=404, detail="Email not found")
        try:
            return EmailResponse(**updated_email_dict)
        except Exception as e_outer:
            logger.error(
                "Outer exception during update_email Pydantic validation: "
                f"{type(e_outer)} - {repr(e_outer)}"
            )
            if hasattr(e_outer, "errors"):  # For pydantic.ValidationError
                logger.error(f"Pydantic errors: {e_outer.errors()}")
            raise  # Re-raise for FastAPI to handle
>>>>>>> main
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
