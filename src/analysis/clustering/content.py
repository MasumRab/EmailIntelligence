"""Content-based branch clustering (task 002, stage 2).

Stage one clusters branches by three aggregate scores, which means two branches
that touch completely unrelated parts of the tree can land in the same cluster
while two branches that edit the same module in different ways can be split.
The branch name makes it worse: a name is a label someone chose, not evidence
of what the diff does.

This stage clusters on what the branch actually changes:

* **paths** — the directories and filenames it adds or modifies
* **identifiers** — the names that appear in the lines it adds
* **commit messages** — the author's own description of each commit

Each source contributes tokens to a per-branch document, the documents are
weighted with TF-IDF (so a token used by every branch carries no weight), and
branches are clustered on cosine distance with average linkage. The cut is
chosen by maximising silhouette over a threshold grid rather than fixed, so a
tightly grouped fleet is not forced into the same number of clusters as a
scattered one.

This is lexical rather than embedding-based: it clusters on the vocabulary a
change introduces, which is the strongest content signal available offline. It
is not a substitute for a code embedding model, and the report says so.
"""

from __future__ import annotations

import math
import re
import subprocess
from typing import Any

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score

MAX_DIFF_LINES = 4000
MAX_IDENTIFIERS = 3000
MIN_TOKEN_LENGTH = 3
THRESHOLD_GRID = tuple(round(0.30 + 0.05 * i, 2) for i in range(13))  # 0.30 .. 0.90
MAX_CLUSTERS = 60

_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}")
_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_NON_WORD = re.compile(r"[^A-Za-z0-9]+")

# Tokens that appear in every diff and therefore identify nothing.
STOPWORDS = frozenset(
    [
        "the",
        "and",
        "for",
        "not",
        "but",
        "with",
        "from",
        "this",
        "that",
        "these",
        "those",
        "then",
        "than",
        "when",
        "where",
        "which",
        "while",
        "into",
        "only",
        "also",
        "such",
        "have",
        "has",
        "had",
        "are",
        "was",
        "were",
        "will",
        "would",
        "can",
        "could",
        "should",
        "def",
        "class",
        "return",
        "import",
        "from",
        "not",
        "none",
        "true",
        "false",
        "self",
        "cls",
        "pass",
        "raise",
        "try",
        "except",
        "finally",
        "with",
        "as",
        "in",
        "is",
        "or",
        "if",
        "else",
        "elif",
        "lambda",
        "yield",
        "async",
        "await",
        "global",
        "nonlocal",
        "print",
        "str",
        "int",
        "float",
        "bool",
        "list",
        "dict",
        "set",
        "tuple",
        "len",
        "range",
        "type",
        "object",
        "super",
        "getattr",
        "setattr",
        "hasattr",
        "isinstance",
        "issubclass",
        "assert",
        "del",
        "assert",
        "except",
        "finally",
        "const",
        "let",
        "var",
        "function",
        "export",
        "default",
        "new",
        "this",
        "static",
        "public",
        "private",
        "protected",
        "void",
        "null",
        "undefined",
        "typeof",
        "instanceof",
        "interface",
        "extends",
        "implements",
        "return",
        "true",
        "false",
        "null",
        "import",
        "require",
        "module",
        "exports",
        "console",
        "log",
        "error",
        "warn",
        "debug",
        "test",
        "tests",
        "assert",
        "expect",
        "describe",
        "it",
        "should",
        "spec",
    ]
)


def _split_identifier(token: str) -> list[str]:
    """Split one identifier into lowercase word parts (camelCase and snake)."""
    parts: list[str] = []
    for chunk in _NON_WORD.split(token):
        for piece in _CAMEL.split(chunk):
            piece = piece.lower()
            if len(piece) >= MIN_TOKEN_LENGTH and piece not in STOPWORDS:
                parts.append(piece)
    return parts


def _path_tokens(path: str) -> list[str]:
    tokens = []
    for piece in _NON_WORD.split(path):
        piece = piece.lower()
        if len(piece) >= MIN_TOKEN_LENGTH and piece not in STOPWORDS:
            tokens.append(f"path/{piece}")
    return tokens


def _diff_added_lines(repo_path: str, merge_base: str, branch_rev: str) -> list[str]:
    """Return the ``+`` lines of a branch's diff, capped to keep memory bounded."""
    result = subprocess.run(
        [
            "git",
            "-C",
            repo_path,
            "diff",
            "-U0",
            "--no-color",
            "--no-ext-diff",
            "--diff-filter=AM",
            f"{merge_base}..{branch_rev}",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    added: list[str] = []
    for line in result.stdout.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:])
            if len(added) >= MAX_DIFF_LINES:
                break
    return added


def build_documents(profile: dict[str, Any], repo_path: str) -> dict[str, list[str]]:
    """Turn one branch git profile into its token document."""
    tokens: list[str] = []

    for path in profile.get("files", {}):
        tokens.extend(_path_tokens(path))

    for commit in profile.get("commits", []):
        for word in _NON_WORD.split(commit.get("subject", "")):
            word = word.lower()
            if len(word) >= MIN_TOKEN_LENGTH and word not in STOPWORDS:
                tokens.append(f"msg/{word}")

    added = _diff_added_lines(repo_path, profile["merge_base"], profile["branch_rev"])
    identifiers: list[str] = []
    for line in added:
        for match in _IDENTIFIER.findall(line):
            identifiers.extend(_split_identifier(match))
            if len(identifiers) >= MAX_IDENTIFIERS:
                break
        if len(identifiers) >= MAX_IDENTIFIERS:
            break
    tokens.extend(f"id/{name}" for name in identifiers)

    return {"tokens": tokens}


def _cluster_signature(
    matrix: np.ndarray,
    labels: np.ndarray,
    cluster_id: int,
    terms: np.ndarray,
    top_n: int = 8,
) -> list[str]:
    """Terms that are over-represented inside this cluster versus outside it."""
    inside = labels == cluster_id
    if not inside.any():
        return []
    mean_inside = matrix[inside].mean(axis=0)
    if (~inside).any():
        mean_outside = matrix[~inside].mean(axis=0)
    else:
        mean_outside = np.zeros_like(mean_inside)
    lift = np.asarray(mean_inside - mean_outside).ravel()
    order = np.argsort(lift)[::-1][:top_n]
    return [str(terms[i]) for i in order if lift[i] > 0.0]


def cluster_content(
    documents: dict[str, list[str]],
    *,
    min_df: int = 2,
) -> dict[str, Any]:
    """Cluster branches by the vocabulary of their diffs.

    ``documents`` maps a branch name to its token list. Branches with no tokens
    cannot be compared on content and are reported as excluded, never silently
    dropped.
    """
    usable = {name: toks for name, toks in documents.items() if toks}
    excluded = sorted(set(documents) - set(usable))

    if len(usable) < 2:
        return {
            "method": "tfidf-cosine-average-linkage",
            "document_count": len(usable),
            "excluded_no_content": excluded,
            "clusters": [],
            "branch_assignments": {},
            "quality_metrics": {
                "total_clusters": len(usable),
                "silhouette_avg": 0.0,
                "threshold": None,
                "vocabulary_size": 0,
            },
        }

    names = list(usable)
    texts = [" ".join(usable[name]) for name in names]

    vectorizer = TfidfVectorizer(
        analyzer="word",
        token_pattern=r"\S+",
        lowercase=False,
        min_df=min_df,
        sublinear_tf=True,
        norm="l2",
    )
    matrix = vectorizer.fit_transform(texts).toarray()
    terms = vectorizer.get_feature_names_out()

    # Rows that became empty after the min_df filter cannot be compared.
    nonzero = np.linalg.norm(matrix, axis=1) > 0
    if nonzero.sum() < 2:
        return {
            "method": "tfidf-cosine-average-linkage",
            "document_count": int(nonzero.sum()),
            "excluded_no_content": excluded
            + sorted(names[i] for i in range(len(names)) if not nonzero[i]),
            "clusters": [],
            "branch_assignments": {},
            "quality_metrics": {
                "total_clusters": 0,
                "silhouette_avg": 0.0,
                "threshold": None,
                "vocabulary_size": int(matrix.shape[1]),
            },
        }

    kept_indices = [i for i in range(len(names)) if nonzero[i]]
    kept_names = [names[i] for i in kept_indices]
    kept_matrix = matrix[kept_indices]
    excluded.extend(sorted(names[i] for i in range(len(names)) if not nonzero[i]))

    distances = pdist(kept_matrix, metric="cosine")
    tree = linkage(distances, method="average")

    best_labels: np.ndarray | None = None
    best_silhouette = -1.0
    best_threshold: float | None = None
    for threshold in THRESHOLD_GRID:
        labels = fcluster(tree, t=threshold, criterion="distance")
        distinct = len(set(labels.tolist()))
        if distinct < 2 or distinct > min(MAX_CLUSTERS, len(kept_names) - 1):
            continue
        try:
            score = float(silhouette_score(kept_matrix, labels, metric="cosine"))
        except ValueError:
            continue
        if math.isfinite(score) and score > best_silhouette:
            best_silhouette = score
            best_labels = labels
            best_threshold = threshold

    if best_labels is None:
        # No threshold separated the fleet: one content community.
        best_labels = np.ones(len(kept_names), dtype=int)
        best_silhouette = 0.0

    assignments = {kept_names[i]: int(best_labels[i]) for i in range(len(kept_names))}

    clusters = []
    for label in sorted(set(best_labels.tolist())):
        member_indices = [i for i, lab in enumerate(best_labels) if lab == label]
        member_branches = [kept_names[i] for i in member_indices]
        member_matrix = kept_matrix[member_indices]
        if len(member_indices) > 1:
            internal = pdist(member_matrix, metric="cosine")
            cohesion = 1.0 - float(np.mean(internal))
        else:
            cohesion = 1.0
        clusters.append(
            {
                "cluster_id": int(label),
                "size": len(member_branches),
                "branches": member_branches,
                "cohesion": round(cohesion, 4),
                "signature_terms": _cluster_signature(
                    kept_matrix, best_labels, label, terms
                ),
            }
        )
    clusters.sort(key=lambda c: (-c["size"], c["cluster_id"]))

    return {
        "method": "tfidf-cosine-average-linkage",
        "note": (
            "Lexical content clustering over path names, added-line identifiers "
            "and commit subjects. It captures shared vocabulary, not shared "
            "behaviour; use it to group a merge wave, not to prove equivalence."
        ),
        "document_count": len(kept_names),
        "excluded_no_content": sorted(set(excluded)),
        "clusters": clusters,
        "branch_assignments": assignments,
        "quality_metrics": {
            "total_clusters": len(clusters),
            "silhouette_avg": round(float(best_silhouette), 4),
            "threshold": best_threshold,
            "vocabulary_size": int(matrix.shape[1]),
        },
    }


def compare_clusterings(
    metric_assignments: dict[str, int], content_assignments: dict[str, int]
) -> dict[str, Any]:
    """Measure how much the score-based and content-based views agree."""
    from sklearn.metrics import adjusted_rand_score

    shared = sorted(set(metric_assignments) & set(content_assignments))
    if len(shared) < 3:
        return {"shared_branches": len(shared), "adjusted_rand_index": None}
    a = [metric_assignments[name] for name in shared]
    b = [content_assignments[name] for name in shared]
    return {
        "shared_branches": len(shared),
        "adjusted_rand_index": round(float(adjusted_rand_score(a, b)), 4),
    }
