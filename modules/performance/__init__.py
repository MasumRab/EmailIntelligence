"""
Performance Monitoring Module for EmailIntelligence Platform.

This module provides system performance monitoring capabilities for the platform.
"""

import logging

import gradio as gr
from fastapi import FastAPI

from src.core.performance_routes import router as performance_router

logger = logging.getLogger(__name__)


def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Register the performance monitoring module with the main application.
    """
    logger.info("Registering performance monitoring module.")

    # Add API routes
    app.include_router(performance_router, prefix="/api/performance", tags=["Performance"])

    logger.info("Performance monitoring module registered successfully.")