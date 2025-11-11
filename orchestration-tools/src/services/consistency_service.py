"""
Service for Goal-Task Consistency Verification
"""
from typing import List, Dict, Optional
from datetime import datetime
from ..models.goal import Goal
from ..models.task import Task
from ..lib.error_handling import logger


class GoalTaskConsistencyService:
    """
    Service for verifying alignment between orchestration goals and implementation tasks
    """
    
    def __init__(self):
        self.goals = {}
        self.tasks = {}
    
    def add_goal(self, goal: Goal):
        """
        Add a goal to the service
        
        Args:
            goal: Goal to add
        """
        self.goals[goal.id] = goal
    
    def add_task(self, task: Task):
        """
        Add a task to the service
        
        Args:
            task: Task to add
        """
        self.tasks[task.id] = task
    
    def verify_alignment(self, goal_id: str, task_id: str, correlation_id: str = None) -> bool:
        """
        Verify that a task is aligned with a goal
        
        Args:
            goal_id: ID of the goal to check
            task_id: ID of the task to check
            correlation_id: Correlation ID for logging
            
        Returns:
            True if task is aligned with goal, False otherwise
        """
        if correlation_id:
            logger.info(f"Verifying alignment between goal {goal_id} and task {task_id}", correlation_id)
        
        goal = self.goals.get(goal_id)
        task = self.tasks.get(task_id)
        
        if not goal:
            if correlation_id:
                logger.error(f"Goal {goal_id} not found", correlation_id)
            return False
        
        if not task:
            if correlation_id:
                logger.error(f"Task {task_id} not found", correlation_id)
            return False
        
        # Check if task is related to goal
        is_aligned = goal_id in task.goal_ids
        
        if correlation_id:
            if is_aligned:
                logger.info(f"Task {task_id} is aligned with goal {goal_id}", correlation_id)
            else:
                logger.warning(f"Task {task_id} is NOT aligned with goal {goal_id}", correlation_id)
        
        return is_aligned
    
    def verify_goal_alignment(self, goal_id: str, correlation_id: str = None) -> Dict[str, any]:
        """
        Verify alignment of all tasks related to a goal
        
        Args:
            goal_id: ID of the goal to check
            correlation_id: Correlation ID for logging
            
        Returns:
            Dictionary with verification results
        """
        if correlation_id:
            logger.info(f"Verifying alignment for all tasks related to goal {goal_id}", correlation_id)
        
        goal = self.goals.get(goal_id)
        if not goal:
            if correlation_id:
                logger.error(f"Goal {goal_id} not found", correlation_id)
            return {
                "goal_id": goal_id,
                "passed": False,
                "error": f"Goal {goal_id} not found"
            }
        
        # Get all tasks related to this goal
        related_tasks = [task for task in self.tasks.values() if goal_id in task.goal_ids]
        
        aligned_tasks = []
        misaligned_tasks = []
        
        for task in related_tasks:
            if self.verify_alignment(goal_id, task.id, correlation_id):
                aligned_tasks.append(task.id)
            else:
                misaligned_tasks.append(task.id)
        
        passed = len(misaligned_tasks) == 0
        
        if correlation_id:
            if passed:
                logger.info(f"All {len(related_tasks)} tasks aligned with goal {goal_id}", correlation_id)
            else:
                logger.warning(f"{len(misaligned_tasks)} tasks misaligned with goal {goal_id}", correlation_id)
        
        return {
            "goal_id": goal_id,
            "passed": passed,
            "total_tasks": len(related_tasks),
            "aligned_tasks": aligned_tasks,
            "misaligned_tasks": misaligned_tasks,
            "details": f"{len(aligned_tasks)} tasks aligned, {len(misaligned_tasks)} tasks misaligned"
        }
    
    def find_misaligned_tasks(self, correlation_id: str = None) -> List[Dict[str, any]]:
        """
        Find all tasks that are not properly aligned with goals
        
        Args:
            correlation_id: Correlation ID for logging
            
        Returns:
            List of dictionaries with misalignment information
        """
        if correlation_id:
            logger.info("Finding all misaligned tasks", correlation_id)
        
        misaligned = []
        
        # Check each task for alignment
        for task in self.tasks.values():
            # A task should be related to at least one goal
            if not task.goal_ids:
                misaligned.append({
                    "task_id": task.id,
                    "issue": "Task not related to any goal",
                    "details": f"Task '{task.name}' has no associated goals"
                })
                continue
            
            # Check alignment with each associated goal
            for goal_id in task.goal_ids:
                if not self.verify_alignment(goal_id, task.id, correlation_id):
                    misaligned.append({
                        "task_id": task.id,
                        "goal_id": goal_id,
                        "issue": "Task-goal misalignment",
                        "details": f"Task '{task.name}' is not properly aligned with goal '{goal_id}'"
                    })
        
        if correlation_id:
            logger.info(f"Found {len(misaligned)} misaligned tasks", correlation_id)
        
        return misaligned