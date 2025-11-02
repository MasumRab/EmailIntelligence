import configparser
configparser.SafeConfigParser = configparser.ConfigParser

import argparse
import logging

import gradio as gr
import uvicorn
import psutil
import platform
from datetime import datetime
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import ValidationError
from .core.module_manager import ModuleManager
from .core.middleware import create_security_middleware, create_security_headers_middleware
from .core.audit_logger import audit_logger, AuditEventType, AuditSeverity
from .core.performance_monitor import performance_monitor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
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
        except Exception as e:
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


def create_app():
    """
    Creates and configures the main FastAPI application and Gradio UI.
    """
    # Create the main FastAPI app
    app = FastAPI(
        title="Email Intelligence Platform",
        description="A modular and extensible platform for email processing and analysis.",
        version="3.0.0",
        openapi_tags=[
            {
                "name": "Dashboard Widgets",
                "description": "Endpoints for managing and rendering dashboard widgets.",
            },
        ],
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add comprehensive security middleware
    app.add_middleware(create_security_middleware(app))
    app.add_middleware(create_security_headers_middleware(app))

    # Add security headers middleware (additional layer)
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        return response

        # Add exception handlers for secure error responses
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": "Validation error", "message": "Invalid input data"},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": "Request error", "message": "An error occurred"},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "message": "An unexpected error occurred"},
        )

    @app.get("/")
    async def root():
        """Redirect root to Gradio UI."""
        return RedirectResponse(url="/ui")

    # Create the main Gradio UI as a placeholder
    # Modules will add their own tabs and components to this.
    with gr.Blocks(theme=gr.themes.Soft(), title="Email Intelligence Platform") as gradio_app:
        gr.Markdown("# Email Intelligence Platform")

        with gr.Tabs():
            with gr.TabItem("Simple UI (A)"):
                gr.Markdown("## Simple & Streamlined UI\nThis is the placeholder for the simple, user-friendly interface where users can run pre-built workflows.")

            with gr.TabItem("Visual Editor (B)"):
                gr.Markdown("## Visual & Node-Based UI\nThis is the placeholder for the powerful, node-based workflow editor.")

            with gr.TabItem("System Status"):
                create_system_status_tab()

            with gr.TabItem("AI Lab"):
                create_ai_lab_tab()

            with gr.TabItem("Gmail Integration"):
                create_gmail_integration_tab()

            with gr.TabItem("Admin Dashboard (C)"):
                gr.Markdown("## Power-User Dashboard\nThis is the placeholder for the admin and power-user dashboard for managing models, users, and system performance.")

    # Add startup and shutdown event handlers for security components
    @app.on_event("startup")
    async def startup_event():
        """Initialize security components on application startup."""
        audit_logger.log_security_event(
            event_type=AuditEventType.SYSTEM_STARTUP,
            severity=AuditSeverity.LOW,
            action="application_startup",
            details={
                "version": "3.0.0",
                "security_components": ["audit_logger", "rate_limiter", "performance_monitor", "security_middleware"],
                "message": "Email Intelligence Platform started with comprehensive security"
            }
        )

        performance_monitor.record_metric(
            "application_startup",
            1,
            "event",
            tags={"component": "application", "version": "3.0.0"}
        )

        logger.info("Security components initialized successfully")

    @app.on_event("shutdown")
    async def shutdown_event():
        """Clean up security components on application shutdown."""
        audit_logger.log_security_event(
            event_type=AuditEventType.SYSTEM_SHUTDOWN,
            severity=AuditSeverity.LOW,
            action="application_shutdown",
            details={"message": "Email Intelligence Platform shutting down"}
        )

        # Shutdown performance monitor
        performance_monitor.shutdown()

        logger.info("Security components shut down successfully")

    # Initialize the Module Manager
    module_manager = ModuleManager(app, gradio_app)
    module_manager.load_modules()

    # Mount the Gradio UI onto the FastAPI app
    # This makes the UI accessible at the '/ui' endpoint
    gr.mount_gradio_app(app, gradio_app, path="/ui")

    logger.info("Application creation complete. FastAPI and Gradio are integrated.")
    return app


def main():
    """
    Main entry point to run the server.
    """
    parser = argparse.ArgumentParser(description="Run the Email Intelligence Platform.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the server on.")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the server on.")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reloading.")
    args = parser.parse_args()

    app = create_app()

    uvicorn.run(
        "src.main:create_app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        factory=True,
    )


if __name__ == "__main__":
    main()
