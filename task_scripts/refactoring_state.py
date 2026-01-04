"""
Refactoring State Management Utilities

This module provides utilities for managing refactoring state with automatic
status cascading, validation, and recovery capabilities.

Compatible with existing taskmaster_common.py patterns for security and backup.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Import existing utilities
from taskmaster_common import SecurityValidator, BackupManager


class RefactoringStateManager:
    """
    Manages refactoring state with automatic cascading and validation.
    
    This class provides:
    - Automatic task → phase → overall status cascading
    - Progress calculation and tracking
    - State consistency validation
    - Backward compatibility with existing state.json formats
    
    Usage:
        manager = RefactoringStateManager("refactor/state.json")
        manager.update_task_status("phase_2", "task_1", "completed")
        errors = manager.validate_state()
    """
    
    VALID_STATUSES = {
        "not_started", "planning", "implementing", 
        "documenting", "testing", "complete", "blocked"
    }
    
    VALID_PHASE_STATUSES = {
        "not_started", "in_progress", "completed", "blocked"
    }
    
    VALID_TASK_STATUSES = {
        "pending", "in_progress", "completed", "failed", "blocked"
    }
    
    def __init__(self, state_file: str, base_dir: str = None):
        """
        Initialize state manager.
        
        Args:
            state_file: Path to state.json file
            base_dir: Base directory for security validation (optional)
        """
        self.state_file = Path(state_file).resolve()
        self.base_dir = Path(base_dir).resolve() if base_dir else None
        
        # Initialize security validator
        self.security_validator = SecurityValidator()
        
        # Validate path security if base_dir provided
        if self.base_dir:
            if not self.security_validator.validate_path_security(
                str(self.state_file), 
                str(self.base_dir)
            ):
                raise ValueError(
                    f"Security validation failed for state file: {self.state_file}"
                )
        
        # Load state
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """
        Load state from file with validation and backward compatibility.
        
        Returns:
            State dictionary
        """
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
        
        # Ensure completed_phases exists
        if "completed_phases" not in state:
            state["completed_phases"] = []
        
        return state
    
    def save_state(self, create_backup: bool = False) -> Optional[str]:
        """
        Save state to file with optional backup.
        
        Args:
            create_backup: Whether to create backup before saving
            
        Returns:
            Backup file path if backup created, None otherwise
        """
        self.state["updated_at"] = datetime.now().isoformat() + "Z"
        
        # Create backup if requested
        backup_path = None
        if create_backup:
            backup_manager = BackupManager()
            backup_path = backup_manager.create_backup(str(self.state_file))
        
        # Save state
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
        
        return backup_path
    
    def update_task_status(
        self, 
        phase_id: str, 
        task_id: str, 
        new_status: str,
        create_backup: bool = False
    ) -> bool:
        """
        Update task status and automatically cascade status updates.
        
        This method:
        1. Validates the new status
        2. Updates the task status
        3. Updates the phase status (if all tasks complete)
        4. Updates the overall status (if all phases complete)
        5. Recalculates progress percentages
        6. Saves the state
        
        Args:
            phase_id: Phase identifier (e.g., "phase_2_implementation")
            task_id: Task identifier (e.g., "add_migration_analyzer")
            new_status: New status for the task
            create_backup: Whether to create backup before updating
            
        Returns:
            True if update successful, False otherwise
            
        Raises:
            ValueError: If status is invalid
            KeyError: If phase_id or task_id not found
        """
        # Validate status
        if new_status not in self.VALID_TASK_STATUSES:
            raise ValueError(
                f"Invalid task status: {new_status}. "
                f"Must be one of {self.VALID_TASK_STATUSES}"
            )
        
        # Get phase
        phases = self.state.get("phases", {})
        if phase_id not in phases:
            raise KeyError(f"Phase not found: {phase_id}")
        
        phase = phases[phase_id]
        tasks = phase.get("tasks", [])
        
        # Handle both list and dict task formats
        task_found = False
        
        if isinstance(tasks, list):
            # List format: list of task dicts
            for task in tasks:
                if isinstance(task, dict) and task.get("id") == task_id:
                    task["status"] = new_status
                    task_found = True
                    break
        elif isinstance(tasks, dict):
            # Dict format: task_id -> task_info
            if task_id in tasks:
                self.state["phases"][phase_id]["tasks"][task_id]["status"] = new_status
                task_found = True
        
        if not task_found:
            raise KeyError(f"Task not found: {phase_id}.{task_id}")
        
        # Cascade: Update phase status
        self._update_phase_status(phase_id)
        
        # Cascade: Update overall status
        self._update_overall_status()
        
        # Update progress
        self.state["progress"] = self._calculate_progress(self.state)
        
        # Save
        self.save_state(create_backup=create_backup)
        
        return True
    
    def _update_phase_status(self, phase_id: str):
        """
        Update phase status based on task statuses.
        
        Args:
            phase_id: Phase identifier
        """
        phase = self.state["phases"][phase_id]
        tasks = phase.get("tasks", [])
        
        # Handle both list and dict formats
        task_statuses = []
        
        if isinstance(tasks, list):
            for task in tasks:
                if isinstance(task, dict):
                    task_statuses.append(task.get("status", "pending"))
        elif isinstance(tasks, dict):
            for task in tasks.values():
                task_statuses.append(task.get("status", "pending"))
        
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
        completed_phases = self.state.setdefault("completed_phases", [])
        if phase_status == "completed" and phase_id not in completed_phases:
            completed_phases.append(phase_id)
    
    def _update_overall_status(self):
        """Update overall status based on phase statuses."""
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
        
        # Update current_phase
        for phase_id, phase in phases.items():
            if phase.get("status") in ["in_progress", "not_started"]:
                self.state["current_phase"] = phase_id
                break
    
    def _calculate_progress(self, state: Dict) -> Dict:
        """
        Calculate progress percentages.
        
        Args:
            state: State dictionary
            
        Returns:
            Progress dictionary with total_tasks, completed_tasks, percentage, by_type
        """
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
        
        Checks:
        - Overall status is valid
        - Phase statuses are valid
        - Task statuses are valid
        - Progress calculation matches actual counts
        - Phase status matches task statuses
        
        Returns:
            List of errors (empty if valid)
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
        
        return errors
    
    def get_status_summary(self) -> Dict:
        """
        Get a summary of the current status.
        
        Returns:
            Dictionary with status summary
        """
        return {
            "refactoring_id": self.state.get("refactoring_id"),
            "title": self.state.get("title"),
            "status": self.state.get("status"),
            "current_phase": self.state.get("current_phase"),
            "progress": self.state.get("progress", {}),
            "validation": self.state.get("validation", {}),
            "files_modified": self.state.get("files_modified", [])
        }
    
    def get_phase_status(self, phase_id: str) -> Optional[Dict]:
        """
        Get status of a specific phase.
        
        Args:
            phase_id: Phase identifier
            
        Returns:
            Phase status dictionary or None if not found
        """
        phase = self.state.get("phases", {}).get(phase_id)
        if phase:
            return {
                "phase_id": phase_id,
                "status": phase.get("status"),
                "tasks": phase.get("tasks", [])
            }
        return None
    
    def get_next_tasks(self, limit: int = 5) -> List[Dict]:
        """
        Get next pending tasks.
        
        Args:
            limit: Maximum number of tasks to return
            
        Returns:
            List of pending tasks
        """
        pending_tasks = []
        
        for phase_id, phase in self.state.get("phases", {}).items():
            if phase.get("status") not in ["completed", "blocked"]:
                tasks = phase.get("tasks", [])
                
                if isinstance(tasks, list):
                    for task in tasks:
                        if isinstance(task, dict) and task.get("status") == "pending":
                            pending_tasks.append({
                                "phase_id": phase_id,
                                "task_id": task.get("id"),
                                "task": task
                            })
                elif isinstance(tasks, dict):
                    for task_id, task in tasks.items():
                        if task.get("status") == "pending":
                            pending_tasks.append({
                                "phase_id": phase_id,
                                "task_id": task_id,
                                "task": task
                            })
        
        return pending_tasks[:limit]


def refactor_init(refactoring_id: str, title: str, base_dir: str = "."):
    """
    Initialize a new refactoring with unified state structure.
    
    Args:
        refactoring_id: Unique identifier for the refactoring
        title: Human-readable title
        base_dir: Base directory for refactoring (default: current directory)
        
    Returns:
        Tuple of (refactor_state_file, implement_state_file) paths
    """
    base_path = Path(base_dir).resolve()
    refactor_dir = base_path / "refactor" / refactoring_id
    implement_dir = base_path / "implement" / refactoring_id
    
    # Create directories
    refactor_dir.mkdir(parents=True, exist_ok=True)
    implement_dir.mkdir(parents=True, exist_ok=True)
    
    # Create unified state
    state = {
        "refactoring_id": refactoring_id,
        "title": title,
        "status": "not_started",
        "created_at": datetime.now().isoformat() + "Z",
        "updated_at": datetime.now().isoformat() + "Z",
        "completed_phases": [],
        "current_phase": "phase_1_analysis",
        "phases": {
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
        },
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
    
    return str(refactor_state_file), str(implement_state_file)


def refactor_status(refactoring_id: str, base_dir: str = ".", verbose: bool = False):
    """
    Check refactoring status and verify state consistency.
    
    Args:
        refactoring_id: ID of the refactoring
        base_dir: Base directory (default: current directory)
        verbose: Show detailed status
        
    Returns:
        True if state files are synchronized, False otherwise
    """
    base_path = Path(base_dir).resolve()
    refactor_state_file = base_path / "refactor" / refactoring_id / "state.json"
    implement_state_file = base_path / "implement" / refactoring_id / "state.json"
    
    # Load both state files
    with open(refactor_state_file, 'r') as f:
        refactor_state = json.load(f)
    
    with open(implement_state_file, 'r') as f:
        implement_state = json.load(f)
    
    # Check synchronization
    if refactor_state != implement_state:
        print("⚠️  WARNING: State files are out of sync!")
        print(f"  Refactor: {refactor_state_file}")
        print(f"  Implement: {implement_state_file}")
        return False
    
    print(f"✓ State files synchronized")
    
    # Display status
    print(f"\nRefactoring: {refactor_state['title']}")
    print(f"ID: {refactor_state['refactoring_id']}")
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


def refactor_sync(refactoring_id: str, base_dir: str = "."):
    """
    Synchronize state files between refactor/ and implement/.
    
    Args:
        refactoring_id: ID of the refactoring
        base_dir: Base directory (default: current directory)
        
    Returns:
        True if synchronization successful, False otherwise
    """
    base_path = Path(base_dir).resolve()
    refactor_state_file = base_path / "refactor" / refactoring_id / "state.json"
    implement_state_file = base_path / "implement" / refactoring_id / "state.json"
    
    # Load refactor state (source of truth)
    with open(refactor_state_file, 'r') as f:
        state = json.load(f)
    
    # Validate state
    try:
        manager = RefactoringStateManager(str(refactor_state_file))
        errors = manager.validate_state()
        
        if errors:
            print("⚠️  State validation failed:")
            for error in errors:
                print(f"  - {error}")
            print("\nFix errors before syncing")
            return False
    except Exception as e:
        print(f"⚠️  Could not validate state: {e}")
        return False
    
    # Write to implement state
    with open(implement_state_file, 'w') as f:
        json.dump(state, f, indent=2)
    
    print(f"✓ Synchronized state files")
    print(f"  Source: {refactor_state_file}")
    print(f"  Target: {implement_state_file}")
    
    return True


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python refactoring_state.py <command> [args]")
        print("Commands:")
        print("  init <id> <title>  - Initialize new refactoring")
        print("  status <id>        - Show refactoring status")
        print("  sync <id>          - Synchronize state files")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        if len(sys.argv) < 4:
            print("Usage: python refactoring_state.py init <id> <title>")
            sys.exit(1)
        
        refactor_id = sys.argv[2]
        title = sys.argv[3]
        
        refactor_file, implement_file = refactor_init(refactor_id, title)
        print(f"✓ Initialized refactoring: {refactor_id}")
        print(f"  Refactor state: {refactor_file}")
        print(f"  Implement state: {implement_file}")
    
    elif command == "status":
        if len(sys.argv) < 3:
            print("Usage: python refactoring_state.py status <id>")
            sys.exit(1)
        
        refactor_id = sys.argv[2]
        refactor_status(refactor_id, verbose=True)
    
    elif command == "sync":
        if len(sys.argv) < 3:
            print("Usage: python refactoring_state.py sync <id>")
            sys.exit(1)
        
        refactor_id = sys.argv[2]
        refactor_sync(refactor_id)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)