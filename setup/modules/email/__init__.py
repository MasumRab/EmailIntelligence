import logging

import gradio as gr
from fastapi import FastAPI

from .routes import router as email_router

logger = logging.getLogger(__name__)


def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Registers the email module with the main application.
    """
    logger.info("Registering email module.")

    # Add the API routes to the main FastAPI app
    app.include_router(email_router, prefix="/api/emails", tags=["Emails"])

    logger.info("Email module registered successfully.")
