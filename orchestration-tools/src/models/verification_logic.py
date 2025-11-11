from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class VerificationLogic(BaseModel):
    """
    Represents verification logic that is subject to formal verification
    """
    id: str  # Unique identifier for the verification logic
    name: str  # Name of the verification logic
    description: str  # Description of the verification logic
    verification_type: str  # Type of verification logic (context, dependency, etc.)
    implementation_path: str  # Path to the implementation for verification
    last_verified_at: Optional[datetime] = None  # Time of last formal verification
    verification_results: Optional[dict] = None  # Results of formal verification
    coverage_percentage: float = 0.0  # Coverage percentage from formal verification
    created_at: datetime = datetime.now()  # Time when verification logic was defined
    updated_at: datetime = datetime.now()  # Time when verification logic was last updated