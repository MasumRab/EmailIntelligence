# Task 0075.4: BranchClusterer

## Purpose
Create a hierarchical clustering engine that combines normalized metrics from Tasks 075.1-075.3, performs Ward linkage clustering, and generates cluster assignments with quality metrics. This is the Stage One integration component that produces categorized branches for downstream processing.

**Scope:** BranchClusterer class only  
**Effort:** 28-36 hours | **Complexity:** 8/10  
**Status:** Ready when 075.1, 075.2, 075.3 complete  
**Blocks:** Tasks 075.5 and 075.6

---

## Success Criteria

Task 0075.4 is complete when:

**Core Functionality:**
- [ ] `BranchClusterer` class accepts analyzer outputs from Tasks 075.1, 075.2, 075.3
- [ ] Successfully combines metrics using 35/35/30 weighted formula
- [ ] Performs hierarchical agglomerative clustering with Ward's linkage method
- [ ] Computes cluster quality metrics (silhouette, Davies-Bouldin, Calinski-Harabasz)
- [ ] Outputs properly formatted dict with cluster assignments and quality metrics
- [ ] Output matches JSON schema exactly

**Quality Assurance:**
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <5 seconds for clustering 50+ branches
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

**Integration Readiness:**
- [ ] Compatible with Task 0075.5 (IntegrationTargetAssigner) input requirements
- [ ] Compatible with Task 0075.6 (PipelineIntegration) consumption patterns
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Subtasks

### 075.4.1: Design Clustering Architecture
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

**Blocks:** 075.4.2, 075.4.3, 075.4.4, 075.4.5, 075.4.6

---

### 075.4.2: Implement Metric Combination System
**Purpose:** Combine outputs from 075.1, 075.2, 075.3  
**Effort:** 4-5 hours  
**Depends on:** 075.4.1, 075.1, 075.2, 075.3

**Steps:**
1. Accept output dicts from all three analyzers
2. Validate that all required metrics present
3. Implement 35/35/30 weighted combination formula
4. Verify result is in [0,1] range
5. Create scoring vectors for clustering input

**Success Criteria:**
- [ ] Accepts input from Tasks 075.1, 075.2, 075.3
- [ ] Validates all metrics present
- [ ] Combines using formula: 0.35*c1 + 0.35*c2 + 0.30*c3
- [ ] Returns score in [0, 1] range
- [ ] Can process 10+ branches without error

**Blocks:** 075.4.3, 075.4.4

---

### 075.4.3: Implement Distance Matrix Calculation
**Purpose:** Compute pairwise distances between branch metric vectors  
**Effort:** 3-4 hours  
**Depends on:** 075.4.2

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

**Blocks:** 075.4.4

---

### 075.4.4: Implement Hierarchical Clustering Engine
**Purpose:** Perform Ward linkage clustering and create dendrogram  
**Effort:** 4-5 hours  
**Depends on:** 075.4.3

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

**Blocks:** 075.4.5, 075.4.6

---

### 075.4.5: Compute Cluster Quality Metrics
**Purpose:** Calculate silhouette, Davies-Bouldin, Calinski-Harabasz scores  
**Effort:** 3-4 hours  
**Depends on:** 075.4.4

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

**Blocks:** 075.4.7

---

### 075.4.6: Compute Cluster Characteristics
**Purpose:** Calculate cluster centers and membership summaries  
**Effort:** 2-3 hours  
**Depends on:** 075.4.4

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

**Blocks:** 075.4.8

---

### 075.4.7: Format Output & Output Validation
**Purpose:** Structure results into JSON dict  
**Effort:** 2-3 hours  
**Depends on:** 075.4.5, 075.4.6

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

**Blocks:** 075.4.8

---

### 075.4.8: Write Unit Tests
**Purpose:** Comprehensive test coverage  
**Effort:** 4-5 hours  
**Depends on:** 075.4.7

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

## Configuration Parameters

- `LINKAGE_METHOD` = "ward"
- `DISTANCE_METRIC` = "euclidean"
- `CLUSTERING_THRESHOLD` = 0.5
- `COMMIT_HISTORY_WEIGHT` = 0.35
- `CODEBASE_STRUCTURE_WEIGHT` = 0.35
- `DIFF_DISTANCE_WEIGHT` = 0.30
- `SILHOUETTE_SAMPLE_SIZE` = 10000
- `MIN_CLUSTER_SIZE` = 2
- `MAX_CLUSTERS_RATIO` = 0.5

---

## Dependencies

**Blocked by:**
- Task 0075.1 (CommitHistoryAnalyzer)
- Task 0075.2 (CodebaseStructureAnalyzer)
- Task 0075.3 (DiffDistanceCalculator)

**Blocks:**
- Task 0075.5 (IntegrationTargetAssigner)
- Task 0075.6 (PipelineIntegration)

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

## Integration Checkpoint

**When to move to 075.5:**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Accepts output from Tasks 075.1, 075.2, 075.3
- [ ] Output matches specification
- [ ] Quality metrics validated
- [ ] Commit message: "feat: complete Task 0075.4 BranchClusterer"

---


---

## Helper Tools (Optional)

The following tools are available to accelerate work or provide validation. **None are required** - every task is completable using only the steps in this file.

### Progress Logging

After completing each sub-subtask, optionally log progress for multi-session continuity:

```python
from memory_api import AgentMemory

memory = AgentMemory()
memory.load_session()

# After completing a sub-subtask
memory.add_work_log(
    action="Completed Task 075.X.Y",
    details="Implementation details and progress"
)
memory.update_todo("task_075_x_y", "completed")
memory.save_session()
```

**What this does:** Maintains session state across work sessions, enables agent handoffs, documents progress.  
**Required?** No - git commits are sufficient.  
**See:** MEMORY_API_FOR_TASKS.md for full usage patterns and examples.

### Check Next Task

After completing this task, see what's next:

```bash
python scripts/next_task.py
```

**See:** SCRIPTS_IN_TASK_WORKFLOW.md § next_task.py for details.

---

## Tools Reference

| Tool | Purpose | When to Use | Required? |
|------|---------|-----------|----------|
| Memory API | Progress logging | After each sub-subtask | No |
| next_task.py | Find next task | After completion | No |

**For detailed usage and troubleshooting:** See SCRIPTS_IN_TASK_WORKFLOW.md (all optional tools documented there)

## Done Definition

Task 0075.4 is done when:
1. All 8 subtasks marked complete
2. Accepts output from Tasks 075.1, 075.2, 075.3
3. Unit tests all passing
4. Code review approved
5. Outputs match specification
6. Ready for hand-off to Task 0075.5


**Last Updated:** January 6, 2026  
**Phase:** 2 Shallow Retrofit  
**Structure:** TASK_STRUCTURE_STANDARD.md
