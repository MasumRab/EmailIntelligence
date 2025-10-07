import logging
from fastapi import FastAPI
import gradio as gr

from .ui import create_workflow_ui

logger = logging.getLogger(__name__)


def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Registers the workflows module with the main application.
    This function adds the workflow UI as a new tab in the Gradio interface.
    """
    logger.info("Registering workflows module.")

    # The workflow UI is defined in a separate function for clarity.
    workflow_ui_tab = create_workflow_ui()

    # Add the UI as a new tab to the main Gradio application.
    with gradio_app:
        with gr.Tab("Workflows"):
            # The create_workflow_ui function returns a gr.Blocks object,
            # which we can directly render here.
            workflow_ui_tab.render()

    logger.info("Workflows module registered successfully.")
