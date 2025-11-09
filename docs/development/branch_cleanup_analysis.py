#!/usr/bin/env python3
"""
Branch Cleanup Analysis Script
Identifies branches that are safe to delete based on merge status, age, and content analysis
"""

import subprocess
from datetime import datetime
from typing import Dict


def run_git_command(cmd: str) -> str:
    """Run a git command and return output"""
    result = subprocess.run(cmd.split(), capture_output=True, text=True, cwd=".")
    return result.stdout.strip()


def get_branch_details(branch: str) -> Dict:
    """Get detailed information about a branch for deletion analysis"""
    info = {
        "name": branch,
        "is_merged": False,
        "age_days": 0,
        "commit_count": 0,
        "last_author": "",
        "last_date": "",
        "is_backup": False,
        "is_duplicate": False,
        "has_recent_commits": False,
        "safety_score": 0,  # 0-100, higher = safer to delete
        "deletion_reason": "",
        "risk_level": "unknown",  # low, medium, high
    }

    try:
        # Check if merged
        merged_cmd = f"git branch --contains {branch} main 2>/dev/null || git branch --contains {branch} scientific 2>/dev/null"
        merged_output = run_git_command(merged_cmd)
        info["is_merged"] = bool(merged_output.strip())

        # Get commit info
        log_cmd = f"git log -1 --format='%an|%ad|%s' --date=iso {branch} 2>/dev/null"
        log_output = run_git_command(log_cmd)
        if log_output and "|" in log_output:
            parts = log_output.split("|", 2)
            if len(parts) >= 3:
                info["last_author"] = parts[0]
                date_str = parts[1].split(" ")[0]  # Get date part only
                try:
                    commit_date = datetime.fromisoformat(date_str)
                    info["age_days"] = (datetime.now() - commit_date).days
                    info["last_date"] = date_str
                    info["has_recent_commits"] = info["age_days"] <= 30
                except:
                    info["age_days"] = 999

        # Get commit count
        count_cmd = f"git rev-list --count {branch} 2>/dev/null"
        count_output = run_git_command(count_cmd)
        info["commit_count"] = int(count_output) if count_output.isdigit() else 0

        # Analyze branch name for patterns
        name_lower = branch.lower()

        # Check for backup patterns
        if any(
            pattern in name_lower
            for pattern in ["backup", "archive", "old", "deprecated"]
        ):
            info["is_backup"] = True

        # Check for duplicate patterns
        if any(
            pattern in name_lower
            for pattern in ["copy", "duplicate", "temp", "test-", "-test"]
        ):
            info["is_duplicate"] = True

        # Calculate safety score
        score = 0

        # High safety factors
        if info["is_merged"]:
            score += 40
        if info["age_days"] > 90:  # Older than 3 months
            score += 30
        if info["is_backup"]:
            score += 20
        if info["is_duplicate"]:
            score += 15
        if info["commit_count"] < 10:  # Very small branches
            score += 10

        # Risk factors (reduce score)
        if not info["is_merged"] and info["commit_count"] > 100:
            score -= 30  # Large unmerged branches are risky
        if info["has_recent_commits"]:
            score -= 20  # Recent branches might still be active
        if "main" in name_lower or "master" in name_lower:
            score -= 50  # Never delete main branches
        if "scientific" in name_lower:
            score -= 50  # Current development branch

        info["safety_score"] = max(0, min(100, score))

        # Determine risk level
        if score >= 70:
            info["risk_level"] = "low"
            info["deletion_reason"] = "Safe to delete - merged, old, or backup branch"
        elif score >= 40:
            info["risk_level"] = "medium"
            info["deletion_reason"] = "Consider deletion - evaluate content first"
        else:
            info["risk_level"] = "high"
            info["deletion_reason"] = "High risk - may contain unique work"

    except Exception as e:
        print(f"Error analyzing branch {branch}: {e}")
        info["deletion_reason"] = f"Analysis error: {e}"

    return info


def analyze_deletable_branches():
    """Main analysis function for branch cleanup"""
    print("🧹 Analyzing Branches for Safe Deletion...\n")

    # Get all local branches except current
    current_branch = run_git_command("git branch --show-current")
    all_branches_output = run_git_command("git branch")
    branches = []

    for line in all_branches_output.split("\n"):
        branch = line.strip().lstrip("* ")
        if branch and branch != current_branch and not branch.startswith("remotes/"):
            branches.append(branch)

    print(f"Analyzing {len(branches)} branches for deletion safety...\n")

    # Analyze each branch
    branch_analysis = []
    for branch in branches:
        print(f"Analyzing: {branch}")
        analysis = get_branch_details(branch)
        branch_analysis.append(analysis)

    # Sort by safety score (highest first = safest to delete)
    branch_analysis.sort(key=lambda x: x["safety_score"], reverse=True)

    # Categorize branches
    safe_to_delete = [b for b in branch_analysis if b["safety_score"] >= 70]
    consider_deletion = [b for b in branch_analysis if 40 <= b["safety_score"] < 70]
    high_risk = [b for b in branch_analysis if b["safety_score"] < 40]

    # Display results
    print("\n" + "=" * 100)
    print("🗑️  BRANCH CLEANUP ANALYSIS RESULTS")
    print("=" * 100)

    def print_branch_section(title, branches, color_code):
        print(f"\n{color_code}{title} ({len(branches)} branches)")
        print("-" * 60)
        if not branches:
            print("None found")
            return

        for branch in branches[:10]:  # Show top 10
            status = "✅ MERGED" if branch["is_merged"] else "❌ UNMERGED"
            age = f"{branch['age_days']}d ago"
            commits = branch["commit_count"]
            score = branch["safety_score"]

            print(f"  {branch['name']}")
            print(
                f"    Status: {status} | Age: {age} | Commits: {commits} | Safety: {score}%"
            )
            print(f"    Reason: {branch['deletion_reason']}")
            print()

        if len(branches) > 10:
            print(f"  ... and {len(branches) - 10} more branches")

    print_branch_section("🟢 SAFE TO DELETE", safe_to_delete, "")
    print_branch_section("🟡 CONSIDER DELETION", consider_deletion, "")
    print_branch_section("🔴 HIGH RISK - DO NOT DELETE", high_risk, "")

    # Summary statistics
    print("\n" + "=" * 100)
    print("📊 DELETION ANALYSIS SUMMARY")
    print("=" * 100)

    total = len(branch_analysis)
    safe_count = len(safe_to_delete)
    consider_count = len(consider_deletion)
    risk_count = len(high_risk)

    print(f"Total Branches Analyzed: {total}")
    print(f"Safe to Delete: {safe_count} ({safe_count / total * 100:.1f}%)")
    print(f"Consider Deletion: {consider_count} ({consider_count / total * 100:.1f}%)")
    print(f"High Risk: {risk_count} ({risk_count / total * 100:.1f}%)")

    # Age distribution of safe branches
    if safe_to_delete:
        old_branches = sum(1 for b in safe_to_delete if b["age_days"] > 90)
        merged_branches = sum(1 for b in safe_to_delete if b["is_merged"])
        backup_branches = sum(1 for b in safe_to_delete if b["is_backup"])

        print("\nSafe Branch Breakdown:")
        print(f"  Old (>90 days): {old_branches}")
        print(f"  Already merged: {merged_branches}")
        print(f"  Backup branches: {backup_branches}")

    # Generate cleanup script
    print("\n🛠️  CLEANUP SCRIPT GENERATED")
    print("-" * 40)
    print("# Safe branches to delete:")
    for branch in safe_to_delete[:5]:  # Show first 5 as examples
        print(
            f"# git branch -D {branch['name']}  # {branch['deletion_reason'][:50]}..."
        )

    print("\n# Consider deletion (review first):")
    for branch in consider_deletion[:3]:
        print(f"# git branch -D {branch['name']}  # Review before deletion")

    print("\n# High risk - DO NOT DELETE:")
    for branch in high_risk[:3]:
        print(f"# KEEP: {branch['name']}  # {branch['risk_level']} risk")


if __name__ == "__main__":
    analyze_deletable_branches()
