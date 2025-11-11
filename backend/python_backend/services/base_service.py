<<<<<<< HEAD
"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Base service class for the Email Intelligence Platform
Provides common functionality for all services
"""

from abc import ABC
from typing import Any, Dict, List, Optional, TypeVar, Generic
from pydantic import BaseModel
from src.core.database import get_db
from src.core.settings import settings


class BaseResponse(BaseModel):
    """Base response model for all API responses"""

    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None


class BaseService(ABC):
    """Abstract base class for all services"""

    def __init__(self):
        self.settings = settings
        self._db = None

    async def get_db(self):
        """Get database instance"""
        if self._db is None:
            self._db = await get_db()
        return self._db

    async def handle_error(self, error: Exception, operation: str = "unknown") -> BaseResponse:
        """Handle errors consistently across services"""
        error_msg = f"Error in {operation}: {str(error)}"
        return BaseResponse(success=False, message="An error occurred", error=error_msg)


# Generic type for model operations
ModelType = TypeVar("ModelType", bound=BaseModel)
=======
>>>>>>> main
