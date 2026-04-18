"""
Git Conflicts Command Module

Implements the git-conflicts command for standalone conflict detection with complexity scoring.
"""

from argparse import Namespace
from typing import Any, Dict, List
from pathlib import Path

from ..interface import Command

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class GitConflictsCommand(Command):
    """
    Command for detecting and analyzing conflicts in the repository.

    This command wraps GitConflictDetector to provide standalone conflict
    detection with complexity scoring to help developers prioritize resolution.
    """

    def __init__(self):
        self._detector = None

    @property
    def name(self) -> str:
        return "git-conflicts"

    @property
    def description(self) -> str:
        return "Detect and rank merge conflicts by complexity"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--path",
            "-p",
            help="Specific file or directory to check for conflicts",
            default=None,
        )
        parser.add_argument(
            "--severity",
            action="store_true",
            help="Show severity level for each conflict",
        )
        parser.add_argument(
            "--json", action="store_true", help="Output results in JSON format"
        )
        parser.add_argument(
            "--verbose", "-v", action="store_true", help="Enable verbose output"
        )
        parser.add_argument(
            "--output",
            "-o",
            help="Output file path (default: stdout)",
            default=None,
        )
        parser.add_argument(
            "--format",
            "-f",
            choices=["json", "yaml", "text"],
            default="json",
            help="Output format (default: json)",
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """Return required dependencies."""
        return {"conflict_detector": "GitConflictDetector"}

    def set_dependencies(self, deps: Dict[str, Any]) -> None:
        """Set dependencies for the command."""
        self._detector = deps.get("conflict_detector")

    def _format_output(self, data: dict, output_format: str) -> str:
        """Format output data in the specified format."""
        try:
            import yaml

            YAML_AVAILABLE = True
        except ImportError:
            YAML_AVAILABLE = False

        if output_format == "yaml":
            if YAML_AVAILABLE:
                return yaml.dump(data, default_flow_style=False, sort_keys=False)
            import json

            return json.dumps(data, indent=2)

        if output_format == "text":
            return self._format_text_output(data)

        import json

        return json.dumps(data, indent=2)

    def _format_text_output(self, data: dict) -> str:
        """Format output as plain text."""
        lines = []
        lines.append(f"Total Conflicts: {data.get('total_conflicts', 0)}")
        if data.get("conflicts"):
            lines.append("Conflicts:")
            for c in data.get("conflicts", []):
                lines.append(f"  - {c.get('file', 'unknown')}")
                lines.append(f"    Severity: {c.get('severity', '?')}")
                lines.append(f"    Blocks: {c.get('blocks', 0)}")
        return "\n".join(lines)

    async def execute(self, args: Namespace) -> int:
        """Execute the git-conflicts command."""
        try:
            from src.git.conflict_detector import GitConflictDetector

            repo_path = Path(args.path) if args.path else Path.cwd()

            detector = self._detector or GitConflictDetector(repo_path)

            conflicts = detector.detect_conflicts_in_repo()

            if not conflicts:
                print("No conflicts detected in repository.")
                return 0

            ranked_conflicts = self._rank_by_complexity(conflicts)

            output_data = {
                "total_conflicts": len(ranked_conflicts),
                "conflicts": [
                    {
                        "file": c.file_path,
                        "severity": c.severity.value
                        if hasattr(c, "severity")
                        else "unknown",
                        "type": c.conflict_type.value
                        if hasattr(c, "conflict_type")
                        else "unknown",
                        "blocks": len(c.conflict_blocks) if c.conflict_blocks else 0,
                    }
                    for c in ranked_conflicts
                ],
            }

            output_format = args.format or "json"

            if args.json or output_format in ("json", "yaml"):
                output_str = self._format_output(output_data, output_format)
                if args.output:
                    Path(args.output).write_text(output_str)
                else:
                    print(output_str)
            else:
                self._print_conflicts(ranked_conflicts, args.verbose, args.severity)

            return 0

        except ImportError as e:
            print(f"Error: Required module not available: {e}")
            return 1
        except Exception as e:
            print(f"Error during conflict detection: {e}")
            if hasattr(args, "verbose") and args.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def _rank_by_complexity(self, conflicts: List) -> List:
        """Rank conflicts by complexity (number of blocks + file type)."""

        def complexity_score(conflict):
            block_count = (
                len(conflict.conflict_blocks) if conflict.conflict_blocks else 0
            )

            extension = Path(conflict.file_path).suffix.lower()
            complex_extensions = {".py": 3, ".js": 2, ".ts": 2, ".jsx": 2, ".tsx": 2}
            complexity = complex_extensions.get(extension, 1)

            return block_count * complexity

        return sorted(conflicts, key=complexity_score, reverse=True)

    def _print_conflicts(
        self, conflicts: List, verbose: bool, show_severity: bool
    ) -> None:
        """Print conflicts in a readable format."""
        print(f"\n=== Detected {len(conflicts)} Conflicts ===\n")

        for i, conflict in enumerate(conflicts, 1):
            print(f"{i}. {conflict.file_path}")

            if show_severity and hasattr(conflict, "severity"):
                print(f"   Severity: {conflict.severity.value}")

            if conflict.conflict_blocks:
                print(f"   Conflict blocks: {len(conflict.conflict_blocks)}")

            if hasattr(conflict, "description") and conflict.description:
                print(f"   {conflict.description}")

            if verbose:
                for j, block in enumerate(conflict.conflict_blocks[:3], 1):
                    print(f"     Block {j}: lines {block.start_line}-{block.end_line}")
                if len(conflict.conflict_blocks) > 3:
                    print(
                        f"     ... and {len(conflict.conflict_blocks) - 3} more blocks"
                    )

            print()
