"""Base service class for all orchestration services."""

from abc import ABC
from typing import Any, Optional, TypeVar, Generic
from pydantic import BaseModel

from src.logging import get_logger


logger = get_logger(__name__)


class BaseResponse(BaseModel):
    """Base response model for service operations."""

    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    correlation_id: Optional[str] = None

    class Config:
        """Pydantic configuration."""
        use_enum_values = True


ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseService(ABC, Generic[ModelType]):
    """Abstract base class for all services."""

    def __init__(self, name: str = "BaseService"):
        """Initialize base service."""
        self.name = name
        self.logger = get_logger(f"{__name__}.{name}")

    async def handle_error(
        self,
        error: Exception,
        operation: str = "unknown",
        correlation_id: Optional[str] = None,
    ) -> BaseResponse:
        """Handle errors consistently across services."""
        error_msg = f"Error in {operation}: {str(error)}"
        self.logger.error(
            error_msg,
            operation=operation,
            error_type=type(error).__name__,
            correlation_id=correlation_id,
        )
        return BaseResponse(
            success=False,
            message="An error occurred",
            error=error_msg,
            correlation_id=correlation_id,
        )

    async def handle_success(
        self,
        message: str = "Operation completed successfully",
        data: Optional[Any] = None,
        correlation_id: Optional[str] = None,
    ) -> BaseResponse:
        """Handle successful operations consistently."""
        self.logger.info(message, correlation_id=correlation_id)
        return BaseResponse(
            success=True,
            message=message,
            data=data,
            correlation_id=correlation_id,
        )
