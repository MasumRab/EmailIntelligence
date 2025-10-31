import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from src.core.auth import get_current_active_user
from src.core.data_source import DataSource
from src.core.database import DatabaseManager
from src.core.exceptions import DatabaseError, GmailServiceError
from src.core.factory import get_data_source
from src.core.models import (
    EmailCreate,
    EmailResponse,
    EmailUpdate,
)
from backend.python_backend.performance_monitor import log_performance

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[EmailResponse])
@log_performance
async def get_emails(
current_user: str = Depends(get_current_active_user),
db: DataSource = Depends(get_data_source),
category_id: int = Query(None),
    search: str = Query(None),
    limit: int = Query(50),
    offset: int = Query(0),
):
    """
    Retrieve all emails, optionally filtered by category or search query.
    """
    try:
        if search and category_id is not None:
            emails = await db.search_emails_by_category(search, category_id, limit, offset)
        elif search:
            emails = await db.search_emails(search, limit)
        elif category_id is not None:
            emails = await db.get_emails_by_category(category_id, limit, offset)
        else:
            emails = await db.get_all_emails(limit, offset)
        return emails
    except DatabaseError as e:
        logger.error(f"Database error while fetching emails: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error occurred.")


@router.get("/{email_id}", response_model=EmailResponse)
@log_performance
async def get_email(email_id: int, current_user: str = Depends(get_current_active_user), db: DataSource = Depends(get_data_source)):
    """
    Retrieve a single email by its ID.
    """
    try:
        email = await db.get_email_by_id(email_id)
        if email:
            return email
        raise HTTPException(status_code=404, detail="Email not found")
    except DatabaseError as e:
        logger.error(f"Database error while fetching email {email_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error occurred.")


@router.post("/", response_model=EmailResponse)
@log_performance
async def create_email(email: EmailCreate, current_user: str = Depends(get_current_active_user), db: DataSource = Depends(get_data_source)):
    """
    Create a new email.
    """
    try:
        email_data = email.model_dump()
        created_email = await db.create_email(email_data)
        return created_email
    except DatabaseError as e:
        logger.error(f"Database error while creating email: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error occurred.")


@router.put("/{email_id}", response_model=EmailResponse)
@log_performance
async def update_email(
email_id: int, email_update: EmailUpdate, current_user: str = Depends(get_current_active_user), db: DataSource = Depends(get_data_source)
):
    """
    Update an existing email.
    """
    try:
        updated_email = await db.update_email(email_id, email_update.model_dump())
        if updated_email:
            return updated_email
        raise HTTPException(status_code=404, detail="Email not found")
    except DatabaseError as e:
        logger.error(f"Database error while updating email {email_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error occurred.")
