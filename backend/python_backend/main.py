"""
FastAPI Backend for Gmail AI Email Management
Unified Python backend with optimized performance and integrated NLP
"""

import json
import logging
import os
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# Updated import to use NLP GmailAIService directly
# Note: We should avoid direct imports of GmailAIService in main.py to prevent circular dependencies
# Instead, dependencies are managed via dependency injection in the routes

# Removed: from .smart_filters import EmailFilter (as per instruction)
from ..python_nlp.smart_filters import SmartFilterManager
from . import (  # action_routes, # Removed; dashboard_routes, # Removed
    category_routes,
    email_routes,
    filter_routes,
    gmail_routes,
    training_routes,
)
from .ai_engine import AdvancedAIEngine
from .exceptions import BaseAppException

# Import new components
from .model_manager import model_manager
from .workflow_manager import workflow_manager
from .performance_monitor import performance_monitor
from ..plugins.plugin_manager import plugin_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Gmail AI Email Management",
    description="Advanced email management with AI categorization and smart filtering",
    version="2.0.0",
)

# Import the get_db function to access the database manager
from .database import get_db


@app.on_event("startup")
async def startup_event():
    """On startup, initialize all services."""
    logger.info("Application startup event received.")
    
    # Initialize database first
    from .database import initialize_db
    await initialize_db()
    
    # Initialize new components
    logger.info("Initializing model manager...")
    model_manager.load_available_models()
    
    logger.info("Initializing workflow manager...")
    # Nothing specific needed for workflow manager initialization
    
    logger.info("Initializing plugin manager...")
    plugin_manager.load_plugins()
    plugin_manager.initialize_all_plugins()
    
    # Initialize other services
    from .dependencies import initialize_services
    await initialize_services()


@app.on_event("shutdown")
async def shutdown_event():
    """On shutdown, save any pending data."""
    logger.info("Application shutdown event received.")
    db = await get_db()
    await db.shutdown()

@app.exception_handler(BaseAppException)
async def app_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5000",
        "http://localhost:5173",
        "https://*.replit.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models are now primarily defined in .models
# Ensure any models needed directly by main.py (e.g. for health endpoint response) are defined or imported.
# For this refactor, ActionExtractionRequest and ActionItem were moved to models.py.
# Other shared request/response models like EmailResponse, CategoryResponse etc. are also in models.py.

# Set up metrics if in production or staging environment
# if os.getenv("NODE_ENV") in ["production", "staging"]: # Removed
    # from .metrics import setup_metrics # Removed
    # setup_metrics(app) # Removed

# Services are now managed by the dependency injection system.

# Include routers in the app
app.include_router(email_routes.router)
app.include_router(category_routes.router)
app.include_router(gmail_routes.router)
app.include_router(filter_routes.router)
app.include_router(training_routes.router)
# app.include_router(action_routes.router) # Removed
# app.include_router(dashboard_routes.router) # Removed

# Include enhanced feature routers
from .enhanced_routes import router as enhanced_router
app.include_router(enhanced_router, prefix="/api/enhanced", tags=["enhanced"])


# Request/Response Models previously defined here are now in .models
# Ensure route files import them from .models


# Health check endpoint (usually kept in main.py)
@app.get("/health")
async def health_check(request: Request):
    """System health check"""
    try:
        # Perform any necessary checks, e.g., DB connectivity if desired
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
        }
    except Exception as e:  # This generic exception is fine for health check's own error
        logger.error(  # Simple log for health check itself
            json.dumps(
                {
                    "message": "Health check failed",
                    "endpoint": str(request.url),
                    "error_type": type(e).__name__,
                    "error_detail": str(e),
                }
            )
        )
        return JSONResponse(
            status_code=503,  # Service Unavailable
            content={
                "status": "unhealthy",
                "error": "Service health check failed.",  # Generic message to client
                "timestamp": datetime.now().isoformat(),
                "endpoint": str(request.url),
            },
        )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True, log_level="info")