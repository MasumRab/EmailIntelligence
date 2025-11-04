"""
Base service class for Email Intelligence Platform
Provides common functionality for all services with improved error handling and logging
"""

import logging
from abc import ABC
from typing import Any, Dict, List, Optional, TypeVar, Generic
from pydantic import BaseModel

from ..database import get_db
from ..settings import settings
from ..exceptions import BaseAppException

logger = logging.getLogger(__name__)


class ServiceResponse(BaseModel):
    """
    Standardized response model for all service operations.
    
    This ensures consistent response format across all services.
    """
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BaseService(ABC):
    """
    Abstract base class for all services with enhanced functionality.
    
    Features:
    - Consistent database access
    - Standardized error handling
    - Configuration access
    - Performance monitoring integration
    - Logging integration
    """
    
    def __init__(self):
        self.settings = settings
        self._db = None
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        
    async def get_db(self):
        """
        Get database instance with lazy initialization.
        
        Returns:
            DatabaseManager instance
        """
        if self._db is None:
            self._db = await get_db()
        return self._db
    
    async def handle_error(
        self, 
        error: Exception, 
        operation: str = "unknown",
        error_code: str = "SERVICE_ERROR"
    ) -> ServiceResponse:
        """
        Handle errors consistently across services with detailed logging.
        
        Args:
            error: The exception that occurred
            operation: The operation that failed
            error_code: Standardized error code
            
        Returns:
            ServiceResponse with error information
        """
        # Log the error with context
        self.logger.error(
            f"Service error in {operation}: {type(error).__name__}: {str(error)}",
            extra={
                "operation": operation,
                "error_type": type(error).__name__,
                "error_message": str(error)
            },
            exc_info=True
        )
        
        # Handle specific exception types
        if isinstance(error, BaseAppException):
            return ServiceResponse(
                success=False,
                message=error.message,
                error=str(error),
                error_code=error.error_code if hasattr(error, 'error_code') else error_code
            )
        
        # Default error handling
        error_msg = f"Error in {operation}: {str(error)}"
        return ServiceResponse(
            success=False,
            message="An error occurred during the operation",
            error=error_msg,
            error_code=error_code
        )
    
    async def handle_success(
        self,
        data: Any = None,
        message: str = "Operation completed successfully",
        metadata: Optional[Dict[str, Any]] = None
    ) -> ServiceResponse:
        """
        Handle successful operations with consistent response format.
        
        Args:
            data: The data to return
            message: Success message
            metadata: Additional metadata
            
        Returns:
            ServiceResponse with success information
        """
        return ServiceResponse(
            success=True,
            message=message,
            data=data,
            metadata=metadata
        )
    
    async def validate_input(self, data: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        Validate input data has required fields.
        
        Args:
            data: Input data dictionary
            required_fields: List of required field names
            
        Returns:
            True if all required fields are present, False otherwise
        """
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            self.logger.warning(f"Missing required fields: {missing_fields}")
            return False
        return True
    
    def sanitize_output(self, data: Any) -> Any:
        """
        Sanitize output data to remove sensitive information.
        
        Args:
            data: Data to sanitize
            
        Returns:
            Sanitized data
        """
        # This is a basic implementation - can be extended as needed
        return data


# Generic type for model operations
ModelType = TypeVar("ModelType", bound=BaseModel)