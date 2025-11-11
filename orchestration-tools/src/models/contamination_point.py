from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class ContaminationPoint(BaseModel):
    """
    Represents a potential contamination point in the tools framework
    """
    id: str  # Unique identifier for the contamination point
    name: str  # Name of the contamination point
    description: str  # Description of the contamination point
    severity: str = "MEDIUM"  # Severity level (LOW, MEDIUM, HIGH, CRITICAL)
    context_boundaries: List[str] = []  # List of context boundaries involved
    created_at: datetime = datetime.now()  # Time when contamination point was identified
    updated_at: datetime = datetime.now()  # Time when contamination point was last updated
    status: str = "UNRESOLVED"  # Status of the contamination point (UNRESOLVED, RESOLVED, MONITORING)