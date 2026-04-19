#!/usr/bin/env python3
"""
Branch Health Analysis Command

Analyzes the health of Git branches by checking for:
- Merge conflict markers
- Unresolved TODO/FIXME comments
- Build/test failures in recent commits
- Commit message quality issues
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any


class BranchHealthCommand:
    """
    Command to analyze Git branch health and identify potential issues.
    """

    def __init__(self, path: str, branch: Optional[str] = None):
        self.repo_path = Path(path).resolve()
        self.branch = branch
        self.issues: List[Dict[str, Any]] = []

    def _run_git(self, args: List[str]) -> str:
        """Run a git command and return output."""
        result = subprocess.run(
            ["git"] + args,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout.strip()

    def _check_conflict_markers(self) -> None:
        """Check for unresolved merge conflict markers."""
        markers = ["<<<<<<<", "=======", ">>>>>>>"]
        for marker in markers:
            output = self._run_git([
                "grep", "-r", f"^{marker}", "--include=*.py", "--include=*.md",
                "--include=*.yml", "--include=*.yaml", "."
            ])
            if output:
                for line in output.split('\n'):
                    if line.strip():
                        self.issues.append({
                            "type": "conflict_marker",
                            "severity": "critical",
                            "message": f"Unresolved conflict marker: {line.strip()}",
                            "file": line.split(':')[0] if ':' in line else "unknown"
                        })

    def _check_todo_comments(self) -> None:
        """Check for unresolved TODO and FIXME comments."""
        output = self._run_git([
            "grep", "-r", "-n", "TODO\\|FIXME\\|XXX\\|HACK",
            "--include=*.py", "--include=*.md", "."
        ])
        if output:
            for line in output.split('\n'):
                if line.strip():
                    parts = line.split(':')
                    self.issues.append({
                        "type": "todo_comment",
                        "severity": "warning",
                        "message": f"Unresolved {line.split()[0]} comment",
                        "file": parts[0] if len(parts) > 0 else "unknown",
                        "line": parts[1] if len(parts) > 1 else "unknown"
                    })

    def _check_build_status(self) -> None:
        """Check for build failures in recent commits."""
        output = self._run_git([
            "log", "--oneline", "-20", "--all", "--grep=build\\|test\\|ci",
            "--grep=fail\\|error", "--oneline"
        ])
        if output:
            self.issues.append({
                "type": "build_issues",
                "severity": "error",
                "message": "Recent build/test failures detected",
                "details": output[:500]
            })

    def _check_commit_quality(self) -> None:
        """Check for commit message quality issues."""
        output = self._run_git([
            "log", "--oneline", "-10", "--format=%s"
        ])
        if output:
            for commit_msg in output.split('\n'):
                if len(commit_msg.split()) < 3:
                    self.issues.append({
                        "type": "commit_message",
                        "severity": "warning",
                        "message": "Vague commit message",
                        "commit": commit_msg[:50]
                    })

    def _check_unmerged_files(self) -> None:
        """Check for files in merge state."""
        unmerged = self._run_git(["status", "--porcelain"])
        if "UU" in unmerged:  # Both modified but not merged
            self.issues.append({
                "type": "unmerged_files",
                "severity": "critical",
                "message": "Files with merge conflicts detected",
                "count": unmerged.count("UU")
            })

    def analyze(self) -> Dict[str, Any]:
        """
        Perform comprehensive branch health analysis.
        
        Returns:
            Dict containing health score and detailed issues
        """
        self._check_conflict_markers()
        self._check_todo_comments()
        self._check_build_status()
        self._check_commit_quality()
        self._check_unmerged_files()

        # Calculate health score (lower is better - represents issues)
        critical_issues = sum(1 for i in self.issues if i["severity"] == "critical")
        warning_issues = sum(1 for i in self.issues if i["severity"] == "warning")
        
        health_score = (critical_issues * 10) + warning_issues
        
        return {
            "branch": self.branch or self._run_git(["branch", "--show-current"]),
            "health_score": health_score,
            "critical_issues": critical_issues,
            "warning_issues": warning_issues,
            "issues": self.issues,
            "status": "healthy" if health_score == 0 else "needs_attention"
        }

    def print_report(self) -> None:
        """Print the branch health report to console."""
        result = self.analyze()
        
        print("\n" + "=" * 60)
        print(f"BRANCH HEALTH REPORT: {result['branch']}")
        print("=" * 60)
        print(f"Health Score: {result['health_score']} ({result['status'].upper()})")
        print(f"Critical Issues: {result['critical_issues']}")
        print(f"Warning Issues: {result['warning_issues']}")
        print()

        if result["issues"]:
            print("🔴 ISSUES FOUND:")
            for i, issue in enumerate(result["issues"], 1):
                severity_icon = "🔴" if issue["severity"] == "critical" else "🟡"
                print(f"\n{i}. {severity_icon} [{issue['type']}] {issue['message']}")
                if "file" in issue:
                    print(f"   File: {issue['file']}")
                if "line" in issue:
                    print(f"   Line: {issue['line']}")
                if "details" in issue:
                    print(f"   Details: {issue['details'][:200]}...")
        else:
            print("✅ No issues found. Branch is healthy!")

        print("=" * 60 + "\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze Git branch health")
    parser.add_argument("--path", "-p", default=".", help="Path to repository")
    parser.add_argument("--branch", "-b", default=None, help="Branch to analyze (default: current)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--post-resolution", action="store_true", help="Run post-resolution checks")
    
    args = parser.parse_args()
    
    cmd = BranchHealthCommand(args.path, args.branch)
    
    if args.json:
        result = cmd.analyze()
        import json
        print(json.dumps(result, indent=2))
    elif args.post_resolution:
        cmd.print_report()
    else:
        cmd.print_report()
