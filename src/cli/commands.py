"""
CLI commands module.
"""

import warnings
from typing import Optional

from ..git.worktree import WorktreeManager
from ..git.conflict_detector import GitConflictDetector
from ..analysis.constitutional.analyzer import ConstitutionalAnalyzer
from ..strategy.generator import StrategyGenerator
from ..resolution.auto_resolver import AutoResolver
from ..validation.validator import ValidationOrchestrator
from ..utils.logger import get_logger

logger = get_logger(__name__)


class CLICommands:
    """
    Handlers for CLI commands.

    DEPRECATED: This class is deprecated and will be removed in a future version.
    Use the new modular command system instead:
    from src.cli.commands.integration import create_registry
    """

    def __init__(self):
        warnings.warn(
            "CLICommands is deprecated and will be removed in a future version. "
            "Use the new modular command system instead: "
            "from src.cli.commands.integration import create_registry",
            DeprecationWarning,
            stacklevel=3,
        )
        self.worktree_manager = WorktreeManager()
        self.conflict_detector = GitConflictDetector()
        self.analyzer = ConstitutionalAnalyzer()
        self.strategy_generator = StrategyGenerator()
        self.resolver = AutoResolver()
        self.validator = ValidationOrchestrator()

    async def analyze(
        self,
        repo_path: str,
        pr_id: Optional[str] = None,
        base_branch: Optional[str] = None,
        head_branch: Optional[str] = None,
    ):
        """
        Analyze conflicts in the repository.
        """
        from ..git.repository import RepositoryOperations
        from pathlib import Path

        print(f"Analyzing repository at {repo_path}...")

        # Initialize repository operations
        repo = RepositoryOperations(Path(repo_path))

        # Determine branches to compare
        try:
            # If no base branch specified, default to 'main'
            if not base_branch:
                base_branch = "main"
                logger.info("Using default base branch", branch=base_branch)

            # If no head branch specified, use current branch
            if not head_branch:
                head_branch = await repo.get_current_branch()
                logger.info("Using current branch as head", branch=head_branch)

            # Validate branches exist
            try:
                await repo.get_commit_sha(base_branch)
            except Exception as e:
                logger.error("Base branch not found", branch=base_branch, error=str(e))
                print(f"Error: Base branch '{base_branch}' not found in repository")
                return

            try:
                await repo.get_commit_sha(head_branch)
            except Exception as e:
                logger.error("Head branch not found", branch=head_branch, error=str(e))
                print(f"Error: Head branch '{head_branch}' not found in repository")
                return

            print(f"Comparing branches: {base_branch} <- {head_branch}")

        except Exception as e:
            logger.error("Failed to determine branches", error=str(e))
            print(f"Error: Failed to determine branches: {e}")
            return

        # 1. Detect conflicts
        conflicts = await self.conflict_detector.detect_conflicts_between_branches(
            head_branch, base_branch
        )
        if not conflicts:
            print("No conflicts detected.")
            return

        print(f"Found {len(conflicts)} conflicts.")

        for conflict in conflicts:
            # 2. Analyze conflict
            analysis = await self.analyzer.analyze(conflict)
            print(
                f"Conflict {conflict.id}: Risk={analysis.risk_level.value}, Score={analysis.complexity_score}"
            )

            # 3. Generate strategies
            strategies = await self.strategy_generator.generate_strategies(
                conflict, analysis
            )
            print(f"Generated {len(strategies)} strategies.")
            for strat in strategies:
                print(f"  - {strat.name} ({strat.type}): {strat.description}")

    async def resolve(self, conflict_id: str, strategy_id: str):
        """
        Resolve a specific conflict.
        """
        print(f"Resolving conflict {conflict_id} with strategy {strategy_id}...")
        # Implementation would look up conflict/strategy and call resolver
        pass

    async def validate(self):
        """
        Run validation checks.
        """
        print("Running validation...")
        results = await self.validator.validate({"files": []})
        for res in results:
            print(f"[{res.status.value}] {res.component}: {res.score}")

    async def analyze_history(self, branch: str, output: Optional[str] = None):
        """
        Analyze git history.
        """
        from ..git.history import GitHistory
        from ..analysis.commits import CommitClassifier

        print(f"Analyzing history for branch: {branch}...")
        history = GitHistory()
        classifier = CommitClassifier()

        commits = await history.get_commits(branch, limit=500)
        stats = classifier.analyze_history(commits)

        report = f"Analysis Report for {branch}\n"
        report += f"Total Commits: {stats['total']}\n\n"
        report += "By Category:\n"
        for cat, count in stats["by_category"].items():
            report += f"  - {cat}: {count}\n"

        report += "\nBy Risk:\n"
        for risk, count in stats["by_risk"].items():
            report += f"  - {risk}: {count}\n"

        print(report)

        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"Report saved to {output}")

    async def plan_rebase(self, branch: str, output: str):
        """
        Generate rebase plan.
        """
        from ..git.history import GitHistory
        from ..analysis.commits import CommitClassifier
        from ..strategy.reordering import RebasePlanner

        print(f"Planning rebase for branch: {branch}...")
        history = GitHistory()
        classifier = CommitClassifier()
        planner = RebasePlanner()

        commits = await history.get_commits(branch, limit=500)
        # Classify all
        for c in commits:
            classifier.classify(c)

        plan = planner.generate_plan(commits)

        with open(output, "w", encoding="utf-8") as f:
            f.write(plan)
        print(f"Rebase plan saved to {output}")
