from typing import List, Optional, Dict
from pydantic import BaseModel


class VerificationProfile(BaseModel):
    """
    Configuration for different verification profiles per branch type
    """
    name: str  # Name of the verification profile (e.g., "main-branch", "scientific-branch")
    description: Optional[str] = None
    required_checks: List[str]  # List of required verification checks
    optional_checks: List[str] = []  # List of optional verification checks
    context_requirements: List[str] = []  # Environment and configuration requirements to verify
    branch_specific_rules: List[str] = []  # Rules specific to the target branch
    notification_config: Optional[Dict] = None  # How and when to notify stakeholders