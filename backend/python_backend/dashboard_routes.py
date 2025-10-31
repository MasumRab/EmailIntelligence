"""
Dashboard routes for the deprecated backend.python_backend module.

This module provides backward compatibility by importing the dashboard
functionality from the new modular architecture.
"""

import warnings

# Issue deprecation warning
warnings.warn(
    "backend.python_backend.dashboard_routes is deprecated. "
    "Use modules.dashboard.routes instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Import from the new modular architecture
try:
    from modules.dashboard.routes import router
except ImportError as e:
    # Fallback for when modules are not available
    from fastapi import APIRouter
    router = APIRouter()
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"Could not import dashboard routes from modules: {e}")