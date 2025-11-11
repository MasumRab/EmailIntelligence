import logging

import gradio as gr
from fastapi import FastAPI

from src.core.ai_engine import set_active_ai_engine
from src.core.ai_routes import router as ai_router

from .engine import DefaultAIEngine

logger = logging.getLogger(__name__)


def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Registers the default AI engine module with the main application.
    This function instantiates and sets the active AI engine.
    """
    logger.info("Registering the Default AI Engine module.")

    # Add API routes
    app.include_router(ai_router, prefix="/api/ai", tags=["AI Engine"])

    # Create an instance of our default AI engine
    default_engine = DefaultAIEngine()

    # Initialize the engine (e.g., load models)
    default_engine.initialize()

    # Set this engine as the active one for the application
    set_active_ai_engine(default_engine)

    # This module does not have a UI component, but one could be added here
    # to display engine stats or allow model switching.

    logger.info("Default AI Engine module registered and set as active.")
