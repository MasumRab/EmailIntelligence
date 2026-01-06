#!/usr/bin/env python3
"""
Branch Cleanup Manager

Core management for branch cleanup operations with safety checks,
review capabilities, and comprehensive logging.
"""

import json
import logging
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

# Import components to avoid circular dependencies


class OperationType(Enum):
    """Types of branch operations."""
    DELETE = "delete"
    MERGE = "merge"
    REBASE = "rebase"
    ARCHIVE = "archive"
    RENAME = "rename"
    SYNC = "sync"


class OperationStatus(Enum):
    """Operation status tracking."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW_REQUIRED = "review_required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ROLLED_BACK = "rolled_back"


@dataclass
class BranchOperation:
    """Individual branch operation definition."""
    operation_id: str
    branch_name: str
    operation_type: OperationType
    target_branch: Optional[str] = None
    priority: str = "normal"
    reason: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: OperationStatus = OperationStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    rollback_available: bool = False


@dataclass
class CleanupPlan:
    """Complete cleanup plan with multiple operations."""
    plan_id: str
    name: str
    description: str
    operations: List[BranchOperation] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "draft"
    reviewed: bool = False
    approved: bool = False
    executed: bool = False
    rollback_available: bool = False


class BranchCleanupManager:
    """Main branch cleanup management system."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.logger = self._setup_logging()
        
        # Initialize components (lazy loading to avoid circular imports)
        self._safety_checker = None
        self._review_validator = None
        self._report_generator = None
        self._rollback_manager = None
        
        # State tracking
        self.plans: Dict[str, CleanupPlan] = {}
        self.operation_history: List[BranchOperation] = []
        self._ensure_directories()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging."""
        log_dir = Path(self.repo_path) / "logs" / "branch_cleanup"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logger = logging.getLogger("branch_cleanup")
        logger.setLevel(logging.INFO)
        
        # File handler
        fh = logging.FileHandler(log_dir / f"cleanup_{datetime.now().strftime('%Y%m%d')}.log")
        fh.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    def _ensure_directories(self):
        """Ensure required directories exist."""
        dirs = [
            "logs/branch_cleanup",
            "reports/branch_cleanup", 
            "backups/branch_cleanup",
            "temp/branch_cleanup"
        ]
        
        for dir_path in dirs:
            (self.repo_path / dir_path).mkdir(parents=True, exist_ok=True)
    
    def create_cleanup_plan(self, name: str, description: str, 
                          branch_data: List[Dict[str, Any]]) -> str:
        """Create a new cleanup plan from branch analysis data."""
        plan_id = f"plan_{int(time.time())}"
        
        operations = []
        for branch_info in branch_data:
            # Determine operation type based on branch analysis
            op_type = self._determine_operation_type(branch_info)
            
            operation = BranchOperation(
                operation_id=f"op_{len(operations)}_{int(time.time())}",
                branch_name=branch_info["name"],
                operation_type=op_type,
                priority=branch_info.get("priority", "normal"),
                reason=branch_info.get("reason", ""),
                metadata=branch_info
            )
            
            operations.append(operation)
        
        plan = CleanupPlan(
            plan_id=plan_id,
            name=name,
            description=description,
            operations=operations
        )
        
        self.plans[plan_id] = plan
        self.logger.info(f"Created cleanup plan: {plan_id} with {len(operations)} operations")
        
        return plan_id
    
    def _determine_operation_type(self, branch_info: Dict[str, Any]) -> OperationType:
        """Determine appropriate operation type for branch."""
        name = branch_info["name"]
        status = branch_info.get("status", "")
        
        # Check for backup branches
        if "backup" in name.lower():
            return OperationType.DELETE
        
        # Check for temporary branches
        temp_patterns = ["temp-", "wip-", "test-", "cleanup-"]
        if any(pattern in name.lower() for pattern in temp_patterns):
            return OperationType.DELETE
        
        # Check for stale feature branches
        if status == "stale" and "feature-" in name.lower():
            return OperationType.ARCHIVE
        
        # Check for branches ready for merge
        if status == "ready_to_merge":
            return OperationType.MERGE
        
        # Default to review required
        return OperationType.DELETE  # Will be caught by safety checks
    
    def review_plan(self, plan_id: str) -> Tuple[bool, List[str]]:
        """Review a cleanup plan for safety and completeness."""
        if plan_id not in self.plans:
            return False, ["Plan not found"]
        
        plan = self.plans[plan_id]
        issues = []
        
        # Safety checks
        safety_issues = self._get_safety_checker().validate_operations(plan.operations)
        issues.extend(safety_issues)
        
        # Review validation
        review_issues = self._get_review_validator().validate_plan(plan)
        issues.extend(review_issues)
        
        # Check for critical branches
        protected_branches = ["main", "master", "develop", "production"]
        for op in plan.operations:
            if op.branch_name in protected_branches:
                issues.append(f"Cannot {op.operation_type.value} protected branch: {op.branch_name}")
        
        if not issues:
            plan.reviewed = True
            plan.status = "reviewed"
            self.logger.info(f"Plan {plan_id} passed review")
        
        return len(issues) == 0, issues
    
    def execute_plan(self, plan_id: str, auto_approve: bool = False) -> bool:
        """Execute a cleanup plan with full safety checks."""
        if plan_id not in self.plans:
            self.logger.error(f"Plan {plan_id} not found")
            return False
        
        plan = self.plans[plan_id]
        
        # Final safety check
        if not plan.reviewed and not auto_approve:
            review_passed, issues = self.review_plan(plan_id)
            if not review_passed:
                self.logger.error(f"Plan {plan_id} failed review: {issues}")
                return False
        
        # Create rollback point
        rollback_id = self._get_rollback_manager().create_checkpoint(
            f"before_cleanup_{plan_id}"
        )
        
        try:
            plan.status = "executing"
            plan.executed = True
            
            for operation in plan.operations:
                self._execute_operation(operation)
            
            plan.status = "completed"
            plan.rollback_available = True
            self.logger.info(f"Successfully executed cleanup plan: {plan_id}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to execute plan {plan_id}: {e}")
            plan.status = "failed"
            
            # Offer rollback
            if rollback_id:
                self.logger.info(f"Rollback available: {rollback_id}")
            
            return False
    
    def _execute_operation(self, operation: BranchOperation):
        """Execute individual branch operation."""
        operation.status = OperationStatus.IN_PROGRESS
        operation.started_at = datetime.now()
        
        try:
            if operation.operation_type == OperationType.DELETE:
                self._delete_branch(operation)
            elif operation.operation_type == OperationType.MERGE:
                self._merge_branch(operation)
            elif operation.operation_type == OperationType.ARCHIVE:
                self._archive_branch(operation)
            elif operation.operation_type == OperationType.SYNC:
                self._sync_branch(operation)
            
            operation.status = OperationStatus.COMPLETED
            operation.completed_at = datetime.now()
            
        except Exception as e:
            operation.status = OperationStatus.FAILED
            operation.error_message = str(e)
            operation.completed_at = datetime.now()
            raise
    
    def _delete_branch(self, operation: BranchOperation):
        """Delete a branch safely."""
        branch_name = operation.branch_name
        
        # Ensure we're not on the branch to be deleted
        current_branch = self._run_git_command("git branch --show-current")
        if current_branch == branch_name:
            self._run_git_command("git checkout main")
        
        # Delete local branch
        self._run_git_command(f"git branch -D {branch_name}")
        
        # Delete remote branch if exists
        try:
            self._run_git_command(f"git push origin --delete {branch_name}")
        except subprocess.CalledProcessError:
            # Remote branch might not exist, that's okay
            pass
        
        self.logger.info(f"Deleted branch: {branch_name}")
    
    def _merge_branch(self, operation: BranchOperation):
        """Merge a branch to its target."""
        branch_name = operation.branch_name
        target = operation.target_branch or "main"
        
        # Checkout target branch
        self._run_git_command(f"git checkout {target}")
        
        # Merge branch
        self._run_git_command(f"git merge {branch_name} --no-ff")
        
        # Push merge
        self._run_git_command(f"git push origin {target}")
        
        # Delete merged branch
        self._delete_branch(operation)
        
        self.logger.info(f"Merged {branch_name} into {target}")
    
    def _archive_branch(self, operation: BranchOperation):
        """Archive a branch with tag."""
        branch_name = operation.branch_name
        tag_name = f"archive/{branch_name}/{int(time.time())}"
        
        # Create tag from branch
        self._run_git_command(f"git tag {tag_name} {branch_name}")
        
        # Push tag
        self._run_git_command(f"git push origin {tag_name}")
        
        # Delete branch
        self._delete_branch(operation)
        
        self.logger.info(f"Archived branch {branch_name} as tag {tag_name}")
    
    def _sync_branch(self, operation: BranchOperation):
        """Sync branch with remote."""
        branch_name = operation.branch_name
        
        # Checkout branch
        self._run_git_command(f"git checkout {branch_name}")
        
        # Pull latest changes
        self._run_git_command(f"git pull origin {branch_name}")
        
        self.logger.info(f"Synced branch: {branch_name}")
    
    def _run_git_command(self, command: str) -> str:
        """Execute git command with error handling."""
        result = subprocess.run(
            command,
            shell=True,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    
    def generate_report(self, plan_id: str) -> str:
        """Generate comprehensive cleanup report."""
        if plan_id not in self.plans:
            return "Plan not found"
        
        plan = self.plans[plan_id]
        return self._get_report_generator().generate_plan_report(plan)
    
    def rollback_plan(self, plan_id: str) -> bool:
        """Rollback a cleanup plan."""
        if plan_id not in self.plans:
            return False
        
        plan = self.plans[plan_id]
        if not plan.rollback_available:
            return False
        
        return self._get_rollback_manager().rollback_to_checkpoint(
            f"before_cleanup_{plan_id}"
        )
    
    def list_plans(self) -> List[Dict[str, Any]]:
        """List all cleanup plans."""
        return [
            {
                "plan_id": plan.plan_id,
                "name": plan.name,
                "status": plan.status,
                "operations_count": len(plan.operations),
                "created_at": plan.created_at.isoformat(),
                "reviewed": plan.reviewed,
                "executed": plan.executed
            }
            for plan in self.plans.values()
        ]
    
    def save_plan(self, plan_id: str, filepath: str):
        """Save plan to file."""
        if plan_id not in self.plans:
            raise ValueError("Plan not found")
        
        plan = self.plans[plan_id]
        
        # Convert to serializable format
        plan_data = asdict(plan)
        for op in plan_data["operations"]:
            op["operation_type"] = op["operation_type"].value
            op["status"] = op["status"].value
            if op["started_at"]:
                op["started_at"] = op["started_at"].isoformat()
            if op["completed_at"]:
                op["completed_at"] = op["completed_at"].isoformat()
        
        plan_data["created_at"] = plan.created_at.isoformat()
        
        with open(filepath, 'w') as f:
            json.dump(plan_data, f, indent=2)
    
    def load_plan(self, filepath: str) -> str:
        """Load plan from file."""
        with open(filepath, 'r') as f:
            plan_data = json.load(f)
        
        # Reconstruct plan object
        operations = []
        for op_data in plan_data["operations"]:
            op_data["operation_type"] = OperationType(op_data["operation_type"])
            op_data["status"] = OperationStatus(op_data["status"])
            operations.append(BranchOperation(**op_data))
        
        plan = CleanupPlan(
            plan_id=plan_data["plan_id"],
            name=plan_data["name"],
            description=plan_data["description"],
            operations=operations,
            created_at=datetime.fromisoformat(plan_data["created_at"]),
            status=plan_data.get("status", "draft"),
            reviewed=plan_data.get("reviewed", False),
            approved=plan_data.get("approved", False),
            executed=plan_data.get("executed", False)
        )
        
        self.plans[plan.plan_id] = plan
        return plan.plan_id
    
    def _get_safety_checker(self):
        if self._safety_checker is None:
            from safety_checker import SafetyChecker
            self._safety_checker = SafetyChecker(self.repo_path)
        return self._safety_checker
    
    def _get_review_validator(self):
        if self._review_validator is None:
            from review_validator import ReviewValidator
            self._review_validator = ReviewValidator(self.repo_path)
        return self._review_validator
    
    def _get_report_generator(self):
        if self._report_generator is None:
            from report_generator import ReportGenerator
            self._report_generator = ReportGenerator(self.repo_path)
        return self._report_generator
    
    def _get_rollback_manager(self):
        if self._rollback_manager is None:
            from rollback_manager import RollbackManager
            self._rollback_manager = RollbackManager(self.repo_path)
        return self._rollback_manager