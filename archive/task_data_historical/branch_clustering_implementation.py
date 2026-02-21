"""
Two-Stage Branch Identification and Clustering Implementation

This module implements the enhanced branch categorization framework
(Task 75 enhancement) with:
- Stage One: Similarity-based clustering
- Stage Two: Target assignment with tagging

The framework analyzes Git branches to determine their similarity and
assigns them to appropriate integration targets (main, scientific, orchestration-tools).
"""

import json
import subprocess
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform

# ============================================================================
# Constants
# ============================================================================

# Commit analysis constants
DEFAULT_SIMILARITY_SCORE = 0.5
MAX_ENTROPY_DIVISOR = 5.0
MIN_BRANCH_AGE_DAYS = 1

# Target assignment thresholds
HEURISTIC_CONFIDENCE_THRESHOLD = 0.95
ORCHESTRATION_AFFINITY_THRESHOLD = 0.75
SCIENTIFIC_AFFINITY_THRESHOLD = 0.70
MAIN_AFFINITY_THRESHOLD = 0.65

# Clustering parameters
DEFAULT_CLUSTERING_THRESHOLD = 0.25
MIN_CLUSTER_SIZE = 2

# Distance calculation weights (sum should equal 1.0)
WEIGHT_COMMIT_HISTORY = 0.35
WEIGHT_CODEBASE_STRUCTURE = 0.35
WEIGHT_DIFF_DISTANCE = 0.30

# Complexity thresholds
SIMPLE_DIVERGENCE_THRESHOLD = 0.1
SIMPLE_CONFLICT_PROBABILITY = 0.1
MODERATE_DIVERGENCE_THRESHOLD = 0.5
MODERATE_CONFLICT_PROBABILITY = 0.3

# Integration targets
TARGET_MAIN = "main"
TARGET_SCIENTIFIC = "scientific"
TARGET_ORCHESTRATION_TOOLS = "orchestration-tools"

# ============================================================================
# Data Classes
# ============================================================================


@dataclass
class CommitMetrics:
    """Metrics derived from commit history analysis"""

    merge_base_distance: int
    divergence_ratio: float
    commit_frequency: float
    shared_contributors: int
    message_similarity_score: float
    branch_age_days: int


@dataclass
class CodebaseMetrics:
    """Metrics from codebase structure analysis"""

    core_directories: List[str]
    file_type_distribution: Dict[str, int]
    code_volume: int  # lines added/deleted
    affects_core: bool
    affects_tests: bool
    affects_infrastructure: bool
    documentation_intensity: float
    config_change_count: int


@dataclass
class DiffMetrics:
    """Metrics from diff distance calculations"""

    file_overlap_ratio: float  # 0.0-1.0
    edit_distance: int
    change_proximity_score: float
    conflict_probability: float  # 0.0-1.0


@dataclass
class MigrationMetrics:
    """Metrics from backend → src migration analysis"""

    migration_status: str  # 'not_started', 'in_progress', 'complete', 'not_applicable'
    has_backend_imports: bool
    has_src_imports: bool
    migration_ratio: float  # 0.0-1.0
    backend_file_count: int
    src_file_count: int


@dataclass
class BranchMetrics:
    """Complete metrics for a branch"""

    branch_name: str
    commit_history: CommitMetrics
    codebase_structure: CodebaseMetrics
    migration_metrics: MigrationMetrics
    timestamp: str
    conflict_probability: float = 0.0


@dataclass
class ClusterAssignment:
    """Result of clustering algorithm"""

    branch: str
    cluster_id: str
    distance_to_centroid: float


@dataclass
class TagAssignment:
    """Tags for a branch based on cluster and target"""

    primary_target: str  # 'main', 'scientific', 'orchestration-tools'
    secondary_targets: List[str]
    tags: List[str]
    confidence: float
    reasoning: str


# ============================================================================
# Stage One: Branch Similarity Analysis
# ============================================================================


class CommitHistoryAnalyzer:
    """Analyzes Git commit patterns and history divergence"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def calculate_metrics(
        self, branch_name: str, primary_branch: str = "origin/main"
    ) -> CommitMetrics:
        """Calculate commit history metrics for a branch"""

        try:
            # 1. Find merge base and calculate divergence
            merge_base = self._get_merge_base(branch_name, primary_branch)
            merge_base_distance = self._count_commits(f"{merge_base}..origin/{branch_name}")

            # 2. Calculate divergence ratio
            primary_commits_since = self._count_commits(f"{merge_base}..{primary_branch}")
            divergence_ratio = merge_base_distance / (primary_commits_since + 1)

            # 3. Commit frequency (commits per day)
            branch_age = self._get_branch_age_days(branch_name)
            commit_frequency = merge_base_distance / max(branch_age, 1)

            # 4. Shared contributors
            shared_contributors = self._count_shared_contributors(branch_name, primary_branch)

            # 5. Commit message similarity
            message_similarity = self._calculate_message_similarity(
                branch_name, primary_branch, merge_base
            )

            return CommitMetrics(
                merge_base_distance=merge_base_distance,
                divergence_ratio=divergence_ratio,
                commit_frequency=commit_frequency,
                shared_contributors=shared_contributors,
                message_similarity_score=message_similarity,
                branch_age_days=branch_age,
            )

        except subprocess.CalledProcessError as e:
            print(f"Error analyzing {branch_name}: {e}")
            return CommitMetrics(0, 0.0, 0.0, 0, 0.0, 0)

    def _get_merge_base(self, branch1: str, branch2: str) -> str:
        """Get merge base between two branches"""
        result = subprocess.run(
            ["git", "merge-base", f"origin/{branch1}", branch2],
            capture_output=True,
            text=True,
            cwd=self.repo_path,
            check=True,
        )
        return result.stdout.strip()

    def _count_commits(self, ref_range: str) -> int:
        """Count commits in a git ref range"""
        result = subprocess.run(
            ["git", "rev-list", "--count", ref_range],
            capture_output=True,
            text=True,
            cwd=self.repo_path,
            check=True,
        )
        return int(result.stdout.strip())

    def _get_branch_age_days(self, branch_name: str) -> int:
        """Calculate age of branch in days"""
        result = subprocess.run(
            ["git", "log", "--reverse", "--format=%ai", f"origin/{branch_name}"],
            capture_output=True,
            text=True,
            cwd=self.repo_path,
            check=True,
        )
        lines = result.stdout.strip().split("\n")
        if not lines:
            return MIN_BRANCH_AGE_DAYS

        try:
            # Try robust parsing first if available or standard isoformat
            first_commit_date = datetime.fromisoformat(lines[0].replace(" +0000", "+00:00"))
        except ValueError:
            # Fallback for simple cases
            first_commit_date = datetime.now()

        age = (datetime.now(first_commit_date.tzinfo) - first_commit_date).days
        return max(age, MIN_BRANCH_AGE_DAYS)

    def _count_shared_contributors(self, branch1: str, branch2: str) -> int:
        """Count shared contributors between branches"""
        result1 = subprocess.run(
            ["git", "log", "--format=%an", f"origin/{branch1}"],
            capture_output=True,
            text=True,
            cwd=self.repo_path,
        )
        result2 = subprocess.run(
            ["git", "log", "--format=%an", branch2],
            capture_output=True,
            text=True,
            cwd=self.repo_path,
        )

        contributors1 = set(result1.stdout.strip().split("\n"))
        contributors2 = set(result2.stdout.strip().split("\n"))

        return len(contributors1 & contributors2)

    def _calculate_message_similarity(
        self, branch_name: str, primary_branch: str, merge_base: str
    ) -> float:
        """Calculate semantic similarity of commit messages"""
        try:
            result = subprocess.run(
                ["git", "log", "--format=%s", f"{merge_base}..origin/{branch_name}"],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )

            messages = result.stdout.strip().split("\n")
            if len(messages) < 2:
                return DEFAULT_SIMILARITY_SCORE

            # Count conventional commit types to analyze message patterns
            type_counts = defaultdict(int)
            for msg in messages:
                if ":" in msg:
                    prefix = msg.split(":")[0].lower()
                    type_counts[prefix] += 1

            # Calculate entropy and convert to similarity score (0-1 range)
            if type_counts:
                entropy = self._calculate_message_entropy(type_counts, len(messages))
                similarity = max(0.0, 1.0 - (entropy / MAX_ENTROPY_DIVISOR))
            else:
                similarity = DEFAULT_SIMILARITY_SCORE

            return min(1.0, max(0.0, similarity))

        except Exception as e:
            print(f"Error calculating message similarity: {e}")
            return DEFAULT_SIMILARITY_SCORE

    def _calculate_message_entropy(self, type_counts: Dict[str, int], total_messages: int) -> float:
        """Calculate entropy of commit message types"""
        return sum(
            (count / total_messages) * np.log2(count / total_messages + 1)
            for count in type_counts.values()
        )


class CodebaseStructureAnalyzer:
    """Analyzes file patterns, directory structure, and code characteristics"""

    CORE_DIRS = {"src", "lib", "core", "orchestration", "scientific", "ai", "ml"}
    TEST_DIRS = {"test", "tests", "__tests__", "spec", "specs"}
    INFRA_DIRS = {"infra", "infrastructure", "docker", ".github", "config", "deploy"}
    DOC_DIRS = {"docs", "documentation", "wiki"}
    CONFIG_PATTERNS = {".yaml", ".yml", ".json", ".toml", ".ini", ".env"}

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def calculate_metrics(
        self, branch_name: str, primary_branch: str = "origin/main"
    ) -> CodebaseMetrics:
        """Calculate codebase structure metrics for a branch"""

        try:
            # Get changed files
            merge_base = self._get_merge_base(branch_name, primary_branch)
            changed_files = self._get_changed_files(merge_base, f"origin/{branch_name}")

            # Categorize files
            core_dirs = set()
            file_type_dist = defaultdict(int)
            code_volume = 0
            config_count = 0
            doc_files = 0
            test_files = 0

            for file_path in changed_files:
                # Extract directory
                parts = file_path.split("/")
                if parts:
                    for part in parts[:-1]:
                        if self._is_core_dir(part):
                            core_dirs.add(part)

                # File type distribution
                ext = file_path.split(".")[-1] if "." in file_path else "none"
                file_type_dist[ext] += 1

                # Categorize by directory
                if any(td in file_path for td in self.TEST_DIRS):
                    test_files += 1
                if any(cd in file_path for cd in self.CONFIG_PATTERNS):
                    config_count += 1
                if any(dd in file_path for dd in self.DOC_DIRS):
                    doc_files += 1

            # Calculate code volume (approximate)
            code_volume = self._calculate_code_volume(merge_base, f"origin/{branch_name}")

            # Documentation intensity
            doc_intensity = (doc_files / max(len(changed_files), 1)) if changed_files else 0.0

            return CodebaseMetrics(
                core_directories=list(core_dirs),
                file_type_distribution=dict(file_type_dist),
                code_volume=code_volume,
                affects_core=len(core_dirs) > 0,
                affects_tests=test_files > 0,
                affects_infrastructure=(any(id in str(changed_files) for id in self.INFRA_DIRS)),
                documentation_intensity=doc_intensity,
                config_change_count=config_count,
            )

        except Exception as e:
            print(f"Error analyzing codebase structure: {e}")
            return CodebaseMetrics([], {}, 0, False, False, False, 0.0, 0)

    def _is_core_dir(self, dirname: str) -> bool:
        """Check if directory is a core directory"""
        return dirname.lower() in self.CORE_DIRS

    def _get_changed_files(self, ref1: str, ref2: str) -> List[str]:
        """Get list of changed files between two refs"""
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{ref1}..{ref2}"],
            capture_output=True,
            text=True,
            cwd=self.repo_path,
        )
        return result.stdout.strip().split("\n") if result.stdout.strip() else []

    def _get_merge_base(self, branch1: str, branch2: str) -> str:
        """Get merge base between two branches"""
        result = subprocess.run(
            ["git", "merge-base", f"origin/{branch1}", branch2],
            capture_output=True,
            text=True,
            cwd=self.repo_path,
            check=True,
        )
        return result.stdout.strip()

    def _calculate_code_volume(self, ref1: str, ref2: str) -> int:
        """Calculate approximate code volume (lines added + deleted)"""
        result = subprocess.run(
            ["git", "diff", "--numstat", f"{ref1}..{ref2}"],
            capture_output=True,
            text=True,
            cwd=self.repo_path,
        )

        total = 0
        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split("\t")
                if len(parts) >= 3:
                    try:
                        added = int(parts[0]) if parts[0] != "-" else 0
                        deleted = int(parts[1]) if parts[1] != "-" else 0
                        total += added + deleted
                    except ValueError:
                        pass

        return total


class DiffDistanceCalculator:
    """Calculates file and code change distance between branches"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def calculate_all_pairs(
        self, branches: List[str], primary_branch: str = "origin/main"
    ) -> Dict[Tuple[str, str], DiffMetrics]:
        """Calculate pairwise diff metrics for all branches"""

        metrics = {}
        for i, branch1 in enumerate(branches):
            for branch2 in branches[i + 1 :]:
                try:
                    m = self.calculate_metrics(branch1, branch2, primary_branch)
                    metrics[(branch1, branch2)] = m
                    # Symmetric: same distance both ways
                    metrics[(branch2, branch1)] = m
                except Exception as e:
                    print(f"Error comparing {branch1} and {branch2}: {e}")
                    # Default high distance for error cases
                    default = DiffMetrics(0.0, 999, 0.0, 0.99)
                    metrics[(branch1, branch2)] = default
                    metrics[(branch2, branch1)] = default

        return metrics

    def calculate_metrics(
        self, branch1: str, branch2: str, primary_branch: str = "origin/main"
    ) -> DiffMetrics:
        """Calculate diff metrics between two branches"""

        # Get changed files for each branch
        files1 = set(self._get_changed_files(primary_branch, f"origin/{branch1}"))
        files2 = set(self._get_changed_files(primary_branch, f"origin/{branch2}"))

        # File overlap
        overlap = len(files1 & files2)
        total_files = len(files1 | files2)
        file_overlap_ratio = overlap / max(total_files, 1)

        # Edit distance (Levenshtein on file list)
        edit_distance = self._levenshtein_distance(sorted(files1), sorted(files2))

        # Change proximity
        proximity = self._calculate_change_proximity(files1, files2)

        # Conflict likelihood
        conflict_prob = self._estimate_conflict_probability(
            branch1, branch2, overlap, file_overlap_ratio
        )

        return DiffMetrics(
            file_overlap_ratio=file_overlap_ratio,
            edit_distance=edit_distance,
            change_proximity_score=proximity,
            conflict_probability=conflict_prob,
        )

    def _get_changed_files(self, ref1: str, ref2: str) -> List[str]:
        """Get list of changed files"""
        try:
            merge_base = subprocess.run(
                ["git", "merge-base", ref1, ref2],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
                check=True,
            ).stdout.strip()

            result = subprocess.run(
                ["git", "diff", "--name-only", f"{merge_base}..{ref2}"],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )
            return result.stdout.strip().split("\n") if result.stdout.strip() else []
        except Exception as e:
            print(f"Error getting changed files: {e}")
            return []

    def _levenshtein_distance(self, list1: List[str], list2: List[str]) -> int:
        """Calculate Levenshtein distance between two lists"""
        m, n = len(list1), len(list2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if list1[i - 1] == list2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],  # deletion
                        dp[i][j - 1],  # insertion
                        dp[i - 1][j - 1],  # substitution
                    )

        return dp[m][n]

    def _calculate_change_proximity(self, files1: Set[str], files2: Set[str]) -> float:
        """Calculate proximity score for code changes"""

        if not files1 or not files2:
            return 0.0

        # Extract directory paths from files
        dirs1 = {"/".join(f.split("/")[:-1]) for f in files1}
        dirs2 = {"/".join(f.split("/")[:-1]) for f in files2}

        # Proximity = overlap of parent directories
        dir_overlap = len(dirs1 & dirs2)
        dir_total = len(dirs1 | dirs2)

        proximity = dir_overlap / max(dir_total, 1)
        return min(1.0, proximity)

    def _estimate_conflict_probability(
        self, branch1: str, branch2: str, file_overlap: int, overlap_ratio: float
    ) -> float:
        """Estimate probability of merge conflict"""

        # Base probability on file overlap
        if overlap_ratio == 0:
            return 0.0

        # More overlap = higher conflict probability
        # But diminishing returns
        base_prob = min(overlap_ratio * 1.5, 1.0)

        # Adjust by specific file types with high conflict likelihood
        # (files that are often conflict-prone)

        return min(1.0, max(0.0, base_prob))


# ============================================================================
# Migration Analysis
# ============================================================================


class MigrationAnalyzer:
    """Analyzes backend → src migration patterns in Git branches"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.backend_imports = {"from backend", "import backend"}
        self.src_imports = {"from src", "import src"}

    def analyze_migration(
        self, branch_name: str, primary_branch: str = "origin/main"
    ) -> MigrationMetrics:
        """
        Analyze migration patterns in a branch.

        Detects backend → src migration by checking for:
        - Backend import statements
        - Src import statements
        - Backend directory changes
        - Src directory changes

        Returns:
            MigrationMetrics with migration status and statistics
        """

        try:
            merge_base = self._get_merge_base(branch_name, primary_branch)
            changed_files = self._get_changed_files(merge_base, f"origin/{branch_name}")

            # Check for migration indicators
            has_backend_imports = self._check_backend_imports(changed_files)
            has_src_imports = self._check_src_imports(changed_files)
            has_backend_dir = any("backend/" in f for f in changed_files)
            has_src_dir = any("src/" in f for f in changed_files)

            # Count files by directory
            backend_file_count = sum(1 for f in changed_files if "backend/" in f)
            src_file_count = sum(1 for f in changed_files if "src/" in f)

            # Calculate migration ratio
            total_files = len(changed_files)
            migration_ratio = (backend_file_count + src_file_count) / max(total_files, 1)

            # Determine migration status
            if has_backend_imports and has_src_imports:
                status = "in_progress"
            elif has_src_imports and not has_backend_imports:
                status = "complete"
            elif has_backend_imports and not has_src_imports:
                status = "not_started"
            else:
                status = "not_applicable"

            return MigrationMetrics(
                migration_status=status,
                has_backend_imports=has_backend_imports,
                has_src_imports=has_src_imports,
                migration_ratio=migration_ratio,
                backend_file_count=backend_file_count,
                src_file_count=src_file_count,
            )

        except subprocess.CalledProcessError as e:
            print(f"Error analyzing migration for {branch_name}: {e}")
            return MigrationMetrics(
                migration_status="not_applicable",
                has_backend_imports=False,
                has_src_imports=False,
                migration_ratio=0.0,
                backend_file_count=0,
                src_file_count=0,
            )

    def _get_merge_base(self, branch1: str, branch2: str) -> str:
        """Get merge base between two branches"""
        result = subprocess.run(
            ["git", "merge-base", f"origin/{branch1}", branch2],
            capture_output=True,
            text=True,
            cwd=self.repo_path,
            check=True,
        )
        return result.stdout.strip()

    def _get_changed_files(self, ref1: str, ref2: str) -> List[str]:
        """Get list of changed files between two refs"""
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{ref1}..{ref2}"],
            capture_output=True,
            text=True,
            cwd=self.repo_path,
        )
        return result.stdout.strip().split("\n") if result.stdout.strip() else []

    def _check_backend_imports(self, files: List[str]) -> bool:
        """Check if files contain backend imports"""
        for file_path in files:
            if not file_path.endswith(".py"):
                continue
            try:
                full_path = Path(self.repo_path) / file_path
                if full_path.exists():
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if any(imp in content for imp in self.backend_imports):
                            return True
            except Exception:
                continue
        return False

    def _check_src_imports(self, files: List[str]) -> bool:
        """Check if files contain src imports"""
        for file_path in files:
            if not file_path.endswith(".py"):
                continue
            try:
                full_path = Path(self.repo_path) / file_path
                if full_path.exists():
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if any(imp in content for imp in self.src_imports):
                            return True
            except Exception:
                continue
        return False


# ============================================================================
# Stage One: Clustering
# ============================================================================


class BranchClusterer:
    """
    Performs hierarchical clustering on branch metrics using Ward's method.

    Clustering considers three weighted dimensions:
    - Commit history similarity (35% weight)
    - Codebase structure similarity (35% weight)
    - Diff distance/conflict probability (30% weight)
    """

    def cluster_branches(
        self,
        branch_metrics: Dict[str, BranchMetrics],
        diff_metrics: Dict[Tuple[str, str], DiffMetrics],
    ) -> Dict[str, List[str]]:
        """
        Cluster branches using hierarchical clustering with Ward's method.

        Process:
        1. Build pairwise distance matrix from branch metrics
        2. Perform hierarchical clustering using Ward's linkage
        3. Cut dendrogram at threshold to form clusters
        4. Return mapping of cluster IDs to branch lists

        Returns:
            Dictionary mapping cluster IDs to lists of branch names
        """

        branches = list(branch_metrics.keys())
        n = len(branches)

        # Build symmetric distance matrix for all branch pairs
        distance_matrix = np.zeros((n, n))

        for i, b1 in enumerate(branches):
            for j, b2 in enumerate(branches):
                if i == j:
                    distance_matrix[i][j] = 0
                elif i < j:
                    # Calculate weighted distance using commit, codebase, and diff metrics
                    dist = self._calculate_distance(
                        branch_metrics[b1], branch_metrics[b2], diff_metrics.get((b1, b2))
                    )
                    distance_matrix[i][j] = dist
                    distance_matrix[j][i] = dist

        # Convert to condensed form required by scipy's hierarchical clustering
        condensed = squareform(distance_matrix)

        # Perform hierarchical clustering using Ward's method
        # Ward's method minimizes variance within clusters
        linkage_matrix = linkage(condensed, method="ward")

        # Cut dendrogram at threshold to form discrete clusters
        clusters_array = fcluster(
            linkage_matrix, t=DEFAULT_CLUSTERING_THRESHOLD, criterion="distance"
        )

        # Group branches by their assigned cluster ID
        clusters = defaultdict(list)
        for branch, cluster_id in zip(branches, clusters_array):
            clusters[f"C{cluster_id}"].append(branch)

        return dict(clusters)

    def _calculate_distance(
        self, metrics1: BranchMetrics, metrics2: BranchMetrics, diff_metrics: DiffMetrics = None
    ) -> float:
        """
        Calculate weighted distance between two branches.

        Distance is computed as a weighted average of three dimensions:
        - Commit history distance (35%)
        - Codebase structure distance (35%)
        - Diff distance/conflict probability (30%)

        Returns:
            Weighted distance value between 0.0 (identical) and 1.0 (completely different)
        """

        # Normalize individual metrics to 0-1 scale
        commit_dist = self._normalize_commit_distance(
            metrics1.commit_history, metrics2.commit_history
        )

        codebase_dist = self._normalize_codebase_distance(
            metrics1.codebase_structure, metrics2.codebase_structure
        )

        # Use default distance if diff metrics unavailable
        diff_dist = (
            self._normalize_diff_distance(diff_metrics)
            if diff_metrics
            else DEFAULT_SIMILARITY_SCORE
        )

        # Calculate weighted combination of distances
        total_distance = (
            WEIGHT_COMMIT_HISTORY * commit_dist
            + WEIGHT_CODEBASE_STRUCTURE * codebase_dist
            + WEIGHT_DIFF_DISTANCE * diff_dist
        )

        return total_distance

    def _normalize_commit_distance(self, m1: CommitMetrics, m2: CommitMetrics) -> float:
        """Normalize commit history distance"""

        # Components
        divergence_dist = abs(m1.divergence_ratio - m2.divergence_ratio)
        message_sim_dist = abs(m1.message_similarity_score - m2.message_similarity_score)
        contributor_dist = abs(m1.shared_contributors - m2.shared_contributors) / max(
            max(m1.shared_contributors, m2.shared_contributors), 1
        )

        return divergence_dist * 0.5 + message_sim_dist * 0.3 + contributor_dist * 0.2

    def _normalize_codebase_distance(self, c1: CodebaseMetrics, c2: CodebaseMetrics) -> float:
        """Normalize codebase structure distance"""

        # Directory similarity
        dirs1 = set(c1.core_directories)
        dirs2 = set(c2.core_directories)
        dir_dist = (
            1.0 - (len(dirs1 & dirs2) / max(len(dirs1 | dirs2), 1)) if dirs1 or dirs2 else 0.5
        )

        # File type distribution similarity
        types1 = set(c1.file_type_distribution.keys())
        types2 = set(c2.file_type_distribution.keys())
        type_dist = (
            1.0 - (len(types1 & types2) / max(len(types1 | types2), 1)) if types1 or types2 else 0.5
        )

        # Code volume similarity (log scale)
        vol1 = np.log1p(c1.code_volume)
        vol2 = np.log1p(c2.code_volume)
        vol_max = max(vol1, vol2)
        vol_dist = abs(vol1 - vol2) / max(vol_max, 1)

        return dir_dist * 0.4 + type_dist * 0.4 + vol_dist * 0.2

    def _normalize_diff_distance(self, diff: DiffMetrics) -> float:
        """Normalize diff distance"""

        # Higher overlap = lower distance
        overlap_dist = 1.0 - diff.file_overlap_ratio

        # Edit distance (log scale)
        edit_dist = diff.edit_distance
        edit_dist_norm = edit_dist / max(edit_dist, 10)  # Normalize

        # Conflict probability
        conflict_dist = diff.conflict_probability

        return overlap_dist * 0.5 + edit_dist_norm * 0.3 + conflict_dist * 0.2


# ============================================================================
# Stage Two: Target Assignment and Tagging
# ============================================================================


class IntegrationTargetAssigner:
    """Assigns branches to integration targets with tagging"""

    HEURISTIC_RULES = [
        (
            lambda b: any(x in b.lower() for x in ["orchestration", "orchestration-tools"]),
            "orchestration-tools",
            "Branch name contains orchestration keyword",
        ),
        (
            lambda b: any(x in b.lower() for x in ["scientific", "ml", "ai", "model", "data"]),
            "scientific",
            "Branch name contains scientific keyword",
        ),
    ]

    AFFINITY_RULES = {
        "orchestration-tools": {
            "patterns": ["orchestration/", "orchestration-tools", "tools/"],
            "weight": 0.9,
        },
        "scientific": {"patterns": ["scientific/", "ai/", "ml/", "model/", "data/"], "weight": 0.9},
        "main": {"patterns": ["src/", "lib/", "utils/", "core/"], "weight": 0.7},
    }

    def assign_target(
        self, branch_name: str, metrics: BranchMetrics
    ) -> TagAssignment:
        """
        Assign integration target and tags to branch using a two-step process:
        1. Check heuristic rules (branch name patterns) for high-confidence matches
        2. Calculate affinity scores based on codebase structure and patterns
        """

        # Step 1: Apply heuristic rules for high-confidence matches
        # These rules check branch names for keywords indicating target
        for predicate, target, reason in self.HEURISTIC_RULES:
            if predicate(branch_name):
                return TagAssignment(
                    primary_target=target,
                    secondary_targets=[],
                    tags=self._generate_tags(branch_name, metrics, target),
                    confidence=HEURISTIC_CONFIDENCE_THRESHOLD,
                    reasoning=reason,
                )

        # Step 2: Calculate affinity scores for each target
        # Affinity is based on directory patterns and file structure
        affinities = self._calculate_affinities(branch_name, metrics)

        # Select target with highest affinity score
        primary_target = max(affinities.items(), key=lambda x: x[1])[0]

        # Extract confidence and generate reasoning
        confidence = affinities[primary_target]
        reasoning = self._generate_reasoning(affinities, branch_name)

        # Identify secondary targets (other targets with reasonable affinity)
        secondary_targets = [
            t for t, score in affinities.items() if t != primary_target and score > 0.5
        ]

        return TagAssignment(
            primary_target=primary_target,
            secondary_targets=secondary_targets,
            tags=self._generate_tags(branch_name, metrics, primary_target),
            confidence=confidence,
            reasoning=reasoning,
        )

    def _calculate_affinities(self, branch_name: str, metrics: BranchMetrics) -> Dict[str, float]:
        """Calculate affinity scores for each target"""

        affinities = dict.fromkeys(["main", "scientific", "orchestration-tools"], 0.0)

        # Check directory patterns
        dirs = metrics.codebase_structure.core_directories

        for target, rules in self.AFFINITY_RULES.items():
            pattern_match_score = sum(
                1 for pattern in rules["patterns"] if any(pattern.rstrip("/") == d for d in dirs)
            ) / max(len(rules["patterns"]), 1)

            affinities[target] = (
                pattern_match_score * rules["weight"] * 0.7
                + self._get_heuristic_score(branch_name, target) * 0.3
            )

        # Normalize
        total = sum(affinities.values())
        if total > 0:
            affinities = {t: score / total for t, score in affinities.items()}
        else:
            affinities["main"] = 1.0

        return affinities

    def _get_heuristic_score(self, branch_name: str, target: str) -> float:
        """Get heuristic match score"""

        name_lower = branch_name.lower()
        target_keywords = {
            "main": ["main", "feature", "feat"],
            "scientific": ["scientific", "ml", "ai", "model", "data"],
            "orchestration-tools": ["orchestration", "tools", "orch"],
        }

        keywords = target_keywords.get(target, [])
        match_count = sum(1 for kw in keywords if kw in name_lower)

        return match_count / max(len(keywords), 1)

    def _generate_tags(self, branch_name: str, metrics: BranchMetrics, target: str) -> List[str]:
        """Generate comprehensive tags for branch"""

        tags = []

        # Primary target tag
        target_tag = f'tag:{target.replace("-", "_")}_branch'
        tags.append(target_tag)

        # Determine execution context based on conflict probability
        conflict_prob = metrics.conflict_probability if hasattr(metrics, "conflict_probability") else 0.15
        if conflict_prob < SIMPLE_CONFLICT_PROBABILITY:
            tags.append("tag:parallel_safe")
        else:
            tags.append("tag:sequential_required")

        # Determine complexity based on divergence ratio
        divergence = metrics.commit_history.divergence_ratio
        if divergence < SIMPLE_DIVERGENCE_THRESHOLD:
            tags.append("tag:simple_merge")
        elif divergence < MODERATE_DIVERGENCE_THRESHOLD:
            tags.append("tag:moderate_complexity")
        else:
            tags.append("tag:high_complexity")

        # Add content type tags based on affected areas
        codebase = metrics.codebase_structure
        if codebase.affects_core:
            tags.append("tag:core_code_changes")
        if codebase.affects_tests:
            tags.append("tag:test_changes")
        if codebase.config_change_count > 0:
            tags.append("tag:config_changes")
        if codebase.documentation_intensity > 0.5:
            tags.append("tag:documentation_only")

        # Validation requirements
        if codebase.affects_core:
            tags.append("tag:requires_e2e_testing")
            tags.append("tag:requires_unit_tests")

        # Migration-related tags
        if hasattr(metrics, "migration_metrics"):
            migration = metrics.migration_metrics
            if migration.migration_status == "in_progress":
                tags.append("tag:migration_in_progress")
            elif migration.migration_status == "complete":
                tags.append("tag:migration_complete")
            elif migration.migration_status == "not_started":
                tags.append("tag:migration_required")

            if migration.migration_ratio > 0.5:
                tags.append("tag:high_migration_impact")

        return tags

    def _generate_reasoning(self, affinities: Dict[str, float], branch_name: str) -> str:
        """Generate human-readable reasoning"""

        sorted_affinities = sorted(affinities.items(), key=lambda x: x[1], reverse=True)

        primary = sorted_affinities[0]
        secondary = sorted_affinities[1] if len(sorted_affinities) > 1 else None

        reason = f"Primary affinity {primary[0]} ({primary[1]:.2%})"

        if secondary and secondary[1] > 0.3:
            reason += f", secondary {secondary[0]} ({secondary[1]:.2%})"

        return reason


# ============================================================================
# Integration and Output
# ============================================================================


class BranchClusteringEngine:
    """Complete two-stage branch clustering engine with multiple execution modes"""

    def __init__(self, repo_path: str = ".", mode: str = "clustering", config: Dict = None):
        """
        Initialize the clustering engine with execution mode.

        Args:
            repo_path: Path to Git repository
            mode: Execution mode - 'identification', 'clustering', or 'hybrid'
            config: Optional configuration dictionary
        """
        self.repo_path = repo_path
        self.mode = self._validate_mode(mode)
        self.config = config or {}

        # Initialize analyzers
        self.commit_analyzer = CommitHistoryAnalyzer(repo_path)
        self.codebase_analyzer = CodebaseStructureAnalyzer(repo_path)
        self.diff_calculator = DiffDistanceCalculator(repo_path)
        self.migration_analyzer = MigrationAnalyzer(repo_path)
        self.clusterer = BranchClusterer()
        self.assigner = IntegrationTargetAssigner()

    def _validate_mode(self, mode: str) -> str:
        """Validate execution mode parameter"""
        valid_modes = {"identification", "clustering", "hybrid"}
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode: {mode}. Must be one of {valid_modes}")
        return mode

    def execute(self, branches: List[str], primary_branch: str = "origin/main") -> Dict:
        """
        Execute pipeline based on configured mode.

        Args:
            branches: List of branch names to analyze
            primary_branch: Primary branch for comparison

        Returns:
            Results dictionary with format depending on execution mode
        """
        if self.mode == "identification":
            return self.execute_identification_pipeline(branches, primary_branch)
        elif self.mode == "clustering":
            categorized, clustering = self.execute_full_pipeline(branches, primary_branch)
            return {"categorized": categorized, "clustering": clustering}
        elif self.mode == "hybrid":
            return self.execute_hybrid_pipeline(branches, primary_branch)
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

    def execute_identification_pipeline(
        self, branches: List[str], primary_branch: str = "origin/main"
    ) -> Dict:
        """
        Execute simple identification pipeline (I2.T4 style).

        This mode focuses on quick branch analysis without clustering,
        suitable for simple identification use cases.

        Returns:
            Dictionary with simple branch categorization results
        """
        print("=" * 70)
        print("IDENTIFICATION MODE: Simple Branch Analysis")
        print("=" * 70)

        results = []
        for branch in branches:
            print(f"Analyzing {branch}...")

            # Calculate metrics
            commit_metrics = self.commit_analyzer.calculate_metrics(branch, primary_branch)
            codebase_metrics = self.codebase_analyzer.calculate_metrics(branch, primary_branch)
            migration_metrics = self.migration_analyzer.analyze_migration(branch, primary_branch)

            # Create branch metrics
            metrics = BranchMetrics(
                branch_name=branch,
                commit_history=commit_metrics,
                codebase_structure=codebase_metrics,
                migration_metrics=migration_metrics,
                timestamp=datetime.now().isoformat(),
            )

            # Simple target assignment
            assignment = self.assigner.assign_target(branch, metrics)

            results.append(
                {
                    "branch": branch,
                    "target": assignment.primary_target,
                    "confidence": assignment.confidence,
                    "reasoning": assignment.reasoning,
                    "tags": assignment.tags,
                    "metrics": {
                        "commit_history": asdict(commit_metrics),
                        "codebase_structure": asdict(codebase_metrics),
                        "migration": asdict(migration_metrics),
                    },
                }
            )

        return {"branches": results, "total_branches": len(results), "mode": "identification"}

    def execute_hybrid_pipeline(
        self, branches: List[str], primary_branch: str = "origin/main"
    ) -> Dict:
        """
        Execute hybrid pipeline (identification with optional clustering).

        This mode provides both simple identification and full clustering results,
        giving users the flexibility to choose the level of detail they need.

        Returns:
            Dictionary containing both identification and clustering results
        """
        print("=" * 70)
        print("HYBRID MODE: Identification with Optional Clustering")
        print("=" * 70)

        # First, run identification pipeline
        identification_results = self.execute_identification_pipeline(branches, primary_branch)

        # Check if clustering is enabled
        enable_clustering = self.config.get("enable_clustering", True)

        if enable_clustering:
            print("\n" + "=" * 70)
            print("Running Clustering Analysis")
            print("=" * 70)

            # Run clustering pipeline
            categorized, clustering = self.execute_full_pipeline(branches, primary_branch)

            # Merge results
            return {
                "identification": identification_results,
                "clustering": {"categorized": categorized, "details": clustering},
                "mode": "hybrid_with_clustering",
            }
        else:
            return {
                "identification": identification_results,
                "mode": "hybrid_no_clustering",
            }

    def execute_full_pipeline(
        self, branches: List[str], primary_branch: str = "origin/main"
    ) -> Tuple[List[Dict], Dict]:
        """
        Execute full two-stage clustering pipeline:
        Stage One: Analyze branch similarity through commit history, codebase structure, and diff metrics
        Stage Two: Assign integration targets and generate comprehensive tags

        Returns:
            Tuple containing:
            - List of categorized branches with targets, tags, and metrics
            - Dictionary with clustering details and quality metrics
        """

        print("=" * 70)
        print("STAGE ONE: Branch Similarity Analysis")
        print("=" * 70)

        # Analyze each branch to collect comprehensive metrics
        branch_metrics = {}
        for branch in branches:
            print(f"Analyzing {branch}...")
            # Calculate all metrics including migration
            commit_metrics = self.commit_analyzer.calculate_metrics(branch, primary_branch)
            codebase_metrics = self.codebase_analyzer.calculate_metrics(branch, primary_branch)
            migration_metrics = self.migration_analyzer.analyze_migration(branch, primary_branch)

            metrics = BranchMetrics(
                branch_name=branch,
                commit_history=commit_metrics,
                codebase_structure=codebase_metrics,
                migration_metrics=migration_metrics,
                timestamp=datetime.now().isoformat(),
            )
            branch_metrics[branch] = metrics

        # Calculate pairwise diff metrics between all branches
        print("Calculating pairwise differences...")
        diff_metrics = self.diff_calculator.calculate_all_pairs(branches, primary_branch)

        # Perform hierarchical clustering based on similarity metrics
        print("Clustering branches...")
        clusters = self.clusterer.cluster_branches(branch_metrics, diff_metrics)

        print("\n" + "=" * 70)
        print("STAGE TWO: Target Assignment and Tagging")
        print("=" * 70)

        # Assign integration targets and generate tags for each branch
        results = []
        for branch in branches:
            print(f"Assigning target for {branch}...")
            # Find which cluster this branch belongs to
            cluster_id = next(cid for cid, members in clusters.items() if branch in members)

            # Assign target and generate tags based on metrics and cluster context
            assignment = self.assigner.assign_target(
                branch, branch_metrics[branch]
            )

            # Build comprehensive result object
            results.append(
                {
                    "branch": branch,
                    "cluster_id": cluster_id,
                    "target": assignment.primary_target,
                    "secondary_targets": assignment.secondary_targets,
                    "confidence": assignment.confidence,
                    "tags": assignment.tags,
                    "reasoning": assignment.reasoning,
                    "metrics": {
                        "commit_history": asdict(branch_metrics[branch].commit_history),
                        "codebase_structure": asdict(branch_metrics[branch].codebase_structure),
                        "migration": asdict(branch_metrics[branch].migration_metrics),
                    },
                }
            )

        # Prepare detailed clustering analysis for output
        clustering_details = {
            "clusters": clusters,
            "branch_metrics": {b: asdict(m) for b, m in branch_metrics.items()},
            "diff_metrics": {str(k): asdict(v) for k, v in diff_metrics.items()},
            "generated_at": datetime.now().isoformat(),
            "total_branches": len(branches),
            "total_clusters": len(clusters),
        }

        return results, clustering_details


# ============================================================================
# Output Generation
# ============================================================================


class OutputGenerator:
    """Generates output files in various formats for different use cases"""

    def __init__(self, config: Dict = None):
        """
        Initialize output generator with configuration.

        Args:
            config: Optional configuration dictionary for output preferences
        """
        self.config = config or {}

    def generate_output(self, results: List[Dict], output_format: str = "detailed") -> Dict:
        """
        Generate output in specified format.

        Args:
            results: List of branch analysis results
            output_format: Format type - 'simple', 'detailed', or 'all'

        Returns:
            Dictionary containing formatted output
        """
        if output_format == "simple":
            return self._generate_simple_output(results)
        elif output_format == "detailed":
            return self._generate_detailed_output(results)
        elif output_format == "all":
            return {
                "simple": self._generate_simple_output(results),
                "detailed": self._generate_detailed_output(results),
            }
        else:
            raise ValueError(f"Unknown output format: {output_format}")

    def _generate_simple_output(self, results: List[Dict]) -> Dict:
        """
        Generate simple JSON output (I2.T4 style).

        Simple format focuses on essential information:
        - Branch name
        - Target assignment
        - Confidence score
        - Reasoning
        - Tags

        Returns:
            Dictionary with simplified branch information
        """
        simplified = []
        for result in results:
            simplified.append(
                {
                    "branch": result["branch"],
                    "target": result.get("target", result.get("primary_target", "main")),
                    "confidence": result.get("confidence", 0.0),
                    "reasoning": result.get("reasoning", ""),
                    "tags": result.get("tags", []),
                }
            )

        return {
            "branches": simplified,
            "total_branches": len(simplified),
            "generated_at": datetime.now().isoformat(),
        }

    def _generate_detailed_output(self, results: List[Dict]) -> Dict:
        """
        Generate detailed JSON output (75.6 style).

        Detailed format includes comprehensive information:
        - All branch metrics
        - Cluster assignments
        - Quality metrics
        - Target assignments with full context

        Returns:
            Dictionary with comprehensive branch analysis results
        """
        # Count targets for summary
        main_count = sum(
            1 for r in results if r.get("target") == "main" or r.get("primary_target") == "main"
        )
        scientific_count = sum(
            1
            for r in results
            if r.get("target") == "scientific" or r.get("primary_target") == "scientific"
        )
        orchestration_count = sum(
            1
            for r in results
            if r.get("target") == "orchestration-tools"
            or r.get("primary_target") == "orchestration-tools"
        )

        return {
            "branches": results,
            "summary": {
                "total_branches": len(results),
                "main_target_count": main_count,
                "scientific_target_count": scientific_count,
                "orchestration_target_count": orchestration_count,
            },
            "generated_at": datetime.now().isoformat(),
        }


# ============================================================================
# File Output Utilities
# ============================================================================


def save_categorized_branches(results: List[Dict], output_file: str):
    """Save categorized branches to JSON"""
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved categorized branches to {output_file}")


def save_clustering_details(details: Dict, output_file: str):
    """Save clustering details to JSON"""
    with open(output_file, "w") as f:
        json.dump(details, f, indent=2, default=str)
    print(f"Saved clustering details to {output_file}")


# ============================================================================
# Main Execution
# ============================================================================

if __name__ == "__main__":
    import sys

    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."

    # Get all remote branches
    result = subprocess.run(["git", "branch", "-r"], capture_output=True, text=True, cwd=repo_path)

    all_branches = [
        line.strip().replace("origin/", "").replace("HEAD -> origin/main", "")
        for line in result.stdout.split("\n")
        if line.strip() and "HEAD ->" not in line
    ]

    # Filter to feature branches
    feature_branches = [
        b for b in all_branches if b not in ["main", "scientific", "orchestration-tools"]
    ]

    # Execute pipeline
    engine = BranchClusteringEngine(repo_path)
    categorized, clustering = engine.execute_full_pipeline(feature_branches)

    # Save outputs
    save_categorized_branches(
        categorized, ".taskmaster/task_data/categorized_branches_enhanced.json"
    )
    save_clustering_details(clustering, ".taskmaster/task_data/clustered_branches.json")

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)
