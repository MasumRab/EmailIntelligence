import json
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

from .database import DatabaseManager, get_db
from .dependencies import get_category_service
from .exceptions import DatabaseError
from .models import CategoryCreate, CategoryResponse
from .performance_monitor import log_performance
from .utils import create_log_data, handle_pydantic_validation
from .services.category_service import CategoryService
from src.core.auth import get_current_active_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/categories", response_model=List[CategoryResponse])
@log_performance(operation="get_categories")
async def get_categories(
    request: Request,
    current_user: str = Depends(get_current_active_user),
    db: DatabaseManager = Depends(get_db)
):
    """
    Retrieves all categories from the database.
    
    Requires authentication.
    """
    try:
        categories = await db.get_all_categories()
        return [CategoryResponse(**cat) for cat in categories]
    except Exception as db_err:
        log_data = create_log_data(
            message="Database operation failed while fetching categories",
            request_url=request.url,
            error_type=type(db_err).__name__,
            error_detail=str(db_err),
            pgcode=None,
        )
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Failed to create category.") from db_err


@router.post("/api/categories", response_model=CategoryResponse)
@log_performance(operation="create_category")
async def create_category(
    request: Request,
    category: CategoryCreate,
    current_user: str = Depends(get_current_active_user),
    category_service: CategoryService = Depends(get_category_service),
):
    """
    Creates a new category in the database.

    Args:
        request (Request): The incoming request object.
        category (CategoryCreate): The category data for creation.
        current_user: The authenticated user making the request.
        db (DatabaseManager): The database manager dependency.

    Returns:
        CategoryResponse: The newly created category.

    Raises:
        HTTPException: If there is a database error or any other failure.
    """
    try:
        new_category = await category_service.create_category(category)
        return CategoryResponse(**new_category)
    except Exception as db_err:
        log_data = create_log_data(
            message="Database operation failed while creating category",
            request_url=request.url,
            error_type=type(db_err).__name__,
            error_detail=str(db_err),
            pgcode=None,
        )
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Failed to create category.") from db_err
