from typing import Optional
from pydantic import BaseModel


class VerificationCheck(BaseModel):
    """
    Represents a specific verification check that can be performed
    """
    name: str  # Name of the verification check
    description: str  # Description of what the check does
    category: str  # Category of check (context, dependency, compatibility, etc.)
    required: bool = True  # Whether this check is required or optional
    timeout: int = 300  # Maximum time allowed for this check (in seconds)
    config: Optional[dict] = None  # Configuration parameters for the check