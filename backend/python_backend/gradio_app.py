import contextlib
import io
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

# For safe sandboxed code execution
from RestrictedPython import compile_restricted_exec, safe_globals

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


def get_models():
    """Placeholder for getting models - in a real implementation, this would connect to ModelManager"""
    try:
        response = requests.get("http://127.0.0.1:8000/api/models")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        # Return mock data if connection fails
        return [
            {"name": "sentiment-default", "status": "loaded", "size_mb": 15.2, "load_time": 1.2},
            {"name": "topic-default", "status": "unloaded", "size_mb": 22.1, "load_time": None},
        ]


def load_model(model_name):
    """Placeholder for loading a model"""
    try:
        response = requests.post(f"http://127.0.0.1:8000/api/models/{model_name}/load")
        if response.status_code == 200:
            return f"Model {model_name} loaded successfully"
        return f"Failed to load model {model_name}"
    except Exception:
        return f"Failed to connect to API to load model {model_name}"


def list_workflows():
    """Placeholder for listing workflows"""
    try:
        response = requests.get("http://127.0.0.1:8000/api/workflows")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        # Return mock data if connection fails
        return ["default_workflow", "custom_workflow"]


def create_workflow(name, description):
    """Placeholder for creating a workflow"""
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/workflows", json={"name": name, "description": description}
        )
        if response.status_code == 200:
            return f"Workflow {name} created successfully"
        return f"Failed to create workflow {name}"
    except Exception:
        return f"Failed to connect to API to create workflow {name}"


def get_system_stats():
    """Placeholder for getting system stats"""
    try:
        response = requests.get("http://127.0.0.1:8000/api/enhanced/performance/system-stats")
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception:
        return {"cpu_usage": 0.0, "memory_usage": 0.0, "disk_usage": 0.0}


def get_performance_metrics(minutes):
    """Placeholder for getting performance metrics"""
    try:
        response = requests.get(
            f"http://127.0.0.1:8000/api/enhanced/performance/metrics?minutes={minutes}"
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []


# Create the Gradio interface
with gr.Blocks(title="Email Intelligence Analysis", theme=gr.themes.Soft()) as iface:
    gr.Markdown("## Email Intelligence Analysis UI (Scientific Branch)")
    gr.Markdown("Analyze emails with AI and visualize results for research purposes.")

    # Define charts for cross-tab updates
    sentiment_chart = gr.Plot(label="Sentiment Gauge")
    topic_chart = gr.Plot(label="Topic Pie Chart")

    with gr.Tabs():
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
            sentiment_chart
            topic_chart
            gr.Markdown(
                "The charts above will automatically update after you analyze an email in the 'Single Email Analysis' tab."
            )

        with gr.TabItem("Scientific Analysis"):
            gr.Markdown("### Advanced Data Analysis with Pandas & Stats")
            data_input = gr.Textbox(
                label="Paste Email Data (JSON format)",
                lines=5,
                placeholder='[{"subject": "Test", "content": "Test content"}]',
            )
            analyze_data_button = gr.Button("Analyze Batch")
            batch_output = gr.Dataframe(label="Batch Analysis Results")
            stats_output = gr.JSON(label="Descriptive Statistics")
            viz_output = gr.Plot(label="Sentiment Distribution")

            def analyze_batch(data_str):
                try:
                    emails = eval(data_str)  # Simple eval for demo; use json.loads in prod
                    results = []
                    for email in emails:
                        result = nlp_engine.analyze_email(email["subject"], email["content"])
                        results.append(result)
                    df = pd.DataFrame(results)
                    stats = df.describe(include="all").to_dict()
                    # Simple viz: sentiment count
                    sentiment_counts = df["sentiment"].value_counts()
                    fig = px.bar(sentiment_counts, title="Sentiment Distribution")
                    return df, stats, fig
                except Exception as e:
                    return pd.DataFrame(), {"error": str(e)}, px.bar(title="Error")

            analyze_data_button.click(
                fn=analyze_batch,
                inputs=data_input,
                outputs=[batch_output, stats_output, viz_output],
            )

        with gr.TabItem("Jupyter Notebook"):
            gr.Markdown("### Interactive Jupyter Analysis")
            gr.Markdown("For advanced scientific analysis, launch Jupyter Notebook.")
            gr.Markdown(
                "Run: `jupyter notebook backend/python_backend/notebooks/email_analysis.ipynb`"
            )
            launch_jupyter_button = gr.Button("Launch Jupyter (External)")
            jupyter_status = gr.Textbox(label="Status", interactive=False)
            launch_jupyter_button.click(
                fn=lambda: "Jupyter launched externally. Check terminal for URL.",
                inputs=[],
                outputs=jupyter_status,
            )

        with gr.TabItem("Custom Code Execution"):
            gr.Markdown("### Run Custom Python Code for Analysis")
            code_input = gr.Code(
                label="Python Code",
                language="python",
                value="""
import pandas as pd
# Example: Load sample data
data = [{"subject": "Hello", "content": "World"}]
df = pd.DataFrame(data)
print(df.head())
""",
            )
            run_code_button = gr.Button("Run Code")
            code_output = gr.Textbox(label="Output", lines=10)

            def run_custom_code(code):
                forbidden_keywords = [
                    "import os",
                    "import sys",
                    "import subprocess",
                    "import socket",
                    "import shutil",
                    "exec(",
                    "eval(",
                    "__import__",
                    "open(",
                    "input(",
                    "os.",
                    "sys.",
                    "subprocess.",
                    "shutil.",
                    "__builtins__",
                    "globals(",
                    "locals(",
                    "breakpoint(",
                ]
                for keyword in forbidden_keywords:
                    if keyword in code:
                        return f"Error: Usage of `{keyword}` is not allowed for security reasons."
                try:
                    # RestrictedPython: safely compile and exec user code
                    exec_globals = safe_globals.copy()
                    # Allow common DS packages
                    exec_globals.update({"pd": pd, "np": np, "plt": plt, "sns": sns})
                    # Capture stdout
                    output = io.StringIO()
                    byte_code = compile_restricted_exec(code)
                    with contextlib.redirect_stdout(output):
                        exec(byte_code, exec_globals)
                    result = output.getvalue()
                    return result if result.strip() else "Code executed successfully (no output)."
                except Exception as e:
                    return f"Error: {str(e)}"

            run_code_button.click(fn=run_custom_code, inputs=code_input, outputs=code_output)

        with gr.TabItem("Model Management"):
            gr.Markdown("### AI Model Management")
            with gr.Row():
                with gr.Column():
                    model_list = gr.Dataframe(
                        headers=["Name", "Status", "Size (MB)", "Load Time (s)"],
                        label="Available Models",
                        interactive=False,
                    )
                    refresh_models_btn = gr.Button("Refresh Models")

                    with gr.Row():
                        model_selector = gr.Dropdown([], label="Select Model")
                        load_model_btn = gr.Button("Load Model")
                        unload_model_btn = gr.Button("Unload Model")

                    model_status_output = gr.Textbox(label="Status", interactive=False)

            def refresh_models():
                models = get_models()
                data = []
                names = []
                for model in models:
                    data.append(
                        [
                            model["name"],
                            model["status"],
                            model["size_mb"],
                            model["load_time"] if model["load_time"] else "N/A",
                        ]
                    )
                    names.append(model["name"])
                return data, names

            def load_selected_model(model_name):
                if not model_name:
                    return "Please select a model first"
                return load_model(model_name)

            refresh_models_btn.click(
                fn=refresh_models,
                inputs=[],
                outputs=[model_list, model_selector]
            )

            load_model_btn.click(
                fn=load_selected_model, inputs=model_selector, outputs=model_status_output
            )

        with gr.TabItem("Model Training"):
            gr.Markdown("### AI Model Training")
            with gr.Row():
                with gr.Column():
                    model_name_input = gr.Textbox(
                        label="Model Name", placeholder="e.g., sentiment_classifier"
                    )
                    model_type_input = gr.Dropdown(
                        ["classification", "ner", "sentiment"],
                        label="Model Type",
                        value="classification",
                    )
                    training_data_input = gr.Textbox(
                        label="Training Data Path", placeholder="path/to/training/data.json"
                    )
                    parameters_input = gr.JSON(
                        label="Hyperparameters", value={"epochs": 10, "batch_size": 32}
                    )
                    start_training_btn = gr.Button("Start Training", variant="primary")
                    training_status = gr.Textbox(label="Training Status", interactive=False)

                with gr.Column():
                    job_id_input = gr.Textbox(
                        label="Job ID", placeholder="Enter job ID to check status"
                    )
                    check_status_btn = gr.Button("Check Status")
                    job_status_output = gr.JSON(label="Job Status")

            def start_training_job(name, model_type, data_path, params):
                try:
                    config = {
                        "model_name": name,
                        "model_type": model_type,
                        "training_data_path": data_path,
                        "parameters": params,
                    }
                    response = requests.post(
                        "http://127.0.0.1:8000/api/training/start", json=config
                    )
                    if response.status_code == 200:
                        result = response.json()
                        return f"Training started. Job ID: {result['job_id']}"
                    else:
                        return f"Error: {response.text}"
                except Exception as e:
                    return f"Failed to start training: {str(e)}"

            def check_training_status(job_id):
                if not job_id:
                    return {"error": "Please enter a job ID"}
                try:
                    response = requests.get(f"http://127.0.0.1:8000/api/training/status/{job_id}")
                    if response.status_code == 200:
                        return response.json()
                    else:
                        return {"error": f"Status {response.status_code}: {response.text}"}
                except Exception as e:
                    return {"error": str(e)}

            start_training_btn.click(
                fn=start_training_job,
                inputs=[model_name_input, model_type_input, training_data_input, parameters_input],
                outputs=training_status,
            )

            check_status_btn.click(
                fn=check_training_status, inputs=job_id_input, outputs=job_status_output
            )

        with gr.TabItem("Workflow Management"):
            gr.Markdown("### Workflow Management")
            with gr.Row():
                with gr.Column():
                    workflow_list = gr.List(label="Available Workflows", interactive=False)
                    refresh_workflows_btn = gr.Button("Refresh Workflows")

                    with gr.Row():
                        workflow_name = gr.Textbox(label="Workflow Name")
                        workflow_description = gr.Textbox(label="Description", lines=2)

                    create_workflow_btn = gr.Button("Create New Workflow")
                    workflow_status_output = gr.Textbox(label="Status", interactive=False)

            def refresh_workflows():
                workflows = list_workflows()
                return workflows

            def create_new_workflow(name, description):
                if not name:
                    return "Please enter a workflow name"
                return create_workflow(name, description)

            refresh_workflows_btn.click(fn=refresh_workflows, inputs=[], outputs=workflow_list)

            create_workflow_btn.click(
                fn=create_new_workflow,
                inputs=[workflow_name, workflow_description],
                outputs=workflow_status_output,
            )

        with gr.TabItem("Performance Monitoring"):
            gr.Markdown("### System Performance Dashboard")
            with gr.Row():
                with gr.Column():
                    system_stats = gr.JSON(label="Current System Stats")
                    refresh_stats_btn = gr.Button("Refresh Stats")

                    with gr.Row():
                        minutes_input = gr.Number(label="Minutes to analyze", value=5)
                        get_metrics_btn = gr.Button("Get Performance Metrics")

                    metrics_output = gr.Dataframe(
                        headers=["Timestamp", "Value", "Unit", "Source"],
                        label="Recent Performance Metrics",
                        interactive=False,
                    )

                    error_rate_output = gr.Number(label="Error Rate (%)")

            def refresh_system_stats():
                stats = get_system_stats()
                return stats

            def get_recent_metrics(minutes):
                metrics = get_performance_metrics(int(minutes))
                data = []
                for metric in metrics:
                    data.append(
                        [metric["timestamp"], metric["value"], metric["unit"], metric["source"]]
                    )
                return data

            def get_error_rate(minutes):
                try:
                    response = requests.get(
                        f"http://127.0.0.1:8000/api/enhanced/performance/error-rate?minutes={int(minutes)}"
                    )
                    if response.status_code == 200:
                        rate = response.json()
                        return rate * 100  # Convert to percentage
                    return 0
                except Exception:
                    return 0

            refresh_stats_btn.click(fn=refresh_system_stats, inputs=[], outputs=system_stats)

            get_metrics_btn.click(
                fn=get_recent_metrics, inputs=minutes_input, outputs=metrics_output
            )

            get_metrics_btn.click(
                fn=get_error_rate, inputs=minutes_input, outputs=error_rate_output
            )



# To launch this app, you can run this file directly.
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gradio UI for Email Intelligence Analysis")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the Gradio UI on")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind the Gradio UI to")
    parser.add_argument("--share", action="store_true", help="Create a public sharing link")

    args = parser.parse_args()

    print(f"Launching Gradio UI for Email Intelligence Analysis on {args.host}:{args.port}...")
    iface.launch(server_name=args.host, server_port=args.port, share=args.share)
