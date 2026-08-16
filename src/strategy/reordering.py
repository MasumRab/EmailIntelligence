"""
Rebase strategy planning module.
"""

from typing import List
from ..git.history import Commit
from ..resolution.types import RiskLevel


class RebasePlanner:
    """
    Generates optimized rebase plans.
    """

    def generate_plan(self, commits: List[Commit]) -> str:
        """
        Generate a rebase todo list markdown content.
        """
        # Sort commits: Security > Infra (chore/build) > Features > Fixes > Docs
        # This is a simplified heuristic based on the user's request

        # Grouping
        groups = {
            "critical": [],
            "infra": [],
            "feat": [],
            "fix": [],
            "docs": [],
            "other": [],
        }

        for commit in commits:
            if commit.risk_level in [RiskLevel.CRITICAL.value, RiskLevel.HIGH.value]:
                groups["critical"].append(commit)
            elif commit.category in ["chore", "build", "ci"]:
                groups["infra"].append(commit)
            elif commit.category == "feat":
                groups["feat"].append(commit)
            elif commit.category == "fix":
                groups["fix"].append(commit)
            elif commit.category in ["docs", "style"]:
                groups["docs"].append(commit)
            else:
                groups["other"].append(commit)

        # Generate Markdown
        md = "# Automated Rebase Plan\n\n"

        md += "## Phase 1: Critical & Infrastructure\n"
        for c in groups["critical"] + groups["infra"]:
            md += f"pick {c.hash} {c.message}\n"

        md += "\n## Phase 2: Features\n"
        for c in groups["feat"]:
            md += f"pick {c.hash} {c.message}\n"

        md += "\n## Phase 3: Fixes\n"
        for c in groups["fix"]:
            md += f"pick {c.hash} {c.message}\n"

        md += "\n## Phase 4: Documentation & Cleanup\n"
        for c in groups["docs"] + groups["other"]:
            md += f"pick {c.hash} {c.message}\n"

        return md
