#!/usr/bin/env python3
"""
optimal_rebase_planner.py - Calculate optimal branch rebase ordering to minimize conflicts

Analyzes branch dependencies and change overlap to determine the safest rebase sequence.
This prevents cascading merge conflicts by rebasing branches in dependency order.

Usage:
    python3 optimal_rebase_planner.py [--base-branch main] [--branches branch1,branch2,...]

Example:
    python3 optimal_rebase_planner.py
    python3 optimal_rebase_planner.py --base-branch main --branches scientific,orchestration-tools
"""

import subprocess
import json
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, deque


@dataclass
class BranchInfo:
    """Information about a branch"""
    name: str
    commit_count: int
    files_changed: int
    authors: int
    last_commit: str
    days_old: int
    depends_on: List[str]  # Branches this branch depends on


@dataclass
class ChangeOverlap:
    """Overlap analysis between two branches"""
    branch_a: str
    branch_b: str
    files_overlap: int
    total_files_a: int
    total_files_b: int
    overlap_percent: float
    conflict_risk: str  # LOW, MEDIUM, HIGH, CRITICAL


@dataclass
class RebaseOrder:
    """Recommended rebase order"""
    order: List[str]
    rationale: List[str]
    risk_level: str  # LOW, MEDIUM, HIGH
    estimated_conflicts: int
    safe_parallel_groups: List[List[str]]  # Branches that can be rebased in parallel


class RebaseAnalyzer:
    """Analyzes branches to determine optimal rebase order"""

    def __init__(self, base_branch: str = "main"):
        self.base_branch = base_branch
        self.branches: Dict[str, BranchInfo] = {}
        self.overlaps: List[ChangeOverlap] = []
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)

    def run_git_command(self, cmd: str) -> str:
        """Run git command safely"""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=30
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            print(f"⚠️  Command timed out: {cmd}")
            return ""
        except Exception as e:
            print(f"❌ Error running command: {e}")
            return ""

    def get_all_branches(self) -> List[str]:
        """Get all local and remote branches (excluding base)"""
        output = self.run_git_command(
            "git branch -a | grep -v HEAD | sed 's/^[* ]*//' | sed 's/^remotes\\/origin\\///'"
        )
        branches = [b.strip() for b in output.split('\n') if b.strip() and b.strip() != self.base_branch]
        # Remove duplicates (local and remote same branch)
        return list(set(branches))

    def get_branch_info(self, branch: str) -> Optional[BranchInfo]:
        """Get detailed info about a branch"""
        try:
            # Commit count since base
            commit_count = len(self.run_git_command(
                f"git log {self.base_branch}..{branch} --oneline"
            ).split('\n'))

            # Files changed
            files_changed = len(self.run_git_command(
                f"git diff {self.base_branch}..{branch} --name-only"
            ).split('\n'))

            # Number of authors
            authors = len(set(self.run_git_command(
                f"git log {self.base_branch}..{branch} --format='%an'"
            ).split('\n')))

            # Last commit message
            last_commit = self.run_git_command(
                f"git log {branch} -1 --format='%s'"
            )

            # Days since last commit
            last_commit_time = self.run_git_command(
                f"git log {branch} -1 --format='%at'"
            )
            import time
            days_old = (int(time.time()) - int(last_commit_time)) // 86400 if last_commit_time else 0

            return BranchInfo(
                name=branch,
                commit_count=commit_count if commit_count > 0 else 1,
                files_changed=files_changed,
                authors=authors,
                last_commit=last_commit[:50],
                days_old=days_old,
                depends_on=[]  # Will be filled by dependency analysis
            )
        except Exception as e:
            print(f"⚠️  Error getting info for {branch}: {e}")
            return None

    def analyze_file_overlap(self, branch_a: str, branch_b: str) -> ChangeOverlap:
        """Analyze file overlap between two branches"""
        try:
            files_a = set(self.run_git_command(
                f"git diff {self.base_branch}..{branch_a} --name-only"
            ).split('\n'))

            files_b = set(self.run_git_command(
                f"git diff {self.base_branch}..{branch_b} --name-only"
            ).split('\n'))

            files_a = {f for f in files_a if f}
            files_b = {f for f in files_b if f}

            overlap = len(files_a & files_b)
            total = len(files_a | files_b)
            overlap_percent = (overlap / total * 100) if total > 0 else 0

            # Determine conflict risk
            if overlap_percent == 0:
                risk = "LOW"
            elif overlap_percent < 20:
                risk = "LOW"
            elif overlap_percent < 50:
                risk = "MEDIUM"
            elif overlap_percent < 75:
                risk = "HIGH"
            else:
                risk = "CRITICAL"

            return ChangeOverlap(
                branch_a=branch_a,
                branch_b=branch_b,
                files_overlap=overlap,
                total_files_a=len(files_a),
                total_files_b=len(files_b),
                overlap_percent=overlap_percent,
                conflict_risk=risk
            )
        except Exception as e:
            print(f"⚠️  Error analyzing overlap: {e}")
            return ChangeOverlap(branch_a, branch_b, 0, 0, 0, 0, "UNKNOWN")

    def detect_dependencies(self) -> Dict[str, Set[str]]:
        """Detect branch dependencies based on merge-base analysis"""
        dependencies: Dict[str, Set[str]] = defaultdict(set)

        for branch in self.branches:
            for other_branch in self.branches:
                if branch == other_branch:
                    continue

                # Check if branch's commits include other_branch's commits
                common = self.run_git_command(
                    f"git merge-base {branch} {other_branch}"
                )
                branch_commit = self.run_git_command(f"git rev-parse {branch}")
                other_commit = self.run_git_command(f"git rev-parse {other_branch}")

                # If common ancestor is other_branch, then branch depends on other_branch
                if common.strip() == other_commit.strip():
                    dependencies[branch].add(other_branch)

        return dependencies

    def calculate_optimal_order(self) -> RebaseOrder:
        """Calculate optimal rebase order using topological sort"""
        # Build dependency graph
        deps = self.detect_dependencies()

        # Topological sort using Kahn's algorithm
        in_degree = {branch: len(deps.get(branch, set())) for branch in self.branches}
        queue = deque([b for b in self.branches if in_degree[b] == 0])
        order = []
        remaining = set(self.branches)

        while queue:
            current = queue.popleft()
            order.append(current)
            remaining.discard(current)

            # Find branches that depend on current
            for branch in remaining:
                deps[branch].discard(current)
                if len(deps[branch]) == 0:
                    queue.append(branch)

        # Handle cycles by adding remaining
        if remaining:
            # Sort by least conflicting first
            remaining_list = sorted(
                remaining,
                key=lambda b: sum(o.overlap_percent for o in self.overlaps
                                  if (o.branch_a == b or o.branch_b == b))
            )
            order.extend(remaining_list)

        # Identify safe parallel groups (branches with no overlap)
        parallel_groups = self._identify_parallel_groups(order)

        # Calculate risk and conflicts
        total_conflict_risk = sum(
            1 if o.conflict_risk in ["HIGH", "CRITICAL"] else 0
            for o in self.overlaps
        )

        risk_level = "LOW" if total_conflict_risk == 0 else (
            "MEDIUM" if total_conflict_risk < 3 else "HIGH"
        )

        rationale = self._generate_rationale(order)

        return RebaseOrder(
            order=order,
            rationale=rationale,
            risk_level=risk_level,
            estimated_conflicts=total_conflict_risk,
            safe_parallel_groups=parallel_groups
        )

    def _identify_parallel_groups(self, order: List[str]) -> List[List[str]]:
        """Identify groups of branches that can be rebased in parallel"""
        groups = []
        current_group = []

        for i, branch in enumerate(order):
            # Check if branch conflicts with any branch in current group
            conflicts = False
            for other in current_group:
                overlap = next(
                    (o for o in self.overlaps
                     if (o.branch_a == branch and o.branch_b == other) or
                        (o.branch_a == other and o.branch_b == branch)),
                    None
                )
                if overlap and overlap.conflict_risk in ["MEDIUM", "HIGH", "CRITICAL"]:
                    conflicts = True
                    break

            if conflicts or len(current_group) > 2:  # Max 3 parallel
                groups.append(current_group)
                current_group = [branch]
            else:
                current_group.append(branch)

        if current_group:
            groups.append(current_group)

        return groups

    def _generate_rationale(self, order: List[str]) -> List[str]:
        """Generate explanation for recommended order"""
        rationale = []

        for i, branch in enumerate(order, 1):
            info = self.branches[branch]
            rationale.append(
                f"{i}. {branch}: {info.commit_count} commits, "
                f"{info.files_changed} files, {info.days_old}d old"
            )

        return rationale

    def analyze(self, branches: Optional[List[str]] = None) -> RebaseOrder:
        """Run full analysis"""
        # Get branches
        if branches:
            branch_list = branches
        else:
            branch_list = self.get_all_branches()

        if not branch_list:
            print("⚠️  No branches to analyze")
            return RebaseOrder([], [], "UNKNOWN", 0, [])

        print(f"📊 Analyzing {len(branch_list)} branches...")

        # Get branch info
        for branch in branch_list:
            info = self.get_branch_info(branch)
            if info:
                self.branches[branch] = info

        # Analyze overlaps
        for i, branch_a in enumerate(branch_list):
            for branch_b in branch_list[i+1:]:
                overlap = self.analyze_file_overlap(branch_a, branch_b)
                self.overlaps.append(overlap)

        # Calculate optimal order
        return self.calculate_optimal_order()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Calculate optimal branch rebase ordering to minimize conflicts"
    )
    parser.add_argument(
        "--base-branch",
        default="main",
        help="Base branch to rebase onto (default: main)"
    )
    parser.add_argument(
        "--branches",
        help="Comma-separated list of branches to analyze (default: all)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed analysis"
    )

    args = parser.parse_args()

    # Parse branches
    branches = None
    if args.branches:
        branches = [b.strip() for b in args.branches.split(',')]

    # Run analysis
    analyzer = RebaseAnalyzer(base_branch=args.base_branch)
    result = analyzer.analyze(branches)

    # Output results
    if args.json:
        output = {
            "order": result.order,
            "risk_level": result.risk_level,
            "estimated_conflicts": result.estimated_conflicts,
            "parallel_groups": result.safe_parallel_groups,
            "rationale": result.rationale
        }
        print(json.dumps(output, indent=2))
    else:
        print("\n" + "=" * 70)
        print("OPTIMAL BRANCH REBASE ORDER")
        print("=" * 70)

        print(f"\n🎯 Recommended Order (Risk: {result.risk_level}):\n")
        for i, branch in enumerate(result.order, 1):
            info = analyzer.branches.get(branch)
            if info:
                print(f"  {i}. {branch:30s} ({info.commit_count:3d} commits, "
                      f"{info.files_changed:3d} files)")

        print(f"\n📋 Rationale:")
        for line in result.rationale:
            print(f"  {line}")

        print(f"\n⚡ Parallel Groups (can rebase concurrently):")
        for i, group in enumerate(result.safe_parallel_groups, 1):
            print(f"  Group {i}: {', '.join(group)}")

        print(f"\n⚠️  Estimated Conflicts: {result.estimated_conflicts}")
        print(f"   Risk Level: {result.risk_level}")

        if analyzer.overlaps:
            print(f"\n📊 Change Overlaps (by risk):\n")
            overlaps_sorted = sorted(analyzer.overlaps, 
                                    key=lambda x: {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(x.conflict_risk, 0),
                                    reverse=True)
            for overlap in overlaps_sorted[:10]:  # Top 10
                emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(overlap.conflict_risk, "⚪")
                print(f"  {emoji} {overlap.branch_a} ↔ {overlap.branch_b}: "
                      f"{overlap.overlap_percent:.0f}% overlap ({overlap.files_overlap} files)")

        print("\n" + "=" * 70)
        print("RECOMMENDED REBASE SEQUENCE:")
        print("=" * 70 + "\n")
        
        for branch in result.order:
            print(f"git rebase {args.base_branch} {branch}")

        print("\n# Or in parallel (if in same group):")
        for group in result.safe_parallel_groups:
            if len(group) > 1:
                print(f"# {' & '.join(group)}")

        print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
