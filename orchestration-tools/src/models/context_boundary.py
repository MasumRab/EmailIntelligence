from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class ContextBoundary(BaseModel):
    """
    Represents a context boundary in the tools framework
    """
    id: str  # Unique identifier for the context boundary
    name: str  # Name of the context boundary
    description: str  # Description of the context boundary
    created_at: datetime = datetime.now()  # Time when context boundary was created
    updated_at: datetime = datetime.now()  # Time when context boundary was last updated
    related_components: List[str] = []  # List of components related to this boundary