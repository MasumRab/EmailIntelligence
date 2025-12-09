"""
Backend Adapter for Gradio UI

This module provides a unified interface for the UI to interact with the core backend services.
It handles dependency injection, fallback mechanisms, and error handling.
"""

import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

# Core Imports
from src.core.factory import get_ai_engine
from src.core.workflow_engine import WorkflowRunner, Workflow
from src.core.performance_monitor import performance_monitor

logger = logging.getLogger(__name__)

# Local Fallback Data Directory
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class BackendClient:
    """
    Adapter class to connect UI to Backend Services.
    Uses generic local JSON fallback for persistence if core services don't support generic KV.
    """

    def __init__(self):
        self._ai_engine = None

    async def _get_ai_engine(self):
        """Lazy load AI Engine"""
        if not self._ai_engine:
            # We need to manually handle the async context manager here since we want a persistent instance
            # or we re-enter it every time. Re-entering is safer for resource management but slower.
            # For this adapter, we will use the factory's context manager per-call or try to hold it.
            # Given the async generator nature of get_ai_engine, we'll use it per-call in analyze_text.
            pass
        return self._ai_engine

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text using the core AIEngine.
        """
        try:
            # Split text into subject/content roughly for the API
            lines = text.split('\n', 1)
            subject = lines[0] if lines else "No Subject"
            content = lines[1] if len(lines) > 1 else text

            async with get_ai_engine() as engine:
                result = await engine.analyze_email(subject, content)
                return result.to_dict()
        except Exception as e:
            logger.error(f"Error in analyze_text: {e}", exc_info=True)
            return {"error": str(e)}

    async def start_workflow(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start a workflow.
        Payload expected to contain 'workflow_id' and 'email_data'.
        """
        workflow_id = payload.get("workflow_id")
        email_data = payload.get("email_data", {})

        if not workflow_id:
            return {"error": "No workflow_id provided"}

        # TODO: Load real workflow definition from registry or DB
        # For now, we construct a dummy workflow if not found, or try to load from a file
        # This part requires a WorkflowRegistry which is not explicitly exposed in the files I read.
        # I will check if I can load a workflow from the local fallback "workflows" storage.

        workflow_def = self.retrieve_item(f"workflow_{workflow_id}")

        if not workflow_def:
             # Fallback to a mock/simple workflow if not found
             logger.warning(f"Workflow {workflow_id} not found in storage. Using dummy.")
             return {"error": f"Workflow {workflow_id} not found"}

        try:
            # Reconstruct Workflow object from stored definition
            # This assumes workflow_def matches the expected dict structure for Workflow constructor
            # The constructor takes: name, nodes, connections
            # But the stored JSON might differ. I'll assume simple mapping for now.

            # Since constructing a real Workflow object from JSON might be complex without a deserializer,
            # and the requirement is to "call the closest matching function",
            # I will return a placeholder response if I can't easily run it,
            # OR I will try to implement a basic runner if possible.

            # Given the constraints, I will return a "not implemented" error for actual execution
            # unless I can find a standard "load_workflow" function in src/core.
            # I did not see one in workflow_engine.py.

            return {
                "status": "failed",
                "error": "Workflow execution from UI not fully wired to backend registry yet."
            }

        except Exception as e:
            logger.error(f"Error starting workflow: {e}")
            return {"error": str(e)}

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get system metrics from PerformanceMonitor.
        """
        try:
            # performance_monitor is a global instance
            return performance_monitor.get_aggregated_metrics()
        except Exception as e:
            logger.error(f"Error getting metrics: {e}")
            return {"error": str(e)}

    def persist_item(self, key: str, data: Dict[str, Any]) -> bool:
        """
        Generic persistence using local JSON files (Fallback).
        Stored in modules/new_ui/data/{key}.json
        """
        try:
            safe_key = "".join(x for x in key if x.isalnum() or x in "_-")
            file_path = DATA_DIR / f"{safe_key}.json"

            # Atomic write
            temp_path = file_path.with_suffix(".tmp")
            with open(temp_path, 'w') as f:
                json.dump(data, f, indent=2)
            temp_path.replace(file_path)

            logger.info(f"Persisted item {key} to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to persist item {key}: {e}")
            return False

    def retrieve_item(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Generic retrieval using local JSON files (Fallback).
        """
        try:
            safe_key = "".join(x for x in key if x.isalnum() or x in "_-")
            file_path = DATA_DIR / f"{safe_key}.json"

            if not file_path.exists():
                return None

            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to retrieve item {key}: {e}")
            return None

    # Helper for the UI to list workflows (generic)
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows stored in the local fallback."""
        workflows = []
        try:
            for file_path in DATA_DIR.glob("workflow_*.json"):
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        workflows.append(data)
                except:
                    continue
        except Exception as e:
            logger.error(f"Error listing workflows: {e}")
        return workflows
