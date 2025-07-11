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
from fastapi.responses import JSONResponse

# Updated import to use NLP GmailAIService directly
from server.python_nlp.gmail_service import GmailAIService

# Removed: from .smart_filters import EmailFilter (as per instruction)
from server.python_nlp.smart_filters import SmartFilterManager

from . import (
    # action_routes, # Removed
    category_routes,
    # dashboard_routes, # Removed
    email_routes,
    filter_routes,
    gmail_routes,
)
from .ai_engine import AdvancedAIEngine

# Import our Python modules
# from .performance_monitor import PerformanceMonitor # Removed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Gmail AI Email Management",
    description="Advanced email management with AI categorization and smart filtering",
    version="2.0.0",
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

# Initialize services
# Services are now initialized within their respective route files
# or kept here if they are used by multiple route files or for general app setup.
gmail_service = GmailAIService()  # Used by gmail_routes
filter_manager = SmartFilterManager()  # Used by filter_routes
ai_engine = AdvancedAIEngine()  # Used by email_routes
# performance_monitor = PerformanceMonitor() # Removed

# Include routers in the app
app.include_router(email_routes.router)
app.include_router(category_routes.router)
app.include_router(gmail_routes.router)
app.include_router(filter_routes.router)
# app.include_router(action_routes.router) # Removed
# app.include_router(dashboard_routes.router) # Removed

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
