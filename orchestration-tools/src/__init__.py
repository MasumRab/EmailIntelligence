"""Orchestration Tools - Verification and Consistency System."""

__version__ = "0.1.0"
__author__ = "EmailIntelligence Team"

from src.models.verification import VerificationResult
from src.models.context import ContextVerification

__all__ = [
    "VerificationResult",
    "ContextVerification",
]
