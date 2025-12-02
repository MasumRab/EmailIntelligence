from fastapi import FastAPI
import gradio as gr
from src.core.module_manager import ModuleManager

def create_app():
    app = FastAPI()

    gradio_app = gr.Blocks()

    # Mount the Gradio app
    app = gr.mount_gradio_app(app, gradio_app, path="/")

    # Load modules
    module_manager = ModuleManager(app, gradio_app)
    module_manager.load_modules()

    return app
