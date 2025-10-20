"""
Gradio UI for the Email Intelligence Platform.

This module creates a Gradio interface that acts as a client to the FastAPI backend.
It provides tools for single email analysis, batch processing, and data visualization.
"""

import gradio as gr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
from typing import Dict, Any, List

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000"  # URL of the FastAPI backend

# --- API Communication ---
def analyze_email_interface(subject: str, content: str) -> Dict[str, Any]:
    """
    Analyzes email subject and content by calling the FastAPI endpoint.
    """
    if not subject and not content:
        return {"error": "Subject and content cannot both be empty."}

    try:
        response = requests.post(
            f"{BASE_URL}/api/ai/analyze",
            json={"subject": subject, "content": content},
            timeout=60
        )
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

# --- UI Components & Visualizations ---
def generate_sentiment_chart(sentiment: str) -> go.Figure:
    """Generate a simple gauge chart for sentiment."""
    if sentiment == "positive":
        value = 1
        color = "green"
    elif sentiment == "negative":
        value = -1
        color = "red"
    else:
        value = 0
        color = "blue"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': "Sentiment Gauge"},
        gauge={'axis': {'range': [-1, 1]}, 'bar': {'color': color}}
    ))
    return fig

def generate_topic_pie(categories: List[str]) -> px.pie:
    """Generate a pie chart for categories."""
    if not categories:
        categories = ["General"]
    
    # Create a DataFrame for Plotly Express
    df = pd.DataFrame({'category': categories})
    category_counts = df['category'].value_counts().reset_index()
    category_counts.columns = ['category', 'count']

    fig = px.pie(category_counts, values='count', names='category', title="Topic Categories")
    return fig

# --- Gradio Interface Definition ---
with gr.Blocks(title="Email Intelligence", theme=gr.themes.Soft()) as iface:
    gr.Markdown("## Email Intelligence Platform")

    with gr.Tabs():
        with gr.TabItem("Single Email Analysis"):
            with gr.Row():
                with gr.Column(scale=2):
                    email_subject = gr.Textbox(label="Email Subject", placeholder="Enter email subject...")
                    email_content = gr.Textbox(label="Email Content", lines=10, placeholder="Enter email content...")
                    analyze_button = gr.Button("Analyze Email", variant="primary")
                with gr.Column(scale=1):
                    gr.Markdown("### Analysis Results")
                    topic_output = gr.Label(label="Topic")
                    sentiment_output = gr.Label(label="Sentiment")
                    reasoning_output = gr.Textbox(label="Reasoning", lines=5, interactive=False)
                    keywords_output = gr.HighlightedText(label="Keywords")
                    analysis_output = gr.JSON(label="Full Analysis (JSON)")

        with gr.TabItem("Visualizations"):
            gr.Markdown("### Data Visualization")
            sentiment_chart = gr.Plot(label="Sentiment Gauge")
            topic_chart = gr.Plot(label="Topic Pie Chart")
            gr.Markdown("Charts update automatically after a successful analysis.")

        with gr.TabItem("Batch Analysis"):
            gr.Markdown("### Advanced Batch Analysis")
            data_input = gr.Textbox(
                label="Paste Email Data (JSON array format)",
                lines=5,
                placeholder='[{"subject": "Subject 1", "content": "Content 1"}, {"subject": "Subject 2", "content": "Content 2"}]'
            )
            analyze_data_button = gr.Button("Analyze Batch")
            batch_output = gr.DataFrame(label="Batch Analysis Results")
            stats_output = gr.JSON(label="Statistics")

    # --- Event Handlers ---
    def update_single_analysis_outputs(subject, content):
        result = analyze_email_interface(subject, content)

        if "error" in result:
            gr.Warning(f"Analysis Error: {result['error']}")
            # Return empty updates for all components
            return gr.update(), gr.update(), result.get("error", "An error occurred."), [], result, gr.update(), gr.update()

        topic = result.get("topic", "N/A")
        sentiment = result.get("sentiment", "N/A")
        reasoning = result.get("reasoning", "N/A")
        categories = result.get("categories", [])
        keywords = result.get("keywords", [])

        highlighted_keywords = [(k, result.get("topic")) for k in keywords]

        sentiment_chart_fig = generate_sentiment_chart(sentiment)
        topic_chart_fig = generate_topic_pie(categories)

        return topic, sentiment, reasoning, highlighted_keywords, result, sentiment_chart_fig, topic_chart_fig

    analyze_button.click(
        fn=update_single_analysis_outputs,
        inputs=[email_subject, email_content],
        outputs=[topic_output, sentiment_output, reasoning_output, keywords_output, analysis_output, sentiment_chart, topic_chart]
    )

    def analyze_batch_data(data_str: str):
        try:
            emails = json.loads(data_str)
            if not isinstance(emails, list):
                return pd.DataFrame(), {"error": "Input must be a JSON array of email objects."}
            if len(emails) > 50:
                gr.Warning("Processing more than 50 emails may be slow.")

            results = [analyze_email_interface(email.get("subject", ""), email.get("content", "")) for email in emails if isinstance(email, dict)]

            df = pd.DataFrame(results)
            # Generate descriptive statistics for the batch
            stats = df.describe(include='all').to_dict()
            return df, stats

        except json.JSONDecodeError as e:
            return pd.DataFrame(), {"error": f"Invalid JSON format: {str(e)}"}
        except Exception as e:
            return pd.DataFrame(), {"error": f"An unexpected error occurred during batch processing: {str(e)}"}

    analyze_data_button.click(
        fn=analyze_batch_data,
        inputs=data_input,
        outputs=[batch_output, stats_output]
    )

# To launch this app, run this file directly.
# Ensure the FastAPI backend is running on BASE_URL.
if __name__ == "__main__":
    iface.launch()
