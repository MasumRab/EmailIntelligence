#!/usr/bin/env python3
"""
Review Validator for Branch Cleanup Plans

Comprehensive review system for cleanup plans including
impact analysis, conflict detection, and approval workflows.
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json

class OperationType(Enum):
    DELETE = "delete"
    MERGE = "merge"
    REBASE = "rebase"
    ARCHIVE = "archive"
    RENAME = "rename"
    SYNC = "sync"

class OperationStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW_REQUIRED = "review_required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ROLLED_BACK = "rolled_back"

@dataclass
class BranchOperation:
    operation_id: str
    branch_name: str
    operation_type: OperationType
    target_branch: str = None
    priority: str = "normal"
    reason: str = ""
    metadata: dict = None
    status: OperationStatus = OperationStatus.PENDING
    created_at: datetime = None
    started_at: datetime = None
    completed_at: datetime = None
    error_message: str = None
    rollback_available: bool = False

@dataclass
class CleanupPlan:
    plan_id: str
    name: str
    description: str
    operations: list = None
    created_at: datetime = None
    status: str = "draft"
    reviewed: bool = False
    approved: bool = False
    executed: bool = False
    rollback_available: bool = False


@dataclass
class ReviewIssue:
    """Individual review issue."""
    issue_id: str
    severity: str  # "critical", "high", "medium", "low", "info"
    category: str  # "safety", "conflict", "impact", "policy"
    description: str
    recommendation: str
    operation_id: Optional[str] = None


@dataclass
class ReviewResult:
    """Complete review result."""
    review_id: str
    plan_id: str
    timestamp: datetime
    reviewer: str
    issues: List[ReviewIssue] = field(default_factory=list)
    overall_status: str = "pending"  # "approved", "rejected", "needs_changes"
    comments: str = ""
    approval_required: bool = True


class ReviewValidator:
    """Comprehensive review validation for cleanup plans."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.review_history: List[ReviewResult] = []
        self.policies = self._load_policies()
    
    def _load_policies(self) -> Dict[str, Any]:
        """Load review policies from config."""
        policies = {
            "max_operations_per_plan": 50,
            "require_approval_for_delete": True,
            "require_approval_for_merge": True,
            "require_review_for_protected_branches": True,
            "max_branch_age_days": 365,
            "require_unique_commit_analysis": True,
            "conflict_resolution_required": True
        }
        
        # Try to load from config file
        config_path = self.repo_path / ".branch_cleanup" / "review_policies.json"
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    file_policies = json.load(f)
                policies.update(file_policies)
            except (json.JSONDecodeError, IOError):
                pass
        
        return policies
    
    def validate_plan(self, plan: CleanupPlan) -> List[str]:
        """Validate cleanup plan and return list of issues."""
        issues = []
        
        # Basic policy validation
        policy_issues = self._validate_policies(plan)
        issues.extend(policy_issues)
        
        # Operation-specific validation
        operation_issues = self._validate_operations(plan.operations)
        issues.extend(operation_issues)
        
        # Conflict analysis
        conflict_issues = self._analyze_conflicts(plan.operations)
        issues.extend(conflict_issues)
        
        # Impact analysis
        impact_issues = self._analyze_impact(plan.operations)
        issues.extend(impact_issues)
        
        return issues
    
    def _validate_policies(self, plan: CleanupPlan) -> List[str]:
        """Validate plan against policies."""
        issues = []
        
        # Check operation count
        if len(plan.operations) > self.policies["max_operations_per_plan"]:
            issues.append(
                f"Plan has {len(plan.operations)} operations, "
                f"exceeds maximum of {self.policies['max_operations_per_plan']}"
            )
        
        # Check for delete operations
        delete_ops = [op for op in plan.operations if op.operation_type == OperationType.DELETE]
        if delete_ops and self.policies["require_approval_for_delete"]:
            issues.append(f"Plan contains {len(delete_ops)} delete operations requiring approval")
        
        # Check for merge operations
        merge_ops = [op for op in plan.operations if op.operation_type == OperationType.MERGE]
        if merge_ops and self.policies["require_approval_for_merge"]:
            issues.append(f"Plan contains {len(merge_ops)} merge operations requiring approval")
        
        return issues
    
    def _validate_operations(self, operations: List[BranchOperation]) -> List[str]:
        """Validate individual operations."""
        issues = []
        
        for operation in operations:
            op_issues = self._validate_operation(operation)
            issues.extend(op_issues)
        
        return issues
    
    def _validate_operation(self, operation: BranchOperation) -> List[str]:
        """Validate individual operation."""
        issues = []
        
        # Check branch exists
        if not self._branch_exists(operation.branch_name):
            issues.append(f"Branch '{operation.branch_name}' does not exist")
        
        # Check target branch for merge operations
        if operation.operation_type == OperationType.MERGE:
            target = operation.target_branch or "main"
            if not self._branch_exists(target):
                issues.append(f"Target branch '{target}' does not exist")
        
        # Check for valid operation reason
        if not operation.reason.strip():
            issues.append(f"Operation on '{operation.branch_name}' missing reason")
        
        return issues
    
    def _analyze_conflicts(self, operations: List[BranchOperation]) -> List[str]:
        """Analyze potential conflicts between operations."""
        issues = []
        
        # Check for duplicate operations on same branch
        branch_operations = {}
        for op in operations:
            if op.branch_name not in branch_operations:
                branch_operations[op.branch_name] = []
            branch_operations[op.branch_name].append(op)
        
        for branch, ops in branch_operations.items():
            if len(ops) > 1:
                issues.append(f"Multiple operations on branch '{branch}': {', '.join(op.operation_type.value for op in ops)}")
        
        # Check for merge conflicts
        merge_ops = [op for op in operations if op.operation_type == OperationType.MERGE]
        for merge_op in merge_ops:
            if self._has_merge_conflicts(merge_op.branch_name, merge_op.target_branch or "main"):
                issues.append(f"Merge operation for '{merge_op.branch_name}' has potential conflicts")
        
        return issues
    
    def _analyze_impact(self, operations: List[BranchOperation]) -> List[str]:
        """Analyze impact of operations."""
        issues = []
        
        # Count operations by type
        op_counts = {}
        for op in operations:
            op_type = op.operation_type.value
            op_counts[op_type] = op_counts.get(op_type, 0) + 1
        
        # High impact warnings
        if op_counts.get("delete", 0) > 5:
            issues.append(f"High impact: {op_counts['delete']} branches will be deleted")
        
        if op_counts.get("merge", 0) > 3:
            issues.append(f"High impact: {op_counts['merge']} branches will be merged")
        
        # Check for unique commit loss
        delete_ops = [op for op in operations if op.operation_type == OperationType.DELETE]
        total_unique_commits = 0
        for op in delete_ops:
            unique_count = self._count_unique_commits(op.branch_name)
            if unique_count > 0:
                total_unique_commits += unique_count
        
        if total_unique_commits > 0:
            issues.append(f"Operations will lose {total_unique_commits} unique commits")
        
        return issues
    
    def _branch_exists(self, branch_name: str) -> bool:
        """Check if branch exists."""
        try:
            subprocess.run(
                ["git", "rev-parse", "--verify", f"refs/heads/{branch_name}"],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def _has_merge_conflicts(self, source: str, target: str) -> bool:
        """Check if merge would have conflicts."""
        try:
            # Try a dry-run merge
            subprocess.run(
                ["git", "merge-tree", f"{target}^{tree}", f"{source}^{tree}", f"{target}^{tree}"],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )
            return False
        except subprocess.CalledProcessError:
            return True
    
    def _count_unique_commits(self, branch_name: str) -> int:
        """Count unique commits on branch."""
        try:
            result = subprocess.run(
                ["git", "log", f"main..{branch_name}", "--oneline"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return len(result.stdout.strip().splitlines())
        except subprocess.CalledProcessError:
            return 0
    
    def create_review(self, plan: CleanupPlan, reviewer: str = "system") -> ReviewResult:
        """Create a formal review for the plan."""
        review_id = f"review_{int(datetime.now().timestamp())}"
        
        issues = []
        
        # Get validation issues
        validation_issues = self.validate_plan(plan)
        for issue_text in validation_issues:
            issue = ReviewIssue(
                issue_id=f"issue_{len(issues)}",
                severity=self._extract_severity(issue_text),
                category=self._categorize_issue(issue_text),
                description=issue_text,
                recommendation=self._generate_recommendation(issue_text)
            )
            issues.append(issue)
        
        # Determine overall status
        critical_issues = [i for i in issues if i.severity == "critical"]
        high_issues = [i for i in issues if i.severity == "high"]
        
        if critical_issues:
            overall_status = "rejected"
        elif high_issues:
            overall_status = "needs_changes"
        else:
            overall_status = "approved"
        
        review = ReviewResult(
            review_id=review_id,
            plan_id=plan.plan_id,
            timestamp=datetime.now(),
            reviewer=reviewer,
            issues=issues,
            overall_status=overall_status,
            approval_required=len(issues) > 0
        )
        
        self.review_history.append(review)
        return review
    
    def _extract_severity(self, issue_text: str) -> str:
        """Extract severity from issue text."""
        if "[ERROR]" in issue_text or "critical" in issue_text.lower():
            return "critical"
        elif "high" in issue_text.lower():
            return "high"
        elif "medium" in issue_text.lower():
            return "medium"
        elif "low" in issue_text.lower():
            return "low"
        else:
            return "info"
    
    def _categorize_issue(self, issue_text: str) -> str:
        """Categorize issue type."""
        if "protected" in issue_text.lower() or "safety" in issue_text.lower():
            return "safety"
        elif "conflict" in issue_text.lower():
            return "conflict"
        elif "impact" in issue_text.lower() or "unique" in issue_text.lower():
            return "impact"
        else:
            return "policy"
    
    def _generate_recommendation(self, issue_text: str) -> str:
        """Generate recommendation for issue."""
        if "protected" in issue_text.lower():
            return "Remove protected branch from operations or use different operation type"
        elif "conflict" in issue_text.lower():
            return "Resolve conflicts before proceeding or manual merge required"
        elif "unique commits" in issue_text.lower():
            return "Consider merging or archiving branch to preserve commits"
        elif "does not exist" in issue_text.lower():
            return "Remove operation or verify branch name"
        else:
            return "Review and address the specific concern"
    
    def approve_review(self, review_id: str, reviewer: str, comments: str = "") -> bool:
        """Approve a review."""
        for review in self.review_history:
            if review.review_id == review_id:
                review.overall_status = "approved"
                review.comments = comments
                review.approval_required = False
                return True
        return False
    
    def reject_review(self, review_id: str, reviewer: str, comments: str = "") -> bool:
        """Reject a review."""
        for review in self.review_history:
            if review.review_id == review_id:
                review.overall_status = "rejected"
                review.comments = comments
                review.approval_required = False
                return True
        return False
    
    def get_review_summary(self, review_id: str) -> Optional[Dict[str, Any]]:
        """Get summary of a review."""
        for review in self.review_history:
            if review.review_id == review_id:
                return {
                    "review_id": review.review_id,
                    "plan_id": review.plan_id,
                    "timestamp": review.timestamp.isoformat(),
                    "reviewer": review.reviewer,
                    "overall_status": review.overall_status,
                    "issues_count": len(review.issues),
                    "critical_issues": len([i for i in review.issues if i.severity == "critical"]),
                    "high_issues": len([i for i in review.issues if i.severity == "high"]),
                    "approval_required": review.approval_required,
                    "comments": review.comments
                }
        return None
    
    def get_all_reviews(self) -> List[Dict[str, Any]]:
        """Get all reviews."""
        return [self.get_review_summary(review.review_id) for review in self.review_history]
    
    def export_review(self, review_id: str, filepath: str) -> bool:
        """Export review to file."""
        for review in self.review_history:
            if review.review_id == review_id:
                review_data = {
                    "review_id": review.review_id,
                    "plan_id": review.plan_id,
                    "timestamp": review.timestamp.isoformat(),
                    "reviewer": review.reviewer,
                    "overall_status": review.overall_status,
                    "comments": review.comments,
                    "approval_required": review.approval_required,
                    "issues": [
                        {
                            "issue_id": issue.issue_id,
                            "severity": issue.severity,
                            "category": issue.category,
                            "description": issue.description,
                            "recommendation": issue.recommendation,
                            "operation_id": issue.operation_id
                        }
                        for issue in review.issues
                    ]
                }
                
                try:
                    with open(filepath, 'w') as f:
                        json.dump(review_data, f, indent=2)
                    return True
                except IOError:
                    return False
        return False