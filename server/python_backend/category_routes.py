import json
import logging
from typing import List

import psycopg2
from fastapi import APIRouter, Depends, HTTPException, Request

from .database import DatabaseManager, get_db
from .models import CategoryCreate, CategoryResponse  # Added CategoryResponse, changed from .main
from .performance_monitor import PerformanceMonitor

logger = logging.getLogger(__name__)
router = APIRouter()
performance_monitor = PerformanceMonitor()  # Initialize performance monitor


@router.get("/api/categories", response_model=List[CategoryResponse])
@performance_monitor.track
async def get_categories(request: Request, db: DatabaseManager = Depends(get_db)):
    """Get all categories"""
    try:
        categories = await db.get_all_categories()
        return [CategoryResponse(**cat) for cat in categories]
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


@router.post("/api/categories", response_model=CategoryResponse)  # Changed to CategoryResponse
@performance_monitor.track
async def create_category(
    request: Request, category: CategoryCreate, db: DatabaseManager = Depends(get_db)
):
    """Create new category"""
    try:
        created_category_dict = await db.create_category(
            category.dict()
        )  # db.create_category returns a dict
        return CategoryResponse(**created_category_dict)  # Ensure it returns CategoryResponse
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
