"""
Plugin Management Module for EmailIntelligence Platform.

This module provides comprehensive plugin lifecycle management,
marketplace integration, and security features for extensible functionality.
"""

import logging

import gradio as gr
from fastapi import FastAPI

from src.core.plugin_routes import router as plugin_router

logger = logging.getLogger(__name__)


def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Register the plugin management module with the main application.
    """
    logger.info("Registering plugin management module.")

    # Add API routes
    app.include_router(plugin_router, tags=["Plugin Management"])

    # Add UI components to the Admin Dashboard
    with gradio_app:
        # This would add plugin management UI to the admin dashboard
        # For now, plugins are managed via API
        pass

    logger.info("Plugin management module registered successfully.")
