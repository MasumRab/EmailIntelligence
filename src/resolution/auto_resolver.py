"""
Automated conflict resolution module.
"""

from ..core.interfaces import IConflictResolver
from ..core.conflict_models import Conflict, ResolutionStrategy, ResolutionPlan, ExecutionStatus
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
        if not conflict or not strategy:
            raise ValueError("Conflict and strategy must be provided")
        if not hasattr(conflict, "id") or not hasattr(strategy, "steps"):
            raise ValueError("Conflict and strategy must have required attributes (id, steps)")

        if not isinstance(strategy.steps, list):
            raise ValueError("Strategy steps must be a list")

        if not hasattr(strategy, "name") or not hasattr(strategy, "id"):
            raise ValueError("Strategy must have required attributes (name, id)")

        logger.info("Creating resolution plan", strategy=strategy.name, conflict_id=conflict.id)

        try:
            plan = ResolutionPlan(
                id=f"plan-{conflict.id}",
                conflict_id=conflict.id,
                strategy_id=strategy.id,
                steps=strategy.steps,  # Strategy already has steps from Generator
                status=ExecutionStatus.PENDING,
            )
            return plan
        except Exception as e:
            logger.error(
                "Failed to create resolution plan",
                error=str(e),
                conflict_id=conflict.id,
                strategy_id=strategy.id,
            )
            raise

    async def execute_plan(self, plan: ResolutionPlan) -> bool:
        """
        Execute the resolution plan.
        """
        if not plan or not isinstance(plan, ResolutionPlan):
            raise ValueError("Invalid resolution plan provided")

        logger.info("Executing resolution plan", plan_id=plan.id)

        try:
            result = await self.executor.execute_plan(plan)
            if result:
                logger.info("Resolution plan executed successfully", plan_id=plan.id)
            else:
                logger.warning("Resolution plan execution failed", plan_id=plan.id)
            return result
        except Exception as e:
            logger.error(
                "Error executing resolution plan", error=str(e), plan_id=plan.id, exc_info=True
            )
            return False
