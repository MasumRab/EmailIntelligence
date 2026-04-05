"""
Git Discover Command Module

Implements automated discovery of remote tooling using semantic intent detection.
Identifies scripts and frameworks that are potentially outside the core product scope.
"""

import subprocess
from argparse import Namespace
from typing import Any, Dict, List

from ..interface import Command


class GitDiscoverCommand(Command):
    """
    Command for rigorously discovering unconsolidated or out-of-scope remote tooling.

    Uses NLP-based semantic matching to categorize tools by their functional intent
    and identifies "shadow" frameworks hidden in remote branches.
    """

    CORE_SCOPE = "Searching, categorizing, and managing emails via frontend and backend workflows."

    def __init__(self):
        self._security_validator = None
        self._nlp = None

    @property
    def name(self) -> str:
        return "git-discover"

    @property
    def description(self) -> str:
        return "Discover remote tooling using semantic intent analysis"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument(
            "--limit",
            type=int,
            default=20,
            help="Limit number of branches to scan"
        )
        parser.add_argument(
            "--threshold",
            type=float,
            default=0.4,
            help="Similarity threshold for 'Out of Scope' flagging"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        return {
            "security_validator": "SecurityValidator",
            "nlp": "NLPService"
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        self._security_validator = dependencies.get("security_validator")
        self._nlp = dependencies.get("nlp")

    async def execute(self, args: Namespace) -> int:
        if not self._nlp:
            print("Error: NLPService not available for discovery."); return 1

        print(f"🕵️  Starting Semantic Discovery Sweep (Core Scope: '{self.CORE_SCOPE}')...")

        try:
            # 1. Get branches
            branches = self._get_remote_branches()[:args.limit]
            print(f"Scanning {len(branches)} branches for hidden DNA...")

            for branch in branches:
                print(f"\n--- Investigating Branch: {branch} ---")

                # 2. Extract functional DNA (script names and folder structure)
                dna = self._extract_branch_dna(branch)
                if not dna:
                    print("  - No significant script logic found.")
                    continue

                # 3. Semantic Intent Analysis
                similarity = await self._nlp.calculate_similarity(dna, self.CORE_SCOPE)

                status = "IN SCOPE" if similarity > args.threshold else "🚨 OUT OF SCOPE / EXTERNAL TOOL"
                print(f"  - Semantic Affinity: {similarity:.2f} ({status})")

                if similarity <= args.threshold:
                    print(f"  - Found potential external toolset in {branch}")
                    # List top scripts found in this 'external' branch
                    for script in self._get_branch_scripts(branch)[:5]:
                        print(f"    [!] {script}")

            return 0
        except Exception as e:
            print(f"Error during discovery: {e}"); return 1

    def _get_remote_branches(self) -> List[str]:
        result = subprocess.run(["git", "branch", "-r"], capture_output=True, text=True)
        return [l.strip().replace("origin/", "") for l in result.stdout.splitlines() if "->" not in l]

    def _extract_branch_dna(self, branch: str) -> str:
        """Combine file names and paths to create a 'Functional Intent' string."""
        scripts = self._get_branch_scripts(branch)
        return " ".join([s.replace("/", " ").replace("_", " ").replace(".py", "") for s in scripts])

    def _get_branch_scripts(self, branch: str) -> List[str]:
        """Fetch list of scripts on a remote branch."""
        result = subprocess.run(
            ["git", "ls-tree", "-r", f"origin/{branch}"],
            capture_output=True, text=True
        )
        return [l.split('\t')[1] for l in result.stdout.splitlines() if l.endswith((".py", ".sh"))]
