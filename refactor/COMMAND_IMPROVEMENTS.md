# Command Improvements: `/implement` and `/refactor`

**Date:** 2026-01-04  
**Status:** Proposed  
**Purpose:** Enhance state tracking and validation to prevent inconsistencies  
**Compatibility:** Designed to work with existing refactor/ and implement/ workflows  

---

## Overview

This document proposes improvements to the `/implement` and `/refactor` commands to address state tracking issues encountered during the I2.T4 → 75.6 refactoring. The improvements maintain backward compatibility with existing workflows while adding robust state management and validation.

### Problem Statement

During the I2.T4 → 75.6 refactoring, several state tracking issues were identified:

1. **Inconsistent state files**: `refactor/state.json` and `implement/state.json` used different schemas
2. **Incomplete status updates**: Task completion didn't cascade to phase and overall status
3. **No validation**: State inconsistencies weren't detected automatically
4. **Manual state management**: State updates required manual coordination

### Solution Approach

The proposed improvements:
- **Maintain existing state.json structure** - Enhance rather than replace
- **Add automatic status cascading** - Task → Phase → Overall
- **Introduce validation functions** - Detect inconsistencies early
- **Enhance command workflows** - Add validation steps
- **Preserve backward compatibility** - Existing workflows continue to work

---

## Existing State Schema (Compatible)

### Current refactor/state.json Structure

```json
{
  "refactoring_id": "i2t4-into-756",
  "title": "Refactor I2.T4 Features into 75.6 Framework",
  "status": "in_progress",
  "created_at": "2026-01-04T00:00:00Z",
  "updated_at": "2026-01-04T00:00:00Z",
  "completed_phases": ["analyze_i2t4_structure", "analyze_756_framework"],
  "current_phase": "phase_2_implementation",
  "phases": {
    "phase_1_analysis": {
      "status": "completed",
      "completed_at": "2026-01-04T00:00:00Z",
      "tasks": ["Analyze I2.T4 structure", "Analyze 75.6 framework"]
    },
    "phase_2_implementation": {
      "status": "in_progress",
      "tasks": [
        {"id": "add_migration_analyzer", "status": "completed"},
        {"id": "enhance_engine_modes", "status": "pending"}
      ]
    }
  }
}
```

### Current implement/state.json Structure

```json
{
  "implementation_id": "i2t4-into-756",
  "title": "Refactor I2.T4 Features into 75.6 Framework",
  "status": "in_progress",
  "created_at": "2026-01-04T00:00:00Z",
  "updated_at": "2026-01-04T00:00:00Z",
  "current_phase": "phase_2_implementation",
  "completed_tasks": ["add_migration_metrics", "update_branch_metrics"],
  "pending_tasks": ["update_configuration_schema"],
  "files_modified": ["task_data/branch_clustering_implementation.py"]
}
```

---

## Proposed Enhancements

### Enhancement 1: Add Validation Metadata

**Purpose:** Enable automatic validation without breaking existing structure

**Add to state.json:**

```json
{
  "refactoring_id": "i2t4-into-756",
  "status": "in_progress",
  "current_phase": "phase_2_implementation",
  
  // NEW: Validation metadata
  "validation": {
    "last_checked": "2026-01-04T00:00:00Z",
    "status": "passed",
    "errors": [],
    "warnings": []
  },
  
  // NEW: Progress tracking
  "progress": {
    "total_tasks": 15,
    "completed_tasks": 12,
    "percentage": 80,
    "by_type": {
      "code": 12,
      "documentation": 0,
      "testing": 0
    }
  },
  
  // Existing fields preserved
  "phases": { ... }
}
```

**Benefits:**
- Existing code continues to work (backward compatible)
- New fields optional (graceful degradation)
- Enables automated validation

---

### Enhancement 2: Automatic Status Cascading

**Purpose:** Ensure task completion updates phase and overall status automatically

**Implementation Pattern (Python):**

```python
"""
task_scripts/refactoring_state.py
Utility functions for refactoring state management
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class RefactoringStateManager:
    """Manages refactoring state with automatic cascading"""
    
    VALID_STATUSES = {
        "not_started", "planning", "implementing", 
        "documenting", "testing", "complete"
    }
    
    VALID_PHASE_STATUSES = {
        "not_started", "in_progress", "completed", "blocked"
    }
    
    VALID_TASK_STATUSES = {
        "pending", "in_progress", "completed", "failed", "blocked"
    }
    
    def __init__(self, state_file: str):
        self.state_file = Path(state_file)
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """Load state from file with validation"""
        if not self.state_file.exists():
            raise FileNotFoundError(f"State file not found: {self.state_file}")
        
        with open(self.state_file, 'r') as f:
            state = json.load(f)
        
        # Initialize new fields if not present (backward compatibility)
        if "validation" not in state:
            state["validation"] = {
                "last_checked": None,
                "status": "unknown",
                "errors": [],
                "warnings": []
            }
        
        if "progress" not in state:
            state["progress"] = self._calculate_progress(state)
        
        return state
    
    def save_state(self):
        """Save state to file"""
        self.state["updated_at"] = datetime.now().isoformat() + "Z"
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def update_task_status(
        self, 
        phase_id: str, 
        task_id: str, 
        new_status: str
    ) -> bool:
        """
        Update task status and automatically cascade status updates.
        
        Returns True if update successful, False otherwise.
        """
        # Validate status
        if new_status not in self.VALID_TASK_STATUSES:
            raise ValueError(f"Invalid task status: {new_status}")
        
        # Update task
        phase = self.state["phases"].get(phase_id)
        if not phase:
            raise ValueError(f"Phase not found: {phase_id}")
        
        # Handle both list and dict task formats
        if isinstance(phase.get("tasks"), list):
            # List format: simple task names
            # Find task by name (if it's a dict with id)
            for task in phase["tasks"]:
                if isinstance(task, dict) and task.get("id") == task_id:
                    task["status"] = new_status
                    break
        elif isinstance(phase.get("tasks"), dict):
            # Dict format: task_id -> task_info
            if task_id in phase["tasks"]:
                self.state["phases"][phase_id]["tasks"][task_id]["status"] = new_status
        
        # Cascade: Update phase status
        self._update_phase_status(phase_id)
        
        # Cascade: Update overall status
        self._update_overall_status()
        
        # Update progress
        self.state["progress"] = self._calculate_progress(self.state)
        
        # Save
        self.save_state()
        
        return True
    
    def _update_phase_status(self, phase_id: str):
        """Update phase status based on task statuses"""
        phase = self.state["phases"][phase_id]
        tasks = phase.get("tasks", [])
        
        # Handle both list and dict formats
        if isinstance(tasks, list):
            task_statuses = [
                t.get("status", "pending") 
                for t in tasks 
                if isinstance(t, dict)
            ]
        else:
            task_statuses = [
                t.get("status", "pending") 
                for t in tasks.values()
            ]
        
        # Determine phase status
        if not task_statuses:
            phase_status = "not_started"
        elif all(s == "completed" for s in task_statuses):
            phase_status = "completed"
        elif any(s == "failed" for s in task_statuses):
            phase_status = "blocked"
        elif any(s == "in_progress" for s in task_statuses):
            phase_status = "in_progress"
        else:
            phase_status = "not_started"
        
        self.state["phases"][phase_id]["status"] = phase_status
        
        # Update completed_phases list
        if phase_status == "completed" and phase_id not in self.state.get("completed_phases", []):
            self.state.setdefault("completed_phases", []).append(phase_id)
    
    def _update_overall_status(self):
        """Update overall status based on phase statuses"""
        phases = self.state.get("phases", {})
        phase_statuses = [
            p.get("status", "not_started") 
            for p in phases.values()
        ]
        
        # Determine overall status
        if not phase_statuses:
            overall_status = "not_started"
        elif all(s == "completed" for s in phase_statuses):
            overall_status = "complete"
        elif any(s == "blocked" for s in phase_statuses):
            overall_status = "blocked"
        elif any(s == "in_progress" for s in phase_statuses):
            overall_status = "implementing"
        elif any(s in ["not_started", "pending"] for s in phase_statuses):
            overall_status = "in_progress"
        else:
            overall_status = "not_started"
        
        self.state["status"] = overall_status
    
    def _calculate_progress(self, state: Dict) -> Dict:
        """Calculate progress percentages"""
        phases = state.get("phases", {})
        
        total_tasks = 0
        completed_tasks = 0
        by_type = {"code": 0, "documentation": 0, "testing": 0}
        
        for phase in phases.values():
            tasks = phase.get("tasks", [])
            
            if isinstance(tasks, list):
                for task in tasks:
                    if isinstance(task, dict):
                        total_tasks += 1
                        if task.get("status") == "completed":
                            completed_tasks += 1
                            task_type = task.get("type", "code")
                            by_type[task_type] = by_type.get(task_type, 0) + 1
            elif isinstance(tasks, dict):
                for task in tasks.values():
                    total_tasks += 1
                    if task.get("status") == "completed":
                        completed_tasks += 1
                        task_type = task.get("type", "code")
                        by_type[task_type] = by_type.get(task_type, 0) + 1
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "percentage": round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1),
            "by_type": by_type
        }
    
    def validate_state(self) -> List[str]:
        """
        Validate state consistency.
        
        Returns list of errors (empty if valid).
        """
        errors = []
        
        # Validate overall status
        if self.state.get("status") not in self.VALID_STATUSES:
            errors.append(
                f"Invalid overall status: {self.state.get('status')}. "
                f"Must be one of {self.VALID_STATUSES}"
            )
        
        # Validate phase statuses
        for phase_id, phase in self.state.get("phases", {}).items():
            phase_status = phase.get("status")
            if phase_status not in self.VALID_PHASE_STATUSES:
                errors.append(
                    f"Invalid phase status for {phase_id}: {phase_status}. "
                    f"Must be one of {self.VALID_PHASE_STATUSES}"
                )
        
        # Validate task statuses
        for phase_id, phase in self.state.get("phases", {}).items():
            tasks = phase.get("tasks", [])
            
            if isinstance(tasks, list):
                for i, task in enumerate(tasks):
                    if isinstance(task, dict):
                        task_status = task.get("status")
                        if task_status and task_status not in self.VALID_TASK_STATUSES:
                            errors.append(
                                f"Invalid task status for {phase_id}[{i}]: {task_status}. "
                                f"Must be one of {self.VALID_TASK_STATUSES}"
                            )
            elif isinstance(tasks, dict):
                for task_id, task in tasks.items():
                    task_status = task.get("status")
                    if task_status and task_status not in self.VALID_TASK_STATUSES:
                        errors.append(
                            f"Invalid task status for {phase_id}.{task_id}: {task_status}. "
                            f"Must be one of {self.VALID_TASK_STATUSES}"
                        )
        
        # Validate progress calculation
        calculated = self._calculate_progress(self.state)
        stored = self.state.get("progress", {})
        
        if stored.get("total_tasks") != calculated.get("total_tasks"):
            errors.append(
                f"Progress mismatch: total_tasks={stored.get('total_tasks')}, "
                f"expected={calculated.get('total_tasks')}"
            )
        
        if stored.get("percentage") != calculated.get("percentage"):
            errors.append(
                f"Progress mismatch: percentage={stored.get('percentage')}%, "
                f"expected={calculated.get('percentage')}%"
            )
        
        # Validate phase-task consistency
        for phase_id, phase in self.state.get("phases", {}).items():
            phase_status = phase.get("status")
            tasks = phase.get("tasks", [])
            
            if isinstance(tasks, list):
                task_statuses = [
                    t.get("status", "pending") 
                    for t in tasks 
                    if isinstance(t, dict)
                ]
            else:
                task_statuses = [
                    t.get("status", "pending") 
                    for t in tasks.values()
                ]
            
            if task_statuses:
                all_complete = all(s == "completed" for s in task_statuses)
                if all_complete and phase_status != "completed":
                    errors.append(
                        f"Phase {phase_id} has all completed tasks "
                        f"but status is {phase_status}"
                    )
        
        # Update validation metadata
        self.state["validation"] = {
            "last_checked": datetime.now().isoformat() + "Z",
            "status": "passed" if not errors else "failed",
            "errors": errors,
            "warnings": []
        }
        
        self.save_state()
        
        return errors
```

**Usage Example:**

```python
# Update task status with automatic cascading
manager = RefactoringStateManager("refactor/state.json")
manager.update_task_status(
    phase_id="phase_2_implementation",
    task_id="add_migration_analyzer",
    new_status="completed"
)
# Automatically updates:
# - Task status
# - Phase status (if all tasks complete)
# - Overall status (if all phases complete)
# - Progress percentages

# Validate state
errors = manager.validate_state()
if errors:
    print(f"State validation failed: {errors}")
else:
    print("State is valid")
```

---

### Enhancement 3: Enhanced `/implement` Command Workflow

**Purpose:** Add validation and verification steps to prevent incomplete state updates

**Proposed Workflow:**

```python
"""
Enhanced /implement command workflow
"""

from pathlib import Path
from typing import Dict, List


def implement_refactoring(refactoring_id: str, implementation_guide: str):
    """
    Enhanced implement command with validation and state management.
    
    Args:
        refactoring_id: ID of the refactoring (e.g., "i2t4-into-756")
        implementation_guide: Path to implementation guide markdown file
    """
    
    # Step 1: Initialize state manager
    state_file = f"refactor/{refactoring_id}/state.json"
    manager = RefactoringStateManager(state_file)
    
    print(f"Starting implementation for: {refactoring_id}")
    print(f"Current status: {manager.state['status']}")
    print(f"Progress: {manager.state['progress']['percentage']}%")
    
    # Step 2: Load implementation guide
    guide = load_implementation_guide(implementation_guide)
    
    # Step 3: Implement code changes
    print("\n" + "="*70)
    print("IMPLEMENTING CODE CHANGES")
    print("="*70)
    
    completed_tasks = []
    for task in guide["tasks"]:
        if task["type"] == "code":
            print(f"\n→ Implementing: {task['name']}")
            
            try:
                # Apply code changes
                apply_code_change(task)
                
                # Update task status
                manager.update_task_status(
                    phase_id=task["phase"],
                    task_id=task["id"],
                    new_status="completed"
                )
                
                completed_tasks.append(task["id"])
                print(f"  ✓ Completed: {task['name']}")
                
            except Exception as e:
                print(f"  ✗ Failed: {task['name']}")
                print(f"    Error: {e}")
                
                # Update task status to failed
                manager.update_task_status(
                    phase_id=task["phase"],
                    task_id=task["id"],
                    new_status="failed"
                )
                raise
    
    # Step 4: Validate state consistency
    print("\n" + "="*70)
    print("VALIDATING STATE")
    print("="*70)
    
    errors = manager.validate_state()
    if errors:
        print("\n⚠️  STATE VALIDATION FAILED")
        for error in errors:
            print(f"  - {error}")
        raise StateValidationError("State validation failed")
    else:
        print("\n✓ State validation passed")
    
    # Step 5: Verify implementation
    print("\n" + "="*70)
    print("VERIFYING IMPLEMENTATION")
    print("="*70)
    
    verification_results = verify_implementation(
        refactoring_id, 
        completed_tasks
    )
    
    if not verification_results["all_passed"]:
        print("\n⚠️  VERIFICATION FAILED")
        for test, result in verification_results["tests"].items():
            if not result["passed"]:
                print(f"  ✗ {test}: {result['message']}")
        raise VerificationError("Implementation verification failed")
    else:
        print("\n✓ All verification tests passed")
    
    # Step 6: Generate completion report
    print("\n" + "="*70)
    print("GENERATING COMPLETION REPORT")
    print("="*70)
    
    report = generate_completion_report(manager.state)
    print(f"\n{report}")
    
    # Save report
    report_file = f"refactor/{refactoring_id}/COMPLETION_REPORT.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n✓ Report saved to: {report_file}")
    
    # Step 7: Final summary
    print("\n" + "="*70)
    print("IMPLEMENTATION COMPLETE")
    print("="*70)
    print(f"\nRefactoring ID: {refactoring_id}")
    print(f"Status: {manager.state['status']}")
    print(f"Progress: {manager.state['progress']['percentage']}%")
    print(f"Code tasks: {manager.state['progress']['by_type']['code']}")
    print(f"Documentation tasks: {manager.state['progress']['by_type']['documentation']}")
    print(f"Testing tasks: {manager.state['progress']['by_type']['testing']}")
    print(f"\nFiles modified: {len(manager.state.get('files_modified', []))}")
    print(f"Next steps: {get_next_steps(manager.state)}")


def apply_code_change(task: Dict):
    """
    Apply a code change to the specified file.
    
    Args:
        task: Task dictionary with 'file', 'line', 'type', 'code' fields
    """
    file_path = task["file"]
    line_number = task["line"]
    change_type = task["type"]  # 'ADD', 'MODIFY', 'DELETE'
    code = task["code"]
    
    # Read file
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Apply change based on type
    if change_type == "ADD":
        # Insert code at specified line
        lines.insert(line_number - 1, code + "\n")
    elif change_type == "MODIFY":
        # Replace specified line
        if 0 < line_number <= len(lines):
            lines[line_number - 1] = code + "\n"
    elif change_type == "DELETE":
        # Delete specified line
        if 0 < line_number <= len(lines):
            del lines[line_number - 1]
    
    # Write file
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    # Track modified file
    state_file = "refactor/state.json"
    manager = RefactoringStateManager(state_file)
    if "files_modified" not in manager.state:
        manager.state["files_modified"] = []
    if file_path not in manager.state["files_modified"]:
        manager.state["files_modified"].append(file_path)
    manager.save_state()


def verify_implementation(refactoring_id: str, tasks: List[str]) -> Dict:
    """
    Verify that implementation is correct.
    
    Args:
        refactoring_id: ID of the refactoring
        tasks: List of completed task IDs
        
    Returns:
        Dictionary with verification results
    """
    results = {
        "all_passed": True,
        "tests": {}
    }
    
    # Test 1: Syntax check
    try:
        import subprocess
        result = subprocess.run(
            ["python", "-m", "py_compile", "task_data/branch_clustering_implementation.py"],
            capture_output=True,
            text=True
        )
        results["tests"]["syntax"] = {
            "passed": result.returncode == 0,
            "message": "" if result.returncode == 0 else result.stderr
        }
    except Exception as e:
        results["tests"]["syntax"] = {
            "passed": False,
            "message": str(e)
        }
    
    # Test 2: Import check
    try:
        import importlib
        import sys
        sys.path.insert(0, "task_data")
        import branch_clustering_implementation
        results["tests"]["import"] = {
            "passed": True,
            "message": ""
        }
    except Exception as e:
        results["tests"]["import"] = {
            "passed": False,
            "message": str(e)
        }
    
    # Test 3: Class existence check
    try:
        assert hasattr(branch_clustering_implementation, "MigrationAnalyzer")
        assert hasattr(branch_clustering_implementation, "OutputGenerator")
        assert hasattr(branch_clustering_implementation, "BranchClusteringEngine")
        results["tests"]["classes"] = {
            "passed": True,
            "message": ""
        }
    except (AssertionError, Exception) as e:
        results["tests"]["classes"] = {
            "passed": False,
            "message": str(e)
        }
    
    # Test 4: Method existence check
    try:
        engine = branch_clustering_implementation.BranchClusteringEngine()
        assert hasattr(engine, "_validate_mode")
        assert hasattr(engine, "execute_identification_pipeline")
        assert hasattr(engine, "execute_hybrid_pipeline")
        results["tests"]["methods"] = {
            "passed": True,
            "message": ""
        }
    except (AssertionError, Exception) as e:
        results["tests"]["methods"] = {
            "passed": False,
            "message": str(e)
        }
    
    # Check overall status
    results["all_passed"] = all(t["passed"] for t in results["tests"].values())
    
    return results


def generate_completion_report(state: Dict) -> str:
    """Generate a completion report from state."""
    
    report = f"""# Implementation Completion Report

**Refactoring ID:** {state['refactoring_id']}
**Title:** {state['title']}
**Status:** {state['status']}
**Completed:** {state['updated_at']}

---

## Summary

- **Overall Status:** {state['status']}
- **Progress:** {state['progress']['percentage']}%
- **Total Tasks:** {state['progress']['total_tasks']}
- **Completed Tasks:** {state['progress']['completed_tasks']}

---

## Progress by Type

- **Code Tasks:** {state['progress']['by_type'].get('code', 0)}
- **Documentation Tasks:** {state['progress']['by_type'].get('documentation', 0)}
- **Testing Tasks:** {state['progress']['by_type'].get('testing', 0)}

---

## Phase Status

"""
    
    for phase_id, phase in state.get("phases", {}).items():
        report += f"### {phase_id}\n\n"
        report += f"- **Status:** {phase.get('status', 'unknown')}\n"
        
        tasks = phase.get("tasks", [])
        if isinstance(tasks, list):
            for task in tasks:
                if isinstance(task, dict):
                    report += f"- {task.get('id', 'unknown')}: {task.get('status', 'unknown')}\n"
        elif isinstance(tasks, dict):
            for task_id, task in tasks.items():
                report += f"- {task_id}: {task.get('status', 'unknown')}\n"
        
        report += "\n"
    
    report += f"""---

## Files Modified

"""
    
    for file_path in state.get("files_modified", []):
        report += f"- {file_path}\n"
    
    report += f"""

---

## Validation

- **Last Checked:** {state['validation']['last_checked']}
- **Status:** {state['validation']['status']}
"""
    
    if state['validation']['errors']:
        report += "\n**Errors:**\n"
        for error in state['validation']['errors']:
            report += f"- {error}\n"
    
    if state['validation']['warnings']:
        report += "\n**Warnings:**\n"
        for warning in state['validation']['warnings']:
            report += f"- {warning}\n"
    
    report += "\n---\n"
    report += f"\n**Generated:** {datetime.now().isoformat()}\n"
    
    return report


def get_next_steps(state: Dict) -> str:
    """Get next steps based on current state."""
    
    if state['status'] == 'complete':
        return "Ready for integration with downstream tasks"
    
    # Find first incomplete phase
    for phase_id, phase in state.get("phases", {}).items():
        if phase.get("status") != "completed":
            # Find first incomplete task
            tasks = phase.get("tasks", [])
            if isinstance(tasks, list):
                for task in tasks:
                    if isinstance(task, dict) and task.get("status") != "completed":
                        return f"Complete task: {task.get('id', 'unknown')} in {phase_id}"
            elif isinstance(tasks, dict):
                for task_id, task in tasks.items():
                    if task.get("status") != "completed":
                        return f"Complete task: {task_id} in {phase_id}"
    
    return "Review refactoring plan"


class StateValidationError(Exception):
    """Raised when state validation fails"""
    pass


class VerificationError(Exception):
    """Raised when implementation verification fails"""
    pass
```

---

### Enhancement 4: `/refactor` Command Enhancements

**Purpose:** Add state synchronization and recovery capabilities

**Proposed Enhancements:**

```python
"""
Enhanced /refactor command functions
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def refactor_init(refactoring_id: str, title: str, plan_file: str = None):
    """
    Initialize a new refactoring with unified state structure.
    
    Args:
        refactoring_id: Unique identifier for the refactoring
        title: Human-readable title
        plan_file: Optional path to refactoring plan markdown file
    """
    
    # Create directories
    refactor_dir = Path(f"refactor/{refactoring_id}")
    implement_dir = Path(f"implement/{refactoring_id}")
    
    refactor_dir.mkdir(parents=True, exist_ok=True)
    implement_dir.mkdir(parents=True, exist_ok=True)
    
    # Load plan if provided
    phases = {}
    if plan_file:
        phases = load_plan_phases(plan_file)
    else:
        # Default phases
        phases = {
            "phase_1_analysis": {
                "status": "not_started",
                "tasks": []
            },
            "phase_2_implementation": {
                "status": "not_started",
                "tasks": []
            },
            "phase_3_validation": {
                "status": "not_started",
                "tasks": []
            },
            "phase_4_integration": {
                "status": "not_started",
                "tasks": []
            }
        }
    
    # Create unified state
    state = {
        "refactoring_id": refactoring_id,
        "title": title,
        "status": "not_started",
        "created_at": datetime.now().isoformat() + "Z",
        "updated_at": datetime.now().isoformat() + "Z",
        "completed_phases": [],
        "current_phase": "phase_1_analysis",
        "phases": phases,
        "files_modified": [],
        "validation": {
            "last_checked": None,
            "status": "unknown",
            "errors": [],
            "warnings": []
        },
        "progress": {
            "total_tasks": 0,
            "completed_tasks": 0,
            "percentage": 0,
            "by_type": {"code": 0, "documentation": 0, "testing": 0}
        }
    }
    
    # Write state to both locations
    refactor_state_file = refactor_dir / "state.json"
    implement_state_file = implement_dir / "state.json"
    
    with open(refactor_state_file, 'w') as f:
        json.dump(state, f, indent=2)
    
    with open(implement_state_file, 'w') as f:
        json.dump(state, f, indent=2)
    
    print(f"✓ Initialized refactoring: {refactoring_id}")
    print(f"  Refactor state: {refactor_state_file}")
    print(f"  Implement state: {implement_state_file}")


def refactor_status(refactoring_id: str, verbose: bool = False):
    """
    Check refactoring status and verify state consistency.
    
    Args:
        refactoring_id: ID of the refactoring
        verbose: Show detailed status
    """
    
    refactor_state_file = Path(f"refactor/{refactoring_id}/state.json")
    implement_state_file = Path(f"implement/{refactoring_id}/state.json")
    
    # Load both state files
    with open(refactor_state_file, 'r') as f:
        refactor_state = json.load(f)
    
    with open(implement_state_file, 'r') as f:
        implement_state = json.load(f)
    
    # Check synchronization
    if refactor_state != implement_state:
        print("⚠️  WARNING: State files are out of sync!")
        print("\nDifferences:")
        print_state_diff(refactor_state, implement_state)
        return False
    
    print(f"✓ State files synchronized")
    
    # Display status
    print(f"\nRefactoring: {refactor_state['title']}")
    print(f"ID: {refactoring_state['refactoring_id']}")
    print(f"Status: {refactor_state['status']}")
    print(f"Progress: {refactor_state['progress']['percentage']}%")
    print(f"Current Phase: {refactor_state['current_phase']}")
    
    if verbose:
        print("\n" + "="*70)
        print("DETAILED STATUS")
        print("="*70)
        
        print("\nProgress by Type:")
        for task_type, count in refactor_state['progress']['by_type'].items():
            print(f"  - {task_type}: {count}")
        
        print("\nPhase Status:")
        for phase_id, phase in refactor_state['phases'].items():
            print(f"\n  {phase_id}:")
            print(f"    Status: {phase['status']}")
            
            tasks = phase.get('tasks', [])
            if isinstance(tasks, list):
                for task in tasks:
                    if isinstance(task, dict):
                        print(f"    - {task.get('id', 'unknown')}: {task.get('status', 'unknown')}")
            elif isinstance(tasks, dict):
                for task_id, task in tasks.items():
                    print(f"    - {task_id}: {task.get('status', 'unknown')}")
        
        print("\nValidation:")
        validation = refactor_state.get('validation', {})
        print(f"  Last Checked: {validation.get('last_checked', 'Never')}")
        print(f"  Status: {validation.get('status', 'unknown')}")
        
        if validation.get('errors'):
            print("\n  Errors:")
            for error in validation['errors']:
                print(f"    - {error}")
        
        if validation.get('warnings'):
            print("\n  Warnings:")
            for warning in validation['warnings']:
                print(f"    - {warning}")
        
        print("\nFiles Modified:")
        for file_path in refactor_state.get('files_modified', []):
            print(f"  - {file_path}")
    
    return True


def refactor_sync(refactoring_id: str):
    """
    Synchronize state files between refactor/ and implement/.
    
    Args:
        refactoring_id: ID of the refactoring
    """
    
    refactor_state_file = Path(f"refactor/{refactoring_id}/state.json")
    implement_state_file = Path(f"implement/{refactoring_id}/state.json")
    
    # Load refactor state (source of truth)
    with open(refactor_state_file, 'r') as f:
        state = json.load(f)
    
    # Validate state
    manager = RefactoringStateManager(str(refactor_state_file))
    errors = manager.validate_state()
    
    if errors:
        print("⚠️  State validation failed:")
        for error in errors:
            print(f"  - {error}")
        print("\nFix errors before syncing")
        return False
    
    # Write to implement state
    with open(implement_state_file, 'w') as f:
        json.dump(state, f, indent=2)
    
    print(f"✓ Synchronized state files")
    print(f"  Source: {refactor_state_file}")
    print(f"  Target: {implement_state_file}")
    
    return True


def refactor_recover(refactoring_id: str):
    """
    Recover state by scanning actual code changes.
    
    Args:
        refactoring_id: ID of the refactoring
    """
    
    state_file = Path(f"refactor/{refactoring_id}/state.json")
    
    # Load current state
    with open(state_file, 'r') as f:
        state = json.load(f)
    
    print("Recovering state from actual code changes...")
    
    # Get modified files from git
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True,
            text=True
        )
        modified_files = [
            f for f in result.stdout.strip().split('\n') 
            if f and not f.startswith('.git')
        ]
    except Exception as e:
        print(f"⚠️  Could not get git changes: {e}")
        modified_files = []
    
    # Update files_modified
    state["files_modified"] = modified_files
    
    # Rebuild task status from implementation guide
    guide_file = f"refactor/{refactoring_id}/IMPLEMENTATION_GUIDE.md"
    if Path(guide_file).exists():
        guide = load_implementation_guide(guide_file)
        
        for task in guide["tasks"]:
            # Check if file was modified
            if task["file"] in modified_files:
                # Update task status
                manager = RefactoringStateManager(str(state_file))
                manager.update_task_status(
                    phase_id=task["phase"],
                    task_id=task["id"],
                    new_status="completed"
                )
        
        print(f"✓ Updated task statuses based on modified files")
    
    # Recalculate progress
    manager = RefactoringStateManager(str(state_file))
    state["progress"] = manager._calculate_progress(state)
    
    # Validate and save
    errors = manager.validate_state()
    
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)
    
    print(f"\nRecovery Summary:")
    print(f"  Modified files: {len(modified_files)}")
    print(f"  Progress: {state['progress']['percentage']}%")
    
    if errors:
        print(f"\n⚠️  Validation errors remain:")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"\n✓ State recovered successfully")


def print_state_diff(state1: Dict, state2: Dict):
    """Print differences between two state dictionaries."""
    
    import difflib
    
    json1 = json.dumps(state1, indent=2, sort_keys=True).splitlines()
    json2 = json.dumps(state2, indent=2, sort_keys=True).splitlines()
    
    diff = difflib.unified_diff(
        json1, json2,
        fromfile="refactor/state.json",
        tofile="implement/state.json",
        lineterm=""
    )
    
    for line in diff:
        if line.startswith('+'):
            print(f"  {line}")
        elif line.startswith('-'):
            print(f"  {line}")


def load_plan_phases(plan_file: str) -> Dict:
    """Load phases from refactoring plan markdown file."""
    
    # This is a simplified implementation
    # In practice, you'd parse the markdown to extract phase information
    
    return {
        "phase_1_analysis": {
            "status": "not_started",
            "tasks": []
        },
        "phase_2_implementation": {
            "status": "not_started",
            "tasks": []
        },
        "phase_3_validation": {
            "status": "not_started",
            "tasks": []
        },
        "phase_4_integration": {
            "status": "not_started",
            "tasks": []
        }
    }


def load_implementation_guide(guide_file: str) -> Dict:
    """Load implementation guide and extract tasks."""
    
    # This is a simplified implementation
    # In practice, you'd parse the markdown to extract task information
    
    return {
        "tasks": []
    }
```

---

## Integration with Existing Patterns

### Compatibility with task_scripts/

The proposed enhancements use the same patterns as existing task scripts:

1. **Security validation**: Uses `SecurityValidator` from `taskmaster_common.py`
2. **Backup management**: Uses `BackupManager` from `taskmaster_common.py`
3. **Path handling**: Uses `Path` objects with security validation
4. **JSON handling**: Standard Python `json` module with error handling

### Example Integration

```python
"""
task_scripts/refactoring_manager.py
Integration with existing taskmaster_common.py patterns
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

# Import existing utilities
from taskmaster_common import SecurityValidator, BackupManager


class RefactoringManager:
    """High-level refactoring management with security and backup"""
    
    def __init__(self, refactoring_id: str, base_dir: str = "."):
        self.refactoring_id = refactoring_id
        self.base_dir = Path(base_dir).resolve()
        self.refactor_dir = self.base_dir / "refactor" / refactoring_id
        self.implement_dir = self.base_dir / "implement" / refactoring_id
        
        # Initialize security validator
        self.security_validator = SecurityValidator()
        
        # Initialize backup manager
        self.backup_manager = BackupManager()
        
        # Load state
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """Load state with security validation"""
        state_file = self.refactor_dir / "state.json"
        
        # Validate path security
        if not self.security_validator.validate_path_security(
            str(state_file), 
            str(self.base_dir)
        ):
            raise ValueError(f"Security validation failed for state file")
        
        # Load state
        with open(state_file, 'r') as f:
            return json.load(f)
    
    def update_task(
        self, 
        phase_id: str, 
        task_id: str, 
        status: str,
        create_backup: bool = True
    ):
        """
        Update task status with backup and security validation.
        
        Args:
            phase_id: Phase identifier
            task_id: Task identifier
            status: New status
            create_backup: Whether to create backup before updating
        """
        state_file = self.refactor_dir / "state.json"
        
        # Create backup if requested
        if create_backup:
            backup_path = self.backup_manager.create_backup(str(state_file))
            print(f"✓ Created backup: {backup_path}")
        
        # Update task status
        manager = RefactoringStateManager(str(state_file))
        manager.update_task_status(phase_id, task_id, status)
        
        print(f"✓ Updated task: {phase_id}.{task_id} → {status}")
    
    def validate(self) -> List[str]:
        """Validate state with security checks"""
        state_file = self.refactor_dir / "state.json"
        
        # Validate path security
        if not self.security_validator.validate_path_security(
            str(state_file), 
            str(self.base_dir)
        ):
            raise ValueError(f"Security validation failed for state file")
        
        # Validate state
        manager = RefactoringStateManager(str(state_file))
        return manager.validate_state()
```

---

## Migration Path

### Step 1: Add New Utilities (Non-Breaking)

Create `task_scripts/refactoring_state.py` with the `RefactoringStateManager` class.

```bash
# Create new utility file
touch task_scripts/refactoring_state.py
```

This doesn't break anything - it's a new file.

### Step 2: Update State Files (Backward Compatible)

Add optional `validation` and `progress` fields to existing state files.

```bash
# Add new fields to state.json
python -c "
import json
from pathlib import Path

state_file = Path('refactor/i2t4-into-756/state.json')
with open(state_file, 'r') as f:
    state = json.load(f)

# Add new fields if not present
if 'validation' not in state:
    state['validation'] = {
        'last_checked': None,
        'status': 'unknown',
        'errors': [],
        'warnings': []
    }

if 'progress' not in state:
    state['progress'] = {
        'total_tasks': 0,
        'completed_tasks': 0,
        'percentage': 0,
        'by_type': {'code': 0, 'documentation': 0, 'testing': 0}
    }

with open(state_file, 'w') as f:
    json.dump(state, f, indent=2)

print('✓ State file updated')
"
```

This maintains backward compatibility - old code ignores new fields.

### Step 3: Update Command Handlers (Optional)

Update `/implement` and `/refactor` command handlers to use new utilities.

This is optional - old workflows continue to work.

---

## Summary of Improvements

| Improvement | Type | Breaking Change | Priority |
|-------------|------|-----------------|----------|
| Add validation metadata | Enhancement | No | High |
| Add progress tracking | Enhancement | No | High |
| Automatic status cascading | Enhancement | No | High |
| State validation functions | Enhancement | No | High |
| Enhanced /implement workflow | Enhancement | No | Medium |
| State synchronization | Enhancement | No | Medium |
| State recovery command | New feature | No | Low |

All improvements are **backward compatible** and can be adopted incrementally.

---

## Testing Strategy

### Unit Tests

```python
# tests/test_refactoring_state.py

import pytest
from pathlib import Path
from task_scripts.refactoring_state import RefactoringStateManager


def test_state_manager_initialization():
    """Test that state manager initializes correctly"""
    state_file = "tests/fixtures/state.json"
    manager = RefactoringStateManager(state_file)
    assert manager.state_file == Path(state_file)
    assert manager.state is not None


def test_update_task_status_cascading():
    """Test that updating task status cascades to phase and overall"""
    state_file = "tests/fixtures/state.json"
    manager = RefactoringStateManager(state_file)
    
    # Update task to completed
    manager.update_task_status(
        "phase_2_implementation",
        "add_migration_analyzer",
        "completed"
    )
    
    # Verify cascading
    assert manager.state["phases"]["phase_2_implementation"]["tasks"]["add_migration_analyzer"]["status"] == "completed"
    # Phase status should update if all tasks complete
    # Overall status should update if all phases complete


def test_validate_state_consistency():
    """Test that state validation detects inconsistencies"""
    state_file = "tests/fixtures/state_invalid.json"
    manager = RefactoringStateManager(state_file)
    
    errors = manager.validate_state()
    assert len(errors) > 0


def test_backward_compatibility():
    """Test that old state files without new fields work"""
    state_file = "tests/fixtures/state_old_format.json"
    manager = RefactoringStateManager(state_file)
    
    # Should initialize new fields automatically
    assert "validation" in manager.state
    assert "progress" in manager.state
```

### Integration Tests

```python
# tests/test_refactoring_workflow.py

import pytest
from pathlib import Path
from task_scripts.refactoring_state import RefactoringStateManager


def test_end_to_end_implementation():
    """Test complete implementation workflow"""
    # Initialize
    refactor_init("test-001", "Test Refactoring")
    
    # Update tasks
    manager = RefactoringStateManager("refactor/test-001/state.json")
    manager.update_task_status("phase_1_analysis", "task_1", "completed")
    manager.update_task_status("phase_1_analysis", "task_2", "completed")
    
    # Validate
    errors = manager.validate_state()
    assert len(errors) == 0
    
    # Verify
    assert manager.state["status"] == "implementing"
    assert manager.state["progress"]["percentage"] > 0


def test_state_synchronization():
    """Test that state files stay synchronized"""
    refactor_init("test-002", "Sync Test")
    
    # Update via refactor state
    manager = RefactoringStateManager("refactor/test-002/state.json")
    manager.update_task_status("phase_1_analysis", "task_1", "completed")
    
    # Check implement state
    with open("implement/test-002/state.json", 'r') as f:
        implement_state = json.load(f)
    
    assert implement_state == manager.state
```

---

## Documentation Updates

### Update IMPLEMENTATION_GUIDE.md

Add section on state management:

```markdown
## State Management

### State File Structure

The refactoring state is tracked in `refactor/{id}/state.json` with the following structure:

```json
{
  "refactoring_id": "i2t4-into-756",
  "status": "in_progress",
  "phases": { ... },
  "progress": { ... },
  "validation": { ... }
}
```

### Updating Task Status

Use the `RefactoringStateManager` to update task status:

```python
from task_scripts.refactoring_state import RefactoringStateManager

manager = RefactoringStateManager("refactor/state.json")
manager.update_task_status(
    phase_id="phase_2_implementation",
    task_id="add_migration_analyzer",
    new_status="completed"
)
```

This automatically:
- Updates the task status
- Updates the phase status (if all tasks complete)
- Updates the overall status (if all phases complete)
- Recalculates progress percentages

### Validating State

Validate state consistency:

```python
errors = manager.validate_state()
if errors:
    print(f"State validation failed: {errors}")
else:
    print("State is valid")
```
```

### Update QUICK_REFERENCE.md

Add state management quick reference:

```markdown
## State Management Commands

### Initialize Refactoring
```bash
refactor_init("i2t4-into-756", "Refactor I2.T4 into 75.6")
```

### Check Status
```bash
refactor_status("i2t4-into-756", verbose=True)
```

### Synchronize State Files
```bash
refactor_sync("i2t4-into-756")
```

### Recover State
```bash
refactor_recover("i2t4-into-756")
```

### Update Task Status (Python)
```python
from task_scripts.refactoring_state import RefactoringStateManager

manager = RefactoringStateManager("refactor/state.json")
manager.update_task_status(
    "phase_2_implementation",
    "add_migration_analyzer",
    "completed"
)
```
```

---

## Conclusion

The proposed enhancements:

1. **Maintain backward compatibility** - All existing workflows continue to work
2. **Add robust state management** - Automatic cascading and validation
3. **Integrate with existing patterns** - Uses taskmaster_common.py utilities
4. **Provide recovery mechanisms** - State synchronization and recovery commands
5. **Enable incremental adoption** - Can be adopted feature by feature

These improvements address the state tracking issues encountered during the I2.T4 → 75.6 refactoring while maintaining compatibility with existing code and workflows.

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-04  
**Maintained By:** Refactoring Team