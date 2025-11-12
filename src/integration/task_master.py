"""
Task Master Integration for EmailIntelligence PR Resolution

This module provides integration with Task Master for enhanced task management
and parallel development support in the PR resolution workflow.

Key Features:
- Task creation and tracking for resolution phases
- Parallel worktree development support
- Task dependency mapping and validation
- Constitutional compliance integration
- Progress tracking and reporting
"""

import asyncio
import json
import os
import subprocess
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import structlog

from ..resolution.constitutional_engine import ConstitutionalEngine

logger = structlog.get_logger()


class TaskStatus(Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    DONE = "done"
    DEFERRED = "deferred"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class TaskPriority(Enum):
    """Task priority enumeration"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ResolutionTask:
    """Task definition for PR resolution"""
    id: str
    title: str
    description: str
    phase: str  # Phase 0, 1, 2, 3, 4
    status: TaskStatus
    priority: TaskPriority
    dependencies: List[str]
    parallel_group: Optional[str]
    worktree_path: Optional[str]
    constitutional_score: float
    created_at: datetime
    updated_at: datetime
    completion_criteria: List[str]
    validation_steps: List[str]
    rollback_procedure: str
    estimated_duration: int  # seconds
    actual_duration: Optional[int] = None
    error_details: Optional[str] = None
    notes: List[str] = None


@dataclass
class WorktreeEnvironment:
    """Worktree environment for isolated development"""
    task_id: str
    worktree_path: str
    branch_name: str
    isolated: bool = True
    created_at: datetime = None
    cleanup_on_complete: bool = True
    status: str = "active"
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()


class TaskMasterIntegration:
    """
    Task Master integration for EmailIntelligence
    
    Provides:
    - Task creation and management
    - Parallel worktree coordination
    - Dependency tracking and validation
    - Constitutional compliance integration
    - Progress reporting and analytics
    """
    
    def __init__(self, project_root: str = None):
        """
        Initialize Task Master integration
        
        Args:
            project_root: Path to project root directory
        """
        self.project_root = project_root or os.getcwd()
        self.tasks: Dict[str, ResolutionTask] = {}
        self.worktree_environments: Dict[str, WorktreeEnvironment] = {}
        self.parallel_groups: Dict[str, List[str]] = {}
        self.constitutional_engine = ConstitutionalEngine()
        self.task_counter = 0
        
        # Initialize parallel execution groups
        self._init_parallel_groups()
        
        logger.info("Task Master integration initialized", project_root=self.project_root)
    
    async def initialize(self) -> bool:
        """Initialize the Task Master integration"""
        try:
            await self.constitutional_engine.initialize()
            await self._load_existing_tasks()
            logger.info("Task Master integration initialized successfully")
            return True
        except Exception as e:
            logger.error("Failed to initialize Task Master integration", error=str(e))
            return False
    
    def _init_parallel_groups(self):
        """Initialize parallel execution groups based on specification"""
        self.parallel_groups = {
            "foundation": ["P1.1", "P1.2"],  # Phase 0
            "core_development": ["P1.3", "P1.4"],  # Phase 1
            "strategy_validation": ["P1.5", "P1.6"],  # Phase 2
            "testing_quality": ["P1.7", "P1.8"],  # Phase 3
            "integration_optimization": ["P1.9", "P1.10"]  # Phase 4
        }
    
    async def create_resolution_task(
        self,
        title: str,
        description: str,
        phase: str,
        priority: TaskPriority = TaskPriority.HIGH,
        dependencies: List[str] = None,
        parallel_group: str = None,
        completion_criteria: List[str] = None,
        validation_steps: List[str] = None,
        rollback_procedure: str = "Manual rollback",
        estimated_duration: int = 3600
    ) -> str:
        """
        Create a new resolution task
        
        Args:
            title: Task title
            description: Task description
            phase: Implementation phase (Phase 0-4)
            priority: Task priority
            dependencies: Task dependencies
            parallel_group: Parallel execution group
            completion_criteria: Completion criteria
            validation_steps: Validation steps
            rollback_procedure: Rollback procedure
            estimated_duration: Estimated duration in seconds
            
        Returns:
            Task ID
        """
        self.task_counter += 1
        task_id = f"T{self.task_counter}"
        
        # Default completion criteria based on phase
        if completion_criteria is None:
            completion_criteria = self._get_default_completion_criteria(phase)
        
        # Default validation steps based on phase
        if validation_steps is None:
            validation_steps = self._get_default_validation_steps(phase)
        
        # Create task
        task = ResolutionTask(
            id=task_id,
            title=title,
            description=description,
            phase=phase,
            status=TaskStatus.PENDING,
            priority=priority,
            dependencies=dependencies or [],
            parallel_group=parallel_group,
            worktree_path=None,
            constitutional_score=0.0,  # Will be calculated during validation
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            completion_criteria=completion_criteria,
            validation_steps=validation_steps,
            rollback_procedure=rollback_procedure,
            estimated_duration=estimated_duration,
            notes=[]
        )
        
        self.tasks[task_id] = task
        
        # Add to parallel group if specified
        if parallel_group and parallel_group in self.parallel_groups:
            self.parallel_groups[parallel_group].append(task_id)
        
        logger.info(
            "Resolution task created",
            task_id=task_id,
            title=title,
            phase=phase,
            parallel_group=parallel_group
        )
        
        return task_id
    
    async def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        notes: str = None,
        constitutional_validation: bool = True
    ) -> bool:
        """
        Update task status
        
        Args:
            task_id: Task ID
            new status
            notes: Additional notes
            constitutional_validation: Whether to run constitutional validation
            
        Returns:
            Success status
        """
        if task_id not in self.tasks:
            logger.error("Task not found", task_id=task_id)
            return False
        
        task = self.tasks[task_id]
        old_status = task.status
        task.status = status
        task.updated_at = datetime.utcnow()
        
        if notes:
            task.notes.append(f"[{datetime.utcnow().isoformat()}] {notes}")
        
        # Run constitutional validation for critical status changes
        if constitutional_validation and status in [TaskStatus.DONE, TaskStatus.BLOCKED]:
            await self._validate_task_constitutional_compliance(task)
        
        # Handle task completion
        if status == TaskStatus.DONE:
            task.actual_duration = (datetime.utcnow() - task.created_at).total_seconds()
            await self._check_and_unblock_dependent_tasks(task_id)
        
        logger.info(
            "Task status updated",
            task_id=task_id,
            old_status=old_status.value,
            new_status=status.value
        )
        
        return True
    
    async def create_worktree_environment(
        self,
        task_id: str,
        branch_name: str = None,
        isolated: bool = True,
        cleanup_on_complete: bool = True
    ) -> Optional[str]:
        """
        Create isolated worktree environment for a task
        
        Args:
            task_id: Task ID
            branch_name: Branch name for worktree
            isolated: Whether environment is isolated
            cleanup_on_complete: Whether to cleanup on completion
            
        Returns:
            Worktree path or None if failed
        """
        if task_id not in self.tasks:
            logger.error("Task not found", task_id=task_id)
            return None
        
        if not branch_name:
            branch_name = f"task-{task_id}-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
        
        try:
            # Create worktree directory
            worktree_base = os.path.join(self.project_root, "worktrees")
            os.makedirs(worktree_base, exist_ok=True)
            worktree_path = os.path.join(worktree_base, branch_name)
            
            # Create worktree using git
            result = subprocess.run([
                "git", "worktree", "add", worktree_path, branch_name
            ], cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(
                    "Failed to create worktree",
                    task_id=task_id,
                    error=result.stderr
                )
                return None
            
            # Create environment configuration
            env = WorktreeEnvironment(
                task_id=task_id,
                worktree_path=worktree_path,
                branch_name=branch_name,
                isolated=isolated,
                cleanup_on_complete=cleanup_on_complete
            )
            
            self.worktree_environments[task_id] = env
            
            # Update task with worktree path
            task = self.tasks[task_id]
            task.worktree_path = worktree_path
            
            logger.info(
                "Worktree environment created",
                task_id=task_id,
                worktree_path=worktree_path,
                branch_name=branch_name
            )
            
            return worktree_path
            
        except Exception as e:
            logger.error(
                "Failed to create worktree environment",
                task_id=task_id, error=str(e)
            )
            return None
    
    async def get_task_dependencies(self, task_id: str, include_blocked: bool = True) -> Dict[str, Any]:
        """
        Get task dependencies and their status
        
        Args:
            task_id: Task ID
            include_blocked: Whether to include blocked dependency information
            
        Returns:
            Dependency information
        """
        if task_id not in self.tasks:
            return {"error": "Task not found"}
        
        task = self.tasks[task_id]
        dependencies_info = {
            "task_id": task_id,
            "dependencies": [],
            "dependents": [],
            "blocked_status": None,
            "unlock_conditions": []
        }
        
        # Get dependency information
        for dep_id in task.dependencies:
            if dep_id in self.tasks:
                dep_task = self.tasks[dep_id]
                dependencies_info["dependencies"].append({
                    "task_id": dep_id,
                    "title": dep_task.title,
                    "status": dep_task.status.value,
                    "completion_criteria": dep_task.completion_criteria,
                    "constitutional_score": dep_task.constitutional_score
                })
        
        # Get dependent tasks
        for other_id, other_task in self.tasks.items():
            if task_id in other_task.dependencies:
                dependencies_info["dependents"].append({
                    "task_id": other_id,
                    "title": other_task.title,
                    "status": other_task.status.value,
                    "priority": other_task.priority.value
                })
        
        # Check if task is blocked
        if include_blocked:
            blocked_reasons = []
            for dep_id in task.dependencies:
                if dep_id in self.tasks:
                    dep_task = self.tasks[dep_id]
                    if dep_task.status != TaskStatus.DONE:
                        blocked_reasons.append(f"Dependency {dep_id} ({dep_task.title}) is not completed")
            
            dependencies_info["blocked_status"] = len(blocked_reasons) > 0
            dependencies_info["block_reasons"] = blocked_reasons
        
        return dependencies_info
    
    async def validate_constitutional_compliance(
        self,
        task_id: str,
        validation_type: str,
        content: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Validate constitutional compliance for task execution
        
        Args:
            task_id: Task ID
            validation_type: Type of validation (specification, strategy, execution)
            content: Content to validate
            context: Additional context
            
        Returns:
            Constitutional validation result
        """
        if task_id not in self.tasks:
            return {"error": "Task not found"}
        
        try:
            if context is None:
                context = {}
            
            context["task_id"] = task_id
            context["validation_timestamp"] = datetime.utcnow().isoformat()
            
            if validation_type == "specification":
                compliance_result = await self.constitutional_engine.validate_specification_template(
                    content, "resolution_task", context
                )
            elif validation_type == "strategy":
                compliance_result = await self.constitutional_engine.validate_execution_phase(
                    "task_execution", json.loads(content), context
                )
            elif validation_type == "execution":
                compliance_result = await self.constitutional_engine.validate_execution_phase(
                    "task_execution", json.loads(content), context
                )
            else:
                return {"error": f"Unknown validation type: {validation_type}"}
            
            # Update task with constitutional score
            task = self.tasks[task_id]
            task.constitutional_score = compliance_result.overall_score
            
            return {
                "task_id": task_id,
                "validation_type": validation_type,
                "compliance_result": asdict(compliance_result),
                "constitutional_score": compliance_result.overall_score,
                "validation_timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(
                "Constitutional validation failed",
                task_id=task_id,
                validation_type=validation_type,
                error=str(e)
            )
            return {"error": str(e)}
    
    async def get_parallel_execution_plan(self, phase: str) -> Dict[str, Any]:
        """
        Get parallel execution plan for a phase
        
        Args:
            phase: Implementation phase
            
        Returns:
            Parallel execution plan
        """
        # Map phase to parallel groups
        phase_groups = {
            "Phase 0": ["foundation"],
            "Phase 1": ["core_development"],
            "Phase 2": ["strategy_validation"],
            "Phase 3": ["testing_quality"],
            "Phase 4": ["integration_optimization"]
        }
        
        relevant_groups = phase_groups.get(phase, [])
        execution_plan = {
            "phase": phase,
            "parallel_groups": {},
            "sequential_dependencies": [],
            "resource_requirements": {},
            "coordination_points": []
        }
        
        for group_name in relevant_groups:
            if group_name in self.parallel_groups:
                group_tasks = []
                for task_id in self.parallel_groups[group_name]:
                    if task_id in self.tasks:
                        task = self.tasks[task_id]
                        group_tasks.append({
                            "task_id": task_id,
                            "title": task.title,
                            "status": task.status.value,
                            "dependencies": task.dependencies,
                            "worktree_path": task.worktree_path,
                            "constitutional_score": task.constitutional_score
                        })
                
                execution_plan["parallel_groups"][group_name] = {
                    "tasks": group_tasks,
                    "can_execute_concurrently": True,
                    "coordination_required": True
                }
        
        return execution_plan
    
    async def cleanup_worktree_environments(self, task_ids: List[str] = None) -> bool:
        """
        Cleanup worktree environments
        
        Args:
            task_ids: Specific task IDs to cleanup (None for all)
            
        Returns:
            Success status
        """
        try:
            tasks_to_cleanup = task_ids or list(self.worktree_environments.keys())
            success_count = 0
            
            for task_id in tasks_to_cleanup:
                if task_id in self.worktree_environments:
                    env = self.worktree_environments[task_id]
                    
                    if not env.cleanup_on_complete:
                        continue
                    
                    # Remove worktree
                    result = subprocess.run([
                        "git", "worktree", "remove", env.worktree_path
                    ], cwd=self.project_root, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        del self.worktree_environments[task_id]
                        
                        # Update task
                        if task_id in self.tasks:
                            self.tasks[task_id].worktree_path = None
                        
                        success_count += 1
                        logger.info("Worktree environment cleaned up", task_id=task_id)
                    else:
                        logger.error(
                            "Failed to cleanup worktree",
                            task_id=task_id, error=result.stderr
                        )
            
            return success_count == len(tasks_to_cleanup)
            
        except Exception as e:
            logger.error("Worktree cleanup failed", error=str(e))
            return False
    
    def _get_default_completion_criteria(self, phase: str) -> List[str]:
        """Get default completion criteria for a phase"""
        criteria_map = {
            "Phase 0": [
                "Constitutional engine initialized",
                "Task Master MCP integration configured",
                "Foundation frameworks established"
            ],
            "Phase 1": [
                "Specification templates created",
                "Interactive creation system implemented",
                "Template validation working"
            ],
            "Phase 2": [
                "Multi-phase strategy generator implemented",
                "Constitutional validation engine integrated",
                "Strategy analysis and comparison working"
            ],
            "Phase 3": [
                "Test-first implementation completed",
                "Quality assurance framework implemented",
                "Test coverage > 90%"
            ],
            "Phase 4": [
                "CLI integration completed",
                "Performance optimization implemented",
                "Final validation passed"
            ]
        }
        return criteria_map.get(phase, ["Task completed successfully"])
    
    def _get_default_validation_steps(self, phase: str) -> List[str]:
        """Get default validation steps for a phase"""
        steps_map = {
            "Phase 0": [
                "Constitutional framework validation",
                "Task Master connectivity test",
                "Basic functionality verification"
            ],
            "Phase 1": [
                "Template generation validation",
                "Constitutional compliance check",
                "Integration testing"
            ],
            "Phase 2": [
                "Strategy generation testing",
                "Constitutional validation testing",
                "Multi-strategy comparison validation"
            ],
            "Phase 3": [
                "Unit test execution",
                "Integration test execution",
                "Performance benchmark validation"
            ],
            "Phase 4": [
                "End-to-end testing",
                "Performance validation",
                "Final constitutional compliance check"
            ]
        }
        return steps_map.get(phase, ["Functional validation"])
    
    async def _validate_task_constitutional_compliance(self, task: ResolutionTask):
        """Validate task against constitutional rules"""
        try:
            # Create task context for validation
            task_context = {
                "task_id": task.id,
                "task_phase": task.phase,
                "task_priority": task.priority.value,
                "validation_timestamp": datetime.utcnow().isoformat()
            }
            
            # Convert task to JSON for validation
            task_json = json.dumps(asdict(task), indent=2, default=str)
            
            # Validate task structure
            compliance_result = await self.constitutional_engine.validate_execution_phase(
                f"task_{task.phase}", json.loads(task_json), task_context
            )
            
            task.constitutional_score = compliance_result.overall_score
            
            logger.info(
                "Task constitutional compliance validated",
                task_id=task.id,
                constitutional_score=compliance_result.overall_score,
                violation_count=len(compliance_result.violations)
            )
            
        except Exception as e:
            logger.error(
                "Constitutional compliance validation failed",
                task_id=task.id, error=str(e)
            )

    async def _check_and_unblock_dependent_tasks(self, completed_task_id: str):
        """Check and unblock tasks dependent on the completed task"""
        for task_id, task in self.tasks.items():
            if completed_task_id in task.dependencies and task.status == TaskStatus.BLOCKED:
                # Check if all dependencies are now satisfied
                all_deps_satisfied = True
                for dep_id in task.dependencies:
                    if dep_id in self.tasks:
                        dep_task = self.tasks[dep_id]
                        if dep_task.status != TaskStatus.DONE:
                            all_deps_satisfied = False
                            break
                
                if all_deps_satisfied:
                    task.status = TaskStatus.PENDING  # Ready to start
                    task.updated_at = datetime.utcnow()
                    logger.info(
                        "Dependent task unblocked",
                        task_id=task_id,
                        dependency=completed_task_id
                    )

    async def _load_existing_tasks(self):
        """Load existing tasks from persistent storage"""
        # This would typically load from a database or file
        # For now, we'll just initialize with the spec-defined tasks
        pass

    def get_task_summary(self) -> Dict[str, Any]:
        """Get comprehensive task summary"""
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for t in self.tasks.values() if t.status == TaskStatus.DONE)
        in_progress_tasks = sum(1 for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS)
        blocked_tasks = sum(1 for t in self.tasks.values() if t.status == TaskStatus.BLOCKED)
        
        # Phase distribution
        phase_distribution = {}
        for task in self.tasks.values():
            phase = task.phase
            if phase not in phase_distribution:
                phase_distribution[phase] = {
                    "total": 0, "completed": 0, "in_progress": 0, "blocked": 0
                }
            
            phase_distribution[phase]["total"] += 1
            if task.status == TaskStatus.DONE:
                phase_distribution[phase]["completed"] += 1
            elif task.status == TaskStatus.IN_PROGRESS:
                phase_distribution[phase]["in_progress"] += 1
            elif task.status == TaskStatus.BLOCKED:
                phase_distribution[phase]["blocked"] += 1
        
        # Constitutional compliance summary
        compliance_scores = [
            t.constitutional_score for t in self.tasks.values()
            if t.constitutional_score > 0
        ]
        avg_constitutional_score = (
            sum(compliance_scores) / len(compliance_scores)
            if compliance_scores else 0.0
        )
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "blocked_tasks": blocked_tasks,
            "completion_rate": completed_tasks / total_tasks if total_tasks > 0 else 0.0,
            "phase_distribution": phase_distribution,
            "average_constitutional_score": avg_constitutional_score,
            "active_worktrees": len(self.worktree_environments),
            "parallel_groups": len(self.parallel_groups),
            "last_updated": datetime.utcnow().isoformat()
        }


async def main():
    """Main function for testing Task Master integration"""
    integration = TaskMasterIntegration()
    
    if not await integration.initialize():
        logger.error("Failed to initialize Task Master integration")
        return
    
    # Create a test task
    await integration.create_resolution_task(
        title="Test Constitutional Engine",
        description="Test constitutional engine functionality",
        phase="Phase 0",
        parallel_group="foundation"
    )
    
    # Get task summary
    summary = integration.get_task_summary()
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())