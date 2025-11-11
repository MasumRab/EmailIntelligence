from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel


class VerificationStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PASS = "PASS"
    FAIL = "FAIL"
    BYPASS = "BYPASS"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ReviewStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class VerificationCheckResult(BaseModel):
    name: str
    status: str  # PASS, FAIL, SKIPPED
    details: str
    executed_at: datetime


class VerificationResult(BaseModel):
    """
    Represents the result of a verification process
    """
    id: str
    branch_name: str  # source branch
    target_branch: str  # target branch for merge validation
    status: VerificationStatus
    timestamp: datetime
    completed_at: Optional[datetime] = None
    details: Dict[str, str] = {}  # Detailed results from each verification check
    report: str = ""  # Generated report with findings
    initiator: str  # User who initiated the verification
    approver: Optional[str] = None  # User who approved the verification (if applicable)
    review_status: ReviewStatus = ReviewStatus.PENDING
    results: Optional[Dict] = None  # Detailed results structure
    created_at: datetime = datetime.now()
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    rejected_by: Optional[str] = None
    rejected_at: Optional[datetime] = None
    profile: Optional[str] = None  # Verification profile used
    correlation_id: Optional[str] = None  # For structured logging
    
    class Config:
        use_enum_values = True