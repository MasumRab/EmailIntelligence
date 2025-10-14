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

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/categories", response_model=List[CategoryResponse])
@log_performance(operation="get_categories")
<<<<<<< HEAD
async def get_categories(
    request: Request, 
    category_service: CategoryService = Depends(get_category_service)
):
    """Get all categories"""
    try:
        result = await category_service.get_all_categories()
        if result.success:
            return result.data
        else:
            # Handle error case
            raise HTTPException(status_code=500, detail=result.error)
    except HTTPException:
        raise
=======
async def get_categories(request: Request, db: DatabaseManager = Depends(get_db)):
    """
    Retrieves all categories from the database.

    Args:
        request (Request): The incoming request object.
        db (DatabaseManager): The database manager dependency.

    Returns:
        List[CategoryResponse]: A list of all categories.

    Raises:
        HTTPException: If there is a database error or any other failure.
    """
    try:
        categories = await db.get_all_categories()
        try:
            return [CategoryResponse(**cat) for cat in categories]
        except Exception as e_outer:
            logger.error(
                "Outer exception during get_categories Pydantic validation: "
                f"{type(e_outer)} - {repr(e_outer)}"
            )
            if hasattr(e_outer, "errors"):  # For pydantic.ValidationError
                logger.error(f"Pydantic errors: {e_outer.errors()}")
            raise  # Re-raise for FastAPI to handle
>>>>>>> main
    except Exception as db_err:
        log_data = create_log_data(
            message="Database operation failed while fetching categories",
            request_url=request.url,
            error_type=type(db_err).__name__,
            error_detail=str(db_err),
            pgcode=None,
        )
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Database service unavailable.")


@router.post("/api/categories", response_model=CategoryResponse)
@log_performance(operation="create_category")
async def create_category(
    request: Request, 
    category: CategoryCreate, 
    category_service: CategoryService = Depends(get_category_service)
):
    """
    Creates a new category in the database.

    Args:
        request (Request): The incoming request object.
        category (CategoryCreate): The category data for creation.
        db (DatabaseManager): The database manager dependency.

    Returns:
        CategoryResponse: The newly created category.

    Raises:
        HTTPException: If there is a database error or any other failure.
    """
    try:
<<<<<<< HEAD
        # Add category through service layer
        result = await category_service.create_category(category.model_dump())
        
        if result.success:
            return result.data
        else:
            # Handle error case
            raise HTTPException(status_code=500, detail=result.error)
    except HTTPException:
        raise
=======
        created_category_dict = await db.create_category(category.model_dump())
        try:
            return CategoryResponse(**created_category_dict)
        except Exception as e_outer:
            logger.error(
                "Outer exception during create_category Pydantic validation: "
                f"{type(e_outer)} - {repr(e_outer)}"
            )
            if hasattr(e_outer, "errors"):  # For pydantic.ValidationError
                logger.error(f"Pydantic errors: {e_outer.errors()}")
            raise  # Re-raise for FastAPI to handle
>>>>>>> main
    except Exception as db_err:
        log_data = create_log_data(
            message="Database operation failed while creating category",
            request_url=request.url,
            error_type=type(db_err).__name__,
            error_detail=str(db_err),
            pgcode=None,
        )
        logger.error(json.dumps(log_data))
<<<<<<< HEAD
        raise DatabaseError(detail="Database service unavailable.")
=======
        raise DatabaseError(detail="Database service unavailable.")
    except Exception as e:
        log_data = create_log_data(
            message="Unhandled error in create_category",
            request_url=request.url,
            error_type=type(e).__name__,
            error_detail=str(e),
        )
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Failed to create category due to an unexpected error.")
>>>>>>> main
