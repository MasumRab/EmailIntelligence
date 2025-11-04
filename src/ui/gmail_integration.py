"""
Gmail Integration UI Component for Email Intelligence Platform
"""

import logging
from datetime import datetime

import gradio as gr
import requests

logger = logging.getLogger(__name__)


def create_gmail_integration_tab():
    """Create the Gmail Integration tab for sync controls and account management."""

    def sync_gmail_emails(max_emails, query_filter, include_ai):
        """Trigger Gmail synchronization."""
        try:
            payload = {
                "maxEmails": int(max_emails),
                "queryFilter": query_filter,
                "includeAIAnalysis": include_ai
            }

            response = requests.post(
                "http://127.0.0.1:8000/api/gmail/sync",
                json=payload,
                timeout=60  # Allow more time for sync
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    summary = f"""
                    ✅ Sync completed successfully!
                    📧 Processed: {result.get('processedCount', 0)} emails
                    💾 Created: {result.get('emailsCreated', 0)} new emails
                    🔗 Batch ID: {result.get('batchInfo', {}).get('batchId', 'N/A')}
                    """
                    return summary.strip(), result
                else:
                    return f"❌ Sync failed: {result.get('error', 'Unknown error')}", result
            else:
                return f"❌ API Error: {response.status_code} - {response.text}", {}

        except Exception as e:
            return f"❌ Sync failed: {str(e)}", {}

    def get_gmail_performance():
        """Get Gmail performance metrics."""
        try:
            response = requests.get("http://127.0.0.1:8000/api/gmail/performance", timeout=10)

            if response.status_code == 200:
                data = response.json()
                summary = f"""
                📊 Gmail Performance Summary:
                🔄 Total Operations: {data.get('summary', {}).get('total_sync_operations', 'N/A')}
                ✅ Success Rate: {data.get('summary', {}).get('success_rate_percent', 'N/A')}%
                ⏱️ Avg Sync Time: {data.get('summary', {}).get('average_sync_time_seconds', 'N/A')}s
                📧 Emails Processed: {data.get('summary', {}).get('total_emails_processed', 'N/A')}
                """
                return summary.strip(), data
            else:
                return f"❌ Failed to get performance data: {response.status_code}", {}

        except Exception as e:
            return f"❌ Error: {str(e)}", {}

    def get_gmail_strategies():
        """Get available Gmail retrieval strategies."""
        try:
            response = requests.get("http://127.0.0.1:8000/api/gmail/strategies", timeout=10)

            if response.status_code == 200:
                data = response.json()
                strategies = data.get("strategies", [])
                if strategies:
                    strategy_list = "\n".join([f"• {s.get('name', 'Unknown')}: {s.get('description', '')}" for s in strategies])
                    return f"Available strategies:\n{strategy_list}", strategies
                else:
                    return "No strategies available", []
            else:
                return f"❌ Failed to get strategies: {response.status_code}", []

        except Exception as e:
            return f"❌ Error: {str(e)}", []

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("# Gmail Integration")
            gr.Markdown("Manage Gmail synchronization, monitor performance, and configure retrieval strategies.")

    with gr.Tabs():
        with gr.TabItem("Sync Control"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Gmail Synchronization")
                    max_emails_input = gr.Number(
                        label="Max Emails to Sync",
                        value=100,
                        minimum=1,
                        maximum=1000
                    )
                    query_filter_input = gr.Textbox(
                        label="Query Filter",
                        placeholder="e.g., newer_than:7d is:unread",
                        value=""
                    )
                    include_ai_checkbox = gr.Checkbox(
                        label="Include AI Analysis",
                        value=True
                    )
                    sync_btn = gr.Button("🚀 Start Sync", variant="primary")

                with gr.Column():
                    gr.Markdown("### Sync Results")
                    sync_status = gr.Textbox(label="Status", interactive=False, lines=6)
                    sync_details = gr.JSON(label="Detailed Results")

            sync_btn.click(
                fn=sync_gmail_emails,
                inputs=[max_emails_input, query_filter_input, include_ai_checkbox],
                outputs=[sync_status, sync_details]
            )

        with gr.TabItem("Performance"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Performance Metrics")
                    refresh_performance_btn = gr.Button("📊 Refresh Metrics", variant="secondary")

                with gr.Column():
                    performance_summary = gr.Textbox(label="Summary", interactive=False, lines=8)
                    performance_details = gr.JSON(label="Detailed Metrics")

            refresh_performance_btn.click(
                fn=get_gmail_performance,
                outputs=[performance_summary, performance_details]
            )

            # Initialize performance data
            perf_summary, perf_details = get_gmail_performance()
            performance_summary.value = perf_summary
            performance_details.value = perf_details

        with gr.TabItem("Strategies"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Retrieval Strategies")
                    refresh_strategies_btn = gr.Button("🔄 Refresh Strategies", variant="secondary")

                with gr.Column():
                    strategies_summary = gr.Textbox(label="Available Strategies", interactive=False, lines=10)
                    strategies_details = gr.JSON(label="Strategy Details")

            refresh_strategies_btn.click(
                fn=get_gmail_strategies,
                outputs=[strategies_summary, strategies_details]
            )

            # Initialize strategies data
            strat_summary, strat_details = get_gmail_strategies()
            strategies_summary.value = strat_summary
            strategies_details.value = strat_details

        with gr.TabItem("Account Status"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Account Information")
                    account_status = gr.Textbox(
                        label="Connection Status",
                        value="🔄 Checking...",
                        interactive=False
                    )
                    last_sync = gr.Textbox(
                        label="Last Sync",
                        interactive=False
                    )
                    api_quota = gr.Textbox(
                        label="API Quota Status",
                        interactive=False
                    )

                with gr.Column():
                    gr.Markdown("### Quick Actions")
                    test_connection_btn = gr.Button("🔗 Test Connection", variant="secondary")
                    connection_test_result = gr.Textbox(label="Test Result", interactive=False)

            def test_gmail_connection():
                """Test Gmail API connection."""
                try:
                    response = requests.get("http://127.0.0.1:8000/api/gmail/performance", timeout=5)
                    if response.status_code == 200:
                        return "✅ Gmail API connection successful"
                    else:
                        return f"❌ Gmail API returned status {response.status_code}"
                except Exception as e:
                    return f"❌ Connection failed: {str(e)}"

            test_connection_btn.click(
                fn=test_gmail_connection,
                outputs=[connection_test_result]
            )

            # Initialize connection test
            connection_test_result.value = test_gmail_connection()