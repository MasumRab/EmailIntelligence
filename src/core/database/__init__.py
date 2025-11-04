"""
Database package for Email Intelligence Platform
"""

from .database_manager import DatabaseManager, get_db, initialize_db
from .constants import *

__all__ = [
    'DatabaseManager',
    'get_db',
    'initialize_db',
    'DATA_DIR',
    'EMAIL_CONTENT_DIR',
    'EMAILS_FILE',
    'CATEGORIES_FILE',
    'USERS_FILE',
    'SETTINGS_FILE',
    'DATA_TYPE_EMAILS',
    'DATA_TYPE_CATEGORIES',
    'DATA_TYPE_USERS',
    'FIELD_ID',
    'FIELD_MESSAGE_ID',
    'FIELD_CATEGORY_ID',
    'FIELD_IS_UNREAD',
    'FIELD_ANALYSIS_METADATA',
    'FIELD_CREATED_AT',
    'FIELD_UPDATED_AT',
    'FIELD_NAME',
    'FIELD_COLOR',
    'FIELD_COUNT',
    'FIELD_TIME',
    'FIELD_CONTENT',
    'FIELD_SUBJECT',
    'FIELD_SENDER',
    'FIELD_SENDER_EMAIL',
    'HEAVY_EMAIL_FIELDS',
    'FIELD_CATEGORY_NAME',
    'FIELD_CATEGORY_COLOR'
]