import logging

import gradio as gr
from fastapi import FastAPI

from .ui import create_scientific_ui

logger = logging.getLogger(__name__)

def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Registers the scientific analysis module with the main application.
    """
    try:
        logger.info("Registering scientific analysis module.")

        # Add the scientific UI component to the main Gradio app
        with gradio_app:
            with gr.TabItem("🔬 Scientific"):
                create_scientific_ui()

        logger.info("Scientific analysis module registered successfully.")
    except Exception as e:
        logger.error(f"Failed to register scientific analysis module: {e}", exc_info=True)
        raise