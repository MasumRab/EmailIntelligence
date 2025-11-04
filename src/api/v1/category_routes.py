"""
Refactored Version 1 API routes for category operations
Following modern architectural patterns with improved service layer integration
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Request, HTTPException

from ...core.models import CategoryResponse, CategoryCreate, CategoryUpdate
from ...core.services.category_service import CategoryService, get_category_service
from ...core.exceptions import CategoryNotFoundException, BaseAppException
from ...core.performance_monitor import log_performance

logger = logging.getLogger(__name__)

# Create router with API version prefix
router = APIRouter(prefix="/api/v1")


@router.get("/categories", response_model=List[CategoryResponse])
@log_performance(operation="get_categories_v1")
async def get_categories_v1(
    request: Request,
    sort_by: str = "name",
    sort_order: str = "asc",
    category_service: CategoryService = Depends(get_category_service),
):
    """
    Retrieves a list of all categories with sorting options.

    Args:
        request: The incoming request object.
        sort_by: Field to sort by (name, count)
        sort_order: Sort order (asc or desc)
        category_service: Category service dependency.

    Returns:
        A list of all categories.

    Raises:
        HTTPException: If there's an error processing the request.
    """
    try:
        result = await category_service.get_all_categories(sort_by=sort_by, sort_order=sort_order)

        if result.success:
            return result.data
        else:
            # Handle service error
            raise HTTPException(
                status_code=400 if result.error_code == "INVALID_INPUT" else 500,
                detail=result.error or result.message
            )
            
    except BaseAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_categories_v1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/categories/{category_id}", response_model=CategoryResponse)
@log_performance(operation="get_category_v1")
async def get_category_v1(
    request: Request,
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
):
    """
    Retrieves a specific category by its unique ID.

    Args:
        request: The incoming request object.
        category_id: The ID of the category to retrieve.
        category_service: Category service dependency.

    Returns:
        The category object if found.

    Raises:
        HTTPException: If the category is not found or there's an error.
    """
    try:
        result = await category_service.get_category_by_id(category_id)

        if result.success:
            return result.data
        else:
            # Handle service error
            if result.error_code == "CATEGORY_NOT_FOUND":
                raise HTTPException(status_code=404, detail="Category not found")
            else:
                raise HTTPException(
                    status_code=400 if result.error_code == "INVALID_INPUT" else 500,
                    detail=result.error or result.message
                )
                
    except CategoryNotFoundException:
        raise HTTPException(status_code=404, detail="Category not found")
    except BaseAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_category_v1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/categories", response_model=CategoryResponse)
@log_performance(operation="create_category_v1")
async def create_category_v1(
    request: Request,
    category: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service),
):
    """
    Create a new category.

    Args:
        request: The incoming request object.
        category: The category data to create.
        category_service: Category service dependency.

    Returns:
        The created category object.

    Raises:
        HTTPException: If there's an error creating the category.
    """
    try:
        result = await category_service.create_category(category)

        if result.success:
            return result.data
        else:
            # Handle service error
            raise HTTPException(
                status_code=400 if result.error_code == "INVALID_INPUT" else 500,
                detail=result.error or result.message
            )
            
    except BaseAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in create_category_v1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/categories/{category_id}", response_model=CategoryResponse)
@log_performance(operation="update_category_v1")
async def update_category_v1(
    request: Request,
    category_id: int,
    category_update: CategoryUpdate,
    category_service: CategoryService = Depends(get_category_service),
):
    """
    Updates an existing category by its ID.

    Args:
        request: The incoming request object.
        category_id: The ID of the category to update.
        category_update: The category data to update.
        category_service: Category service dependency.

    Returns:
        The updated category object.

    Raises:
        HTTPException: If the category is not found or there's an error.
    """
    try:
        result = await category_service.update_category(category_id, category_update)

        if result.success:
            return result.data
        else:
            # Handle service error
            if result.error_code == "CATEGORY_NOT_FOUND":
                raise HTTPException(status_code=404, detail="Category not found")
            else:
                raise HTTPException(
                    status_code=400 if result.error_code == "INVALID_INPUT" else 500,
                    detail=result.error or result.message
                )
                
    except CategoryNotFoundException:
        raise HTTPException(status_code=404, detail="Category not found")
    except BaseAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in update_category_v1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/categories/{category_id}")
@log_performance(operation="delete_category_v1")
async def delete_category_v1(
    request: Request,
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
):
    """
    Deletes a category by its ID.

    Args:
        request: The incoming request object.
        category_id: The ID of the category to delete.
        category_service: Category service dependency.

    Returns:
        A success message.

    Raises:
        HTTPException: If the category is not found or there's an error.
    """
    try:
        result = await category_service.delete_category(category_id)

        if result.success:
            return {"message": result.message}
        else:
            # Handle service error
            if result.error_code == "CATEGORY_NOT_FOUND":
                raise HTTPException(status_code=404, detail="Category not found")
            else:
                raise HTTPException(
                    status_code=400 if result.error_code == "INVALID_INPUT" else 500,
                    detail=result.error or result.message
                )
                
    except CategoryNotFoundException:
        raise HTTPException(status_code=404, detail="Category not found")
    except BaseAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in delete_category_v1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/categories/name/{name}", response_model=CategoryResponse)
@log_performance(operation="get_category_by_name_v1")
async def get_category_by_name_v1(
    request: Request,
    name: str,
    category_service: CategoryService = Depends(get_category_service),
):
    """
    Retrieves a specific category by its name.

    Args:
        request: The incoming request object.
        name: The name of the category to retrieve.
        category_service: Category service dependency.

    Returns:
        The category object if found.

    Raises:
        HTTPException: If the category is not found or there's an error.
    """
    try:
        result = await category_service.get_category_by_name(name)

        if result.success:
            return result.data
        else:
            # Handle service error
            if result.error_code == "CATEGORY_NOT_FOUND":
                raise HTTPException(status_code=404, detail="Category not found")
            else:
                raise HTTPException(
                    status_code=400 if result.error_code == "INVALID_INPUT" else 500,
                    detail=result.error or result.message
                )
                
    except CategoryNotFoundException:
        raise HTTPException(status_code=404, detail="Category not found")
    except BaseAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_category_by_name_v1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/categories/stats")
@log_performance(operation="get_category_stats_v1")
async def get_category_stats_v1(
    request: Request,
    category_service: CategoryService = Depends(get_category_service),
):
    """
    Get category statistics.

    Args:
        request: The incoming request object.
        category_service: Category service dependency.

    Returns:
        Category statistics and analytics.

    Raises:
        HTTPException: If there's an error processing the request.
    """
    try:
        result = await category_service.get_category_statistics()

        if result.success:
            return result.data
        else:
            # Handle service error
            raise HTTPException(
                status_code=400 if result.error_code == "INVALID_INPUT" else 500,
                detail=result.error or result.message
            )
            
    except BaseAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_category_stats_v1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")