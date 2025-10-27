import json
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status

# Updated imports to use the new core framework components
from src.core.data.factory import get_data_source
from src.core.data.data_source import DataSource
from src.core.exceptions import DatabaseError
from src.core.factory import get_data_source
from src.core.models import CategoryCreate, CategoryResponse
from src.core.performance_monitor import log_performance
from src.core.auth import get_current_active_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
@log_performance("get_categories")
async def get_categories(
    request: Request,
    current_user: str = Depends(get_current_active_user),
    db: DataSource = Depends(get_data_source)
):
    """
    Retrieves all categories from the database.
    Requires authentication.
    """
    try:
        categories = await db.get_all_categories()
        return [CategoryResponse(**cat) for cat in categories]
    except Exception as e:
        logger.error(f"Failed to get categories: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch categories")


@router.post("/", response_model=CategoryResponse)
@log_performance("create_category")
async def create_category(
    request: Request,
    category: CategoryCreate,
    current_user: str = Depends(get_current_active_user),
    db: DataSource = Depends(get_data_source)
):
    """
    Creates a new category in the database.
    Requires authentication.
    """
    try:
        created_category_dict = await db.create_category(category.model_dump())
        return CategoryResponse(**created_category_dict)
    except Exception as e:
        logger.error(f"Failed to create category: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create category.")
