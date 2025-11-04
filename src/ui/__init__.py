"""
UI Components for Email Intelligence Platform
"""

from .system_status import create_system_status_tab
from .ai_lab import create_ai_lab_tab
from .gmail_integration import create_gmail_integration_tab

__all__ = [
    'create_system_status_tab',
    'create_ai_lab_tab', 
    'create_gmail_integration_tab'
]