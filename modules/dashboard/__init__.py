import logging

from fastapi import FastAPI

from .ui import create_dashboard_ui
from .routes import router as dashboard_router

logger = logging.getLogger(__name__)

<<<<<<< HEAD
def register(app: FastAPI, gradio_app: gr.Blocks):
=======

def register(app: FastAPI, gradio_app):
>>>>>>> scientific
    """
    Registers the dashboard module with the main application.

    This includes API routes with authentication dependencies for secure access
    to dashboard statistics and metrics.
    """
<<<<<<< HEAD
    logger.info("Registering dashboard module.")
    
    # Add the API routes to the main FastAPI app
    app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])
    
    # Add the dashboard UI component to the main Gradio app
    with gradio_app:
        with gr.TabItem("📈 Dashboard"):
            create_dashboard_ui()
    
    logger.info("Dashboard module registered successfully.")
=======
    logger.info("Registering dashboard module with authentication support.")

    try:
        # Add the API routes to the main FastAPI app
        # Routes include authentication dependencies (get_current_active_user)
        app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])

        logger.info("Dashboard module registered successfully with authentication enabled.")

    except Exception as e:
        logger.error(f"Failed to register dashboard module: {e}", exc_info=True)
        raise
>>>>>>> scientific
