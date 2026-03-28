"""
An example plugin that registers a new workflow.
"""

import logging
from typing import Any, Dict

from src.core.ai_engine import AdvancedAIEngine
from src.core.database import DatabaseManager
from backend.python_nlp.smart_filters import SmartFilterManager

# Note: Plugins need to import from the main application's modules.
# This requires the main application to be installed as a package or
# for the PYTHONPATH to be set up correctly.
from backend.node_engine.node_base import BaseNode, DataType, ExecutionContext, NodePort
from backend.node_engine.workflow_engine import WorkflowEngine

logger = logging.getLogger(__name__)


class ExampleUppercaseNode(BaseNode):
    """
    An example node that converts email subject to uppercase.
    This demonstrates how to create custom node types for the Node Engine.
    """

    def __init__(self, config: Dict[str, Any] = None, node_id: str = None, name: str = None):
        super().__init__(
            node_id, name or "Example Uppercase", "Converts email subject to uppercase"
        )
        self.config = config or {}

        # Define input and output ports
        self.input_ports = [
            NodePort(
                "emails",
                DataType.EMAIL_LIST,
                required=True,
                description="List of emails to process",
            )
        ]
        self.output_ports = [
            NodePort(
                "processed_emails",
                DataType.EMAIL_LIST,
                required=True,
                description="Processed emails with uppercase subjects",
            )
        ]

    async def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        """Execute the uppercase transformation on email subjects."""
        try:
            input_emails = self.inputs.get("emails", [])

            if not input_emails:
                return {"processed_emails": []}

            processed_emails = []
            for email in input_emails:
                processed_email = email.copy()
                if "subject" in processed_email:
                    processed_email["subject"] = processed_email["subject"].upper()
                processed_email["processed_by"] = "example_uppercase_node"
                processed_emails.append(processed_email)

            logger.info(f"Processed {len(processed_emails)} emails with uppercase transformation")

            return {"processed_emails": processed_emails}

        except Exception as e:
            logger.error(f"ExampleUppercaseNode execution failed: {e}")
            context.add_error(self.node_id, f"Uppercase processing failed: {str(e)}")
            return {"processed_emails": []}


def register(
    workflow_engine: WorkflowEngine,
    ai_engine: AdvancedAIEngine = None,
    filter_manager: SmartFilterManager = None,
    db: DatabaseManager = None,
    **kwargs,
):
    """
    The required register function for the plugin.
    This function is called by the PluginManager at startup.
    Registers the custom node type with the workflow engine.
    """
    logger.info("Registering the ExampleUppercaseNode.")
    # Register the custom node type
    workflow_engine.register_node_type(ExampleUppercaseNode)
    logger.info("ExampleUppercaseNode registered successfully")
