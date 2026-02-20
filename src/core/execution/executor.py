import subprocess
from typing import List, Optional
from src.core.base import Action, LogicEngine
from src.core.models.execution import ExecutionPlan

class ActionExecutor(LogicEngine):
    """Executes atomic actions with rollback support."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run

    def validate(self, context: dict) -> bool:
        return True

    def execute_plan(self, plan: ExecutionPlan) -> bool:
        for action in plan.actions:
            if not self.execute_action(action):
                if plan.rollback_on_failure:
                    self.rollback(plan, action)
                return False
        return True

    def execute_action(self, action: Action) -> bool:
        if self.dry_run:
            print(f"[DRY-RUN] Executing: {action.description} ({action.command})")
            return True
            
        try:
            subprocess.run(action.command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def rollback(self, plan: ExecutionPlan, failed_action: Action):
        print(f"Rolling back after failure in {failed_action.id}")
        # Logic to iterate backwards and call rollback_command
        pass
