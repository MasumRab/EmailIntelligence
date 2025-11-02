import logging

import gradio as gr
from fastapi import FastAPI

from .ui import create_dashboard_ui

logger = logging.getLogger(__name__)

def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Registers the dashboard module with the main application.
    """
    logger.info("Registering dashboard module.")
    
    # Add the dashboard UI component to the main Gradio app
    with gradio_app:
        with gr.TabItem("📈 Dashboard"):
            create_dashboard_ui()
    
    logger.info("Dashboard module registered successfully.")