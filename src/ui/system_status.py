"""
System Status UI Component for Email Intelligence Platform
"""

import logging
import platform
from datetime import datetime

import gradio as gr
import psutil
import requests

logger = logging.getLogger(__name__)


def create_system_status_tab():
    """Create the System Status tab with monitoring and diagnostics."""

    def refresh_system_status():
        """Refresh and return current system status."""
        try:
            # System information
            system_info = {
                "os": platform.system(),
                "os_version": platform.version(),
                "python_version": platform.python_version(),
                "cpu_count": psutil.cpu_count(),
            }

            # Current resource usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            # Get dashboard stats
            try:
                dashboard_response = requests.get("http://127.0.0.1:8000/api/dashboard/stats", timeout=2)
                dashboard_data = dashboard_response.json() if dashboard_response.status_code == 200 else {}
            except (requests.RequestException, ValueError) as e:
                dashboard_data = {"error": f"Dashboard API unavailable: {str(e)}"}

            # Get Gmail performance metrics
            try:
                gmail_response = requests.get("http://127.0.0.1:8000/api/gmail/performance", timeout=2)
                gmail_data = gmail_response.json() if gmail_response.status_code == 200 else {}
            except (requests.RequestException, ValueError) as e:
                gmail_data = {"error": f"Gmail API unavailable: {str(e)}"}

            return {
                "system_info": system_info,
                "cpu_usage": f"{cpu_percent:.1f}%",
                "memory_usage": f"{memory.percent:.1f}%",
                "disk_usage": f"{disk.percent:.1f}%",
                "total_emails": dashboard_data.get("total_emails", "N/A"),
                "unread_emails": dashboard_data.get("unread_emails", "N/A"),
                "gmail_status": "Connected" if not gmail_data.get("error") else "Disconnected",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except (psutil.Error, OSError, ValueError, KeyError) as e:
            logger.error(f"Error refreshing system status: {e}")
            return {
                "system_info": {"error": "Unable to retrieve system info"},
                "cpu_usage": "N/A",
                "memory_usage": "N/A",
                "disk_usage": "N/A",
                "total_emails": "N/A",
                "unread_emails": "N/A",
                "gmail_status": "Error",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("# System Status Dashboard")
            gr.Markdown("Monitor system performance, health metrics, and operational status.")

        refresh_btn = gr.Button("🔄 Refresh", variant="secondary")

    with gr.Tabs():
        with gr.TabItem("Overview"):
            with gr.Row():
                with gr.Column():
                    status_indicator = gr.Textbox(
                        label="System Status",
                        value="🟢 Online",
                        interactive=False
                    )

                    system_info = gr.JSON(label="System Information")

                    last_updated = gr.Textbox(
                        label="Last Updated",
                        interactive=False
                    )

            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Email Statistics")
                    total_emails = gr.Textbox(label="Total Emails", interactive=False)
                    unread_emails = gr.Textbox(label="Unread Emails", interactive=False)

                with gr.Column():
                    gr.Markdown("### Integration Status")
                    gmail_status = gr.Textbox(label="Gmail API", interactive=False)
                    cpu_usage = gr.Textbox(label="CPU Usage", interactive=False)
                    memory_usage = gr.Textbox(label="Memory Usage", interactive=False)
                    disk_usage = gr.Textbox(label="Disk Usage", interactive=False)

        with gr.TabItem("Performance"):
            gr.Markdown("### Performance Metrics")
            gr.Markdown("*Detailed performance monitoring coming soon...*")

        with gr.TabItem("Health Checks"):
            gr.Markdown("### Service Health")
            gr.Markdown("*Automated health checks coming soon...*")

        with gr.TabItem("Resources"):
            gr.Markdown("### System Resources")
            gr.Markdown("*Resource monitoring details coming soon...*")

    # Connect refresh button
    refresh_btn.click(
        fn=refresh_system_status,
        outputs=[
            system_info, last_updated, total_emails, unread_emails,
            gmail_status, cpu_usage, memory_usage, disk_usage
        ]
    )

    # Initial load
    initial_data = refresh_system_status()
    system_info.value = initial_data["system_info"]
    last_updated.value = initial_data["last_updated"]
    total_emails.value = initial_data["total_emails"]
    unread_emails.value = initial_data["unread_emails"]
    gmail_status.value = initial_data["gmail_status"]
    cpu_usage.value = initial_data["cpu_usage"]
    memory_usage.value = initial_data["memory_usage"]
    disk_usage.value = initial_data["disk_usage"]