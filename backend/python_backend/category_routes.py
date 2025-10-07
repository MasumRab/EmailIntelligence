import json
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

from .database import DatabaseManager, get_db
from .exceptions import DatabaseError
from .models import CategoryCreate, CategoryResponse  # Added CategoryResponse, changed from .main
from .performance_monitor import log_performance
from .utils import handle_pydantic_validation, create_log_data

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/categories", response_model=List[CategoryResponse])
@log_performance(operation="get_categories")
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
<<<<<<< HEAD
        return await handle_pydantic_validation(categories, CategoryResponse, "get_categories")
    except Exception as db_err:
        log_data = create_log_data(
            message="Database operation failed while fetching categories",
            request_url=request.url,
            error_type=type(db_err).__name__,
            error_detail=str(db_err),
            pgcode=None,
        )
=======
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
>>>>>>> origin/feature/git-history-analysis-report
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Database service unavailable.")
    except Exception as e:
        log_data = create_log_data(
            message="Unhandled error in get_categories",
            request_url=request.url,
            error_type=type(e).__name__,
            error_detail=str(e),
        )
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Failed to fetch categories due to an unexpected error.")


@router.post("/api/categories", response_model=CategoryResponse)  # Changed to CategoryResponse
@log_performance(operation="create_category")
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
<<<<<<< HEAD
        created_category_dict = await db.create_category(
            category.model_dump()
        )  # db.create_category returns a dict
        # Use the utility function to handle Pydantic validation
        validated_categories = await handle_pydantic_validation([created_category_dict], CategoryResponse, "create_category")
        return validated_categories[0]  # Return the single validated category
    except Exception as db_err:
        log_data = create_log_data(
            message="Database operation failed while creating category",
            request_url=request.url,
            error_type=type(db_err).__name__,
            error_detail=str(db_err),
            pgcode=None,
        )
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
    except psycopg2.Error as db_err:
        log_data = {
            "message": "Database operation failed while creating category",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
            "pgcode": db_err.pgcode if hasattr(db_err, "pgcode") else None,
        }
>>>>>>> origin/feature/git-history-analysis-report
        logger.error(json.dumps(log_data))
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