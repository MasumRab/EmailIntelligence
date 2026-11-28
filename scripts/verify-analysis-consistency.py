#!/usr/bin/env python3
"""
Analysis Documents Consistency Verifier

Verifies that analysis documents are consistent and critical issues are resolved.
Run this script to check for drift or issues in the analysis documentation.
"""

import json
import sys
from pathlib import Path


def check_conflict_markers():
    """Check for conflict markers in key files."""
    issues = []
    launch_py = Path("setup/launch.py")

    if launch_py.exists():
        content = launch_py.read_text()
        if "<<<<<<< HEAD" in content and "=======" in content:
            # Check if it's a string literal or actual conflict
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                if (
                    line.strip().startswith("<<<<<<<")
                    and "conflict_markers" not in line
                ):
                    issues.append(
                        f"CRITICAL: setup/launch.py has conflict marker at line {i}"
                    )

    return issues


def check_claude_md_tracked():
    """Verify CLAUDE.md is tracked in git."""
    import subprocess

    issues = []

    result = subprocess.run(
        ["git", "ls-files", "CLAUDE.md"], capture_output=True, text=True
    )

    if result.returncode != 0 or not result.stdout.strip():
        issues.append("CRITICAL: CLAUDE.md is not tracked in git")

    return issues


def check_metrics_consistency():
    """Verify metrics are consistent across documents."""
    issues = []
    metrics_file = Path("docs/analysis/PROJECT_METRICS.json")

    if metrics_file.exists():
        try:
            data = json.loads(metrics_file.read_text())
            health = data.get("health", {}).get("overall", 0)
            if health != 62:
                issues.append(
                    f"WARN: PROJECT_METRICS.json health is {health}, expected 62"
                )
        except json.JSONDecodeError:
            issues.append("ERROR: PROJECT_METRICS.json is not valid JSON")
    else:
        issues.append("WARN: PROJECT_METRICS.json not found")

    return issues


def check_gitignore_claude():
    """Verify CLAUDE.md is not in .gitignore."""
    issues = []
    gitignore = Path(".gitignore")

    if gitignore.exists():
        content = gitignore.read_text()
        for i, line in enumerate(content.split("\n"), 1):
            if line.strip() == "CLAUDE.md" and not line.strip().startswith("#"):
                issues.append(
                    f"CRITICAL: CLAUDE.md is gitignored at .gitignore line {i}"
                )

    return issues


def main():
    """Run all checks and report results."""
    print("=" * 60)
    print("Analysis Documents Consistency Verifier")
    print("=" * 60)
    print()

    all_issues = []

    # Run checks
    print("Checking for conflict markers...")
    all_issues.extend(check_conflict_markers())

    print("Checking CLAUDE.md tracking...")
    all_issues.extend(check_claude_md_tracked())

    print("Checking metrics consistency...")
    all_issues.extend(check_metrics_consistency())

    print("Checking .gitignore...")
    all_issues.extend(check_gitignore_claude())

    print()

    # Report results
    if all_issues:
        print("ISSUES FOUND:")
        print("-" * 40)
        for issue in all_issues:
            print(f"  {'❌' if 'CRITICAL' in issue else '⚠️'} {issue}")
        print()
        print("=" * 60)
        print("VERIFICATION FAILED")
        print("=" * 60)
        return 1
    else:
        print("✅ All checks passed - analysis documents verified")
        print()
        print("=" * 60)
        print("VERIFICATION SUCCESSFUL")
        print("=" * 60)
        return 0


if __name__ == "__main__":
    sys.exit(main())
