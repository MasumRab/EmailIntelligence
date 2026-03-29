import gradio as gr
import pandas as pd
import json
import asyncio
from src.core.factory import get_data_source
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

async def analyze_batch_emails(emails_data: str):
    """
    Analyze a batch of emails provided in JSON format.
    """
    try:
        # Parse the JSON input
        emails = json.loads(emails_data)
        
        if not isinstance(emails, list):
            return pd.DataFrame(), {"error": "Input must be a JSON array of email objects"}
        
        if len(emails) > 100:
            return pd.DataFrame(), {"error": "Too many emails, maximum 100 allowed"}
        
        results = []
        
        # Get the data source
        data_source = await get_data_source()
        
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
                # Use AI engine for analysis
                if hasattr(data_source, 'ai_engine') and data_source.ai_engine:
                    ai_engine = data_source.ai_engine
                    full_text = f"{subject} {content}"
                    
                    # Perform comprehensive analysis
                    analysis_result = {}
                    
                    # Sentiment analysis
                    try:
                        sentiment = ai_engine.analyze_sentiment(full_text)
                        analysis_result["sentiment"] = sentiment
                    except Exception as e:
                        logger.warning(f"Sentiment analysis failed: {e}")
                        analysis_result["sentiment"] = {"label": "unknown", "confidence": 0.0}
                    
                    # Topic classification
                    try:
                        topics = ai_engine.classify_topic(full_text)
                        analysis_result["topic"] = topics
                    except Exception as e:
                        logger.warning(f"Topic classification failed: {e}")
                        analysis_result["topic"] = ["General"]
                    
                    # Intent recognition
                    try:
                        intent = ai_engine.recognize_intent(full_text)
                        analysis_result["intent"] = intent
                    except Exception as e:
                        logger.warning(f"Intent recognition failed: {e}")
                        analysis_result["intent"] = {"type": "unknown", "confidence": 0.0}
                    
                    # Urgency detection
                    try:
                        urgency = ai_engine.detect_urgency(full_text)
                        analysis_result["urgency"] = urgency
                    except Exception as e:
                        logger.warning(f"Urgency detection failed: {e}")
                        analysis_result["urgency"] = {"level": "unknown", "confidence": 0.0}
                    
                    # Add to results
                    result_entry = {
                        "subject": subject,
                        "topic": analysis_result.get("topic", ["General"])[0] if isinstance(analysis_result.get("topic"), list) else analysis_result.get("topic", "General"),
                        "sentiment": analysis_result.get("sentiment", {}).get("label", "unknown"),
                        "intent": analysis_result.get("intent", {}).get("type", "unknown"),
                        "urgency": analysis_result.get("urgency", {}).get("level", "unknown")
                    }
                    
                    results.append(result_entry)
                else:
                    # Fallback if no AI engine available
                    results.append({
                        "subject": subject,
                        "topic": "General",
                        "sentiment": "neutral",
                        "intent": "unknown",
                        "urgency": "low"
                    })
                    
            except Exception as e:
                logger.error(f"Failed to analyze email: {e}")
                results.append({"error": f"Failed to analyze email: {str(e)}"})
        
        # Create DataFrame from results
        if results:
            df = pd.DataFrame(results)
        else:
            df = pd.DataFrame(columns=["subject", "topic", "sentiment", "intent", "urgency"])
        
        # Generate basic statistics
        if not df.empty:
            stats = df.describe(include='all').to_dict()
        else:
            stats = {"error": "No valid results to analyze"}
        
        return df, stats
        
    except json.JSONDecodeError as e:
        return pd.DataFrame(), {"error": f"Invalid JSON: {str(e)}"}
    except Exception as e:
        return pd.DataFrame(), {"error": f"An error occurred: {str(e)}"}

def create_scientific_ui():
    """Creates the scientific analysis UI components."""
    with gr.Blocks() as scientific_tab:
        gr.Markdown("# 🔬 Scientific Analysis")
        gr.Markdown("## Advanced data analysis for email intelligence")
        
        gr.Markdown("""
        ### Batch Email Analysis
        
        Analyze multiple emails at once using JSON format:
        
        ```
        [
          {
            "subject": "Email subject",
            "content": "Email content"
          },
          {
            "subject": "Another email subject",
            "content": "Another email content"
          }
        ]
        ```
        """)
        
        with gr.Row():
            with gr.Column():
                data_input = gr.Textbox(
                    label="Paste Email Data (JSON format)",
                    lines=10,
                    placeholder='[{"subject": "Test", "content": "Test content"}]',
                    value='[\n  {\n    "subject": "Project Update",\n    "content": "The project is progressing well and we are on schedule."\n  },\n  {\n    "subject": "Meeting Reminder",\n    "content": "This is to remind you about the meeting tomorrow."\n  }\n]'
                )
                analyze_data_button = gr.Button("Analyze Batch", variant="primary")
                
            with gr.Column():
                batch_output = gr.Dataframe(label="Batch Analysis Results", interactive=False)
                stats_output = gr.JSON(label="Statistics")
        
        def analyze_batch_wrapper(data_str):
            """Wrapper to run async function."""
            return asyncio.run(analyze_batch_emails(data_str))
        
        # Set up event handlers
        analyze_data_button.click(
            fn=analyze_batch_wrapper,
            inputs=data_input,
            outputs=[batch_output, stats_output]
        )
    
    return scientific_tab