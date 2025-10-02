import gradio as gr
import logging
import plotly.graph_objects as go
from backend.python_nlp.nlp_engine import NLPEngine

# Initialize the NLP Engine
nlp_engine = NLPEngine()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sentiment_chart(analysis):
    """Creates a bar chart for sentiment polarity."""
    sentiment = analysis.get("sentiment", "neutral")
    polarity = analysis.get("details", {}).get("sentiment_analysis", {}).get("polarity", 0)

    colors = {'positive': 'green', 'negative': 'red', 'neutral': 'blue'}

    fig = go.Figure(go.Bar(
        x=[polarity],
        y=['Sentiment'],
        orientation='h',
        marker_color=colors.get(sentiment, 'grey'),
        text=[f"{sentiment.capitalize()}: {polarity:.2f}"],
        textposition='auto'
    ))
    fig.update_layout(
        title_text='Sentiment Polarity',
        xaxis_title="Polarity Score (-1 to 1)",
        yaxis_visible=False,
        xaxis=dict(range=[-1, 1])
    )
    return fig

def create_topic_chart(analysis):
    """Creates a pie chart for topic confidence."""
    topic_details = analysis.get("details", {}).get("topic_analysis", {})
    topic = topic_details.get("topic", "N/A")
    confidence = topic_details.get("confidence", 0)

    labels = [topic.replace("_", " ").title(), 'Other']
    values = [confidence, 1 - confidence]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text='Topic Confidence')
    return fig

def analyze_email_interface(subject, content):
    """
    Analyzes email subject and content, returning values for all UI components.
    """
    empty_str = ""
    empty_fig = go.Figure()
    error_json = {"error": "An error occurred. See logs for details."}

    if not subject and not content:
        error_json["error"] = "Subject and content cannot both be empty."
        return error_json, empty_str, empty_str, empty_str, empty_str, empty_str, empty_fig, empty_fig

    try:
        logger.info("Analyzing email...")
        analysis_result = nlp_engine.analyze_email(subject, content)
        if not analysis_result:
            logger.error("Analysis returned None or empty result.")
            return error_json, empty_str, empty_str, empty_str, empty_str, empty_str, empty_fig, empty_fig

        logger.info("Analysis complete. Formatting output for UI.")
        topic = analysis_result.get("topic", "N/A")
        sentiment = analysis_result.get("sentiment", "N/A")
        intent = analysis_result.get("intent", "N/A")
        urgency = analysis_result.get("urgency", "N/A")
        reasoning = analysis_result.get("reasoning", "N/A")

        sentiment_chart = create_sentiment_chart(analysis_result)
        topic_chart = create_topic_chart(analysis_result)

        return analysis_result, topic, sentiment, intent, urgency, reasoning, sentiment_chart, topic_chart
    except Exception as e:
        logger.error(f"Error in Gradio interface: {e}", exc_info=True)
        error_json["error"] = f"An exception occurred: {e}"
        return error_json, empty_str, empty_str, empty_str, empty_str, empty_str, empty_fig, empty_fig

# Create the Gradio interface
with gr.Blocks(title="Email Intelligence Analysis", theme=gr.themes.Soft()) as iface:
    gr.Markdown("## Email Intelligence Analysis UI")
    gr.Markdown("Enter the subject and content of an email to analyze its sentiment, topic, intent, and urgency.")

    with gr.Row():
        with gr.Column(scale=2):
            email_subject = gr.Textbox(label="Email Subject", placeholder="Enter email subject...")
            email_content = gr.Textbox(label="Email Content", lines=10, placeholder="Enter email content...")
            analyze_button = gr.Button("Analyze Email", variant="primary")

    with gr.Tabs():
        with gr.TabItem("Analysis Summary"):
            with gr.Row():
                with gr.Column(scale=1):
                    topic_output = gr.Textbox(label="Topic", interactive=False)
                    sentiment_output = gr.Textbox(label="Sentiment", interactive=False)
                    intent_output = gr.Textbox(label="Intent", interactive=False)
                    urgency_output = gr.Textbox(label="Urgency", interactive=False)
                with gr.Column(scale=2):
                    reasoning_output = gr.Textbox(label="Reasoning", lines=8, interactive=False)
            gr.Markdown("### Full Analysis (JSON)")
            analysis_output_json = gr.JSON(label="AI Analysis")

        with gr.TabItem("Visualizations"):
            with gr.Row():
                sentiment_plot = gr.Plot(label="Sentiment Analysis")
                topic_plot = gr.Plot(label="Topic Analysis")

    outputs = [
        analysis_output_json,
        topic_output,
        sentiment_output,
        intent_output,
        urgency_output,
        reasoning_output,
        sentiment_plot,
        topic_plot,
    ]
    analyze_button.click(
        fn=analyze_email_interface,
        inputs=[email_subject, email_content],
        outputs=outputs
    )

# To launch this app, you can run this file directly.
if __name__ == "__main__":
    print("Launching Gradio UI for Email Intelligence Analysis...")
    iface.launch()