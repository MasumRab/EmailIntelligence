"""
Factory module for creating the FastAPI application with context control integration.

This module provides a create_app factory function that is compatible with
the remote branch's expectations while preserving all local branch functionality
and integrating context control patterns from the remote branch.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest
import logging
from typing import Optional
import time
import hashlib
import os

# Import the actual backend implementation from the local branch
from src.backend.python_backend.main import app as local_backend_app

# Import context control from remote branch architecture
try:
    from src.context_control.core import ContextController
    from src.context_control.models import ProjectConfig
    from src.context_control.exceptions import ContextNotFoundError
    from src.context_control.isolation import ContextIsolator
    from src.context_control.validation import ContextValidator
    from src.context_control.config import ContextControlConfig
    CONTEXT_CONTROL_AVAILABLE = True
except ImportError:
    CONTEXT_CONTROL_AVAILABLE = False
    ContextController = None
    ProjectConfig = None
    ContextNotFoundError = Exception
    ContextIsolator = None
    ContextValidator = None
    ContextControlConfig = None


class ContextControlMiddleware(BaseHTTPMiddleware):
    """Middleware to manage context control for requests based on remote branch patterns."""
    
    def __init__(self, app):
        super().__init__(app)
        self.context_controller = ContextController() if CONTEXT_CONTROL_AVAILABLE else None
        self.validator = ContextValidator() if CONTEXT_CONTROL_AVAILABLE else None
    
    async def dispatch(self, request: StarletteRequest, call_next):
        """Process request with context control."""
        start_time = time.time()
        
        # Create or retrieve context for this request
        if CONTEXT_CONTROL_AVAILABLE and self.context_controller:
            try:
                # Create a context for this request
                context_id = hashlib.sha256(f"{request.client.host}:{request.url.path}:{time.time()}".encode()).hexdigest()[:12]
                
                # Store context in request state
                request.state.context_id = context_id
                request.state.context_controller = self.context_controller
                
                # Add context isolation if available
                if ContextIsolator:
                    request.state.context_isolator = ContextIsolator
                
            except Exception as e:
                # If context creation fails, continue without it
                request.state.context_error = str(e)
        
        # Process the request
        response = await call_next(request)
        
        # Add context-related headers to response
        if hasattr(request.state, 'context_id'):
            response.headers["X-Context-ID"] = request.state.context_id
            
        # Add timing information
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        return response


def create_app() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.
    
    This function is compatible with the remote branch's service startup
    configuration that expects src.main:create_app with --factory option.
    It integrates context control patterns from the remote branch while
    preserving all functionality from the local branch.
    
    Returns:
        FastAPI: Configured FastAPI application instance with context control
    """
    # Use the actual backend app from local implementation
    app = local_backend_app
    
    # Add context control middleware if available (from remote branch pattern)
    if CONTEXT_CONTROL_AVAILABLE:
        app.add_middleware(ContextControlMiddleware)
    
    # Add CORS middleware as expected by both architectures
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Should be configured based on environment
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add a health check endpoint that's common in both architectures
    @app.get("/health")
    async def health_check():
        """Health check endpoint compatible with both architectures."""
        health_status = {
            "status": "healthy",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
            "context_control_available": CONTEXT_CONTROL_AVAILABLE
        }
        
        # Add context-specific health info if available
        if CONTEXT_CONTROL_AVAILABLE:
            try:
                health_status["context_controller"] = {
                    "available": ContextController is not None,
                    "validator": ContextValidator is not None,
                    "isolator": ContextIsolator is not None,
                    "config": ContextControlConfig is not None
                }
            except:
                pass
        
        return health_status
    
    # Add an endpoint to get context control configuration
    @app.get("/context-control/config")
    async def get_context_config():
        """Endpoint to retrieve context control configuration."""
        if CONTEXT_CONTROL_AVAILABLE and ContextControlConfig:
            try:
                config = ContextControlConfig()
                return {
                    "config": config.dict(),
                    "context_control_available": True
                }
            except Exception as e:
                return {
                    "context_control_available": True,
                    "config_error": str(e)
                }
        else:
            return {
                "context_control_available": False,
                "message": "Context control not available in this environment"
            }
    
    # Set up logging as expected by both architectures
    logging.basicConfig(level=logging.INFO)
    
    return app


# For backward compatibility when called directly (non-factory usage)
if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 8000)),
        log_level="info"
    )