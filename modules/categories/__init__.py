import logging

import gradio as gr
from fastapi import FastAPI

from .routes import router as category_router

logger = logging.getLogger(__name__)


def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Registers the categories module with the main application.
    """
    logger.info("Registering categories module.")

    # Add the API routes to the main FastAPI app
    app.include_router(category_router, prefix="/api/categories", tags=["Categories"])

    # This module does not have a Gradio UI component, but if it did,
    # it would be added here. For example:
    # with gradio_app:
    #     with gr.Tab("Categories"):
    #         gr.Markdown("## Category Management")
    #         # ... add Gradio components here

    logger.info("Categories module registered successfully.")
