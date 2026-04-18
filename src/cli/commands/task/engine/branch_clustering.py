import subprocess
import ast
import hashlib
import re
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict
from datetime import datetime

# Optional scientific dependencies with lazy imports and fallbacks
try:
    import numpy as np
    import scipy.cluster.hierarchy as hierarchy
    from scipy.spatial.distance import squareform

    HAS_SCIENTIFIC = True
except ImportError:
    HAS_SCIENTIFIC = False

try:
    import libcst as cst

    HAVE_LIBCST = True
except ImportError:
    HAVE_LIBCST = False


class GitAnalysisError(Exception):
    """Raised when git commands fail due to bad refs or fetching errors."""

    pass


def hash_content(code: str) -> str:
    return hashlib.md5(code.encode()).hexdigest()


# ============================================================================
# Constants & Thresholds
# ============================================================================
DEFAULT_SIMILARITY_SCORE = 0.5
MIN_BRANCH_AGE_DAYS = 1
CLUSTERING_THRESHOLD = 0.25

# Distance weights
WEIGHT_COMMIT_HISTORY = 0.35
WEIGHT_CODEBASE_STRUCTURE = 0.35
WEIGHT_DIFF_DISTANCE = 0.30


class BranchAnalyzer:
    """Analyzes a branch using ast and libcst to extract semantic features."""

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def get_changed_files(self, branch: str, base_branch: str) -> List[str]:
        """Gets all files changed between branches."""
        try:
            cmd = ["git", "diff", "--name-only", f"{base_branch}...origin/{branch}"]
            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True, check=True
            )
            files = [f for f in result.stdout.strip().split("\n") if f]
            return files
        except subprocess.CalledProcessError:
            return []

    def get_file_content(self, branch: str, filepath: str) -> str:
        """Gets the content of a file at a specific branch."""
        try:
            cmd = ["git", "show", f"origin/{branch}:{filepath}"]
            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

    def analyze_file(self, content: str) -> Dict[str, Any]:
        """Extracts features from Python code."""
        result = {
            "functions": [],
            "classes": [],
            "imports": [],
            "docstrings": [],
            "comments": [],
            "structural_hash": "",
            "content_hash": hash_content(content) if content else "",
        }

        if not content:
            return result

        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(
                    node,
                    (ast.FunctionDef, getattr(ast, "AsyncFunctionDef", type(None))),
                ):
                    result["functions"].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    result["classes"].append(node.name)
                elif isinstance(node, ast.Import):
                    for name in node.names:
                        result["imports"].append(name.name)
                elif isinstance(node, ast.ImportFrom):
                    mod = node.module or ""
                    for name in node.names:
                        result["imports"].append(f"{mod}.{name.name}")

            result["structural_hash"] = hash_content(
                ast.dump(tree, annotate_fields=False, include_attributes=False)
            )
        except SyntaxError:
            pass

        if HAVE_LIBCST:
            try:
                cst_tree = cst.parse_module(content)

                class CommentVisitor(cst.CSTVisitor):
                    def __init__(self):
                        self.comments = []

                    def visit_Comment(self, node):
                        self.comments.append(node.value)

                visitor = CommentVisitor()
                cst_tree.visit(visitor)
                result["comments"] = visitor.comments
            except SyntaxError as e:
                # Invalid syntax - skip CST parsing but log
                import logging

                logging.debug(f"CST parse skipped due to syntax: {e}")
            except Exception as e:
                import logging

                logging.warning(f"CST comment extraction failed: {e}")

        return result


class ClusterEngine:
    """
    Advanced two-stage branch clustering engine.
    Restored from historical fidelity implementation.
    """

    def __init__(self, repo_path: str = ".", mode: str = "hybrid"):
        self.repo_path = repo_path
        self.mode = mode
        self.analyzer = BranchAnalyzer(repo_path)

    def execute(
        self, branches: List[str], primary_branch: str = "origin/main"
    ) -> Dict[str, Any]:
        """
        Executes the two-stage identification and clustering pipeline.
        """
        branch_metrics = self._collect_metrics(branches, primary_branch)

        # Stage One: Similarity-based clustering (if scientific stack available)
        clusters = {}
        if HAS_SCIENTIFIC and len(branches) > 1:
            clusters = self._perform_clustering(branch_metrics)

        # Stage Two: Target assignment with tagging
        assignments = {}
        for branch in branches:
            metrics = branch_metrics[branch]
            target, confidence, reasoning, tags = self._assign_target(branch, metrics)

            assignments[branch] = {
                "target": target,
                "confidence": confidence,
                "reasoning": reasoning,
                "tags": tags,
                "cluster_id": clusters.get(branch, "Unclustered"),
                "metrics": {
                    "files_changed": len(metrics["files_changed"]),
                    "logic_volume": len(metrics["functions"]) + len(metrics["classes"]),
                },
            }

        return assignments

    def _collect_metrics(
        self, branches: List[str], primary_branch: str
    ) -> Dict[str, Any]:
        """Collects semantic and structural metrics for all branches."""
        metrics = {}
        for branch in branches:
            files = self.analyzer.get_changed_files(branch, primary_branch)
            py_files = [f for f in files if f.endswith(".py")]

            agg = {
                "files_changed": files,
                "functions": set(),
                "classes": set(),
                "imports": set(),
                "structural_hashes": set(),
                "divergence_ratio": self._get_divergence_ratio(branch, primary_branch),
            }

            for f in py_files:
                feat = self.analyzer.analyze_file(
                    self.analyzer.get_file_content(branch, f)
                )
                agg["functions"].update(feat["functions"])
                agg["classes"].update(feat["classes"])
                agg["imports"].update(feat["imports"])
                if feat["structural_hash"]:
                    agg["structural_hashes"].add(feat["structural_hash"])

            metrics[branch] = agg
        return metrics

    def _perform_clustering(self, metrics: Dict[str, Any]) -> Dict[str, str]:
        """Performs hierarchical clustering using Ward's method."""
        branches = list(metrics.keys())
        n = len(branches)
        dist_matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(i + 1, n):
                dist = self._calculate_branch_distance(
                    metrics[branches[i]], metrics[branches[j]]
                )
                dist_matrix[i][j] = dist_matrix[j][i] = dist

        condensed = squareform(dist_matrix)
        linkage_matrix = hierarchy.linkage(condensed, method="ward")
        clusters_array = hierarchy.fcluster(
            linkage_matrix, t=CLUSTERING_THRESHOLD, criterion="distance"
        )

        return {branch: f"C{cid}" for branch, cid in zip(branches, clusters_array)}

    def _calculate_branch_distance(self, m1: Dict, m2: Dict) -> float:
        """Calculates normalized distance between two branch feature sets."""
        # 1. Directory/File overlap
        f1, f2 = set(m1["files_changed"]), set(m2["files_changed"])
        overlap = len(f1 & f2) / max(len(f1 | f2), 1)
        file_dist = 1.0 - overlap

        # 2. Logic overlap (functions/classes)
        l1 = set(m1["functions"]) | set(m1["classes"])
        l2 = set(m2["functions"]) | set(m2["classes"])
        logic_overlap = len(l1 & l2) / max(len(l1 | l2), 1) if l1 or l2 else 0.5
        logic_dist = 1.0 - logic_overlap

        # Weighted distance
        return (file_dist * 0.5) + (logic_dist * 0.5)

    def _get_divergence_ratio(self, branch: str, primary: str) -> float:
        """Calculates distance from merge base vs primary commits."""
        try:
            base = subprocess.check_output(
                ["git", "merge-base", f"origin/{branch}", primary], text=True
            ).strip()
            branch_cnt = int(
                subprocess.check_output(
                    ["git", "rev-list", "--count", f"{base}..origin/{branch}"],
                    text=True,
                ).strip()
            )
            primary_cnt = int(
                subprocess.check_output(
                    ["git", "rev-list", "--count", f"{base}..{primary}"], text=True
                ).strip()
            )
            return branch_cnt / (primary_cnt + 1)
        except subprocess.CalledProcessError as e:
            # Git command failed - log and return safe default
            import logging

            logging.debug(f"Git command failed for divergence ratio: {e}")
            return 0.5
        except Exception as e:
            import logging

            logging.warning(f"Divergence ratio calculation failed: {e}")
            return 0.5

    def _assign_target(self, branch: str, metrics: Dict[str, Any]) -> tuple:
        """Heuristic-based target assignment."""
        name = branch.lower()
        tokens = re.split(r"[-_/\s\.]", name)
        files = metrics["files_changed"]
        imports = metrics["imports"]

        # 1. Orchestration Affinity
        if any(x in tokens for x in ["orch", "orchestration", "tools", "cli"]) or any(
            "taskmaster" in f or "src/cli" in f for f in files
        ):
            return (
                "orchestration-tools",
                0.9,
                "Modifies CLI/Orchestration infrastructure",
                ["tag:orchestration_branch"],
            )

        # 2. Scientific Affinity
        if (
            any(x in tokens for x in ["scientific", "ml", "ai", "model"])
            or any("python_nlp" in f or "ai_engine" in f for f in files)
            or any(x in imports for x in ["transformers", "torch", "sklearn"])
        ):
            return (
                "scientific",
                0.9,
                "Contains NLP/AI/ML logic or dependencies",
                ["tag:scientific_branch", "tag:ml_deps"],
            )

        # 3. Main/Feature fallback
        return "main", 0.6, "General feature or bugfix", ["tag:feature_branch"]
