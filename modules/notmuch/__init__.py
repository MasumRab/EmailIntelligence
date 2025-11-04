import logging

import gradio as gr
from fastapi import FastAPI

from .ui import create_notmuch_ui

logger = logging.getLogger(__name__)

def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Registers the Notmuch UI as a new tab in the main Gradio application.
    """
    try:
        logger.info("Registering Notmuch module.")
        
        # Add the Notmuch UI component to the main Gradio app
        with gradio_app:
            with gr.TabItem("Notmuch Search"):
                create_notmuch_ui()
        
        logger.info("Notmuch module registered successfully.")
    except Exception as e:
        logger.error(f"Failed to register Notmuch module: {e}", exc_info=True)
        raise
