"""
AI Lab UI Component for Email Intelligence Platform
"""

import logging
from datetime import datetime

import gradio as gr
import requests

logger = logging.getLogger(__name__)


def create_ai_lab_tab():
    """Create the AI Lab tab for scientific exploration and model testing."""

    def analyze_email_ai_lab(subject, content, analysis_type):
        """Analyze email content using AI models."""
        if not subject and not content:
            return {"error": "Subject and content cannot both be empty."}, "", ""

        try:
            # Call the AI analysis endpoint
            response = requests.post(
                "http://127.0.0.1:8000/api/ai/analyze",
                json={"subject": subject, "content": content},
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()

                # Format results based on analysis type
                if analysis_type == "sentiment":
                    sentiment = result.get("sentiment", "unknown")
                    confidence = result.get("sentiment_confidence", 0)
                    return result, f"Sentiment: {sentiment} (confidence: {confidence:.2f})", ""

                elif analysis_type == "topic":
                    topic = result.get("topic", "unknown")
                    confidence = result.get("topic_confidence", 0)
                    return result, f"Topic: {topic} (confidence: {confidence:.2f})", ""

                elif analysis_type == "intent":
                    intent = result.get("intent", "unknown")
                    confidence = result.get("intent_confidence", 0)
                    return result, f"Intent: {intent} (confidence: {confidence:.2f})", ""

                elif analysis_type == "comprehensive":
                    summary = f"""
                    Sentiment: {result.get('sentiment', 'unknown')} ({result.get('sentiment_confidence', 0):.2f})
                    Topic: {result.get('topic', 'unknown')} ({result.get('topic_confidence', 0):.2f})
                    Intent: {result.get('intent', 'unknown')} ({result.get('intent_confidence', 0):.2f})
                    Urgency: {result.get('urgency', 'unknown')} ({result.get('urgency_confidence', 0):.2f})
                    """
                    return result, summary.strip(), ""

                else:
                    return result, "Analysis completed", ""

            else:
                error_msg = f"Failed to analyze email. Status: {response.status_code}"
                return {"error": error_msg}, error_msg, ""

        except Exception as e:
            error_msg = f"Analysis failed: {str(e)}"
            return {"error": error_msg}, error_msg, ""

    def batch_analyze_emails(email_texts, analysis_type):
        """Analyze multiple emails in batch."""
        if not email_texts.strip():
            return "No email content provided", []

        try:
            emails = [email.strip() for email in email_texts.split('\n\n') if email.strip()]
            results = []

            for i, email_content in enumerate(emails[:10]):  # Limit to 10 emails
                try:
                    # Simple subject extraction (first line)
                    lines = email_content.split('\n', 1)
                    subject = lines[0] if len(lines) > 0 else f"Email {i+1}"
                    content = lines[1] if len(lines) > 1 else email_content

                    response = requests.post(
                        "http://127.0.0.1:8000/api/ai/analyze",
                        json={"subject": subject, "content": content},
                        timeout=30
                    )

                    if response.status_code == 200:
                        result = response.json()
                        results.append({
                            "email_id": i+1,
                            "subject": subject[:50] + "..." if len(subject) > 50 else subject,
                            "sentiment": result.get("sentiment", "unknown"),
                            "topic": result.get("topic", "unknown"),
                            "intent": result.get("intent", "unknown"),
                            "urgency": result.get("urgency", "unknown"),
                        })
                    else:
                        results.append({
                            "email_id": i+1,
                            "subject": subject[:50] + "..." if len(subject) > 50 else subject,
                            "error": f"API Error: {response.status_code}"
                        })

                except Exception as e:
                    results.append({
                        "email_id": i+1,
                        "subject": f"Email {i+1}",
                        "error": str(e)
                    })

            # Format results for display
            if results:
                summary = f"Analyzed {len(results)} emails successfully"
                return summary, results
            else:
                return "No emails were successfully analyzed", []

        except Exception as e:
            return f"Batch analysis failed: {str(e)}", []

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("# AI Lab")
            gr.Markdown("Advanced AI model testing and scientific exploration tools.")

    with gr.Tabs():
        with gr.TabItem("Single Analysis"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Email Analysis")
                    subject_input = gr.Textbox(label="Email Subject", placeholder="Enter email subject...")
                    content_input = gr.TextArea(label="Email Content", placeholder="Enter email content...", lines=8)
                    analysis_type = gr.Dropdown(
                        label="Analysis Type",
                        choices=["comprehensive", "sentiment", "topic", "intent", "urgency"],
                        value="comprehensive"
                    )
                    analyze_btn = gr.Button("🔍 Analyze", variant="primary")

                with gr.Column():
                    gr.Markdown("### Results")
                    raw_output = gr.JSON(label="Raw AI Output")
                    summary_output = gr.Textbox(label="Summary", interactive=False)
                    confidence_plot = gr.Plot(label="Confidence Scores")

            analyze_btn.click(
                fn=analyze_email_ai_lab,
                inputs=[subject_input, content_input, analysis_type],
                outputs=[raw_output, summary_output, confidence_plot]
            )

        with gr.TabItem("Batch Analysis"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Batch Email Analysis")
                    batch_input = gr.TextArea(
                        label="Email Batch",
                        placeholder="Paste multiple emails here, separated by blank lines...\n\nSubject: Example 1\nContent: This is the first email...\n\nSubject: Example 2\nContent: This is the second email...",
                        lines=12
                    )
                    batch_analysis_type = gr.Dropdown(
                        label="Analysis Type",
                        choices=["comprehensive", "sentiment", "topic", "intent"],
                        value="comprehensive"
                    )
                    batch_analyze_btn = gr.Button("📊 Batch Analyze", variant="primary")

                with gr.Column():
                    gr.Markdown("### Batch Results")
                    batch_summary = gr.Textbox(label="Summary", interactive=False)
                    batch_results_table = gr.Dataframe(
                        headers=["Email ID", "Subject", "Sentiment", "Topic", "Intent", "Urgency"],
                        label="Analysis Results"
                    )

            batch_analyze_btn.click(
                fn=batch_analyze_emails,
                inputs=[batch_input, batch_analysis_type],
                outputs=[batch_summary, batch_results_table]
            )

        with gr.TabItem("Model Management"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Model Status")
                    model_status = gr.JSON(label="Available Models")

                    refresh_models_btn = gr.Button("🔄 Refresh Models", variant="secondary")

                with gr.Column():
                    gr.Markdown("### Model Testing")
                    test_input = gr.Textbox(label="Test Input", placeholder="Enter text to test model...")
                    test_model_btn = gr.Button("🧪 Test Model", variant="secondary")
                    test_output = gr.JSON(label="Test Results")

            def refresh_model_status():
                """Get current model status."""
                try:
                    # This would call a model management API when implemented
                    return {"models": ["sentiment_model", "topic_model", "intent_model", "urgency_model"], "status": "active"}
                except Exception as e:
                    return {"error": f"Model status unavailable: {str(e)}"}

            refresh_models_btn.click(fn=refresh_model_status, outputs=[model_status])

            # Initialize model status
            model_status.value = refresh_model_status()
