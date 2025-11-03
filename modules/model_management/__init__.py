"""
Model Management Module for EmailIntelligence Platform.

This module provides dynamic AI model management capabilities,
including loading, unloading, versioning, and performance monitoring.
"""

import logging

import gradio as gr
from fastapi import FastAPI

from src.core.model_routes import router as model_router

logger = logging.getLogger(__name__)


def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Register the model management module with the main application.
    """
    logger.info("Registering model management module.")

    # Add API routes
    app.include_router(model_router, tags=["Model Management"])

    # Add UI components to the Admin Dashboard
    with gradio_app:
        # Find the Admin Dashboard tab and add model management UI
        # This would be enhanced with actual Gradio components
        pass

    logger.info("Model management module registered successfully.")
