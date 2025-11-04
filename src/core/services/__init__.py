"""
Services package for Email Intelligence Platform
"""

from .base_service import BaseService, ServiceResponse
from .email_service import EmailService, get_email_service
from .category_service import CategoryService, get_category_service

__all__ = [
    'BaseService',
    'ServiceResponse',
    'EmailService',
    'get_email_service',
    'CategoryService',
    'get_category_service'
]