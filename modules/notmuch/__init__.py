import gradio as gr
from fastapi import FastAPI
from .ui import create_notmuch_ui

def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Registers the Notmuch UI as a new tab in the main Gradio application.
    """
    with gradio_app:
        with gr.TabItem("Notmuch Search"):
            create_notmuch_ui()
