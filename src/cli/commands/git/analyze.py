"""
Analyze Command Module

Implements the analyze command for conflict analysis and architectural validation.
Unified implementation of conflict detection and architectural governance.
"""

import sys
import subprocess
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict

from ..interface import Command


class AnalyzeCommand(Command):
    """
    Command for analyzing repository conflicts between branches.

    This command detects conflicts, analyzes them for complexity,
    and generates resolution strategies. Includes architectural layering validation.
    """

    @property
    def name(self) -> str:
        return "git-analyze"

    @property
    def description(self) -> str:
        return "Analyze repository conflicts and verify architectural integrity"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "repo_path", help="Path to the repository", nargs="?", default="."
        )
        parser.add_argument(
            "revision_range",
            nargs="?",
            help="Commit range (e.g., 'HEAD~5..HEAD', branch name)",
        )
        parser.add_argument("--pr", dest="pr_id", help="Pull Request ID (optional)")
        parser.add_argument(
            "--base-branch",
            default="main",
            help="Base branch for conflict detection (default: main)",
        )
        parser.add_argument(
            "--head-branch",
            help="Head branch for conflict detection (default: current branch)",
        )
        parser.add_argument(
            "--arch-check",
            action="store_true",
            help="Verify architectural rules (layering, forbidden imports)",
        )
        parser.add_argument(
            "--report",
            action="store_true",
            help="Generate a full IntentReport for the entire branch",
        )
        parser.add_argument(
            "--output-file", type=str, help="Path to save output (JSON format)"
        )
        parser.add_argument("--json", action="store_true", help="Output in JSON format")
        parser.add_argument(
            "--verbose", "-v", action="store_true", help="Enable verbose output"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {
            "conflict_detector": "GitConflictDetector",
            "analyzer": "ConstitutionalAnalyzer",
            "strategy_generator": "StrategyGenerator",
            "repository_ops": "RepositoryOperations",
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Set command dependencies."""
        self._detector = dependencies.get("conflict_detector")
        self._analyzer = dependencies.get("analyzer")
        self._strategy_gen = dependencies.get("strategy_generator")
        self._repo_ops = dependencies.get("repository_ops")

    async def execute(self, args: Namespace) -> int:
        """Execute the analyze command."""
        try:
            repo_path = Path(args.repo_path)
            if not repo_path.exists():
                print(f"Error: Repository path does not exist: {args.repo_path}")
                return 1

            # Handle AnalysisService-based analysis (from main_old.py legacy)
            if hasattr(args, "report") and args.report:
                return await self._execute_full_report(args, repo_path)

            # Handle basic conflict analysis
            return await self._execute_conflict_analysis(args, repo_path)

        except Exception as e:
            print(f"Error during analysis: {e}")
            return 1

    async def _execute_full_report(self, args: Namespace, repo_path: Path) -> int:
        """Execute full IntentReport generation (legacy main_old.py feature)."""
        import asyncio
        import json
        from datetime import datetime

        # Try to use AnalysisService if available
        try:
            from src.services.analysis_service import AnalysisService

            analysis_service = AnalysisService(str(repo_path))

            # Get branch name
            current_branch = await self._get_current_branch(repo_path)

            # Generate IntentReport
            revision_range = getattr(args, "revision_range", None)
            intent_report = await analysis_service.generate_intent_report(
                branch_name=current_branch, revision_range=revision_range
            )

            output_data = intent_report.to_dict()

            if args.output_file:
                with open(args.output_file, "w") as f:
                    json.dump(output_data, f, indent=4)
                print(f"Analysis report saved to {args.output_file}")
            else:
                # Human-readable output
                print(
                    f"Intent Report for branch '{intent_report.branch_name}' (Generated at {intent_report.generated_at.isoformat()}):"
                )
                for narrative in intent_report.commit_narratives:
                    print(f"\n--- Commit: {narrative.commit_hexsha[:7]} ---")
                    print(f"Author: {narrative.author_name}")
                    print(
                        f"Date: {datetime.fromtimestamp(narrative.authored_date).isoformat()}"
                    )
                    print(
                        f"Message: {narrative.commit_message.strip().splitlines()[0]}"
                    )
                    print(f"Narrative: {narrative.synthesized_narrative}")
                    if not narrative.is_consistent:
                        print(
                            f"Consistency: NOT CONSISTENT - {narrative.discrepancy_notes}"
                        )
                print("\nAnalysis complete.")

            return 0

        except ImportError as e:
            print(f"AnalysisService not available: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error generating report: {e}", file=sys.stderr)
            return 1

    async def _execute_conflict_analysis(self, args: Namespace, repo_path: Path) -> int:
        """Execute basic conflict detection analysis."""

        # 1. Perform Architectural Check if requested
        if args.arch_check:
            self._perform_arch_check(repo_path)

        # 2. Determine and Validate Branches
        base_branch = args.base_branch
        head_branch = args.head_branch

        if not head_branch:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                head_branch = result.stdout.strip()
            else:
                print("Error: Could not determine current branch")
                return 1

        print(f"🔍 Analyzing conflicts: {base_branch} <- {head_branch}")

        # 3. Detect and Analyze Conflicts
        if self._detector:
            conflicts = await self._detector.detect_conflicts_between_branches(
                head_branch, base_branch
            )
            if not conflicts:
                print("No git conflicts detected.")
            else:
                print(f"Found {len(conflicts)} conflicts.")
                for conflict in conflicts:
                    print(
                        f"  - Conflict in {conflict.file_path} (Risk: {conflict.severity.value})"
                    )

        return 0

    async def _get_current_branch(self, repo_path: Path) -> str:
        """Get current branch name."""
        import subprocess

        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() if result.returncode == 0 else "unknown"

    # --- Architectural Rule Logic (Ported DNA) ---

    def _perform_arch_check(self, path: Path) -> None:
        """Ported logic to enforce layering and import boundaries."""
        print("\n🏗️  ENFORCING ARCHITECTURAL RULES")
        py_files = list(path.rglob("*.py"))
        print(f"  - Scanning {len(py_files)} files for layer violations...")

        for py_file in py_files:
            if "venv" in str(py_file) or ".iflow" in str(py_file):
                continue
            self._check_file_layering(py_file)

    def _check_file_layering(self, file_path: Path) -> None:
        """Simple rule: Core should not import CLI/Backend."""
        import ast

        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content)
            if "src/core/" in str(file_path):
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        module = self._get_module_name(node)
                        if any(x in module for x in ["src.cli", "src.backend"]):
                            print(
                                f"  [VIOLATION] Core file '{file_path.name}' imports higher layer: {module}"
                            )
        except Exception:
            pass

    def _get_module_name(self, node: Any) -> str:
        if hasattr(node, "module") and node.module:
            return node.module
        if hasattr(node, "names"):
            return node.names[0].name
        return ""
