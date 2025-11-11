import logging

import gradio as gr
from fastapi import FastAPI

from .ui import create_visualization_ui

logger = logging.getLogger(__name__)

def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Registers the visualization module with the main application.
    """
    logger.info("Registering visualization module.")

    # Add the visualization UI component to the main Gradio app
    with gradio_app:
        with gr.TabItem("📊 Visualization"):
            create_visualization_ui()

    logger.info("Visualization module registered successfully.")