"""
Smart Filter Nodes for the Advanced Workflow Engine.

This module provides node implementations that integrate with the SmartFilterManager
to enable intelligent email filtering within workflows.
"""

import logging
from typing import Any, Dict, List, Optional
import time

from .advanced_workflow_engine import BaseNode, NodeMetadata
from .smart_filter_manager import get_smart_filter_manager, EmailFilter

logger = logging.getLogger(__name__)


class SmartFilterInputNode(BaseNode):
    """Node that provides email data as input to smart filtering workflows."""

    def get_metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Smart Filter Input",
            description="Provides email data as input to smart filtering workflows",
            version="1.0.0",
            input_types={},
            output_types={
                "email": dict,
                "subject": str,
                "content": str,
                "sender": str,
                "sender_email": str,
            },
        )

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # Get email data from inputs or use provided email_data parameter
        email_data = inputs.get("email_data", {})

        return {
            "email": email_data,
            "subject": email_data.get("subject", ""),
            "content": email_data.get("content", email_data.get("body", "")),
            "sender": email_data.get("sender", ""),
            "sender_email": email_data.get("sender_email", email_data.get("sender", "")),
        }


class SmartFilterProcessingNode(BaseNode):
    """Node that applies smart filters to email data."""

    def get_metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Smart Filter Processing",
            description="Applies smart filters to email data and returns filtering results",
            version="1.0.0",
            input_types={
                "email": dict,
                "subject": str,
                "content": str,
                "sender": str,
                "sender_email": str,
            },
            output_types={
                "filtered_email": dict,
                "filters_matched": list,
                "actions_taken": list,
                "categories": list,
                "filtering_result": dict,
            },
        )

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # Get the smart filter manager
        filter_manager = get_smart_filter_manager()

        # Prepare email data for filtering
        email_data = inputs.get("email", {})
        email_data["subject"] = inputs.get("subject", "")
        email_data["content"] = inputs.get("content", "")
        email_data["sender"] = inputs.get("sender", "")
        email_data["sender_email"] = inputs.get("sender_email", "")

        # Apply filters to the email
        filtering_result = await filter_manager.apply_filters_to_email(email_data)

        # Update the email with filtering results
        filtered_email = {
            **email_data,
            "filtering_results": filtering_result,
            "filtered_at": time.time(),
        }

        return {
            "filtered_email": filtered_email,
            "filters_matched": filtering_result.get("filters_matched", []),
            "actions_taken": filtering_result.get("actions_taken", []),
            "categories": filtering_result.get("categories", []),
            "filtering_result": filtering_result,
        }


class SmartFilterCreationNode(BaseNode):
    """Node that creates new smart filters from email samples."""

    def get_metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Smart Filter Creation",
            description="Creates new smart filters from email samples",
            version="1.0.0",
            input_types={
                "email_samples": list,
                "filter_name": str,
                "filter_description": str,
                "criteria": dict,
                "actions": dict,
                "priority": int,
            },
            output_types={
                "created_filters": list,
                "new_filter": dict,
                "creation_result": dict,
            },
        )

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # Get the smart filter manager
        filter_manager = get_smart_filter_manager()

        # Check if we're creating intelligent filters from samples
        email_samples = inputs.get("email_samples", [])
        if email_samples:
            # Create intelligent filters from email samples
            created_filters = await filter_manager.create_intelligent_filters(email_samples)
            return {
                "created_filters": [f.__dict__ for f in created_filters],
                "new_filter": created_filters[0].__dict__ if created_filters else {},
                "creation_result": {
                    "status": "success",
                    "message": f"Created {len(created_filters)} intelligent filters",
                    "count": len(created_filters),
                },
            }

        # Check if we're creating a custom filter
        filter_name = inputs.get("filter_name")
        if filter_name:
            # Create a custom filter
            criteria = inputs.get("criteria", {})
            actions = inputs.get("actions", {})
            priority = inputs.get("priority", 5)
            description = inputs.get("filter_description", f"Filter for {filter_name}")

            new_filter = await filter_manager.add_custom_filter(
                name=filter_name,
                description=description,
                criteria=criteria,
                actions=actions,
                priority=priority,
            )

            return {
                "created_filters": [new_filter.__dict__],
                "new_filter": new_filter.__dict__,
                "creation_result": {
                    "status": "success",
                    "message": f"Created custom filter '{filter_name}'",
                    "filter_id": new_filter.filter_id,
                },
            }

        # If no samples or name provided, return empty result
        return {
            "created_filters": [],
            "new_filter": {},
            "creation_result": {
                "status": "error",
                "message": "No email samples or filter name provided",
            },
        }


class SmartFilterManagementNode(BaseNode):
    """Node that manages existing smart filters (update, delete, status)."""

    def get_metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Smart Filter Management",
            description="Manages existing smart filters (update, delete, status)",
            version="1.0.0",
            input_types={
                "filter_id": str,
                "action": str,  # "update", "delete", "enable", "disable", "get"
                "update_data": dict,
            },
            output_types={
                "filter": dict,
                "management_result": dict,
                "filters_list": list,
            },
        )

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # Get the smart filter manager
        filter_manager = get_smart_filter_manager()

        # Get inputs
        filter_id = inputs.get("filter_id")
        action = inputs.get("action", "get").lower()
        update_data = inputs.get("update_data", {})

        try:
            if action == "get" and filter_id:
                # Get a specific filter
                filter_obj = await filter_manager.get_filter_by_id(filter_id)
                if filter_obj:
                    return {
                        "filter": filter_obj.__dict__,
                        "management_result": {
                            "status": "success",
                            "message": f"Retrieved filter {filter_id}",
                        },
                        "filters_list": [],
                    }
                else:
                    return {
                        "filter": {},
                        "management_result": {
                            "status": "error",
                            "message": f"Filter {filter_id} not found",
                        },
                        "filters_list": [],
                    }

            elif action == "update" and filter_id:
                # Update a filter
                result = await filter_manager.update_filter(filter_id, **update_data)
                if result:
                    updated_filter = await filter_manager.get_filter_by_id(filter_id)
                    return {
                        "filter": updated_filter.__dict__ if updated_filter else {},
                        "management_result": {
                            "status": "success",
                            "message": f"Updated filter {filter_id}",
                        },
                        "filters_list": [],
                    }
                else:
                    return {
                        "filter": {},
                        "management_result": {
                            "status": "error",
                            "message": f"Failed to update filter {filter_id}",
                        },
                        "filters_list": [],
                    }

            elif action == "delete" and filter_id:
                # Delete a filter
                result = await filter_manager.delete_filter(filter_id)
                return {
                    "filter": {},
                    "management_result": {
                        "status": "success" if result else "error",
                        "message": f"Deleted filter {filter_id}" if result else f"Failed to delete filter {filter_id}",
                    },
                    "filters_list": [],
                }

            elif action in ["enable", "disable"] and filter_id:
                # Enable or disable a filter
                is_active = action == "enable"
                result = await filter_manager.update_filter_status(filter_id, is_active)
                return {
                    "filter": {},
                    "management_result": {
                        "status": "success" if result else "error",
                        "message": f"{'Enabled' if is_active else 'Disabled'} filter {filter_id}" if result else f"Failed to {action} filter {filter_id}",
                    },
                    "filters_list": [],
                }

            elif action == "list":
                # List all active filters
                filters = await filter_manager.get_active_filters_sorted()
                return {
                    "filter": {},
                    "management_result": {
                        "status": "success",
                        "message": f"Retrieved {len(filters)} active filters",
                    },
                    "filters_list": [f.__dict__ for f in filters],
                }

            elif action == "prune":
                # Prune ineffective filters
                result = await filter_manager.prune_ineffective_filters()
                return {
                    "filter": {},
                    "management_result": {
                        "status": "success",
                        "message": f"Pruned {len(result['pruned_filters'])} filters, disabled {len(result['disabled_filters'])} filters",
                        "pruning_result": result,
                    },
                    "filters_list": [],
                }

            else:
                return {
                    "filter": {},
                    "management_result": {
                        "status": "error",
                        "message": "Invalid action or missing filter_id",
                    },
                    "filters_list": [],
                }

        except Exception as e:
            logger.error(f"Error in SmartFilterManagementNode: {str(e)}")
            return {
                "filter": {},
                "management_result": {
                    "status": "error",
                    "message": f"Error managing filter: {str(e)}",
                },
                "filters_list": [],
            }


# Example workflow demonstrating smart filter integration
def create_smart_filter_workflow_example():
    """Create an example workflow that demonstrates smart filter integration."""
    from .advanced_workflow_engine import Workflow, WorkflowManager, initialize_workflow_system

    # Initialize the workflow system
    workflow_manager = initialize_workflow_system()

    # Register smart filter node types
    workflow_manager.register_node_type("smart_filter_input", SmartFilterInputNode)
    workflow_manager.register_node_type("smart_filter_processing", SmartFilterProcessingNode)
    workflow_manager.register_node_type("smart_filter_creation", SmartFilterCreationNode)
    workflow_manager.register_node_type("smart_filter_management", SmartFilterManagementNode)

    # Create a workflow
    workflow = workflow_manager.create_workflow(
        name="Smart Email Filtering Workflow",
        description="A workflow that demonstrates smart email filtering capabilities",
    )

    # Add nodes to the workflow
    workflow.add_node(
        node_type="smart_filter_input",
        node_id="email_input",
        x=0,
        y=0,
    )

    workflow.add_node(
        node_type="smart_filter_processing",
        node_id="filter_processor",
        x=200,
        y=0,
    )

    workflow.add_node(
        node_type="smart_filter_creation",
        node_id="filter_creator",
        x=400,
        y=0,
    )

    # Add connections between nodes
    workflow.add_connection(
        source_node_id="email_input",
        source_output="email",
        target_node_id="filter_processor",
        target_input="email",
    )

    workflow.add_connection(
        source_node_id="email_input",
        source_output="subject",
        target_node_id="filter_processor",
        target_input="subject",
    )

    workflow.add_connection(
        source_node_id="email_input",
        source_output="content",
        target_node_id="filter_processor",
        target_input="content",
    )

    workflow.add_connection(
        source_node_id="email_input",
        source_output="sender",
        target_node_id="filter_processor",
        target_input="sender",
    )

    workflow.add_connection(
        source_node_id="email_input",
        source_output="sender_email",
        target_node_id="filter_processor",
        target_input="sender_email",
    )

    # Save the workflow
    workflow_manager.save_workflow(workflow)

    return workflow


# Register node types when module is imported
def register_smart_filter_nodes(workflow_manager):
    """Register smart filter node types with the workflow manager."""
    workflow_manager.register_node_type("smart_filter_input", SmartFilterInputNode)
    workflow_manager.register_node_type("smart_filter_processing", SmartFilterProcessingNode)
    workflow_manager.register_node_type("smart_filter_creation", SmartFilterCreationNode)
    workflow_manager.register_node_type("smart_filter_management", SmartFilterManagementNode)