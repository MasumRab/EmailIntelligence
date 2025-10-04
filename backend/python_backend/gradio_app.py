import gradio as gr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
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

    # Use analyze_email (singular)
    analysis_result = nlp_engine.analyze_email(subject, content)

    if analysis_result:
        return analysis_result
    return {"error": "Failed to analyze email."}

def generate_sentiment_chart(sentiment):
    """Generate a simple bar chart for sentiment."""
    if sentiment == "positive":
        value = 1
    elif sentiment == "negative":
        value = -1
    else:
        value = 0
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': "Sentiment Gauge"},
        gauge={'axis': {'range': [-1, 1]}, 'bar': {'color': "darkblue"}}
    ))
    return fig

def generate_topic_pie(categories):
    """Generate a pie chart for categories."""
    if not categories:
        categories = ["General"]
    fig = px.pie(values=[1]*len(categories), names=categories, title="Topic Categories")
    return fig

# Create the Gradio interface
with gr.Blocks(title="Email Intelligence Analysis", theme=gr.themes.Soft()) as iface:
    gr.Markdown("## Email Intelligence Analysis UI (Scientific Branch)")
    gr.Markdown("Analyze emails with AI and visualize results for research purposes.")

    with gr.Tabs():
        with gr.TabItem("Single Email Analysis"):
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

        with gr.TabItem("Visualization"):
            gr.Markdown("### Data Visualization")
            sentiment_chart = gr.Plot(label="Sentiment Gauge")
            topic_chart = gr.Plot(label="Topic Pie Chart")
            # For demo, use sample data or trigger from analysis
            gr.Button("Generate Sample Charts").click(
                fn=lambda: (generate_sentiment_chart("neutral"), generate_topic_pie(["Work", "Personal"])),
                inputs=[],
                outputs=[sentiment_chart, topic_chart]
            )

        with gr.TabItem("Scientific Analysis"):
            gr.Markdown("### Advanced Data Analysis")
            data_input = gr.Textbox(label="Paste Email Data (JSON format)", lines=5, placeholder='[{"subject": "Test", "content": "Test content"}]')
            analyze_data_button = gr.Button("Analyze Batch")
            batch_output = gr.Dataframe(label="Batch Analysis Results")
            stats_output = gr.JSON(label="Statistics")

            def analyze_batch(data_str):
                try:
                    emails = eval(data_str)  # Simple eval for demo; use json.loads in prod
                    results = []
                    for email in emails:
                        result = nlp_engine.analyze_email(email["subject"], email["content"])
                        results.append(result)
                    df = pd.DataFrame(results)
                    stats = df.describe(include='all').to_dict()
                    return df, stats
                except Exception as e:
                    return pd.DataFrame(), {"error": str(e)}

            analyze_data_button.click(
                fn=analyze_batch,
                inputs=data_input,
                outputs=[batch_output, stats_output]
            )

        with gr.TabItem("Jupyter Notebook"):
            gr.Markdown("### Interactive Jupyter Analysis")
            gr.Markdown("For advanced scientific analysis, launch Jupyter Notebook.")
            gr.Markdown("Run: `jupyter notebook backend/python_backend/notebooks/email_analysis.ipynb`")
            launch_jupyter_button = gr.Button("Launch Jupyter (External)")
            launch_jupyter_button.click(
                fn=lambda: "Jupyter launched externally. Check terminal.",
                inputs=[],
                outputs=gr.Textbox(label="Status")
            )

# To launch this app, you can run this file directly.
if __name__ == "__main__":
    print("Launching Gradio UI for Email Intelligence Analysis...")
    iface.launch()