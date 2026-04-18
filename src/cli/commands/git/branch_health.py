"""
Branch Health Command Module

Implements the branch-health command for pre-rebase health analysis.
"""

from argparse import Namespace
from typing import Any, Dict, List, Optional
from pathlib import Path

from ..interface import Command

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class BranchHealthCommand(Command):
    """
    Command for analyzing branch health before rebasing.

    This command wraps RebaseAnalyzer to provide health scores and
    risk factors to help developers plan rebase strategies.
    """

    def __init__(self):
        self._analyzer = None
        self._repo_ops = None

    @property
    def name(self) -> str:
        return "branch-health"

    @property
    def description(self) -> str:
        return "Analyze branch health and predict rebase difficulty"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "branch",
            nargs="?",
            help="Branch to analyze (default: current branch)",
            default=None,
        )
        parser.add_argument(
            "--target",
            "-t",
            help="Target branch to compare against (default: main)",
            default="main",
        )
        parser.add_argument(
            "--json", action="store_true", help="Output results in JSON format"
        )
        parser.add_argument(
            "--verbose", "-v", action="store_true", help="Enable verbose output"
        )
        parser.add_argument(
            "--risks-only", action="store_true", help="Show only risk factors"
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
        return {
            "rebase_analyzer": "RebaseAnalyzer",
            "repository_ops": "RepositoryOperations",
        }

    def set_dependencies(self, deps: Dict[str, Any]) -> None:
        """Set dependencies for the command."""
        self._analyzer = deps.get("rebase_analyzer")
        self._repo_ops = deps.get("repository_ops")

    def _format_output(self, data: Dict[str, Any], output_format: str) -> str:
        """Format output data in the specified format."""
        import json

        if output_format == "yaml":
            if YAML_AVAILABLE:
                return yaml.dump(data, default_flow_style=False, sort_keys=False)
            return json.dumps(data, indent=2)

        if output_format == "text":
            return self._format_text_output(data)

        return json.dumps(data, indent=2)

    def _format_text_output(self, data: Dict[str, Any]) -> str:
        """Format output as plain text."""
        lines = []
        lines.append(f"Branch: {data.get('branch', 'unknown')}")
        lines.append(f"Target: {data.get('target', 'unknown')}")
        lines.append(f"Health Score: {data.get('health_score', 0)}/100")
        if data.get("risks"):
            lines.append("Risks:")
            for risk in data.get("risks", []):
                lines.append(
                    f"  - [{risk.get('severity', '?')}] {risk.get('message', '')}"
                )
        return "\n".join(lines)

    async def execute(self, args: Namespace) -> int:
        """Execute the branch-health command."""
        try:
            from src.services.rebase_analyzer import RebaseAnalyzer
            from src.git.repository import RepositoryOperations

            branch = args.branch
            target = args.target
            repo_path = Path.cwd()

            repo_ops = self._repo_ops or RepositoryOperations(repo_path)

            if not branch:
                branch = repo_ops.get_current_branch_sync()

            health_score, risks = self._analyze_branch_health(repo_ops, branch, target)

            output_data = {
                "branch": branch,
                "target": target,
                "health_score": health_score,
                "risks": risks,
            }

            output_format = args.format or "json"

            if args.json or output_format in ("json", "yaml"):
                output_str = self._format_output(output_data, output_format)
                if args.output:
                    Path(args.output).write_text(output_str)
                else:
                    print(output_str)
            else:
                self._print_health_report(
                    branch, target, health_score, risks, args.risks_only
                )

            return 0

        except ImportError as e:
            print(f"Error: Required module not available: {e}")
            return 1
        except Exception as e:
            print(f"Error during branch health analysis: {e}")
            if hasattr(args, "verbose") and args.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def _analyze_branch_health(
        self, repo_ops, branch: str, target: str
    ) -> tuple[int, List[Dict[str, str]]]:
        """Analyze branch health and return score + risks."""

        risks = []
        score = 100

        try:
            cmd = ["git", "rev-list", "--left-right", f"{target}...{branch}", "--count"]
            stdout, stderr, code = repo_ops.run_command_sync(cmd)

            if code == 0 and stdout.strip():
                parts = stdout.strip().split()
                if len(parts) >= 2:
                    ahead = int(parts[0])
                    behind = int(parts[1])

                    if behind > 0:
                        risks.append(
                            {
                                "type": "divergence",
                                "severity": "high" if behind > 50 else "medium",
                                "message": f"Branch is {behind} commits behind {target}",
                            }
                        )
                        score -= min(behind, 50)

                    if ahead > 100:
                        risks.append(
                            {
                                "type": "commit_count",
                                "severity": "medium",
                                "message": f"Branch has {ahead} new commits (high divergence risk)",
                            }
                        )
                        score -= 10
        except Exception as e:
            risks.append(
                {
                    "type": "analysis_error",
                    "severity": "high",
                    "message": f"Could not analyze divergence: {e}",
                }
            )
            score -= 20

        try:
            cmd = ["git", "log", f"{target}..{branch}", "--oneline", "--name-only"]
            stdout, _, code = repo_ops.run_command_sync(cmd)

            if code == 0 and stdout:
                files_changed = set()
                for line in stdout.strip().split("\n"):
                    if line and not line.startswith(" ") and ":" in line:
                        continue
                    if line.strip() and not line[0].isalnum():
                        files_changed.add(line.strip())

                if len(files_changed) > 50:
                    risks.append(
                        {
                            "type": "file_count",
                            "severity": "high",
                            "message": f"Branch modifies {len(files_changed)} files (high conflict probability)",
                        }
                    )
                    score -= 15
        except Exception:
            pass

        try:
            cmd = ["git", "merge-base", target, branch]
            stdout, _, code = repo_ops.run_command_sync(cmd)

            if code == 0 and stdout.strip():
                cmd = ["git", "log", f"{stdout.strip()}..{branch}", "--oneline"]
                merge_commits, _, _ = repo_ops.run_command_sync(cmd)
                merge_count = len([m for m in merge_commits.split("\n") if m.strip()])

                if merge_count > 10:
                    risks.append(
                        {
                            "type": "rebase_history",
                            "severity": "low",
                            "message": f"Branch has {merge_count} merge commits",
                        }
                    )
                    score -= 5
        except Exception:
            pass

        try:
            cmd = ["git", "log", f"{target}..{branch}", "--grep=rebase", "--oneline"]
            stdout, _, _ = repo_ops.run_command_sync(cmd)

            if stdout.strip():
                risks.append(
                    {
                        "type": "rebase_detected",
                        "severity": "medium",
                        "message": "Branch appears to have been rebased",
                    }
                )
                score -= 10
        except Exception:
            pass

        score = max(0, min(100, score))
        return score, risks

    def _print_health_report(
        self,
        branch: str,
        target: str,
        score: int,
        risks: List[Dict[str, str]],
        risks_only: bool = False,
    ) -> None:
        """Print health report in a readable format."""

        if not risks_only:
            print(f"\n=== Branch Health Report ===")
            print(f"Branch: {branch}")
            print(f"Target: {target}")
            print()

            if score >= 80:
                status = "EXCELLENT"
                color = "\033[92m"
            elif score >= 60:
                status = "GOOD"
                color = "\033[93m"
            elif score >= 40:
                status = "FAIR"
                color = "\033[93m"
            else:
                status = "POOR"
                color = "\033[91m"

            reset = "\033[0m"
            print(f"Health Score: {color}{score}/100{reset} ({status})")
            print()

        if risks:
            print("Risk Factors:")
            print("-" * 40)

            severity_order = {"high": 0, "medium": 1, "low": 2}
            sorted_risks = sorted(
                risks, key=lambda r: severity_order.get(r.get("severity", "low"), 2)
            )

            for risk in sorted_risks:
                sev = risk.get("severity", "low").upper()
                if sev == "HIGH":
                    marker = "[!]"
                elif sev == "MEDIUM":
                    marker = "[~]"
                else:
                    marker = "[.]"

                print(f"  {marker} {risk.get('message', 'Unknown risk')}")

            print()
        else:
            print("No significant risks detected.")

        if not risks_only:
            if score >= 80:
                print("Status: Ready for rebase.")
            elif score >= 60:
                print("Status: Rebase recommended - low risk.")
            elif score >= 40:
                print(
                    "Status: Proceed with caution - review risks above before rebase."
                )
            else:
                print(
                    "Status: High risk rebase - ensure backup branch exists and test thoroughly."
                )
            print()
