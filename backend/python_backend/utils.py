"""
Utility functions to reduce code duplication across the backend.
"""
import json
import logging
from typing import Any, Callable, List

logger = logging.getLogger(__name__)


async def handle_pydantic_validation(items: List[Any], model_class: Any, operation_name: str) -> List[Any]:
    """
    Utility function to handle Pydantic model validation for lists of items.
    
    Args:
        items: List of raw data to convert to Pydantic models
        model_class: Pydantic model class to instantiate
        operation_name: Name of the operation for logging purposes
    
    Returns:
        List of validated Pydantic model instances
    """
    try:
        return [model_class(**item) for item in items]
    except Exception as e_outer:
        logger.error(f"Outer exception during {operation_name} Pydantic validation: {type(e_outer)} - {repr(e_outer)}")
        if hasattr(e_outer, 'errors'):  # For pydantic.ValidationError
            logger.error(f"Pydantic errors: {e_outer.errors()}")
        raise  # Re-raise for FastAPI to handle


def create_log_data(message: str, request_url: str, error_type: str, error_detail: str, **kwargs) -> dict:
    """
    Utility function to create standardized log data across the application.
    
    Args:
        message: Log message
        request_url: URL of the request
        error_type: Type of the error
        error_detail: Detail of the error
        **kwargs: Additional fields to include in log data
    
    Returns:
        Dictionary containing standardized log data
    """
    log_data = {
        "message": message,
        "endpoint": str(request_url),
        "error_type": error_type,
        "error_detail": error_detail,
    }
    log_data.update(kwargs)
    return log_data