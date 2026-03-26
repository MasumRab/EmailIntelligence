import gradio as gr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import asyncio
import logging
from typing import Dict, Any, List

from src.core.factory import get_data_source

logger = logging.getLogger(__name__)

async def analyze_email_interface(subject, content):
    """
    Analyzes email subject and content using the active AI engine.
    """
    if not subject and not content:
        return {"error": "Subject and content cannot both be empty."}

    try:
        data_source = await get_data_source()
        if hasattr(data_source, 'ai_engine') and data_source.ai_engine:
            # Use the AI engine directly
            ai_engine = data_source.ai_engine
            
            full_text = f"{subject} {content}"
            
            # Perform AI analysis
            analysis_results = {}
            
            # Sentiment analysis
            try:
                sentiment = ai_engine.analyze_sentiment(full_text)
                analysis_results["sentiment"] = sentiment
            except Exception as e:
                logger.warning(f"Sentiment analysis failed: {e}")
                analysis_results["sentiment"] = {"label": "N/A", "confidence": 0.0}
            
            # Topic classification
            try:
                topics = ai_engine.classify_topic(full_text)
                analysis_results["topics"] = topics
            except Exception as e:
                logger.warning(f"Topic classification failed: {e}")
                analysis_results["topics"] = ["General"]
            
            # Intent recognition
            try:
                intent = ai_engine.recognize_intent(full_text)
                analysis_results["intent"] = intent
            except Exception as e:
                logger.warning(f"Intent recognition failed: {e}")
                analysis_results["intent"] = {"type": "N/A", "confidence": 0.0}
            
            # Urgency detection
            try:
                urgency = ai_engine.detect_urgency(full_text)
                analysis_results["urgency"] = urgency
            except Exception as e:
                logger.warning(f"Urgency detection failed: {e}")
                analysis_results["urgency"] = {"level": "N/A", "confidence": 0.0}
            
            return analysis_results
        else:
            return {"error": "AI engine not available"}
    except Exception as e:
        logger.error(f"Error in email analysis: {e}")
        return {"error": f"An exception occurred: {str(e)}"}


def generate_sentiment_chart(sentiment_result):
    """Generate a sentiment gauge chart."""
    try:
        if isinstance(sentiment_result, dict):
            label = sentiment_result.get("label", "neutral").lower()
        else:
            label = str(sentiment_result).lower()
            
        if label == "positive":
            value = 1
        elif label == "negative":
            value = -1
        else:
            value = 0
            
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=value,
                title={"text": "Sentiment Gauge"},
                gauge={
                    "axis": {"range": [-1, 1]}, 
                    "bar": {"color": "darkblue"},
                    "steps": [
                        {"range": [-1, -0.33], "color": "red"},
                        {"range": [-0.33, 0.33], "color": "lightgray"},
                        {"range": [0.33, 1], "color": "green"}
                    ]
                },
            )
        )
        return fig
    except Exception as e:
        logger.error(f"Error generating sentiment chart: {e}")
        # Return empty figure
        return go.Figure()


def generate_topic_pie(topics_result):
    """Generate a pie chart for topics."""
    try:
        if isinstance(topics_result, list):
            topics = topics_result
        elif isinstance(topics_result, dict):
            topics = [topics_result.get("category", "General")]
        else:
            topics = ["General"]
            
        if not topics:
            topics = ["General"]
            
        # Create values for the pie chart (equal distribution for demo)
        values = [1] * len(topics)
        fig = px.pie(values=values, names=topics, title="Topic Categories")
        return fig
    except Exception as e:
        logger.error(f"Error generating topic chart: {e}")
        # Return empty figure
        return px.pie(values=[1], names=["General"], title="Topic Categories")


def create_analysis_ui():
    """Creates the single email analysis UI components."""
    with gr.Blocks() as analysis_tab:
        gr.Markdown("# Single Email Analysis")
        gr.Markdown("## Analyze individual emails for sentiment, topics, and intent")
        
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
                intent_output = gr.Label(label="Intent")
                urgency_output = gr.Label(label="Urgency")
                reasoning_output = gr.Textbox(label="Detailed Analysis", lines=5)
                keywords_output = gr.HighlightedText(label="Key Terms")
                analysis_output = gr.JSON(label="Full Analysis (JSON)")

        # Visualization section
        gr.Markdown("### Visual Analysis")
        with gr.Row():
            sentiment_chart = gr.Plot(label="Sentiment Gauge")
            topic_chart = gr.Plot(label="Topic Distribution")

        async def update_outputs(subject, content):
            """Update all outputs based on email analysis."""
            result = await analyze_email_interface(subject, content)
            
            if "error" in result:
                error_msg = result.get("error", "An error occurred.")
                return (
                    gr.update(),  # topic
                    gr.update(),  # sentiment
                    gr.update(),  # intent
                    gr.update(),  # urgency
                    error_msg,    # reasoning
                    [],           # keywords
                    result,       # analysis JSON
                    generate_sentiment_chart("neutral"),  # sentiment chart
                    generate_topic_pie(["Error"])         # topic chart
                )

            # Extract results
            topic = "General"
            topics_list = []
            if "topics" in result:
                if isinstance(result["topics"], list):
                    topics_list = result["topics"]
                    topic = topics_list[0] if topics_list else "General"
                elif isinstance(result["topics"], dict):
                    topic = result["topics"].get("category", "General")
                    topics_list = [topic]
                else:
                    topic = str(result["topics"])
                    topics_list = [topic]
            
            sentiment = "Neutral"
            sentiment_label = "neutral"
            if "sentiment" in result:
                if isinstance(result["sentiment"], dict):
                    sentiment = result["sentiment"].get("label", "Neutral")
                    sentiment_label = sentiment.lower()
                else:
                    sentiment = str(result["sentiment"])
                    sentiment_label = sentiment.lower()
            
            intent = "N/A"
            if "intent" in result:
                if isinstance(result["intent"], dict):
                    intent = result["intent"].get("type", "N/A")
                else:
                    intent = str(result["intent"])
            
            urgency = "N/A"
            if "urgency" in result:
                if isinstance(result["urgency"], dict):
                    urgency = result["urgency"].get("level", "N/A")
                else:
                    urgency = str(result["urgency"])
            
            # Extract keywords (simplified for demo)
            keywords = []
            if "sentiment" in result and isinstance(result["sentiment"], dict):
                confidence = result["sentiment"].get("confidence", 0)
                keywords.append((sentiment, f"Confidence: {confidence:.2f}"))
            
            # Create detailed reasoning
            reasoning = f"Analyzed email with {len(subject.split()) + len(content.split())} words.\n"
            reasoning += f"Detected topic: {topic}\n"
            reasoning += f"Sentiment: {sentiment}\n"
            reasoning += f"Intent: {intent}\n"
            reasoning += f"Urgency: {urgency}"
            
            # Generate charts
            sentiment_chart_fig = generate_sentiment_chart(sentiment_label)
            topic_chart_fig = generate_topic_pie(topics_list)
            
            return (
                {topic: 1.0},  # topic label format
                {sentiment: 1.0},  # sentiment label format
                {intent: 1.0},  # intent label format
                {urgency: 1.0},  # urgency label format
                reasoning,
                keywords,
                result,
                sentiment_chart_fig,
                topic_chart_fig
            )
        
        # Set up event handlers
        analyze_button.click(
            fn=lambda s, c: asyncio.run(update_outputs(s, c)),
            inputs=[email_subject, email_content],
            outputs=[
                topic_output,
                sentiment_output,
                intent_output,
                urgency_output,
                reasoning_output,
                keywords_output,
                analysis_output,
                sentiment_chart,
                topic_chart,
            ],
        )
    
    return analysis_tab