import gradio as gr
from .email_retrieval_ui import email_retrieval_tab


def register(app, gradio_app):
    with gradio_app:
        with gr.Tabs():
            with gr.TabItem("Email Retrieval"):
                email_retrieval_tab
