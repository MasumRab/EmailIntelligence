"""Gmail Service - Deprecated alias for GmailAIService."""
import warnings
warnings.warn(
    "Importing from backend.python_backend.gmail_service is deprecated. "
    "Use src.backend.python_nlp.gmail_service.GmailAIService instead.",
    DeprecationWarning,
    stacklevel=2
)

from src.backend.python_nlp.gmail_service import GmailAIService

__all__ = ["GmailAIService"]
