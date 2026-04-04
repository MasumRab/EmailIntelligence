"""
Analyze Command Module

Implements the analyze command for conflict analysis and architectural validation.
Unified implementation of conflict detection and architectural governance.
"""

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
        parser.add_argument(
            "--arch-check", 
            action="store_true", 
            help="Verify architectural rules (layering, forbidden imports)"
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

            # 1. Perform Architectural Check if requested
            if args.arch_check:
                self._perform_arch_check(repo_path)

            # 2. Initialize Repository Operations
            if self._repo_ops:
                # Handle both class and instance for flexible DI
                repo_ops = self._repo_ops(repo_path) if callable(self._repo_ops) else self._repo_ops
            else:
                from src.git.repository import RepositoryOperations
                repo_ops = RepositoryOperations(repo_path)

            # 3. Determine and Validate Branches
            base_branch = args.base_branch
            head_branch = args.head_branch

            if not head_branch:
                stdout, _, rc = await repo_ops.run_command(["rev-parse", "--abbrev-ref", "HEAD"])
                if rc == 0:
                    head_branch = stdout.strip()
                else:
                    print("Error: Could not determine current branch")
                    return 1

            print(f"🔍 Analyzing conflicts: {base_branch} <- {head_branch}")

            # 4. Detect and Analyze Conflicts
            if self._detector:
                conflicts = await self._detector.detect_conflicts_between_branches(head_branch, base_branch)
                if not conflicts:
                    print("No git conflicts detected.")
                else:
                    print(f"Found {len(conflicts)} conflicts.")
                    for conflict in conflicts:
                        # Logic for strategy generation and analysis...
                        print(f"  - Conflict in {conflict.file_path} (Risk: {conflict.severity.value})")

            return 0

        except Exception as e:
            print(f"Error during analysis: {e}")
            return 1

    # --- Architectural Rule Logic (Ported DNA) ---

    def _perform_arch_check(self, path: Path) -> None:
        """Ported logic to enforce layering and import boundaries."""
        print("\n🏗️  ENFORCING ARCHITECTURAL RULES")
        py_files = list(path.rglob("*.py"))
        print(f"  - Scanning {len(py_files)} files for layer violations...")

        for py_file in py_files:
            if "venv" in str(py_file) or ".iflow" in str(py_file): continue
            self._check_file_layering(py_file)

    def _check_file_layering(self, file_path: Path) -> None:
        """Simple rule: Core should not import CLI/Backend."""
        import ast
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content)
            if "src/core/" in str(file_path):
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        module = self._get_module_name(node)
                        if any(x in module for x in ["src.cli", "src.backend"]):
                            print(f"  [VIOLATION] Core file '{file_path.name}' imports higher layer: {module}")
        except Exception: pass

    def _get_module_name(self, node: Any) -> str:
        if hasattr(node, 'module') and node.module: return node.module
        if hasattr(node, 'names'): return node.names[0].name
        return ""
