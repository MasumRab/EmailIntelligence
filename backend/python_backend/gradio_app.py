<<<<<<< HEAD
import contextlib
import io
import json
from typing import Any, Dict, List
=======
"""
A Gradio web interface for interactively testing the Email Intelligence NLP Engine.

This script launches a simple web UI that allows users to input an email's
subject and content and view the AI analysis results in real-time. It's a
useful tool for debugging, demonstration, and manual testing of the NLP
capabilities.
"""
>>>>>>> main

import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
<<<<<<< HEAD
import requests
import seaborn as sns

# For safe sandboxed code execution
from RestrictedPython import compile_restricted_exec, safe_globals

from backend.python_nlp.nlp_engine import NLPEngine

# Initialize the NLP Engine
nlp_engine = NLPEngine()
=======
import json
import seaborn as sns
import requests
from typing import Dict, Any, List

# Define a base URL for the API
BASE_URL = "http://127.0.0.1:8000"
>>>>>>> main


def analyze_email_interface(subject, content):
    """
    Analyzes email subject and content by calling the FastAPI endpoint.
    """
    if not subject and not content:
        return {"error": "Subject and content cannot both be empty."}
<<<<<<< HEAD

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
=======
    
    try:
        response = requests.post(f"{BASE_URL}/api/ai/analyze", json={"subject": subject, "content": content})
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to analyze email. Status code: {response.status_code}, Response: {response.text}"}
    except Exception as e:
        return {"error": f"An exception occurred: {str(e)}"}
>>>>>>> main


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


def get_emails_list(category_id=None, search=None):
    """Fetch emails from API with optional filters"""
    try:
        params = {}
        if category_id is not None:
            params['category_id'] = category_id
        if search:
            params['search'] = search
        response = requests.get("http://127.0.0.1:8000/api/emails", params=params)
        if response.status_code == 200:
            emails = response.json()
            # Convert to list of lists for Dataframe
            data = []
            for email in emails:
                data.append([
                    email['id'],
                    email['time'][:19],  # Truncate datetime
                    email['sender'],
                    email['subject'],
                    email.get('category', ''),
                    'Read' if not email.get('isUnread', True) else 'Unread'
                ])
            return data
        return []
    except Exception:
        return []


def get_categories():
    """Fetch categories from API"""
    try:
        response = requests.get("http://127.0.0.1:8000/api/categories")
        if response.status_code == 200:
            cats = response.json()
            return {cat['name']: cat['id'] for cat in cats}
        return {}
    except Exception:
        return {}


def get_email_details(email_id):
    """Fetch detailed email by ID"""
    try:
        response = requests.get(f"http://127.0.0.1:8000/api/emails/{email_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None


def update_email(email_id, updates):
    """Update email via API"""
    try:
        response = requests.put(f"http://127.0.0.1:8000/api/emails/{email_id}", json=updates)
        return response.status_code == 200
    except Exception:
        return False


# Create the Gradio interface
with gr.Blocks(title="Email Intelligence", theme=gr.themes.Soft()) as iface:
    gr.Markdown("## Email Intelligence Platform")

    with gr.Tabs():
        with gr.TabItem("📈 Dashboard"):
            # ... (Implementation from previous step)

        with gr.TabItem("📥 Inbox"):
            gr.Markdown("## Inbox")
            email_df = gr.DataFrame(headers=["ID", "Subject", "From", "Date"], interactive=True, label="Emails")
            
            with gr.Row():
<<<<<<< HEAD
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
=======
                category_filter = gr.Dropdown(label="Filter by Category")
                search_box = gr.Textbox(label="Search")
                refresh_inbox_btn = gr.Button("Refresh Inbox")

            with gr.Row():
                with gr.Column():
                    selected_subject = gr.Textbox(label="Subject", interactive=False)
                    selected_from = gr.Textbox(label="From", interactive=False)
                    selected_content = gr.Textbox(label="Content", lines=10, interactive=False)
                with gr.Column():
                    gr.Markdown("### AI Analysis")
                    selected_analysis = gr.JSON(label="Full Analysis")
                    is_important_output = gr.Markdown(label="Importance")

            def get_emails(category=None, search=None):
                try:
                    params = {}
                    if category and category != "All":
                        cat_response = requests.get(f"{BASE_URL}/api/categories")
                        if cat_response.status_code == 200:
                            cats = {c['name']: c['id'] for c in cat_response.json()}
                            if category in cats:
                                params["category_id"] = cats[category]
                    if search:
                        params["search"] = search

                    response = requests.get(f"{BASE_URL}/api/emails", params=params)
                    if response.status_code == 200:
                        emails = response.json()
                        df = pd.DataFrame(emails)
                        if not df.empty:
                            return df[["id", "subject", "sender", "time"]]
                        else:
                            return pd.DataFrame()
                    return pd.DataFrame()
                except Exception as e:
                    return pd.DataFrame()

            def get_categories():
                try:
                    response = requests.get(f"{BASE_URL}/api/categories")
                    if response.status_code == 200:
                        categories = [c["name"] for c in response.json()]
                        return ["All"] + categories
                    return ["All"]
                except:
                    return ["All"]

            def on_select(evt: gr.SelectData):
                email_id = evt.value[0] # Assuming the first column is ID
                response = requests.get(f"{BASE_URL}/api/emails/{email_id}")
                if response.status_code == 200:
                    email = response.json()
                    is_important = email["aiAnalysis"].get("isImportant", False)
                    importance_icon = "⭐ Important" if is_important else "Not Important"
                    return email["subject"], email["sender"], email["content"], email["aiAnalysis"], importance_icon
                return "", "", "", {}, ""

            iface.load(fn=get_categories, outputs=category_filter)
            iface.load(fn=get_emails, outputs=email_df)
            refresh_inbox_btn.click(fn=get_emails, inputs=[category_filter, search_box], outputs=email_df)
            category_filter.change(fn=get_emails, inputs=[category_filter, search_box], outputs=email_df)
            search_box.submit(fn=get_emails, inputs=[category_filter, search_box], outputs=email_df)
            email_df.select(fn=on_select, outputs=[selected_subject, selected_from, selected_content, selected_analysis, is_important_output])

        with gr.TabItem("📧 Gmail"):
            # ... (Implementation from previous step)

        with gr.TabItem("🔬 AI Lab"):
            gr.Markdown("## AI Lab: Advanced Tools")
            with gr.Tabs():
                with gr.TabItem("Single Email Analysis"):
                    # ... (Implementation from previous step)

                with gr.TabItem("Batch Analysis"):
                    gr.Markdown("### Advanced Data Analysis with Pandas & Stats")
                    data_input = gr.Textbox(label="Paste Email Data (JSON format)", lines=5, placeholder='[{"subject": "Test", "content": "Test content"}]')
                    analyze_data_button = gr.Button("Analyze Batch")
                    batch_output = gr.Dataframe(label="Batch Analysis Results")
                    stats_output = gr.JSON(label="Descriptive Statistics")
                    viz_output = gr.Plot(label="Sentiment Distribution")

                    def analyze_batch(data_str):
                        try:
                            emails = json.loads(data_str)
                            results = []
                            for email in emails:
                                # In a real implementation, this should call the /api/ai/analyze endpoint for each email
                                result = analyze_email_interface(email["subject"], email["content"])
                                results.append(result)
                            df = pd.DataFrame(results)
                            stats = df.describe(include="all").to_dict()
                            sentiment_counts = df["sentiment"].value_counts()
                            fig = px.bar(sentiment_counts, title="Sentiment Distribution")
                            return df, stats, fig
                        except Exception as e:
                            return pd.DataFrame(), {"error": str(e)}, px.bar(title="Error")

                    analyze_data_button.click(fn=analyze_batch, inputs=data_input, outputs=[batch_output, stats_output, viz_output])

                with gr.TabItem("Model Management"):
                    gr.Markdown("### AI Model Management")
                    with gr.Row():
                        with gr.Column():
                            model_list = gr.Dataframe(headers=["Name", "Status", "Size (MB)", "Load Time (s)"], label="Available Models", interactive=False)
                            refresh_models_btn = gr.Button("Refresh Models")
>>>>>>> main

                    with gr.Row():
                        model_selector = gr.Dropdown([], label="Select Model")
                        load_model_btn = gr.Button("Load Model")
                        unload_model_btn = gr.Button("Unload Model")

                    model_status_output = gr.Textbox(label="Status", interactive=False)
<<<<<<< HEAD

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
=======

                    def refresh_models():
                        try:
                            response = requests.get(f"{BASE_URL}/api/models")
                            if response.status_code == 200:
                                models = response.json()
                                data = [[m.get('name'), m.get('status'), m.get('size_mb'), m.get('load_time')] for m in models]
                                names = [m.get('name') for m in models]
                                return data, gr.Dropdown.update(choices=names)
                            return [], gr.Dropdown.update(choices=[])
                        except Exception as e:
                            return [], gr.Dropdown.update(choices=[])
>>>>>>> main

                    def load_selected_model(model_name):
                        if not model_name:
                            return "Please select a model first"
                        try:
                            response = requests.post(f"{BASE_URL}/api/models/{model_name}/load")
                            return response.json().get("message", "Error")
                        except Exception as e:
                            return str(e)

                    def unload_selected_model(model_name):
                        if not model_name:
                            return "Please select a model first"
                        try:
                            response = requests.post(f"{BASE_URL}/api/models/{model_name}/unload")
                            return response.json().get("message", "Error")
                        except Exception as e:
                            return str(e)

                    refresh_models_btn.click(fn=refresh_models, outputs=[model_list, model_selector])
                    load_model_btn.click(fn=load_selected_model, inputs=model_selector, outputs=model_status_output)
                    unload_model_btn.click(fn=unload_selected_model, inputs=model_selector, outputs=model_status_output)

                with gr.TabItem("Advanced"):
                    gr.Markdown("### Jupyter & Custom Code")
                    gr.Markdown("For advanced scientific analysis, launch Jupyter Notebook: `jupyter notebook backend/python_backend/notebooks/email_analysis.ipynb`")
                    with gr.Accordion("Custom Code Execution", open=False):
                        code_input = gr.Code(label="Python Code", language="python", value='import pandas as pd\ndata = [{"subject": "Hello", "content": "World"}]\ndf = pd.DataFrame(data)\nprint(df.head())')
                        run_code_button = gr.Button("Run Code")
                        code_output = gr.Textbox(label="Output", lines=10)

                        def run_custom_code(code):
                            # This is a sandboxed execution and should be used with caution.
                            # In a real production app, this would need extreme security measures.
                            try:
                                from io import StringIO
                                import sys
                                old_stdout = sys.stdout
                                sys.stdout = captured_output = StringIO()
                                exec(code, {'pd': pd, 'np': np, 'plt': plt, 'sns': sns})
                                sys.stdout = old_stdout
                                return captured_output.getvalue()
                            except Exception as e:
                                return str(e)

                        run_code_button.click(fn=run_custom_code, inputs=code_input, outputs=code_output)

        with gr.TabItem("⚙️ System Status"):
            gr.Markdown("## System Performance & Health")
            with gr.Row():
<<<<<<< HEAD
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

        with gr.TabItem("Email Retrieval & Filtering"):
            gr.Markdown("### Interactive Email Retrieval and Filtering")
            gr.Markdown("Search, filter, and manage your emails.")

            # Search and filters
            with gr.Row():
                search_box = gr.Textbox(label="Search", placeholder="Search subject, sender, content...")
                category_filter = gr.Dropdown(["All"], label="Category", value="All")
                read_filter = gr.Dropdown(["All", "Read", "Unread"], label="Read Status", value="All")
                search_btn = gr.Button("Search", variant="primary")

            # Email list
            email_table = gr.Dataframe(
                headers=["ID", "Date", "Sender", "Subject", "Category", "Status"],
                label="Emails",
                interactive=False,
                value=[]
            )

            # Pagination
            with gr.Row():
                prev_btn = gr.Button("Previous")
                page_input = gr.Number(label="Page", value=1, minimum=1, precision=0)
                next_btn = gr.Button("Next")
                page_size = gr.Number(label="Page Size", value=20, minimum=1, maximum=100, precision=0)

            # Details view
            selected_email_id = gr.State()
            details_view = gr.JSON(label="Selected Email Details")

            # Actions
            with gr.Row():
                mark_read_btn = gr.Button("Mark as Read")
                mark_unread_btn = gr.Button("Mark as Unread")
                change_category_dropdown = gr.Dropdown(["All"], label="Change Category")
                change_category_btn = gr.Button("Change Category")
                reanalyze_btn = gr.Button("Re-analyze")

            # State for all emails and current page
            all_emails_state = gr.State([])
            current_page_state = gr.State(1)

            # Load initial data
            def load_initial_data():
                cats = get_categories()
                cat_options = ["All"] + list(cats.keys())
                emails = get_emails_list()
                displayed = emails[:20]
                return emails, displayed, cat_options, cat_options[1:] if len(cat_options) > 1 else [], 1

            all_emails_state.value, email_table.value, category_filter.choices, change_category_dropdown.choices, current_page_state.value = load_initial_data()

            # Search function
            def search_emails(search, category, read_status, page_size_val):
                cat_id = None
                if category and category != "All":
                    cats = get_categories()
                    cat_id = cats.get(category)
                emails = get_emails_list(category_id=cat_id, search=search if search else None)
                # Filter by read status
                if read_status == "Read":
                    emails = [e for e in emails if e[5] == "Read"]
                elif read_status == "Unread":
                    emails = [e for e in emails if e[5] == "Unread"]
                # Paginate
                start = 0
                end = min(page_size_val, len(emails))
                displayed = emails[start:end]
                return emails, displayed, 1, 1

            search_btn.click(
                fn=search_emails,
                inputs=[search_box, category_filter, read_filter, page_size],
                outputs=[all_emails_state, email_table, current_page_state, page_input]
            )

            # Pagination functions
            def go_to_page(all_emails, page, page_size_val, direction):
                total_pages = max(1, (len(all_emails) + page_size_val - 1) // page_size_val)
                new_page = page + direction
                new_page = max(1, min(total_pages, new_page))
                start = (new_page - 1) * page_size_val
                end = start + page_size_val
                displayed = all_emails[start:end]
                return displayed, new_page, new_page

            prev_btn.click(
                fn=lambda all_emails, page, page_size_val: go_to_page(all_emails, page, page_size_val, -1),
                inputs=[all_emails_state, current_page_state, page_size],
                outputs=[email_table, current_page_state, page_input]
            )

            next_btn.click(
                fn=lambda all_emails, page, page_size_val: go_to_page(all_emails, page, page_size_val, 1),
                inputs=[all_emails_state, current_page_state, page_size],
                outputs=[email_table, current_page_state, page_input]
            )

            def change_page(all_emails, page, page_size_val):
                start = (page - 1) * page_size_val
                end = start + page_size_val
                displayed = all_emails[start:end]
                return displayed, page

            page_input.change(
                fn=change_page,
                inputs=[all_emails_state, page_input, page_size],
                outputs=[email_table, current_page_state]
            )

            # Select email for details
            def select_email(evt: gr.SelectData, all_emails):
                if evt.index[0] < len(all_emails):
                    email_id = all_emails[evt.index[0]][0]
                    details = get_email_details(email_id)
                    return email_id, details
                return None, None

            email_table.select(
                fn=select_email,
                inputs=[all_emails_state],
                outputs=[selected_email_id, details_view]
            )

            # Action functions
            def mark_read_unread(email_id, is_unread, search, category, read_status, page_size_val):
                if email_id:
                    success = update_email(email_id, {"isUnread": is_unread})
                    if success:
                        # Refresh search
                        return search_emails(search, category, read_status, page_size_val)
                return all_emails_state.value, email_table.value, current_page_state.value, page_input.value

            mark_read_btn.click(
                fn=lambda email_id, search, category, read_status, page_size_val: mark_read_unread(email_id, False, search, category, read_status, page_size_val),
                inputs=[selected_email_id, search_box, category_filter, read_filter, page_size],
                outputs=[all_emails_state, email_table, current_page_state, page_input]
            )

            mark_unread_btn.click(
                fn=lambda email_id, search, category, read_status, page_size_val: mark_read_unread(email_id, True, search, category, read_status, page_size_val),
                inputs=[selected_email_id, search_box, category_filter, read_filter, page_size],
                outputs=[all_emails_state, email_table, current_page_state, page_input]
            )

            def change_category(email_id, new_category, search, category, read_status, page_size_val):
                if email_id and new_category and new_category != "All":
                    cats = get_categories()
                    cat_id = cats.get(new_category)
                    if cat_id is not None:
                        success = update_email(email_id, {"categoryId": cat_id})
                        if success:
                            return search_emails(search, category, read_status, page_size_val)
                return all_emails_state.value, email_table.value, current_page_state.value, page_input.value

            change_category_btn.click(
                fn=change_category,
                inputs=[selected_email_id, change_category_dropdown, search_box, category_filter, read_filter, page_size],
                outputs=[all_emails_state, email_table, current_page_state, page_input]
            )

            # Re-analyze: for now, just trigger update without changes (assuming workflow re-runs)
            reanalyze_btn.click(
                fn=lambda email_id: update_email(email_id, {}) if email_id else False,
                inputs=[selected_email_id],
                outputs=[]
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
=======
                refresh_health_btn = gr.Button("Refresh Health Status")
            health_output = gr.JSON(label="System Health")

            def get_system_health():
                try:
                    response = requests.get(f"{BASE_URL}/health")
                    if response.status_code == 200:
                        return response.json()
                    return {"status": "unhealthy", "reason": f"API returned status {response.status_code}"}
                except Exception as e:
                    return {"status": "unhealthy", "reason": str(e)}
            
            refresh_health_btn.click(fn=get_system_health, outputs=health_output)
>>>>>>> main
