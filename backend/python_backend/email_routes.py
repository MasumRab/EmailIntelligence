import json
import logging
from typing import List, Optional

import psycopg2
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request

from ..python_nlp.smart_filters import SmartFilterManager  # Corrected import

from .ai_engine import AdvancedAIEngine
from .exceptions import AIAnalysisError, DatabaseError
from .database import DatabaseManager, get_db
from .dependencies import get_ai_engine, get_filter_manager
from .performance_monitor import log_performance
from .models import EmailResponse  # Changed from .main to .models
from .models import EmailCreate, EmailUpdate

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
    """Get emails with optional filtering"""
    try:
        if search and category_id is not None:
            emails = await db.search_emails_by_category(search, category_id)
        elif search:
            emails = await db.search_emails(search)
        elif category_id is not None:
            emails = await db.get_emails_by_category(category_id)
        else:
            emails = await db.get_all_emails()
        try:
            return [EmailResponse(**email) for email in emails]
        except Exception as e_outer:
            logger.error(f"Outer exception during get_emails Pydantic validation: {type(e_outer)} - {repr(e_outer)}")
            if hasattr(e_outer, 'errors'): # For pydantic.ValidationError
                logger.error(f"Pydantic errors: {e_outer.errors()}")
            raise # Re-raise for FastAPI to handle
    except psycopg2.Error as db_err:
        log_data = {
            "message": "Database operation failed while fetching emails",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
            "pgcode": db_err.pgcode if hasattr(db_err, "pgcode") else None,
        }
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Database service unavailable.")
    except Exception as e:
        log_data = {
            "message": "Unhandled error in get_emails",
                    "endpoint": str(request.url),
                    "error_type": type(e).__name__,
                    "error_detail": str(e),
                }
        logger.error(json.dumps(log_data)) # Added logger call
        raise HTTPException(status_code=500, detail="Failed to fetch emails")


@router.get("/api/emails/{email_id}", response_model=EmailResponse)  # Changed to EmailResponse
@log_performance("get_email")
async def get_email(request: Request, email_id: int, db: DatabaseManager = Depends(get_db)):
    """Get specific email by ID"""
    try:
        email = await db.get_email_by_id(email_id)
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        try:
            return EmailResponse(**email)  # Ensure it returns EmailResponse
        except Exception as e_outer:
            logger.error(f"Outer exception during get_email Pydantic validation: {type(e_outer)} - {repr(e_outer)}")
            if hasattr(e_outer, 'errors'): # For pydantic.ValidationError
                logger.error(f"Pydantic errors: {e_outer.errors()}")
            raise # Re-raise for FastAPI to handle
    except HTTPException:
        raise
    except psycopg2.Error as db_err:
        log_data = {
            "message": f"Database operation failed while fetching email id {email_id}",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
            "pgcode": db_err.pgcode if hasattr(db_err, "pgcode") else None,
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
        logger.error(json.dumps(log_data)) # Added logger call
        raise HTTPException(status_code=500, detail="Failed to fetch email")


@router.post("/api/emails", response_model=EmailResponse)  # Changed to EmailResponse
@log_performance("create_email")
async def create_email(
    request: Request,
    email: EmailCreate,
    background_tasks: BackgroundTasks,
    db: DatabaseManager = Depends(get_db),
    ai_engine: AdvancedAIEngine = Depends(get_ai_engine),
    filter_manager: SmartFilterManager = Depends(get_filter_manager),
):
    """Create new email with AI analysis"""
    try:
        # Perform AI analysis, now requires db for category matching
        ai_analysis = await ai_engine.analyze_email(email.subject, email.content, db=db)

        # Apply smart filters
        filter_results = await filter_manager.apply_filters_to_email_data(
            email.model_dump()
        )  # Corrected method name

        # Create email with enhanced data
        email_data = email.model_dump()
        email_data.update(
            {
                "confidence": int(ai_analysis.confidence * 100),
                "categoryId": ai_analysis.category_id,
                "labels": ai_analysis.suggested_labels,
                "analysisMetadata": ai_analysis.to_dict(), # Assuming AIAnalysisResult has to_dict, or use model_dump if Pydantic
            }
        )

        created_email_dict = await db.create_email(email_data)  # db.create_email returns a dict

        try:
            return EmailResponse(**created_email_dict)  # Ensure it returns EmailResponse
        except Exception as e_outer:
            logger.error(f"Outer exception during create_email Pydantic validation: {type(e_outer)} - {repr(e_outer)}")
            if hasattr(e_outer, 'errors'): # For pydantic.ValidationError
                logger.error(f"Pydantic errors: {e_outer.errors()}")
            raise # Re-raise for FastAPI to handle
    except psycopg2.Error as db_err:
        log_data = {
            "message": "Database operation failed while creating email",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
            "pgcode": db_err.pgcode if hasattr(db_err, "pgcode") else None,
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
    """Update email"""
    try:
        updated_email_dict = await db.update_email(
            email_id, email_update.model_dump(exclude_unset=True)
        )  # db.update_email returns a dict
        if not updated_email_dict:
            raise HTTPException(status_code=404, detail="Email not found")
        try:
            return EmailResponse(**updated_email_dict)  # Ensure it returns EmailResponse
        except Exception as e_outer:
            logger.error(f"Outer exception during update_email Pydantic validation: {type(e_outer)} - {repr(e_outer)}")
            if hasattr(e_outer, 'errors'): # For pydantic.ValidationError
                logger.error(f"Pydantic errors: {e_outer.errors()}")
            raise # Re-raise for FastAPI to handle
    except HTTPException:
        raise
    except psycopg2.Error as db_err:
        log_data = {
            "message": f"Database operation failed while updating email id {email_id}",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
            "pgcode": db_err.pgcode if hasattr(db_err, "pgcode") else None,
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