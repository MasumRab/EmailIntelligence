import argparse
import logging

import gradio as gr
import uvicorn
from fastapi import FastAPI

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

    # Create the main Gradio UI as a placeholder
    # Modules will add their own tabs and components to this.
    with gr.Blocks(theme=gr.themes.Soft(), title="Email Intelligence Platform") as gradio_app:
        gr.Markdown("# Email Intelligence Platform")
        gr.Markdown("Welcome! Modules will be loaded into tabs below.")

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
