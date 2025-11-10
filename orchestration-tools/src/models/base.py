"""Base model for all data structures."""

from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel as PydanticBaseModel, Field


class BaseModel(PydanticBaseModel):
    """Base Pydantic model with common fields and configuration."""

    id: Optional[str] = Field(default=None, description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
        validate_assignment = True
        use_enum_values = True
