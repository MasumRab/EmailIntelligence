<<<<<<< HEAD
"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.
"""

import json
from typing import Any, Dict, List

import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import seaborn as sns

from backend.python_nlp.nlp_engine import NLPEngine

# Initialize the NLP Engine
nlp_engine = NLPEngine()

BASE_URL = "http://127.0.0.1:8000"


def analyze_email_interface(subject, content):
    """
    Analyzes email subject and content by calling the FastAPI endpoint.
    """
    if not subject and not content:
        return {"error": "Subject and content cannot both be empty."}

    try:
        response = requests.post(
            f"{BASE_URL}/api/ai/analyze", json={"subject": subject, "content": content}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"Failed to analyze email. Status code: {response.status_code}, Response: {response.text}"
            }
    except Exception as e:
        return {"error": f"An exception occurred: {str(e)}"}


def generate_sentiment_chart(sentiment):
    """Generate a simple bar chart for sentiment."""
    if sentiment == "positive":
        value = 1
    elif sentiment == "negative":
        value = -1
    else:
        value = 0
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": "Sentiment Gauge"},
            gauge={"axis": {"range": [-1, 1]}, "bar": {"color": "darkblue"}},
        )
    )
    return fig


def generate_topic_pie(categories):
    """Generate a pie chart for categories."""
    if not categories:
        categories = ["General"]
    fig = px.pie(values=[1] * len(categories), names=categories, title="Topic Categories")
    return fig


# Create the Gradio interface
with gr.Blocks(title="Email Intelligence", theme=gr.themes.Soft()) as iface:
    gr.Markdown("## Email Intelligence Platform")

    with gr.Tabs():
        with gr.TabItem("📈 Dashboard"):
            gr.Markdown("## Dashboard")
            # ... (Implementation from previous step)

        with gr.TabItem("📥 Inbox"):
            gr.Markdown("## Inbox")
            email_df = gr.DataFrame(
                headers=["ID", "Subject", "From", "Date"], interactive=True, label="Emails"
            )

        with gr.TabItem("Single Email Analysis"):
            with gr.Row():
                with gr.Column(scale=2):
                    email_subject = gr.Textbox(
                        label="Email Subject", placeholder="Enter email subject..."
                    )
                    email_content = gr.Textbox(
                        label="Email Content", lines=10, placeholder="Enter email content..."
                    )
                    analyze_button = gr.Button("Analyze Email", variant="primary")
                with gr.Column(scale=1):
                    gr.Markdown("### Analysis Results")
                    topic_output = gr.Label(label="Topic")
                    sentiment_output = gr.Label(label="Sentiment")
                    reasoning_output = gr.Textbox(label="Reasoning", lines=5)
                    keywords_output = gr.HighlightedText(label="Keywords")
                    analysis_output = gr.JSON(label="Full Analysis (JSON)")

            def update_outputs(subject, content):
                result = analyze_email_interface(subject, content)
                if "error" in result:
                    return (
                        gr.update(),
                        gr.update(),
                        result.get("error", "An error occurred."),
                        [],
                        result,
                        gr.update(),
                        gr.update(),
                    )

                topic = result.get("topic", "N/A")
                sentiment = result.get("sentiment", "N/A")
                reasoning = result.get("reasoning", "N/A")
                categories = result.get("categories", [])

                keywords = result.get("keywords", [])
                highlighted_keywords = [(k, result.get("topic")) for k in keywords]

                sentiment_chart_fig = generate_sentiment_chart(sentiment)
                topic_chart_fig = generate_topic_pie(categories)

                return (
                    topic,
                    sentiment,
                    reasoning,
                    highlighted_keywords,
                    result,
                    sentiment_chart_fig,
                    topic_chart_fig,
                )

            analyze_button.click(
                fn=update_outputs,
                inputs=[email_subject, email_content],
                outputs=[
                    topic_output,
                    sentiment_output,
                    reasoning_output,
                    keywords_output,
                    analysis_output,
                    sentiment_chart,
                    topic_chart,
                ],
            )

        with gr.TabItem("Visualization"):
            gr.Markdown("### Data Visualization")
            sentiment_chart = gr.Plot(label="Sentiment Gauge")
            topic_chart = gr.Plot(label="Topic Pie Chart")
            gr.Markdown(
                "The charts above will automatically update after you analyze an email in the 'Single Email Analysis' tab."
            )

        with gr.TabItem("Scientific Analysis"):
            gr.Markdown("### Advanced Data Analysis")
            data_input = gr.Textbox(
                label="Paste Email Data (JSON format)",
                lines=5,
                placeholder='[{"subject": "Test", "content": "Test content"}]',
            )
            analyze_data_button = gr.Button("Analyze Batch")
            batch_output = gr.Dataframe(label="Batch Analysis Results")
            stats_output = gr.JSON(label="Statistics")

            def analyze_batch(data_str):
                try:
                    emails = json.loads(data_str)  # Switched to safe parsing
                    if not isinstance(emails, list):
                        return pd.DataFrame(), {
                            "error": "Input must be a JSON array of email objects"
                        }
                    if len(emails) > 100:
                        return pd.DataFrame(), {"error": "Too many emails, maximum 100 allowed"}
                    results = []
                    for email in emails:
                        if (
                            not isinstance(email, dict)
                            or "subject" not in email
                            or "content" not in email
                        ):
                            continue  # Skip invalid entries
                        subject = str(email["subject"])[:1000]  # Limit subject length
                        content = str(email["content"])[:10000]  # Limit content length
                        try:
                            result = nlp_engine.analyze_email(subject, content)
                            results.append(result)
                        except Exception as e:
                            results.append({"error": f"Failed to analyze email: {str(e)}"})
                    df = pd.DataFrame(results)
                    stats = df.describe(include="all").to_dict()
                    return df, stats
                except json.JSONDecodeError as e:
                    return pd.DataFrame(), {"error": f"Invalid JSON: {str(e)}"}
                except Exception as e:
                    return pd.DataFrame(), {"error": str(e)}

            analyze_data_button.click(
                fn=analyze_batch, inputs=data_input, outputs=[batch_output, stats_output]
            )

        with gr.TabItem("Jupyter Notebook"):
            gr.Markdown("### Interactive Jupyter Analysis")
            gr.Markdown("For advanced scientific analysis, launch Jupyter Notebook.")
            gr.Markdown(
                "Run: `jupyter notebook backend/python_backend/notebooks/email_analysis.ipynb`"
            )
            launch_jupyter_button = gr.Button("Launch Jupyter (External)")
            launch_jupyter_button.click(
                fn=lambda: "Jupyter launched externally. Check terminal.",
                inputs=[],
                outputs=gr.Textbox(label="Status"),
            )


# To launch this app, you can run this file directly.
if __name__ == "__main__":
    iface.launch()
=======
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d
