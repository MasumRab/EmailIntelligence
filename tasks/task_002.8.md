# Task 002.8: TestingSuite

**Status:** Ready for Implementation
**Priority:** High
**Effort:** 24-32 hours
**Complexity:** 6/10
**Dependencies:** 002.1, 002.2, 002.3, 002.4, 002.5, 002.6

---

## Overview/Purpose

Implement a comprehensive test suite covering unit tests for all Task 002 components (002.1-002.5), integration tests for the full pipeline (002.6), output validation tests, edge case tests, and performance/stress tests. This is a Stage Three component that validates the entire branch clustering system before framework integration.

**Scope:** All test files, fixtures, conftest.py, and pytest configuration
**Target:** >90% code coverage, all integration tests passing

---

## Success Criteria

Task 002.8 is complete when:

### Core Functionality
- [ ] Unit test files exist for all 5 analyzers: `test_commit_history_analyzer.py`, `test_codebase_structure_analyzer.py`, `test_diff_distance_calculator.py`, `test_branch_clusterer.py`, `test_integration_target_assigner.py`
- [ ] Integration test files exist: `test_full_pipeline.py`, `test_pipeline_caching.py`, `test_json_outputs.py`
- [ ] All test case function signatures from specification implemented
- [ ] CommitHistoryAnalyzer: 12 test cases pass
- [ ] CodebaseStructureAnalyzer: 12 test cases pass
- [ ] DiffDistanceCalculator: 12 test cases pass (including binary file and deletion handling)
- [ ] BranchClusterer: 12 test cases pass (metric combination, distance matrix, HAC, silhouette, Davies-Bouldin, Calinski-Harabasz, cohesion, outlier)
- [ ] IntegrationTargetAssigner: 12 test cases pass (heuristic rules, affinity scoring, consensus, tags, 30+ tags)
- [ ] Full Pipeline: 10 integration tests pass
- [ ] Output Validation: 6 tests pass (schema, NaN check, field presence, consistency)
- [ ] Edge Cases: 5 tests pass (empty repo, invalid names, large commits, binary-only, deleted branch)
- [ ] Performance: 3 tests pass (100-branch throughput, 50-branch memory, cache growth)

### Quality Assurance
- [ ] >90% code coverage on all components
- [ ] pytest.ini configured with coverage reporting
- [ ] conftest.py provides shared fixtures (sample_repo, analyzer_outputs, pipeline_results)
- [ ] Tests run in CI/CD pipeline
- [ ] All test output clear and actionable
- [ ] No flaky tests

### Integration Readiness
- [ ] Test fixtures compatible with all component interfaces
- [ ] Pipeline downstream compatibility test validates Tasks 79, 80, 83, 101 tag usage
- [ ] Test execution commands documented

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 002.1 (CommitHistoryAnalyzer) complete
- [ ] Task 002.2 (CodebaseStructureAnalyzer) complete
- [ ] Task 002.3 (DiffDistanceCalculator) complete
- [ ] Task 002.4 (BranchClusterer) complete
- [ ] Task 002.5 (IntegrationTargetAssigner) complete
- [ ] Task 002.6 (BranchClusteringPipeline) complete
- [ ] pytest, pytest-cov, pytest-xdist installed

### Blocks (What This Task Unblocks)
- Task 002.9 (FrameworkIntegration) — tests must pass before final integration

### External Dependencies
- `pytest` >= 6.0 (test framework)
- `pytest-cov` (coverage reporting)
- `pytest-xdist` (parallel test execution)

---

## Sub-subtasks Breakdown

### 002.8.1: Test Infrastructure Setup
**Effort:** 3-4 hours
**Depends on:** None

**Steps:**
1. Create test directory structure: `tests/unit/`, `tests/integration/`, `tests/fixtures/`
2. Create `conftest.py` with shared fixtures
3. Create `pytest.ini` with configuration
4. Create mock git repo fixture in `tests/fixtures/sample_repo/`
5. Create expected output fixtures in `tests/fixtures/analyzer_outputs/` and `tests/fixtures/pipeline_results/`

**Success Criteria:**
- [ ] `pytest tests/` runs without import errors
- [ ] All fixtures accessible from test files
- [ ] Coverage reporting configured

---

### 002.8.2: CommitHistoryAnalyzer Unit Tests (12 tests)
**Effort:** 3-4 hours
**Depends on:** 002.8.1

**Test Functions:**
1. `test_commit_recency_metric()` — recent commits score > 0.8
2. `test_commit_frequency_velocity()` — 50 commits/10 days scores > 0.7
3. `test_authorship_diversity()` — 5 unique authors scores > 0.7
4. `test_merge_readiness_recent()` — recently synced scores > 0.85
5. `test_merge_readiness_stale()` — 50+ commits behind scores < 0.4
6. `test_stability_score_calculation()` — low churn scores > 0.7
7. `test_nonexistent_branch_raises_error()` — BranchNotFoundError raised
8. `test_new_branch_handling()` — 1-commit branch, all metrics in [0,1]
9. `test_stale_branch_handling()` — 120-day old branch, recency < 0.2
10. `test_aggregate_score_normalization()` — 0 <= aggregate <= 1 for all
11. `test_output_schema_validation()` — all required fields present
12. `test_metrics_aggregation_weights()` — aggregate matches weighted sum (0.25/0.20/0.20/0.20/0.15)

---

### 002.8.3: CodebaseStructureAnalyzer Unit Tests (12 tests)
**Effort:** 3-4 hours
**Depends on:** 002.8.1

**Test Functions:**
1. `test_directory_similarity_identical()` — same tree scores 1.0
2. `test_directory_similarity_partial()` — 1 added dir in 10 scores 0.7-0.95
3. `test_file_additions_minimal()` — 2/100 new files scores > 0.8
4. `test_file_additions_many()` — 50/100 new files scores < 0.5
5. `test_core_module_stability_preserved()` — no core changes scores 1.0
6. `test_core_module_stability_modified()` — 5 src/ files modified scores 0.7-0.9
7. `test_core_module_stability_deleted()` — core deletions scores < 0.5
8. `test_namespace_isolation_clustered()` — 10 files in 1 dir scores > 0.7
9. `test_namespace_isolation_scattered()` — 10 files in 10 dirs scores < 0.5
10. `test_empty_branch_handling()` — identical to main, all metrics high
11. `test_aggregate_score_range()` — 0 <= aggregate <= 1
12. `test_output_schema_validation()` — all required fields present

---

### 002.8.4: DiffDistanceCalculator Unit Tests (12 tests)
**Effort:** 3-4 hours
**Depends on:** 002.8.1

**Test Functions:**
1. `test_code_churn_minimal()` — 50/5000 lines scores > 0.9
2. `test_code_churn_high()` — 2000/5000 lines scores < 0.4
3. `test_change_concentration_low()` — 50 files changed scores < 0.5
4. `test_change_concentration_high()` — 2 files changed scores > 0.9
5. `test_diff_complexity_concentrated()` — 500 lines in 1 file scores > 0.7
6. `test_diff_complexity_distributed()` — 10 lines each in 20 files scores < 0.5
7. `test_integration_risk_risky_files()` — config changes scores < 0.6
8. `test_integration_risk_safe_files()` — docs-only changes scores > 0.8
9. `test_binary_files_ignored()` — binary files don't affect line counts
10. `test_deleted_files_handling()` — deletions counted (total_lines_deleted == 100)
11. `test_empty_diff_handling()` — no changes, metrics ~0.5 or high
12. `test_aggregate_score_range()` — 0 <= aggregate <= 1

---

### 002.8.5: BranchClusterer Unit Tests (12 tests)
**Effort:** 3-4 hours
**Depends on:** 002.8.1

**Test Functions:**
1. `test_clustering_metric_combination()` — weights 35/35/30 produce correct combined_score
2. `test_distance_matrix_calculation()` — distance[i,j] = 1 - similarity for 3 branches
3. `test_hierarchical_clustering_convergence()` — 10 branches, linkage_matrix shape (9, 4)
4. `test_dendrogram_cut_threshold()` — threshold=0.5 produces correct cluster assignments
5. `test_single_cluster_all_similar()` — 5 identical branches, all in cluster 0
6. `test_multiple_clusters_different()` — 10 varying branches, >1 cluster formed
7. `test_silhouette_score_calculation()` — scores in [-1, 1] range
8. `test_davies_bouldin_index_computation()` — index >= 0
9. `test_calinski_harabasz_index_computation()` — index >= 0
10. `test_cluster_cohesion_calculation()` — similar branches, cohesion > 0.8
11. `test_output_schema_validation()` — all required fields present
12. `test_outlier_handling()` — 1 outlier + 9 similar, outlier in separate cluster

---

### 002.8.6: IntegrationTargetAssigner Unit Tests (12 tests)
**Effort:** 3-4 hours
**Depends on:** 002.8.1

**Test Functions:**
1. `test_heuristic_rule_high_merge_readiness()` — merge_readiness > 0.9 → main, confidence > 0.95
2. `test_heuristic_rule_science_branch_name()` — "science" in name → scientific target
3. `test_heuristic_rule_orchestration_branch_name()` — "orchestration" in name → orchestration-tools
4. `test_affinity_scoring_main_archetype()` — main-like metrics → main, confidence > 0.70
5. `test_affinity_scoring_scientific_archetype()` — science-like metrics → scientific, confidence > 0.70
6. `test_cluster_consensus_majority()` — 7/10 in main → target=main, confidence=cohesion*0.7
7. `test_default_to_main_fallback()` — ambiguous metrics → main, confidence=0.65
8. `test_tag_generation_core_feature()` — codebase_structure > 0.85 → "core-feature" tag
9. `test_tag_generation_risk_low()` — integration_risk > 0.75 → "low-risk" tag
10. `test_tag_generation_risk_high()` — integration_risk < 0.5 → "high-risk" tag
11. `test_tag_generation_complexity_simple()` — all metrics > 0.8 → "simple" tag
12. `test_tag_generation_30_plus_tags()` — representative branch generates >= 30 tags

---

### 002.8.7: Full Pipeline Integration Tests (10 tests)
**Effort:** 4-5 hours
**Depends on:** 002.8.1

**Test Functions:**
1. `test_pipeline_e2e_13_branches()` — all outputs generated, no exceptions
2. `test_pipeline_json_outputs_generated()` — 3 files: categorized_branches.json, clustered_branches.json, enhanced_orchestration_branches.json
3. `test_pipeline_caching_enabled()` — second run faster than first
4. `test_pipeline_caching_miss()` — new branch re-analyzed, others cached
5. `test_pipeline_parallel_execution()` — use_parallel=True, time < sequential
6. `test_pipeline_single_branch()` — single branch input produces results
7. `test_pipeline_large_batch_50_branches()` — 50 branches complete without error
8. `test_pipeline_json_schema_validation()` — all JSON files validate against schema
9. `test_pipeline_consistency_across_runs()` — same input → same output
10. `test_pipeline_downstream_compatibility()` — tags valid for Tasks 79, 80, 83, 101

---

### 002.8.8: Output Validation, Edge Case, and Performance Tests
**Effort:** 3-4 hours
**Depends on:** 002.8.1

**Output Validation (6 tests):**
1. `test_categorized_branches_schema()` — required fields, types, ranges
2. `test_clustered_branches_schema()` — cluster assignments, quality metrics
3. `test_enhanced_orchestration_schema()` — orchestration-specific fields
4. `test_json_no_nan_values()` — no NaN or Inf in JSON
5. `test_json_no_missing_required_fields()` — all required fields present
6. `test_json_consistent_branch_listing()` — same branches across all JSON files

**Edge Cases (5 tests):**
7. `test_empty_repository()` — no branches → empty results or clear error
8. `test_invalid_branch_names()` — special characters handled
9. `test_very_large_single_commit()` — 10000+ lines, no overflow
10. `test_binary_only_branch()` — binary-only changes, metrics computed
11. `test_deleted_branch_handling()` — clear error message

**Performance (3 tests):**
12. `test_performance_100_branches()` — completes < 10 minutes (600s)
13. `test_memory_usage_50_branches()` — peak memory < 1 GB
14. `test_cache_file_sizes()` — 10 runs, cache_dir < 100 MB

---

## Specification Details

### Test File Structure

```
tests/
├── unit/
│   ├── test_commit_history_analyzer.py      # 12 tests (Task 002.1)
│   ├── test_codebase_structure_analyzer.py   # 12 tests (Task 002.2)
│   ├── test_diff_distance_calculator.py      # 12 tests (Task 002.3)
│   ├── test_branch_clusterer.py              # 12 tests (Task 002.4)
│   └── test_integration_target_assigner.py   # 12 tests (Task 002.5)
├── integration/
│   ├── test_full_pipeline.py                 # 10 tests (Task 002.6)
│   ├── test_pipeline_caching.py              # Caching-specific tests
│   └── test_json_outputs.py                  # Output validation + edge cases
├── fixtures/
│   ├── sample_repo/                          # Mock git repo for testing
│   ├── analyzer_outputs/                     # Expected outputs from each analyzer
│   └── pipeline_results/                     # Expected pipeline results
└── conftest.py                               # Pytest fixtures and shared setup
```

### pytest.ini Configuration

```ini
[pytest]
minversion = 6.0
addopts = -v --tb=short --cov=clustering --cov-report=html
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### conftest.py Fixtures

```python
import pytest

@pytest.fixture(scope="session")
def sample_repo(tmp_path_factory):
    """Create mock git repo with diverse branches for testing."""
    repo_dir = tmp_path_factory.mktemp("sample_repo")
    # Initialize git repo, create branches with known characteristics
    return str(repo_dir)

@pytest.fixture
def analyzer_outputs():
    """Sample outputs from Tasks 002.1-002.3 for unit testing."""
    return {
        "commit_history": { ... },
        "codebase_structure": { ... },
        "diff_distance": { ... }
    }

@pytest.fixture
def pipeline_results():
    """Sample results from Task 002.6 for integration testing."""
    return {
        "categorized_branches": [ ... ],
        "clustered_branches": [ ... ],
        "quality_metrics": { ... },
        "linkage_matrix": [ ... ]
    }
```

### Test Execution Commands

```bash
# Run all tests
pytest tests/

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Run with coverage report
pytest --cov=clustering tests/

# Run specific test file
pytest tests/unit/test_commit_history_analyzer.py

# Run specific test function
pytest tests/unit/test_commit_history_analyzer.py::test_commit_recency_metric

# Run in parallel (requires pytest-xdist)
pytest -n auto tests/

# Run with verbose output and short tracebacks
pytest -v --tb=short tests/
```

---

## Implementation Guide

### Step 1: Create Directory Structure
```bash
mkdir -p tests/unit tests/integration tests/fixtures/sample_repo
mkdir -p tests/fixtures/analyzer_outputs tests/fixtures/pipeline_results
touch tests/__init__.py tests/unit/__init__.py tests/integration/__init__.py
```

### Step 2: Build conftest.py First
Build the `sample_repo` fixture that creates a mock git repository with:
- 13 branches with varying characteristics (recent, stale, single-commit, multi-author)
- Known commit histories for deterministic test assertions
- File structures matching real repo patterns

### Step 3: Implement Unit Tests by Component
For each analyzer, follow the pattern:
```python
class TestCommitHistoryAnalyzer:
    def test_commit_recency_metric(self, sample_repo):
        analyzer = CommitHistoryAnalyzer(sample_repo)
        result = analyzer.analyze("feature/recent")
        assert result['metrics']['commit_recency'] > 0.8
```

### Step 4: Implement Integration Tests
Use the full pipeline with sample_repo fixture:
```python
def test_pipeline_e2e_13_branches(sample_repo):
    pipeline = BranchClusteringPipeline(sample_repo)
    results = pipeline.run()
    assert len(results['categorized_branches']) == 13
    assert results['quality_metrics'] is not None
```

### Step 5: Add Performance Tests with Markers
```python
@pytest.mark.slow
def test_performance_100_branches(sample_repo):
    import time
    start = time.time()
    # Generate 100 test branches and run pipeline
    elapsed = time.time() - start
    assert elapsed < 600
```

---

## Configuration & Defaults

```ini
# pytest.ini
[pytest]
minversion = 6.0
addopts = -v --tb=short --cov=clustering --cov-report=html
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks integration tests
```

Coverage thresholds:
- Overall: >90%
- Per-component: >85%
- Critical paths (pipeline, assignment): >95%

---

## Typical Development Workflow

1. Set up test directory structure and conftest.py
2. Write CommitHistoryAnalyzer tests first (most straightforward)
3. Write CodebaseStructureAnalyzer and DiffDistanceCalculator tests in parallel
4. Write BranchClusterer tests (depends on understanding metric combination)
5. Write IntegrationTargetAssigner tests (most complex — heuristic rules, affinity, consensus, tags)
6. Write full pipeline integration tests
7. Write output validation tests (JSON schema, data integrity)
8. Write edge case tests (empty repo, invalid names, large commits)
9. Write performance tests last (need all components working)
10. Run full suite with coverage, iterate until >90%
11. Fix any flaky tests
12. Generate final coverage report

---

## Integration Handoff

### For Task 002.9 (FrameworkIntegration)
- All tests must pass before framework integration begins
- Coverage report demonstrates system reliability
- Integration tests validate downstream compatibility with Tasks 79, 80, 83, 101
- Test fixtures serve as documentation of expected component behavior

### Test Fixture Reuse
- `sample_repo` fixture reusable by Task 002.9 validation tests
- `pipeline_results` fixture documents expected data structures
- Downstream compatibility test provides tag validation baseline

---

## Common Gotchas & Solutions

**Gotcha 1: Mock git repo state pollution between tests**
```python
# WRONG: Using shared mutable repo across tests
# RIGHT: Use tmp_path_factory with session scope, or reset repo state in fixture teardown
@pytest.fixture(scope="session")
def sample_repo(tmp_path_factory):
    repo = tmp_path_factory.mktemp("repo")
    # Initialize fresh repo
    return repo
```

**Gotcha 2: Floating point comparison in metric assertions**
```python
# WRONG: assert result['score'] == 0.85
# RIGHT: assert abs(result['score'] - 0.85) < 0.01
# OR: assert 0.84 < result['score'] < 0.86
import pytest
assert result['score'] == pytest.approx(0.85, abs=0.01)
```

**Gotcha 3: Performance tests inconsistent on different hardware**
```python
# WRONG: assert elapsed < 2.0  # Fails on slow CI machines
# RIGHT: Use generous thresholds and mark as slow
@pytest.mark.slow
def test_performance():
    assert elapsed < 600  # 10 minutes — generous for CI
```

**Gotcha 4: Test ordering dependencies**
```python
# WRONG: test_caching relies on test_pipeline running first
# RIGHT: Each test is fully self-contained with own setup/teardown
def test_pipeline_caching_enabled(sample_repo):
    pipeline = BranchClusteringPipeline(sample_repo)
    pipeline.run()  # First run — populate cache
    pipeline.run()  # Second run — should use cache
```

**Gotcha 5: JSON schema validation missing nested fields**
```python
# WRONG: Checking only top-level keys
# RIGHT: Validate nested structure recursively
def validate_schema(data, schema):
    for key, expected_type in schema.items():
        assert key in data, f"Missing key: {key}"
        if isinstance(expected_type, dict):
            validate_schema(data[key], expected_type)
```

---

## Integration Checkpoint

**When to move to Task 002.9 (FrameworkIntegration):**

- [ ] All 8 sub-subtasks complete
- [ ] All 74 test cases implemented and passing:
  - 12 CommitHistoryAnalyzer + 12 CodebaseStructureAnalyzer + 12 DiffDistanceCalculator
  - 12 BranchClusterer + 12 IntegrationTargetAssigner
  - 10 Full Pipeline + 6 Output Validation + 5 Edge Cases + 3 Performance
- [ ] >90% code coverage achieved
- [ ] No flaky tests
- [ ] Coverage report generated (HTML)
- [ ] All edge cases handled gracefully
- [ ] Performance benchmarks within thresholds
- [ ] Code review approved
- [ ] Commit message: "feat: complete Task 002.8 TestingSuite"

---

## Done Definition

Task 002.8 is done when:

1. All 8 sub-subtasks marked complete
2. All 74 test cases pass (`pytest tests/` exits 0)
3. Code coverage >90% on all components
4. Coverage HTML report generated
5. No memory leaks or performance regressions
6. Edge cases handled gracefully with clear error messages
7. Test output clear and actionable
8. All tests self-contained (no ordering dependencies)
9. Code review approved
10. Ready for hand-off to Task 002.9

---

## Provenance

**Source:** HANDOFF_75.8_TestingSuite
**Original Task ID:** 75.8
**Migrated To:** 002.8
**Migration Date:** 2026-01-29
**Consolidation:** All test case function signatures and test structure from HANDOFF preserved in 14-section standard format

---

## Next Steps

1. **Immediate:** Begin with sub-subtask 002.8.1 (Design Comprehensive Test Architecture and Framework)
2. **Week 1:** Complete all 8 sub-subtasks with proper test coverage for each component
3. **Week 1-2:** Implement unit tests for all 5 analyzer components (002.1-002.5)
4. **Week 2:** Create integration tests for pipeline components (002.4, 002.6)
5. **Week 2:** Write comprehensive tests for all 7 testing scenarios
6. **Week 2-3:** Performance validation and coverage optimization
7. **Week 3:** Code review and documentation completion
8. **Upon completion:** Ready for hand-off to Task 002.9 (FrameworkIntegration)
9. **Parallel tasks:** Task 002.9 (FrameworkIntegration) can proceed in parallel
