"""
Parallel Coordination Module for EmailIntelligence PR Resolution

This module provides coordination mechanisms for parallel development
in worktree-based environments with task dependency tracking.

Key Features:
- Parallel worktree coordination
- Task dependency mapping and validation
- Resource sharing and isolation
- Coordination barriers and synchronization
"""

import asyncio
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import structlog

from ..integration.task_master import TaskMasterIntegration, TaskStatus

logger = structlog.get_logger()


class CoordinationStatus(Enum):
    """Parallel coordination status"""
    PENDING = "pending"
    COORDINATING = "coordinating"
    EXECUTING = "executing"
    SYNCHRONIZING = "synchronizing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ResourceType(Enum):
    """Resource type for coordination"""
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    GIT_REPOSITORY = "git_repository"
    WORKTREE = "worktree"
    CONSTITUTIONAL_ENGINE = "constitutional_engine"


@dataclass
class CoordinationBarrier:
    """Synchronization barrier for parallel execution"""
    id: str
    name: str
    tasks: List[str]
    condition: str  # "all_complete", "any_complete", "majority_complete"
    threshold: float  # For majority_complete
    timeout: Optional[int]  # seconds
    created_at: datetime
    triggered_at: Optional[datetime] = None
    status: str = "active"


@dataclass
class ResourceAllocation:
    """Resource allocation for parallel tasks"""
    task_id: str
    resource_type: ResourceType
    allocated: bool
    capacity: float
    current_usage: float
    isolation_level: str  # "none", "shared", "isolated"
    worktree_path: Optional[str] = None


class ParallelCoordination:
    """
    Parallel coordination system for EmailIntelligence
    
    Provides:
    - Parallel worktree coordination
    - Task dependency validation and management
    - Resource allocation and isolation
    - Synchronization barriers and coordination points
    - Real-time coordination monitoring
    """
    
    def __init__(self, task_master: TaskMasterIntegration):
        """
        Initialize parallel coordination
        
        Args:
            task_master: Task Master integration instance
        """
        self.task_master = task_master
        self.coordination_barriers: Dict[str, CoordinationBarrier] = {}
        self.resource_allocations: Dict[str, ResourceAllocation] = {}
        self.active_coordinations: Dict[str, Dict[str, Any]] = {}
        self.coordination_lock = asyncio.Lock()
        
        logger.info("Parallel coordination system initialized")
    
    async def initialize_parallel_execution(
        self,
        parallel_group: str,
        tasks: List[str],
        coordination_strategy: str = "worktree_isolated"
    ) -> str:
        """
        Initialize parallel execution for a group of tasks
        
        Args:
            parallel_group: Name of parallel execution group
            tasks: List of task IDs to execute in parallel
            coordination_strategy: Coordination strategy to use
            
        Returns:
            Coordination session ID
        """
        session_id = f"coord_{parallel_group}_{int(datetime.utcnow().timestamp())}"
        
        async with self.coordination_lock:
            self.active_coordinations[session_id] = {
                "session_id": session_id,
                "parallel_group": parallel_group,
                "tasks": tasks,
                "strategy": coordination_strategy,
                "status": CoordinationStatus.PENDING,
                "created_at": datetime.utcnow(),
                "barriers": [],
                "resource_requirements": {},
                "execution_plan": {}
            }
        
        logger.info(
            "Parallel execution initialized",
            session_id=session_id,
            parallel_group=parallel_group,
            task_count=len(tasks)
        )
        
        return session_id
    
    async def create_coordination_barrier(
        self,
        session_id: str,
        name: str,
        tasks: List[str],
        condition: str = "all_complete",
        threshold: float = 1.0,
        timeout: int = 3600
    ) -> str:
        """
        Create a coordination barrier for task synchronization
        
        Args:
            session_id: Coordination session ID
            name: Barrier name
            tasks: Task IDs that must coordinate
            condition: Barrier condition
            threshold: Threshold for majority_complete
            timeout: Barrier timeout in seconds
            
        Returns:
            Barrier ID
        """
        barrier_id = f"barrier_{name}_{int(datetime.utcnow().timestamp())}"
        
        barrier = CoordinationBarrier(
            id=barrier_id,
            name=name,
            tasks=tasks,
            condition=condition,
            threshold=threshold,
            timeout=timeout,
            created_at=datetime.utcnow()
        )
        
        self.coordination_barriers[barrier_id] = barrier
        
        # Add barrier to session
        if session_id in self.active_coordinations:
            self.active_coordinations[session_id]["barriers"].append(barrier_id)
        
        logger.info(
            "Coordination barrier created",
            barrier_id=barrier_id,
            session_id=session_id,
            tasks=tasks,
            condition=condition
        )
        
        return barrier_id
    
    async def validate_task_dependencies(self, task_ids: List[str]) -> Dict[str, Any]:
        """
        Validate task dependencies for parallel execution
        
        Args:
            task_ids: List of task IDs to validate
            
        Returns:
            Dependency validation result
        """
        validation_result = {
            "valid": True,
            "circular_dependencies": [],
            "blocked_tasks": [],
            "dependency_graph": {},
            "parallel_execution_viable": True,
            "recommendations": []
        }
        
        # Build dependency graph
        for task_id in task_ids:
            dep_info = await self.task_master.get_task_dependencies(task_id)
            validation_result["dependency_graph"][task_id] = dep_info
            
            # Check for circular dependencies
            if self._has_circular_dependency(task_id, task_ids, set()):
                validation_result["circular_dependencies"].append(task_id)
                validation_result["valid"] = False
            
            # Check for blocked tasks
            if dep_info.get("blocked_status", False):
                validation_result["blocked_tasks"].append({
                    "task_id": task_id,
                    "reasons": dep_info.get("block_reasons", [])
                })
                validation_result["valid"] = False
        
        # Check if parallel execution is viable
        validation_result["parallel_execution_viable"] = self._assess_parallel_viability(
            task_ids, validation_result["dependency_graph"]
        )
        
        # Generate recommendations
        validation_result["recommendations"] = self._generate_dependency_recommendations(
            validation_result
        )
        
        logger.info(
            "Task dependency validation completed",
            task_count=len(task_ids),
            valid=validation_result["valid"],
            parallel_viable=validation_result["parallel_execution_viable"]
        )
        
        return validation_result
    
    async def allocate_worktree_resources(
        self,
        task_id: str,
        resource_requirements: Dict[ResourceType, float]
    ) -> Dict[str, Any]:
        """
        Allocate worktree resources for a task
        
        Args:
            task_id: Task ID
            resource_requirements: Required resources
            
        Returns:
            Allocation result
        """
        allocation_result = {
            "task_id": task_id,
            "allocated": True,
            "worktree_path": None,
            "resource_allocations": {},
            "isolation_confirmed": True
        }
        
        try:
            # Create worktree if not exists
            if task_id not in self.task_master.worktree_environments:
                worktree_path = await self.task_master.create_worktree_environment(
                    task_id, cleanup_on_complete=True
                )
                
                if not worktree_path:
                    allocation_result["allocated"] = False
                    allocation_result["error"] = "Failed to create worktree"
                    return allocation_result
                
                allocation_result["worktree_path"] = worktree_path
            
            # Allocate resources
            for resource_type, required_capacity in resource_requirements.items():
                allocation = ResourceAllocation(
                    task_id=task_id,
                    resource_type=resource_type,
                    allocated=True,
                    capacity=required_capacity,
                    current_usage=0.0,
                    isolation_level="isolated",
                    worktree_path=allocation_result["worktree_path"]
                )
                
                self.resource_allocations[f"{task_id}_{resource_type.value}"] = allocation
                allocation_result["resource_allocations"][resource_type.value] = asdict(allocation)
            
            logger.info(
                "Worktree resources allocated",
                task_id=task_id,
                worktree_path=allocation_result["worktree_path"],
                resource_count=len(resource_requirements)
            )
            
        except Exception as e:
            logger.error(
                "Resource allocation failed",
                task_id=task_id,
                error=str(e)
            )
            allocation_result["allocated"] = False
            allocation_result["error"] = str(e)
        
        return allocation_result
    
    async def execute_parallel_coordination(
        self,
        session_id: str,
        execution_callbacks: Dict[str, callable]
    ) -> Dict[str, Any]:
        """
        Execute parallel coordination session
        
        Args:
            session_id: Coordination session ID
            execution_callbacks: Task execution callbacks
            
        Returns:
            Execution result
        """
        if session_id not in self.active_coordinations:
            return {"error": "Session not found"}
        
        coordination = self.active_coordinations[session_id]
        tasks = coordination["tasks"]
        
        # Update status
        coordination["status"] = CoordinationStatus.COORDINATING
        
        # Validate dependencies
        dependency_validation = await self.validate_task_dependencies(tasks)
        if not dependency_validation["valid"]:
            coordination["status"] = CoordinationStatus.FAILED
            return {
                "error": "Dependency validation failed",
                "validation_result": dependency_validation
            }
        
        # Create coordination barriers
        await self._create_default_barriers(session_id, tasks)
        
        coordination["status"] = CoordinationStatus.EXECUTING
        
        # Execute tasks in parallel
        execution_results = await self._execute_parallel_tasks(
            session_id, tasks, execution_callbacks
        )
        
        # Synchronize at barriers
        coordination["status"] = CoordinationStatus.SYNCHRONIZING
        barrier_results = await self._synchronize_at_barriers(session_id)
        
        coordination["status"] = CoordinationStatus.COMPLETED
        
        final_result = {
            "session_id": session_id,
            "status": coordination["status"].value,
            "execution_results": execution_results,
            "barrier_results": barrier_results,
            "completed_at": datetime.utcnow().isoformat(),
            "duration_seconds": (datetime.utcnow() - coordination["created_at"]).total_seconds()
        }
        
        logger.info(
            "Parallel coordination completed",
            session_id=session_id,
            task_count=len(tasks),
            execution_results_count=len(execution_results)
        )
        
        return final_result
    
    def _has_circular_dependency(
        self, 
        task_id: str, 
        all_tasks: List[str], 
        visited: Set[str]
    ) -> bool:
        """Check for circular dependencies"""
        if task_id in visited:
            return True
        
        visited.add(task_id)
        
        if task_id in self.task_master.tasks:
            task = self.task_master.tasks[task_id]
            for dep_id in task.dependencies:
                if dep_id in all_tasks and self._has_circular_dependency(dep_id, all_tasks, visited.copy()):
                    return True
        
        return False
    
    def _assess_parallel_viability(
        self, 
        task_ids: List[str], 
        dependency_graph: Dict[str, Any]
    ) -> bool:
        """Assess if tasks can be executed in parallel"""
        # Check if any tasks have interdependencies
        for task_id in task_ids:
            task_deps = dependency_graph.get(task_id, {}).get("dependencies", [])
            for dep in task_deps:
                if dep["task_id"] in task_ids:
                    # Check if dependency is not yet completed
                    if dep["status"] != "done":
                        return False
        
        return True
    
    def _generate_dependency_recommendations(self, validation_result: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on dependency validation"""
        recommendations = []
        
        if validation_result["circular_dependencies"]:
            recommendations.append("🔄 BREAK: Resolve circular dependencies before parallel execution")
        
        if validation_result["blocked_tasks"]:
            recommendations.append("🚫 UNBLOCK: Complete blocked tasks or resolve blocking dependencies")
        
        if not validation_result["parallel_execution_viable"]:
            recommendations.append("🔄 SEQUENTIAL: Consider sequential execution for dependent tasks")
        
        if len(validation_result["dependency_graph"]) > 10:
            recommendations.append("⚠️ COMPLEX: Large task set may benefit from subdivision")
        
        return recommendations
    
    async def _create_default_barriers(self, session_id: str, tasks: List[str]):
        """Create default coordination barriers"""
        # Pre-execution barrier
        await self.create_coordination_barrier(
            session_id, "pre_execution", tasks, "all_complete", timeout=1800
        )
        
        # Mid-execution barrier (constitutional validation)
        await self.create_coordination_barrier(
            session_id, "constitutional_validation", tasks, "majority_complete", 
            threshold=0.8, timeout=3600
        )
        
        # Post-execution barrier
        await self.create_coordination_barrier(
            session_id, "post_execution", tasks, "all_complete", timeout=1800
        )
    
    async def _execute_parallel_tasks(
        self,
        session_id: str,
        tasks: List[str],
        execution_callbacks: Dict[str, callable]
    ) -> Dict[str, Any]:
        """Execute tasks in parallel"""
        execution_tasks = []
        
        for task_id in tasks:
            if task_id in execution_callbacks:
                task = asyncio.create_task(execution_callbacks[task_id](task_id))
                execution_tasks.append((task_id, task))
        
        # Wait for all tasks to complete
        results = {}
        for task_id, task in execution_tasks:
            try:
                result = await task
                results[task_id] = {"success": True, "result": result}
                
                # Update task status
                await self.task_master.update_task_status(
                    task_id, TaskStatus.DONE, f"Completed in parallel coordination {session_id}"
                )
                
            except Exception as e:
                results[task_id] = {"success": False, "error": str(e)}
                
                # Update task status
                await self.task_master.update_task_status(
                    task_id, TaskStatus.BLOCKED, f"Failed in parallel coordination: {str(e)}"
                )
        
        return results
    
    async def _synchronize_at_barriers(self, session_id: str) -> Dict[str, Any]:
        """Synchronize execution at coordination barriers"""
        if session_id not in self.active_coordinations:
            return {}
        
        coordination = self.active_coordinations[session_id]
        barrier_results = {}
        
        for barrier_id in coordination["barriers"]:
            if barrier_id in self.coordination_barriers:
                barrier = self.coordination_barriers[barrier_id]
                result = await self._wait_for_barrier(barrier)
                barrier_results[barrier_id] = result
                
                if result["triggered"]:
                    logger.info("Barrier synchronized", barrier_id=barrier_id)
        
        return barrier_results
    
    async def _wait_for_barrier(self, barrier: CoordinationBarrier) -> Dict[str, Any]:
        """Wait for a coordination barrier to be triggered"""
        start_time = datetime.utcnow()
        timeout = barrier.timeout or 3600
        
        while (datetime.utcnow() - start_time).total_seconds() < timeout:
            # Check barrier condition
            if await self._check_barrier_condition(barrier):
                barrier.triggered_at = datetime.utcnow()
                return {
                    "triggered": True,
                    "triggered_at": barrier.triggered_at.isoformat(),
                    "wait_time_seconds": (barrier.triggered_at - start_time).total_seconds()
                }
            
            await asyncio.sleep(1)  # Check every second
        
        return {
            "triggered": False,
            "timeout": True,
            "wait_time_seconds": timeout
        }
    
    async def _check_barrier_condition(self, barrier: CoordinationBarrier) -> bool:
        """Check if barrier condition is met"""
        completed_tasks = []
        
        for task_id in barrier.tasks:
            if task_id in self.task_master.tasks:
                task = self.task_master.tasks[task_id]
                if task.status == TaskStatus.DONE:
                    completed_tasks.append(task_id)
        
        completed_ratio = len(completed_tasks) / len(barrier.tasks)
        
        if barrier.condition == "all_complete":
            return completed_ratio >= 1.0
        elif barrier.condition == "any_complete":
            return completed_ratio > 0.0
        elif barrier.condition == "majority_complete":
            return completed_ratio >= barrier.threshold
        
        return False
    
    async def cleanup_coordination_session(self, session_id: str) -> bool:
        """Cleanup coordination session and resources"""
        try:
            if session_id in self.active_coordinations:
                coordination = self.active_coordinations[session_id]
                
                # Clean up worktree environments for session tasks
                for task_id in coordination["tasks"]:
                    if task_id in self.task_master.worktree_environments:
                        await self.task_master.cleanup_worktree_environments([task_id])
                
                # Remove barriers
                for barrier_id in coordination["barriers"]:
                    if barrier_id in self.coordination_barriers:
                        del self.coordination_barriers[barrier_id]
                
                # Remove resource allocations
                for task_id in coordination["tasks"]:
                    allocation_keys = [
                        key for key in self.resource_allocations.keys()
                        if key.startswith(task_id)
                    ]
                    for key in allocation_keys:
                        del self.resource_allocations[key]
                
                # Remove coordination session
                del self.active_coordinations[session_id]
                
                logger.info("Coordination session cleaned up", session_id=session_id)
                return True
            
            return False
            
        except Exception as e:
            logger.error(
                "Failed to cleanup coordination session",
                session_id=session_id, error=str(e)
            )
        return False


def get_coordination_status(self, session_id: str) -> Dict[str, Any]:
    """Get current coordination status"""
    if session_id not in self.active_coordinations:
        return {"error": "Session not found"}
    
    coordination = self.active_coordinations[session_id]
    
    return {
        "session_id": session_id,
        "parallel_group": coordination["parallel_group"],
        "status": coordination["status"].value,
        "task_count": len(coordination["tasks"]),
        "barrier_count": len(coordination["barriers"]),
        "created_at": coordination["created_at"].isoformat(),
        "active_barriers": [
            barrier_id for barrier_id in coordination["barriers"]
            if (barrier_id in self.coordination_barriers and
                self.coordination_barriers[barrier_id].triggered_at is None)
        ]
    }