from fastapi import FastAPI
import gradio as gr
from .main import router

def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Registers the dashboard module with the main FastAPI application.
    """
    app.include_router(router)
