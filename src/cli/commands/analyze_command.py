"""
Analyze Command Module

Implements the analyze command for conflict analysis between branches.
"""

from argparse import Namespace
from pathlib import Path
from typing import Any, Dict

from .interface import Command


class AnalyzeCommand(Command):
    """
    Command for analyzing repository conflicts between branches.

    This command detects conflicts between branches, analyzes them for complexity,
    and generates resolution strategies.
    """

    @property
    def name(self) -> str:
        return "analyze"

    @property
    def description(self) -> str:
        return "Analyze repository conflicts between branches"

    def add_arguments(self, parser: Any) -> None:
        """
        Add command-specific arguments.

        Args:
            parser: ArgumentParser subparser for this command
        """
        parser.add_argument("repo_path", help="Path to the repository")
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

    def get_dependencies(self) -> Dict[str, Any]:
        """
        Get required dependencies for this command.

        Returns:
            Dict mapping dependency names to types
        """
        return {
            "conflict_detector": "GitConflictDetector",
            "analyzer": "ConstitutionalAnalyzer",
            "strategy_generator": "StrategyGenerator",
            "repository_ops": "RepositoryOperations",
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """
        Set command dependencies.

        Args:
            dependencies: Dict of dependency instances
        """
        self._detector = dependencies.get("conflict_detector")
        self._analyzer = dependencies.get("analyzer")
        self._strategy_gen = dependencies.get("strategy_generator")
        self._repo_ops = dependencies.get("repository_ops")

    async def execute(self, args: Namespace) -> int:
        """
        Execute the analyze command.

        Args:
            args: Parsed command-line arguments

        Returns:
            int: Exit code (0 for success, 1 for error)
        """
        try:
            # Validate repository path
            repo_path = Path(args.repo_path)
            if not repo_path.exists():
                print(f"Error: Repository path does not exist: {args.repo_path}")
                return 1

            # Initialize repository operations
            if self._repo_ops:
                self._repo_ops = self._repo_ops(repo_path)
            else:
                from ..git.repository import RepositoryOperations

                self._repo_ops = RepositoryOperations(repo_path)

            # Determine branches
            base_branch = args.base_branch
            head_branch = args.head_branch

            # Get current branch if head_branch not specified
            if not head_branch:
                try:
                    stdout, stderr, rc = await self._repo_ops.run_command(
                        ["rev-parse", "--abbrev-ref", "HEAD"]
                    )
                    if rc == 0:
                        head_branch = stdout.strip()
                    else:
                        print("Error: Could not determine current branch")
                        print(f"Git error: {stderr}")
                        return 1
                except Exception as e:
                    print(f"Error determining current branch: {e}")
                    return 1

            # Validate branches exist
            for branch_name, branch_var in [
                ("base", base_branch),
                ("head", head_branch),
            ]:
                try:
                    stdout, stderr, rc = await self._repo_ops.run_command(
                        ["rev-parse", "--verify", branch_var]
                    )
                    if rc != 0:
                        print(
                            f"Error: {branch_name.title()} branch '{branch_var}' not found"
                        )
                        print(f"Git error: {stderr}")
                        return 1
                except Exception as e:
                    print(f"Error validating {branch_name} branch '{branch_var}': {e}")
                    return 1

            print(f"Analyzing repository at {args.repo_path}...")
            print(f"Comparing branches: {base_branch} <- {head_branch}")

            # Detect conflicts
            try:
                conflicts = await self._detector.detect_conflicts_between_branches(
                    head_branch, base_branch
                )
            except Exception as e:
                print(f"Error detecting conflicts: {e}")
                return 1

            if not conflicts:
                print("No conflicts detected.")
                return 0

            print(f"Found {len(conflicts)} conflicts.")

            # Analyze each conflict
            for conflict in conflicts:
                try:
                    # Analyze conflict complexity
                    analysis = await self._analyzer.analyze_constitutional_compliance(
                        code=f"Conflict in {conflict.file_path}",
                        context={"conflict": conflict},
                    )

                    # Generate resolution strategy
                    strategy = await self._strategy_gen.generate_resolution_strategy(
                        [conflict]
                    )

                    # Print conflict info
                    print(
                        f"Conflict {conflict.id}: "
                        f"Risk={conflict.severity.value}, "
                        f"Score={getattr(analysis, 'compliance_score', 'N/A'):.2f}"
                    )
                    print(
                        f"  Strategy: {getattr(strategy, 'strategy_type', 'unknown')}"
                    )

                    # Show first few steps if available
                    steps = getattr(strategy, "steps", [])
                    for step in steps[:3]:  # Limit to first 3 steps
                        desc = (
                            step.get("description", "Step")
                            if isinstance(step, dict)
                            else str(step)
                        )
                        print(f"    - {desc}")

                except Exception as e:
                    print(f"Error analyzing conflict {conflict.id}: {e}")
                    continue

            return 0

        except Exception as e:
            print(f"Error during analysis: {e}")
            return 1
