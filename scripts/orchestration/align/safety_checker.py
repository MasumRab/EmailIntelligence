#!/usr/bin/env python3
"""
Safety Checker for Branch Operations

Comprehensive safety validation before executing branch operations.
Prevents accidental deletion of important branches and data loss.
"""

import subprocess
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass

from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

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
class SafetyRule:
    """Individual safety rule definition."""
    rule_id: str
    name: str
    description: str
    check_function: callable
    severity: str = "error"  # "error", "warning", "info"
    enabled: bool = True


class SafetyChecker:
    """Comprehensive safety checking for branch operations."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.rules = self._initialize_rules()
        self.protected_branches = self._get_protected_branches()
        self.recent_commits = self._get_recent_commits()
    
    def _initialize_rules(self) -> List[SafetyRule]:
        """Initialize all safety rules."""
        return [
            SafetyRule(
                "protected_branches",
                "Protected Branch Check",
                "Prevent operations on protected branches",
                self._check_protected_branches
            ),
            SafetyRule(
                "uncommitted_changes",
                "Uncommitted Changes Check",
                "Check for uncommitted changes on target branches",
                self._check_uncommitted_changes
            ),
            SafetyRule(
                "recent_commits",
                "Recent Commits Check",
                "Warn about operations on branches with recent commits",
                self._check_recent_commits
            ),
            SafetyRule(
                "open_prs",
                "Open Pull Requests Check",
                "Check for open pull requests",
                self._check_open_pull_requests
            ),
            SafetyRule(
                "branch_dependencies",
                "Branch Dependencies Check",
                "Check for dependent branches",
                self._check_branch_dependencies
            ),
            SafetyRule(
                "unique_commits",
                "Unique Commits Check",
                "Check for commits not present in target branch",
                self._check_unique_commits
            ),
            SafetyRule(
                "branch_age",
                "Branch Age Check",
                "Warn about very old branches",
                self._check_branch_age
            ),
            SafetyRule(
                "worktree_check",
                "Worktree Check",
                "Check if branch is used in worktrees",
                self._check_worktree_usage
            )
        ]
    
    def _get_protected_branches(self) -> Set[str]:
        """Get list of protected branches."""
        # Default protected branches
        protected = {"main", "master", "develop", "production", "staging"}
        
        # Check for additional protected branches in config
        try:
            result = subprocess.run(
                ["git", "config", "--get", "branchCleanup.protectedBranches"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                additional = set(result.stdout.strip().split(","))
                protected.update(additional)
        except subprocess.CalledProcessError:
            pass
        
        return protected
    
    def _get_recent_commits(self, days: int = 7) -> Dict[str, List[datetime]]:
        """Get recent commits for all branches."""
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        try:
            result = subprocess.run(
                ["git", "for-each-ref", "--format=%(refname:short)%00%(committerdate:iso8601)",
                 f"--sort=-committerdate", f"--merged=since={since_date}", "refs/heads/"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            recent_commits = {}
            for line in result.stdout.splitlines():
                if line.strip():
                    branch, date_str = line.split("\x00")
                    if branch not in recent_commits:
                        recent_commits[branch] = []
                    recent_commits[branch].append(datetime.fromisoformat(date_str))
            
            return recent_commits
            
        except subprocess.CalledProcessError:
            return {}
    
    def validate_operations(self, operations: List[BranchOperation]) -> List[str]:
        """Validate all operations and return list of issues."""
        issues = []
        
        for operation in operations:
            operation_issues = self.validate_operation(operation)
            issues.extend(operation_issues)
        
        return issues
    
    def validate_operation(self, operation: BranchOperation) -> List[str]:
        """Validate individual operation."""
        issues = []
        
        for rule in self.rules:
            if not rule.enabled:
                continue
            
            try:
                rule_issues = rule.check_function(operation)
                if rule_issues:
                    for issue in rule_issues:
                        issues.append(f"[{rule.severity.upper()}] {rule.name}: {issue}")
            except Exception as e:
                issues.append(f"[ERROR] Rule '{rule.name}' failed: {e}")
        
        return issues
    
    def _check_protected_branches(self, operation: BranchOperation) -> List[str]:
        """Check if operation targets protected branch."""
        issues = []
        
        if operation.branch_name in self.protected_branches:
            issues.append(f"Cannot {operation.operation_type.value} protected branch '{operation.branch_name}'")
        
        if operation.target_branch in self.protected_branches:
            if operation.operation_type == OperationType.DELETE:
                issues.append(f"Cannot delete branch that targets protected branch '{operation.target_branch}'")
        
        return issues
    
    def _check_uncommitted_changes(self, operation: BranchOperation) -> List[str]:
        """Check for uncommitted changes on branches."""
        issues = []
        
        # Check current branch for uncommitted changes
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout.strip():
                current_branch = subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=True
                ).stdout.strip()
                
                if current_branch in [operation.branch_name, operation.target_branch]:
                    issues.append(f"Branch '{current_branch}' has uncommitted changes")
        
        except subprocess.CalledProcessError:
            issues.append("Failed to check for uncommitted changes")
        
        return issues
    
    def _check_recent_commits(self, operation: BranchOperation) -> List[str]:
        """Check for recent commits on branch."""
        issues = []
        
        if operation.branch_name in self.recent_commits:
            recent_count = len(self.recent_commits[operation.branch_name])
            if recent_count > 0:
                latest_commit = max(self.recent_commits[operation.branch_name])
                days_ago = (datetime.now() - latest_commit).days
                
                if days_ago <= 1:
                    issues.append(f"Branch '{operation.branch_name}' has commits from {days_ago} day(s) ago")
                elif days_ago <= 7:
                    issues.append(f"Branch '{operation.branch_name}' has {recent_count} recent commit(s)")
        
        return issues
    
    def _check_open_pull_requests(self, operation: BranchOperation) -> List[str]:
        """Check for open pull requests."""
        issues = []
        
        # This would integrate with GitHub/GitLab API
        # For now, check for common PR branch patterns
        if any(pattern in operation.branch_name.lower() for pattern in ["pr/", "pull/", "merge/"]):
            issues.append(f"Branch '{operation.branch_name}' appears to be a pull request branch")
        
        return issues
    
    def _check_branch_dependencies(self, operation: BranchOperation) -> List[str]:
        """Check for branches that depend on this branch."""
        issues = []
        
        try:
            # Get all branches
            result = subprocess.run(
                ["git", "for-each-ref", "--format=%(refname:short)", "refs/heads/"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            all_branches = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            
            # Check if any branch has this branch as upstream
            for branch in all_branches:
                if branch == operation.branch_name:
                    continue
                
                try:
                    upstream = subprocess.run(
                        ["git", "config", "--get", f"branch.{branch}.merge"],
                        cwd=self.repo_path,
                        capture_output=True,
                        text=True
                    )
                    
                    if upstream.returncode == 0 and operation.branch_name in upstream.stdout:
                        issues.append(f"Branch '{branch}' depends on '{operation.branch_name}'")
                
                except subprocess.CalledProcessError:
                    continue
        
        except subprocess.CalledProcessError:
            issues.append("Failed to check branch dependencies")
        
        return issues
    
    def _check_unique_commits(self, operation: BranchOperation) -> List[str]:
        """Check for unique commits that would be lost."""
        issues = []
        
        if operation.operation_type in [OperationType.DELETE, OperationType.ARCHIVE]:
            target = operation.target_branch or "main"
            
            try:
                # Get commits unique to this branch
                result = subprocess.run(
                    ["git", "log", f"{target}..{operation.branch_name}", "--oneline"],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                unique_commits = result.stdout.strip().splitlines()
                if unique_commits:
                    issues.append(f"Branch '{operation.branch_name}' has {len(unique_commits)} unique commit(s) that would be lost")
            
            except subprocess.CalledProcessError:
                issues.append(f"Failed to check unique commits for '{operation.branch_name}'")
        
        return issues
    
    def _check_branch_age(self, operation: BranchOperation) -> List[str]:
        """Check branch age for very old branches."""
        issues = []
        
        try:
            # Get last commit date
            result = subprocess.run(
                ["git", "log", "-1", "--format=%ci", operation.branch_name],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout.strip():
                last_commit = datetime.strptime(result.stdout.strip(), "%Y-%m-%d %H:%M:%S %z")
                days_old = (datetime.now() - last_commit.replace(tzinfo=None)).days
                
                if days_old > 365:
                    issues.append(f"Branch '{operation.branch_name}' is {days_old} days old")
                elif days_old > 90:
                    issues.append(f"Branch '{operation.branch_name}' is {days_old} days old (consider reviewing)")
        
        except subprocess.CalledProcessError:
            issues.append(f"Failed to check age for '{operation.branch_name}'")
        
        return issues
    
    def _check_worktree_usage(self, operation: BranchOperation) -> List[str]:
        """Check if branch is used in worktrees."""
        issues = []
        
        try:
            # List worktrees
            result = subprocess.run(
                ["git", "worktree", "list"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.splitlines():
                if operation.branch_name in line:
                    issues.append(f"Branch '{operation.branch_name}' is used in a worktree")
                    break
        
        except subprocess.CalledProcessError:
            # Worktree command not available or no worktrees
            pass
        
        return issues
    
    def add_custom_rule(self, rule: SafetyRule):
        """Add custom safety rule."""
        self.rules.append(rule)
    
    def enable_rule(self, rule_id: str):
        """Enable a specific rule."""
        for rule in self.rules:
            if rule.rule_id == rule_id:
                rule.enabled = True
                return True
        return False
    
    def disable_rule(self, rule_id: str):
        """Disable a specific rule."""
        for rule in self.rules:
            if rule.rule_id == rule_id:
                rule.enabled = False
                return True
        return False
    
    def get_rule_status(self) -> List[Dict[str, Any]]:
        """Get status of all rules."""
        return [
            {
                "rule_id": rule.rule_id,
                "name": rule.name,
                "description": rule.description,
                "severity": rule.severity,
                "enabled": rule.enabled
            }
            for rule in self.rules
        ]
    
    def quick_sanity_check(self, branch_name: str) -> bool:
        """Quick sanity check for a branch."""
        # Check if it's a protected branch
        if branch_name in self.protected_branches:
            return False
        
        # Check if it's the current branch
        try:
            current = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()
            
            if current == branch_name:
                return False
        except subprocess.CalledProcessError:
            return False
        
        return True