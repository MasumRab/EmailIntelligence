"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Version 1 API routes for category operations
Following the new architectural patterns with service layer and API versioning
"""
from typing import List
import logging
from fastapi import APIRouter, Depends, Request

from backend.python_backend.models import CategoryResponse, CategoryCreate
from backend.python_backend.services.category_service import CategoryService
from backend.python_backend.dependencies import get_category_service
from backend.python_backend.performance_monitor import log_performance

logger = logging.getLogger(__name__)

# Create router with API version prefix
router = APIRouter(prefix="/v1")

@router.get("/categories", response_model=List[CategoryResponse])
@log_performance(operation="get_categories_v1")
async def get_categories_v1(
    request: Request,
    category_service: CategoryService = Depends(get_category_service)
):
    """
    Retrieves a list of all categories.

    Args:
        request: The incoming request object.
        category_service: Category service dependency.

    Returns:
        A list of all categories.
    """
    result = await category_service.get_all_categories()
    
    if result.success:
        # For this endpoint, we return the list directly rather than wrapping in BaseResponse
        # since the response model is List[CategoryResponse]
        return result.data
    else:
        # Handle error case - in a complete implementation, we'd have specific error handling
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=result.error)


@router.post("/categories", response_model=CategoryResponse)
@log_performance(operation="create_category_v1")
async def create_category_v1(
    request: Request,
    category: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service)
):
    """
    Create a new category.

    Args:
        request: The incoming request object.
        category: The category data to create.
        category_service: Category service dependency.

    Returns:
        The created category object.
    """
    # Convert CategoryCreate to dict for service layer
    category_data = category.model_dump()
    
    result = await category_service.create_category(category_data)
    
    if result.success:
        # Create a successful response
        from pydantic import BaseModel
        # Since CategoryResponse would be the proper model, 
        # for now we'll use the returned data directly
        return result.data
    else:
        # Handle error case
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=result.error)