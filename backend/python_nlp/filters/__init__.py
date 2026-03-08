"""
Init file for the filters package.
"""

from .filter_manager import SmartFilterManager
from .filter_models import EmailFilter

__all__ = ["SmartFilterManager", "EmailFilter"]