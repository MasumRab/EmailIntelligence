from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class UserRole(str):
    READ = "READ"
    RUN = "RUN"
    REVIEW = "REVIEW"
    ADMIN = "ADMIN"


class User(BaseModel):
    """
    Represents users in the verification system
    """
    id: str  # Unique identifier for the user
    username: str  # User identifier
    api_key: str  # API key for authentication (encrypted)
    role: UserRole  # User role (READ, RUN, REVIEW, ADMIN)
    permissions: List[str] = []  # Specific permissions granted to the user
    created_at: datetime = datetime.now()  # Time when user account was created
    last_accessed: Optional[datetime] = None  # Time of last access