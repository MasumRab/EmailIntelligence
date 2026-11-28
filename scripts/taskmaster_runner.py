#!/usr/bin/env python3
"""
Task Master Runner Utility

Provides a unified interface for running task-master parse-prd with fallback to simulation.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Callable, List, Optional


def run_task_master_parse_prd(
    prd_file: str,
    output_dir: str = None,
    fallback_simulation: bool = True,
    extract_task_info_func: Callable = None,
    original_task_files: List[str] = None,
    simulation_description: str = "simulation",
    project_root: str = None,
) -> str:
    """
    Run task-master parse-prd to generate tasks from PRD.
    Falls back to simulation if task-master is not available.

    Args:
        prd_file: Path to the PRD file
        output_dir: Optional output directory for tasks.json
        fallback_simulation: Whether to fall back to simulation if task-master is unavailable
        extract_task_info_func: Function to extract task info from markdown (for simulation)
        original_task_files: List of original task files (for simulation)
        simulation_description: Description for simulation mode output
        project_root: Project root directory for task-master

    Returns:
        Path to the generated tasks.json file
    """
    task_master_available = shutil.which("task-master") is not None

    if task_master_available:
        try:
            cmd = ["task-master", "parse-prd", prd_file]
            if output_dir:
                cmd.extend(["--output", output_dir])
            if project_root:
                cmd.extend(["--project-root", project_root])

            print(f"🚀 Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                print("✅ task-master parse-prd completed successfully")
                output_path = output_dir or ".taskmaster/tasks/tasks.json"
                if os.path.exists(output_path):
                    return output_path
                default_path = ".taskmaster/tasks/tasks.json"
                if os.path.exists(default_path):
                    return default_path
                print(f"⚠️ Output file not found at expected paths, using default")
                return default_path
            else:
                print(f"⚠️ task-master parse-prd failed: {result.stderr}")
                if fallback_simulation:
                    print("Falling back to simulation mode...")
                    return _simulate_parse_prd(
                        prd_file,
                        output_dir,
                        extract_task_info_func,
                        original_task_files,
                        simulation_description,
                    )
                raise RuntimeError(f"task-master parse-prd failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("⚠️ task-master parse-prd timed out (300s limit)")
            if fallback_simulation:
                print("Falling back to simulation mode...")
                return _simulate_parse_prd(
                    prd_file,
                    output_dir,
                    extract_task_info_func,
                    original_task_files,
                    simulation_description,
                )
            raise
        except Exception as e:
            print(f"⚠️ Error running task-master: {e}")
            if fallback_simulation:
                print("Falling back to simulation mode...")
                return _simulate_parse_prd(
                    prd_file,
                    output_dir,
                    extract_task_info_func,
                    original_task_files,
                    simulation_description,
                )
            raise
    elif fallback_simulation:
        print("⚠️ task-master not found in PATH, using simulation mode")
        return _simulate_parse_prd(
            prd_file,
            output_dir,
            extract_task_info_func,
            original_task_files,
            simulation_description,
        )
    else:
        raise RuntimeError("task-master not found and fallback_simulation is disabled")


def _simulate_parse_prd(
    prd_file: str,
    output_dir: str = None,
    extract_task_info_func: Callable = None,
    original_task_files: List[str] = None,
    simulation_description: str = "simulation",
) -> str:
    """
    Fallback simulation when task-master is not available.
    This should only be used for testing when task-master cannot be installed.

    Args:
        prd_file: Path to the PRD file (used for context)
        output_dir: Optional output directory
        extract_task_info_func: Function to extract task info from markdown
        original_task_files: List of original task files
        simulation_description: Description for the output

    Returns:
        Path to the simulated tasks.json file
    """
    print(f"📋 Simulating task-master parse-prd ({simulation_description})")

    if extract_task_info_func is None or original_task_files is None:
        raise ValueError(
            "extract_task_info_func and original_task_files are required for simulation"
        )

    tasks_json = {
        "master": {
            "name": "Task Master",
            "version": "1.0.0",
            "description": f"Tasks generated from PRD ({simulation_description})",
            "lastUpdated": "2026-01-27T00:00:00Z",
            "tasks": [],
        }
    }

    for task_file in original_task_files:
        original_info = extract_task_info_func(task_file)

        simulated_task = {
            "id": original_info["id"],
            "title": original_info["title"],
            "description": original_info.get("purpose", ""),
            "status": original_info.get("status", "pending"),
            "priority": original_info.get("priority", "medium"),
            "dependencies": [],
            "details": original_info.get("details", ""),
            "subtasks": [],
            "testStrategy": original_info.get("test_strategy", ""),
            "complexity": original_info.get("complexity", ""),
            "effort": original_info.get("effort", ""),
            "updatedAt": "2026-01-27T00:00:00Z",
            "createdAt": "2026-01-27T00:00:00Z",
        }

        # Parse dependencies
        deps = original_info.get("dependencies", "")
        if deps and str(deps).lower() not in ["none", "null", ""]:
            deps_list = re.split(r"[,\s]+| and ", str(deps))
            deps_list = [d.strip() for d in deps_list if d.strip()]
            simulated_task["dependencies"] = deps_list

        # Add extended fields if available
        for field in [
            "blocks",
            "initiative",
            "scope",
            "focus",
            "owner",
            "prerequisites",
            "specification_details",
            "implementation_guide",
            "configuration_params",
            "performance_targets",
            "common_gotchas",
            "integration_checkpoint",
            "done_definition",
            "next_steps",
            "extended_metadata",
        ]:
            if original_info.get(field):
                simulated_task[field] = original_info[field]

        # Add success criteria
        if original_info.get("success_criteria"):
            simulated_task["success_criteria"] = original_info["success_criteria"]

        # Add subtasks
        for subtask in original_info.get("subtasks", []):
            simulated_subtask = {
                "id": subtask.get("id", 1),
                "title": subtask.get("title", ""),
                "description": "",
                "dependencies": [],
                "details": "",
                "testStrategy": "",
                "status": subtask.get("status", "pending"),
                "parentId": original_info["id"],
                "effort": "",
            }
            simulated_task["subtasks"].append(simulated_subtask)

        tasks_json["master"]["tasks"].append(simulated_task)

    # Determine output path
    if output_dir:
        output_path = Path(output_dir) / "tasks.json"
    else:
        output_path = Path("simulated_tasks.json")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tasks_json, f, indent=2)

    print(f"📝 Simulated tasks written to: {output_path}")
    return str(output_path)


def check_task_master_available() -> bool:
    """Check if task-master is available in PATH."""
    return shutil.which("task-master") is not None
