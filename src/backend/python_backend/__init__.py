"""
Python Backend Package

FastAPI backend for EmailIntelligence application.
"""

from . import (
    ai_routes,
    category_routes,
    dashboard_routes,
    email_routes,
    filter_routes,
    gmail_routes,
    model_routes,
    performance_routes,
    workflow_routes,
    enhanced_routes,
    advanced_workflow_routes,
    node_workflow_routes,
    training_routes,
)

# For backward compatibility
action_routes = ai_routes
