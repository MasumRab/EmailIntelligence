# Task 75.6: Pipeline Integration Module

## Quick Summary
Implement the pipeline orchestration module that integrates all Stage One and Stage Two components into a unified execution workflow. This is a Stage Two component—depends on Tasks 75.1-75.5.

**Effort:** 20-28 hours | **Complexity:** 6/10 | **Parallelizable:** No (depends on all Stage One)

---

## What to Build

A Python module `BranchClusteringPipeline` that:
1. Orchestrates execution of all five analyzers
2. Handles data flow between components
3. Manages caching and incremental updates
4. Generates final JSON outputs
5. Integrates with downstream tasks (79, 80, 83, 101)

### Class Signature
```python
class BranchClusteringPipeline:
    def __init__(self, repo_path: str, config: dict = None)
    def run(self, branches: list = None, use_cache: bool = True) -> dict
    def get_branch_tags(self, branch_name: str) -> list
    def export_json_outputs(self, output_dir: str) -> dict
```

---

## Execution Flow

```
Input: List of branches
  ↓
┌─────────────────────────────────────┐
│ Parallelize (if use_cache=True):    │
│  • CommitHistoryAnalyzer            │ → Task 75.1 output
│  • CodebaseStructureAnalyzer        │ → Task 75.2 output
│  • DiffDistanceCalculator           │ → Task 75.3 output
└─────────────────────────────────────┘
  ↓
  Combine metrics (weighted 35/35/30)
  ↓
┌─────────────────────────────────────┐
│ BranchClusterer                     │ → Task 75.4 output
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│ IntegrationTargetAssigner           │ → Task 75.5 output
└─────────────────────────────────────┘
  ↓
Output: Three JSON files
  • categorized_branches.json
  • clustered_branches.json
  • enhanced_orchestration_branches.json
```

---

## Input Specification

### Input 1: Branch List
```python
branches = [
    "feature/auth-system",
    "feature/api-refactor",
    "feature/data-pipeline",
    ...
]
```

### Input 2: Optional Configuration
```python
config = {
    "commit_history_weight": 0.35,
    "codebase_structure_weight": 0.35,
    "diff_distance_weight": 0.30,
    "clustering_threshold": 0.5,
    "cache_dir": ".taskmaster/cache/",
    "use_parallel": True,
    "max_workers": 4
}
```

---

## Output Specification

### Output 1: categorized_branches.json
```json
{
  "metadata": {
    "generated_timestamp": "2025-12-22T10:55:00Z",
    "total_branches": 13,
    "total_clusters": 3,
    "pipeline_version": "1.0"
  },
  "branches": {
    "feature/auth-system": {
      "branch_name": "feature/auth-system",
      "integration_target": "main",
      "cluster_id": 0,
      "confidence": 0.92,
      "tags": ["core-feature", "security-sensitive", ...],
      "metrics": {
        "commit_history_aggregate": 0.749,
        "codebase_structure_aggregate": 0.794,
        "diff_distance_aggregate": 0.750,
        "combined_score": 0.764
      }
    },
    ...
  },
  "summary": {
    "by_target": {
      "main": 8,
      "scientific": 3,
      "orchestration-tools": 2
    },
    "by_risk": {
      "low-risk": 7,
      "medium-risk": 5,
      "high-risk": 1
    }
  }
}
```

### Output 2: clustered_branches.json
```json
{
  "metadata": {
    "generated_timestamp": "2025-12-22T10:55:00Z",
    "clustering_method": "hierarchical_agglomerative",
    "linkage_method": "ward",
    "distance_metric": "euclidean",
    "threshold": 0.5
  },
  "clusters": [
    {
      "cluster_id": 0,
      "size": 8,
      "branches": ["feature/auth-system", ...],
      "center": {
        "commit_history_weight": 0.749,
        "codebase_structure_weight": 0.794,
        "diff_distance_weight": 0.750,
        "combined_score": 0.764
      },
      "cohesion": 0.92,
      "silhouette_score": 0.68
    },
    ...
  ],
  "quality_metrics": {
    "silhouette_avg": 0.71,
    "davies_bouldin_index": 0.85,
    "calinski_harabasz_index": 15.3
  },
  "dendrogram_html": "path/to/dendrogram.html"
}
```

### Output 3: enhanced_orchestration_branches.json
```json
{
  "metadata": {
    "generated_timestamp": "2025-12-22T10:55:00Z",
    "orchestration_branches_count": 24,
    "pipeline_version": "1.0"
  },
  "branches": [
    {
      "branch_name": "feature/orchestration-auth",
      "integration_target": "orchestration-tools",
      "cluster_id": 2,
      "confidence": 0.81,
      "tags": ["orchestration-branch", "authentication", ...],
      "metrics": {...},
      "execution_context": {
        "parallel_capability": true,
        "test_intensity": "high",
        "validation_suites": ["unit", "integration", "orchestration"]
      }
    },
    ...
  ],
  "orchestration_summary": {
    "total_branches": 24,
    "by_capability": {
      "parallelizable": 18,
      "serial": 6
    },
    "validation_distribution": {
      "high_intensity": 8,
      "medium_intensity": 12,
      "low_intensity": 4
    }
  }
}
```

---

## Implementation Checklist

- [ ] Create `BranchClusteringPipeline` class
- [ ] Initialize with repo_path and optional config
- [ ] Implement `run()` method with orchestration logic
- [ ] Implement parallelization for Tasks 75.1-75.3 (if use_parallel=True)
- [ ] Instantiate and call CommitHistoryAnalyzer for each branch
- [ ] Instantiate and call CodebaseStructureAnalyzer for each branch
- [ ] Instantiate and call DiffDistanceCalculator for each branch
- [ ] Combine metrics (35/35/30 weighting)
- [ ] Instantiate and call BranchClusterer
- [ ] Instantiate and call IntegrationTargetAssigner
- [ ] Generate categorized_branches.json
- [ ] Generate clustered_branches.json
- [ ] Generate enhanced_orchestration_branches.json (filter for orchestration-tools)
- [ ] Implement caching layer (save intermediate outputs)
- [ ] Implement `get_branch_tags(branch_name)` utility method
- [ ] Implement `export_json_outputs(output_dir)` method
- [ ] Add logging and progress reporting
- [ ] Return pipeline results dict
- [ ] Add docstrings (Google style)

---

## Caching Strategy

```python
# Cache structure
.taskmaster/cache/
├── branch_metrics/
│   ├── feature__auth-system__commit_history.json
│   ├── feature__auth-system__codebase_structure.json
│   ├── feature__auth-system__diff_distance.json
│   └── ...
├── pipeline_results/
│   ├── last_run.json
│   └── history.log
└── dendrograms/
    └── dendrogram_2025-12-22.html

# On run():
# 1. Check cache for branch metrics
# 2. Re-run analyzers only for cache misses
# 3. Save new metrics to cache
# 4. Always re-run clustering/assignment (combines metrics)
```

---

## Parallelization Strategy

Use `concurrent.futures.ThreadPoolExecutor`:

```python
def run_analyzers_parallel(self, branches: list):
    with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
        futures = {}
        
        # Submit commit history analyzer tasks
        for branch in branches:
            future = executor.submit(
                self.commit_history_analyzer.analyze, branch
            )
            futures[('commit', branch)] = future
        
        # Submit codebase structure analyzer tasks
        for branch in branches:
            future = executor.submit(
                self.codebase_structure_analyzer.analyze, branch
            )
            futures[('codebase', branch)] = future
        
        # Submit diff distance analyzer tasks
        for branch in branches:
            future = executor.submit(
                self.diff_distance_calculator.analyze, branch
            )
            futures[('diff', branch)] = future
        
        # Collect results
        results = {}
        for key, future in futures.items():
            results[key] = future.result()
        
        return results
```

---

## Downstream Integration Points

### Task 79 (Execution Control)
Uses execution context tags:
- `parallel_capability`: true/false (Task 75 provides via tags)
- `serial_dependency_count`: inferred from tag analysis

### Task 80 (Validation Intensity Selection)
Uses complexity tags:
- `simple` → low intensity
- `moderate` → medium intensity
- `complex` → high intensity

### Task 83 (Test Suite Selection)
Uses validation tags:
- `testing-required-high` → full test suite
- `testing-required-medium` → integration tests
- `testing-optional` → smoke tests only

### Task 101 (Orchestration Filter)
Uses orchestration tags:
- `orchestration-branch` → passes filter
- Others → filtered out

---

## Configuration

Accept these parameters in `__init__` or config file:

```python
CONFIG_DEFAULTS = {
    "commit_history_weight": 0.35,
    "codebase_structure_weight": 0.35,
    "diff_distance_weight": 0.30,
    "clustering_threshold": 0.5,
    "cache_dir": ".taskmaster/cache/",
    "output_dir": ".taskmaster/outputs/",
    "use_parallel": True,
    "max_workers": 4,
    "cache_retention_days": 7,
    "generate_dendrogram": True,
    "verbose_logging": False
}
```

---

## Test Cases

1. **Fresh run**: No cache, analyze 10 branches, export all outputs
2. **Incremental run**: 2 new branches added, use cache for others
3. **Single branch**: Run pipeline for single branch (e.g., debugging)
4. **Large batch**: 50+ branches (test parallelization)
5. **Cache refresh**: Force re-analysis of all branches

---

## Dependencies

- All Stage One components: Task 75.1-75.3 (classes must be importable)
- Stage One clustering: Task 75.4 (BranchClusterer)
- Stage Two assignment: Task 75.5 (IntegrationTargetAssigner)
- Python built-in: `json`, `logging`, `pathlib`, `concurrent.futures`
- Optional: `plotly` for dendrogram HTML generation
- Feeds into **Task 75.7 (Visualization & Reporting)**

---

## Logging Output

```
[2025-12-22 10:55:00] INFO: BranchClusteringPipeline initialized (13 branches)
[2025-12-22 10:55:01] INFO: Using cache for 10 branches, analyzing 3 new branches
[2025-12-22 10:55:05] INFO: CommitHistoryAnalyzer: completed 3/3
[2025-12-22 10:55:10] INFO: CodebaseStructureAnalyzer: completed 3/3
[2025-12-22 10:55:15] INFO: DiffDistanceCalculator: completed 3/3
[2025-12-22 10:55:20] INFO: BranchClusterer: 13 branches → 3 clusters
[2025-12-22 10:55:22] INFO: IntegrationTargetAssigner: 13 branches assigned
[2025-12-22 10:55:25] INFO: Generated categorized_branches.json (8 main, 3 scientific, 2 orchestration)
[2025-12-22 10:55:26] INFO: Pipeline complete. Results saved to .taskmaster/outputs/
```

---

## Next Steps After Completion

1. Unit test with 5-10 branch fixtures
2. Integration test with real repo (13 branches)
3. Verify JSON output schema validation
4. Test caching and incremental updates
5. Pass outputs to Task 75.7 (Visualization & Reporting)

**Blocked by:** 75.1, 75.2, 75.3, 75.4, 75.5 (all must complete first)
**Enables:** 75.7, 75.8, 75.9 (Stage Three)
