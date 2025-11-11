import logging

import gradio as gr
from fastapi import FastAPI

from .ui import create_analysis_ui

logger = logging.getLogger(__name__)

def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Registers the analysis module with the main application.
    """
    try:
        logger.info("Registering analysis module.")

        # Add the analysis UI component to the main Gradio app
        with gradio_app:
            with gr.TabItem("🔬 Analysis"):
                create_analysis_ui()

        logger.info("Analysis module registered successfully.")
    except Exception as e:
        logger.error(f"Failed to register analysis module: {e}", exc_info=True)
        raise