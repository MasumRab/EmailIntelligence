"""
Analyze History Command Module

Implements the analyze-history command for git history analysis and lost work recovery.
Unified implementation of pattern detection and dangling commit recovery.
"""

from argparse import Namespace
import subprocess
from pathlib import Path
from typing import Any, Dict

from ..interface import Command


class AnalyzeHistoryCommand(Command):
    """
    Command for analyzing git commit history and recovering lost work.

    This command parses git logs to identify patterns and uses git fsck
    to discover unreachable commits that may contain valuable source code.
    """

    @property
    def name(self) -> str:
        return "analyze-history"

    @property
    def description(self) -> str:
        return "Analyze git commit history and recover lost work"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--branch", default="HEAD", help="Branch to analyze (default: HEAD)"
        )
        parser.add_argument(
            "--limit", type=int, default=500, help="Max commits to analyze"
        )
        parser.add_argument(
            "--lost-found", 
            action="store_true", 
            help="Scan for dangling/unreachable commits containing source code"
        )
        parser.add_argument("--output", help="Output file for report")

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {
            "history": "GitHistory",
            "classifier": "CommitClassifier",
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Set command dependencies."""
        self._history = dependencies.get("history")
        self._classifier = dependencies.get("classifier")

    async def execute(self, args: Namespace) -> int:
        """Execute the analyze-history command."""
        # 1. Handle Lost & Found mode
        if args.lost_found:
            return await self._scan_lost_found()

        # 2. Standard History Analysis
        try:
            branch = args.branch or "HEAD"
            print(f"Analyzing history for branch: {branch}...")

            if not self._history or not self._classifier:
                print("Warning: History services not injected. Running basic log.")
                subprocess.run(["git", "log", "-n", str(args.limit), "--oneline", branch])
                return 0

            commits = await self._history.get_commits(branch, limit=args.limit)
            if not commits:
                print("No commits found.")
                return 0

            stats = self._classifier.analyze_history(commits)
            report = self._build_report(branch, stats)
            print(f"\n{report}")

            if args.output:
                Path(args.output).write_text(report, encoding='utf-8')
                print(f"Report saved to {args.output}")

            return 0
        except Exception as e:
            print(f"Error during history analysis: {e}")
            return 1

    def _build_report(self, branch: str, stats: Dict) -> str:
        lines = [f"Analysis Report for {branch}", f"Total Commits: {stats.get('total', 0)}", ""]
        lines.append("By Category:")
        for cat, count in stats.get("by_category", {}).items():
            lines.append(f"  - {cat}: {count}")
        lines.append("\nBy Risk:")
        for risk, count in stats.get("by_risk", {}).items():
            lines.append(f"  - {risk}: {count}")
        return "\n".join(lines)

    # --- Lost & Found Logic (Ported DNA) ---

    async def _scan_lost_found(self) -> int:
        """Ported logic to find dangling source code commits."""
        print("🔍 SCANNING FOR UNREACHABLE COMMITS (git fsck)...")
        try:
            result = subprocess.run(
                ["git", "fsck", "--unreachable", "--no-reflogs"],
                capture_output=True, text=True
            )
            dangling = [line.split()[2] for line in result.stdout.splitlines() if "unreachable commit" in line]
            if not dangling:
                print("No unreachable commits found.")
                return 0

            found_count = 0
            for sha in dangling:
                files = subprocess.run(["git", "show", "--name-only", "--format=", sha], capture_output=True, text=True).stdout
                if any(p in files for p in ["src/", "backend/", "client/", "conductor/"]):
                    msg = subprocess.run(["git", "show", "--no-patch", "--format=%%B", sha], capture_output=True, text=True).stdout.strip()
                    print(f"\n📦 FOUND LOST WORK: {sha}\n   Message: {msg[:80]}...")
                    found_count += 1
            print(f"\n✅ Scan complete. Identified {found_count} potential recovery targets.")
            return 0
        except Exception as e:
            print(f"Error during recovery scan: {e}"); return 1
