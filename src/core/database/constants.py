"""
Database constants for Email Intelligence Platform
"""

from pathlib import Path
import os

# File paths - now configurable via environment variable
# Use a more general default that works across different deployment scenarios
DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
EMAIL_CONTENT_DIR = DATA_DIR / "email_content"
EMAILS_FILE = DATA_DIR / "emails.json.gz"
CATEGORIES_FILE = DATA_DIR / "categories.json.gz"
USERS_FILE = DATA_DIR / "users.json.gz"
SETTINGS_FILE = DATA_DIR / "settings.json"

# Data types
DATA_TYPE_EMAILS = "emails"
DATA_TYPE_CATEGORIES = "categories"
DATA_TYPE_USERS = "users"

# Field names
FIELD_ID = "id"
FIELD_MESSAGE_ID = "message_id"
FIELD_CATEGORY_ID = "category_id"
FIELD_IS_UNREAD = "is_unread"
FIELD_ANALYSIS_METADATA = "analysis_metadata"
FIELD_CREATED_AT = "created_at"
FIELD_UPDATED_AT = "updated_at"
FIELD_NAME = "name"
FIELD_COLOR = "color"
FIELD_COUNT = "count"
FIELD_TIME = "time"
FIELD_CONTENT = "content"
FIELD_SUBJECT = "subject"
FIELD_SENDER = "sender"
FIELD_SENDER_EMAIL = "sender_email"
HEAVY_EMAIL_FIELDS = [FIELD_CONTENT, "content_html"]

# UI field names
FIELD_CATEGORY_NAME = "categoryName"
FIELD_CATEGORY_COLOR = "categoryColor"