import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
<<<<<<< HEAD
import json
import seaborn as sns
=======
import seaborn as sns

# For safe sandboxed code execution
from RestrictedPython import compile_restricted_exec
from RestrictedPython import safe_globals
import io
import contextlib

>>>>>>> origin/main
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

    # Define charts for cross-tab updates
    sentiment_chart = gr.Plot(label="Sentiment Gauge")
    topic_chart = gr.Plot(label="Topic Pie Chart")

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
                    reasoning_output = gr.Textbox(label="Reasoning", lines=5)
                    keywords_output = gr.HighlightedText(label="Keywords")
                    analysis_output = gr.JSON(label="Full Analysis (JSON)")

            def update_outputs(subject, content):
                result = analyze_email_interface(subject, content)
                if "error" in result:
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
                fn=update_outputs,
                inputs=[email_subject, email_content],
                outputs=[topic_output, sentiment_output, reasoning_output, keywords_output, analysis_output, sentiment_chart, topic_chart]
            )

        with gr.TabItem("Visualization"):
            gr.Markdown("### Data Visualization")
            sentiment_chart
            topic_chart
            gr.Markdown("The charts above will automatically update after you analyze an email in the 'Single Email Analysis' tab.")

        with gr.TabItem("Scientific Analysis"):
            gr.Markdown("### Advanced Data Analysis with Pandas & Stats")
            data_input = gr.Textbox(label="Paste Email Data (JSON format)", lines=5, placeholder='[{"subject": "Test", "content": "Test content"}]')
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
                    stats = df.describe(include='all').to_dict()
                    # Simple viz: sentiment count
                    sentiment_counts = df['sentiment'].value_counts()
                    fig = px.bar(sentiment_counts, title="Sentiment Distribution")
                    return df, stats, fig
                except Exception as e:
                    return pd.DataFrame(), {"error": str(e)}, px.bar(title="Error")

            analyze_data_button.click(
                fn=analyze_batch,
                inputs=data_input,
                outputs=[batch_output, stats_output, viz_output]
            )

        with gr.TabItem("Jupyter Notebook"):
            gr.Markdown("### Interactive Jupyter Analysis")
            gr.Markdown("For advanced scientific analysis, launch Jupyter Notebook.")
            gr.Markdown("Run: `jupyter notebook backend/python_backend/notebooks/email_analysis.ipynb`")
            launch_jupyter_button = gr.Button("Launch Jupyter (External)")
            jupyter_status = gr.Textbox(label="Status", interactive=False)
            launch_jupyter_button.click(
                fn=lambda: "Jupyter launched externally. Check terminal for URL.",
                inputs=[],
                outputs=jupyter_status
            )

        with gr.TabItem("Custom Code Execution"):
            gr.Markdown("### Run Custom Python Code for Analysis")
            code_input = gr.Code(label="Python Code", language="python", value="""
import pandas as pd
# Example: Load sample data
data = [{"subject": "Hello", "content": "World"}]
df = pd.DataFrame(data)
print(df.head())
""")
            run_code_button = gr.Button("Run Code")
            code_output = gr.Textbox(label="Output", lines=10)

            def run_custom_code(code):
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

            run_code_button.click(
                fn=run_custom_code,
                inputs=code_input,
                outputs=code_output
            )

# To launch this app, you can run this file directly.
if __name__ == "__main__":
    print("Launching Gradio UI for Email Intelligence Analysis...")
    iface.launch()