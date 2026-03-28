import logging

import gradio as gr
from fastapi import FastAPI

from .ui import create_inbox_ui

logger = logging.getLogger(__name__)

def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Registers the inbox module with the main application.
    """
    logger.info("Registering inbox module.")
    
    # Add the inbox UI component to the main Gradio app
    with gradio_app:
        with gr.TabItem("📥 Inbox"):
            create_inbox_ui()
    
    logger.info("Inbox module registered successfully.")