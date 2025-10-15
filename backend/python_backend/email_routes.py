import json
import logging
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request

from ..python_nlp.smart_filters import SmartFilterManager  # Corrected import
from .ai_engine import AdvancedAIEngine
from .database import DatabaseManager, get_db
from .dependencies import get_ai_engine, get_filter_manager, get_workflow_engine
from .exceptions import AIAnalysisError, DatabaseError
from .models import EmailResponse  # Changed from .main to .models
from .models import EmailCreate, EmailUpdate
from .performance_monitor import log_performance
from .utils import create_log_data, handle_pydantic_validation
from .workflow_engine import WorkflowEngine

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/emails", response_model=List[EmailResponse])
@log_performance("get_emails")
async def get_emails(
    request: Request,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: DatabaseManager = Depends(get_db),
):
    """
    Retrieves a list of emails, with optional filtering by category and search term.

    Args:
        request: The incoming request object.
        category_id: An optional category ID to filter emails.
        search: An optional search term to filter emails by subject, content, or sender.
        db: The database manager dependency.

    Returns:
        A list of emails that match the filtering criteria.

    Raises:
        HTTPException: If a database error occurs or if there's a validation error.
    """
    try:
        if search and category_id is not None:
            emails = await db.search_emails_by_category(search, category_id)
        elif search:
            emails = await db.search_emails(search)
        elif category_id is not None:
            emails = await db.get_emails_by_category(category_id)
        else:
            emails = await db.get_all_emails()

        return await handle_pydantic_validation(emails, EmailResponse, "get_emails")
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
        log_data = create_log_data(
            message="Unhandled error in get_emails",
            request_url=request.url,
            error_type=type(e).__name__,
            error_detail=str(e),
        )
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Failed to fetch emails due to an unexpected error.")
        raise DatabaseError(detail="Database service unavailable.")
    except Exception as e:
        log_data = {
            "message": "Unhandled error in get_emails",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Failed to fetch emails due to an unexpected error.")


@router.get("/api/emails/{email_id}", response_model=EmailResponse)  # Changed to EmailResponse
@log_performance("get_email")
async def get_email(request: Request, email_id: int, db: DatabaseManager = Depends(get_db)):
    """
    Retrieves a specific email by its unique ID.

    Args:
        request: The incoming request object.
        email_id: The ID of the email to retrieve.
        db: The database manager dependency.

    Returns:
        The email object if found.

    Raises:
        HTTPException: If the email is not found, or if a database or validation error occurs.
    """
    try:
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
    except HTTPException:
        raise
    except Exception as db_err:
        log_data = {
            "message": f"Database operation failed while fetching email id {email_id}",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
            "pgcode": None,
        }
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Database service unavailable.")
    except Exception as e:
        log_data = {
            "message": f"Unhandled error fetching email id {email_id}",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to fetch email")


@router.post("/api/emails", response_model=EmailResponse)  # Changed to EmailResponse
@log_performance("create_email")
async def create_email(
    request: Request,
    email: EmailCreate,
    background_tasks: BackgroundTasks,
    db: DatabaseManager = Depends(get_db),
    workflow_engine: WorkflowEngine = Depends(get_workflow_engine),
):
    """
    Creates a new email by running it through the active workflow.

    The workflow performs AI analysis, applies smart filters, and enriches the email data
    before it's saved to the database.

    Args:
        request: The incoming request object.
        email: The email data for creation.
        background_tasks: FastAPI's background task runner.
        db: The database manager dependency.
        workflow_engine: The workflow engine dependency.

    Returns:
        The newly created and enriched email object.

    Raises:
        HTTPException: If a database error or any other failure occurs.
    """
    try:
        processed_email_data = await workflow_engine.run_workflow(email.model_dump())

        created_email_dict = await db.create_email(processed_email_data)

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
        log_data = {
            "message": "Database operation failed while creating email",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
            "pgcode": None,
        }
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Database service unavailable.")
    except Exception as e:
        log_data = {
            "message": "Unhandled error in create_email",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise AIAnalysisError(detail="Failed to create email due to an unexpected error.")


@router.put("/api/emails/{email_id}", response_model=EmailResponse)  # Changed to EmailResponse
@log_performance("update_email")
async def update_email(
    request: Request,
    email_id: int,
    email_update: EmailUpdate,
    db: DatabaseManager = Depends(get_db),
):
    """
    Updates an existing email by its ID.

    Args:
        request: The incoming request object.
        email_id: The ID of the email to update.
        email_update: The email data to update.
        db: The database manager dependency.

    Returns:
        The updated email object.

    Raises:
        HTTPException: If the email is not found, or if a database or validation error occurs.
    """
    try:
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
    except HTTPException:
        raise
    except Exception as db_err:
        log_data = {
            "message": f"Database operation failed while updating email id {email_id}",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
            "pgcode": None,
        }
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Database service unavailable.")
    except Exception as e:
        log_data = {
            "message": f"Unhandled error updating email id {email_id}",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Failed to update email due to an unexpected error.")
