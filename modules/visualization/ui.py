import gradio as gr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import asyncio
from src.core.factory import get_data_source
import logging

logger = logging.getLogger(__name__)

def create_visualization_ui():
    """Creates the visualization UI components."""
    with gr.Blocks() as visualization_tab:
        gr.Markdown("# 📊 Visualization")
        gr.Markdown("## Data visualization and analytics for your email intelligence")

        with gr.Row():
            with gr.Column():
                gr.Markdown("### Email Analytics")
                email_count_chart = gr.Plot(label="Email Volume Over Time")
                sentiment_distribution = gr.Plot(label="Sentiment Distribution")

            with gr.Column():
                gr.Markdown("### Category Analytics")
                category_chart = gr.Plot(label="Email Categories")
                urgency_chart = gr.Plot(label="Urgency Levels")

        refresh_btn = gr.Button("Refresh Visualizations")

        def generate_sample_email_volume_chart():
            """Generate a sample email volume chart."""
            # Sample data - in real implementation, this would come from the database
            dates = pd.date_range(start='2025-10-01', end='2025-10-31', freq='D')
            counts = [25, 30, 15, 40, 35, 20, 28, 45, 33, 27, 38, 42, 18, 31, 29,
                     36, 44, 22, 39, 34, 26, 41, 37, 23, 32, 46, 24, 35, 40, 21, 29]

            df = pd.DataFrame({'date': dates, 'count': counts})
            fig = px.line(df, x='date', y='count', title='Email Volume Over Time')
            fig.update_layout(xaxis_title="Date", yaxis_title="Email Count")
            return fig

        def generate_sample_sentiment_chart():
            """Generate a sample sentiment distribution chart."""
            # Sample data
            sentiments = ['Positive', 'Negative', 'Neutral']
            counts = [120, 45, 85]

            fig = px.pie(values=counts, names=sentiments, title='Sentiment Distribution')
            return fig

        def generate_sample_category_chart():
            """Generate a sample category chart."""
            # Sample data
            categories = ['Work', 'Personal', 'Promotions', 'Social', 'Updates']
            counts = [145, 92, 67, 38, 29]

            fig = px.bar(x=categories, y=counts, title='Email Categories')
            fig.update_layout(xaxis_title="Category", yaxis_title="Email Count")
            return fig

        def generate_sample_urgency_chart():
            """Generate a sample urgency chart."""
            # Sample data
            levels = ['High', 'Medium', 'Low']
            counts = [32, 87, 131]

            fig = px.bar(x=levels, y=counts, title='Urgency Levels')
            fig.update_layout(xaxis_title="Urgency Level", yaxis_title="Email Count")
            return fig

        def refresh_visualizations():
            """Refresh all visualization charts."""
            return (
                generate_sample_email_volume_chart(),
                generate_sample_sentiment_chart(),
                generate_sample_category_chart(),
                generate_sample_urgency_chart()
            )

        # Set up event handlers
        refresh_btn.click(
            fn=refresh_visualizations,
            inputs=[],
            outputs=[
                email_count_chart,
                sentiment_distribution,
                category_chart,
                urgency_chart
            ]
        )

        # Initialize on load
        visualization_tab.load(
            fn=refresh_visualizations,
            inputs=[],
            outputs=[
                email_count_chart,
                sentiment_distribution,
                category_chart,
                urgency_chart
            ]
        )

    return visualization_tab