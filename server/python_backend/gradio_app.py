import gradio as gr

from server.python_backend.ai_engine import \
    AdvancedAIEngine  # Assuming ai_engine.py is in the same directory

# Initialize the AI Engine
ai_engine = AdvancedAIEngine()

# def analyze_email_interface(subject, content):
#     """
#     Analyzes email subject and content using AdvancedAIEngine.
#     Returns the AIAnalysisResult as a dictionary (Gradio handles JSON conversion).
#     """
#     email_data = {"subject": subject, "content": content}
#     ai_result = ai_engine.analyze_email(email_data)
#     return ai_result.model_dump()  # Convert Pydantic model to dict for Gradio

# Create the Gradio interface with Tabs
with gr.Blocks(
    title="No-Code Email Platform (Gradio UI)", theme=gr.themes.Soft()
) as iface:
    with gr.Tab("Email Builder"):
        gr.Markdown(
            "## Email Builder Interface (No-Code Style)"
        )  # Main title for the tab
        with gr.Row():
            with gr.Column(scale=1, min_width=200):  # Component Library
                gr.Markdown("### Component Library")
                with gr.Accordion("Text Elements"):
                    gr.Button("Heading")
                    gr.Button("Paragraph")
                    gr.Button("List")
                with gr.Accordion("Media Elements"):
                    gr.Button("Image")
                    gr.Button("Video Link")
                with gr.Accordion("Layout Elements"):
                    gr.Button("Spacer")
                    gr.Button("Divider")
                with gr.Accordion("Interactive Elements"):
                    gr.Button("Button")
                    gr.Button("Social Share")
            with gr.Column(scale=3):  # Canvas
                gr.Markdown("### Email Canvas")
                gr.Textbox(
                    label="Canvas Area",
                    lines=20,
                    interactive=False,
                    placeholder="Drag components here to build your email.",
                )
            with gr.Column(scale=1, min_width=200):  # Properties Panel
                gr.Markdown("### Properties")
                gr.JSON(label="Selected Component Properties")
                # Or:
                # gr.Textbox(label="Property 1", interactive=False)
                # gr.Textbox(label="Property 2", interactive=False)
                # gr.Textbox(label="Property 3", interactive=False)
        # More components will be added here in later steps
    with gr.Tab("Campaigns"):
        gr.Markdown("## Manage Email Campaigns")
        gr.DataFrame(
            headers=["Campaign Name", "Status", "Sent", "Open Rate"],
            value=[
                ["Summer Sale", "Sent", 10000, "25%"],
                ["New Product Launch", "Draft", 0, "0%"],
            ],
            label="Campaigns List",
        )
        with gr.Row():
            gr.Button("New Campaign")
            gr.Button("Edit Selected")
            gr.Button("Delete Selected")
    with gr.Tab("Analytics"):
        gr.Markdown("## Email Marketing Analytics")
        gr.Markdown("### Open Rate Over Time\n_Placeholder for chart_")
        gr.DataFrame(
            headers=["Metric", "Value"],
            value=[
                ["Total Emails Sent", 15000],
                ["Average Open Rate", "22%"],
                ["Click-through Rate", "3.5%"],
            ],
            label="Key Metrics",
        )
    with gr.Tab("Settings"):
        gr.Markdown("## Application Settings")
        with gr.Accordion("API Configuration"):
            gr.Textbox(
                label="Email Service API Key",
                placeholder="Enter your API key",
                type="password",
            )
            gr.Dropdown(
                label="Email Provider",
                choices=["Provider A", "Provider B", "Provider C"],
            )
        with gr.Accordion("Notification Settings"):
            gr.Checkbox(label="Enable email notifications for new subscribers")
            gr.Checkbox(label="Enable email notifications for campaign completions")
        gr.Button("Save Settings")

# Launch the Gradio app
if __name__ == "__main__":
    iface.launch()
