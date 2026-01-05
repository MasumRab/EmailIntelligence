# Task 002.4: BranchClusterer

**Status:** Ready when 002.1-002.3 complete  
**Priority:** High  
**Effort:** 28-36 hours  
**Complexity:** 8/10  
**Dependencies:** Task 002.1, Task 002.2, Task 002.3  
**Blocks:** Task 002.5 (IntegrationTargetAssigner)

---

## Purpose

Create a hierarchical clustering engine that combines normalized metrics from Tasks 002.1-002.3, performs Ward linkage clustering, and generates cluster assignments with quality metrics. This is the Stage One integration component.

**Scope:** BranchClusterer class only  
**Depends on:** Outputs from 002.1, 002.2, 002.3  
**Blocks:** Task 002.5

---

## Success Criteria

Task 002.4 is complete when:

### Core Functionality
- [ ] `BranchClusterer` class accepts analyzer outputs from Tasks 002.1, 002.2, 002.3
- [ ] Successfully combines metrics using 35/35/30 weighted formula
- [ ] Performs hierarchical agglomerative clustering with Ward's linkage method
- [ ] Computes cluster quality metrics:
  - [ ] Silhouette score ([-1, 1] range, higher = better)
  - [ ] Davies-Bouldin index ([0, ∞), lower = better)
  - [ ] Calinski-Harabasz index ([0, ∞), higher = better)
- [ ] Outputs properly formatted dict with cluster assignments and quality metrics
- [ ] Output matches JSON schema exactly

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <5 seconds for clustering 50+ branches
- [ ] Memory: <100 MB per analysis
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

### Integration Readiness
- [ ] Compatible with Task 002.5 (IntegrationTargetAssigner) input requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate
- [ ] All metrics in valid ranges (no NaN/Inf)

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 002.1 (CommitHistoryAnalyzer) complete with outputs
- [ ] Task 002.2 (CodebaseStructureAnalyzer) complete with outputs
- [ ] Task 002.3 (DiffDistanceCalculator) complete with outputs
- [ ] scipy.cluster.hierarchy library installed
- [ ] scipy.spatial.distance library
- [ ] sklearn.metrics library

### Blocks (What This Task Unblocks)
- Task 002.5 (IntegrationTargetAssigner)

---

## Sub-subtasks

### 002.4.1: Design Clustering Architecture
**Effort:** 3-4 hours | **Depends on:** None

**Steps:**
1. Review hierarchical agglomerative clustering (HAC)
2. Document linkage method choice (Ward's method)
3. Document distance metric choice (Euclidean)
4. Define dendrogram cut threshold strategy
5. Define quality metrics (silhouette, Davies-Bouldin, Calinski-Harabasz)

**Success Criteria:**
- [ ] Clustering algorithm documented
- [ ] Linkage method specified (Ward)
- [ ] Distance metric specified (Euclidean)
- [ ] Threshold strategy defined
- [ ] Quality metrics documented

---

### 002.4.2: Implement Metric Combination System
**Effort:** 4-5 hours | **Depends on:** 002.4.1, Tasks 002.1-002.3

**Steps:**
1. Accept output dicts from all three analyzers
2. Validate that all required metrics present
3. Implement 35/35/30 weighted combination formula
4. Verify result is in [0,1] range
5. Create scoring vectors for clustering input

**Success Criteria:**
- [ ] Accepts input from Tasks 002.1, 002.2, 002.3
- [ ] Validates all metrics present
- [ ] Combines using: 0.35×002.1 + 0.35×002.2 + 0.30×002.3
- [ ] Returns score in [0, 1] range
- [ ] Can process 10+ branches without error

---

### 002.4.3: Implement Distance Matrix Calculation
**Effort:** 3-4 hours | **Depends on:** 002.4.2

**Steps:**
1. Extract metric vectors for all branches
2. Normalize vectors (all should be 0-1)
3. Choose distance metric (Euclidean)
4. Calculate pairwise distances
5. Format as NxN distance matrix

**Success Criteria:**
- [ ] Computes distance matrix for N branches
- [ ] Distance matrix is symmetric
- [ ] Diagonal is zero
- [ ] All distances in valid range
- [ ] Performance acceptable (<1s for 50 branches)

---

### 002.4.4: Implement Hierarchical Clustering Engine
**Effort:** 4-5 hours | **Depends on:** 002.4.3

**Steps:**
1. Import scipy.cluster.hierarchy functions
2. Implement linkage computation using Ward method
3. Generate dendrogram from linkage matrix
4. Implement dendrogram cutting at threshold
5. Assign branches to clusters

**Success Criteria:**
- [ ] Linkage matrix has correct shape (N-1, 4)
- [ ] Ward linkage applied correctly
- [ ] Dendrogram can be generated
- [ ] Cutting produces valid clusters
- [ ] All branches assigned to clusters

---

### 002.4.5: Compute Cluster Quality Metrics
**Effort:** 3-4 hours | **Depends on:** 002.4.4

**Steps:**
1. Compute silhouette score for each branch
2. Compute average silhouette across all branches
3. Compute Davies-Bouldin index
4. Compute Calinski-Harabasz index
5. Compute cluster cohesion per cluster

**Success Criteria:**
- [ ] Silhouette score computed in [-1, 1] range
- [ ] Davies-Bouldin index computed
- [ ] Calinski-Harabasz index computed
- [ ] Cluster cohesion scores computed
- [ ] No NaN or Inf values

---

### 002.4.6: Compute Cluster Characteristics
**Effort:** 2-3 hours | **Depends on:** 002.4.4

**Steps:**
1. Identify member branches per cluster
2. Compute cluster center (mean of metrics)
3. Calculate cluster size
4. Document cluster membership list
5. Compute cluster radius

**Success Criteria:**
- [ ] Cluster center is valid metric vector
- [ ] All branches assigned to exactly one cluster
- [ ] Cluster sizes sum to total branch count
- [ ] Cluster centers documented
- [ ] Membership lists complete

---

### 002.4.7: Format Output & Validation
**Effort:** 2-3 hours | **Depends on:** 002.4.5, 002.4.6

**Steps:**
1. Create output dict structure matching spec
2. Populate clusters array with all cluster data
3. Create branch_assignments mapping
4. Include quality_metrics object
5. Validate output against JSON schema

**Success Criteria:**
- [ ] Output dict has all required fields
- [ ] Clusters array populated correctly
- [ ] branch_assignments complete
- [ ] quality_metrics object included
- [ ] Schema validation passes

---

### 002.4.8: Write Unit Tests
**Effort:** 4-5 hours | **Depends on:** 002.4.7

**Steps:**
1. Create test fixtures with known clustering scenarios
2. Implement 8+ test cases
3. Mock analyzer outputs
4. Add performance tests
5. Generate coverage report (>95%)

**Success Criteria:**
- [ ] 8+ test cases implemented
- [ ] All tests pass
- [ ] Code coverage >95%
- [ ] Edge cases covered
- [ ] Quality metrics validated

---

## Specification

### Output Format

```json
{
  "clusters": [
    {
      "cluster_id": 0,
      "branches": ["feature/auth", "feature/user-management"],
      "size": 2,
      "characteristics": {
        "avg_recency": 0.79,
        "avg_complexity": 0.65,
        "avg_risk": 0.45
      }
    }
  ],
  "branch_assignments": {
    "feature/auth": 0,
    "feature/user-management": 0
  },
  "quality_metrics": {
    "silhouette_score": 0.65,
    "davies_bouldin_index": 0.85,
    "calinski_harabasz_index": 12.5
  },
  "analysis_timestamp": "2025-12-22T10:45:00Z"
}
```

### Metric Combination Formula

```
combined_score = (0.35 × commit_history_score) + 
                 (0.35 × codebase_structure_score) + 
                 (0.30 × diff_distance_score)
```

### Quality Metric Interpretation

- **Silhouette Score:** >0.7 excellent, >0.5 good, <0.25 poor
- **Davies-Bouldin Index:** <1.0 excellent, <1.5 good, <2.0 acceptable
- **Calinski-Harabasz Score:** >10 good, higher is better

---

## Implementation Guide

### 002.4.2: Metric Combination

```python
def combine_metrics(
    commit_result: dict,
    structure_result: dict,
    diff_result: dict
) -> float:
    """Combine three analyzer outputs."""
    # Extract aggregate scores
    commit_score = commit_result['aggregate_score']
    structure_score = structure_result['aggregate_score']
    diff_score = diff_result['aggregate_score']
    
    # Verify all in [0, 1]
    assert 0 <= commit_score <= 1
    assert 0 <= structure_score <= 1
    assert 0 <= diff_score <= 1
    
    # Weighted combination
    combined = (0.35 * commit_score + 
                0.35 * structure_score + 
                0.30 * diff_score)
    
    return max(0.0, min(1.0, combined))
```

### 002.4.4: Hierarchical Clustering

```python
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from scipy.spatial.distance import pdist, squareform

def perform_clustering(
    distance_matrix: np.ndarray,
    method: str = 'ward'
) -> Tuple[np.ndarray, np.ndarray]:
    """Perform Ward linkage clustering."""
    # Condensed distance format for scipy
    condensed_distances = pdist(distance_matrix, metric='euclidean')
    
    # Linkage with Ward method
    Z = linkage(condensed_distances, method='ward')
    
    # Cut dendrogram at threshold
    threshold = 0.5
    clusters = fcluster(Z, t=threshold, criterion='distance')
    
    return Z, clusters
```

### 002.4.5: Quality Metrics

```python
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

def compute_quality_metrics(
    distance_matrix: np.ndarray,
    clusters: np.ndarray
) -> dict:
    """Compute clustering quality metrics."""
    silhouette = silhouette_score(distance_matrix, clusters)
    davies_bouldin = davies_bouldin_score(distance_matrix, clusters)
    calinski_harabasz = calinski_harabasz_score(distance_matrix, clusters)
    
    return {
        'silhouette_score': float(silhouette),
        'davies_bouldin_index': float(davies_bouldin),
        'calinski_harabasz_index': float(calinski_harabasz)
    }
```

---

## Configuration Parameters

```yaml
clustering:
  linkage_method: "ward"
  distance_metric: "euclidean"
  threshold: 0.5
  min_cluster_size: 2
  max_clusters: 10
  
  weights:
    commit_history: 0.35
    codebase_structure: 0.35
    diff_distance: 0.30
```

---

## Performance Targets

- 50 branches: <10 seconds
- Memory: <100 MB
- All quality metrics computed without overflow

---

## Testing Strategy

Minimum 8 test cases:

```python
def test_metric_combination_in_range():
    """Combined score should be in [0, 1]"""
    
def test_clustering_produces_valid_clusters():
    """All branches assigned to clusters"""
    
def test_silhouette_score_valid():
    """Silhouette score in [-1, 1]"""
    
def test_davies_bouldin_valid():
    """Davies-Bouldin index >= 0"""
    
def test_calinski_harabasz_valid():
    """Calinski-Harabasz score >= 0"""
    
def test_branch_assignment_complete():
    """All branches assigned to exactly one cluster"""
    
def test_cluster_characteristics_computed():
    """Cluster centers computed correctly"""
    
def test_output_schema_valid():
    """Output matches JSON schema"""
```

---

## Common Gotchas & Solutions

**Gotcha 1: Metrics outside valid range**
```python
# Ensure clipping
combined = max(0.0, min(1.0, combined_score))
```

**Gotcha 2: All branches cluster together**
```python
# If too few clusters, adjust threshold
if len(unique_clusters) < 2:
    clusters = fcluster(Z, t=5, criterion='maxclust')
```

**Gotcha 3: Distance matrix not symmetric**
```python
# Ensure symmetry
distance_matrix = (distance_matrix + distance_matrix.T) / 2
```

**Gotcha 4: NaN in quality metrics**
```python
# Check denominators and handle edge cases
if len(unique_clusters) < 2:
    return 0.0  # Cannot compute silhouette
```

---

## Helper Tools (Optional)

The following tools are available to accelerate work or provide validation. **None are required** - every task is completable using only the steps in this file.

### Progress Logging

After completing each sub-subtask, optionally log progress for multi-session continuity:

```python
from memory_api import AgentMemory

memory = AgentMemory()
memory.load_session()

# After completing sub-subtask 002.4.5
memory.add_work_log(
    action="Completed Task 002.4.5: Compute Cluster Quality Metrics",
    details="Silhouette, Davies-Bouldin, Calinski-Harabasz scores computed, no NaN values"
)
memory.update_todo("task_002_4_5", "completed")
memory.save_session()
```

**What this does:** Maintains session state across work sessions, enables agent handoffs, documents progress.  
**Required?** No - git commits are sufficient.  
**See:** MEMORY_API_FOR_TASKS.md for full usage patterns and examples.

### Output Validation

After completing sub-subtask 002.4.8 (Unit Testing), optionally validate output format:

```bash
python scripts/compare_task_files.py \
  --validate src/clustering/branch_clusterer.py \
  --schema specification.json
```

**What this does:** Checks your clusterer output JSON matches the schema in the Specification section above.  
**Expected output:** `✓ Valid schema` (means you're ready to move to Task 002.5)  
**Required?** No - manual verification against Specification section is sufficient.  
**See:** SCRIPTS_IN_TASK_WORKFLOW.md § compare_task_files.py for troubleshooting.

### Check Next Task

After completing Task 002.4, see what's next:

```bash
python scripts/next_task.py

# Output shows: Task 002.5 (IntegrationTargetAssigner) ready
```

**See:** SCRIPTS_IN_TASK_WORKFLOW.md § next_task.py for details.

---

## Tools Reference

| Tool | Purpose | When to Use | Required? |
|------|---------|-----------|----------|
| Memory API | Progress logging | After each sub-subtask | No |
| compare_task_files.py | Output validation | After 002.4.8 | No |
| next_task.py | Find next task | After completion | No |

**For detailed usage and troubleshooting:** See SCRIPTS_IN_TASK_WORKFLOW.md (all optional tools documented there)

---

## Integration Checkpoint

- [ ] All 8 sub-subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Accepts output from Tasks 002.1, 002.2, 002.3
- [ ] Output matches specification
- [ ] Quality metrics validated
- [ ] Ready for Task 002.5

---

## Done Definition

1. ✅ All 8 sub-subtasks marked complete
2. ✅ Unit tests pass (>95% coverage)
3. ✅ Code review approved
4. ✅ Outputs match specification
5. ✅ Accepts input from Tasks 002.1-002.3
6. ✅ Ready for hand-off to Task 002.5
7. ✅ Commit: "feat: complete Task 002.4 BranchClusterer"

---

**Last Updated:** January 6, 2026  
**Consolidated from:** Task 75.4 (task-75.4.md) with 60 original success criteria preserved  
**Structure:** TASK_STRUCTURE_STANDARD.md
