from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TokenUsage(BaseModel):
    """
    Represents token usage metrics in the tools framework
    """
    id: str  # Unique identifier for the token usage record
    component: str  # Component that used the tokens
    operation: str  # Operation that consumed the tokens
    tokens_used: int  # Number of tokens used
    tokens_allowed: int  # Number of tokens allowed for this operation
    timestamp: datetime = datetime.now()  # Time when usage was recorded
    correlation_id: Optional[str] = None  # Correlation ID for structured logging