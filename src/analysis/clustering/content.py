"""Content-based branch clustering (task 002, stage 2).

Stage one clusters branches by three aggregate scores, which means two branches
that touch completely unrelated parts of the tree can land in the same cluster
while two branches that edit the same module in different ways can be split.
The branch name makes it worse: a name is a label someone chose, not evidence
of what the diff does.

This stage clusters on what the branch actually changes, at several detail
levels, with a deterministic hashed representation and a hierarchy of cuts:

* **detail levels** — six independent feature families, each extracted at its
  own granularity: path segments and hierarchical path prefixes, identifier
  words and adjacent identifier pairs, commit-message words and word pairs,
  and sub-word character 4-grams. A change that renames ``charge_handler`` to
  ``settle_handler`` still shares its sub-word level; a change that only edits
  paths still separates at the path level.
* **deterministic hashing** — every token is mapped to one of 65,536 buckets by
  ``blake2b``, with the sign taken from the digest's high bit. The mapping does
  not depend on the process, the platform, ``PYTHONHASHSEED`` or a fitted
  vocabulary, so the same branch always produces the same vector and the same
  cluster. No vocabulary is learned, so an unseen branch cannot shift an
  existing branch's features.
* **hierarchical cuts** — one average-linkage tree is cut at a grid of cosine
  thresholds, giving coarse-to-fine partitions of the same fleet. The primary
  partition is the cut with the best silhouette; every finer cluster records
  the coarser cluster that contains its majority, so the result is a tree
  rather than a single flat grouping.

This is lexical rather than embedding-based: it clusters on the vocabulary a
change introduces, which is the strongest content signal available offline. It
is not a substitute for a code embedding model, and the report says so.
"""

from __future__ import annotations

import hashlib
import itertools
import math
import re
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.sparse import csr_matrix, hstack
from scipy.spatial.distance import squareform
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.metrics.pairwise import pairwise_distances

MAX_DIFF_LINES = 4000
MAX_IDENTIFIERS = 3000
MIN_TOKEN_LENGTH = 3
BUCKETS = 1 << 16
MAX_CLUSTERS = 60

# Coarse-to-fine cosine thresholds. The primary cut is the one with the best
# silhouette; the others are reported as the hierarchy around it.
CUT_GRID = (0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95)

# Detail levels and their relative weight in the combined vector. Structure
# outweighs prose: what a branch touches is stronger evidence than how the
# author described it.
LEVEL_WEIGHTS: dict[str, float] = {
    "path": 1.00,
    "path_pair": 0.70,
    "symbol": 1.20,
    "symbol_pair": 0.80,
    "message": 0.60,
    "subword": 0.40,
}

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
        "const",
        "let",
        "var",
        "function",
        "export",
        "default",
        "new",
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
        "expect",
        "describe",
        "it",
        "spec",
    ]
)


# ----------------------------------------------------------------- hashing


def stable_bucket(token: str) -> tuple[int, float]:
    """Map a token to ``(bucket, sign)`` deterministically.

    ``hashlib.blake2b`` is stable across processes and platforms, unlike
    ``hash()`` (salted per process) and unlike a fitted vocabulary (which
    depends on the corpus and its ordering). The high bit of the digest picks
    the sign, so collisions cancel on average instead of always accumulating.
    """
    digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
    value = int.from_bytes(digest, "big")
    bucket = value % BUCKETS
    sign = 1.0 if (value >> 63) & 1 else -1.0
    return bucket, sign


# ------------------------------------------------------------ extraction


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


def _path_hierarchy(path: str) -> list[str]:
    """Every prefix of a path, so a deep file also counts for its directories."""
    parts = [p for p in _NON_WORD.split(path.lower()) if len(p) >= MIN_TOKEN_LENGTH]
    return [f"prefix/{'/'.join(parts[: i + 1])}" for i in range(min(len(parts), 6))]


def _bigrams(tokens: list[str]) -> list[str]:
    return [f"pair/{a}+{b}" for a, b in itertools.pairwise(tokens)]


def _subwords(token: str, size: int = 4) -> list[str]:
    if len(token) < size:
        return []
    return [f"cg/{token[i : i + size]}" for i in range(len(token) - size + 1)]


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


@dataclass
class FeatureDocument:
    """One branch's features, split by detail level."""

    levels: dict[str, list[str]] = field(default_factory=dict)

    def tokens(self) -> list[str]:
        return [token for level in self.levels.values() for token in level]


def build_documents(profile: dict[str, Any], repo_path: str) -> dict[str, Any]:
    """Turn one branch git profile into its multi-level token document."""
    paths = list(profile.get("files", {}))
    path_tokens: list[str] = []
    hierarchy: list[str] = []
    for path in paths:
        path_tokens.extend(_path_tokens(path))
        hierarchy.extend(_path_hierarchy(path))

    message_words: list[str] = []
    for commit in profile.get("commits", []):
        for word in _NON_WORD.split(commit.get("subject", "")):
            word = word.lower()
            if len(word) >= MIN_TOKEN_LENGTH and word not in STOPWORDS:
                message_words.append(f"msg/{word}")

    added = _diff_added_lines(repo_path, profile["merge_base"], profile["branch_rev"])
    identifiers: list[str] = []
    for line in added:
        for match in _IDENTIFIER.findall(line):
            identifiers.extend(_split_identifier(match))
            if len(identifiers) >= MAX_IDENTIFIERS:
                break
        if len(identifiers) >= MAX_IDENTIFIERS:
            break
    symbols = [f"id/{name}" for name in identifiers]
    subwords: list[str] = []
    for name in identifiers:
        subwords.extend(_subwords(name))

    levels = {
        "path": hierarchy + path_tokens,
        "path_pair": _bigrams(path_tokens),
        "symbol": symbols,
        "symbol_pair": _bigrams(identifiers),
        "message": message_words + _bigrams(message_words),
        "subword": subwords,
    }
    document = FeatureDocument(levels=levels)
    return {"tokens": document.tokens(), "levels": levels}


# -------------------------------------------------------------- clustering


def _hashed_matrix(
    levels: list[list[str]],
    bucket_terms: dict[int, Counter[str]],
    offset: int = 0,
) -> csr_matrix:
    """Build one sparse, L2-normalised, sign-hashed row per document."""
    rows: list[int] = []
    cols: list[int] = []
    values: list[float] = []
    for row, tokens in enumerate(levels):
        counts: dict[int, float] = {}
        for token in tokens:
            bucket, sign = stable_bucket(token)
            counts[bucket] = counts.get(bucket, 0.0) + sign
            bucket_terms.setdefault(offset + bucket, Counter())[token] += 1
        norm = math.sqrt(sum(v * v for v in counts.values()))
        if norm == 0.0:
            continue
        rows.extend([row] * len(counts))
        cols.extend(counts)
        values.extend(v / norm for v in counts.values())
    return csr_matrix(
        (values, (rows, cols)), shape=(len(levels), BUCKETS), dtype=np.float64
    )


def _carry_term(bucket_terms: dict[int, Counter[str]], bucket: int) -> str | None:
    counter = bucket_terms.get(bucket)
    if not counter:
        return None
    # Deterministic tie-break: most frequent, then lexicographic.
    return min(counter.items(), key=lambda kv: (-kv[1], kv[0]))[0]


def _cluster_signature(
    matrix: csr_matrix,
    labels: np.ndarray,
    cluster_id: int,
    bucket_terms: dict[int, Counter[str]],
    top_n: int = 8,
) -> list[str]:
    """Tokens whose bucket is over-represented inside this cluster."""
    inside = labels == cluster_id
    if not inside.any():
        return []
    mean_inside = np.asarray(matrix[inside].mean(axis=0)).ravel()
    if (~inside).any():
        mean_outside = np.asarray(matrix[~inside].mean(axis=0)).ravel()
    else:
        mean_outside = np.zeros_like(mean_inside)
    # Features are sign-hashed, so compare magnitudes: a bucket that holds only
    # the other class has a negative outside mean, and subtracting it would
    # nominate that class's tokens as this cluster's signature.
    lift = np.abs(mean_inside) - np.abs(mean_outside)
    order = np.argsort(lift)[::-1][: top_n * 2]
    terms: list[str] = []
    for index in order:
        if lift[index] <= 0.0 or mean_inside[index] == 0.0:
            continue
        term = _carry_term(bucket_terms, int(index))
        if term is not None:
            terms.append(term)
        if len(terms) >= top_n:
            break
    return terms


def _partition(
    distances: np.ndarray, threshold: float
) -> tuple[np.ndarray, float] | None:
    # linkage wants the condensed form; a square matrix would be read as
    # observation vectors, which is a silent way to cluster the wrong thing.
    tree = linkage(squareform(distances, checks=False), method="average")
    labels = fcluster(tree, t=threshold, criterion="distance")
    distinct = len(set(labels.tolist()))
    if distinct < 2 or distinct > min(MAX_CLUSTERS, len(labels) - 1):
        return None
    try:
        score = float(silhouette_score(distances, labels, metric="precomputed"))
    except ValueError:
        return None
    if not math.isfinite(score):
        return None
    return labels, score


def cluster_content(
    documents: dict[str, Any],
    *,
    min_df: int = 1,
) -> dict[str, Any]:
    """Cluster branches by the multi-level vocabulary of their diffs.

    ``documents`` maps a branch name to the dict returned by
    :func:`build_documents` (or, for a single-level caller, to a token list).
    Branches with no tokens cannot be compared on content and are reported as
    excluded, never silently dropped.
    """
    normalised: dict[str, dict[str, list[str]]] = {}
    for name, value in documents.items():
        if isinstance(value, dict):
            levels = value.get("levels") or {"symbol": value.get("tokens", [])}
        else:
            levels = {"symbol": list(value)}
        if any(levels.values()):
            normalised[name] = levels
    excluded = sorted(set(documents) - set(normalised))

    empty = {
        "method": "multilevel-deterministic-hash-average-linkage",
        "document_count": len(normalised),
        "excluded_no_content": excluded,
        "levels": sorted(LEVEL_WEIGHTS),
        "clusters": [],
        "branch_assignments": {},
        "hierarchy": [],
        "level_agreement": {},
        "quality_metrics": {
            "total_clusters": len(normalised),
            "silhouette_avg": 0.0,
            "threshold": None,
            "vocabulary_size": BUCKETS,
        },
    }
    if len(normalised) < 2:
        return empty

    names = list(normalised)
    bucket_terms: dict[int, Counter[str]] = {}

    # One matrix per level, plus the weighted concatenation. Levels are hashed
    # into the same bucket space but kept as separate blocks in the combined
    # matrix, so a collision in one level cannot impersonate another level.
    level_matrices = {
        level: _hashed_matrix(
            [normalised[name].get(level, []) for name in names],
            bucket_terms,
            offset=position * BUCKETS,
        )
        for position, level in enumerate(LEVEL_WEIGHTS)
    }
    combined = _weighted_concat(level_matrices)
    combined = _drop_empty_rows(combined, names)
    kept_names = combined["names"]
    matrix = combined["matrix"]
    excluded.extend(combined["excluded"])

    if len(kept_names) < 2:
        return {**empty, "excluded_no_content": sorted(set(excluded))}

    distances = pairwise_distances(matrix, metric="cosine")
    np.fill_diagonal(distances, 0.0)

    partitions: dict[float, tuple[np.ndarray, float]] = {}
    for threshold in CUT_GRID:
        partition = _partition(distances, threshold)
        if partition is not None:
            partitions[threshold] = partition

    if not partitions:
        # No threshold separated the fleet: one content community.
        labels = np.ones(len(kept_names), dtype=int)
        best_threshold: float | None = None
        best_silhouette = 0.0
    else:
        best_threshold, (labels, best_silhouette) = max(
            partitions.items(), key=lambda item: item[1][1]
        )

    hierarchy = []
    for threshold in sorted(partitions):
        cut_labels, cut_score = partitions[threshold]
        hierarchy.append(
            {
                "threshold": threshold,
                "clusters": len(set(cut_labels.tolist())),
                "silhouette": round(cut_score, 4),
                "primary": threshold == best_threshold,
            }
        )

    assignments = {kept_names[i]: int(labels[i]) for i in range(len(kept_names))}

    clusters = []
    for label in sorted(set(labels.tolist())):
        members = [i for i, lab in enumerate(labels) if lab == label]
        member_branches = [kept_names[i] for i in members]
        if len(members) > 1:
            internal = distances[np.ix_(members, members)]
            upper = internal[np.triu_indices(len(members), k=1)]
            cohesion = 1.0 - float(np.mean(upper))
        else:
            cohesion = 1.0
        clusters.append(
            {
                "cluster_id": int(label),
                "size": len(member_branches),
                "branches": member_branches,
                "cohesion": round(cohesion, 4),
                "signature_terms": _cluster_signature(
                    matrix, labels, label, bucket_terms
                ),
            }
        )
    clusters.sort(key=lambda c: (-c["size"], c["cluster_id"]))

    # Which coarser cluster contains each of this partition's clusters.
    parental: dict[int, dict[int, int]] = {}
    for threshold in sorted(partitions):
        if threshold >= (best_threshold if best_threshold is not None else 1.0):
            continue
        coarse_labels, _ = partitions[threshold]
        mapping: dict[int, int] = {}
        for label in {int(x) for x in labels}:
            members = np.asarray([i for i, lab in enumerate(labels) if lab == label])
            parents = coarse_labels[members]
            mapping[label] = int(Counter(parents.tolist()).most_common(1)[0][0])
        parental[int(threshold * 100)] = mapping
    for cluster in clusters:
        for key, mapping in parental.items():
            cluster.setdefault("parent", {})[f"cut_{key}"] = mapping.get(
                cluster["cluster_id"]
            )

    level_agreement: dict[str, float | None] = {}
    for level, level_matrix in level_matrices.items():
        rows = [names.index(name) for name in kept_names]
        level_rows = level_matrix.tocsr()[rows]
        level_distances = pairwise_distances(level_rows, metric="cosine")
        np.fill_diagonal(level_distances, 0.0)
        level_partition = None
        for threshold in CUT_GRID:
            level_partition = _partition(level_distances, threshold)
            if level_partition is not None:
                break
        if level_partition is None:
            level_agreement[level] = None
        else:
            level_agreement[level] = round(
                float(adjusted_rand_score(labels, level_partition[0])), 4
            )

    return {
        "method": "multilevel-deterministic-hash-average-linkage",
        "hash": {
            "function": "blake2b-64",
            "buckets": BUCKETS,
            "levels": LEVEL_WEIGHTS,
            "vocabulary_learned": False,
        },
        "note": (
            "Deterministic hashed multi-level clustering over path segments and "
            "prefixes, identifier words and pairs, commit-subject words and pairs, "
            "and sub-word 4-grams. It captures shared vocabulary, not shared "
            "behaviour; use it to group a merge wave, not to prove equivalence."
        ),
        "document_count": len(kept_names),
        "excluded_no_content": sorted(set(excluded)),
        "levels": sorted(LEVEL_WEIGHTS),
        "clusters": clusters,
        "branch_assignments": assignments,
        "hierarchy": hierarchy,
        "level_agreement": level_agreement,
        "quality_metrics": {
            "total_clusters": len(clusters),
            "silhouette_avg": round(float(best_silhouette), 4),
            "threshold": best_threshold,
            "vocabulary_size": BUCKETS,
        },
    }


def _weighted_concat(matrices: dict[str, csr_matrix]) -> csr_matrix:
    """Concatenate level blocks with their weights, keeping level boundaries."""
    blocks = []
    for level, matrix in matrices.items():
        blocks.append(matrix * LEVEL_WEIGHTS[level])
    return hstack(blocks, format="csr")


def _drop_empty_rows(matrix: csr_matrix, names: list[str]) -> dict[str, Any]:
    norms = np.sqrt(np.asarray(matrix.multiply(matrix).sum(axis=1)).ravel())
    kept = [i for i, norm in enumerate(norms) if norm > 0.0]
    dropped = [names[i] for i, norm in enumerate(norms) if norm <= 0.0]
    return {
        "matrix": matrix[kept],
        "names": [names[i] for i in kept],
        "excluded": dropped,
    }


def compare_clusterings(
    metric_assignments: dict[str, int], content_assignments: dict[str, int]
) -> dict[str, Any]:
    """Measure how much the score-based and content-based views agree."""
    shared = sorted(set(metric_assignments) & set(content_assignments))
    if len(shared) < 3:
        return {"shared_branches": len(shared), "adjusted_rand_index": None}
    a = [metric_assignments[name] for name in shared]
    b = [content_assignments[name] for name in shared]
    return {
        "shared_branches": len(shared),
        "adjusted_rand_index": round(float(adjusted_rand_score(a, b)), 4),
    }
