"""
FastAPI Backend for Gmail AI Email Management
Unified Python backend with optimized performance and integrated NLP
"""

import logging
import os
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from ..plugins.plugin_manager import plugin_manager
from .dependencies import (
    get_category_service,
    get_db,
    get_email_service,
)
from .exceptions import AppException, BaseAppException
from .model_manager import model_manager
from .routes import (
    category_routes,
    email_routes,
    filter_routes,
    gmail_routes,
)
# Enhanced and new routes
from .enhanced_routes import router as enhanced_router
from .workflow_routes import router as workflow_router
from .node_workflow_routes import router as node_workflow_router
from .advanced_workflow_routes import router as advanced_workflow_router

from .settings import settings

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

    logger.info("Initializing plugin manager...")
    plugin_manager.load_plugins()
    plugin_manager.initialize_all_plugins()

    # Initialize other services if needed (most are handled by Depends)
    logger.info("Startup complete. Services are ready.")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown: perform cleanup."""
    db = await get_db()
    await db.shutdown()
    logger.info("Application shutdown complete.")


# --- Exception Handlers ---
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
            "details": str(exc)
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


# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
# Include legacy routers for backward compatibility
app.include_router(email_routes.router, tags=["Legacy Emails"])
app.include_router(category_routes.router, tags=["Legacy Categories"])
app.include_router(gmail_routes.router, tags=["Legacy Gmail"])
app.include_router(filter_routes.router, tags=["Legacy Filters"])

# Include enhanced feature routers
app.include_router(enhanced_router, prefix="/api/enhanced", tags=["Enhanced Features"])

# Include workflow routes (legacy and node-based)
app.include_router(workflow_router, prefix="/api/workflows", tags=["Workflows"])

# Include advanced workflow routes (will use node-based system)
app.include_router(advanced_workflow_router, prefix="/api/advanced-workflows", tags=["Advanced Workflows"])

# Include node-based workflow routes
app.include_router(node_workflow_router, prefix="/api/nodes", tags=["Node Workflows"])


# --- Health Check ---
@app.get("/health", tags=["System"])
async def health_check(request: Request):
    """System health check"""
    try:
        # Simple check, can be expanded to check DB connection etc.
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": settings.app_version,
            "app_name": settings.app_name,
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        return JSONResponse(
            status_code=503,  # Service Unavailable
            content={
                "status": "unhealthy",
                "error": "Service health check failed.",
                "timestamp": datetime.now().isoformat(),
            },
        )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run("backend.python_backend.main:app", host="0.0.0.0", port=port, reload=True, log_level="info")
