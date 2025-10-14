import json
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

# Updated imports to use the new core framework components
from src.core.data.factory import get_data_source
from src.core.data.data_source import DataSource
from src.core.exceptions import DatabaseError
from src.core.performance_monitor import log_performance
from src.core.models import CategoryCreate, CategoryResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/categories", response_model=List[CategoryResponse])
@log_performance("get_categories")
async def get_categories(request: Request, data_source: DataSource = Depends(get_data_source)):
    """
    Retrieves all categories from the data source.
    """
    try:
        categories = await data_source.get_all_categories()
        return [CategoryResponse(**cat) for cat in categories]
    except Exception as e:
        logger.error(f"Failed to get categories: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve categories.")


@router.post("/api/categories", response_model=CategoryResponse)
@log_performance("create_category")
async def create_category(
    request: Request, category: CategoryCreate, data_source: DataSource = Depends(get_data_source)
):
    """
    Creates a new category in the data source.
    """
    try:
        created_category_dict = await data_source.create_category(category.model_dump())
        return CategoryResponse(**created_category_dict)
    except Exception as e:
        logger.error(f"Failed to create category: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create category.")
