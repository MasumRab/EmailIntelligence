# Task 75.4: BranchClusterer

## Purpose
Create a hierarchical clustering engine that combines normalized metrics from Tasks 75.1-75.3, performs Ward linkage clustering, and generates cluster assignments with quality metrics. This is the Stage One integration component that produces categorized branches for downstream processing.

**Scope:** BranchClusterer class only  
**Effort:** 28-36 hours | **Complexity:** 8/10  
**Status:** Ready when 75.1, 75.2, 75.3 complete  
**Blocks:** Tasks 75.5 and 75.6

---

## Quick Navigation

Navigate this document using these links:

- [Purpose](#purpose)
- [Developer Quick Reference](#developer-quick-reference)
- [Success Criteria](#success-criteria)
- [Subtasks Overview](#subtasks-overview)
- [Subtask Details](#subtasks)
- [Configuration & Defaults](#configuration--defaults)
- [Technical Reference](#technical-reference)
- [Common Gotchas & Solutions](#common-gotchas--solutions)
- [Development Workflow](#typical-development-workflow)
- [Integration Handoff](#integration-handoff)
- [Integration Checkpoint](#integration-checkpoint)
- [Done Definition](#done-definition)

**Pro tip:** Use Ctrl+F to search within sections, or click links above to jump directly

---

## Developer Quick Reference

### What to Build
A Python class `BranchClusterer` that:
1. Combines metrics from Tasks 75.1, 75.2, 75.3 (35/35/30 weights)
2. Performs hierarchical agglomerative clustering with Ward linkage
3. Returns cluster assignments and quality metrics

### Class Signature
```python
class BranchClusterer:
    def __init__(self, repo_path: str)
    def cluster(self, analyzer_outputs: List[dict]) -> dict
```

---

## Success Criteria

Task 75.4 is complete when:

**Core Functionality:**
- [ ] `BranchClusterer` class accepts analyzer outputs from Tasks 75.1, 75.2, 75.3
- [ ] Successfully combines metrics using 35/35/30 weighted formula
- [ ] Performs hierarchical agglomerative clustering with Ward's linkage method
- [ ] Computes cluster quality metrics (silhouette, Davies-Bouldin, Calinski-Harabasz)
- [ ] Outputs properly formatted dict with cluster assignments and quality metrics
- [ ] Output matches JSON schema exactly

**Performance Targets:**
- [ ] Clustering: **< 10 seconds** for 50+ branches
- [ ] Memory usage: **< 100 MB** for clustering operations
- [ ] Distance matrix computation: **O(n²)** where n = branches (typical: <1 second for 50)
- [ ] Linkage computation: **O(n²)** complexity (<3 seconds for 50 branches)
- [ ] Quality metrics computation: **< 2 seconds** for 50 branches
- [ ] All metrics valid, **no NaN or Inf values**
- [ ] Dendrogram generation: **< 5 seconds** for 50 branches

**Quality Assurance:**
- [ ] Unit tests pass (minimum 8 test cases with **>95% code coverage**)
- [ ] No exceptions raised for valid inputs (comprehensive error handling)
- [ ] Code quality: Passes linting, follows PEP 8, includes comprehensive docstrings

**Integration Readiness:**
- [ ] Compatible with Task 75.5 (IntegrationTargetAssigner) input requirements
- [ ] Compatible with Task 75.6 (PipelineIntegration) consumption patterns
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Subtasks Overview

### Dependency Flow Diagram

```
75.4.1 (3-4h)
[Design]                    
    │
    ├─→ 75.4.2 (4-5h)
    │   [Metric Combo]
    │       │
    │       ├─→ 75.4.3 (3-4h)
    │           [Distance]
    │               │
    │               ├─→ 75.4.4 (4-5h) ────────┐
    │               │  [Clustering]            │
    │               │                          ├─→ 75.4.6 (2-3h) ──┐
    │               ├─→ 75.4.5 (3-4h) ────────┤  [Output]          │
    │               │  [Quality Metrics]       │                    ├─→ 75.4.7 (4-5h)
    │               │                          │  [Tests]           │
    │               │                          ├─────────────────────┘
    │               └──────────────────────────┘
    │
    └─ (blocking 75.4.2, 75.4.3, 75.4.4-5, 75.4.6, 75.4.7)

Critical Path: 75.4.1 → 75.4.2 → 75.4.3 → 75.4.4-75.4.5 (parallel) → 75.4.6 → 75.4.7
Minimum Duration: 28-32 hours (with parallelization)
```

### Parallel Opportunities

**Can run in parallel (after 75.4.3):**
- 75.4.4: Dendrogram generation & Ward linkage
- 75.4.5: Quality metrics computation (silhouette, Davies-Bouldin, Calinski-Harabasz)

Both depend only on distance matrix (75.4.3) and are independent of each other. **Estimated parallel execution saves 3-4 hours.**

**Must be sequential:**
- 75.4.1 → 75.4.2 (design prerequisites)
- 75.4.2 → 75.4.3 (need combined metrics for distance)
- 75.4.3 → 75.4.4-75.4.5 (distance matrix input)
- 75.4.4-75.4.5 → 75.4.6 (need cluster assignments)
- 75.4.6 → 75.4.7 (need output format for testing)

### Timeline with Parallelization

**Days 1-2: Design (75.4.1)**
- Review hierarchical agglomerative clustering (HAC)
- Document Ward linkage, Euclidean distance, threshold strategy
- Document quality metrics interpretation

**Days 2-3: Metric Combination (75.4.2)**
- Implement 35/35/30 weighted formula
- Validate inputs from 75.1-75.3
- Test with 10+ branch combinations

**Days 3-4: Distance Matrix (75.4.3)**
- Extract and normalize metric vectors
- Compute pairwise Euclidean distances
- Verify matrix symmetry and diagonal zeros

**Days 4-5: Clustering in Parallel (75.4.4-75.4.5)**
- **75.4.4 (Person A, Days 4-5):** Ward linkage, dendrogram, threshold cutting, cluster assignment
- **75.4.5 (Person B, Days 4-5):** Silhouette, Davies-Bouldin, Calinski-Harabasz scores
- Merge results at end of Day 5

**Days 5-6: Output & Testing (75.4.6-75.4.7)**
- Day 5: Format output dict, cluster characteristics, JSON validation
- Day 6: Implement 8+ unit tests, >95% coverage

---

## Subtasks

### 75.4.1: Design Clustering Architecture
**Purpose:** Define clustering algorithm, linkage method, and quality metrics  
**Effort:** 3-4 hours

**Steps:**
1. Review hierarchical agglomerative clustering (HAC)
2. Document linkage method choice (Ward's method)
3. Document distance metric choice (Euclidean)
4. Define dendrogram cut threshold strategy
5. Define quality metrics (silhouette, Davies-Bouldin, Calinski-Harabasz)

**Success Criteria:**
- [ ] Clustering algorithm documented
- [ ] Linkage method specified
- [ ] Distance metric specified
- [ ] Threshold strategy defined
- [ ] Quality metrics documented

### Implementation Checklist (From HANDOFF)
- [ ] Choose hierarchical agglomerative clustering (HAC) with Ward method
- [ ] Use Euclidean distance metric on normalized vectors
- [ ] Document dendrogram cut threshold strategy (default: 0.5)
- [ ] Define silhouette score range [-1, 1] interpretation
- [ ] Define Davies-Bouldin index (lower is better) interpretation
- [ ] Define Calinski-Harabasz index (higher is better) interpretation

**Blocks:** 75.4.2, 75.4.3, 75.4.4, 75.4.5, 75.4.6

---

### 75.4.2: Implement Metric Combination System
**Purpose:** Combine outputs from 75.1, 75.2, 75.3  
**Effort:** 4-5 hours  
**Depends on:** 75.4.1, 75.1, 75.2, 75.3

**Steps:**
1. Accept output dicts from all three analyzers
2. Validate that all required metrics present
3. Implement 35/35/30 weighted combination formula
4. Verify result is in [0,1] range
5. Create scoring vectors for clustering input

**Success Criteria:**
- [ ] Accepts input from Tasks 75.1, 75.2, 75.3
- [ ] Validates all metrics present
- [ ] Combines using formula: 0.35*c1 + 0.35*c2 + 0.30*c3
- [ ] Returns score in [0, 1] range
- [ ] Can process 10+ branches without error

**Blocks:** 75.4.3, 75.4.4


### Implementation Checklist (From HANDOFF)
- [ ] Validate output from Tasks 75.1, 75.2, 75.3 (required fields present)
- [ ] Implement 35/35/30 weighted combination formula
- [ ] Verify combined_score always in [0, 1] range
- [ ] Create scoring vector for clustering input
- [ ] Test with 10+ branch combinations
---

### 75.4.3: Implement Distance Matrix Calculation
**Purpose:** Compute pairwise distances between branch metric vectors  
**Effort:** 3-4 hours  
**Depends on:** 75.4.2

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
- [ ] Performance acceptable (<1 second for 50 branches)

**Blocks:** 75.4.4


### Implementation Checklist (From HANDOFF)
- [ ] Extract normalized metric vectors for all branches
- [ ] Compute pairwise distances using Euclidean metric
- [ ] Verify distance matrix is symmetric
- [ ] Verify diagonal is zero
- [ ] Format as NxN distance matrix
---

### 75.4.4: Implement Hierarchical Clustering Engine
**Purpose:** Perform Ward linkage clustering and create dendrogram  
**Effort:** 4-5 hours  
**Depends on:** 75.4.3

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

**Blocks:** 75.4.5, 75.4.6


### Implementation Checklist (From HANDOFF)
- [ ] Import scipy.cluster.hierarchy.linkage
- [ ] Implement Ward linkage on distance matrix
- [ ] Generate dendrogram from linkage matrix
- [ ] Cut dendrogram at configured threshold
- [ ] Assign all branches to clusters
---

### 75.4.5: Compute Cluster Quality Metrics
**Purpose:** Calculate silhouette, Davies-Bouldin, Calinski-Harabasz scores  
**Effort:** 3-4 hours  
**Depends on:** 75.4.4

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

**Blocks:** 75.4.7


### Implementation Checklist (From HANDOFF)
- [ ] Compute silhouette score for each branch
- [ ] Compute average silhouette across all branches
- [ ] Compute Davies-Bouldin index
- [ ] Compute Calinski-Harabasz index
- [ ] Ensure no NaN or Inf values in metrics
---

### 75.4.6: Compute Cluster Characteristics
**Purpose:** Calculate cluster centers and membership summaries  
**Effort:** 2-3 hours  
**Depends on:** 75.4.4

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

**Blocks:** 75.4.8


### Implementation Checklist (From HANDOFF)
- [ ] Identify member branches per cluster
- [ ] Compute cluster center (mean of metrics)
- [ ] Calculate cluster size for each cluster
- [ ] Document cluster membership lists
- [ ] Verify all branches assigned to exactly one cluster
---

### 75.4.7: Format Output & Output Validation
**Purpose:** Structure results into JSON dict  
**Effort:** 2-3 hours  
**Depends on:** 75.4.5, 75.4.6

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

**Blocks:** 75.4.8

---

### 75.4.8: Write Unit Tests
**Purpose:** Comprehensive test coverage  
**Effort:** 4-5 hours  
**Depends on:** 75.4.7

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



### Test Case Examples (From HANDOFF)

1. **test_low_distance_clustering**: 3-5 similar branches
   - Expected: Cluster together, silhouette_score > 0.6

2. **test_mixed_distances**: 10 branches with varying metrics
   - Expected: Multiple clusters formed, quality_metrics computed

3. **test_outlier_branch**: 1 branch very different from others
   - Expected: Separate cluster, appropriate silhouette scores

4. **test_all_similar**: All branches similar
   - Expected: 1 large cluster, high silhouette score

5. **test_all_different**: All branches distinct
   - Expected: N clusters (one per branch), valid quality metrics

6. **test_quality_metrics_validity**: Any clustering configuration
   - Expected: silhouette in [-1,1], davies_bouldin >= 0, calinski_harabasz >= 0

7. **test_dendrogram_data_structure**: Linkage matrix structure
   - Expected: Shape (N-1, 4) for N branches

8. **test_performance**: Cluster 50 branches
   - Expected: Complete in <5 seconds

---

## Configuration & Defaults

All parameters should be externalized to configuration files (not hardcoded). Use YAML format:

```yaml
# config/branch_clusterer.yaml
branch_clusterer:
  # Clustering Algorithm
  linkage_method: "ward"  # Options: ward, complete, average, single
  distance_metric: "euclidean"  # Euclidean distance for normalized vectors
  clustering_threshold: 0.5  # Dendrogram cut threshold (0-1)
  
  # Metric Weights
  commit_history_weight: 0.35  # Weight from Task 75.1
  codebase_structure_weight: 0.35  # Weight from Task 75.2
  diff_distance_weight: 0.30  # Weight from Task 75.3
  
  # Quality Metrics
  silhouette_sample_size: 10000  # Sample size for silhouette computation
  davies_bouldin_enabled: true  # Compute Davies-Bouldin index
  calinski_harabasz_enabled: true  # Compute Calinski-Harabasz score
  
  # Cluster Constraints
  min_cluster_size: 2  # Minimum branches per cluster
  max_clusters_ratio: 0.5  # Max clusters = branches * ratio
```

**How to use in code:**
```python
import yaml

def load_config(config_path='config/branch_clusterer.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)['branch_clusterer']

config = load_config()
LINKAGE_METHOD = config['linkage_method']
DISTANCE_METRIC = config['distance_metric']
CLUSTERING_THRESHOLD = config['clustering_threshold']
# ... etc
```

**Why externalize?**
- Adjust thresholds without code recompilation
- Different configurations for dev/test/prod environments
- Enable/disable metrics based on performance needs
- Tune weights based on organizational preferences
- Easy rollback if clustering parameters need adjustment

---

## Dependencies

**Blocked by:**
- Task 75.1 (CommitHistoryAnalyzer)
- Task 75.2 (CodebaseStructureAnalyzer)
- Task 75.3 (DiffDistanceCalculator)

**Blocks:**
- Task 75.5 (IntegrationTargetAssigner)
- Task 75.6 (PipelineIntegration)

**External libraries:**
- scipy.cluster.hierarchy
- scipy.spatial.distance
- sklearn.metrics

---

## Quality Metric Interpretation

- **Silhouette Score:** >0.7 excellent, >0.5 good, <0.25 poor
- **Davies-Bouldin Index:** <1.0 excellent, <1.5 good, <2.0 acceptable
- **Calinski-Harabasz Score:** >10 good, higher is better

---

## Typical Development Workflow

Complete step-by-step git workflow for implementing this task:

### Setup Your Feature Branch

```bash
# 1. Create and push feature branch
git checkout -b feat/branch-clusterer
git push -u origin feat/branch-clusterer

# 2. Create directory structure
mkdir -p src/clustering tests/clustering
touch src/clustering/__init__.py
git add src/clustering/
git commit -m "chore: create clustering module structure"
```

### Subtask 75.4.1: Design Clustering Architecture

```bash
# Document design decisions in code comments
cat > src/clustering/design.md << 'EOF'
# BranchClusterer Design

## Algorithm: Hierarchical Agglomerative Clustering (HAC)
- Linkage Method: Ward (minimizes within-cluster variance)
- Distance Metric: Euclidean on normalized vectors
- Threshold: 0.5 (adjustable via config)

## Quality Metrics
- Silhouette Score: [-1, 1], >0.7 excellent
- Davies-Bouldin Index: lower is better
- Calinski-Harabasz Score: higher is better
EOF

git add src/clustering/design.md
git commit -m "docs: document clustering design (75.4.1)"
```

### Subtask 75.4.2-75.4.3: Metric Combination & Distance Matrix

```bash
cat > src/clustering/metrics.py << 'EOF'
from typing import List, Dict
import numpy as np
from scipy.spatial.distance import pdist, squareform

class MetricCombiner:
    COMMIT_WEIGHT = 0.35
    CODEBASE_WEIGHT = 0.35
    DIFF_WEIGHT = 0.30
    
    @staticmethod
    def combine_metrics(analyzer_outputs: List[Dict]) -> np.ndarray:
        """Combine 75.1, 75.2, 75.3 outputs using weighted formula."""
        combined_scores = []
        for output in analyzer_outputs:
            score = (
                COMMIT_WEIGHT * output['commit_history'] +
                CODEBASE_WEIGHT * output['codebase_structure'] +
                DIFF_WEIGHT * output['diff_distance']
            )
            combined_scores.append(score)
        return np.array(combined_scores)
    
    @staticmethod
    def compute_distance_matrix(vectors: np.ndarray) -> np.ndarray:
        """Compute pairwise Euclidean distances."""
        distances = pdist(vectors, metric='euclidean')
        return squareform(distances)
EOF

git add src/clustering/metrics.py
git commit -m "feat: implement metric combination and distance matrix (75.4.2, 75.4.3)"
```

### Subtask 75.4.4-75.4.5: Clustering & Quality Metrics

```bash
cat > src/clustering/clusterer.py << 'EOF'
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.cluster.hierarchy import cut_tree
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import numpy as np

class BranchClusterer:
    def __init__(self, config: Dict):
        self.linkage_method = config['linkage_method']
        self.threshold = config['clustering_threshold']
    
    def cluster(self, distance_matrix: np.ndarray) -> Dict:
        """Perform clustering and compute quality metrics."""
        # 75.4.4: Linkage computation
        linkage_matrix = linkage(distance_matrix, method=self.linkage_method)
        
        # Cut dendrogram at threshold
        cluster_assignments = fcluster(
            linkage_matrix, 
            t=self.threshold, 
            criterion='distance'
        )
        
        # 75.4.5: Quality metrics
        silhouette = silhouette_score(distance_matrix, cluster_assignments)
        davies_bouldin = davies_bouldin_score(distance_matrix, cluster_assignments)
        calinski_harabasz = calinski_harabasz_score(distance_matrix, cluster_assignments)
        
        return {
            'linkage_matrix': linkage_matrix,
            'cluster_assignments': cluster_assignments,
            'quality_metrics': {
                'silhouette_score': silhouette,
                'davies_bouldin_index': davies_bouldin,
                'calinski_harabasz_score': calinski_harabasz
            }
        }
EOF

git add src/clustering/clusterer.py
git commit -m "feat: implement hierarchical clustering and quality metrics (75.4.4, 75.4.5)"
```

### Subtask 75.4.6-75.4.7: Output & Tests

```bash
# Format output and create test suite
cat > src/clustering/output.py << 'EOF'
def format_output(clustering_result: Dict, branches: List[str]) -> Dict:
    """Format clustering results into output schema."""
    return {
        'clusters': format_clusters(clustering_result, branches),
        'branch_assignments': dict(zip(branches, clustering_result['cluster_assignments'])),
        'quality_metrics': clustering_result['quality_metrics']
    }
EOF

# Create comprehensive tests
cat > tests/clustering/test_clusterer.py << 'EOF'
import pytest
from src.clustering.clusterer import BranchClusterer

class TestBranchClusterer:
    def test_low_distance_clustering(self):
        # 3-5 similar branches should cluster together
        pass
    
    def test_quality_metrics_validity(self):
        # silhouette in [-1,1], davies_bouldin >= 0
        pass
    
    # [8+ test cases total]
EOF

git add src/clustering/output.py tests/clustering/
git commit -m "feat: implement output formatting and comprehensive unit tests (75.4.6, 75.4.7)"
```

### Configuration & Commit

```bash
# Create configuration file
mkdir -p config
cat > config/branch_clusterer.yaml << 'EOF'
branch_clusterer:
  linkage_method: "ward"
  distance_metric: "euclidean"
  clustering_threshold: 0.5
  commit_history_weight: 0.35
  codebase_structure_weight: 0.35
  diff_distance_weight: 0.30
EOF

git add config/
git commit -m "config: branch_clusterer configuration parameters"

# Push and create PR
git push origin feat/branch-clusterer
gh pr create --title "Complete Task 75.4: BranchClusterer" \
             --body "Implements hierarchical clustering with Ward linkage, quality metrics, and comprehensive testing. 28-32 hours of work with parallelization of quality metrics computation."
```

---

## Integration Handoff

### What Gets Passed to Task 75.5

**Task 75.5 (IntegrationTargetAssigner) expects input in this format:**

```python
from src.clustering.clusterer import BranchClusterer

clusterer = BranchClusterer(config)
clustering_output = clusterer.cluster(distance_matrix)

# Output is a dict with:
# {
#   "clusters": [
#     {
#       "cluster_id": 0,
#       "member_branches": ["branch1", "branch2", ...],
#       "cluster_center": {...},
#       "quality_metrics": {
#         "silhouette_score": 0.65,
#         "davies_bouldin_index": 1.2,
#         "calinski_harabasz_score": 15.3
#       }
#     }
#   ],
#   "branch_assignments": {"branch1": 0, "branch2": 0, ...},
#   "overall_quality": {...}
# }
```

**Task 75.5 uses these outputs by:**
1. Reading cluster assignments to group similar branches
2. Using cluster quality metrics to assess confidence in grouping
3. Using cluster centers to match branches against target archetypes
4. Using branch-to-cluster mappings to drive assignment decision hierarchy

**Validation before handoff:**
```bash
# Verify output matches specification
python -c "
from src.clustering.clusterer import BranchClusterer
clusterer = BranchClusterer({...})
result = clusterer.cluster(distance_matrix)

# Check required fields
assert 'clusters' in result
assert 'branch_assignments' in result
assert 'overall_quality' in result

# Check value ranges
for cluster in result['clusters']:
    assert 'cluster_id' in cluster
    assert 'member_branches' in cluster
    assert 'cluster_center' in cluster
    assert 'quality_metrics' in cluster
    
# Check metric ranges
quality = result['overall_quality']
assert -1 <= quality['silhouette_score'] <= 1
assert quality['davies_bouldin_index'] >= 0
assert quality['calinski_harabasz_score'] >= 0

print('✓ Output valid and ready for Task 75.5')
"
```

---

## Common Gotchas & Solutions

### Gotcha 1: NaN Values in Quality Metrics ⚠️

**Problem:** Silhouette, Davies-Bouldin, or Calinski-Harabasz scores contain NaN or Inf
**Symptom:** Quality metrics validation fails; downstream tasks receive invalid data
**Root Cause:** Edge cases like single-element clusters, identical vectors, or constant features cause undefined metric calculations

**Solution:**
```python
import numpy as np
from sklearn.metrics import silhouette_score

def compute_safe_silhouette(X, labels):
    """Compute silhouette score with NaN handling."""
    try:
        score = silhouette_score(X, labels)
        if np.isnan(score) or np.isinf(score):
            # Fallback: all similar or all different
            return 0.0 if len(np.unique(labels)) == 1 else -0.1
        return score
    except Exception as e:
        logger.warning(f"Silhouette computation failed: {e}")
        return 0.0
```

**Test:**
```python
def test_quality_metrics_validity():
    # Edge case: single cluster
    labels = np.array([0, 0, 0])
    X = np.array([[1, 2], [1, 2], [1, 2]])
    score = compute_safe_silhouette(X, labels)
    assert not np.isnan(score) and not np.isinf(score)
    assert score == 0.0  # Single cluster is neutral
```

---

### Gotcha 2: Distance Matrix Not Symmetric ⚠️

**Problem:** pdist/squareform produces asymmetric distance matrix
**Symptom:** scipy.cluster.hierarchy.linkage fails or produces incorrect clustering
**Root Cause:** Floating-point arithmetic or incorrect distance computation

**Solution:**
```python
def compute_distance_matrix_safe(vectors):
    """Compute symmetric distance matrix."""
    distances = pdist(vectors, metric='euclidean')
    matrix = squareform(distances)
    
    # Ensure symmetry
    matrix = (matrix + matrix.T) / 2.0
    
    # Verify diagonal is zero
    np.fill_diagonal(matrix, 0)
    
    assert np.allclose(matrix, matrix.T), "Distance matrix not symmetric"
    assert np.allclose(np.diag(matrix), 0), "Diagonal not zero"
    
    return matrix
```

**Test:**
```python
def test_distance_matrix_symmetric():
    vectors = np.array([[0.5, 0.3], [0.7, 0.8], [0.2, 0.9]])
    matrix = compute_distance_matrix_safe(vectors)
    
    assert np.allclose(matrix, matrix.T)
    assert np.allclose(np.diag(matrix), 0)
```

---

### Gotcha 3: Ward Linkage Requires Euclidean Distance ⚠️

**Problem:** Using non-Euclidean distances with Ward linkage produces invalid linkage matrix
**Symptom:** scipy error "Ward only works with Euclidean distances"
**Root Cause:** Ward linkage formula mathematically requires Euclidean distance

**Solution:**
```python
def linkage_safe(distance_matrix, method='ward'):
    """Compute linkage with validation."""
    if method == 'ward':
        # Ward requires Euclidean distances, use pdist directly
        from scipy.spatial.distance import pdist, squareform
        # OR convert from distance matrix
        Z = linkage(distance_matrix, method='ward')
    else:
        Z = linkage(distance_matrix, method=method)
    
    assert Z.shape[1] == 4, "Linkage matrix has wrong shape"
    return Z
```

**Test:**
```python
def test_ward_linkage_valid():
    distance_matrix = compute_distance_matrix(vectors)
    Z = linkage(distance_matrix, method='ward')
    assert Z.shape[0] == len(vectors) - 1
    assert Z.shape[1] == 4
```

---

### Gotcha 4: All Branches in Single Cluster ⚠️

**Problem:** Dendrogram threshold too high → all branches cluster together
**Symptom:** Only 1 cluster created; silhouette score undefined (requires 2+ clusters)
**Root Cause:** Threshold value too conservative; similar metrics → high distances required to split

**Solution:**
```python
def cluster_with_min_clusters(linkage_matrix, vectors, threshold, min_clusters=2):
    """Ensure minimum number of clusters."""
    labels = fcluster(linkage_matrix, t=threshold, criterion='distance')
    
    # If only one cluster, use different criterion
    if len(np.unique(labels)) < min_clusters:
        n_clusters = max(min_clusters, len(np.unique(vectors)) // 10)
        labels = fcluster(linkage_matrix, t=n_clusters, criterion='maxclust')
    
    return labels
```

**Test:**
```python
def test_minimum_clusters_enforced():
    # All similar branches
    similar_vectors = np.array([[0.5, 0.5]] * 5)
    labels = cluster_with_min_clusters(Z, similar_vectors, threshold=0.5, min_clusters=2)
    assert len(np.unique(labels)) >= 2
```

---

### Gotcha 5: Memory Explosion with Large Branch Sets ⚠️

**Problem:** Distance matrix O(n²) memory for large n; 100 branches → 10,000 values per metric
**Symptom:** Out of memory error during clustering
**Root Cause:** Creating full distance matrix instead of condensed distance vector

**Solution:**
```python
def memory_efficient_clustering(vectors):
    """Use condensed distance format."""
    from scipy.spatial.distance import pdist, squareform
    
    # Use condensed format during computation
    condensed_distances = pdist(vectors, metric='euclidean')
    
    # linkage accepts condensed format directly
    Z = linkage(condensed_distances, method='ward')
    
    # Only expand to full matrix if needed for metrics
    if need_full_matrix:
        full_matrix = squareform(condensed_distances)
    
    return Z
```

**Benchmark:**
```python
def test_memory_usage():
    vectors = np.random.rand(100, 10)
    condensed = pdist(vectors)  # ~5000 values
    
    import sys
    assert sys.getsizeof(condensed) < 100_000  # << full matrix ~80KB
```

---

### Gotcha 6: Invalid Threshold Values ⚠️

**Problem:** Threshold outside valid range causes incorrect cluster assignments
**Symptom:** Dendrogram cutting produces unexpected cluster counts
**Root Cause:** Threshold not normalized to [0, max_distance]

**Solution:**
```python
def validate_threshold(linkage_matrix, threshold):
    """Validate and normalize threshold."""
    max_distance = linkage_matrix[-1, 2]  # Last merge distance
    
    if threshold < 0 or threshold > max_distance:
        logger.warning(f"Threshold {threshold} outside [0, {max_distance}]")
        threshold = min(max_distance * 0.5, threshold)  # Default to 50% of max
    
    return threshold
```

**Test:**
```python
def test_threshold_validation():
    Z = linkage(distance_matrix, method='ward')
    max_dist = Z[-1, 2]
    
    valid = validate_threshold(Z, 0.5)
    assert 0 <= valid <= max_dist
```

---

### Gotcha 7: Comparing Metrics Across Different Clustering Thresholds ⚠️

**Problem:** Silhouette scores not comparable when threshold changes cluster count
**Symptom:** Quality metrics inconsistent; hard to choose optimal threshold
**Root Cause:** Different number of clusters → different metric ranges

**Solution:**
```python
def find_optimal_threshold(linkage_matrix, vectors, thresholds):
    """Find threshold maximizing silhouette score."""
    best_threshold = None
    best_score = -2
    
    for threshold in thresholds:
        labels = fcluster(linkage_matrix, t=threshold, criterion='distance')
        
        # Skip single-cluster solutions
        if len(np.unique(labels)) < 2:
            continue
        
        score = silhouette_score(vectors, labels)
        if score > best_score:
            best_score = score
            best_threshold = threshold
    
    return best_threshold
```

**Test:**
```python
def test_optimal_threshold_selection():
    thresholds = [0.1, 0.3, 0.5, 0.7, 0.9]
    optimal = find_optimal_threshold(Z, vectors, thresholds)
    assert optimal in thresholds
```

---

### Gotcha 8: Dendrogram Data Structure Misalignment ⚠️

**Problem:** Linkage matrix has wrong shape or format for downstream tasks
**Symptom:** Task 75.5 can't parse cluster data; visualization fails
**Root Cause:** Inconsistent dendrogram format or missing required fields

**Solution:**
```python
def validate_dendrogram_format(linkage_matrix):
    """Validate linkage matrix conforms to expected format."""
    n_rows, n_cols = linkage_matrix.shape
    
    # Linkage matrix must have shape (n_samples - 1, 4)
    assert n_cols == 4, f"Linkage matrix should have 4 columns, got {n_cols}"
    
    # Check column ranges
    assert np.all(linkage_matrix[:, 0] >= 0), "Column 0 (sample idx 1) out of range"
    assert np.all(linkage_matrix[:, 1] >= 0), "Column 1 (sample idx 2) out of range"
    assert np.all(linkage_matrix[:, 2] >= 0), "Column 2 (distances) negative"
    assert np.all(linkage_matrix[:, 3] > 0), "Column 3 (cluster size) invalid"
    
    return True
```

**Test:**
```python
def test_dendrogram_valid_format():
    Z = linkage(distance_matrix, method='ward')
    assert validate_dendrogram_format(Z)
    assert Z.shape[0] == len(vectors) - 1
    assert Z.shape[1] == 4
```

---

## Integration Checkpoint

**When to move to 75.5:**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Accepts output from Tasks 75.1, 75.2, 75.3
- [ ] Output matches specification
- [ ] Quality metrics validated
- [ ] Commit message: "feat: complete Task 75.4 BranchClusterer"

---

## Done Definition

Task 75.4 is done when:
1. All 8 subtasks marked complete
2. Accepts output from Tasks 75.1, 75.2, 75.3
3. Unit tests all passing
4. Code review approved
5. Outputs match specification
6. Ready for hand-off to Task 75.5
