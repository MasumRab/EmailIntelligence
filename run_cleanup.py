#!/usr/bin/env python3
"""
Simple branch cleanup script using the branch cleanup scaffold
"""

import json
import sys
import os

# Add the scripts directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts', 'branch_cleanup'))

from cleanup_manager import BranchCleanupManager
from safety_checker import SafetyChecker
from rollback_manager import RollbackManager

def main():
    repo_path = "."
    
    # Create manager
    manager = BranchCleanupManager(repo_path)
    
    # Create checkpoint first
    rollback_manager = RollbackManager(repo_path)
    checkpoint_id = rollback_manager.create_checkpoint(
        "Before Branch Cleanup",
        "Systematic cleanup of old branches"
    )
    print(f"✅ Created checkpoint: {checkpoint_id}")
    
    # Define branches to clean up based on our analysis
    branches_to_cleanup = [
        {
            "name": "temp-for-orchestration-changes",
            "status": "temporary",
            "priority": "low",
            "reason": "Temporary branch for orchestration changes",
            "commits_ahead": 76,
            "last_commit": "2025-11-10",
            "metadata": {}
        },
        {
            "name": "align-feature-notmuch-tagging-1-v2",
            "status": "stale",
            "priority": "low",
            "reason": "Old feature branch, superseded",
            "commits_ahead": 152,
            "last_commit": "2025-11-06",
            "metadata": {}
        },
        {
            "name": "cleanup-orchestration-tools",
            "status": "completed",
            "priority": "low",
            "reason": "Cleanup branch no longer needed",
            "commits_ahead": 35,
            "last_commit": "2025-11-05",
            "metadata": {}
        },
        {
            "name": "recover-lost-commit",
            "status": "temporary",
            "priority": "low",
            "reason": "Temporary recovery branch",
            "commits_ahead": 12,
            "last_commit": "2025-11-04",
            "metadata": {}
        },
        {
            "name": "orchestration-tools-changes",
            "status": "superseded",
            "priority": "low",
            "reason": "Superseded by main orchestration-tools branch",
            "commits_ahead": 92,
            "last_commit": "2025-11-11",
            "metadata": {}
        }
    ]
    
    # Create cleanup plan
    plan_id = manager.create_cleanup_plan(
        name="Systematic Branch Cleanup",
        description="Clean up temporary, stale, and superseded branches",
        branch_data=branches_to_cleanup
    )
    print(f"✅ Created cleanup plan: {plan_id}")
    
    # Review plan
    review_passed, issues = manager.review_plan(plan_id)
    
    if review_passed:
        print("✅ Plan passed safety review")
        
        # Execute plan
        if manager.execute_plan(plan_id, auto_approve=True):
            print("✅ Plan executed successfully")
            
            # Generate report
            report_path = manager.generate_report(plan_id)
            print(f"📊 Report generated: {report_path}")
            
        else:
            print("❌ Plan execution failed")
            sys.exit(1)
    else:
        print("❌ Plan has issues:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)

if __name__ == "__main__":
    main()