"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Constants for the Email Intelligence backend.
"""

from .database import FIELD_NAME, FIELD_COLOR, FIELD_COUNT

DEFAULT_CATEGORY_COLOR = "#6366f1"

DEFAULT_CATEGORIES = [
    {
        FIELD_NAME: "Primary",
        "description": "Default primary category",
        FIELD_COLOR: "#4CAF50",
        FIELD_COUNT: 0,
    },
    {
        FIELD_NAME: "Promotions",
        "description": "Promotional emails",
        FIELD_COLOR: "#2196F3",
        FIELD_COUNT: 0,
    },
    {
        FIELD_NAME: "Social",
        "description": "Social media notifications",
        FIELD_COLOR: "#FFC107",
        FIELD_COUNT: 0,
    },
    {
        FIELD_NAME: "Updates",
        "description": "Updates and notifications",
        FIELD_COLOR: "#9C27B0",
        FIELD_COUNT: 0,
    },
    {
        FIELD_NAME: "Forums",
        "description": "Forum discussions",
        FIELD_COLOR: "#795548",
        FIELD_COUNT: 0,
    },
]
