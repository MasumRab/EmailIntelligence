"""
Cluster Branches Command Module

Implements two-stage branch identification and clustering using AST and LibCST.
Ported from .taskmaster/archive/task_data_historical/branch_clustering_implementation.py.
"""

import json
import subprocess
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List

from ..interface import Command
from .engine.branch_clustering import ClusterEngine


class ClusterBranchesCommand(Command):
    """
    Command for identifying and clustering Git branches based on similarity.

    Categorizes branches into integration targets (main, scientific, orchestration)
    using structural code analysis (AST), dependency graph (imports), and docstrings.
    """

    def __init__(self):
        self._security_validator = None
        self.engine = None

    @property
    def name(self) -> str:
        return "branch-cluster"

    @property
    def description(self) -> str:
        return "Cluster and categorize Git branches by semantic and structural similarity"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--primary",
            default="origin/main",
            help="Primary branch for comparison"
        )
        parser.add_argument(
            "--mode",
            choices=["identification", "clustering", "hybrid"],
            default="hybrid",
            help="Analysis mode"
        )
        parser.add_argument(
            "--output",
            help="Path to save results as JSON"
        )
        parser.add_argument(
            "--validate",
            help="Path to clustering rules YAML for Natural Language validation"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {
            "security_validator": "SecurityValidator"
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Set command dependencies."""
        self._security_validator = dependencies.get("security_validator")

    def get_dependencies(self) -> Dict[str, Any]:
        return {}

    async def execute(self, args: Namespace) -> int:
        """Execute the branch clustering command."""
        print(f"🔍 Analyzing branches against '{args.primary}' in mode '{args.mode}'...")

        if not self.engine: self.engine = ClusterEngine(repo_path=".", mode=args.mode)

        try:
            # 1. Get list of remote feature branches
            branches = self._get_remote_branches()
            if not branches:
                print("No remote branches found to analyze.")
                return 0

            print(
                f"Found {len(branches)} branches. Performing semantic similarity analysis...")

            # 2. Execute deep clustering engine
            results = {
                "timestamp": Path(".").stat().st_mtime,
                "primary_branch": args.primary,
                "mode": args.mode,
                "assignments": {}
            }

            feature_branches = [
                b for b in branches if b not in [
                    'main',
                    'scientific',
                    'orchestration-tools']]

            assignments = self.engine.execute(feature_branches, args.primary)
            results["assignments"] = assignments

            for branch, data in assignments.items():
                print(
                    f"  - {branch} -> Target: {data['target']} [Conf: {data['confidence']}] [{', '.join(data['tags'])}]")
                print(f"    Reasoning: {data['reasoning']}")

            if args.output:
                output_path = Path(args.output)
                if self._security_validator:
                    is_safe, error = self._security_validator.validate_path_security(
                        str(output_path.absolute()))
                    if not is_safe:
                        print(f"Error: Security violation: {error}")
                        return 1

                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2)
                print(f"\n🚀 Results saved to {args.output}")

            # 3. Natural Language Validation Layer
            if getattr(args, 'validate', None):
                print(
                    f"\n✔️ Running validation against rules: {args.validate}")
                from .engine.validation_framework import Validator
                validator = Validator(args.validate)
                valid = validator.validate(results)
                if not valid:
                    print("❌ Validation failed!")
                    return 1
                print("✅ Validation passed!")

            return 0
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error during clustering: {e}")
            return 1

    def _get_remote_branches(self) -> List[str]:
        """Get list of remote branch names."""
        result = subprocess.run(
            ["git", "branch", "-r"],
            capture_output=True, text=True, check=True
        )
        branches = []
        for line in result.stdout.strip().split("\n"):
            if "->" in line:
                continue
            name = line.strip().replace("origin/", "")
            branches.append(name)
        return branches
