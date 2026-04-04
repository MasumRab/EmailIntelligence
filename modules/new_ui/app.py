import gradio as gr
import json
import time
import random
import os
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

# Import Adapter
from modules.new_ui.backend_adapter import BackendClient
from modules.new_ui.utils import clean_text, extract_keywords

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GradioUI")

# Initialize Backend Client
client = BackendClient()

# ============== UI Functions ==============

async def analyze_single_email(subject: str, content: str) -> tuple:
    """Analyze a single email using the real backend"""
    if not subject and not content:
        return (
            {"error": "Please provide email subject or content"},
            "❌ No input provided",
            None
        )

    try:
        full_text = f"{subject}\n{content}"
        result = await client.analyze_text(full_text)

        if "error" in result:
             return result, f"❌ Analysis failed: {result['error']}", None

        # Extract values safely with defaults
        sentiment = result.get('sentiment', 'neutral')
        confidence = result.get('confidence', 0.0)
        topic = result.get('topic', 'unknown')
        intent = result.get('intent', 'unknown')
        urgency = result.get('urgency', 'low')
        keywords = result.get('keywords', [])

        # Create summary
        summary = f"""
📧 **Email Analysis Complete**

**Sentiment:** {str(sentiment).capitalize()} ({confidence:.0%} confidence)
**Topic:** {str(topic).capitalize()}
**Intent:** {str(intent).capitalize()}
**Urgency:** {str(urgency).capitalize()}

**Keywords:** {', '.join(keywords[:5]) if keywords else 'None detected'}
"""

        # Create chart data
        import plotly.graph_objects as go

        fig = go.Figure(data=[
            go.Bar(
                x=['Confidence'],
                y=[confidence],
                marker_color='#3b82f6',
                text=[f"{confidence:.0%}"],
                textposition='auto'
            )
        ])
        fig.update_layout(
            title="Analysis Confidence",
            yaxis_title="Score",
            yaxis_range=[0, 1],
            template="plotly_white",
            height=300
        )

        return result, summary, fig

    except Exception as e:
        logger.error(f"UI Analysis error: {e}")
        return {"error": str(e)}, f"❌ Analysis failed: {str(e)}", None

async def batch_analyze_emails(emails_text: str) -> tuple:
    """Analyze multiple emails"""
    if not emails_text.strip():
        return "No emails provided", []

    emails = [e.strip() for e in emails_text.split("---") if e.strip()]
    results = []

    for i, email in enumerate(emails, 1):
        lines = email.split("\n", 1)
        subject = lines[0] if lines else f"Email {i}"
        content = lines[1] if len(lines) > 1 else email

        # Call backend for each
        analysis = await client.analyze_text(f"{subject}\n{content}")

        results.append({
            "Email #": i,
            "Subject": subject[:50] + "..." if len(subject) > 50 else subject,
            "Sentiment": analysis.get("sentiment", "unknown"),
            "Topic": analysis.get("topic", "unknown"),
            "Urgency": analysis.get("urgency", "unknown")
        })

    summary = f"✅ Analyzed {len(results)} emails successfully"
    return summary, results

def get_dashboard_stats() -> tuple:
    """Get dashboard statistics from backend metrics"""
    stats = client.get_metrics()

    # Flatten the aggregated metrics for display
    display_stats = {}
    for key, val in stats.items():
        if isinstance(val, dict) and 'avg' in val:
            display_stats[key] = f"{val['avg']:.2f}ms (avg)"
        else:
            display_stats[key] = val

    summary = f"""
📊 **System Metrics**

See raw JSON for detailed performance breakdowns.
"""

    return stats, summary

def list_available_workflows() -> tuple:
    """List available workflows from generic storage"""
    workflows = client.list_workflows()

    workflow_list = []
    for wf in workflows:
        workflow_list.append({
            "ID": wf.get("id"),
            "Name": wf.get("name"),
            "Description": wf.get("description"),
        })

    return workflow_list, f"Found {len(workflows)} workflows"

async def run_workflow_on_email(workflow_id: str, subject: str, content: str) -> tuple:
    """Run a workflow on an email"""
    if not workflow_id:
        return {"error": "Please select a workflow"}, "❌ No workflow selected"

    email_data = {"subject": subject, "content": content}
    payload = {"workflow_id": workflow_id, "email_data": email_data}

    result = await client.start_workflow(payload)

    status = f"""
✅ **Workflow Request Processed**

**Workflow:** {workflow_id}
**Result:** {result.get('status', 'unknown')}
"""

    return result, status

def create_smart_filter(name: str, criteria_json: str, priority: int) -> tuple:
    """Create a smart filter and persist it"""
    try:
        criteria = json.loads(criteria_json) if criteria_json else {}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON in criteria"}, "❌ Invalid criteria JSON"

    filter_id = f"filter_{name.lower().replace(' ', '_')}_{int(time.time())}"

    new_filter = {
        "filter_id": filter_id,
        "name": name,
        "criteria": criteria,
        "priority": priority,
        "created_at": datetime.now().isoformat(),
        "is_active": True
    }

    # Persist using generic storage
    success = client.persist_item(filter_id, new_filter)

    if success:
        return new_filter, f"✅ Filter '{name}' created and saved with ID: {filter_id}"
    else:
        return {"error": "Failed to save"}, "❌ Failed to save filter"

def get_system_health() -> tuple:
    """Get system health status"""
    import psutil

    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        health = {
            "status": "healthy" if cpu_percent < 80 and memory.percent < 80 else "degraded",
            "cpu_usage": f"{cpu_percent}%",
            "memory_usage": f"{memory.percent}%",
            "disk_usage": f"{disk.percent}%",
            "uptime": "Running",
            "last_check": datetime.now().isoformat()
        }

        status_emoji = "🟢" if health["status"] == "healthy" else "🟡"
        summary = f"""
{status_emoji} **System Status: {health['status'].upper()}**

**Resources:**
- CPU: {health['cpu_usage']}
- Memory: {health['memory_usage']}
- Disk: {health['disk_usage']}
"""
        return health, summary

    except Exception as e:
        return {"error": str(e)}, f"❌ Health check failed: {str(e)}"

# ============== Build Gradio UI ==============

with gr.Blocks() as demo:
    gr.Markdown(
        """
        # 📧 Email Intelligence Platform

        A comprehensive AI-powered email analysis system.
        """
    )

    with gr.Tabs():
        # Tab 1: Email Analysis
        with gr.Tab("🔍 Email Analysis"):
            gr.Markdown("### Analyze emails using AI-powered NLP")

            with gr.Row():
                with gr.Column(scale=1):
                    email_subject = gr.Textbox(
                        label="Email Subject",
                        placeholder="Enter email subject...",
                        lines=1
                    )
                    email_content = gr.TextArea(
                        label="Email Content",
                        placeholder="Enter email body content...",
                        lines=8
                    )
                    analyze_btn = gr.Button("🔍 Analyze Email", variant="primary")

                with gr.Column(scale=1):
                    analysis_summary = gr.Markdown(label="Analysis Summary")
                    confidence_chart = gr.Plot(label="Confidence Scores")

            with gr.Accordion("Raw Analysis Output", open=False):
                analysis_json = gr.JSON(label="Full Analysis Results")

            analyze_btn.click(
                fn=analyze_single_email,
                inputs=[email_subject, email_content],
                outputs=[analysis_json, analysis_summary, confidence_chart],
                api_visibility="public"
            )

            gr.Markdown("---")
            gr.Markdown("### Batch Analysis")

            with gr.Row():
                with gr.Column():
                    batch_emails = gr.TextArea(
                        label="Emails (separate with ---)",
                        placeholder="Subject: First email\nContent here...\n---\nSubject: Second email\nMore content...",
                        lines=10
                    )
                    batch_analyze_btn = gr.Button("📊 Batch Analyze", variant="secondary")

                with gr.Column():
                    batch_summary = gr.Textbox(label="Summary", interactive=False)
                    batch_results = gr.Dataframe(
                        label="Results",
                        headers=["Email #", "Subject", "Sentiment", "Topic", "Urgency"]
                    )

            batch_analyze_btn.click(
                fn=batch_analyze_emails,
                inputs=[batch_emails],
                outputs=[batch_summary, batch_results],
                api_visibility="public"
            )

        # Tab 2: Workflows
        with gr.Tab("⚙️ Workflows"):
            gr.Markdown("### Workflow Management")

            with gr.Row():
                with gr.Column():
                    refresh_workflows_btn = gr.Button("🔄 Refresh Workflows", variant="secondary")
                    workflows_table = gr.Dataframe(
                        label="Available Workflows",
                        headers=["ID", "Name", "Description"]
                    )
                    workflows_status = gr.Textbox(label="Status", interactive=False)

                with gr.Column():
                    gr.Markdown("### Run Workflow on Email")
                    # Note: Choices would need to be dynamic in a real app, updated by backend
                    workflow_select = gr.Textbox(label="Workflow ID", placeholder="e.g. workflow_1")
                    wf_subject = gr.Textbox(label="Email Subject", placeholder="Test subject...")
                    wf_content = gr.TextArea(label="Email Content", placeholder="Test content...", lines=4)
                    run_workflow_btn = gr.Button("▶️ Run Workflow", variant="primary")
                    workflow_result = gr.Markdown(label="Result")
                    workflow_json = gr.JSON(label="Workflow Output")

            refresh_workflows_btn.click(
                fn=list_available_workflows,
                inputs=[],
                outputs=[workflows_table, workflows_status],
                api_visibility="public"
            )

            run_workflow_btn.click(
                fn=run_workflow_on_email,
                inputs=[workflow_select, wf_subject, wf_content],
                outputs=[workflow_json, workflow_result],
                api_visibility="public"
            )

        # Tab 3: Smart Filters
        with gr.Tab("🎯 Smart Filters"):
            gr.Markdown("### Create and Manage Smart Filters")

            with gr.Row():
                with gr.Column():
                    filter_name = gr.Textbox(
                        label="Filter Name",
                        placeholder="e.g., Urgent Work Emails"
                    )
                    filter_criteria = gr.Code(
                        label="Filter Criteria (JSON)",
                        language="json",
                        value='{\n  "subject_keywords": ["urgent", "important"],\n  "from_patterns": ["@company.com"]\n}'
                    )
                    filter_priority = gr.Slider(
                        label="Priority",
                        minimum=1,
                        maximum=10,
                        value=5,
                        step=1
                    )
                    create_filter_btn = gr.Button("➕ Create Filter", variant="primary")

                with gr.Column():
                    filter_status = gr.Markdown(label="Status")
                    filter_output = gr.JSON(label="Created Filter")

            create_filter_btn.click(
                fn=create_smart_filter,
                inputs=[filter_name, filter_criteria, filter_priority],
                outputs=[filter_output, filter_status],
                api_visibility="public"
            )

        # Tab 4: Dashboard
        with gr.Tab("📊 Dashboard"):
            gr.Markdown("### System Statistics & Metrics")

            with gr.Row():
                refresh_stats_btn = gr.Button("🔄 Refresh Statistics", variant="secondary")

            with gr.Row():
                with gr.Column():
                    stats_summary = gr.Markdown(label="Statistics Summary")

                with gr.Column():
                    stats_json = gr.JSON(label="Raw Statistics")

            refresh_stats_btn.click(
                fn=get_dashboard_stats,
                inputs=[],
                outputs=[stats_json, stats_summary],
                api_visibility="public"
            )

        # Tab 5: System Health
        with gr.Tab("🏥 System Health"):
            gr.Markdown("### System Health Monitoring")

            with gr.Row():
                health_check_btn = gr.Button("🔍 Check Health", variant="primary")

            with gr.Row():
                with gr.Column():
                    health_summary = gr.Markdown(label="Health Summary")

                with gr.Column():
                    health_json = gr.JSON(label="Health Details")

            health_check_btn.click(
                fn=get_system_health,
                inputs=[],
                outputs=[health_json, health_summary],
                api_visibility="public"
            )

# Launch Logic
if __name__ == "__main__":
    server_name = os.environ.get("GRADIO_SERVER_NAME", "127.0.0.1")
    start_port = int(os.environ.get("GRADIO_SERVER_PORT", "7860"))

    # Simple port retry loop
    for port in range(start_port, start_port + 10):
        try:
            print(f"Attempting to launch on port {port}...")
            demo.launch(
                server_name=server_name,
                server_port=port,
                share=False
            )
            break
        except OSError:
            print(f"Port {port} is busy, trying next...")
            continue
