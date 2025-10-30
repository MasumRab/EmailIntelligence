"""
Error handling middleware and utilities for the Email Intelligence Platform.
Provides consistent error responses and logging.
"""

import logging
import uuid
from typing import Callable, Awaitable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from .exceptions import BaseAppException, APIError


logger = logging.getLogger(__name__)


def generate_request_id():
    """Generate a unique request ID for tracking purposes."""
    return str(uuid.uuid4())


def log_error(request: Request, exc: Exception, request_id: str = None):
    """Log error with context for debugging."""
    logger.error(
        "Error occurred",
        extra={
            "request_id": request_id,
            "url": str(request.url),
            "method": request.method,
            "headers": dict(request.headers),
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        },
    )


async def app_exception_handler(request: Request, exc: BaseAppException):
    """
    Global handler for custom application exceptions.
    Returns consistent error responses.
    """
    request_id = request.headers.get("X-Request-ID") or generate_request_id()
    
    # Log the error with context
    log_error(request, exc, request_id)
    
    # Return consistent error response
    return JSONResponse(
        status_code=exc.status_code,
        content={
            **exc.detail,
            "request_id": request_id
        }
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    """
    Global handler for validation errors.
    Returns consistent 422 validation error responses.
    """
    request_id = request.headers.get("X-Request-ID") or generate_request_id()
    
    # Log the error with context
    log_error(request, exc, request_id)
    
    # Format validation errors for consistent response
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error['loc']),
            "message": error['msg'],
            "type": error['type']
        })
    
    error_response = {
        "success": False,
        "message": "Validation failed",
        "error_code": "VALIDATION_ERROR",
        "details": errors,
        "request_id": request_id
    }
    
    return JSONResponse(
        status_code=422,
        content=error_response
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Global handler for unexpected errors.
    Returns consistent error responses and logs appropriately.
    """
    request_id = request.headers.get("X-Request-ID") or generate_request_id()
    
    # Log the error with context
    log_error(request, exc, request_id)
    
    # For security, don't expose internal error details to the client
    error_response = {
        "success": False,
        "message": "An unexpected error occurred",
        "error_code": "INTERNAL_ERROR",
        "details": "Please contact support if the problem persists",
        "request_id": request_id
    }
    
    # Return 500 for internal server errors
    return JSONResponse(
        status_code=500,
        content=error_response
    )


def add_error_handlers(app):
    """
    Add standardized error handlers to the FastAPI application.
    """
    app.add_exception_handler(BaseAppException, app_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)