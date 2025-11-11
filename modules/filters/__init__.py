"""
Filters Module for EmailIntelligence Platform.

This module provides email filtering capabilities for the platform.
"""

import logging

import gradio as gr
from fastapi import FastAPI

from src.core.filter_routes import router as filter_router

logger = logging.getLogger(__name__)


def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Register the filters module with the main application.
    """
    logger.info("Registering filters module.")

    # Add API routes
    app.include_router(filter_router, prefix="/api/filters", tags=["Filters"])

    logger.info("Filters module registered successfully.")