from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class FormalVerificationTool(BaseModel):
    """
    Represents a formal verification tool used in the system
    """
    id: str  # Unique identifier for the formal verification tool
    name: str  # Name of the formal verification tool
    description: str  # Description of the formal verification tool
    version: str  # Version of the formal verification tool
    supported_verification_types: List[str]  # Types of verification this tool supports
    created_at: datetime = datetime.now()  # Time when tool was registered
    updated_at: datetime = datetime.now()  # Time when tool was last updated
    enabled: bool = True  # Whether the tool is currently enabled