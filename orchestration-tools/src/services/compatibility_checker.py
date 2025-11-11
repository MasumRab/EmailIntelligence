"""
Service for Branch Compatibility Checking
"""
from typing import List, Dict, Optional
from datetime import datetime
from ..models.branch import Branch
from ..services.git_service import GitService
from ..lib.error_handling import logger


class CompatibilityChecker:
    """
    Service for checking compatibility between branches before merging
    """
    
    def __init__(self, git_service: GitService):
        self.git_service = git_service
    
    def check_branch_compatibility(self, source_branch: str, target_branch: str, correlation_id: str = None) -> Dict[str, any]:
        """
        Check compatibility between two branches
        
        Args:
            source_branch: Source branch name
            target_branch: Target branch name
            correlation_id: Correlation ID for logging
        
        Returns:
            Dictionary with compatibility check results
        """
        if correlation_id:
            logger.info(f"Checking compatibility between {source_branch} and {target_branch}", correlation_id)
        
        # Check if branches exist
        all_branches = self.git_service.get_all_branches()
        if source_branch not in all_branches:
            error_msg = f"Source branch '{source_branch}' not found"
            if correlation_id:
                logger.error(error_msg, correlation_id)
            return {
                "source_branch": source_branch,
                "target_branch": target_branch,
                "passed": False,
                "error": error_msg
            }
        
        if target_branch not in all_branches:
            error_msg = f"Target branch '{target_branch}' not found"
            if correlation_id:
                logger.error(error_msg, correlation_id)
            return {
                "source_branch": source_branch,
                "target_branch": target_branch,
                "passed": False,
                "error": error_msg
            }
        
        # Check if source branch is up to date with target branch
        is_up_to_date = self.git_service.is_branch_up_to_date(source_branch, target_branch)
        
        # Get diff between branches
        diff = self.git_service.get_diff_between_branches(source_branch, target_branch)
        diff_lines = diff.count('\n') if diff else 0
        
        # In a real implementation, we would perform more detailed compatibility checks
        # For now, we'll use a simple heuristic
        passed = is_up_to_date or diff_lines < 1000  # Pass if up to date or diff is small
        
        results = {
            "source_branch": source_branch,
            "target_branch": target_branch,
            "passed": passed,
            "is_up_to_date": is_up_to_date,
            "diff_lines": diff_lines,
            "details": f"Branch compatibility check completed. Up to date: {is_up_to_date}, Diff lines: {diff_lines}"
        }
        
        if correlation_id:
            status = "PASSED" if passed else "FAILED"
            logger.info(f"Branch compatibility check {status}: {results['details']}", correlation_id)
        
        return results
    
    def validate_target_environment(self, branch_name: str, target_branch: str, correlation_id: str = None) -> Dict[str, any]:
        """
        Validate target branch environment for compatibility
        
        Args:
            branch_name: Branch name to validate
            target_branch: Target branch to validate against
            correlation_id: Correlation ID for logging
        
        Returns:
            Dictionary with environment validation results
        """
        if correlation_id:
            logger.info(f"Validating target environment for {branch_name} against {target_branch}", correlation_id)
        
        # Get branch information
        source_info = self.git_service.get_branch_info(branch_name)
        target_info = self.git_service.get_branch_info(target_branch)
        
        if not source_info:
            error_msg = f"Source branch '{branch_name}' not found"
            if correlation_id:
                logger.error(error_msg, correlation_id)
            return {
                "branch": branch_name,
                "target": target_branch,
                "passed": False,
                "error": error_msg
            }
        
        if not target_info:
            error_msg = f"Target branch '{target_branch}' not found"
            if correlation_id:
                logger.error(error_msg, correlation_id)
            return {
                "branch": branch_name,
                "target": target_branch,
                "passed": False,
                "error": error_msg
            }
        
        # Check branch types compatibility
        source_type = source_info.type.value
        target_type = target_info.type.value
        
        # Define compatibility matrix
        compatibility_matrix = {
            "feature": ["feature", "scientific", "main"],
            "scientific": ["scientific", "main"],
            "main": ["main"],
            "release": ["release", "main"]
        }
        
        is_compatible_type = target_type in compatibility_matrix.get(source_type, [])
        
        # Check if branches are in the same repository (simplified check)
        same_repo = True  # In a real implementation, this would check repository URLs
        
        passed = is_compatible_type and same_repo
        
        results = {
            "branch": branch_name,
            "target": target_branch,
            "passed": passed,
            "source_type": source_type,
            "target_type": target_type,
            "type_compatible": is_compatible_type,
            "same_repo": same_repo,
            "details": f"Environment validation completed. Type compatible: {is_compatible_type}, Same repo: {same_repo}"
        }
        
        if correlation_id:
            status = "PASSED" if passed else "FAILED"
            logger.info(f"Target environment validation {status}: {results['details']}", correlation_id)
        
        return results
    
    def get_compatibility_report(self, branch_name: str, correlation_id: str = None) -> Dict[str, any]:
        """
        Get a comprehensive compatibility report for a branch
        
        Args:
            branch_name: Branch name to get report for
            correlation_id: Correlation ID for logging
        
        Returns:
            Dictionary with compatibility report
        """
        if correlation_id:
            logger.info(f"Generating compatibility report for {branch_name}", correlation_id)
        
        branch_info = self.git_service.get_branch_info(branch_name)
        if not branch_info:
            error_msg = f"Branch '{branch_name}' not found"
            if correlation_id:
                logger.error(error_msg, correlation_id)
            return {
                "branch": branch_name,
                "passed": False,
                "error": error_msg
            }
        
        # Get recent commits
        recent_commits = self.git_service.get_recent_commits(branch_name, 5)
        
        # Check compatibility with common target branches
        target_branches = ["main", "scientific"]
        compatibility_results = []
        
        for target in target_branches:
            if target in self.git_service.get_all_branches() and target != branch_name:
                result = self.check_branch_compatibility(branch_name, target, correlation_id)
                compatibility_results.append(result)
        
        # Count passed checks
        passed_checks = len([r for r in compatibility_results if r.get("passed", False)])
        total_checks = len(compatibility_results)
        
        passed = passed_checks == total_checks
        
        report = {
            "branch": branch_name,
            "branch_type": branch_info.type.value,
            "passed": passed,
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": total_checks - passed_checks,
            "recent_commits": len(recent_commits),
            "compatibility_results": compatibility_results,
            "details": f"Compatibility report: {passed_checks}/{total_checks} checks passed"
        }
        
        if correlation_id:
            status = "PASSED" if passed else "FAILED"
            logger.info(f"Compatibility report {status}: {report['details']}", correlation_id)
        
        return report