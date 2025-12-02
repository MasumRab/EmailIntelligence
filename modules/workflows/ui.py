import gradio as gr

def create_workflow_ui():
    with gr.Blocks() as workflow_ui:
        gr.Markdown("## Workflow Editor")
    return workflow_ui
