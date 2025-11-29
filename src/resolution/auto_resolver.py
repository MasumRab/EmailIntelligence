
"""
Automated conflict resolution module.
"""

from typing import List, Dict, Any

from ..core.interfaces import IConflictResolver
from ..core.models import (
    Conflict, 
    ResolutionStrategy, 
    ResolutionPlan, 
    ResolutionStep,
    ExecutionStatus
)
from .executor import ResolutionExecutor
from ..utils.logger import get_logger

logger = get_logger(__name__)

class AutoResolver(IConflictResolver):
    """
    Automatically resolves conflicts based on strategies.
    """
    
    def __init__(self):
        self.executor = ResolutionExecutor()
        
    async def resolve(self, conflict: Conflict, strategy: ResolutionStrategy) -> ResolutionPlan:
        """
        Create a resolution plan from a strategy.
        """
        logger.info("Creating resolution plan", strategy=strategy.name)
        
        plan = ResolutionPlan(
            id=f"plan-{conflict.id}",
            conflict_id=conflict.id,
            strategy_id=strategy.id,
            steps=strategy.steps, # Strategy already has steps from Generator
            status=ExecutionStatus.PENDING
        )
        
        return plan

    async def execute_plan(self, plan: ResolutionPlan) -> bool:
        """
        Execute the resolution plan.
        """
        return await self.executor.execute_plan(plan)
