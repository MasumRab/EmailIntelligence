import logging
import psutil
import platform
from datetime import datetime
# TODO: Remove unused asyncio import after confirming no async operations needed
import asyncio

import gradio as gr
from fastapi import FastAPI, HTTPException
import requests

from .models import SystemStatus, HealthCheck

logger = logging.getLogger(__name__)


def register(app: FastAPI, gradio_app: gr.Blocks):
    """
    Registers the system status module with the main application.
    """
    logger.info("Registering system status module.")

    # The UI is handled in main.py, this module provides the backend functionality
    # and can be extended to add API endpoints if needed

    logger.info("System status module registered successfully.")


def create_system_status_ui():
    """Create the System Status tab interface."""

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## System Health Dashboard")
            gr.Markdown("Monitor system performance, health metrics, and operational status.")

        refresh_btn = gr.Button("🔄 Refresh", variant="secondary")

    with gr.Tabs():
        with gr.TabItem("Overview"):
            create_overview_tab()

        with gr.TabItem("Performance"):
            create_performance_tab()

        with gr.TabItem("Health Checks"):
            create_health_tab()

        with gr.TabItem("Resources"):
            create_resources_tab()


def create_overview_tab():
    """Create the system overview dashboard."""

    with gr.Row():
        with gr.Column():
            status_indicator = gr.Textbox(
                label="System Status",
                value="🟢 Online",
                interactive=False
            )

            uptime_display = gr.Textbox(
                label="System Uptime",
                interactive=False
            )

            last_updated = gr.Textbox(
                label="Last Updated",
                interactive=False
            )

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Email Statistics")
            total_emails = gr.Number(label="Total Emails", interactive=False)
            unread_emails = gr.Number(label="Unread Emails", interactive=False)
            categorized_plot = gr.Plot(label="Email Categories")

        with gr.Column():
            gr.Markdown("### Performance Metrics")
            avg_response_time = gr.Number(label="Avg Response Time (ms)", interactive=False)
            total_operations = gr.Number(label="Total Operations", interactive=False)
            performance_plot = gr.Plot(label="Operation Performance")


def create_performance_tab():
    """Create the performance monitoring tab."""

    with gr.Row():
        with gr.Column():
            gr.Markdown("### API Performance")
            api_response_times = gr.Plot(label="API Response Times")
            operation_counts = gr.Plot(label="Operation Counts")

        with gr.Column():
            gr.Markdown("### System Performance")
            cpu_usage_plot = gr.Plot(label="CPU Usage Over Time")
            memory_usage_plot = gr.Plot(label="Memory Usage Over Time")


def create_health_tab():
    """Create the health checks tab."""

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Service Health")
            backend_status = gr.Textbox(label="Backend API", interactive=False)
            database_status = gr.Textbox(label="Database", interactive=False)
            ai_engine_status = gr.Textbox(label="AI Engine", interactive=False)

        with gr.Column():
            gr.Markdown("### Gmail Integration")
            gmail_status = gr.Textbox(label="Gmail API", interactive=False)
            gmail_performance = gr.JSON(label="Performance Metrics")


def create_resources_tab():
    """Create the system resources tab."""

    with gr.Row():
        with gr.Column():
            gr.Markdown("### System Resources")
            cpu_percent = gr.Number(label="CPU Usage (%)", interactive=False)
            memory_percent = gr.Number(label="Memory Usage (%)", interactive=False)
            disk_usage = gr.Number(label="Disk Usage (%)", interactive=False)

        with gr.Column():
            gr.Markdown("### Network")
            network_io = gr.JSON(label="Network I/O")


async def get_system_status() -> SystemStatus:
    """Get comprehensive system status information."""

    try:
        # System information
        system_info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
        }

        # Current resource usage
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        # Network I/O
        net_io = psutil.net_io_counters()
        network_stats = {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
        }

        # Get dashboard stats
        try:
            dashboard_response = requests.get("http://127.0.0.1:8000/api/dashboard/stats", timeout=5)
            dashboard_data = dashboard_response.json() if dashboard_response.status_code == 200 else {}
        except:
            dashboard_data = {}

        # Get Gmail performance metrics
        try:
            gmail_response = requests.get("http://127.0.0.1:8000/api/gmail/performance", timeout=5)
            gmail_data = gmail_response.json() if gmail_response.status_code == 200 else {}
        except:
            gmail_data = {}

        return SystemStatus(
            system_info=system_info,
            cpu_usage=cpu_percent,
            memory_usage=memory.percent,
            memory_total=memory.total,
            memory_used=memory.used,
            disk_usage=disk.percent,
            disk_total=disk.total,
            disk_used=disk.used,
            network_stats=network_stats,
            dashboard_stats=dashboard_data,
            gmail_performance=gmail_data,
            timestamp=datetime.now().isoformat(),
            uptime_seconds=0  # Would need to track from startup
        )

    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get system status: {str(e)}")


async def perform_health_checks() -> HealthCheck:
    """Perform comprehensive health checks on all services."""

    health_results = {}

    # Backend API health check
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        health_results["backend_api"] = {
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "response_time": response.elapsed.total_seconds() * 1000,
            "details": response.json() if response.status_code == 200 else {"error": response.text}
        }
    except Exception as e:
        health_results["backend_api"] = {
            "status": "unhealthy",
            "error": str(e)
        }

    # Database health check
    try:
        response = requests.get("http://127.0.0.1:8000/api/emails?limit=1", timeout=5)
        health_results["database"] = {
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "response_time": response.elapsed.total_seconds() * 1000
        }
    except Exception as e:
        health_results["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }

    # AI Engine health check
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/ai/analyze",
            json={"subject": "test", "content": "test"},
            timeout=10
        )
        health_results["ai_engine"] = {
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "response_time": response.elapsed.total_seconds() * 1000
        }
    except Exception as e:
        health_results["ai_engine"] = {
            "status": "unhealthy",
            "error": str(e)
        }

    # Gmail API health check
    try:
        response = requests.get("http://127.0.0.1:8000/api/gmail/performance", timeout=5)
        health_results["gmail_api"] = {
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "response_time": response.elapsed.total_seconds() * 1000
        }
    except Exception as e:
        health_results["gmail_api"] = {
            "status": "unhealthy",
            "error": str(e)
        }

    overall_status = "healthy" if all(
        check.get("status") == "healthy" for check in health_results.values()
    ) else "unhealthy"

    return HealthCheck(
        overall_status=overall_status,
        service_checks=health_results,
        timestamp=datetime.now().isoformat()
    )