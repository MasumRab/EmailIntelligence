import configparser
configparser.SafeConfigParser = configparser.ConfigParser

import argparse
import logging

import gradio as gr
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from .core.module_manager import ModuleManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app():
    """
    Creates and configures the main FastAPI application and Gradio UI.
    """
    # Create the main FastAPI app
    app = FastAPI(
        title="Email Intelligence Platform",
        description="A modular and extensible platform for email processing and analysis.",
        version="3.0.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add security headers middleware
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        return response

        # Add exception handlers for secure error responses
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": "Validation error", "message": "Invalid input data"},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": "Request error", "message": "An error occurred"},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "message": "An unexpected error occurred"},
        )

    @app.get("/")
    async def root():
        """Redirect root to Gradio UI."""
        return RedirectResponse(url="/ui")

    # Create the main Gradio UI as a placeholder
    # Modules will add their own tabs and components to this.
    with gr.Blocks(theme=gr.themes.Soft(), title="Email Intelligence Platform") as gradio_app:
        gr.Markdown("# Email Intelligence Platform")

        with gr.Tabs():
            with gr.TabItem("Simple UI (A)"):
                gr.Markdown("## Simple & Streamlined UI\nThis is the placeholder for the simple, user-friendly interface where users can run pre-built workflows.")

            with gr.TabItem("Visual Editor (B)"):
                gr.Markdown("## Visual & Node-Based UI\nThis is the placeholder for the powerful, node-based workflow editor.")

            with gr.TabItem("Admin Dashboard (C)"):
                gr.Markdown("## Power-User Dashboard\nThis is the placeholder for the admin and power-user dashboard for managing models, users, and system performance.")

    # Initialize the Module Manager
    module_manager = ModuleManager(app, gradio_app)
    module_manager.load_modules()

    # Mount the Gradio UI onto the FastAPI app
    # This makes the UI accessible at the '/ui' endpoint
    gr.mount_gradio_app(app, gradio_app, path="/ui")

    logger.info("Application creation complete. FastAPI and Gradio are integrated.")
    return app


def main():
    """
    Main entry point to run the server.
    """
    parser = argparse.ArgumentParser(description="Run the Email Intelligence Platform.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the server on.")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the server on.")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reloading.")
    args = parser.parse_args()

    app = create_app()

    uvicorn.run(
        "src.main:create_app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        factory=True,
    )


if __name__ == "__main__":
    main()
