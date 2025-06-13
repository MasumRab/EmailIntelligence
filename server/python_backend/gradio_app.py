import gradio as gr
from server.python_backend.ai_engine import AdvancedAIEngine # Assuming ai_engine.py is in the same directory

# Initialize the AI Engine
ai_engine = AdvancedAIEngine()

def analyze_email_interface(subject, content):
    """
    Analyzes email subject and content using AdvancedAIEngine.
    Returns the AIAnalysisResult as a dictionary (Gradio handles JSON conversion).
    """
    email_data = {"subject": subject, "content": content}
    ai_result = ai_engine.analyze_email(email_data)
    return ai_result.model_dump()  # Convert Pydantic model to dict for Gradio

# Create the Gradio interface
iface = gr.Interface(
    fn=analyze_email_interface,
    inputs=[
        gr.Textbox(lines=2, placeholder="Enter Email Subject Here...", label="Subject"),
        gr.Textbox(lines=5, placeholder="Enter Email Content Here...", label="Content")
    ],
    outputs=gr.JSON(label="AI Analysis Result"),
    title="Email Analyzer AI",
    description="Analyzes email subject and content using an advanced AI engine."
)

# Launch the Gradio app
if __name__ == "__main__":
    iface.launch()
