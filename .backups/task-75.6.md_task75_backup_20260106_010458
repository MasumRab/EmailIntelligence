# Task 75.6: PipelineIntegration

## Purpose
Orchestrate all Stage One and Stage Two components into a production pipeline. This Stage Two task integrates analyzers, clustering, and assignment into a cohesive system with caching, performance optimization, and output generation.

**Scope:** BranchClusteringEngine orchestrator  
**Effort:** 20-28 hours | **Complexity:** 6/10  
**Status:** Ready when 75.1-75.5 complete  
**Blocks:** Tasks 75.7, 75.8

---

## Quick Navigation

Navigate this document using these links:

- [Purpose](#purpose)
- [Success Criteria](#success-criteria)
- [Output Files](#output-files)
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

## Success Criteria

Task 75.6 is complete when:

**Core Functionality:**
- [ ] `BranchClusteringEngine` orchestrates all prior tasks
- [ ] Executes 75.1, 75.2, 75.3 analyzers in parallel
- [ ] Feeds outputs to 75.4 (BranchClusterer)
- [ ] Feeds clustering to 75.5 (IntegrationTargetAssigner)
- [ ] Generates three JSON output files (specification format)
- [ ] Implements caching for performance optimization
- [ ] Output JSON files match schema exactly

**Performance Targets:**
- [ ] End-to-end pipeline: **< 120 seconds** for 13+ branches
- [ ] Analyzer execution (parallel): **< 30 seconds** each
- [ ] Clustering: **< 10 seconds**
- [ ] Assignment: **< 5 seconds**
- [ ] Output generation: **< 5 seconds**
- [ ] Cache hit rate: **> 70%** on second run
- [ ] Memory: **< 100 MB** peak usage

**Quality Assurance:**
- [ ] Unit tests pass (minimum 6 test cases with **>90% code coverage**) 
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <2 minutes for 13+ branches
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

**Integration Readiness:**
- [ ] Compatible with Task 75.7 (VisualizationReporting) input
- [ ] Compatible with Task 75.8 (TestingSuite) input
- [ ] Generates downstream-compatible output files
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Output Files

### 1. categorized_branches.json
Target assignments with tags and confidence scores

```json
{
  "branches": [
    {
      "branch_name": "orchestration-tools",
      "target_assignment": "main",
      "confidence_score": 0.95,
      "reasoning": "High stability, core framework changes",
      "tags": ["tag:main_branch", "tag:sequential_required", ...],
      "affinity_score": 0.87,
      "cluster_id": 1
    }
  ],
  "summary": {
    "total_branches": 13,
    "main_target_count": 4,
    "science_target_count": 5,
    "orchestration_target_count": 4
  }
}
```

### 2. clustered_branches.json
Cluster analysis with quality metrics

```json
{
  "clusters": [
    {
      "cluster_id": 0,
      "member_branches": ["branch1", "branch2", ...],
      "cluster_center": {...},
      "cluster_size": 4,
      "quality_metrics": {
        "silhouette_score": 0.65,
        "davies_bouldin_index": 1.2,
        "calinski_harabasz_score": 15.3
      }
    }
  ],
  "overall_quality": {
    "silhouette_score": 0.62,
    "davies_bouldin_index": 1.3,
    "calinski_harabasz_score": 14.8
  }
}
```

### 3. enhanced_orchestration_branches.json
Special handling for orchestration-tools branches

```json
{
  "orchestration_branches": [
    {
      "branch_name": "orchestration-tools",
      "classification": "core",
      "tags": ["tag:task_101_orchestration", ...],
      "integration_target": "main",
      "execution_strategy": "sequential_required"
    }
  ],
  "summary": {
    "total_orchestration_branches": 4,
    "core_branches": 2,
    "extension_branches": 2
  }
}
```

---

## Subtasks Overview

### Dependency Flow Diagram

```
75.6.1 (2-3h)         75.6.3 (3-4h)    75.6.5 (3-4h)
[Design]              [Caching]        [Performance]
    │                     │                 │
    ├─→ 75.6.2 (4-5h) ───┼─────┬───────────┘
    │   [Orchestration]   │     │
    │                     ├─→ 75.6.6 (2-3h) ──┐
    ├─→ 75.6.4 (3-4h) ───┤     │              ├─→ 75.6.8 (3-4h)
    │   [Output Gen]      │     │ [Error]      │  [Tests & Final]
    │                     │     │              │
    │                     ├─→ 75.6.7 (2-3h) ──┘
    │                     │     [Config]
    │                     │
    └─────────────────────┘

Critical Path: 75.6.1 → 75.6.2 → (75.6.4 + 75.6.3/5) → 75.6.6 → 75.6.8
Minimum Duration: 20-28 hours (with parallelization)
```

### Parallel Opportunities

**Can run in parallel (after 75.6.2):**
- 75.6.3: Caching strategy (3-4 hours)
- 75.6.5: Performance optimization (3-4 hours)

Both depend on orchestration core (75.6.2) but are independent. **Estimated parallel execution saves 3-4 hours.**

**Must be sequential:**
- 75.6.1 → 75.6.2 (design prerequisites)
- 75.6.2 → 75.6.4 (need orchestration for output)
- 75.6.2 → 75.6.3/5 (parallelizable optimization)
- 75.6.3/5 → 75.6.6 (caching/perf before error handling)
- 75.6.6 → 75.6.8 (need all components for testing)

### Timeline with Parallelization

**Days 1: Design (75.6.1)**
- Document end-to-end pipeline flow
- Design parallelization strategy
- Plan output specifications

**Days 1-2: Pipeline Orchestration (75.6.2)**
- Implement BranchClusteringEngine
- Execute analyzers, clustering, assignment
- Add progress tracking and logging

**Days 2-4: Parallel Implementation (75.6.3, 75.6.5)**
- **75.6.3 (Person A, Days 2-3):** File-based caching, invalidation, stats
- **75.6.5 (Person B, Days 2-4):** Profiling, parallelization, optimization
- Merge results at end of Day 3

**Days 3-5: Output & Integration (75.6.4, 75.6.6, 75.6.7)**
- Day 3: Generate three JSON output files
- Day 4: Comprehensive error handling and recovery
- Day 4: Configuration management (YAML)
- Day 5: Integration tests, coverage report

---
## Subtasks

### 75.6.1: Design Pipeline Architecture
**Purpose:** Design overall orchestration flow  
**Effort:** 2-3 hours

**Steps:**
1. Document end-to-end pipeline flow
2. Define dependency graph
3. Design parallelization strategy
4. Plan caching strategy
5. Define output specifications

**Success Criteria:**
- [ ] Pipeline flow clearly documented
- [ ] Dependencies identified
- [ ] Parallelization approach specified
- [ ] Caching strategy designed


### Implementation Checklist (From HANDOFF)
- [ ] Document end-to-end pipeline flow (analyzers → clustering → assignment)
- [ ] Identify all component dependencies
- [ ] Design parallelization strategy for Tasks 75.1-75.3
- [ ] Plan caching strategy (file-based, cache invalidation)
- [ ] Define output file specifications
---

### 75.6.2: Implement Pipeline Orchestration
**Purpose:** Create BranchClusteringEngine orchestrator  
**Effort:** 4-5 hours

**Steps:**
1. Create engine class with initialization
2. Implement sequential/parallel execution logic
3. Implement error handling and recovery
4. Add progress tracking/logging
5. Implement timeout handling

**Success Criteria:**
- [ ] Executes all components correctly
- [ ] Handles errors gracefully
- [ ] Provides useful progress feedback
- [ ] Completes within time limits


### Implementation Checklist (From HANDOFF)
- [ ] Create BranchClusteringEngine class with __init__ and run methods
- [ ] Implement sequential/parallel execution logic
- [ ] Add error handling and recovery mechanisms
- [ ] Implement progress tracking and logging
- [ ] Add timeout handling for long-running tasks
---

### 75.6.3: Implement Caching Strategy
**Purpose:** Optimize performance through caching  
**Effort:** 3-4 hours

**Steps:**
1. Design cache key strategy
2. Implement file-based caching
3. Add cache invalidation logic
4. Implement cache size limits
5. Add cache statistics tracking

**Success Criteria:**
- [ ] Caches analyzer outputs
- [ ] Invalidates when needed
- [ ] Respects size limits
- [ ] Provides cache hit statistics


### Implementation Checklist (From HANDOFF)
- [ ] Design cache key strategy (branch name + metric type)
- [ ] Implement file-based caching system
- [ ] Add cache invalidation logic (when to re-analyze)
- [ ] Implement cache size limits and cleanup
- [ ] Add cache statistics tracking
---

### 75.6.4: Implement Output Generation
**Purpose:** Generate three JSON output files  
**Effort:** 3-4 hours

**Steps:**
1. Implement categorized_branches.json generation
2. Implement clustered_branches.json generation
3. Implement enhanced_orchestration_branches.json generation
4. Add output validation
5. Add output formatting/prettification

**Success Criteria:**
- [ ] All three files generated correctly
- [ ] Files match JSON schema
- [ ] Output is valid JSON
- [ ] Formatting is consistent


### Implementation Checklist (From HANDOFF)
- [ ] Implement categorized_branches.json generation
- [ ] Implement clustered_branches.json generation
- [ ] Implement enhanced_orchestration_branches.json generation
- [ ] Add JSON schema validation
- [ ] Add output formatting (pretty-print, indentation)
---

### 75.6.5: Implement Performance Optimization
**Purpose:** Optimize for speed and resource usage  
**Effort:** 3-4 hours

**Steps:**
1. Profile execution to identify bottlenecks
2. Implement parallelization where possible
3. Optimize data structures
4. Implement streaming for large datasets
5. Monitor memory usage

**Success Criteria:**
- [ ] Meets <2 minute target for 13 branches
- [ ] Memory usage reasonable (<100MB)
- [ ] CPU usage efficient
- [ ] Parallelization working


### Implementation Checklist (From HANDOFF)
- [ ] Profile execution to identify bottlenecks
- [ ] Implement parallelization using ThreadPoolExecutor
- [ ] Optimize data structures (e.g., use sets vs lists)
- [ ] Implement streaming for large datasets
- [ ] Monitor memory usage during execution
---

### 75.6.6: Implement Error Handling & Recovery
**Purpose:** Ensure robust operation  
**Effort:** 2-3 hours

**Steps:**
1. Implement comprehensive error handling
2. Add logging at all stages
3. Implement retry logic for transient errors
4. Add graceful degradation
5. Document error codes and recovery

**Success Criteria:**
- [ ] All error paths handled
- [ ] Errors logged with context
- [ ] Graceful degradation working
- [ ] Recovery logic tested


### Implementation Checklist (From HANDOFF)
- [ ] Implement comprehensive error handling
- [ ] Add logging at all stages
- [ ] Implement retry logic for transient errors
- [ ] Add graceful degradation
- [ ] Document all error codes and recovery strategies
---

### 75.6.7: Implement Configuration Management
**Purpose:** Externalize all configuration  
**Effort:** 2-3 hours

**Steps:**
1. Define configuration schema
2. Implement config file loading
3. Implement config validation
4. Add defaults and overrides
5. Document all parameters

**Success Criteria:**
- [ ] All parameters configurable
- [ ] Config file format simple
- [ ] Validation working
- [ ] Documentation complete


### Implementation Checklist (From HANDOFF)
- [ ] Define configuration schema (YAML/JSON)
- [ ] Implement config file loading
- [ ] Implement config validation
- [ ] Add defaults and environment variable overrides
- [ ] Document all configuration parameters
---

### 75.6.8: Write Integration Tests
**Purpose:** Comprehensive integration testing  
**Effort:** 3-4 hours

**Steps:**
1. Create test fixtures with sample branches
2. Implement 6+ integration test cases
3. Test end-to-end pipeline
4. Test output file generation
5. Generate coverage report

**Success Criteria:**
- [ ] 6+ integration tests pass
- [ ] End-to-end flow verified
- [ ] Output files validated
- [ ] Coverage >90%


### Implementation Checklist (From HANDOFF)
- [ ] Create integration test fixtures
- [ ] Implement 6+ end-to-end tests
- [ ] Test output file generation and validation
- [ ] Test error recovery paths
- [ ] Generate coverage report


### Test Case Examples (From HANDOFF)

1. **test_pipeline_e2e_13_branches**: Full pipeline with 13 diverse branches
   - Expected: All outputs generated, no exceptions, <2 minutes

2. **test_json_outputs_generated**: Three JSON files created
   - Expected: categorized_branches.json, clustered_branches.json, enhanced_orchestration_branches.json

3. **test_caching_enabled**: Second run uses cache, faster execution
   - Expected: Second run completes faster than first

4. **test_caching_miss**: New branch added after first run
   - Expected: New branch analyzed, others from cache

5. **test_parallel_execution**: Analyzers run in parallel
   - Expected: Parallelization enabled, faster than sequential

6. **test_single_branch**: Pipeline with single branch input
   - Expected: Results generated correctly for 1 branch

7. **test_large_batch_50_branches**: Pipeline handles 50+ branches
   - Expected: Completes without error, within time limits

8. **test_json_schema_validation**: All JSON outputs conform to schema
    - Expected: Each JSON file validates successfully

### Test Cases: Execution Modes (Task 75.6 Enhancement)

9. **test_identification_mode_execution**: Identification mode with migration analysis
    - Setup: 5 branches with mixed backend/src imports
    - Execute: `engine = BranchClusteringEngine(mode="identification"); results = engine.execute(branches)`
    - Expected: Simple JSON output in <30s, includes migration tags, I2.T4 compatible format
    - Validation: Check output has branch, target, confidence, tags fields

10. **test_clustering_mode_execution**: Full clustering mode
    - Setup: 13 branches with varying similarities
    - Execute: `engine = BranchClusteringEngine(mode="clustering"); results = engine.execute(branches)`
    - Expected: Detailed JSON output with clusters and quality metrics, <120s
    - Validation: Verify clusters array, quality_metrics present

11. **test_hybrid_mode_with_clustering**: Hybrid mode includes clustering
    - Setup: 10 branches
    - Execute: `engine = BranchClusteringEngine(mode="hybrid", config={"enable_clustering_in_hybrid": true})`
    - Expected: Both simple and detailed outputs, <90s
    - Validation: Verify both output formats present

12. **test_hybrid_mode_without_clustering**: Hybrid mode identification only
    - Setup: 10 branches
    - Execute: `engine = BranchClusteringEngine(mode="hybrid", config={"enable_clustering_in_hybrid": false})`
    - Expected: Only simple identification output, <30s
    - Validation: Verify simple output only, no clustering data

13. **test_migration_analysis_detection**: Migration status detection
    - Setup: Branches with backend imports, src imports, both, or neither
    - Expected: Correct migration status tags assigned (tag:migration_required, tag:migration_in_progress, tag:migration_complete)
    - Validation: Verify status matches branch code structure

14. **test_simple_output_format**: Simple format (I2.T4 compatible)
    - Setup: Any branches
    - Execute: `OutputGenerator().generate_output(results, "simple")`
    - Expected: List of objects with branch, target, confidence, reasoning, tags
    - Validation: Each object has all required fields, valid types

15. **test_detailed_output_format**: Detailed format with metrics
    - Setup: Any branches  
    - Execute: `OutputGenerator().generate_output(results, "detailed")`
    - Expected: Dict with clusters, quality_metrics, branch_analysis
    - Validation: All metric fields present and numeric

16. **test_all_output_format**: Combined output format
    - Setup: Any branches
    - Execute: `OutputGenerator().generate_output(results, "all")`
    - Expected: Dict containing both "simple" and "detailed" keys
    - Validation: Both formats present and valid

17. **test_mode_validation_invalid**: Invalid mode rejected
    - Execute: `BranchClusteringEngine(mode="invalid")`
    - Expected: Raises ValueError with clear message
    - Validation: Error message mentions valid modes

18. **test_backward_compatibility_i2t4**: Identification mode matches I2.T4
    - Setup: Branches previously analyzed with I2.T4
    - Execute: Compare identification mode output with I2.T4 output
    - Expected: Simple JSON structure identical to I2.T4 format
    - Validation: No breaking changes to existing consumers

---

## Configuration & Defaults

All parameters should be externalized to configuration files (not hardcoded). Use YAML format:

```yaml
# config/branch_clustering_engine.yaml
branch_clustering_engine:
  # Parallelization
  enable_parallelization: true  # Run analyzers in parallel
  num_parallel_workers: 3  # Number of threads
  execution_timeout_seconds: 300  # 5 minutes max
  
  # Caching
  enable_caching: true  # Cache analyzer outputs
  cache_dir: "./cache"  # Cache location
  cache_max_size_mb: 500  # Maximum cache size
  cache_invalidation_hours: 24  # Refresh cache daily
  
  # Output
  output_dir: "./output"  # Output JSON directory
  pretty_print_json: true  # Formatted output
  
  # Components (nested configs)
  commit_history_analyzer:
    lookback_days: 30
    max_commits: 1000
  
  codebase_structure_analyzer:
    include_extensions: [.py, .js, .ts, .java]
    exclude_patterns: ["__pycache__", "node_modules"]
  
  branch_clusterer:
    linkage_method: "ward"
    clustering_threshold: 0.5
  
  integration_target_assigner:
    level1_merge_readiness_threshold: 0.9
    level2_affinity_threshold: 0.70
```

**How to use in code:**
```python
import yaml

def load_config(config_path='config/branch_clustering_engine.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)['branch_clustering_engine']

config = load_config()
ENABLE_PARALLELIZATION = config['enable_parallelization']
NUM_WORKERS = config['num_parallel_workers']
CACHE_DIR = config['cache_dir']
# ... etc
```

**Why externalize?**
- Tune performance without recompiling
- Different configs for dev/test/prod environments
- Enable/disable features on-the-fly
- Adjust timeouts based on infrastructure
- Easy switching between caching strategies

---

## Configuration: Execution Modes (Task 75.6 Enhancement)

Three execution modes are supported for different analysis workflows:

```yaml
# Add to config/branch_clustering_engine.yaml
execution:
  mode: clustering                      # identification | clustering | hybrid
  enable_migration_analysis: true
  enable_clustering_in_hybrid: true
  output_format: detailed               # simple | detailed | all
```

### Mode: identification
- **Purpose:** Simple, fast branch categorization (I2.T4 compatible)
- **Performance:** <30 seconds for 13 branches
- **Memory:** <50MB
- **Output:** Simple JSON with branch, target, confidence, tags
- **Use case:** Quick categorization when detailed analysis not needed

**Configuration:**
```yaml
execution:
  mode: identification
  enable_migration_analysis: true
  output_format: simple
```

**Usage:**
```python
from task_data.branch_clustering_implementation import BranchClusteringEngine

engine = BranchClusteringEngine(mode="identification")
results = engine.execute(branches)
# Returns: [{"branch": "...", "target": "...", "confidence": 0.95, ...}]
```

### Mode: clustering
- **Purpose:** Full analysis with hierarchical agglomerative clustering
- **Performance:** <120 seconds for 13 branches
- **Memory:** <100MB
- **Output:** Detailed JSON with clustering metrics and quality scores
- **Use case:** Deep similarity analysis, cluster understanding

**Configuration:**
```yaml
execution:
  mode: clustering
  enable_migration_analysis: true
  output_format: detailed
```

**Usage:**
```python
from task_data.branch_clustering_implementation import BranchClusteringEngine

engine = BranchClusteringEngine(mode="clustering")
results = engine.execute(branches)
# Returns: {"clusters": [...], "quality_metrics": {...}}
```

### Mode: hybrid
- **Purpose:** Combined simple + clustering analysis
- **Performance:** <90 seconds for 13 branches
- **Memory:** <75MB
- **Output:** Both simple and detailed JSON formats
- **Use case:** Comprehensive analysis when all perspectives needed

**Configuration:**
```yaml
execution:
  mode: hybrid
  enable_migration_analysis: true
  enable_clustering_in_hybrid: true
  output_format: all
```

**Usage:**
```python
from task_data.branch_clustering_implementation import BranchClusteringEngine

engine = BranchClusteringEngine(mode="hybrid")
results = engine.execute(branches)
# Returns: {"simple": [...], "detailed": {...}}
```

### Migration Analysis (All Modes)

Migration analysis detects backend → src migration patterns automatically in all modes:

- `tag:migration_required` - Has backend imports only
- `tag:migration_in_progress` - Has both backend and src imports
- `tag:migration_complete` - Has src imports only

Disable with:
```yaml
execution:
  enable_migration_analysis: false
```

### Clustering in Hybrid Mode

Control whether hybrid mode includes clustering:

```yaml
execution:
  mode: hybrid
  enable_clustering_in_hybrid: true   # Include full clustering
  # OR
  enable_clustering_in_hybrid: false  # Identification only
```

---

## Typical Development Workflow

Complete git workflow for implementing Task 75.6:

```bash
# Setup
git checkout -b feat/branch-clustering-engine
mkdir -p src/engine tests/engine

# Main orchestrator (all major subtasks integrated)
cat > src/engine/engine.py << 'EOF'
from concurrent.futures import ThreadPoolExecutor
from src.analyzers.commit import CommitHistoryAnalyzer
from src.clustering.clusterer import BranchClusterer
from src.assignment.assigner import IntegrationTargetAssigner
import json

class BranchClusteringEngine:
    def __init__(self, repo_path, config):
        self.repo_path = repo_path
        self.config = config
    
    def run(self, branches):
        """Execute full pipeline with parallelization."""
        # Parallel analyzer execution (75.6.2)
        with ThreadPoolExecutor(max_workers=3) as executor:
            commit_f = executor.submit(CommitHistoryAnalyzer(...).analyze)
            structure_f = executor.submit(CodebaseStructureAnalyzer(...).analyze)
            diff_f = executor.submit(DiffDistanceCalculator(...).analyze)
            
            outputs = {
                'commit': commit_f.result(timeout=300),
                'structure': structure_f.result(timeout=300),
                'diff': diff_f.result(timeout=300)
            }
        
        # Clustering (75.6.3 via 75.4)
        clusterer = BranchClusterer(self.config)
        clusters = clusterer.cluster(outputs)
        
        # Assignment (75.6.4 via 75.5)
        assigner = IntegrationTargetAssigner(self.config)
        assignments = assigner.assign(clusters)
        
        # Generate outputs (75.6.5)
        self._generate_json_outputs(clusters, assignments)
        return assignments

git add src/engine/engine.py
git commit -m "feat: implement BranchClusteringEngine orchestrator (75.6)"
git push origin feat/branch-clustering-engine
```

---

## Integration Handoff

**Task 75.6 Outputs (3 JSON files):**

```
categorized_branches.json  <- contains branch assignments & tags
clustered_branches.json    <- contains cluster analysis & metrics
enhanced_orchestration_branches.json <- special orchestration handling
```

**Task 75.7 (Visualization) consumes:** All 3 JSON files for dashboard
**Task 75.8 (Testing) consumes:** All 3 JSON files for test validation

Validation:
```bash
python -c "
import json
files = ['categorized_branches.json', 'clustered_branches.json', 'enhanced_orchestration_branches.json']
for f in files:
    data = json.load(open(f))
    assert 'clusters' in data or 'branches' in data
    print(f'✓ {f} valid')
"
```

---

## Common Gotchas & Solutions

### Gotcha 1: Parallelization Causes Race Conditions ⚠️

**Problem:** ThreadPoolExecutor results arrive out of order
**Symptom:** Output dependencies violated
**Solution:** Use futures with explicit ordering

```python
results = {
    'commit': commit_future.result(timeout=300),
    'structure': structure_future.result(timeout=300),
    'diff': diff_future.result(timeout=300)
}
```

### Gotcha 2: Cache Invalidation Failure ⚠️

**Problem:** Stale cache causes incorrect analysis
**Symptom:** Second run produces same results despite branch changes
**Solution:** Hash-based cache keys

```python
import hashlib
key = hashlib.sha256(f"{branch_name}:{hash(metrics)}".encode()).hexdigest()
```

### Gotcha 3: Output JSON Schema Mismatch ⚠️

**Problem:** Generated JSON doesn't validate against schema
**Symptom:** Downstream tasks fail to parse output
**Solution:** Validate before writing

```python
import jsonschema
jsonschema.validate(output_dict, SCHEMA)
with open('output.json', 'w') as f:
    json.dump(output_dict, f)
```

### Gotcha 4: Memory Explosion with Caching ⚠️

**Problem:** Cache grows unbounded
**Symptom:** Out of memory after 100+ branches
**Solution:** Implement LRU eviction

```python
from functools import lru_cache
@lru_cache(maxsize=500)
def cached_analyze(branch_name):
    return expensive_analysis(branch_name)
```

### Gotcha 5: Analyzer Timeout Cascades ⚠️

**Problem:** One slow analyzer blocks entire pipeline
**Symptom:** Pipeline timeout even though one analyzer is fast
**Solution:** Independent timeout per analyzer

```python
for name, future in futures.items():
    try:
        result = future.result(timeout=30)
    except TimeoutError:
        logger.error(f"{name} timeout - using cached")
        result = fallback_cache.get(name)
```

---

## Technical Reference (From HANDOFF)

### Execution Flow Diagram
```
Input: List of branches
  ↓
┌─────────────────────────────────────┐
│ Parallelize (if enabled):           │
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

### Cache Strategy
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

### Performance Targets
- **Commit Analyzer:** <30 seconds
- **Structure Analyzer:** <30 seconds
- **Diff Calculator:** <45 seconds
- **Clustering:** <10 seconds
- **Assignment:** <5 seconds
- **End-to-end Pipeline:** <120 seconds (2 minutes) for 13+ branches

### Dependencies & Integration
- **Blocked by:** Tasks 75.1-75.5 (all must complete first)
- **Feeds into:** Task 75.7 (Visualization & Reporting), Task 75.8 (Testing), Task 75.9 (Framework Integration)
- **External libraries:** concurrent.futures, json, logging, pathlib

---

## Integration Checkpoint

**When to move to 75.7 & 75.8:**
- [ ] All 8 subtasks complete
- [ ] Integration tests passing (>90% coverage)
- [ ] Accepts outputs from Tasks 75.1-75.5
- [ ] Generates all three JSON files
- [ ] Output files match specification
- [ ] Performance meets targets (<2 minutes)
- [ ] Ready for visualization and testing

---

## Performance Targets

- **End-to-end execution:** <2 minutes for 13+ branches
- **Analyzer execution:** <30 seconds each (parallel)
- **Clustering:** <10 seconds
- **Assignment:** <5 seconds
- **Output generation:** <5 seconds
- **Memory usage:** <100MB peak

---

## Done Definition

Task 75.6 is done when:
1. All 8 subtasks marked complete
2. Integration tests pass (>90% coverage)
3. End-to-end pipeline working
4. All output files generated correctly
5. Performance targets met
6. Ready for visualization (75.7) and testing (75.8)

---

## Quick Usage Examples (Task 75.6 Enhancement)

### Example 1: Identification Mode (Quick Analysis)

```python
from task_data.branch_clustering_implementation import BranchClusteringEngine

# Create engine in identification mode
engine = BranchClusteringEngine(mode="identification")

# Analyze branches
branches = ["feature-auth", "feature-db-refactor", "feature-api-docs"]
results = engine.execute(branches)

# Results: List of simple assignments
for result in results:
    print(f"{result['branch']} → {result['target']} (confidence: {result['confidence']:.2f})")
    print(f"  Tags: {', '.join(result['tags'][:3])}...")

# Output:
# feature-auth → main (confidence: 0.95)
#   Tags: tag:core_changes, tag:sequential_required, tag:migration_complete...
# feature-db-refactor → scientific (confidence: 0.88)
#   Tags: tag:data_changes, tag:migration_in_progress, tag:complex...
# feature-api-docs → main (confidence: 0.92)
#   Tags: tag:documentation, tag:low_risk, tag:simple...
```

### Example 2: Clustering Mode (Deep Analysis)

```python
from task_data.branch_clustering_implementation import BranchClusteringEngine
import json

# Create engine in clustering mode
engine = BranchClusteringEngine(mode="clustering")

# Analyze branches
branches = [
    "feature-auth", "feature-auth-v2", "feature-db-refactor",
    "feature-api-v1", "feature-api-v2", "bugfix-security"
]
results = engine.execute(branches)

# Results: Dict with clusters and quality metrics
print(f"Clusters found: {len(results['clusters'])}")
for cluster in results['clusters']:
    print(f"\nCluster {cluster['cluster_id']}:")
    print(f"  Members: {', '.join(cluster['member_branches'][:3])}")
    print(f"  Silhouette score: {cluster['quality_metrics']['silhouette_score']:.3f}")

# Output:
# Clusters found: 2
# Cluster 0:
#   Members: feature-auth, feature-auth-v2, bugfix-security
#   Silhouette score: 0.742
# Cluster 1:
#   Members: feature-db-refactor, feature-api-v1, feature-api-v2
#   Silhouette score: 0.638
```

### Example 3: Hybrid Mode (Complete Analysis)

```python
from task_data.branch_clustering_implementation import BranchClusteringEngine

# Create engine in hybrid mode
engine = BranchClusteringEngine(
    mode="hybrid",
    config={
        "enable_clustering_in_hybrid": True,
        "enable_migration_analysis": True
    }
)

# Analyze branches
branches = ["feature-auth", "feature-db", "feature-api"]
results = engine.execute(branches)

# Results: Both simple and detailed outputs
print("Simple assignments:")
for branch_result in results['simple']:
    print(f"  {branch_result['branch']} → {branch_result['target']}")

print("\nCluster analysis:")
print(f"  Found {len(results['detailed']['clusters'])} cluster(s)")
print(f"  Overall silhouette: {results['detailed']['overall_quality']['silhouette_score']:.3f}")

# Output:
# Simple assignments:
#   feature-auth → main
#   feature-db → scientific
#   feature-api → main
# 
# Cluster analysis:
#   Found 2 cluster(s)
#   Overall silhouette: 0.65
```

### Example 4: Migration Analysis

```python
from task_data.branch_clustering_implementation import BranchClusteringEngine

# Create engine with migration analysis enabled
engine = BranchClusteringEngine(
    mode="identification",
    config={"enable_migration_analysis": True}
)

# Analyze branches that have backend→src migration
branches = [
    "feature-backend-to-src",  # Has both backend and src imports
    "feature-src-only",         # Has only src imports
    "feature-backend-only"      # Has only backend imports
]
results = engine.execute(branches)

# Check migration tags
for result in results:
    migration_tags = [tag for tag in result['tags'] if 'migration' in tag]
    print(f"{result['branch']}: {migration_tags}")

# Output:
# feature-backend-to-src: ['tag:migration_in_progress']
# feature-src-only: ['tag:migration_complete']
# feature-backend-only: ['tag:migration_required']
```

### Example 5: Custom Configuration

```python
from task_data.branch_clustering_implementation import BranchClusteringEngine
import yaml

# Load custom configuration
with open('config/branch_clustering_engine.yaml', 'r') as f:
    config = yaml.safe_load(f)['branch_clustering_engine']

# Create engine with custom config
engine = BranchClusteringEngine(
    repo_path="/path/to/repo",
    mode="clustering",
    config=config
)

# Use custom parallelization settings
branches = list(range(50))  # 50 branches
results = engine.execute(branches, primary_branch="origin/main")

print(f"Analysis completed: {len(results)} branches processed")
print(f"Cache hit rate: {cache_stats['hit_rate']:.1%}")
```

### Example 6: Integration with Downstream Tasks

```python
from task_data.branch_clustering_implementation import BranchClusteringEngine
import json

# Run full pipeline
engine = BranchClusteringEngine(mode="clustering")
results = engine.execute(branches)

# Task 75.7 (Visualization) consumes outputs
with open('output/categorized_branches.json', 'w') as f:
    json.dump({
        'branches': results['categorized'],
        'summary': results['summary']
    }, f)

# Task 75.8 (Testing) consumes outputs
with open('output/clustered_branches.json', 'w') as f:
    json.dump({
        'clusters': results['clusters'],
        'overall_quality': results['overall_quality']
    }, f)

# Task 75.9 (Framework Integration) uses outputs
with open('output/enhanced_orchestration_branches.json', 'w') as f:
    json.dump({
        'orchestration_branches': results['orchestration_branches'],
        'summary': results['orchestration_summary']
    }, f)

print("✓ Output files generated for downstream tasks")
```
