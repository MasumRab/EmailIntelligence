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

# Import the EmailIntelligence CLI application
try:
    from emailintelligence_cli import EmailIntelligenceCLI
    # Create a basic FastAPI app for CLI operations
    from fastapi import FastAPI
    app_instance = FastAPI(
        title="EmailIntelligence CLI Service",
        description="AI-powered git worktree-based conflict resolution service",
        version="2.0.0"
    )

    # Add CLI-specific routes if CLI is available
    cli = EmailIntelligenceCLI()
    CONTEXT_CONTROL_AVAILABLE = True
except ImportError:
    # Fallback when CLI is not available
    from fastapi import FastAPI
    app_instance = FastAPI(
        title="EmailIntelligence Service",
        description="Email Intelligence Platform",
        version="2.0.0"
    )
    cli = None
    CONTEXT_CONTROL_AVAILABLE = False
    ContextController = None
    ProjectConfig = None
    ContextNotFoundError = Exception
    ContextIsolator = None
    ContextValidator = None
    ContextControlConfig = None


class CLIMiddleware(BaseHTTPMiddleware):
    """Middleware to manage CLI-specific operations."""

    def __init__(self, app):
        super().__init__(app)
        self.cli_available = cli is not None

    async def dispatch(self, request: StarletteRequest, call_next):
        """Process request with CLI-specific handling."""
        start_time = time.time()

        # Add CLI-related information to request state
        if self.cli_available:
            try:
                # Create a request ID for tracking
                request_id = hashlib.sha256(f"{request.client.host}:{request.url.path}:{time.time()}".encode()).hexdigest()[:12]

                # Store request info in request state
                request.state.request_id = request_id
                request.state.cli_available = self.cli_available

            except Exception as e:
                # If request ID creation fails, continue without it
                request.state.request_error = str(e)

        # Process the request
        response = await call_next(request)

        # Add CLI-related headers to response
        if hasattr(request.state, 'request_id'):
            response.headers["X-Request-ID"] = request.state.request_id

        # Add timing information
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        return response


def create_app() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.

    This function provides compatibility with service startup patterns
    that expect src.main:create_app with --factory option.
    It focuses on CLI functionality while maintaining basic service capabilities.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    # Use the app instance with CLI functionality
    app = app_instance

    # Add CLI middleware if CLI is available
    if cli:
        app.add_middleware(CLIMiddleware)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Should be configured based on environment
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add a health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        health_status = {
            "status": "healthy",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
            "cli_available": cli is not None
        }

        # Add CLI-specific health info if available
        if cli:
            try:
                health_status["cli_features"] = {
                    "available": True,
                    "version": "2.0.0",
                    "features": ["conflict_detection", "constitutional_analysis", "auto_resolution"]
                }
            except:
                pass

        return health_status

    # Add an endpoint to access CLI functionality
    @app.get("/cli/status")
    async def cli_status():
        """Endpoint to check CLI status and capabilities."""
        if cli:
            return {
                "cli_status": "available",
                "capabilities": [
                    "setup_resolution",
                    "analyze_constitutional",
                    "develop_spec_kit_strategy",
                    "align_content",
                    "validate_resolution"
                ]
            }
        else:
            return {
                "cli_status": "unavailable",
                "message": "EmailIntelligence CLI not available in this environment"
            }

    # Set up logging
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