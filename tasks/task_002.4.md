# Task 002.4: BranchClusterer

**Status:** Ready for Implementation
**Priority:** High
**Effort:** 28-36 hours
**Complexity:** 8/10
**Dependencies:** 002.1, 002.2, 002.3

---

## Overview/Purpose

Implement the `BranchClusterer` class that clusters branches using Hierarchical Agglomerative Clustering (HAC) based on combined metrics from Tasks 002.1-002.3. This is a Stage One integration component that combines all three analyzer outputs into a unified clustering result with quality metrics and dendrogram data.

**Scope:** BranchClusterer class only
**Depends on:** CommitHistoryAnalyzer (002.1), CodebaseStructureAnalyzer (002.2), DiffDistanceCalculator (002.3)

---

## Success Criteria

Task 002.4 is complete when:

### Core Functionality
- [ ] `BranchClusterer` class accepts `repo_path` (str) and `threshold` (float, default 0.5)
- [ ] `cluster()` method accepts dict of branch analyzer outputs from 002.1-002.3
- [ ] Combines metrics using weighted formula: 35% commit_history + 35% codebase_structure + 30% diff_distance
- [ ] Computes pairwise distance matrix using `1 - combined_score` as distance
- [ ] Performs HAC with Ward's linkage method
- [ ] Cuts dendrogram at configurable threshold to form final clusters
- [ ] Returns properly formatted dict with clusters, branch_assignments, quality_metrics, dendogram_data
- [ ] Output matches JSON schema exactly

### Quality Assurance
- [ ] Unit tests pass (minimum 5 test scenarios with >95% coverage)
- [ ] Silhouette score, Davies-Bouldin index, and Calinski-Harabasz index computed correctly
- [ ] No exceptions raised for valid inputs (including edge cases: 1 branch, all-identical)
- [ ] Performance: <5 seconds for 50 branches
- [ ] Code quality: PEP 8 compliant, Google-style docstrings

### Integration Readiness
- [ ] Input format compatible with 002.1/002.2/002.3 output schemas
- [ ] Output format compatible with Task 002.5 (IntegrationTargetAssigner) input
- [ ] Configuration externalized and validated
- [ ] All weights sum to 1.0 (0.35 + 0.35 + 0.30)

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 002.1 (CommitHistoryAnalyzer) complete — provides commit_history aggregate scores
- [ ] Task 002.2 (CodebaseStructureAnalyzer) complete — provides codebase_structure aggregate scores
- [ ] Task 002.3 (DiffDistanceCalculator) complete — provides diff_distance aggregate scores
- [ ] Development environment configured with scipy and sklearn

### Blocks (What This Task Unblocks)
- Task 002.5 (IntegrationTargetAssigner)
- Task 002.6 (PipelineIntegration)

### External Dependencies
- `scipy.cluster.hierarchy` — linkage, fcluster, dendrogram
- `scipy.spatial.distance` — pdist, squareform
- `sklearn.metrics` — silhouette_score, davies_bouldin_score, calinski_harabasz_score
- Python 3.8+

---

## Sub-subtasks Breakdown

### 002.4.1: Input Validation and Metric Combination
**Effort:** 4-5 hours
**Depends on:** None (within this task)

**Steps:**
1. Validate all 3 analyzer outputs present for each branch
2. Extract aggregate_score from each analyzer output
3. Compute combined_score using weighted formula
4. Store as feature vectors for clustering

**Success Criteria:**
- [ ] Validates presence of commit_history, codebase_structure, diff_distance for each branch
- [ ] Raises ValueError with descriptive message if any analyzer output missing
- [ ] combined_score is in [0, 1] range for all branches
- [ ] Weights sum to exactly 1.0

---

### 002.4.2: Distance Matrix Computation
**Effort:** 3-4 hours
**Depends on:** 002.4.1

**Steps:**
1. Build feature vectors (3-tuple of normalized scores per branch)
2. Compute pairwise distances using pdist with euclidean metric
3. Convert to square form for quality metric computation

**Success Criteria:**
- [ ] Distance matrix is symmetric
- [ ] Diagonal entries are zero
- [ ] All distances are non-negative

---

### 002.4.3: Hierarchical Clustering Implementation
**Effort:** 6-8 hours
**Depends on:** 002.4.2

**Steps:**
1. Apply scipy linkage with Ward's method
2. Cut dendrogram at threshold using fcluster
3. Extract cluster assignments for each branch
4. Compute cluster centers as mean of member scores
5. Compute per-cluster cohesion (average internal distance)

**Success Criteria:**
- [ ] Linkage matrix has correct shape (n-1, 4)
- [ ] Every branch assigned to exactly one cluster
- [ ] Cluster centers reflect actual member averages

---

### 002.4.4: Quality Metrics Computation
**Effort:** 4-5 hours
**Depends on:** 002.4.3

**Steps:**
1. Compute silhouette score (per-branch and average)
2. Compute Davies-Bouldin index
3. Compute Calinski-Harabasz index
4. Handle edge cases (single cluster, all identical branches)

**Success Criteria:**
- [ ] Silhouette in [-1, 1], >0.5 indicates good clustering
- [ ] Davies-Bouldin in [0, ∞), lower is better
- [ ] Calinski-Harabasz in [0, ∞), higher is better
- [ ] Single-cluster edge case handled gracefully

---

### 002.4.5: Output Formatting and Dendrogram Data
**Effort:** 4-5 hours
**Depends on:** 002.4.4

**Steps:**
1. Build clusters array with cluster_id, branches, center, size, cohesion, silhouette
2. Build branch_assignments mapping
3. Package quality_metrics
4. Extract dendogram_data (linkage_matrix, branch_indices)
5. Add clustering_timestamp

**Success Criteria:**
- [ ] Output dict matches specification schema exactly
- [ ] All numeric values are JSON-serializable (no numpy types)
- [ ] Timestamp is ISO 8601 format

---

### 002.4.6: Testing and Edge Cases
**Effort:** 5-6 hours
**Depends on:** 002.4.5

**Steps:**
1. Test with 3-5 similar branches (should form one cluster)
2. Test with 10 branches with varying metrics (multiple clusters)
3. Test with 1 outlier branch (own cluster)
4. Test all branches identical (1 large cluster)
5. Test all branches maximally different (N clusters)

**Success Criteria:**
- [ ] All 5 test scenarios pass
- [ ] Edge cases handled without exceptions
- [ ] Quality metrics reasonable for each scenario

---

## Specification Details

### Class Interface

```python
class BranchClusterer:
    def __init__(self, repo_path: str, threshold: float = 0.5):
        """Initialize BranchClusterer.

        Args:
            repo_path: Path to the git repository.
            threshold: Distance threshold for cutting dendrogram (default 0.5).
        """

    def cluster(self, analyzer_outputs: dict) -> dict:
        """Cluster branches based on combined analyzer metrics.

        Args:
            analyzer_outputs: Dict mapping branch names to analyzer results.

        Returns:
            Dict with clusters, branch_assignments, quality_metrics, dendogram_data.
        """
```

### Input Schema

```json
{
  "feature/auth-system": {
    "commit_history": {
      "metrics": {
        "commit_recency": 0.87,
        "commit_frequency": 0.65,
        "authorship_diversity": 0.72,
        "merge_readiness": 0.91,
        "stability_score": 0.58
      },
      "aggregate_score": 0.749
    },
    "codebase_structure": {
      "metrics": {
        "directory_similarity": 0.82,
        "file_additions": 0.68,
        "core_module_stability": 0.95,
        "namespace_isolation": 0.71
      },
      "aggregate_score": 0.794
    },
    "diff_distance": {
      "metrics": {
        "code_churn": 0.72,
        "change_concentration": 0.81,
        "diff_complexity": 0.68,
        "integration_risk": 0.79
      },
      "aggregate_score": 0.750
    }
  }
}
```

### Output Schema

```json
{
  "clusters": [
    {
      "cluster_id": 0,
      "branches": ["feature/auth-system", "feature/user-profile"],
      "cluster_center": {
        "commit_history_weight": 0.749,
        "codebase_structure_weight": 0.794,
        "diff_distance_weight": 0.750,
        "combined_score": 0.764
      },
      "size": 2,
      "cohesion": 0.92,
      "silhouette_score": 0.68
    }
  ],
  "branch_assignments": {
    "feature/auth-system": 0,
    "feature/api-refactor": 1,
    "feature/user-profile": 0
  },
  "quality_metrics": {
    "total_clusters": 2,
    "silhouette_avg": 0.71,
    "davies_bouldin_index": 0.85,
    "calinski_harabasz_index": 15.3
  },
  "dendogram_data": {
    "linkage_matrix": [[0, 1, 0.35, 2], [2, 3, 0.52, 3]],
    "branch_indices": [0, 1, 2]
  },
  "clustering_timestamp": "2025-12-22T10:45:00Z"
}
```

### Metric Combination Formula

```
combined_score = (
    0.35 * commit_history_aggregate +
    0.35 * codebase_structure_aggregate +
    0.30 * diff_distance_aggregate
)
```

All component aggregates already normalized to [0, 1], so combined_score is also [0, 1].

### Quality Metrics Reference

| Metric | Range | Interpretation |
|--------|-------|----------------|
| **Silhouette Score** | [-1, 1] | >0.5 good, >0.7 excellent |
| **Davies-Bouldin Index** | [0, ∞) | Lower is better (<1 excellent) |
| **Calinski-Harabasz Index** | [0, ∞) | Higher is better (>10 good) |

---

## Implementation Guide

### Step 1: Metric Combination and Validation

```python
def cluster(self, analyzer_outputs: dict):
    # 1. Validate and combine metrics
    combined_scores = {}
    for branch, scores in analyzer_outputs.items():
        for key in ['commit_history', 'codebase_structure', 'diff_distance']:
            if key not in scores:
                raise ValueError(f"Missing '{key}' in analyzer output for {branch}")

        combined = (
            0.35 * scores['commit_history']['aggregate_score'] +
            0.35 * scores['codebase_structure']['aggregate_score'] +
            0.30 * scores['diff_distance']['aggregate_score']
        )
        combined_scores[branch] = combined
```

### Step 2: Distance Matrix and Clustering

```python
    # 2. Build feature vectors and compute distance matrix
    branches = list(combined_scores.keys())
    vectors = []
    for branch in branches:
        s = analyzer_outputs[branch]
        vectors.append([
            s['commit_history']['aggregate_score'],
            s['codebase_structure']['aggregate_score'],
            s['diff_distance']['aggregate_score']
        ])

    vectors = np.array(vectors)
    distances = pdist(vectors, metric='euclidean')

    # 3. Hierarchical clustering
    linkage_matrix = linkage(distances, method='ward')
    cluster_labels = fcluster(linkage_matrix, t=self.threshold, criterion='distance')
```

### Step 3: Quality Metrics

```python
    # 4. Compute quality metrics
    distance_matrix = squareform(distances)

    if len(set(cluster_labels)) > 1:
        sil_avg = silhouette_score(distance_matrix, cluster_labels, metric='precomputed')
        db_index = davies_bouldin_score(vectors, cluster_labels)
        ch_index = calinski_harabasz_score(vectors, cluster_labels)
    else:
        sil_avg = 0.0
        db_index = 0.0
        ch_index = 0.0
```

### Step 4: Build Output

```python
    # 5. Build cluster details
    cluster_details = []
    unique_labels = sorted(set(cluster_labels))

    for label in unique_labels:
        member_indices = [i for i, l in enumerate(cluster_labels) if l == label]
        member_branches = [branches[i] for i in member_indices]
        member_vectors = vectors[member_indices]
        center = member_vectors.mean(axis=0)
        internal_dists = pdist(member_vectors, metric='euclidean')
        cohesion = 1.0 - (internal_dists.mean() if len(internal_dists) > 0 else 0.0)

        cluster_details.append({
            "cluster_id": int(label),
            "branches": member_branches,
            "cluster_center": {
                "commit_history_weight": float(center[0]),
                "codebase_structure_weight": float(center[1]),
                "diff_distance_weight": float(center[2]),
                "combined_score": float(
                    0.35 * center[0] + 0.35 * center[1] + 0.30 * center[2]
                )
            },
            "size": len(member_branches),
            "cohesion": float(cohesion),
            "silhouette_score": float(sil_avg)
        })

    # 6. Format final output
    return {
        "clusters": cluster_details,
        "branch_assignments": {
            branches[i]: int(cluster_labels[i])
            for i in range(len(branches))
        },
        "quality_metrics": {
            "total_clusters": len(unique_labels),
            "silhouette_avg": float(sil_avg),
            "davies_bouldin_index": float(db_index),
            "calinski_harabasz_index": float(ch_index)
        },
        "dendogram_data": {
            "linkage_matrix": linkage_matrix.tolist(),
            "branch_indices": list(range(len(branches)))
        },
        "clustering_timestamp": datetime.utcnow().isoformat() + "Z"
    }
```

---

## Configuration & Defaults

```python
COMMIT_HISTORY_WEIGHT = 0.35
CODEBASE_STRUCTURE_WEIGHT = 0.35
DIFF_DISTANCE_WEIGHT = 0.30
CLUSTERING_THRESHOLD = 0.5
LINKAGE_METHOD = "ward"
DISTANCE_METRIC = "euclidean"
```

YAML config file (`config/task_002_clustering.yaml`):

```yaml
branch_clusterer:
  commit_history_weight: 0.35
  codebase_structure_weight: 0.35
  diff_distance_weight: 0.30
  clustering_threshold: 0.5
  linkage_method: "ward"
  distance_metric: "euclidean"
```

Load in code:

```python
import yaml

with open('config/task_002_clustering.yaml') as f:
    CONFIG = yaml.safe_load(f)
```

---

## Typical Development Workflow

1. **Day 1-2:** Implement input validation and metric combination (002.4.1)
2. **Day 2-3:** Build distance matrix computation (002.4.2)
3. **Day 3-5:** Implement HAC with Ward's method and dendrogram cutting (002.4.3)
4. **Day 5-6:** Add quality metrics computation (002.4.4)
5. **Day 6-7:** Format output and extract dendrogram data (002.4.5)
6. **Day 7-8:** Write all tests and handle edge cases (002.4.6)
7. **Day 8-9:** Code review, docstrings, PEP 8 cleanup

---

## Integration Handoff

### Downstream Tasks

| Task | Consumes | Purpose |
|------|----------|---------|
| **002.5** (IntegrationTargetAssigner) | Full output dict (clusters, assignments, quality) | Assigns branches to integration targets using cluster data |
| **002.6** (PipelineIntegration) | Full output dict | Orchestrates end-to-end pipeline, generates JSON outputs |

### Integration Contract

Task 002.5 expects the output dict with:
- `clusters` array with `cluster_id`, `branches`, `cluster_center`
- `branch_assignments` mapping branch names to cluster IDs
- `quality_metrics` for pipeline reporting

---

## Common Gotchas & Solutions

**Gotcha 1: Single branch input**
```python
# WRONG: pdist fails with single item
distances = pdist([single_vector])  # Empty result

# RIGHT: Handle edge case
if len(branches) == 1:
    return single_branch_result(branches[0])
```

**Gotcha 2: Numpy types not JSON-serializable**
```python
# WRONG
return {"score": np.float64(0.75)}  # TypeError: not serializable

# RIGHT
return {"score": float(np.float64(0.75))}  # Cast to native Python
```

**Gotcha 3: All branches identical**
```python
# WRONG: silhouette_score fails when all distances are zero
sil = silhouette_score(zeros_matrix, labels)  # ValueError

# RIGHT: Check for degenerate case
if len(set(cluster_labels)) <= 1 or np.allclose(distances, 0):
    sil_avg = 0.0
```

**Gotcha 4: Weights not summing to 1.0**
```python
# WRONG: 0.35 + 0.35 + 0.30 might not equal 1.0 due to float precision
assert sum(weights) == 1.0  # Can fail

# RIGHT: Use tolerance
assert abs(sum(weights) - 1.0) < 1e-9, f"Weights sum to {sum(weights)}"
```

---

## Integration Checkpoint

**When to move to Task 002.5 (IntegrationTargetAssigner):**

- [ ] All 6 sub-subtasks complete
- [ ] All 5 test scenarios pass (similar, mixed, outlier, identical, different)
- [ ] Quality metrics computed correctly for each scenario
- [ ] Output matches specification schema exactly
- [ ] No numpy types in output (all native Python)
- [ ] Edge cases handled (1 branch, 0 branches, all identical)
- [ ] Performance: <5 seconds for 50 branches
- [ ] Code review approved
- [ ] Commit message: `feat: complete Task 002.4 BranchClusterer`

---

## Done Definition

Task 002.4 is done when:

1. All 6 sub-subtasks marked complete
2. Unit tests pass (>95% coverage) for all 5 test scenarios
3. Code review approved
4. Output matches specification schema exactly
5. Quality metrics (silhouette, Davies-Bouldin, Calinski-Harabasz) validated
6. Edge cases handled without exceptions
7. Documentation complete (Google-style docstrings)
8. Performance benchmarks met (<5 seconds for 50 branches)
9. Ready for hand-off to Task 002.5
10. Commit: `feat: complete Task 002.4 BranchClusterer`

---

## Provenance

- **Primary source:** HANDOFF_75.4_BranchClusterer.md (archived in task_data/migration_backup_20260129/)
- **Task ID mapping:** Original Task 75.4 → Current Task 002.4
- **Structure standard:** TASK_STRUCTURE_STANDARD.md (14-section format, approved January 6, 2026)
- **Upstream dependencies:** Task 002.1 (CommitHistoryAnalyzer), Task 002.2 (CodebaseStructureAnalyzer), Task 002.3 (DiffDistanceCalculator)
- **Downstream consumers:** Task 002.5 (IntegrationTargetAssigner), Task 002.6 (PipelineIntegration)

---

## Next Steps

1. **Immediate:** Begin with sub-subtask 002.4.1 (Input Validation and Metric Combination)
2. **Week 1-2:** Complete all 6 sub-subtasks with proper metric combination
3. **Week 2-3:** Implement clustering algorithm with Ward's linkage method
4. **Week 3:** Write comprehensive tests for all 5 clustering scenarios
5. **Week 3:** Performance validation and optimization
6. **Week 3-4:** Code review and documentation completion
7. **Upon completion:** Ready for hand-off to Task 002.5 (IntegrationTargetAssigner)
8. **Parallel tasks:** Task 002.7 (VisualizationReporting), Task 002.8 (TestingSuite) can proceed in parallel

## Performance Targets

[Performance targets to be defined]


## Testing Strategy

[Testing strategy to be defined]
