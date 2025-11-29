
"""
Resolution execution module.
"""

from typing import List, Dict, Any
from pathlib import Path

from ..core.models import (
    ResolutionPlan, 
    ResolutionStep, 
    ExecutionStatus,
    CodeChange
)
from ..git.repository import RepositoryOperations
from ..utils.logger import get_logger

logger = get_logger(__name__)

class ResolutionExecutor:
    """
    Executes resolution plans.
    """
    
    def __init__(self, repo_path: Path = None):
        self.repo = RepositoryOperations(repo_path)
        
    async def execute_plan(self, plan: ResolutionPlan) -> bool:
        """
        Execute a resolution plan step-by-step.
        """
        logger.info("Executing plan", plan_id=plan.id)
        
        plan.status = ExecutionStatus.IN_PROGRESS
        
        try:
            for step in plan.steps:
                success = await self._execute_step(step)
                if not success:
                    logger.error("Step failed", step=step.description)
                    plan.status = ExecutionStatus.FAILED
                    # TODO: Trigger rollback
                    return False
                    
            plan.status = ExecutionStatus.COMPLETED
            logger.info("Plan executed successfully")
            return True
            
        except Exception as e:
            logger.error("Plan execution error", error=str(e))
            plan.status = ExecutionStatus.FAILED
            return False

    async def _execute_step(self, step: ResolutionStep) -> bool:
        """Execute a single resolution step."""
        logger.info("Executing step", action=step.action)
        
        try:
            if step.action == "git_checkout":
                # params: source, file
                await self.repo.run_git(["checkout", step.params["source"], "--", step.params["file"]])
                
            elif step.action == "git_add":
                # params: file
                await self.repo.run_git(["add", step.params["file"]])
                
            elif step.action == "write_file":
                # params: file, content (optional if passed in context)
                # This is simplified; usually content comes from previous steps
                pass
                
            elif step.action == "manual_edit":
                # Pause for user input (CLI interaction)
                # For now, just log
                logger.info("Waiting for manual edit...")
                
            return True
            
        except Exception as e:
            logger.error("Step execution failed", error=str(e))
            return False
