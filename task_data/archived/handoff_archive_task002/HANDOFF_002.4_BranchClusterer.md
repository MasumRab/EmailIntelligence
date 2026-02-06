# Task 75.4: BranchClusterer (Hierarchical Clustering Engine)

## Quick Summary
Implement the `BranchClusterer` class that clusters branches using hierarchical agglomerative clustering based on combined metrics from Tasks 75.1-75.3. This is a Stage One component—depends on outputs from all three analyzers.

**Effort:** 28-36 hours | **Complexity:** 8/10 | **Parallelizable:** No (depends on 75.1, 75.2, 75.3)

---

## What to Build

A Python class `BranchClusterer` that:
1. Accepts metric outputs from CommitHistoryAnalyzer, CodebaseStructureAnalyzer, DiffDistanceCalculator
2. Combines metrics using weighted formula (35%, 35%, 30%)
3. Performs hierarchical agglomerative clustering using Ward's method
4. Returns cluster assignments with quality metrics

### Class Signature
```python
class BranchClusterer:
    def __init__(self, repo_path: str, threshold: float = 0.5)
    def cluster(self, analyzer_outputs: dict) -> dict
```

---

## Input Specification

### Input Format
Expects dict with branch names as keys, each containing outputs from Tasks 75.1-75.3:

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
  },
  "feature/api-refactor": { ... }
}
```

---

## Output Specification

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
    "linkage_matrix": [[...], [...], ...],
    "branch_indices": [0, 1, 2, ...]
  },
  "clustering_timestamp": "2025-12-22T10:45:00Z"
}
```

---

## Metric Combination Formula

```
combined_score = (
    0.35 * commit_history_aggregate +
    0.35 * codebase_structure_aggregate +
    0.30 * diff_distance_aggregate
)
```

All component aggregates already normalized to [0, 1], so combined_score is also [0, 1].

---

## Clustering Algorithm

### Hierarchical Agglomerative Clustering (HAC)

1. **Initialize**: Each branch is a cluster
2. **Distance metric**: Use `1 - combined_score` as distance
3. **Linkage method**: Ward's method (minimizes within-cluster variance)
4. **Dendrogram**: Cut at configurable threshold to form final clusters
5. **Quality metrics**: Compute silhouette, Davies-Bouldin, Calinski-Harabasz

### Distance Matrix Calculation

```
# For each pair of branches
distance = 1 - cosine_similarity(
    [commit, codebase, diff],
    [commit, codebase, diff]
)
# OR use Euclidean distance on normalized vectors
```

---

## Implementation Checklist

- [ ] Create data structure for branch metrics (validate all 3 analyzer outputs present)
- [ ] Combine metrics using 35/35/30 weighted formula
- [ ] Compute distance matrix (1 - similarity for all branch pairs)
- [ ] Implement or use scipy.cluster.hierarchy.linkage with Ward method
- [ ] Generate dendrogram data
- [ ] Cut dendrogram at configurable threshold to form clusters
- [ ] Assign branches to clusters based on cut
- [ ] Calculate cluster centers (mean of member scores)
- [ ] Compute cohesion for each cluster (avg internal distance)
- [ ] Compute silhouette scores (for each branch and average)
- [ ] Compute Davies-Bouldin index (cluster separation metric)
- [ ] Compute Calinski-Harabasz index (cluster validity metric)
- [ ] Return dict matching output spec exactly
- [ ] Add docstrings (Google style)
- [ ] Log clustering progress and diagnostics

---

## Quality Metrics Explanation

| Metric | Range | Interpretation |
|--------|-------|-----------------|
| **Silhouette Score** | [-1, 1] | >0.5 good, >0.7 excellent |
| **Davies-Bouldin Index** | [0, ∞) | Lower is better (<1 excellent) |
| **Calinski-Harabasz Index** | [0, ∞) | Higher is better (>10 good) |

---

## Test Cases

1. **Low-distance branches**: 3-5 similar branches, should cluster together
2. **Mixed distances**: 10 branches with varying metrics, multiple clusters
3. **Outliers**: 1 branch very different from others (own cluster)
4. **All similar**: All branches similar, 1 large cluster
5. **All different**: All branches distinct, N clusters (one per branch)

---

## Dependencies

- `scipy.cluster.hierarchy` (linkage, dendrogram, fcluster)
- `scipy.spatial.distance` (pdist, squareform)
- `sklearn.metrics` (silhouette_score, davies_bouldin_score, calinski_harabasz_score)
- Outputs from **Task 75.1, 75.2, 75.3** (required)
- Feeds into **Task 75.5 (IntegrationTargetAssigner)**

---

## Configuration

Accept these parameters in `__init__` or config file:

```python
COMMIT_HISTORY_WEIGHT = 0.35
CODEBASE_STRUCTURE_WEIGHT = 0.35
DIFF_DISTANCE_WEIGHT = 0.30
CLUSTERING_THRESHOLD = 0.5  # Distance threshold for cutting dendrogram
LINKAGE_METHOD = "ward"  # "ward", "complete", "average", etc.
DISTANCE_METRIC = "euclidean"  # "euclidean", "cosine", etc.
```

---

## Algorithm Pseudocode

```python
def cluster(self, analyzer_outputs: dict):
    # 1. Combine metrics
    combined_scores = {}
    for branch, scores in analyzer_outputs.items():
        combined = (
            0.35 * scores['commit_history']['aggregate_score'] +
            0.35 * scores['codebase_structure']['aggregate_score'] +
            0.30 * scores['diff_distance']['aggregate_score']
        )
        combined_scores[branch] = combined
    
    # 2. Compute distance matrix
    branches = list(combined_scores.keys())
    vectors = [...]  # 3-tuple of normalized scores
    distances = pdist(vectors, metric='euclidean')
    distance_matrix = squareform(distances)
    
    # 3. Hierarchical clustering
    linkage_matrix = linkage(distances, method='ward')
    clusters = fcluster(linkage_matrix, t=self.threshold, criterion='distance')
    
    # 4. Compute quality metrics
    silhouette = silhouette_score(distance_matrix, clusters)
    davies_bouldin = davies_bouldin_score(vectors, clusters)
    calinski_harabasz = calinski_harabasz_score(vectors, clusters)
    
    # 5. Format output
    return {...}  # See output spec
```

---

## Next Steps After Completion

1. Unit test with 10-20 branch fixtures
2. Validate clustering coherence (similar branches in same cluster)
3. Verify quality metrics are reasonable
4. Check dendrogram visualization (optional: plot for debugging)
5. Pass output to Task 75.5 (IntegrationTargetAssigner)

**Blocked by:** 75.1, 75.2, 75.3 (must complete first)
**Enables:** 75.5, 75.6, 75.7-75.9 (Stage Two and Three)
