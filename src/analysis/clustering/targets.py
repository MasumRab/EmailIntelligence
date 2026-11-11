"""Integration-target assignment and tagging (task 002.5).

Turns the clusterer's ``branch_assignments`` into per-branch integration
targets (``main``, ``scientific``, ``orchestration-tools``) through the
four-level hierarchy:

1. heuristics (confidence 0.85-0.95)
2. archetype affinity via cosine similarity (<= 0.95)
3. cluster consensus among already-decided siblings (<= 0.70)
4. default to ``main`` at 0.65 confidence

Each branch additionally receives tags drawn from a nine-category catalog.

The assigner needs metric detail that the clusterer output does not carry, so
``assign()`` accepts the analyzer mapping as an optional second argument. When
it is omitted the assigner runs the three analyzers itself against
``repo_path``.
"""

from __future__ import annotations

import math
import re
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

INTEGRATION_TARGETS = ("main", "scientific", "orchestration-tools")

HEURISTIC_CONFIDENCE_THRESHOLD = 0.95
AFFINITY_CONFIDENCE_THRESHOLD = 0.70
CLUSTER_CONSENSUS_THRESHOLD = 0.60
DEFAULT_TARGET = "main"
DEFAULT_CONFIDENCE = 0.65

TARGET_ARCHETYPES = {
    "main": {"commit_history": 0.85, "codebase_structure": 0.90, "diff_distance": 0.75},
    "scientific": {
        "commit_history": 0.65,
        "codebase_structure": 0.70,
        "diff_distance": 0.50,
    },
    "orchestration-tools": {
        "commit_history": 0.70,
        "codebase_structure": 0.75,
        "diff_distance": 0.65,
    },
}

DOMAIN_PATTERNS = {
    "authentication": ("auth", "login", "session", "user", "jwt", "oauth"),
    "api-changes": ("api", "endpoint", "rest", "graphql", "router", "route"),
    "orchestration": (
        "orchestration",
        "pipeline",
        "scheduler",
        "dask",
        "workflow",
        "orchestrator",
    ),
    "data-science": ("ml", "ai", "data", "science", "analytics", "model", "dataset"),
    "testing": ("test", "tests", "spec", "coverage", "qa"),
    "documentation": ("docs", "doc", "readme", "guide"),
}

TAG_CATALOG = {
    "scope": [
        "core-feature",
        "minor-feature",
        "experiment",
        "refactoring",
        "bug-fix",
        "infrastructure",
    ],
    "risk_level": ["low-risk", "medium-risk", "high-risk"],
    "complexity": ["simple", "moderate", "complex"],
    "dev_status": [
        "active-development",
        "stale",
        "ready-for-merge",
        "requires-review",
        "staging",
    ],
    "file_impact": [
        "low-file-impact",
        "moderate-file-impact",
        "high-file-impact",
        "massive-impact",
    ],
    "domain": [
        "authentication",
        "api-changes",
        "orchestration",
        "data-science",
        "testing",
        "documentation",
    ],
    "validation": [
        "testing-required-high",
        "testing-required-medium",
        "testing-optional",
        "auto-mergeable",
    ],
    "target": ["main-ready", "scientific-branch", "orchestration-branch"],
    "special_flags": [
        "has-breaking-changes",
        "concurrent-development",
        "merge-conflict-risk",
    ],
}

_TARGET_TAG = {
    "main": "main-ready",
    "scientific": "scientific-branch",
    "orchestration-tools": "orchestration-branch",
}

_TOKEN_SPLIT = re.compile(r"[/_\-.]+")


def _segments(branch_name: str) -> list[str]:
    """Split a branch name into lowercase word segments (not substrings)."""
    return [part for part in _TOKEN_SPLIT.split(branch_name.lower()) if part]


def _cosine(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=False))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


class IntegrationTargetAssigner:
    """Assign branches to integration targets and tag them."""

    def __init__(self, repo_path: str, main_branch: str = "main"):
        self.repo_path = repo_path
        self.main_branch = main_branch

    # ------------------------------------------------------------------ input

    def _branch_metrics(
        self, branch_name: str, analyzer_outputs: dict[str, dict[str, Any]] | None
    ) -> dict[str, float]:
        """Flatten the three analyzer blocks into the flat metric dict tags use."""
        if analyzer_outputs is not None and branch_name in analyzer_outputs:
            blocks = analyzer_outputs[branch_name]
        else:
            from .commit_history import CommitHistoryAnalyzer
            from .diff_distance import DiffDistanceCalculator
            from .structure import CodebaseStructureAnalyzer

            blocks = {
                "commit_history": CommitHistoryAnalyzer(
                    self.repo_path, main_branch=self.main_branch
                ).analyze_sync(branch_name),
                "codebase_structure": CodebaseStructureAnalyzer(
                    self.repo_path, main_branch=self.main_branch
                ).analyze(branch_name),
                "diff_distance": DiffDistanceCalculator(
                    self.repo_path, main_branch=self.main_branch
                ).analyze(branch_name),
            }

        history = blocks.get("commit_history", {})
        structure = blocks.get("codebase_structure", {})
        diff = blocks.get("diff_distance", {})
        h = history.get("metrics", {})
        s = structure.get("metrics", {})
        d = diff.get("metrics", {})

        return {
            "commit_history": float(history.get("aggregate_score", 0.0)),
            "codebase_structure": float(structure.get("aggregate_score", 0.0)),
            "diff_distance": float(diff.get("aggregate_score", 0.0)),
            "commit_recency": float(h.get("commit_recency", 0.0)),
            "merge_readiness": float(h.get("merge_readiness", 0.0)),
            "authorship_diversity": float(h.get("authorship_diversity", 0.0)),
            # The structure analyzer names this metric directly; using its
            # aggregate instead would fire the flag on almost every branch.
            "core_module_stability": float(s.get("core_module_stability", 1.0)),
            "code_churn": float(d.get("code_churn", 0.0)),
            "integration_risk": float(d.get("integration_risk", 0.0)),
            "diff_complexity": float(d.get("diff_complexity", 0.0)),
            "files_affected": float(diff.get("files_affected", 0)),
        }

    # ------------------------------------------------------------ hierarchy

    @staticmethod
    def _apply_heuristics(
        branch_name: str, m: dict[str, float]
    ) -> tuple[str, float, str]:
        """Level 1: explicit rules from task 002.5.6."""
        if m["merge_readiness"] > 0.90 and m["integration_risk"] < 0.20:
            return (
                "main",
                0.95,
                "Heuristic rule match (high merge_readiness + low integration_risk)",
            )

        words = set(_segments(branch_name))
        if words & {"science", "scientific", "data", "analytics", "research"}:
            return "scientific", 0.92, "Heuristic rule match (scientific branch name)"
        if words & {"orchestration", "orchestrator", "devops", "pipeline", "workflow"}:
            return (
                "orchestration-tools",
                0.94,
                "Heuristic rule match (orchestration branch name)",
            )

        if m["code_churn"] < 0.30 and m["files_affected"] < 10:
            return "main", 0.90, "Heuristic rule match (low churn, few files)"
        if m["code_churn"] > 0.70 and m["files_affected"] > 30:
            return (
                "scientific",
                0.85,
                "Heuristic rule match (high churn, wide file impact)",
            )

        return DEFAULT_TARGET, 0.0, "No heuristic rule matched"

    @staticmethod
    def _affinity_scoring(m: dict[str, float]) -> tuple[str, float, str]:
        """Level 2: cosine similarity against the three target archetypes.

        The three archetypes point in almost the same direction, so a cosine
        comparison is only informative when one target clearly leads. An
        inconclusive result returns zero confidence so the hierarchy falls
        through to cluster consensus instead of confidently picking the
        archetype with the smallest norm.
        """
        vector = [m["commit_history"], m["codebase_structure"], m["diff_distance"]]
        ranked = sorted(
            (
                (_cosine(vector, list(archetype.values())), target)
                for target, archetype in TARGET_ARCHETYPES.items()
            ),
            reverse=True,
        )
        (best_score, best_target), (second_score, _) = ranked[0], ranked[1]

        margin = best_score - second_score
        if best_score < AFFINITY_CONFIDENCE_THRESHOLD or margin < 0.01:
            return (
                DEFAULT_TARGET,
                0.0,
                (
                    f"Affinity inconclusive (best {best_target} {best_score:.3f}, "
                    f"runner-up {second_score:.3f})"
                ),
            )

        return (
            best_target,
            min(0.95, best_score),
            f"Affinity scoring (cosine similarity {best_score:.3f} to {best_target})",
        )

    @staticmethod
    def _cluster_consensus(
        cluster_id: int,
        cluster_data: dict[str, Any],
        decided: dict[str, dict[str, Any]],
    ) -> tuple[str, float, str]:
        """Level 3: majority target among already-decided members of the cluster."""
        siblings = [
            row["integration_target"]
            for name, row in decided.items()
            if row["cluster_id"] == cluster_id
        ]
        if not siblings:
            return DEFAULT_TARGET, 0.0, "No cluster consensus available"
        winner = max(set(siblings), key=siblings.count)
        share = siblings.count(winner) / len(siblings)
        return (
            winner,
            float(share),
            f"Cluster consensus ({winner} chosen by {share:.0%} of {len(siblings)} siblings)",
        )

    # ------------------------------------------------------------------ tags

    def _generate_tags(
        self, branch_name: str, m: dict[str, float], target: str
    ) -> list[str]:
        tags: list[str] = []

        # Scope
        if m["codebase_structure"] > 0.85:
            tags.append("core-feature")
        if m["files_affected"] < 5:
            tags.append("minor-feature")
        if m["diff_complexity"] > 0.75:
            tags.append("refactoring")

        # Risk
        if m["integration_risk"] > 0.75 and m["code_churn"] < 0.40:
            tags.append("low-risk")
        elif m["integration_risk"] < 0.50 and m["code_churn"] > 0.70:
            tags.append("high-risk")
        else:
            tags.append("medium-risk")

        # Complexity
        if (
            m["commit_history"] > 0.8
            and m["codebase_structure"] > 0.8
            and m["diff_distance"] > 0.8
        ):
            tags.append("simple")
        elif m["diff_complexity"] > 0.75:
            tags.append("complex")
        else:
            tags.append("moderate")

        # Development status
        if m["merge_readiness"] > 0.85:
            tags.append("ready-for-merge")
        if m["commit_recency"] > 0.80:
            tags.append("active-development")
        if m["commit_recency"] < 0.10:
            tags.append("stale")
        if "ready-for-merge" not in tags and "stale" not in tags:
            tags.append("requires-review")

        # File impact
        files = m["files_affected"]
        if files < 5:
            tags.append("low-file-impact")
        elif files <= 15:
            tags.append("moderate-file-impact")
        elif files <= 30:
            tags.append("high-file-impact")
        else:
            tags.append("massive-impact")

        # Domain — match whole name segments, never substrings
        words = set(_segments(branch_name))
        for tag, patterns in DOMAIN_PATTERNS.items():
            if words & set(patterns):
                tags.append(tag)

        # Validation strategy
        if m["integration_risk"] > 0.70 or files > 15:
            tags.append("testing-required-high")
        elif "medium-risk" in tags:
            tags.append("testing-required-medium")
        else:
            tags.append("testing-optional")

        # Target
        tags.append(_TARGET_TAG.get(target, "main-ready"))

        # Special flags
        if m["core_module_stability"] < 0.80:
            tags.append("has-breaking-changes")
        if m["authorship_diversity"] > 0.70:
            tags.append("concurrent-development")

        # Preserve declaration order while removing duplicates.
        return list(dict.fromkeys(tags))

    # ------------------------------------------------------------------ entry

    def assign(
        self,
        cluster_data: dict[str, Any],
        analyzer_outputs: dict[str, dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Assign every branch in ``cluster_data`` to an integration target."""
        results: dict[str, dict[str, Any]] = {}

        for branch_name, cluster_id in cluster_data.get(
            "branch_assignments", {}
        ).items():
            metrics = self._branch_metrics(branch_name, analyzer_outputs)

            # Each level returns confidence 0.0 when it reaches no decision.
            # The configured 0.95 heuristic gate cannot be used directly: the
            # task's own rules are calibrated at 0.85-0.94, so gating on it
            # would let cosine affinity override every name-based heuristic.
            target, confidence, rationale = self._apply_heuristics(branch_name, metrics)
            if confidence <= 0.0:
                target, confidence, rationale = self._affinity_scoring(metrics)
            if confidence < AFFINITY_CONFIDENCE_THRESHOLD:
                consensus_target, consensus_conf, consensus_rationale = (
                    self._cluster_consensus(cluster_id, cluster_data, results)
                )
                if consensus_conf > confidence:
                    target, confidence, rationale = (
                        consensus_target,
                        consensus_conf,
                        consensus_rationale,
                    )
            if confidence < CLUSTER_CONSENSUS_THRESHOLD:
                target, confidence, rationale = (
                    DEFAULT_TARGET,
                    DEFAULT_CONFIDENCE,
                    "Default assignment (no rule matched)",
                )

            results[branch_name] = {
                "branch_name": branch_name,
                "integration_target": target,
                "cluster_id": cluster_id,
                "confidence": round(float(confidence), 4),
                "decision_rationale": rationale,
                "tags": self._generate_tags(branch_name, metrics, target),
            }

        return self._format_output(results)

    @staticmethod
    def _format_output(results: dict[str, dict[str, Any]]) -> dict[str, Any]:
        summary: dict[str, dict[str, Any]] = {
            target: {"branch_count": 0, "total_confidence": 0.0, "key_tags": []}
            for target in INTEGRATION_TARGETS
        }
        tag_counts: dict[str, dict[str, int]] = {t: {} for t in INTEGRATION_TARGETS}

        for row in results.values():
            target = row["integration_target"]
            bucket = summary.setdefault(
                target, {"branch_count": 0, "total_confidence": 0.0, "key_tags": []}
            )
            bucket["branch_count"] += 1
            bucket["total_confidence"] += row["confidence"]
            for tag in row["tags"]:
                tag_counts.setdefault(target, {})
                tag_counts[target][tag] = tag_counts[target].get(tag, 0) + 1

        for target, bucket in summary.items():
            count = bucket["branch_count"]
            bucket["total_confidence"] = (
                round(bucket["total_confidence"] / count, 4) if count else 0.0
            )
            ranked = sorted(
                tag_counts.get(target, {}).items(), key=lambda kv: (-kv[1], kv[0])
            )
            bucket["key_tags"] = [tag for tag, _ in ranked[:5]]

        return {
            "categorized_branches": results,
            "integration_target_summary": summary,
            "tag_catalog": {"by_category": TAG_CATALOG},
            "assignment_timestamp": datetime.now(UTC).isoformat(),
        }
