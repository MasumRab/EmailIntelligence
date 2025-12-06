from fastapi import FastAPI
import gradio as gr

def create_app():
    app = FastAPI()

    gradio_app = gr.Blocks()
    app = gr.mount_gradio_app(app, gradio_app, path="/")

    return app
