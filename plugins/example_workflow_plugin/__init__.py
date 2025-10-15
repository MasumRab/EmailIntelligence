"""
An example plugin that registers a new workflow.
"""

import logging
from typing import Any, Dict

from backend.python_backend.ai_engine import AdvancedAIEngine
from backend.python_backend.database import DatabaseManager

# Note: Plugins need to import from the main application's modules.
# This requires the main application to be installed as a package or
# for the PYTHONPATH to be set up correctly.
from backend.python_backend.workflow_engine import BaseWorkflow, WorkflowEngine
from backend.python_nlp.smart_filters import SmartFilterManager

logger = logging.getLogger(__name__)


class ExampleUpperCaseWorkflow(BaseWorkflow):
    """
    An example workflow that converts the email subject to uppercase.
    """

    def __init__(
        self,
        ai_engine: "AdvancedAIEngine",
        filter_manager: "SmartFilterManager",
        db: "DatabaseManager",
    ):
        # Call the parent constructor with the required dependencies
        super().__init__(ai_engine, filter_manager, db)
        logger.info("ExampleUpperCaseWorkflow instance created.")

    @property
    def name(self) -> str:
        return "example_uppercase"

    async def execute(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts the subject to uppercase and adds a note.
        This workflow intentionally does not use the AI engine,
        to demonstrate a simple transformation.
        """
        logger.info(f"Executing example_uppercase workflow for email: {email_data.get('subject')}")

        processed_data = email_data.copy()

        if "subject" in processed_data:
            processed_data["subject"] = processed_data["subject"].upper()

        processed_data["workflow_status"] = "processed_by_example_uppercase_workflow"

        return processed_data


def register(
    workflow_engine: WorkflowEngine,
    ai_engine: AdvancedAIEngine,
    filter_manager: SmartFilterManager,
    db: DatabaseManager,
    **kwargs,
):
    """
    The required register function for the plugin.
    This function is called by the PluginManager at startup.
    """
    logger.info("Registering the ExampleUpperCaseWorkflow.")
    # Instantiate the workflow with the required dependencies
    example_workflow = ExampleUpperCaseWorkflow(ai_engine, filter_manager, db)
    workflow_engine.register_workflow(example_workflow)
