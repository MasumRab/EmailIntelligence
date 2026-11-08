#!/usr/bin/env python3
"""
Branch Cleanup CLI

Command-line interface for branch cleanup operations.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

from cleanup_manager import BranchCleanupManager


def load_branch_data(filepath: str) -> List[Dict[str, Any]]:
    """Load branch analysis data from file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def cmd_analyze(args):
    """Analyze branches and create cleanup plan."""
    manager = BranchCleanupManager(args.repo_path)
    
    # Load branch data
    branch_data = load_branch_data(args.input)
    
    # Create cleanup plan
    plan_id = manager.create_cleanup_plan(
        name=args.name,
        description=args.description or "Automated cleanup plan",
        branch_data=branch_data
    )
    
    print(f"Created cleanup plan: {plan_id}")
    
    # Review plan
    if args.review:
        review_passed, issues = manager.review_plan(plan_id)
        
        if review_passed:
            print("✅ Plan passed safety review")
        else:
            print("❌ Plan has issues:")
            for issue in issues:
                print(f"  - {issue}")
    
    # Generate report
    report_path = manager.generate_report(plan_id, args.format)
    print(f"Report generated: {report_path}")
    
    # Execute if requested
    if args.execute:
        if manager.execute_plan(plan_id, args.auto_approve):
            print("✅ Plan executed successfully")
        else:
            print("❌ Plan execution failed")
            sys.exit(1)


def cmd_plan(args):
    """List cleanup plans."""
    manager = BranchCleanupManager(args.repo_path)
    plans = manager.list_plans()
    
    if not plans:
        print("No cleanup plans found")
        return
    
    print("Cleanup Plans:")
    print("-" * 80)
    for plan in plans:
        status_emoji = "✅" if plan["status"] == "completed" else "⏳" if plan["status"] == "executing" else "📋"
        print(f"{status_emoji} {plan['plan_id']}: {plan['name']}")
        print(f"   Status: {plan['status']}")
        print(f"   Operations: {plan['operations_count']}")
        print(f"   Created: {plan['created_at']}")
        print(f"   Reviewed: {plan['reviewed']}")
        print(f"   Executed: {plan['executed']}")
        print()


def cmd_execute(args):
    """Execute a cleanup plan."""
    manager = BranchCleanupManager(args.repo_path)
    
    if manager.execute_plan(args.plan_id, args.auto_approve):
        print(f"✅ Plan {args.plan_id} executed successfully")
        
        # Generate report
        report_path = manager.generate_report(args.plan_id, args.format)
        print(f"Report generated: {report_path}")
    else:
        print(f"❌ Plan {args.plan_id} execution failed")
        sys.exit(1)


def cmd_review(args):
    """Review a cleanup plan."""
    manager = BranchCleanupManager(args.repo_path)
    
    review_passed, issues = manager.review_plan(args.plan_id)
    
    if review_passed:
        print("✅ Plan passed safety review")
    else:
        print("❌ Plan has issues:")
        for issue in issues:
            print(f"  - {issue}")
        
        if args.strict:
            sys.exit(1)


def cmd_report(args):
    """Generate report for a plan."""
    manager = BranchCleanupManager(args.repo_path)
    
    report_path = manager.generate_report(args.plan_id, args.format)
    print(f"Report generated: {report_path}")


def cmd_rollback(args):
    """Rollback to a checkpoint."""
    manager = RollbackManager(args.repo_path)
    
    if args.create:
        checkpoint_id = manager.create_checkpoint(args.name, args.description or "")
        print(f"Created checkpoint: {checkpoint_id}")
    elif args.list:
        checkpoints = manager.list_checkpoints()
        if not checkpoints:
            print("No checkpoints found")
            return
        
        print("Available Checkpoints:")
        print("-" * 80)
        for checkpoint in checkpoints:
            print(f"📦 {checkpoint['checkpoint_id']}: {checkpoint['name']}")
            print(f"   Created: {checkpoint['created_at']}")
            print(f"   Branches: {checkpoint['branches_count']}")
            print(f"   Tags: {checkpoint['tags_count']}")
            print()
    elif args.rollback:
        if manager.rollback_to_checkpoint(args.rollback):
            print(f"✅ Rolled back to checkpoint: {args.rollback}")
        else:
            print(f"❌ Rollback failed: {args.rollback}")
            sys.exit(1)
    elif args.delete:
        if manager.delete_checkpoint(args.delete):
            print(f"✅ Deleted checkpoint: {args.delete}")
        else:
            print(f"❌ Failed to delete checkpoint: {args.delete}")
            sys.exit(1)


def cmd_safety(args):
    """Run safety checks."""
    checker = SafetyChecker(args.repo_path)
    
    if args.rules:
        rules = checker.get_rule_status()
        print("Safety Rules:")
        print("-" * 60)
        for rule in rules:
            status = "✅" if rule["enabled"] else "❌"
            print(f"{status} {rule['rule_id']}: {rule['name']}")
            print(f"   {rule['description']}")
            print(f"   Severity: {rule['severity']}")
            print()
    elif args.enable:
        if checker.enable_rule(args.enable):
            print(f"✅ Enabled rule: {args.enable}")
        else:
            print(f"❌ Failed to enable rule: {args.enable}")
            sys.exit(1)
    elif args.disable:
        if checker.disable_rule(args.disable):
            print(f"✅ Disabled rule: {args.disable}")
        else:
            print(f"❌ Failed to disable rule: {args.disable}")
            sys.exit(1)


def cmd_validate(args):
    """Validate branch for safety."""
    checker = SafetyChecker(args.repo_path)
    
    if checker.quick_sanity_check(args.branch):
        print(f"✅ Branch '{args.branch}' passed sanity check")
    else:
        print(f"❌ Branch '{args.branch}' failed sanity check")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Branch Cleanup Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze branches and create plan
  branch-cleanup analyze branches.json --name "Weekly Cleanup" --review

  # List all plans
  branch-cleanup plan

  # Execute a plan
  branch-cleanup execute plan_1234567890

  # Create rollback checkpoint
  branch-cleanup rollback --create "Before Cleanup"

  # Rollback to checkpoint
  branch-cleanup rollback --rollback checkpoint_1234567890

  # Run safety check on branch
  branch-cleanup validate feature-old-branch
        """
    )
    
    parser.add_argument(
        "--repo-path",
        default=".",
        help="Repository path (default: current directory)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze branches and create cleanup plan")
    analyze_parser.add_argument("input", help="Branch analysis JSON file")
    analyze_parser.add_argument("--name", required=True, help="Plan name")
    analyze_parser.add_argument("--description", help="Plan description")
    analyze_parser.add_argument("--review", action="store_true", help="Run safety review")
    analyze_parser.add_argument("--execute", action="store_true", help="Execute plan after creation")
    analyze_parser.add_argument("--auto-approve", action="store_true", help="Auto-approve execution")
    analyze_parser.add_argument("--format", choices=["html", "json", "text"], default="html", help="Report format")
    
    # Plan command
    plan_parser = subparsers.add_parser("plan", help="List cleanup plans")
    
    # Execute command
    execute_parser = subparsers.add_parser("execute", help="Execute cleanup plan")
    execute_parser.add_argument("plan_id", help="Plan ID to execute")
    execute_parser.add_argument("--auto-approve", action="store_true", help="Auto-approve execution")
    execute_parser.add_argument("--format", choices=["html", "json", "text"], default="html", help="Report format")
    
    # Review command
    review_parser = subparsers.add_parser("review", help="Review cleanup plan")
    review_parser.add_argument("plan_id", help="Plan ID to review")
    review_parser.add_argument("--strict", action="store_true", help="Exit on any issues")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate report for plan")
    report_parser.add_argument("plan_id", help="Plan ID")
    report_parser.add_argument("--format", choices=["html", "json", "text"], default="html", help="Report format")
    
    # Rollback command
    rollback_parser = subparsers.add_parser("rollback", help="Manage rollback checkpoints")
    rollback_group = rollback_parser.add_mutually_exclusive_group(required=True)
    rollback_group.add_argument("--create", metavar="NAME", help="Create checkpoint")
    rollback_group.add_argument("--list", action="store_true", help="List checkpoints")
    rollback_group.add_argument("--rollback", metavar="ID", help="Rollback to checkpoint")
    rollback_group.add_argument("--delete", metavar="ID", help="Delete checkpoint")
    rollback_parser.add_argument("--description", help="Checkpoint description")
    
    # Safety command
    safety_parser = subparsers.add_parser("safety", help="Manage safety rules")
    safety_group = safety_parser.add_mutually_exclusive_group(required=True)
    safety_group.add_argument("--rules", action="store_true", help="List safety rules")
    safety_group.add_argument("--enable", metavar="RULE_ID", help="Enable safety rule")
    safety_group.add_argument("--disable", metavar="RULE_ID", help="Disable safety rule")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate branch safety")
    validate_parser.add_argument("branch", help="Branch name to validate")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Route to appropriate command
    if args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "plan":
        cmd_plan(args)
    elif args.command == "execute":
        cmd_execute(args)
    elif args.command == "review":
        cmd_review(args)
    elif args.command == "report":
        cmd_report(args)
    elif args.command == "rollback":
        cmd_rollback(args)
    elif args.command == "safety":
        cmd_safety(args)
    elif args.command == "validate":
        cmd_validate(args)


if __name__ == "__main__":
    main()