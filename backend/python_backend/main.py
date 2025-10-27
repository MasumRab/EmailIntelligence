"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

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
from pydantic import ValidationError

from ..plugins.plugin_manager import plugin_manager
from backend.python_nlp.gmail_service import GmailAIService

# Removed: from .smart_filters import EmailFilter (as per instruction)
from backend.python_nlp.smart_filters import SmartFilterManager

from . import (
    action_routes,
    ai_routes,
    category_routes,
    dashboard_routes,
    email_routes,
    filter_routes,
    gmail_routes,
    training_routes,
    workflow_routes,
    model_routes,
    performance_routes,
)
from .auth import create_access_token, get_current_user, TokenData
from src.core.auth import authenticate_user
from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException, status
from datetime import timedelta
from .ai_engine import AdvancedAIEngine
from .exceptions import AppException

# Import new components
from .model_manager import model_manager
from .performance_monitor import performance_monitor
from .settings import settings
from .database import db_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with settings
app = FastAPI(
    title=settings.app_name,
    description="Advanced email management with AI categorization and smart filtering",
    version=settings.app_version,
)


@app.on_event("startup")
async def startup_event():
    """On startup, initialize all services."""
    logger.info("Application startup event received.")

    # Initialize database first
    from .database import initialize_db

    await initialize_db()

    # Initialize new components
    logger.info("Initializing model manager...")
    model_manager.discover_models()

    logger.info("Initializing workflow manager...")
    # Nothing specific needed for workflow manager initialization

    logger.info("Initializing plugin manager...")
    plugin_manager.load_plugins()
    plugin_manager.initialize_all_plugins()

    # Initialize other services
    from .dependencies import initialize_services

    await initialize_services()
    await db_manager.connect()


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown: disconnect from the database."""
    await db_manager.close()


@app.exception_handler(AppException)

async def app_exception_handler(request: Request, exc: AppException):

    return JSONResponse(

        status_code=exc.status_code,

        content=exc.detail,

    )


@app.exception_handler(BaseAppException)

async def base_app_exception_handler(request: Request, exc: BaseAppException):

    return JSONResponse(

        status_code=500,

        content={

            "success": False,

            "message": "An internal error occurred",

            "error_code": "INTERNAL_ERROR",
            "details": str(exc),
        },

    )





@app.exception_handler(ValidationError)

async def validation_exception_handler(request: Request, exc: ValidationError):

    """Handle Pydantic validation errors with detailed 422 responses."""

    return JSONResponse(

        status_code=422,

        content={

            "detail": exc.errors(),

            "message": "Validation error with provided data.",

        },

    )


# Configure CORS using settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models are now primarily defined in .models
# Ensure any models needed directly by main.py (e.g. for health endpoint response) are defined or imported.
# For this refactor, ActionExtractionRequest and ActionItem were moved to models.py.
# Other shared request/response models like EmailResponse, CategoryResponse etc. are also in models.py.

# Set up metrics if in production or staging environment
if os.getenv("NODE_ENV") in ["production", "staging"]:
    from .metrics import setup_metrics

    setup_metrics(app)

# Initialize services
# Services are now initialized within their respective route files
# or kept here if they are used by multiple route files or for general app setup.
gmail_service = GmailAIService()  # Used by gmail_routes
filter_manager = SmartFilterManager()  # Used by filter_routes
ai_engine = AdvancedAIEngine(model_manager)  # Used by email_routes, action_routes
performance_monitor = performance_monitor  # Used by all routes via @performance_monitor.track

# Include versioned API routers
from .routes.v1.email_routes import router as email_router_v1
from .routes.v1.category_routes import router as category_router_v1

# Mount versioned APIs
app.include_router(email_router_v1, prefix="/api/v1", tags=["emails-v1"])
app.include_router(category_router_v1, prefix="/api/v1", tags=["categories-v1"])

# Include legacy routers for backward compatibility
app.include_router(email_routes.router)
app.include_router(category_routes.router)
app.include_router(gmail_routes.router)
app.include_router(filter_routes.router)
app.include_router(training_routes.router)
app.include_router(workflow_routes.router)
app.include_router(model_routes.router)
app.include_router(performance_routes.router)
app.include_router(action_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(ai_routes.router)

# Include enhanced feature routers
from .enhanced_routes import router as enhanced_router

app.include_router(enhanced_router, prefix="/api/enhanced", tags=["enhanced"])

# Include workflow routes (legacy and node-based)
from .workflow_routes import router as workflow_router

app.include_router(workflow_router, prefix="", tags=["workflows"])

# Include advanced workflow routes (will use node-based system)
from .advanced_workflow_routes import router as advanced_workflow_router

app.include_router(advanced_workflow_router, prefix="/api/workflows", tags=["advanced-workflows"])

# Include node-based workflow routes
from .node_workflow_routes import router as node_workflow_router

app.include_router(node_workflow_router, prefix="/api/nodes", tags=["node-workflows"])

# Initialize workflow manager instance (using the node-based workflow manager)
try:
    from backend.node_engine.workflow_manager import workflow_manager as node_workflow_manager

    workflow_manager_instance = node_workflow_manager
except ImportError:
    # Fallback if node engine is not available
    workflow_manager_instance = None

# Request/Response Models previously defined here are now in .models
# Ensure route files import them from .models


# Authentication endpoints
@app.post("/token")
async def login(username: str, password: str):
    """Login endpoint to get access token"""
    # Use the new authentication system
    db = await get_db()
    user = await authenticate_user(username, password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Try to get the settings if possible
    try:
        from .settings import settings
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    except ImportError:
        # Use a default if settings are not available
        access_token_expires = timedelta(minutes=30)
    
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Health check endpoint (usually kept in main.py)
@app.get("/health")
async def health_check(request: Request):
    """System health check"""
    try:
        # Perform any necessary checks, e.g., DB connectivity if desired
        # await db.execute_query("SELECT 1") # Example DB check
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": settings.app_version,
            "app_name": settings.app_name,
        }
    except (ValueError, RuntimeError, OSError) as e:  # Specific exceptions for health check
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
