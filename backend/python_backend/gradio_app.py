import gradio as gr
from backend.python_nlp.nlp_engine import NLPEngine

# Initialize the NLP Engine
nlp_engine = NLPEngine()

def analyze_email_interface(subject, content):
    """
    Analyzes email subject and content using the NLPEngine.
    Returns the analysis result as a dictionary for Gradio to display.
    """
    if not subject and not content:
        return {"error": "Subject and content cannot both be empty."}

    email_data = {"subject": subject, "content": content}
    # The NLPEngine's analyze_emails method expects a list of emails
    analysis_result = nlp_engine.analyze_emails([email_data])

    # Return the analysis of the first (and only) email
    if analysis_result:
        return analysis_result[0]
    return {"error": "Failed to analyze email."}

# Create the Gradio interface
with gr.Blocks(title="Email Intelligence Analysis", theme=gr.themes.Soft()) as iface:
    gr.Markdown("## Email Intelligence Analysis UI")
    gr.Markdown("Enter the subject and content of an email to analyze its sentiment, topic, intent, and urgency.")

    with gr.Row():
        with gr.Column(scale=2):
            email_subject = gr.Textbox(label="Email Subject", placeholder="Enter email subject...")
            email_content = gr.Textbox(label="Email Content", lines=10, placeholder="Enter email content...")
            analyze_button = gr.Button("Analyze Email", variant="primary")
        with gr.Column(scale=1):
            gr.Markdown("### Analysis Results")
            analysis_output = gr.JSON(label="AI Analysis")

    analyze_button.click(
        fn=analyze_email_interface,
        inputs=[email_subject, email_content],
        outputs=analysis_output
    )

# To launch this app, you can run this file directly.
if __name__ == "__main__":
    print("Launching Gradio UI for Email Intelligence Analysis...")
    iface.launch()