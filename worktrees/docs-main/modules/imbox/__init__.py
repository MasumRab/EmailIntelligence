import gradio as gr
from .imbox_ui import imbox_tab


def register(app, gradio_app):
    with gradio_app:
        with gr.Tabs():
            with gr.TabItem("Imbox"):
                imbox_tab
