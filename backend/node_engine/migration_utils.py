"""
Workflow Migration Utilities for the Email Intelligence Platform.

This module provides utilities to convert legacy workflow formats
to the new node-based workflow format.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.node_engine.email_nodes import (
    ActionNode,
    AIAnalysisNode,
    EmailSourceNode,
    FilterNode,
    PreprocessingNode,
)
from backend.node_engine.node_base import Connection
from backend.node_engine.node_base import Workflow as NodeWorkflow
from backend.node_engine.workflow_manager import workflow_manager

logger = logging.getLogger(__name__)


class WorkflowMigrationError(Exception):
    """Exception raised when workflow migration fails."""

    pass


class WorkflowMigrationService:
    """Service for migrating legacy workflows to node-based format."""

    def __init__(self):
        self.migration_rules = {
            # Mapping of legacy configuration elements to node types
            "default_workflow": self._migrate_default_workflow,
            "file_based_workflow": self._migrate_file_based_workflow,
        }

    def migrate_legacy_workflow(
        self, workflow_config: Dict[str, Any], workflow_name: str = None
    ) -> NodeWorkflow:
        """
        Migrate a legacy workflow configuration to a node-based workflow.

        Args:
            workflow_config: The legacy workflow configuration dictionary
            workflow_name: Optional name for the new workflow (defaults to legacy name)

        Returns:
            NodeWorkflow: The newly created node-based workflow
        """
        try:
            # Determine workflow type based on configuration structure
            if "models" in workflow_config:
                # This is a file-based workflow
                return self._migrate_file_based_workflow(workflow_config, workflow_name)
            else:
                # Default to file-based migration as it's the most common
                return self._migrate_file_based_workflow(workflow_config, workflow_name)
        except Exception as e:
            logger.error(f"Failed to migrate workflow: {e}")
            raise WorkflowMigrationError(f"Migration failed: {str(e)}")

    def _migrate_file_based_workflow(
        self, config: Dict[str, Any], workflow_name: str = None
    ) -> NodeWorkflow:
        """
        Migrate a file-based legacy workflow to node-based format.

        Legacy file-based workflows typically have:
        - name
        - models (e.g., {"sentiment": "model_name", "topic": "model_name"})
        - description
        """
        workflow_name = workflow_name or config.get("name", "migrated_workflow")
        description = config.get("description", "Migrated from legacy format")

        # Create the new node-based workflow
        node_workflow = NodeWorkflow(
            workflow_id=config.get("workflow_id"), name=workflow_name, description=description
        )

        # Create the standard email processing pipeline
        # 1. Email Source Node
        source_node = EmailSourceNode(
            name="Email Source (Migrated)",
            config={"provider": "legacy_import"},
            node_id="source_" + workflow_name.lower().replace(" ", "_"),
        )
        node_workflow.add_node(source_node)

        # 2. Preprocessing Node
        preprocessing_node = PreprocessingNode(
            name="Email Preprocessor (Migrated)",
            node_id="preprocessing_" + workflow_name.lower().replace(" ", "_"),
        )
        node_workflow.add_node(preprocessing_node)

        # 3. AI Analysis Node (using models from legacy config)
        ai_analysis_node = AIAnalysisNode(
            name="AI Analyzer (Migrated)",
            config={"models": config.get("models", {})},  # Use legacy models
            node_id="ai_analysis_" + workflow_name.lower().replace(" ", "_"),
        )
        node_workflow.add_node(ai_analysis_node)

        # 4. Filter Node (basic implementation)
        filter_node = FilterNode(
            name="Filter (Migrated)", node_id="filter_" + workflow_name.lower().replace(" ", "_")
        )
        node_workflow.add_node(filter_node)

        # 5. Action Node (placeholder)
        action_node = ActionNode(
            name="Action Executor (Migrated)",
            node_id="action_" + workflow_name.lower().replace(" ", "_"),
        )
        node_workflow.add_node(action_node)

        # Create connections following the standard pipeline
        # source -> preprocessing
        node_workflow.add_connection(
            Connection(
                source_node_id=source_node.node_id,
                source_port="emails",
                target_node_id=preprocessing_node.node_id,
                target_port="emails",
            )
        )

        # preprocessing -> ai_analysis
        node_workflow.add_connection(
            Connection(
                source_node_id=preprocessing_node.node_id,
                source_port="processed_emails",
                target_node_id=ai_analysis_node.node_id,
                target_port="emails",
            )
        )

        # ai_analysis -> filter
        node_workflow.add_connection(
            Connection(
                source_node_id=ai_analysis_node.node_id,
                source_port="analysis_results",
                target_node_id=filter_node.node_id,
                target_port="emails",
            )
        )

        # filter -> action
        node_workflow.add_connection(
            Connection(
                source_node_id=filter_node.node_id,
                source_port="filtered_emails",
                target_node_id=action_node.node_id,
                target_port="emails",
            )
        )

        # Also connect analysis results to action as "actions"
        # (for demo purposes in migration)
        node_workflow.add_connection(
            Connection(
                source_node_id=ai_analysis_node.node_id,
                source_port="summary",
                target_node_id=action_node.node_id,
                target_port="actions",
            )
        )

        return node_workflow

    def _migrate_default_workflow(
        self, config: Dict[str, Any], workflow_name: str = None
    ) -> NodeWorkflow:
        """
        Migrate a default legacy workflow to node-based format.
        This is a specialized case for the default workflow.
        """
        # Default workflow has specific models like {"sentiment": "sentiment-default", "topic": "topic-default"}
        # Use the same approach as file-based migration
        return self._migrate_file_based_workflow(config, workflow_name)

    def migrate_workflow_file(self, file_path: str, output_path: str = None) -> str:
        """
        Migrate a legacy workflow from a file to node-based format and save it.

        Args:
            file_path: Path to the legacy workflow file
            output_path: Optional output path for the new workflow (defaults to node engine workflow dir)

        Returns:
            str: Path to the new workflow file
        """
        try:
            # Read legacy workflow file
            with open(file_path, "r", encoding="utf-8") as f:
                legacy_config = json.load(f)

            # Perform migration
            node_workflow = self.migrate_legacy_workflow(legacy_config)

            # Save the new workflow
            if output_path:
                # Save to specified path (needs to be handled manually)
                workflow_manager.save_workflow(node_workflow)
                return f"Workflow saved to default location with ID: {node_workflow.workflow_id}"
            else:
                # Save using the workflow manager to default location
                workflow_manager.save_workflow(node_workflow)
                return f"Workflow saved with ID: {node_workflow.workflow_id}"

        except Exception as e:
            logger.error(f"Failed to migrate workflow file {file_path}: {e}")
            raise WorkflowMigrationError(f"File migration failed: {str(e)}")

    def get_migration_report(self, legacy_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a report about what would be migrated from a legacy configuration.

        Args:
            legacy_config: The legacy workflow configuration

        Returns:
            Dict with migration report details
        """
        report = {
            "original_config_keys": list(legacy_config.keys()),
            "detected_workflow_type": "file_based",
            "models_found": list(legacy_config.get("models", {}).keys()),
            "estimated_nodes": 5,  # source, preprocessing, ai, filter, action
            "connections_estimated": 5,
            "mappable_features": ["models", "description", "name"],
            "potential_issues": [],
        }

        # Check for potential issues
        if not legacy_config.get("models"):
            report["potential_issues"].append("No models specified in legacy config")

        return report


class WorkflowMigrationManager:
    """Manager for handling workflow migrations across the system."""

    def __init__(self):
        self.migration_service = WorkflowMigrationService()
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")

    def migrate_all_legacy_workflows(self, legacy_workflows_dir: str) -> Dict[str, Any]:
        """
        Migrate all legacy workflows in a directory to node-based format.

        Args:
            legacy_workflows_dir: Directory containing legacy workflow files

        Returns:
            Dict with migration summary
        """
        legacy_dir = Path(legacy_workflows_dir)
        if not legacy_dir.exists():
            raise WorkflowMigrationError(
                f"Legacy workflows directory does not exist: {legacy_workflows_dir}"
            )

        summary = {
            "successful_migrations": 0,
            "failed_migrations": 0,
            "errors": [],
            "migrated_files": [],
        }

        for workflow_file in legacy_dir.glob("*.json"):
            try:
                # Migrate individual file
                result = self.migration_service.migrate_workflow_file(str(workflow_file))
                summary["successful_migrations"] += 1
                summary["migrated_files"].append({"original": str(workflow_file), "result": result})
                self.logger.info(f"Successfully migrated: {workflow_file.name}")
            except Exception as e:
                summary["failed_migrations"] += 1
                summary["errors"].append({"file": str(workflow_file), "error": str(e)})
                self.logger.error(f"Failed to migrate {workflow_file.name}: {e}")

        return summary

    def generate_migration_plan(self, legacy_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a detailed migration plan for a legacy workflow.

        Args:
            legacy_config: The legacy workflow configuration

        Returns:
            Dict with detailed migration plan
        """
        report = self.migration_service.get_migration_report(legacy_config)

        # Create a detailed plan
        plan = {
            "report": report,
            "migration_steps": [
                "1. Create Email Source Node",
                "2. Create Preprocessing Node",
                "3. Create AI Analysis Node with legacy models",
                "4. Create Filter Node",
                "5. Create Action Node",
                "6. Connect nodes in standard pipeline order",
            ],
            "node_mapping": {
                "email_source": "EmailSourceNode",
                "preprocessing": "PreprocessingNode",
                "ai_analysis": "AIAnalysisNode (with legacy models)",
                "filter": "FilterNode",
                "action": "ActionNode",
            },
            "connection_pattern": "Linear pipeline: source -> preprocessing -> ai_analysis -> filter -> action",
        }

        return plan


# Global migration manager instance
migration_manager = WorkflowMigrationManager()


# Convenience functions for direct usage
def migrate_legacy_workflow(
    legacy_config: Dict[str, Any], workflow_name: str = None
) -> NodeWorkflow:
    """Migrate a legacy workflow configuration to node-based format."""
    return migration_manager.migration_service.migrate_legacy_workflow(legacy_config, workflow_name)


def migrate_workflow_file(file_path: str, output_path: str = None) -> str:
    """Migrate a legacy workflow file to node-based format."""
    return migration_manager.migration_service.migrate_workflow_file(file_path, output_path)


def get_migration_report(legacy_config: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a migration report for a legacy configuration."""
    return migration_manager.migration_service.get_migration_report(legacy_config)


def migrate_all_legacy_workflows(legacy_workflows_dir: str) -> Dict[str, Any]:
    """Migrate all legacy workflows in a directory."""
    return migration_manager.migrate_all_legacy_workflows(legacy_workflows_dir)


def generate_migration_plan(legacy_config: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a detailed migration plan for a legacy workflow."""
    return migration_manager.generate_migration_plan(legacy_config)
