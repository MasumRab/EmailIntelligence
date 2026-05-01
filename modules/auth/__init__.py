import logging

import gradio as gr
from fastapi import FastAPI

from .routes import router as auth_router

logger = logging.getLogger(__name__)


def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Registers the auth module with the main application.
    """
    logger.info("Registering auth module.")

    # Add the API routes to the main FastAPI app
    app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])

    logger.info("Auth module registered successfully.")
