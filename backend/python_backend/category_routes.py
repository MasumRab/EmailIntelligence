import json
import logging
from typing import List

import psycopg2
from fastapi import APIRouter, Depends, HTTPException, Request

from .database import DatabaseManager, get_db
from .exceptions import DatabaseError
from .performance_monitor import log_performance
from .models import CategoryCreate, CategoryResponse  # Added CategoryResponse, changed from .main

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/categories", response_model=List[CategoryResponse])
@log_performance("get_categories")
async def get_categories(request: Request, db: DatabaseManager = Depends(get_db)):
    """Get all categories"""
    try:
        categories = await db.get_all_categories()
        try:
            return [CategoryResponse(**cat) for cat in categories]
        except Exception as e_outer:
            logger.error(f"Outer exception during get_categories Pydantic validation: {type(e_outer)} - {repr(e_outer)}")
            if hasattr(e_outer, 'errors'): # For pydantic.ValidationError
                logger.error(f"Pydantic errors: {e_outer.errors()}")
            raise # Re-raise for FastAPI to handle
    except psycopg2.Error as db_err:
        log_data = {
            "message": "Database operation failed while fetching categories",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
            "pgcode": db_err.pgcode if hasattr(db_err, "pgcode") else None,
        }
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Database service unavailable.")
    except Exception as e:
        log_data = {
            "message": "Unhandled error in get_categories",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Failed to fetch categories due to an unexpected error.")


@router.post("/api/categories", response_model=CategoryResponse)  # Changed to CategoryResponse
@log_performance("create_category")
async def create_category(
    request: Request, category: CategoryCreate, db: DatabaseManager = Depends(get_db)
):
    """Create new category"""
    try:
        created_category_dict = await db.create_category(
            category.model_dump()
        )  # db.create_category returns a dict
        try:
            return CategoryResponse(
                **created_category_dict
            )  # Ensure it returns CategoryResponse
        except Exception as e_outer:
            logger.error(f"Outer exception during create_category Pydantic validation: {type(e_outer)} - {repr(e_outer)}")
            if hasattr(e_outer, 'errors'): # For pydantic.ValidationError
                logger.error(f"Pydantic errors: {e_outer.errors()}")
            raise # Re-raise for FastAPI to handle
    except psycopg2.Error as db_err:
        log_data = {
            "message": "Database operation failed while creating category",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
            "pgcode": db_err.pgcode if hasattr(db_err, "pgcode") else None,
        }
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Database service unavailable.")
    except Exception as e:
        log_data = {
            "message": "Unhandled error in create_category",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Failed to create category due to an unexpected error.")