"""
A Gradio web interface for interactively testing the Email Intelligence NLP Engine.

This script launches a simple web UI that allows users to input an email's
subject and content and view the AI analysis results in real-time. It's a
useful tool for debugging, demonstration, and manual testing of the NLP
capabilities.
"""

import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import seaborn as sns
import requests
from typing import Dict, Any, List
import ast
# Define a base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def analyze_email_interface(subject, content):
    """
    Analyzes email subject and content by calling the FastAPI endpoint.
    """
    if not subject and not content:
        return {"error": "Subject and content cannot both be empty."}
    
    try:
        response = requests.post(f"{BASE_URL}/api/ai/analyze", json={"subject": subject, "content": content})
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to analyze email. Status code: {response.status_code}, Response: {response.text}"}
    except Exception as e:
        return {"error": f"An exception occurred: {str(e)}"}

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

                    with gr.Row():
                        model_selector = gr.Dropdown([], label="Select Model")
                        load_model_btn = gr.Button("Load Model")
                        unload_model_btn = gr.Button("Unload Model")

                    model_status_output = gr.Textbox(label="Status", interactive=False)

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
                            # Code execution is now strictly limited.
                            # Only allows evaluation of safe Python literals.
                            try:
                                result = ast.literal_eval(code)
                                return str(result)
                            except Exception as e:
                                return f"Error: {str(e)}"

                        run_code_button.click(fn=run_custom_code, inputs=code_input, outputs=code_output)

        with gr.TabItem("⚙️ System Status"):
            gr.Markdown("## System Performance & Health")
            with gr.Row():
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
