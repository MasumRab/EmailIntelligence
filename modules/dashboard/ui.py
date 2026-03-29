import gradio as gr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def create_dashboard_ui():
    """Creates the dashboard UI components."""
    with gr.Blocks() as dashboard_tab:
        gr.Markdown("# Dashboard")
        gr.Markdown("## Email Intelligence Platform Overview")
        
        # Stats cards
        with gr.Row():
            with gr.Column():
                total_emails = gr.Number(label="Total Emails", value=0)
            with gr.Column():
                unread_emails = gr.Number(label="Unread Emails", value=0)
            with gr.Column():
                categories_count = gr.Number(label="Categories", value=0)
            with gr.Column():
                today_emails = gr.Number(label="Emails Today", value=0)
        
        # Charts row
        with gr.Row():
            with gr.Column():
                sentiment_chart = gr.Plot(label="Sentiment Analysis")
            with gr.Column():
                category_chart = gr.Plot(label="Email Categories")
        
        # Recent emails
        with gr.Row():
            recent_emails = gr.DataFrame(
                headers=["Subject", "From", "Date", "Category", "Sentiment"],
                label="Recent Emails",
                interactive=False
            )
        
        # Refresh button
        refresh_btn = gr.Button("Refresh Dashboard")
        
        def generate_sentiment_chart():
            """Generate a sample sentiment chart."""
            # Sample data - in real implementation, this would come from the database
            sentiments = ["Positive", "Negative", "Neutral"]
            counts = [45, 25, 30]
            
            fig = px.pie(values=counts, names=sentiments, title="Email Sentiment Distribution")
            return fig
        
        def generate_category_chart():
            """Generate a sample category chart."""
            # Sample data - in real implementation, this would come from the database
            categories = ["Work", "Personal", "Promotions", "Social", "Updates"]
            counts = [120, 85, 65, 45, 35]
            
            fig = px.bar(x=categories, y=counts, title="Emails by Category")
            fig.update_layout(xaxis_title="Category", yaxis_title="Email Count")
            return fig
        
        def refresh_dashboard():
            """Refresh dashboard data."""
            # Sample data - in real implementation, this would fetch from the database
            stats = {
                "total": 350,
                "unread": 42,
                "categories": 12,
                "today": 18
            }
            
            recent_data = pd.DataFrame([
                {"Subject": "Project Update", "From": "boss@company.com", "Date": "2025-11-02", "Category": "Work", "Sentiment": "Positive"},
                {"Subject": "Meeting Reminder", "From": "assistant@company.com", "Date": "2025-11-02", "Category": "Work", "Sentiment": "Neutral"},
                {"Subject": "Family Gathering", "From": "mom@gmail.com", "Date": "2025-11-01", "Category": "Personal", "Sentiment": "Positive"},
                {"Subject": "Special Offer", "From": "store@example.com", "Date": "2025-11-01", "Category": "Promotions", "Sentiment": "Neutral"},
                {"Subject": "Friend Request", "From": "friend@social.com", "Date": "2025-10-31", "Category": "Social", "Sentiment": "Positive"}
            ])
            
            return (
                stats["total"],
                stats["unread"], 
                stats["categories"],
                stats["today"],
                generate_sentiment_chart(),
                generate_category_chart(),
                recent_data
            )
        
        # Set up event handlers
        refresh_btn.click(
            fn=refresh_dashboard,
            inputs=[],
            outputs=[
                total_emails,
                unread_emails,
                categories_count,
                today_emails,
                sentiment_chart,
                category_chart,
                recent_emails
            ]
        )
        
        # Initialize on load
        dashboard_tab.load(
            fn=refresh_dashboard,
            inputs=[],
            outputs=[
                total_emails,
                unread_emails,
                categories_count,
                today_emails,
                sentiment_chart,
                category_chart,
                recent_emails
            ]
        )
    
    return dashboard_tab