# Task 002.6: PipelineIntegration

**Status:** Ready for Implementation
**Priority:** High
**Effort:** 20-28 hours
**Complexity:** 6/10
**Dependencies:** 002.1, 002.2, 002.3, 002.4, 002.5

---

## Overview/Purpose

Implement the `BranchClusteringPipeline` class that orchestrates all Stage One and Stage Two components into a unified execution workflow. This module ties together the three analyzers (002.1-002.3), the clusterer (002.4), and the target assigner (002.5) into a single pipeline that produces three JSON output files, manages caching, and supports parallel execution.

**Scope:** BranchClusteringPipeline class and output generation
**Depends on:** All five preceding components (002.1 through 002.5)

---

## Success Criteria

Task 002.6 is complete when:

### Core Functionality
- [ ] `BranchClusteringPipeline` class accepts `repo_path` and optional `config`
- [ ] `run()` method orchestrates all five components in correct order
- [ ] Stage One analyzers (002.1-002.3) run in parallel via ThreadPoolExecutor when enabled
- [ ] `get_branch_tags()` returns tags for a single branch
- [ ] `export_json_outputs()` writes three JSON files to output directory
- [ ] Caching layer stores/retrieves intermediate analyzer results
- [ ] Output files match schemas exactly

### Quality Assurance
- [ ] Unit tests pass (minimum 5 test scenarios with >95% coverage)
- [ ] Parallel execution produces same results as serial execution
- [ ] Cache invalidation works correctly for new/changed branches
- [ ] No exceptions for valid inputs including edge cases
- [ ] Code quality: PEP 8 compliant, Google-style docstrings

### Integration Readiness
- [ ] Output JSON files consumable by Tasks 79, 80, 83, 101
- [ ] Logging output matches expected format
- [ ] Configuration externalized and validated
- [ ] Pipeline version tracked in output metadata

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 002.1 (CommitHistoryAnalyzer) complete and importable
- [ ] Task 002.2 (CodebaseStructureAnalyzer) complete and importable
- [ ] Task 002.3 (DiffDistanceCalculator) complete and importable
- [ ] Task 002.4 (BranchClusterer) complete and importable
- [ ] Task 002.5 (IntegrationTargetAssigner) complete and importable

### Blocks (What This Task Unblocks)
- Task 79 (Execution Control)
- Task 80 (Validation Intensity Selection)
- Task 83 (Test Suite Selection)
- Task 101 (Orchestration Filter)

### External Dependencies
- Python built-in: `json`, `logging`, `pathlib`, `concurrent.futures`, `datetime`
- Optional: `plotly` for dendrogram HTML generation

---

## Sub-subtasks Breakdown

### 002.6.1: Pipeline Class Skeleton and Configuration
**Effort:** 2-3 hours
**Depends on:** None (within this task)

**Steps:**
1. Create BranchClusteringPipeline class with __init__
2. Load and validate configuration with defaults
3. Instantiate all five component classes
4. Set up logging

**Success Criteria:**
- [ ] Class initializes without errors
- [ ] Config merges user values with defaults
- [ ] All five components instantiated
- [ ] Logger configured with standard format

---

### 002.6.2: Serial Execution Pipeline
**Effort:** 3-4 hours
**Depends on:** 002.6.1

**Steps:**
1. Implement run() with serial execution flow
2. Call analyzers for each branch sequentially
3. Pass combined metrics to BranchClusterer
4. Pass cluster data to IntegrationTargetAssigner
5. Return complete pipeline results

**Success Criteria:**
- [ ] Pipeline executes all components in correct order
- [ ] Data flows correctly between components
- [ ] Results include all component outputs

---

### 002.6.3: Parallel Execution with ThreadPoolExecutor
**Effort:** 3-4 hours
**Depends on:** 002.6.2

**Steps:**
1. Implement run_analyzers_parallel() using ThreadPoolExecutor
2. Submit all three analyzers per branch concurrently
3. Collect results with future.result()
4. Verify identical output to serial execution

**Success Criteria:**
- [ ] Parallel results match serial results exactly
- [ ] max_workers is configurable
- [ ] Graceful handling of analyzer failures in parallel mode

---

### 002.6.4: Caching Layer
**Effort:** 3-4 hours
**Depends on:** 002.6.2

**Steps:**
1. Create cache directory structure
2. Save analyzer results per branch to JSON files
3. Check cache on run, skip analysis for cached branches
4. Implement cache_retention_days expiration
5. Force refresh option (use_cache=False)

**Success Criteria:**
- [ ] Cache hit skips analyzer re-execution
- [ ] Cache miss triggers fresh analysis
- [ ] Expired cache entries are re-analyzed
- [ ] use_cache=False forces full re-analysis

---

### 002.6.5: JSON Output Generation
**Effort:** 4-5 hours
**Depends on:** 002.6.2

**Steps:**
1. Generate categorized_branches.json with metadata and summary
2. Generate clustered_branches.json with cluster details and quality metrics
3. Generate enhanced_orchestration_branches.json filtered for orchestration targets
4. Implement export_json_outputs() method

**Success Criteria:**
- [ ] All three JSON files match schemas exactly
- [ ] Metadata includes timestamp, version, counts
- [ ] enhanced_orchestration_branches.json filters correctly
- [ ] Files written atomically (temp + rename)

---

### 002.6.6: Utility Methods and Logging
**Effort:** 2-3 hours
**Depends on:** 002.6.5

**Steps:**
1. Implement get_branch_tags(branch_name) utility
2. Add progress logging throughout pipeline
3. Add timing information to logs
4. Add error handling and recovery

**Success Criteria:**
- [ ] get_branch_tags returns correct tags for any branch
- [ ] Log output matches expected format (see Logging section)
- [ ] Pipeline failures produce actionable error messages

---

### 002.6.7: Integration Testing
**Effort:** 3-4 hours
**Depends on:** 002.6.3, 002.6.4, 002.6.5, 002.6.6

**Steps:**
1. Test fresh run (no cache, 10 branches)
2. Test incremental run (2 new branches, cached others)
3. Test single branch mode
4. Test large batch (50+ branches with parallelization)
5. Test cache refresh (force re-analysis)

**Success Criteria:**
- [ ] All 5 test scenarios pass
- [ ] Parallel and serial produce identical results
- [ ] Cache correctly handles all scenarios

---

## Specification Details

### Class Interface

```python
class BranchClusteringPipeline:
    def __init__(self, repo_path: str, config: dict = None):
        """Initialize pipeline with all components.

        Args:
            repo_path: Path to the git repository.
            config: Optional configuration overrides.
        """

    def run(self, branches: list = None, use_cache: bool = True) -> dict:
        """Execute full pipeline for given branches.

        Args:
            branches: List of branch names. If None, discovers all branches.
            use_cache: Whether to use cached analyzer results.

        Returns:
            Complete pipeline results dict.
        """

    def get_branch_tags(self, branch_name: str) -> list:
        """Get tags for a specific branch from last pipeline run.

        Args:
            branch_name: Name of the branch.

        Returns:
            List of tag strings.
        """

    def export_json_outputs(self, output_dir: str) -> dict:
        """Export pipeline results as three JSON files.

        Args:
            output_dir: Directory to write output files.

        Returns:
            Dict with paths to generated files.
        """
```

### Execution Flow Diagram

```
Input: List of branches
  │
  ▼
┌─────────────────────────────────────────┐
│  Stage One (Parallel if use_parallel):  │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │ CommitHistoryAnalyzer (002.1)   │────│──▶ commit_history scores
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │ CodebaseStructureAnalyzer(002.2)│────│──▶ codebase_structure scores
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │ DiffDistanceCalculator (002.3)  │────│──▶ diff_distance scores
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
  │
  ▼ Combined metrics (weighted 35/35/30)
  │
┌─────────────────────────────────────────┐
│  BranchClusterer (002.4)                │
│  → clusters, assignments, quality       │
└─────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────┐
│  IntegrationTargetAssigner (002.5)      │
│  → targets, tags, confidence            │
└─────────────────────────────────────────┘
  │
  ▼ Output: Three JSON files
  │
  ├──▶ categorized_branches.json
  ├──▶ clustered_branches.json
  └──▶ enhanced_orchestration_branches.json
```

### Output Schema 1: categorized_branches.json

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
      "tags": ["core-feature", "security-sensitive", "low-risk"],
      "metrics": {
        "commit_history_aggregate": 0.749,
        "codebase_structure_aggregate": 0.794,
        "diff_distance_aggregate": 0.750,
        "combined_score": 0.764
      }
    }
  },
  "summary": {
    "by_target": {"main": 8, "scientific": 3, "orchestration-tools": 2},
    "by_risk": {"low-risk": 7, "medium-risk": 5, "high-risk": 1}
  }
}
```

### Output Schema 2: clustered_branches.json

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
      "branches": ["feature/auth-system"],
      "center": {
        "commit_history_weight": 0.749,
        "codebase_structure_weight": 0.794,
        "diff_distance_weight": 0.750,
        "combined_score": 0.764
      },
      "cohesion": 0.92,
      "silhouette_score": 0.68
    }
  ],
  "quality_metrics": {
    "silhouette_avg": 0.71,
    "davies_bouldin_index": 0.85,
    "calinski_harabasz_index": 15.3
  },
  "dendrogram_html": "path/to/dendrogram.html"
}
```

### Output Schema 3: enhanced_orchestration_branches.json

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
      "tags": ["orchestration-branch", "authentication"],
      "metrics": {},
      "execution_context": {
        "parallel_capability": true,
        "test_intensity": "high",
        "validation_suites": ["unit", "integration", "orchestration"]
      }
    }
  ],
  "orchestration_summary": {
    "total_branches": 24,
    "by_capability": {"parallelizable": 18, "serial": 6},
    "validation_distribution": {"high_intensity": 8, "medium_intensity": 12, "low_intensity": 4}
  }
}
```

---

## Implementation Guide

### Step 1: Pipeline Initialization

```python
class BranchClusteringPipeline:
    def __init__(self, repo_path: str, config: dict = None):
        self.repo_path = repo_path
        self.config = {**CONFIG_DEFAULTS, **(config or {})}
        self.logger = logging.getLogger(__name__)

        self.commit_analyzer = CommitHistoryAnalyzer(repo_path)
        self.structure_analyzer = CodebaseStructureAnalyzer(repo_path)
        self.diff_calculator = DiffDistanceCalculator(repo_path)
        self.clusterer = BranchClusterer(repo_path, self.config['clustering_threshold'])
        self.assigner = IntegrationTargetAssigner(repo_path)

        self._last_results = None
```

### Step 2: Parallel Analyzer Execution

```python
def _run_analyzers_parallel(self, branches: list) -> dict:
    results = {}
    with ThreadPoolExecutor(max_workers=self.config['max_workers']) as executor:
        futures = {}

        for branch in branches:
            futures[('commit', branch)] = executor.submit(
                self.commit_analyzer.analyze, branch
            )
            futures[('codebase', branch)] = executor.submit(
                self.structure_analyzer.analyze, branch
            )
            futures[('diff', branch)] = executor.submit(
                self.diff_calculator.analyze, branch
            )

        for (analyzer_type, branch), future in futures.items():
            if branch not in results:
                results[branch] = {}
            key_map = {'commit': 'commit_history', 'codebase': 'codebase_structure',
                       'diff': 'diff_distance'}
            results[branch][key_map[analyzer_type]] = future.result()

    return results
```

### Step 3: Main Pipeline Orchestration

```python
def run(self, branches: list = None, use_cache: bool = True) -> dict:
    self.logger.info(f"BranchClusteringPipeline initialized ({len(branches)} branches)")

    # Check cache
    cached, uncached = self._partition_cached(branches) if use_cache else ([], branches)
    self.logger.info(f"Using cache for {len(cached)} branches, analyzing {len(uncached)} new")

    # Run analyzers
    if self.config['use_parallel']:
        new_results = self._run_analyzers_parallel(uncached)
    else:
        new_results = self._run_analyzers_serial(uncached)

    # Merge with cached results
    all_results = {**self._load_cached(cached), **new_results}

    # Save to cache
    self._save_to_cache(new_results)

    # Cluster
    cluster_data = self.clusterer.cluster(all_results)
    self.logger.info(
        f"BranchClusterer: {len(branches)} branches → "
        f"{cluster_data['quality_metrics']['total_clusters']} clusters"
    )

    # Assign targets
    assignment_data = self.assigner.assign(cluster_data)
    self.logger.info(f"IntegrationTargetAssigner: {len(branches)} branches assigned")

    self._last_results = {
        "analyzer_outputs": all_results,
        "cluster_data": cluster_data,
        "assignment_data": assignment_data
    }

    return self._last_results
```

### Step 4: JSON Export

```python
def export_json_outputs(self, output_dir: str) -> dict:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    files = {}
    for name, data in [
        ("categorized_branches.json", self._build_categorized()),
        ("clustered_branches.json", self._build_clustered()),
        ("enhanced_orchestration_branches.json", self._build_orchestration())
    ]:
        path = output_path / name
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        files[name] = str(path)
        self.logger.info(f"Generated {name}")

    self.logger.info(f"Pipeline complete. Results saved to {output_dir}")
    return files
```

---

## Configuration & Defaults

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

### Cache File Structure

```
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
```

---

## Typical Development Workflow

1. **Day 1:** Pipeline skeleton, config loading, component instantiation (002.6.1)
2. **Day 2:** Serial execution pipeline with full data flow (002.6.2)
3. **Day 3:** Parallel execution with ThreadPoolExecutor (002.6.3)
4. **Day 4:** Caching layer with expiration and invalidation (002.6.4)
5. **Day 5-6:** JSON output generation for all three files (002.6.5)
6. **Day 6:** Utility methods, logging, progress reporting (002.6.6)
7. **Day 7:** Integration testing across all scenarios (002.6.7)

---

## Integration Handoff

### Downstream Integration Points

| Downstream Task | JSON File Consumed | Tags/Fields Used |
|-----------------|-------------------|------------------|
| **Task 79** (Execution Control) | enhanced_orchestration_branches.json | `parallel_capability`, `execution_context` |
| **Task 80** (Validation Intensity) | categorized_branches.json | `simple`/`moderate`/`complex` tags |
| **Task 83** (Test Suite Selection) | categorized_branches.json | `testing-required-high`/`medium`/`optional` tags |
| **Task 101** (Orchestration Filter) | enhanced_orchestration_branches.json | `orchestration-branch` tag filters |

### Logging Output Example

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

## Common Gotchas & Solutions

**Gotcha 1: ThreadPoolExecutor swallows exceptions**
```python
# WRONG: Exception in thread lost silently
future = executor.submit(analyzer.analyze, branch)
results[branch] = future.result()  # May raise, but only when .result() called

# RIGHT: Wrap with explicit error handling
try:
    results[branch] = future.result(timeout=60)
except Exception as e:
    self.logger.error(f"Analyzer failed for {branch}: {e}")
    raise
```

**Gotcha 2: Cache file naming with slashes**
```python
# WRONG: Branch name "feature/auth" creates nested directories
cache_path = cache_dir / f"{branch_name}_commit.json"  # Creates feature/ subdirectory

# RIGHT: Replace slashes with double underscores
safe_name = branch_name.replace("/", "__")
cache_path = cache_dir / f"{safe_name}_commit.json"
```

**Gotcha 3: Stale cache after branch force-push**
```python
# WRONG: Cache based only on branch name
if cache_file.exists():
    return load_cache(cache_file)

# RIGHT: Include branch HEAD SHA in cache key
branch_sha = get_branch_head_sha(branch)
cache_key = f"{safe_name}_{branch_sha[:8]}"
```

**Gotcha 4: JSON output not atomic**
```python
# WRONG: Partial write if interrupted
with open(output_path, 'w') as f:
    json.dump(data, f)

# RIGHT: Write to temp, then rename
tmp_path = output_path.with_suffix('.tmp')
with open(tmp_path, 'w') as f:
    json.dump(data, f, indent=2)
tmp_path.rename(output_path)
```

---

## Integration Checkpoint

**When pipeline is ready for downstream consumption:**

- [ ] All 7 sub-subtasks complete (002.6.1 through 002.6.7)
- [ ] All 5 test scenarios pass (fresh, incremental, single, large, cache refresh)
- [ ] Three JSON output files generated and schema-validated
- [ ] Parallel and serial execution produce identical results
- [ ] Caching works correctly (hit, miss, expiration, force refresh)
- [ ] Logging output matches expected format
- [ ] All downstream tasks (79, 80, 83, 101) can consume outputs
- [ ] Code review approved
- [ ] Commit message: `feat: complete Task 002.6 PipelineIntegration`

---

## Done Definition

Task 002.6 is done when:

1. All 7 sub-subtasks marked complete
2. Unit and integration tests pass (>95% coverage)
3. Code review approved
4. Three JSON files generated matching schemas exactly
5. Pipeline runs end-to-end without errors
6. Parallel execution verified equivalent to serial
7. Caching layer functional with proper invalidation
8. Logging provides clear execution visibility
9. Documentation complete (Google-style docstrings)
10. Commit: `feat: complete Task 002.6 PipelineIntegration`

---

## Provenance

- **Primary source:** HANDOFF_75.6_PipelineIntegration.md (archived in task_data/migration_backup_20260129/)
- **Task ID mapping:** Original Task 75.6 → Current Task 002.6
- **Structure standard:** TASK_STRUCTURE_STANDARD.md (14-section format, approved January 6, 2026)
- **Upstream dependencies:** Tasks 002.1, 002.2, 002.3, 002.4, 002.5
- **Downstream consumers:** Task 79 (Execution Control), Task 80 (Validation Intensity), Task 83 (Test Suite Selection), Task 101 (Orchestration Filter)

---

## Next Steps

1. **Immediate:** Begin with sub-subtask 002.6.1 (Design Pipeline Architecture and Execution Flow)
2. **Week 1:** Complete all 7 sub-subtasks with proper orchestration logic
3. **Week 1-2:** Implement parallel execution framework for Stage One analyzers
4. **Week 2:** Create caching layer with proper invalidation strategy
5. **Week 2:** Write comprehensive tests for all 7 pipeline scenarios
6. **Week 2-3:** Performance validation and optimization for large repositories
7. **Week 3:** Code review and documentation completion
8. **Upon completion:** Ready for hand-off to downstream tasks (79, 80, 83, 101)
9. **Parallel tasks:** Task 002.7 (VisualizationReporting), Task 002.8 (TestingSuite) can proceed in parallel
