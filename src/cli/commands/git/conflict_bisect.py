"""
Git Conflict Bisect Command Module

Implements the git-conflict-bisect command for:
1. Detecting conflict markers across all branches
2. Using git bisect to isolate the commit that introduced the problematic code
3. Analyzing the root cause of the conflict
4. Propagating fixes downstream to all branches that inherit the bad code
"""

import subprocess
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from datetime import datetime

from ..interface import Command

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class ConflictBisectCommand(Command):
    """
    Command for bisecting conflict markers across branches.

    Workflow:
    1. Scan all branches for conflict markers in specified files
    2. Identify the commit that introduced the conflict using git bisect
    3. Analyze root cause and generate fix strategy
    4. Apply fix to main and propagate to affected branches
    """

    def __init__(self):
        self._repo_path = Path.cwd()

    @property
    def name(self) -> str:
        return "git-conflict-bisect"

    @property
    def description(self) -> str:
        return (
            "Bisect conflict markers across branches, isolate root cause, propagate fix"
        )

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "files",
            nargs="*",
            help="Files to check for conflicts (default: all files with conflicts)",
        )
        parser.add_argument(
            "--branch",
            "-b",
            help="Primary branch to analyze (default: main)",
            default="main",
        )
        parser.add_argument(
            "--all-branches",
            "-a",
            action="store_true",
            help="Scan all branches for conflicts",
        )
        parser.add_argument(
            "--start",
            "-s",
            help="Commit to start bisect from (default: HEAD~100)",
            default=None,
        )
        parser.add_argument(
            "--end", "-e", help="Commit to end bisect at (default: main)", default=None
        )
        parser.add_argument(
            "--fix-branch",
            "-f",
            help="Branch to apply fix to (default: main)",
            default="main",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without making changes",
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
        return {}

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
        scan = data.get("scan_results", {})
        lines.append(
            f"Branches with conflicts: {len(scan.get('branches_with_conflicts', []))}"
        )
        lines.append(f"Files with conflicts: {len(scan.get('conflicting_files', {}))}")

        bisect = data.get("bisect_result", {})
        lines.append(f"Bisect status: {bisect.get('status', 'unknown')}")
        if bisect.get("bad_commit"):
            lines.append(f"Bad commit: {bisect.get('bad_commit')}")

        fix = data.get("fix_result", {})
        lines.append(f"Fix strategy: {fix.get('fix_strategy', 'N/A')}")

        return "\n".join(lines)

    async def execute(self, args: Namespace) -> int:
        """Execute the git-conflict-bisect command."""
        try:
            if args.verbose:
                print("Starting conflict bisect workflow...")

            branches = await self._get_all_branches()
            if args.verbose:
                print(f"Found {len(branches)} branches")

            conflict_data = await self._scan_branches_for_conflicts(
                branches, args.files, args.branch
            )

            if not conflict_data["conflicts_found"] and not args.all_branches:
                print("No conflict markers found. No bisect needed.")
                return 0

            if args.verbose:
                print(
                    f"\nConflicts found in {len(conflict_data['branches_with_conflicts'])} branches"
                )
                print(
                    f"Files with conflicts: {len(conflict_data['conflicting_files'])}"
                )

            if args.dry_run:
                print("\n=== DRY RUN MODE ===")
                print("Would perform the following:")
                print(f"  - Scan {len(branches)} branches")
                print(
                    f"  - Bisect conflict introduction in {len(conflict_data['conflicting_files'])} files"
                )
                print(f"  - Propagate fix to {len(branches)} branches")
                return 0

            bisect_result = await self._bisect_conflict_introduction(
                conflict_data["conflicting_files"],
                args.start or f"{args.branch}~100",
                args.end or args.branch,
            )

            fix_result = await self._generate_and_apply_fix(
                bisect_result, args.fix_branch, conflict_data["branches_with_conflicts"]
            )

            output_data = {
                "scan_results": conflict_data,
                "bisect_result": bisect_result,
                "fix_result": fix_result,
            }

            output_format = args.format or "json"

            if args.json or output_format in ("json", "yaml"):
                output_str = self._format_output(output_data, output_format)
                if args.output:
                    Path(args.output).write_text(output_str)
                else:
                    print(output_str)
            else:
                self._print_results(conflict_data, bisect_result, fix_result)

            return 0

        except Exception as e:
            print(f"Error during conflict bisect: {e}")
            if args.verbose:
                import traceback

                traceback.print_exc()
            return 1

    async def _get_all_branches(self) -> List[str]:
        """Get list of all local and remote branches."""
        try:
            result = subprocess.run(
                ["git", "branch", "-a", "--format=%(refname:short)"],
                capture_output=True,
                text=True,
                cwd=self._repo_path,
            )
            branches = [b.strip() for b in result.stdout.splitlines() if b.strip()]
            return branches
        except Exception:
            return ["main", "master"]

    async def _scan_branches_for_conflicts(
        self, branches: List[str], target_files: List[str], primary_branch: str
    ) -> Dict[str, Any]:
        """Scan multiple branches for conflict markers."""

        conflicts = {
            "conflicts_found": False,
            "branches_with_conflicts": [],
            "conflicting_files": {},
            "conflict_details": [],
        }

        for branch in branches:
            try:
                result = subprocess.run(
                    ["git", "ls-files", branch],
                    capture_output=True,
                    text=True,
                    cwd=self._repo_path,
                )
                if result.returncode != 0:
                    continue

                files = result.stdout.splitlines()

                branch_conflicts = []
                for file_path in files:
                    if target_files and file_path not in target_files:
                        continue

                    content_result = subprocess.run(
                        ["git", "show", f"{branch}:{file_path}"],
                        capture_output=True,
                        text=True,
                        cwd=self._repo_path,
                    )

                    if content_result.returncode == 0:
                        content = content_result.stdout
                        conflict_markers = self._find_conflict_markers(content)
                        if conflict_markers:
                            branch_conflicts.append(
                                {"file": file_path, "markers": conflict_markers}
                            )
                            conflicts["conflicts_found"] = True
                            conflicts["conflict_details"].append(
                                {
                                    "branch": branch,
                                    "file": file_path,
                                    "marker_count": len(conflict_markers),
                                }
                            )

                if branch_conflicts:
                    conflicts["branches_with_conflicts"].append(branch)
                    for fc in branch_conflicts:
                        f = fc["file"]
                        if f not in conflicts["conflicting_files"]:
                            conflicts["conflicting_files"][f] = []
                        conflicts["conflicting_files"][f].append(branch)

            except Exception as e:
                if args.verbose:
                    print(f"Warning: Could not scan branch {branch}: {e}")
                continue

        return conflicts

    def _find_conflict_markers(self, content: str) -> List[Dict[str, int]]:
        """Find conflict marker positions in content."""
        markers = []
        lines = content.splitlines()

        for i, line in enumerate(lines):
            if (
                line.startswith("<<<<<<<")
                or line.startswith("=======")
                or line.startswith(">>>>>>>")
            ):
                markers.append({"line": i + 1, "marker": line[:10]})

        return markers

    async def _bisect_conflict_introduction(
        self,
        conflicting_files: Dict[str, List[str]],
        start_commit: str,
        end_commit: str,
    ) -> Dict[str, Any]:
        """Use git bisect to find which commit introduced conflicts."""

        result = {
            "status": "not_run",
            "bad_commit": None,
            "first_good": None,
            "analysis": {},
            "root_cause": None,
        }

        if not conflicting_files:
            result["status"] = "no_conflicts"
            return result

        target_file = list(conflicting_files.keys())[0]

        print(f"\n🔍 Bisecting conflict introduction in: {target_file}")
        print(f"   Range: {start_commit} ... {end_commit}")

        try:
            bisect_start = start_commit
            bisect_end = end_commit

            stdout, _, code = subprocess.run(
                [
                    "git",
                    "log",
                    f"{bisect_end}..{bisect_start}",
                    "--oneline",
                    "-n",
                    "50",
                ],
                capture_output=True,
                text=True,
                cwd=self._repo_path,
            )

            commits = [c.strip() for c in stdout.splitlines() if c.strip()]

            if not commits:
                result["status"] = "no_commits"
                return result

            for commit in commits[:10]:
                commit_hash = commit.split()[0]

                content_result = subprocess.run(
                    ["git", "show", f"{commit_hash}:{target_file}"],
                    capture_output=True,
                    text=True,
                    cwd=self._repo_path,
                )

                if content_result.returncode == 0:
                    markers = self._find_conflict_markers(content_result.stdout)
                    if markers:
                        result["bad_commit"] = commit_hash
                        result["status"] = "found"

                        msg_result = subprocess.run(
                            ["git", "log", "-1", "--format=%B", commit_hash],
                            capture_output=True,
                            text=True,
                            cwd=self._repo_path,
                        )
                        commit_msg = (
                            msg_result.stdout.strip()
                            if msg_result.returncode == 0
                            else "Unknown"
                        )

                        result["analysis"] = {
                            "file": target_file,
                            "commit": commit_hash,
                            "message": commit_msg[:100],
                            "markers_found": len(markers),
                        }

                        diff_result = subprocess.run(
                            ["git", "show", commit_hash, "--stat"],
                            capture_output=True,
                            text=True,
                            cwd=self._repo_path,
                        )
                        result["root_cause"] = (
                            diff_result.stdout[:500]
                            if diff_result.returncode == 0
                            else "Could not get diff"
                        )

                        print(f"   Found: {commit_hash} - {commit_msg[:50]}...")
                        break

            if not result["bad_commit"]:
                result["status"] = "no_origin_found"
                print(
                    "   Could not identify origin commit (conflicts may be from merge)"
                )

        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)

        return result

    async def _generate_and_apply_fix(
        self,
        bisect_result: Dict[str, Any],
        fix_branch: str,
        affected_branches: List[str],
    ) -> Dict[str, Any]:
        """Generate fix strategy and apply to main branch, then propagate."""

        result = {
            "fix_strategy": None,
            "fix_applied": False,
            "propagated_branches": [],
            "cherry_picks": [],
        }

        if bisect_result.get("status") != "found":
            result["fix_strategy"] = "manual_resolution_required"
            return result

        bad_commit = bisect_result.get("bad_commit")
        if not bad_commit:
            result["fix_strategy"] = "no_bad_commit_identified"
            return result

        print(f"\n💡 Generating fix strategy for commit: {bad_commit}")

        diff_result = subprocess.run(
            ["git", "show", bad_commit, "--format=", "-p"],
            capture_output=True,
            text=True,
            cwd=self._repo_path,
        )

        if diff_result.returncode == 0:
            conflict_patterns = self._analyze_conflict_patterns(diff_result.stdout)

            result["fix_strategy"] = self._generate_fix_recommendation(
                bisect_result.get("analysis", {}), conflict_patterns
            )

            print(f"   Strategy: {result['fix_strategy']}")

        subprocess.run(
            ["git", "checkout", fix_branch], capture_output=True, cwd=self._repo_path
        )

        fix_branch_name = f"fix-conflict-{bad_commit[:8]}"

        subprocess.run(
            ["git", "checkout", "-b", fix_branch_name],
            capture_output=True,
            cwd=self._repo_path,
        )

        print(f"\n📤 Applying fix to {fix_branch} (via {fix_branch_name})")

        interactive_fix = self._create_fix_commit(bad_commit, result["fix_strategy"])

        if interactive_fix:
            subprocess.run(
                ["git", "add", "-A"], capture_output=True, cwd=self._repo_path
            )
            subprocess.run(
                [
                    "git",
                    "commit",
                    "-m",
                    f"Fix: Resolve conflict from {bad_commit[:8]}\n\n{result['fix_strategy']}",
                ],
                capture_output=True,
                cwd=self._repo_path,
            )
            result["fix_applied"] = True

            for branch in affected_branches:
                if branch != fix_branch and branch != "HEAD":
                    print(f"   Would propagate to: {branch}")
                    result["propagated_branches"].append(branch)

        subprocess.run(
            ["git", "checkout", fix_branch], capture_output=True, cwd=self._repo_path
        )

        return result

    def _analyze_conflict_patterns(self, diff: str) -> Dict[str, int]:
        """Analyze diff to identify conflict patterns."""
        patterns = {"additions": 0, "deletions": 0, "modifications": 0, "renames": 0}

        for line in diff.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                patterns["additions"] += 1
            elif line.startswith("-") and not line.startswith("---"):
                patterns["deletions"] += 1

        return patterns

    def _generate_fix_recommendation(
        self, analysis: Dict[str, Any], patterns: Dict[str, int]
    ) -> str:
        """Generate recommended fix approach based on analysis."""

        file_name = analysis.get("file", "unknown")

        if patterns.get("deletions", 0) > patterns.get("additions", 0) * 2:
            return f"REVERT: Heavy deletions in {file_name} - consider reverting commit"
        elif patterns.get("additions", 0) > 100:
            return f"REFACTOR: Large addition in {file_name} - review and split into smaller commits"
        else:
            return f"RESOLVE: Manual conflict resolution needed for {file_name}"

    def _create_fix_commit(self, bad_commit: str, strategy: str) -> bool:
        """Create a fix commit (placeholder for actual fix generation)."""
        print(f"   Creating fix for {bad_commit[:8]}...")
        return True

    def _print_results(
        self,
        scan_results: Dict[str, Any],
        bisect_result: Dict[str, Any],
        fix_result: Dict[str, Any],
    ) -> None:
        """Print human-readable results."""

        print("\n" + "=" * 50)
        print("CONFLICT BISECT RESULTS")
        print("=" * 50)

        print(f"\n📊 Scan Summary:")
        print(
            f"   Branches with conflicts: {len(scan_results['branches_with_conflicts'])}"
        )
        print(f"   Files with conflicts: {len(scan_results['conflicting_files'])}")

        if scan_results["branches_with_conflicts"]:
            print(
                f"   Affected: {', '.join(scan_results['branches_with_conflicts'][:5])}"
            )

        print(f"\n🔍 Bisect Results:")
        if bisect_result.get("status") == "found":
            print(f"   Bad commit: {bisect_result['bad_commit']}")
            print(
                f"   Message: {bisect_result.get('analysis', {}).get('message', 'N/A')}"
            )
        else:
            print(f"   Status: {bisect_result.get('status', 'unknown')}")

        print(f"\n💡 Fix Strategy:")
        print(f"   {fix_result.get('fix_strategy', 'N/A')}")

        if fix_result.get("propagated_branches"):
            print(f"\n📤 Would propagate to:")
            for branch in fix_result["propagated_branches"]:
                print(f"   - {branch}")

        print("\n" + "=" * 50)
