import json
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

# Updated imports to use the new core framework components
from src.core.data_source import DataSource
from src.core.database import DatabaseManager
from src.core.exceptions import DatabaseError
from src.core.factory import get_data_source
from src.core.models import CategoryCreate, CategoryResponse
from backend.python_backend.performance_monitor import log_performance

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
@log_performance("get_categories")
async def get_categories(request: Request, db: DataSource = Depends(get_data_source)):
    """
    Retrieves all categories from the database.
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
    request: Request, category: CategoryCreate, db: DataSource = Depends(get_data_source)
):
    """
    Creates a new category in the database.
    """
    try:
        created_category_coro = db.create_category(category.model_dump())
        created_category_dict = await created_category_coro
        return CategoryResponse(**created_category_dict)
    except Exception as e:
        logger.error(f"Failed to create category: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create category.")
