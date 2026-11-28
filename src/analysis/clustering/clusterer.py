"""Hierarchical branch clustering (task 002.4).

Consumes the three stage-one analyzer blocks per branch and produces clusters,
per-branch assignments, clustering-quality metrics and the raw dendrogram data.

Metric combination is fixed by the task specification::

    combined = 0.35 * commit_history + 0.35 * codebase_structure + 0.30 * diff_distance

The narrow ``cluster()`` contract takes the combined ``analyzer_outputs`` mapping
so the clusterer never shells out itself.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)

COMMIT_HISTORY_WEIGHT = 0.35
CODEBASE_STRUCTURE_WEIGHT = 0.35
DIFF_DISTANCE_WEIGHT = 0.30
CLUSTERING_THRESHOLD = 0.5
LINKAGE_METHOD = "ward"
DISTANCE_METRIC = "euclidean"

REQUIRED_BLOCKS = ("commit_history", "codebase_structure", "diff_distance")


def _combined(history: float, structure: float, diff: float) -> float:
    return (
        COMMIT_HISTORY_WEIGHT * history
        + CODEBASE_STRUCTURE_WEIGHT * structure
        + DIFF_DISTANCE_WEIGHT * diff
    )


class BranchClusterer:
    """Cluster branches from their combined analyzer scores."""

    def __init__(self, repo_path: str, threshold: float = CLUSTERING_THRESHOLD):
        self.repo_path = repo_path
        self.threshold = threshold

    def cluster(self, analyzer_outputs: dict[str, dict[str, Any]]) -> dict[str, Any]:
        """Cluster ``analyzer_outputs`` and return the task-002.4 result dict."""
        branches: list[str] = list(analyzer_outputs)
        if not branches:
            return self._empty_result()

        vectors: list[list[float]] = []
        for branch in branches:
            scores = analyzer_outputs[branch]
            for key in REQUIRED_BLOCKS:
                if key not in scores:
                    raise ValueError(f"Missing '{key}' in analyzer output for {branch}")
            vectors.append(
                [
                    float(scores["commit_history"]["aggregate_score"]),
                    float(scores["codebase_structure"]["aggregate_score"]),
                    float(scores["diff_distance"]["aggregate_score"]),
                ]
            )

        matrix = np.asarray(vectors, dtype=float)

        # A single branch (or a set where every branch scores identically)
        # cannot be split; report one cluster rather than letting linkage fail.
        if len(branches) < 2 or np.allclose(matrix, matrix[0]):
            labels = np.ones(len(branches), dtype=int)
            linkage_matrix = np.zeros((0, 4))
            distances = np.zeros(0)
        else:
            distances = pdist(matrix, metric=DISTANCE_METRIC)
            linkage_matrix = linkage(distances, method=LINKAGE_METHOD)
            labels = fcluster(linkage_matrix, t=self.threshold, criterion="distance")

        distinct = len(set(labels.tolist()))
        sil_avg = db_index = ch_index = 0.0
        if distinct > 1 and len(set(map(tuple, matrix.tolist()))) > 1:
            distance_matrix = squareform(distances)
            try:
                sil_avg = float(
                    silhouette_score(distance_matrix, labels, metric="precomputed")
                )
            except ValueError:
                sil_avg = 0.0
            try:
                db_index = float(davies_bouldin_score(matrix, labels))
                ch_index = float(calinski_harabasz_score(matrix, labels))
            except ValueError:
                db_index = ch_index = 0.0

        cluster_details = []
        for label in sorted(set(labels.tolist())):
            member_indices = [i for i, lab in enumerate(labels) if lab == label]
            member_branches = [branches[i] for i in member_indices]
            member_vectors = matrix[member_indices]
            center = member_vectors.mean(axis=0)
            internal = pdist(member_vectors, metric=DISTANCE_METRIC)
            cohesion = 1.0 - (float(internal.mean()) if internal.size else 0.0)

            cluster_details.append(
                {
                    "cluster_id": int(label),
                    "branches": member_branches,
                    "cluster_center": {
                        "commit_history_weight": float(center[0]),
                        "codebase_structure_weight": float(center[1]),
                        "diff_distance_weight": float(center[2]),
                        "combined_score": float(_combined(*center)),
                    },
                    "size": len(member_branches),
                    "cohesion": float(cohesion),
                    "silhouette_score": float(sil_avg),
                }
            )

        return {
            "clusters": cluster_details,
            "branch_assignments": {
                branches[i]: int(labels[i]) for i in range(len(branches))
            },
            "quality_metrics": {
                "total_clusters": distinct,
                "silhouette_avg": sil_avg,
                "davies_bouldin_index": db_index,
                "calinski_harabasz_index": ch_index,
            },
            "dendogram_data": {
                "linkage_matrix": linkage_matrix.tolist(),
                "branch_indices": list(range(len(branches))),
            },
            "clustering_timestamp": datetime.now(UTC).isoformat(),
        }

    @staticmethod
    def _empty_result() -> dict[str, Any]:
        return {
            "clusters": [],
            "branch_assignments": {},
            "quality_metrics": {
                "total_clusters": 0,
                "silhouette_avg": 0.0,
                "davies_bouldin_index": 0.0,
                "calinski_harabasz_index": 0.0,
            },
            "dendogram_data": {"linkage_matrix": [], "branch_indices": []},
            "clustering_timestamp": datetime.now(UTC).isoformat(),
        }
