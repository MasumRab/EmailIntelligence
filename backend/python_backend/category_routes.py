import json
import logging
from typing import List

import psycopg2
from fastapi import APIRouter, Depends, HTTPException, Request

from .database import DatabaseManager, get_db
from .models import CategoryCreate, CategoryResponse  # Added CategoryResponse, changed from .main
# from .performance_monitor import PerformanceMonitor # Removed

logger = logging.getLogger(__name__)
router = APIRouter()
# performance_monitor = PerformanceMonitor() # Removed


@router.get("/api/categories", response_model=List[CategoryResponse])
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
    except psycopg2.Error as db_err:
        log_data = {
            "message": "Database operation failed while fetching categories",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
            "pgcode": db_err.pgcode if hasattr(db_err, "pgcode") else None,
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=503, detail="Database service unavailable.")
    except Exception as e:
        log_data = {
            "message": "Unhandled error in get_categories",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to fetch categories")


@router.post("/api/categories", response_model=CategoryResponse)
async def create_category(
    request: Request, category: CategoryCreate, db: DatabaseManager = Depends(get_db)
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
    except psycopg2.Error as db_err:
        log_data = {
            "message": "Database operation failed while creating category",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
            "pgcode": db_err.pgcode if hasattr(db_err, "pgcode") else None,
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=503, detail="Database service unavailable.")
    except Exception as e:
        log_data = {
            "message": "Unhandled error in create_category",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to create category")
