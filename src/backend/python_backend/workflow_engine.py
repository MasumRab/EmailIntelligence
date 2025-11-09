"""
Workflow Engine for the Email Intelligence Platform

This module provides a system for defining, discovering, and executing
standardized email processing workflows.
"""

import json
import logging
import os
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List

# Forward-referencing for type hints
if TYPE_CHECKING:
    from ..python_nlp.smart_filters import SmartFilterManager
    from .ai_engine import AdvancedAIEngine
    from .database import DatabaseManager

from .database import DATA_DIR, SETTINGS_FILE

logger = logging.getLogger(__name__)

WORKFLOWS_DIR = DATA_DIR / "workflows"


class BaseWorkflow(ABC):
    """
    Abstract base class for all email processing workflows.
    """

    def __init__(
        self,
        ai_engine: "AdvancedAIEngine",
        filter_manager: "SmartFilterManager",
        db: "DatabaseManager",
    ):
        self._ai_engine = ai_engine
        self._filter_manager = filter_manager
        self._db = db

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def execute(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        pass


class WorkflowEngine:
    """
    Manages the registration and execution of workflows.
    """

    def __init__(self):
        self._workflows: Dict[str, BaseWorkflow] = {}
        self.active_workflow: BaseWorkflow = None
        self.settings_file = SETTINGS_FILE
        # Store references to managers to create new workflows at runtime
        self._ai_engine: "AdvancedAIEngine" = None
        self._filter_manager: "SmartFilterManager" = None
        self._db: "DatabaseManager" = None

    def _load_settings(self) -> Dict[str, Any]:
        """Loads settings from the JSON file."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                logger.error(f"Failed to load settings file: {e}")
        return {}

    def _save_settings(self):
        """Saves the current settings to the JSON file."""
        settings = {
            "active_workflow": self.active_workflow.name
            if self.active_workflow
            else None
        }
        try:
            with open(self.settings_file, "w") as f:
                json.dump(settings, f, indent=4)
            logger.info(f"Saved settings to {self.settings_file}")
        except IOError as e:
            logger.error(f"Failed to save settings file: {e}")

    def register_workflow(self, workflow: BaseWorkflow):
        """Registers a new workflow."""
        if workflow.name in self._workflows:
            logger.warning(
                f"Workflow '{workflow.name}' is already registered. Overwriting."
            )
        logger.info(f"Registering workflow: {workflow.name}")
        self._workflows[workflow.name] = workflow

    async def discover_workflows(
        self,
        ai_engine: "AdvancedAIEngine",
        filter_manager: "SmartFilterManager",
        db: "DatabaseManager",
    ):
        """Discovers code-based, file-based, and plugin-based workflows."""
        logger.info("Discovering workflows...")
        # Store manager references for later use
        self._ai_engine = ai_engine
        self._filter_manager = filter_manager
        self._db = db

        # 1. Register code-based workflows (like the default)
        default_workflow = DefaultWorkflow(ai_engine, filter_manager, db)
        self.register_workflow(default_workflow)

        # 2. Discover file-based workflows
        if not os.path.exists(WORKFLOWS_DIR):
            os.makedirs(WORKFLOWS_DIR)
            logger.info(f"Created workflows directory: {WORKFLOWS_DIR}")

        for filename in os.listdir(WORKFLOWS_DIR):
            if filename.endswith(".json"):
                file_path = os.path.join(WORKFLOWS_DIR, filename)
                try:
                    with open(file_path, "r") as f:
                        config = json.load(f)
                        await self.create_and_register_workflow_from_config(
                            config, from_file=True
                        )
                except Exception as e:
                    logger.error(f"Failed to load workflow from '{filename}': {e}")

        # 3. Load settings and set the active workflow
        settings = self._load_settings()
        active_workflow_name = settings.get("active_workflow")

        if active_workflow_name and active_workflow_name in self._workflows:
            self.set_active_workflow(active_workflow_name, persist=False)
        else:
            self.set_active_workflow(default_workflow.name)

        logger.info(
            f"Workflows discovered. Active workflow: '{self.active_workflow.name}'"
        )

    async def create_and_register_workflow_from_config(
        self, config: Dict[str, Any], from_file: bool = False
    ):
        """Creates, saves, and registers a new workflow from a config dictionary."""
        workflow_name = config.get("name")
        if not workflow_name:
            raise ValueError("Workflow configuration must have a 'name'.")

        if workflow_name in self._workflows and not from_file:
            raise ValueError(f"A workflow with name '{workflow_name}' already exists.")

        # Create the workflow instance first to ensure it's valid
        file_workflow = FileBasedWorkflow(
            self._ai_engine, self._filter_manager, self._db, config
        )

        # Save the configuration to a file if it's a new creation from the API
        if not from_file:
            file_path = WORKFLOWS_DIR / f"{workflow_name}.json"
            if os.path.exists(file_path):
                raise ValueError(f"Workflow file '{file_path}' already exists.")
            try:
                with open(file_path, "w") as f:
                    json.dump(config, f, indent=4)
                logger.info(f"Saved new workflow configuration to '{file_path}'.")
            except IOError as e:
                raise IOError(f"Failed to save workflow file: {e}")

        # Now, register the workflow instance, making it immediately available.
        self.register_workflow(file_workflow)

    def set_active_workflow(self, workflow_name: str, persist: bool = True):
        """Sets the currently active workflow and optionally persists the setting."""
        if workflow_name not in self._workflows:
            raise ValueError(f"Workflow '{workflow_name}' not found.")
        self.active_workflow = self._workflows[workflow_name]
        logger.info(f"Active workflow set to: {self.active_workflow.name}")
        if persist:
            self._save_settings()

    def list_workflows(self) -> List[str]:
        """Returns a list of the names of all registered workflows."""
        return list(self._workflows.keys())

    async def run_workflow(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Runs the active workflow on the given email data."""
        if not self.active_workflow:
            raise RuntimeError("No active workflow is set.")
        return await self.active_workflow.execute(email_data)


class DefaultWorkflow(BaseWorkflow):
    """The default workflow that uses a hardcoded set of models."""

    def __init__(
        self,
        ai_engine: "AdvancedAIEngine",
        filter_manager: "SmartFilterManager",
        db: "DatabaseManager",
    ):
        super().__init__(ai_engine, filter_manager, db)
        self.models = {"sentiment": "sentiment-default", "topic": "topic-default"}

    @property
    def name(self) -> str:
        return "default"

    async def execute(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(
            f"Executing default workflow for email: {email_data.get('subject')}"
        )
        ai_analysis = await self._ai_engine.analyze_email(
            email_data["subject"],
            email_data["content"],
            models_to_use=self.models,
            db=self._db,
        )
        filter_results = await self._filter_manager.apply_filters_to_email_data(
            email_data
        )
        processed_data = email_data.copy()
        processed_data.update(
            {
                "confidence": int(ai_analysis.confidence * 100),
                "categoryId": ai_analysis.category_id,
                "labels": ai_analysis.suggested_labels,
                "analysisMetadata": ai_analysis.to_dict(),
                "filterResults": filter_results,
                "workflow_status": "processed_by_default_workflow",
            }
        )
        return processed_data


class FileBasedWorkflow(BaseWorkflow):
    """A generic workflow configured by a JSON file."""

    def __init__(
        self,
        ai_engine: "AdvancedAIEngine",
        filter_manager: "SmartFilterManager",
        db: "DatabaseManager",
        config: Dict[str, Any],
    ):
        super().__init__(ai_engine, filter_manager, db)
        self._name = config.get("name", "unnamed_file_workflow")
        self.models = config.get("models", {})
        self.description = config.get("description", "")

    @property
    def name(self) -> str:
        return self._name

    async def execute(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(
            f"Executing file-based workflow '{self.name}' for email: {email_data.get('subject')}"
        )
        ai_analysis = await self._ai_engine.analyze_email(
            email_data["subject"],
            email_data["content"],
            models_to_use=self.models,
            db=self._db,
        )
        filter_results = await self._filter_manager.apply_filters_to_email_data(
            email_data
        )
        processed_data = email_data.copy()
        processed_data.update(
            {
                "confidence": int(ai_analysis.confidence * 100),
                "categoryId": ai_analysis.category_id,
                "labels": ai_analysis.suggested_labels,
                "analysisMetadata": ai_analysis.to_dict(),
                "filterResults": filter_results,
                "workflow_status": f"processed_by_{self.name}",
            }
        )
        return processed_data
