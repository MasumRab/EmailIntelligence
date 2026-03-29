import logging

from fastapi import FastAPI

from .routes import router as dashboard_router

logger = logging.getLogger(__name__)


def register(app: FastAPI, gradio_app):
    """
    Registers the dashboard module with the main application.

    This includes API routes with authentication dependencies for secure access
    to dashboard statistics and metrics.
    """
    logger.info("Registering dashboard module with authentication support.")

    try:
        # Add the API routes to the main FastAPI app
        # Routes include authentication dependencies (get_current_active_user)
        app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])

        logger.info("Dashboard module registered successfully with authentication enabled.")

    except Exception as e:
        logger.error(f"Failed to register dashboard module: {e}", exc_info=True)
        raise
