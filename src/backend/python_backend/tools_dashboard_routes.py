"""
Tools Dashboard API Routes.

This module provides API endpoints for accessing and managing the various scripts,
tools, and isolated components of the Email Intelligence platform.
"""

import asyncio
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from src.core.auth import get_current_active_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/tools", tags=["tools"])

# Define the project root for script execution
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


class ScriptExecutionRequest(BaseModel):
    """Request model for script execution."""
    script_name: str
    args: Optional[List[str]] = None
    working_directory: Optional[str] = None


class ScriptExecutionResponse(BaseModel):
    """Response model for script execution."""
    script_name: str
    status: str
    output: Optional[str] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    timestamp: datetime


class ToolStatus(BaseModel):
    """Status model for individual tools."""
    name: str
    category: str
    status: str
    description: str
    last_run: Optional[datetime] = None
    health_check: Optional[str] = None


class ToolsDashboardResponse(BaseModel):
    """Response model for tools dashboard overview."""
    tools: List[ToolStatus]
    categories: List[str]
    system_health: Dict[str, Any]


# Define available tools and scripts
AVAILABLE_TOOLS = [
    # Context Control Tools
    {
        "name": "context-control",
        "category": "Context Control",
        "description": "CLI tool for Agent Context Control",
        "script_path": "scripts/context-control",
        "health_check": "validate_context"
    },
    {
        "name": "validate_imports",
        "category": "Validation",
        "description": "Import validation script for CI/CD pipeline",
        "script_path": "scripts/validate_imports.py",
        "health_check": "check_imports"
    },
    {
        "name": "worktree_context_detector",
        "category": "Validation",
        "description": "Detect worktree context for git hooks",
        "script_path": "scripts/worktree_context_detector.py",
        "health_check": "check_worktree"
    },

    # Agent Tools
    {
        "name": "agent_performance_monitor",
        "category": "Monitoring",
        "description": "Real-time agent performance metrics",
        "script_path": "scripts/agents/agent_performance_monitor.py",
        "health_check": "check_agent_health"
    },
    {
        "name": "agent_health_monitor",
        "category": "Monitoring",
        "description": "Monitor agent health status",
        "script_path": "scripts/agents/agent_health_monitor.py",
        "health_check": "check_agent_status"
    },

    # Analysis and Code Quality Tools
    {
        "name": "codebase_analysis",
        "category": "Analysis",
        "description": "Comprehensive codebase analysis for issues",
        "script_path": "codebase_analysis.py",
        "health_check": "check_codebase"
    },
    {
        "name": "analyze_repo",
        "category": "Analysis",
        "description": "Repository analysis and metrics",
        "script_path": "analyze_repo.py",
        "health_check": "check_repo_analysis"
    },

    # Task Management Tools
    {
        "name": "task_completion_tracker",
        "category": "Task Management",
        "description": "Track task completion progress",
        "script_path": "scripts/task_completion_tracker.py",
        "health_check": "check_task_tracking"
    },
    {
        "name": "completion_predictor",
        "category": "Task Management",
        "description": "Predict task completion times",
        "script_path": "scripts/completion_predictor.py",
        "health_check": "check_prediction"
    },

    # Maintenance and Documentation Tools
    {
        "name": "maintenance_scheduler",
        "category": "Maintenance",
        "description": "Schedule and manage maintenance tasks",
        "script_path": "scripts/maintenance_scheduler.py",
        "health_check": "check_maintenance"
    },
    {
        "name": "maintenance_docs",
        "category": "Documentation",
        "description": "Generate maintenance documentation",
        "script_path": "scripts/maintenance_docs.py",
        "health_check": "check_docs"
    },

    # Validation and Testing Tools
    {
        "name": "incremental_validator",
        "category": "Validation",
        "description": "Incremental validation of changes",
        "script_path": "scripts/incremental_validator.py",
        "health_check": "check_incremental_validation"
    },
    {
        "name": "validation_cache",
        "category": "Validation",
        "description": "Cache validation results for performance",
        "script_path": "scripts/validation_cache.py",
        "health_check": "check_validation_cache"
    }
]


def get_tool_categories() -> List[str]:
    """Get unique tool categories."""
    return list(set(tool["category"] for tool in AVAILABLE_TOOLS))


async def run_script_safely(script_path: str, args: Optional[List[str]] = None,
                          working_directory: Optional[str] = None) -> Dict[str, Any]:
    """
    Run a script safely with proper error handling and timeout.

    Args:
        script_path: Path to the script relative to project root
        args: Optional list of arguments to pass to the script
        working_directory: Optional working directory override

    Returns:
        Dict containing execution results
    """
    start_time = datetime.now()
    full_script_path = PROJECT_ROOT / script_path

    if not full_script_path.exists():
        return {
            "status": "error",
            "error": f"Script not found: {script_path}",
            "execution_time": (datetime.now() - start_time).total_seconds()
        }

    try:
        # Prepare command
        if script_path.endswith('.py'):
            cmd = [sys.executable, str(full_script_path)]
        else:
            cmd = [str(full_script_path)]

        if args:
            cmd.extend(args)

        # Execute script with timeout
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=working_directory or str(PROJECT_ROOT),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**dict(os.environ), "PYTHONPATH": str(PROJECT_ROOT)}
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=30.0  # 30 second timeout
            )
        except asyncio.TimeoutError:
            process.kill()
            return {
                "status": "timeout",
                "error": "Script execution timed out after 30 seconds",
                "execution_time": 30.0
            }

        execution_time = (datetime.now() - start_time).total_seconds()

        return {
            "status": "success" if process.returncode == 0 else "error",
            "output": stdout.decode('utf-8', errors='ignore').strip() if stdout else None,
            "error": stderr.decode('utf-8', errors='ignore').strip() if stderr else None,
            "execution_time": execution_time,
            "return_code": process.returncode
        }

    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        return {
            "status": "error",
            "error": f"Failed to execute script: {str(e)}",
            "execution_time": execution_time
        }


async def check_tool_health(tool_config: Dict[str, Any]) -> str:
    """
    Perform a basic health check for a tool.

    Args:
        tool_config: Tool configuration dictionary

    Returns:
        Health status string
    """
    script_path = tool_config["script_path"]

    # For Python scripts, try importing the module first
    if script_path.endswith('.py'):
        try:
            module_name = script_path.replace('.py', '').replace('/', '.')
            if module_name.startswith('scripts.'):
                module_name = module_name  # Already correct
            elif module_name.startswith('scripts/'):
                module_name = module_name.replace('scripts/', 'scripts.')

            # Try to import the module
            __import__(module_name)
            return "healthy"
        except ImportError:
            return "import_error"
        except Exception as e:
            return f"error: {str(e)}"
    else:
        # For non-Python scripts, check if file exists and is executable
        full_path = PROJECT_ROOT / script_path
        if full_path.exists():
            import stat
            if full_path.stat().st_mode & stat.S_IEXEC:
                return "healthy"
            else:
                return "not_executable"
        else:
            return "not_found"


@router.get("/dashboard", response_model=ToolsDashboardResponse)
async def get_tools_dashboard(
    current_user: str = Depends(get_current_active_user)
):
    """
    Get the tools dashboard overview with all available tools and their status.

    Returns:
        ToolsDashboardResponse: Dashboard data with tool statuses
    """
    try:
        logger.info(f"Tools dashboard requested by user: {current_user}")

        tools_status = []
        for tool_config in AVAILABLE_TOOLS:
            health_status = await check_tool_health(tool_config)
            tools_status.append(ToolStatus(
                name=tool_config["name"],
                category=tool_config["category"],
                status=health_status,
                description=tool_config["description"],
                health_check=tool_config["health_check"]
            ))

        # Get system health information
        system_health = {
            "total_tools": len(AVAILABLE_TOOLS),
            "healthy_tools": sum(1 for tool in tools_status if tool.status == "healthy"),
            "categories": get_tool_categories(),
            "last_updated": datetime.now()
        }

        return ToolsDashboardResponse(
            tools=tools_status,
            categories=get_tool_categories(),
            system_health=system_health
        )

    except Exception as e:
        logger.error(f"Error fetching tools dashboard for user {current_user}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching tools dashboard.")


@router.post("/execute", response_model=ScriptExecutionResponse)
async def execute_script(
    request: ScriptExecutionRequest,
    background_tasks: BackgroundTasks,
    current_user: str = Depends(get_current_active_user)
):
    """
    Execute a script with the given parameters.

    Args:
        request: Script execution request
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user

    Returns:
        ScriptExecutionResponse: Execution results
    """
    try:
        logger.info(f"Script execution requested by user {current_user}: {request.script_name}")

        # Find the tool configuration
        tool_config = None
        for tool in AVAILABLE_TOOLS:
            if tool["name"] == request.script_name:
                tool_config = tool
                break

        if not tool_config:
            raise HTTPException(status_code=404, detail=f"Tool '{request.script_name}' not found")

        # Execute the script
        result = await run_script_safely(
            tool_config["script_path"],
            request.args,
            request.working_directory
        )

        response = ScriptExecutionResponse(
            script_name=request.script_name,
            status=result["status"],
            output=result.get("output"),
            error=result.get("error"),
            execution_time=result.get("execution_time"),
            timestamp=datetime.now()
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing script {request.script_name} for user {current_user}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error executing script: {str(e)}")


@router.get("/categories")
async def get_tool_categories_endpoint(
    current_user: str = Depends(get_current_active_user)
):
    """
    Get all available tool categories.

    Returns:
        Dict with categories list
    """
    return {"categories": get_tool_categories()}


@router.get("/tools/{category}")
async def get_tools_by_category(
    category: str,
    current_user: str = Depends(get_current_active_user)
):
    """
    Get all tools in a specific category.

    Args:
        category: Tool category to filter by

    Returns:
        List of tools in the category
    """
    tools_in_category = [
        tool for tool in AVAILABLE_TOOLS
        if tool["category"].lower() == category.lower()
    ]

    tools_status = []
    for tool_config in tools_in_category:
        health_status = await check_tool_health(tool_config)
        tools_status.append(ToolStatus(
            name=tool_config["name"],
            category=tool_config["category"],
            status=health_status,
            description=tool_config["description"],
            health_check=tool_config["health_check"]
        ))

    return {"tools": tools_status}