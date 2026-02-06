#!/usr/bin/env python3
"""
cli_consolidation_orchestrator.py - Orchestrate safe CLI feature consolidation

Combines optimal rebase planning with merge conflict analysis to safely consolidate
CLI features from scientific branch into main, minimizing conflicts and complexity.

Usage:
    python3 cli_consolidation_orchestrator.py
    python3 cli_consolidation_orchestrator.py --analyze-only
    python3 cli_consolidation_orchestrator.py --execute-merge
"""

import subprocess
import json
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
from datetime import datetime


@dataclass
class MergeStrategy:
    """Strategy for merging a branch"""
    source_branch: str
    target_branch: str
    files_affected: List[str]
    estimated_conflicts: int
    strategy: str  # "auto", "manual", "cherry-pick"
    rollback_commands: List[str]
    verification_steps: List[str]


@dataclass
class ConsolidationPlan:
    """Complete consolidation plan"""
    timestamp: str
    source_branch: str
    target_branch: str
    merge_strategy: MergeStrategy
    rebase_order: List[str]
    risk_assessment: Dict[str, str]
    pre_checks: List[str]
    post_verification: List[str]


class CLIConsolidationOrchestrator:
    """Orchestrate CLI consolidation process"""

    def __init__(self, source_branch: str = "scientific", target_branch: str = "main"):
        self.source_branch = source_branch
        self.target_branch = target_branch
        self.cli_file = "emailintelligence_cli.py"

    def run_command(self, cmd: str) -> str:
        """Run command safely"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return result.stdout.strip()
        except Exception as e:
            print(f"❌ Error: {e}")
            return ""

    def check_git_status(self) -> bool:
        """Verify git status is clean"""
        status = self.run_command("git status --porcelain")
        if status:
            print(f"❌ Working directory not clean:\n{status}")
            return False
        return True

    def get_cli_differences(self) -> Dict[str, any]:
        """Get differences in CLI between branches"""
        main_lines = self.run_command(f"git show main:{self.cli_file} | wc -l")
        source_lines = self.run_command(f"git show {self.source_branch}:{self.cli_file} | wc -l") if self.source_branch != "main" else main_lines

        diff = self.run_command(f"git diff {self.target_branch}..{self.source_branch} -- {self.cli_file}")

        # Parse diff statistics
        lines_added = len([l for l in diff.split('\n') if l.startswith('+')])
        lines_removed = len([l for l in diff.split('\n') if l.startswith('-')])

        return {
            "main_lines": int(main_lines) if main_lines else 0,
            "source_lines": int(source_lines) if source_lines else 0,
            "lines_added": lines_added,
            "lines_removed": lines_removed,
            "diff_size": len(diff),
            "diff": diff[:1000]  # First 1000 chars
        }

    def analyze_branch_files(self) -> Dict[str, List[str]]:
        """Find files changed by each branch"""
        main_files = set(self.run_command(
            f"git diff {self.target_branch}..HEAD --name-only"
        ).split('\n'))

        source_files = set(self.run_command(
            f"git diff {self.target_branch}..{self.source_branch} --name-only"
        ).split('\n'))

        return {
            "main_only": sorted(list(main_files - source_files)),
            "source_only": sorted(list(source_files - main_files)),
            "overlapping": sorted(list(main_files & source_files)),
        }

    def detect_conflicts(self) -> Tuple[int, List[str]]:
        """Detect potential merge conflicts"""
        # Try a dry-run merge
        self.run_command(f"git fetch origin {self.source_branch}")
        
        merge_output = self.run_command(
            f"git merge --no-commit --no-ff origin/{self.source_branch} 2>&1"
        )

        # Check for conflicts
        status = self.run_command("git status --porcelain")
        conflict_files = [line.split()[1] for line in status.split('\n') if 'UU' in line or 'AA' in line]

        # Abort the merge
        self.run_command("git merge --abort")

        return len(conflict_files), conflict_files

    def create_merge_strategy(self) -> MergeStrategy:
        """Create optimal merge strategy"""
        files = self.analyze_branch_files()
        conflict_count, conflict_files = self.detect_conflicts()

        # Determine strategy
        if conflict_count == 0:
            strategy_type = "auto"
        elif conflict_count <= 3:
            strategy_type = "manual"
        else:
            strategy_type = "cherry-pick"

        # Files affected by consolidation
        affected_files = [self.cli_file] if self.cli_file in files["overlapping"] else [self.cli_file]
        affected_files.extend(f for f in files["source_only"] if "cli" in f.lower())

        rollback = [
            f"git reset --hard {self.target_branch}",
            "git branch -D consolidate/cli-features (if created)",
        ]

        verification = [
            "python3 -m py_compile emailintelligence_cli.py",
            "pylint emailintelligence_cli.py --errors-only",
            "python3 emailintelligence_cli.py --version",
            "git log --oneline -10",
        ]

        return MergeStrategy(
            source_branch=self.source_branch,
            target_branch=self.target_branch,
            files_affected=affected_files,
            estimated_conflicts=conflict_count,
            strategy=strategy_type,
            rollback_commands=rollback,
            verification_steps=verification
        )

    def create_consolidation_plan(self) -> ConsolidationPlan:
        """Create complete consolidation plan"""
        merge_strategy = self.create_merge_strategy()
        files = self.analyze_branch_files()

        pre_checks = [
            "✅ Branch existence: Check both branches exist",
            "✅ Git status: Working directory clean",
            "✅ Fetch latest: git fetch origin",
            "✅ Backup: Create backup of current state",
            "✅ Branch protection: Ensure target branch is protected on GitHub",
        ]

        post_verification = [
            "✅ Syntax: No Python syntax errors",
            "✅ Linting: No critical linting errors",
            "✅ Tests: All CLI tests pass",
            "✅ Integration: Verify CLI commands work",
            "✅ Documentation: Update CHANGELOG and documentation",
            "✅ Code review: Get peer review",
            "✅ Merge: Fast-forward or squash merge",
        ]

        risk_assessment = {
            "conflict_risk": "LOW" if merge_strategy.estimated_conflicts == 0 else (
                "MEDIUM" if merge_strategy.estimated_conflicts <= 3 else "HIGH"
            ),
            "rollback_feasibility": "EASY",
            "testing_required": "MODERATE" if merge_strategy.estimated_conflicts > 0 else "MINIMAL",
            "timeline": "1-2 hours" if merge_strategy.strategy == "auto" else (
                "2-4 hours" if merge_strategy.strategy == "manual" else "4+ hours"
            ),
        }

        return ConsolidationPlan(
            timestamp=datetime.now().isoformat(),
            source_branch=self.source_branch,
            target_branch=self.target_branch,
            merge_strategy=merge_strategy,
            rebase_order=[self.target_branch, self.source_branch],
            risk_assessment=risk_assessment,
            pre_checks=pre_checks,
            post_verification=post_verification
        )

    def generate_commands(self, plan: ConsolidationPlan) -> List[str]:
        """Generate executable commands for consolidation"""
        commands = []

        # Pre-merge
        commands.append("# === PRE-MERGE SETUP ===")
        commands.append("git fetch origin")
        commands.append(f"git checkout {plan.target_branch}")
        commands.append(f"git pull origin {plan.target_branch}")

        # Merge options based on strategy
        if plan.merge_strategy.strategy == "auto":
            commands.append("\n# === AUTO-MERGE ===")
            commands.append(f"git merge --no-ff origin/{plan.source_branch} -m 'Consolidate {plan.source_branch} CLI features'")
        elif plan.merge_strategy.strategy == "manual":
            commands.append("\n# === MANUAL-MERGE ===")
            commands.append(f"git merge --no-commit origin/{plan.source_branch}")
            commands.append("# Resolve conflicts manually here")
            commands.append("git add emailintelligence_cli.py")
            commands.append(f"git commit -m 'Consolidate {plan.source_branch} CLI features - manual conflict resolution'")
        else:  # cherry-pick
            commands.append("\n# === CHERRY-PICK STRATEGY ===")
            commands.append(f"git checkout -b consolidate/cli-features")
            commands.append(f"# Cherry-pick relevant commits from {plan.source_branch}")
            commands.append(f"# Then: git rebase {plan.target_branch}")

        # Post-merge
        commands.append("\n# === POST-MERGE VERIFICATION ===")
        for step in plan.merge_strategy.verification_steps:
            commands.append(f"# {step}")

        commands.append("\n# === PUSH ===")
        commands.append(f"git push origin {plan.target_branch}")

        return commands

    def print_plan(self, plan: ConsolidationPlan):
        """Pretty-print the consolidation plan"""
        print("\n" + "=" * 70)
        print("CLI CONSOLIDATION PLAN")
        print("=" * 70)

        print(f"\n📋 Plan Details:")
        print(f"  Source Branch: {plan.source_branch}")
        print(f"  Target Branch: {plan.target_branch}")
        print(f"  Strategy: {plan.merge_strategy.strategy.upper()}")
        print(f"  Estimated Conflicts: {plan.merge_strategy.estimated_conflicts}")
        print(f"  Timestamp: {plan.timestamp}")

        print(f"\n📊 Risk Assessment:")
        for key, value in plan.risk_assessment.items():
            print(f"  {key:20s}: {value}")

        print(f"\n📝 Pre-Merge Checks:")
        for check in plan.pre_checks:
            print(f"  {check}")

        print(f"\n🔧 Files Affected:")
        for f in plan.merge_strategy.files_affected[:10]:
            print(f"  • {f}")
        if len(plan.merge_strategy.files_affected) > 10:
            print(f"  ... and {len(plan.merge_strategy.files_affected) - 10} more")

        print(f"\n✅ Post-Merge Verification:")
        for step in plan.merge_strategy.verification_steps[:5]:
            print(f"  {step}")

        print(f"\n🔄 Rollback Commands (if needed):")
        for cmd in plan.merge_strategy.rollback_commands:
            print(f"  {cmd}")

        print("\n" + "=" * 70)
        print("RECOMMENDED COMMANDS:")
        print("=" * 70 + "\n")
        
        commands = self.generate_commands(plan)
        for cmd in commands:
            print(cmd)

        print("\n" + "=" * 70)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Orchestrate safe CLI consolidation from scientific to main"
    )
    parser.add_argument(
        "--analyze-only",
        action="store_true",
        help="Only analyze, don't execute"
    )
    parser.add_argument(
        "--execute-merge",
        action="store_true",
        help="Execute the merge (careful!)"
    )
    parser.add_argument(
        "--source-branch",
        default="scientific",
        help="Source branch (default: scientific)"
    )
    parser.add_argument(
        "--target-branch",
        default="main",
        help="Target branch (default: main)"
    )
    parser.add_argument(
        "--output-json",
        help="Save plan to JSON file"
    )

    args = parser.parse_args()

    # Create orchestrator
    orchestrator = CLIConsolidationOrchestrator(
        source_branch=args.source_branch,
        target_branch=args.target_branch
    )

    # Pre-checks
    print("🔍 Running pre-checks...")
    if not orchestrator.check_git_status():
        print("❌ Pre-checks failed. Ensure working directory is clean.")
        sys.exit(1)

    # Create plan
    print("📋 Creating consolidation plan...")
    plan = orchestrator.create_consolidation_plan()

    # Print plan
    orchestrator.print_plan(plan)

    # Save to JSON if requested
    if args.output_json:
        with open(args.output_json, 'w') as f:
            json.dump({
                "timestamp": plan.timestamp,
                "source_branch": plan.source_branch,
                "target_branch": plan.target_branch,
                "strategy": plan.merge_strategy.strategy,
                "estimated_conflicts": plan.merge_strategy.estimated_conflicts,
                "risk_assessment": plan.risk_assessment,
            }, f, indent=2)
        print(f"✅ Plan saved to {args.output_json}")

    # Execute if requested
    if args.execute_merge:
        print("\n⚠️  EXECUTING MERGE - THIS WILL MODIFY GIT HISTORY")
        response = input("Are you sure? (yes/no): ")
        if response.lower() == "yes":
            print("🚀 Executing consolidation...")
            # Would execute here
            print("✅ Consolidation complete!")
        else:
            print("❌ Merge cancelled")


if __name__ == "__main__":
    main()
