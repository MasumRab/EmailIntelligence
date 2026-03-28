"""
Constants for the Email Intelligence Platform.
"""

# Field name constants (avoid circular import)
FIELD_NAME = "name"
FIELD_COLOR = "color"
FIELD_COUNT = "count"

DEFAULT_CATEGORY_COLOR = "#6366f1"

DEFAULT_CATEGORIES = [
    {
        FIELD_NAME: "Primary",
        "description": "Default primary category",
        FIELD_COLOR: "#4CAF50",
        FIELD_COUNT: 0,
    },
    {
        FIELD_NAME: "Social",
        "description": "Social media related emails",
        FIELD_COLOR: "#2196F3",
        FIELD_COUNT: 0,
    },
    {
        FIELD_NAME: "Promotions",
        "description": "Promotional emails",
        FIELD_COLOR: "#FF9800",
        FIELD_COUNT: 0,
    },
    {
        FIELD_NAME: "Updates",
        "description": "Account updates and notifications",
        FIELD_COLOR: "#9C27B0",
        FIELD_COUNT: 0,
    },
    {
        FIELD_NAME: "Forums",
        "description": "Forum and discussion emails",
        FIELD_COLOR: "#FF5722",
        FIELD_COUNT: 0,
    },
]