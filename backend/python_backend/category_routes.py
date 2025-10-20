import json
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

from .dependencies import get_category_service
from .exceptions import DatabaseError
from .models import CategoryCreate, CategoryResponse
from .performance_monitor import log_performance
from .services.category_service import CategoryService
from .utils import create_log_data

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/categories", response_model=List[CategoryResponse])
@log_performance(operation="get_categories")
async def get_categories(
    request: Request, 
    category_service: CategoryService = Depends(get_category_service)
):
    """
    Retrieves all categories using the category service.
    """
    try:
        result = await category_service.get_all_categories()
        if result.success:
            return result.data
        else:
            raise HTTPException(status_code=500, detail=result.error)
    except HTTPException:
        raise  # Re-raise HTTPException to let FastAPI handle it
    except Exception as e:
        log_data = create_log_data(
            message="Unhandled error fetching categories",
            request_url=request.url,
            error_type=type(e).__name__,
            error_detail=str(e),
        )
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Failed to fetch categories due to an unexpected error.")


@router.post("/api/categories", response_model=CategoryResponse)
@log_performance(operation="create_category")
async def create_category(
    request: Request, 
    category: CategoryCreate, 
    category_service: CategoryService = Depends(get_category_service)
):
    """
    Creates a new category using the category service.
    """
    try:
        result = await category_service.create_category(category.model_dump())
        
        if result.success:
            return result.data
        else:
            # Handle potential validation or other creation errors from the service
            if "already exists" in result.error:
                raise HTTPException(status_code=409, detail=result.error) # Conflict
            raise HTTPException(status_code=500, detail=result.error)
    except HTTPException:
        raise # Re-raise HTTPException
    except Exception as e:
        log_data = create_log_data(
            message="Unhandled error in create_category",
            request_url=request.url,
            error_type=type(e).__name__,
            error_detail=str(e),
        )
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Failed to create category due to an unexpected error.")
