# Task 75.8: TestingSuite

## Purpose
Implement comprehensive testing across all Stage One and Stage Two components (Tasks 75.1-75.6). This Stage Three task ensures system reliability, performance, and correctness through unit tests, integration tests, and performance benchmarks.

**Scope:** Complete testing framework and test suite  
**Effort:** 24-32 hours | **Complexity:** 6/10  
**Status:** Ready when 75.6 complete  
**Blocks:**

---

## Quick Navigation

Navigate this document using these links:

- [Purpose](#purpose)
- [Success Criteria](#success-criteria)
- [Test Categories](#test-categories)
- [Subtasks Overview](#subtasks-overview)
- [Subtask Details](#subtasks)
- [Configuration](#configuration--defaults)
- [Technical Reference](#technical-reference)
- [Gotchas](#common-gotchas--solutions)
- [Workflow](#typical-development-workflow)
- [Integration Handoff](#integration-handoff)
- [Checkpoint](#integration-checkpoint)
- [Done Definition](#done-definition)

**Pro tip:** Use Ctrl+F to search within sections, or click links above to jump directly

---

--- Task 75.9
**Dependencies:** Tasks 75.1-75.6

---

## Success Criteria

Task 75.8 is complete when:

**Unit Testing:**
- [ ] Unit tests for all 75.1-75.6 components (minimum 30+ tests)
- [ ] Code coverage >90% across all modules
- [ ] All tests pass with zero failures
- [ ] Edge cases covered (empty inputs, invalid data, etc.)
- [ ] Exception handling tested

**Integration Testing:**
- [ ] End-to-end pipeline tests (minimum 8+ tests)
- [ ] Output file validation tests
- [ ] Component interaction tests
- [ ] Error handling integration tests
- [ ] Performance regression tests

**Performance Testing:**
- [ ] Benchmarks for each component (75.1-75.6)
- [ ] End-to-end performance target verification (<2 minutes for 13 branches)
- [ ] Memory usage profiling
- [ ] CPU usage analysis
- [ ] Scalability testing (with >13 branches)

**Test Infrastructure:**
- [ ] pytest configuration and setup
- [ ] Test fixtures and test data
- [ ] Coverage reporting
- [ ] Performance reporting
- [ ] CI/CD integration guidance

**Quality Metrics:**
- [ ] All tests automated and reproducible
- [ ] Test documentation complete
- [ ] Failure diagnostics clear and actionable
- [ ] Test suite execution <5 minutes total

---

## Test Categories

### Unit Tests (75.1-75.6)

**Task 75.1 - CommitHistoryAnalyzer (5+ tests)**
```
test_commit_history_loading
test_commit_parsing
test_commit_filtering_by_date
test_author_aggregation
test_edge_cases_empty_history
```

**Task 75.2 - CodebaseStructureAnalyzer (5+ tests)**
```
test_codebase_loading
test_directory_structure_parsing
test_file_count_aggregation
test_language_detection
test_edge_cases_empty_codebase
```

**Task 75.3 - DiffDistanceCalculator (5+ tests)**
```
test_diff_calculation
test_distance_metrics
test_normalization
test_similarity_scoring
test_edge_cases_identical_branches
```

**Task 75.4 - BranchClusterer (6+ tests)**
```
test_clustering_algorithm
test_cluster_quality_metrics
test_silhouette_calculation
test_davies_bouldin_calculation
test_calinski_harabasz_calculation
test_edge_cases_single_branch
```

**Task 75.5 - IntegrationTargetAssigner (5+ tests)**
```
test_confidence_scoring
test_target_assignment
test_affinity_scoring
test_tag_assignment
test_edge_cases_low_confidence
```

**Task 75.6 - BranchClusteringEngine (4+ tests)**
```
test_pipeline_orchestration
test_component_integration
test_output_file_generation
test_caching_mechanism
```

### Integration Tests (8+ tests)

```
test_end_to_end_pipeline
test_pipeline_with_all_branches
test_output_file_validation
test_json_schema_compliance
test_error_recovery
test_pipeline_idempotence
test_concurrent_execution
test_partial_failure_handling
```

### Performance Tests (5+ tests)

```
test_commit_analyzer_performance
test_structure_analyzer_performance
test_diff_calculator_performance
test_clustering_performance
test_end_to_end_performance_target
```

---

## Output Files

### 1. test_results_summary.json
Aggregated test results and metrics

```json
{
  "test_run_timestamp": "2024-01-04T12:00:00Z",
  "total_tests": 40,
  "passed": 40,
  "failed": 0,
  "skipped": 0,
  "success_rate": 100,
  "total_duration_seconds": 125,
  "coverage": {
    "overall_percentage": 92.5,
    "by_module": {
      "commit_analyzer": 95,
      "structure_analyzer": 88,
      "diff_calculator": 93,
      "clusterer": 90,
      "assignment": 91,
      "engine": 87
    }
  }
}
```

### 2. performance_benchmark_report.json
Performance metrics for each component

```json
{
  "benchmark_run_timestamp": "2024-01-04T12:00:00Z",
  "components": {
    "commit_analyzer": {
      "avg_duration_seconds": 12.5,
      "min_duration_seconds": 11.2,
      "max_duration_seconds": 14.1,
      "target_seconds": 30,
      "status": "pass"
    },
    "structure_analyzer": {
      "avg_duration_seconds": 8.3,
      "target_seconds": 30,
      "status": "pass"
    },
    "end_to_end_pipeline": {
      "avg_duration_seconds": 85,
      "max_duration_seconds": 110,
      "target_seconds": 120,
      "status": "pass"
    }
  }
}
```

### 3. coverage_report.html
HTML coverage report (generated by pytest-cov)

### 4. test_documentation.md
Complete testing guide and results documentation

---

## Subtasks Overview

### Dependency Flow Diagram

```
75.8.1 (2-3h)
[Test Infrastructure]
    │
    ├─→ 75.8.2 (4-5h) ────────┐
    │   [Unit Tests 75.1-75.3] │
    │                          ├─→ 75.8.4 (4-5h) ────────┐
    ├─→ 75.8.3 (4-5h) ────────┤  [Integration Tests]     │
    │   [Unit Tests 75.4-75.6] │                         ├─→ 75.8.6 (2-3h) ──┐
    │                          ├─→ 75.8.5 (3-4h) ────────┤  [Coverage Report] │
    └─→ 75.8.7 (2-3h) ────────┤  [Performance Tests]     │                   ├─→ 75.8.8 (2-3h)
        [Test Documentation]   │                         │  [CI/CD Setup]    │
                               │                         │                   │
                               └─────────────────────────┘                   │
                                                                            │
                                                                           ─┘

Critical Path: 75.8.1 → 75.8.2-75.8.3 (parallel) → 75.8.4 → 75.8.6 → 75.8.8
Minimum Duration: 24-32 hours (with parallelization)
```

### Parallel Opportunities

**Can run in parallel (after 75.8.1):**
- 75.8.2: Unit tests for analyzers (4-5 hours)
- 75.8.3: Unit tests for clustering/assignment (4-5 hours)
- 75.8.7: Documentation (2-3 hours)

These tasks depend only on test infrastructure (75.8.1) and are independent. **Estimated parallel execution saves 8-10 hours.**

**Must be sequential:**
- 75.8.1 → all others (infrastructure prerequisite)
- 75.8.2, 75.8.3 → 75.8.4 (need unit tests before integration)
- 75.8.4 → 75.8.6 (need tests before coverage report)
- 75.8.6 → 75.8.8 (need results before CI/CD)

### Timeline with Parallelization

**Days 1: Test Infrastructure (75.8.1)**
- Install pytest, pytest-cov, pytest-benchmark
- Create conftest.py with fixtures
- Create test data

**Days 1-3: Parallel Unit Tests (75.8.2, 75.8.3, 75.8.7)**
- **75.8.2 (Person A, Days 2-3):** Tests for Tasks 75.1-75.3
- **75.8.3 (Person B, Days 2-3):** Tests for Tasks 75.4-75.6
- **75.8.7 (Person C, Days 2-3):** Test documentation
- Merge at end of Day 3

**Days 3-4: Integration Testing (75.8.4)**
- End-to-end pipeline tests
- Component interaction tests
- Performance regression tests

**Days 4-5: Reports & CI/CD (75.8.5-75.8.8)**
- Day 4: Performance benchmarks, coverage reports
- Day 5: CI/CD setup, final validation

---

## Subtasks

### 75.8.1: Setup Test Infrastructure
**Purpose:** Configure testing framework and tools  
**Effort:** 2-3 hours

**Steps:**
1. Install pytest, pytest-cov, pytest-benchmark
2. Create conftest.py with shared fixtures
3. Create test data and fixtures
4. Setup CI/CD test execution
5. Configure coverage thresholds

**Success Criteria:**
- [ ] pytest runs successfully
- [ ] Test fixtures load correctly
- [ ] Coverage reports generate
- [ ] CI/CD integration ready


### Implementation Checklist (From HANDOFF)
- [ ] Install pytest, pytest-cov, pytest-benchmark
- [ ] Create conftest.py with shared fixtures
- [ ] Create test data and branch fixtures
- [ ] Setup CI/CD test execution
- [ ] Configure coverage thresholds (>90%)
---

### 75.8.2: Implement Unit Tests for 75.1-75.3
**Purpose:** Test analyzers (commit, structure, diff)  
**Effort:** 4-5 hours

**Steps:**
1. Create test modules for each analyzer
2. Implement comprehensive unit tests
3. Test edge cases and error conditions
4. Verify analyzer output correctness
5. Achieve >90% coverage per module

**Success Criteria:**
- [ ] 15+ unit tests pass
- [ ] Coverage >90% for analyzers
- [ ] All edge cases covered
- [ ] Error handling tested


### Implementation Checklist (From HANDOFF)
- [ ] Create test modules for Tasks 75.1-75.3 analyzers
- [ ] Implement 15+ unit tests for analyzers
- [ ] Test edge cases and error conditions
- [ ] Verify analyzer output correctness
- [ ] Achieve >90% coverage per module
---

### 75.8.3: Implement Unit Tests for 75.4-75.6
**Purpose:** Test clusterer, assigner, and engine  
**Effort:** 4-5 hours

**Steps:**
1. Create test modules for 75.4, 75.5, 75.6
2. Implement comprehensive unit tests
3. Test clustering quality metrics
4. Test assignment logic
5. Test orchestration flow

**Success Criteria:**
- [ ] 15+ unit tests pass
- [ ] Coverage >90% for components
- [ ] All edge cases covered
- [ ] Orchestration tested end-to-end


### Implementation Checklist (From HANDOFF)
- [ ] Create test modules for Tasks 75.4-75.6
- [ ] Implement 15+ unit tests for clustering/assignment/engine
- [ ] Test clustering quality metrics
- [ ] Test assignment logic
- [ ] Test orchestration flow
---

### 75.8.4: Implement Integration Tests
**Purpose:** Test component interactions  
**Effort:** 3-4 hours

**Steps:**
1. Create integration test module
2. Implement end-to-end pipeline tests
3. Test output file generation
4. Test error recovery paths
5. Test concurrent execution

**Success Criteria:**
- [ ] 8+ integration tests pass
- [ ] End-to-end flow verified
- [ ] Output files validated
- [ ] Error recovery confirmed


### Implementation Checklist (From HANDOFF)
- [ ] Create integration test module
- [ ] Implement 8+ end-to-end pipeline tests
- [ ] Test output file generation
- [ ] Test error recovery paths
- [ ] Test concurrent execution
---

### 75.8.5: Implement Performance Tests
**Purpose:** Benchmark and verify performance targets  
**Effort:** 3-4 hours

**Steps:**
1. Implement performance benchmark tests
2. Benchmark each component
3. Verify <2 minute target for pipeline
4. Profile memory usage
5. Generate performance report

**Success Criteria:**
- [ ] All components meet performance targets
- [ ] End-to-end performance <120 seconds
- [ ] Memory usage <100MB
- [ ] Benchmarks reproducible


### Implementation Checklist (From HANDOFF)
- [ ] Implement performance benchmark tests
- [ ] Benchmark each component individually
- [ ] Verify <2 minute target for full pipeline
- [ ] Profile memory usage
- [ ] Generate performance report
---

### 75.8.6: Generate Coverage Reports
**Purpose:** Create coverage documentation  
**Effort:** 2-3 hours

**Steps:**
1. Generate HTML coverage report
2. Identify coverage gaps
3. Add tests for gaps
4. Document coverage by module
5. Set coverage thresholds

**Success Criteria:**
- [ ] Coverage report generated
- [ ] Overall coverage >90%
- [ ] Coverage by module >85%
- [ ] Gaps identified and addressed


### Implementation Checklist (From HANDOFF)
- [ ] Generate HTML coverage report
- [ ] Identify coverage gaps
- [ ] Add tests for gaps
- [ ] Document coverage by module
- [ ] Set coverage thresholds in CI/CD
---

### 75.8.7: Implement Test Documentation
**Purpose:** Document testing approach and results  
**Effort:** 2-3 hours

**Steps:**
1. Document test structure and organization
2. Create test execution guide
3. Document test data and fixtures
4. Create failure diagnosis guide
5. Document CI/CD integration

**Success Criteria:**
- [ ] Testing guide complete
- [ ] Test execution reproducible
- [ ] Failure diagnosis documented
- [ ] CI/CD integration clear


### Implementation Checklist (From HANDOFF)
- [ ] Document test structure and organization
- [ ] Create test execution guide
- [ ] Document test data and fixtures
- [ ] Create failure diagnosis guide
- [ ] Document CI/CD integration
---

### 75.8.8: Verify Test Results & Quality
**Purpose:** Final verification and quality assurance  
**Effort:** 2-3 hours

**Steps:**
1. Run complete test suite
2. Verify all tests pass
3. Verify coverage >90%
4. Verify performance targets met
5. Document final results

**Success Criteria:**
- [ ] All tests pass (40+ tests)
- [ ] Coverage >90%
- [ ] Performance targets met
- [ ] Ready for production


### Implementation Checklist (From HANDOFF)
- [ ] Run complete test suite
- [ ] Verify all tests pass
- [ ] Verify coverage >90%
- [ ] Verify performance targets met
- [ ] Document final results
---

## Typical Development Workflow

```bash
git checkout -b feat/comprehensive-testing
mkdir -p tests/{unit,integration,performance} test_data

# Step 1: Setup test infrastructure (75.8.1)
cat > pytest.ini << 'EOF'
[pytest]
minversion = 6.0
addopts = -v --tb=short --cov=src --cov-report=html --cov-report=term
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
EOF

cat > tests/conftest.py << 'EOF'
import pytest
import tempfile
import shutil

@pytest.fixture
def test_repo():
    """Create temporary test repository."""
    repo_dir = tempfile.mkdtemp()
    yield repo_dir
    shutil.rmtree(repo_dir)

@pytest.fixture
def sample_branches():
    """Sample branch data for testing."""
    return ['main', 'feature/auth', 'feature/api', 'bugfix/db-issue']

git add pytest.ini tests/conftest.py
git commit -m "test: pytest infrastructure (75.8.1)"
```

# Step 2: Unit tests for analyzers (75.8.2)
```bash
cat > tests/unit/test_commit_history_analyzer.py << 'EOF'
import pytest
from src.analyzers import CommitHistoryAnalyzer

class TestCommitHistoryAnalyzer:
    def test_initialization(self, test_repo):
        analyzer = CommitHistoryAnalyzer(test_repo)
        assert analyzer is not None
    
    def test_analyze_returns_dict(self, test_repo):
        analyzer = CommitHistoryAnalyzer(test_repo)
        result = analyzer.analyze('main')
        assert isinstance(result, dict)
        assert 'metrics' in result
    
    # ... more tests (15+ total)
EOF

git add tests/unit/
git commit -m "test: unit tests for analyzers (75.8.2)"
```

# Step 3: Unit tests for clustering (75.8.3)
```bash
cat > tests/unit/test_branch_clusterer.py << 'EOF'
import pytest
from src.clustering import BranchClusterer

class TestBranchClusterer:
    def test_clustering_algorithm(self):
        # Test Ward linkage clustering
        pass
    
    def test_quality_metrics(self):
        # Test silhouette, Davies-Bouldin, Calinski-Harabasz
        pass
    
    # ... more tests (15+ total)
EOF

git add tests/unit/
git commit -m "test: unit tests for clustering/assignment (75.8.3)"
```

# Step 4: Integration tests (75.8.4)
```bash
cat > tests/integration/test_end_to_end_pipeline.py << 'EOF'
import pytest

class TestEndToEndPipeline:
    def test_complete_pipeline(self, test_repo, sample_branches):
        # Full pipeline: analyze → cluster → assign → output
        pass
    
    def test_output_file_generation(self):
        # Verify all output files created
        pass
    
    # ... more tests (8+ total)
EOF

git add tests/integration/
git commit -m "test: integration tests (75.8.4)"
```

# Step 5: Performance tests (75.8.5)
```bash
cat > tests/performance/test_benchmarks.py << 'EOF'
import pytest

class TestPerformance:
    @pytest.mark.benchmark
    def test_commit_analyzer_performance(self, benchmark):
        # Single analysis <2 seconds
        benchmark(analyzer.analyze, 'branch')
    
    @pytest.mark.benchmark
    def test_full_pipeline_performance(self, benchmark):
        # Full pipeline <120 seconds for 13 branches
        benchmark(engine.execute, branches)
EOF

git add tests/performance/
git commit -m "test: performance benchmarks (75.8.5)"
```

# Step 6: Coverage report (75.8.6)
```bash
pytest tests/ -v --cov=src --cov-report=html --cov-report=term
# Verify coverage >90%
cat > htmlcov/index.html  # Generated HTML report

git add htmlcov/
git commit -m "test: coverage report (75.8.6)"
```

# Step 7: Documentation (75.8.7)
```bash
cat > docs/TESTING_GUIDE.md << 'EOF'
# Testing Guide

## Running Tests

### All tests
\`\`\`bash
pytest tests/ -v
\`\`\`

### Unit tests only
\`\`\`bash
pytest tests/unit/ -v
\`\`\`

### With coverage
\`\`\`bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
\`\`\`

## Performance Benchmarks

\`\`\`bash
pytest tests/performance/ -v --benchmark-only
\`\`\`
EOF

git add docs/TESTING_GUIDE.md
git commit -m "docs: testing guide (75.8.7)"
```

# Step 8: CI/CD setup (75.8.8)
```bash
cat > .github/workflows/test.yml << 'EOF'
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --cov=src
      - uses: codecov/codecov-action@v2
EOF

git add .github/workflows/test.yml
git commit -m "ci: GitHub Actions test workflow (75.8.8)"

# Final push
pytest tests/ -v --cov=src --cov-report=html
git push origin feat/comprehensive-testing
```

---

## Integration Handoff

**Task 75.6 Outputs → Task 75.8:**
- clustered_branches.json
- categorized_branches.json
- branch_export.json

**Task 75.8 Outputs → Task 75.9:**
- All passing unit/integration/performance tests
- Coverage report (>90%)
- CI/CD workflow configured
- Test documentation

---

## Common Gotchas & Solutions

### Gotcha 1: Test Fixtures Don't Cleanup After Themselves ⚠️

**Problem:** Test temporary files/repos accumulate, disk fills up
**Symptom:** `OSError: No space left on device`
**Root Cause:** Fixtures not using context managers or cleanup

**Solution:**
```python
import tempfile
import shutil

@pytest.fixture
def test_repo():
    """Create and cleanup temporary repo."""
    repo_dir = tempfile.mkdtemp(prefix='test_')
    try:
        yield repo_dir
    finally:
        shutil.rmtree(repo_dir, ignore_errors=True)  # Cleanup
```

**Test:**
```bash
df -h  # Check disk before and after test run
```

---

### Gotcha 2: Coverage Reports Don't Show All Modules ⚠️

**Problem:** Coverage report missing modules even though they're used
**Symptom:** Coverage <90%, missing modules in report
**Root Cause:** pytest-cov not configured to find all packages

**Solution:**
```bash
# pytest.ini
[pytest]
addopts = --cov=src --cov=tests --cov-report=html
```

```bash
# Or command line
pytest tests/ --cov=src --cov=tests --cov-report=html
```

**Test:**
```bash
coverage html
open htmlcov/index.html
# Verify all modules listed
```

---

### Gotcha 3: Performance Tests Take Too Long ⚠️

**Problem:** Benchmark tests take >10 minutes to run
**Symptom:** CI/CD timeout before test completion
**Root Cause:** Running too many benchmark iterations

**Solution:**
```python
@pytest.mark.benchmark(
    min_rounds=3,  # Reduce from default 5
    max_time=1.0,  # 1 second max per test
)
def test_analyzer_performance(self, benchmark):
    benchmark(analyzer.analyze, branch)
```

**Test:**
```bash
pytest tests/performance/ -v --benchmark-only
# Should complete in <5 minutes
```

---

### Gotcha 4: Unit Tests Pass But Integration Tests Fail ⚠️

**Problem:** Components work individually but fail when combined
**Symptom:** All unit tests pass, but end-to-end fails
**Root Cause:** Mock/stub differences between unit and integration

**Solution:**
```python
# Use pytest fixtures for both unit and integration
@pytest.fixture(scope='session')
def real_repo():
    """Real repository for integration tests."""
    return '/path/to/test/repo'

@pytest.fixture
def mock_repo(mocker):
    """Mocked repo for unit tests."""
    return mocker.MagicMock()

# Unit tests use mock_repo
# Integration tests use real_repo
```

**Test:**
```bash
pytest tests/unit/ -v          # Unit tests
pytest tests/integration/ -v   # Integration tests
```

---

### Gotcha 5: Tests Fail on CI But Pass Locally ⚠️

**Problem:** Tests pass in local env but fail on GitHub Actions
**Symptom:** Green locally, red on CI
**Root Cause:** Environment differences (Python version, OS, dependencies)

**Solution:**
```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    steps:
      - uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      - run: pytest tests/ -v
```

**Test:**
```bash
# Test locally with same Python version
python --version
pytest tests/ -v
```

---

### Gotcha 6: Benchmark Results Vary Wildly ⚠️

**Problem:** Performance test passes sometimes, fails sometimes
**Symptom:** Inconsistent benchmark results (0.5-5 seconds variance)
**Root Cause:** System load, warm-up effects, GC pauses

**Solution:**
```python
@pytest.mark.benchmark
def test_performance(self, benchmark):
    """Benchmark with stable conditions."""
    # Warm up
    for _ in range(3):
        analyzer.analyze('branch')
    
    # Measure
    result = benchmark(analyzer.analyze, 'branch')
    
    # Result includes min, max, mean, median
    assert result < 2.0  # 2 seconds
```

**Tune:**
```bash
pytest tests/ -v --benchmark-sort=mean --benchmark-compare
```

---

### Gotcha 7: Mock Data Doesn't Match Real Schema ⚠️

**Problem:** Mock test data doesn't match actual output schema
**Symptom:** Unit tests pass, but integration fails with `KeyError`
**Root Cause:** Mock data not validated against actual schema

**Solution:**
```python
import json
from jsonschema import validate

# Load real schema
with open('schema/clustered_branches.schema.json') as f:
    schema = json.load(f)

@pytest.fixture
def mock_clustered_branches():
    """Mock data matching real schema."""
    return {
        'branches': [...],
        'quality_metrics': {...}
    }

def test_mock_data_valid():
    """Verify mock matches schema."""
    validate(instance=mock_clustered_branches, schema=schema)
```

---

### Gotcha 8: CI/CD Secret Exposure in Logs ⚠️

**Problem:** API keys or secrets accidentally logged in CI output
**Symptom:** Security warning: credentials in job logs
**Root Cause:** Not masking sensitive config values

**Solution:**
```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    env:
      # GitHub automatically masks secrets
      API_KEY: ${{ secrets.API_KEY }}
    steps:
      - run: echo "Starting tests..."
        # API_KEY will be masked in logs as ***
```

**Verify:**
```bash
# Check logs don't contain actual secrets
grep -r "sk-" .github/workflows/  # Should be empty
```

---

## Configuration Parameters

- `TEST_FRAMEWORK` = "pytest"
- `COVERAGE_THRESHOLD_PERCENTAGE` = 90
- `PERFORMANCE_TIMEOUT_SECONDS` = 300
- `BENCHMARK_RUNS_PER_TEST` = 5
- `CI_EXECUTION_TIMEOUT_MINUTES` = 10
- `VERBOSE_OUTPUT` = true

---


## Technical Reference (From HANDOFF)

### Test Framework Setup
```bash
# pytest.ini configuration
[pytest]
minversion = 6.0
addopts = -v --tb=short --cov=clustering --cov-report=html
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### Test Directory Structure
```
tests/
├── unit/
│   ├── test_commit_history_analyzer.py
│   ├── test_codebase_structure_analyzer.py
│   ├── test_diff_distance_calculator.py
│   ├── test_branch_clusterer.py
│   └── test_integration_target_assigner.py
├── integration/
│   ├── test_full_pipeline.py
│   ├── test_pipeline_caching.py
│   └── test_json_outputs.py
├── fixtures/
│   ├── sample_repo/  (Mock git repo)
│   ├── analyzer_outputs/  (Expected outputs)
│   └── pipeline_results/  (Expected results)
└── conftest.py  (Shared fixtures)
```

### Performance Baselines
- Commit Analyzer: <30 seconds per branch
- Structure Analyzer: <30 seconds per branch
- Diff Calculator: <45 seconds per branch
- Clustering: <10 seconds for 13+ branches
- Assignment: <5 seconds for 13+ branches
- Full Pipeline: <120 seconds for 13+ branches

### Dependencies & Integration
- Blocked by: Tasks 75.1-75.6 (all must complete first)
- Feeds into: Task 75.9 (FrameworkIntegration)
- External libraries: pytest, pytest-cov, pytest-xdist, pytest-benchmark

---

## Integration Checkpoint

**When to move to 75.9:**
- [ ] All 8 subtasks complete
- [ ] 40+ unit/integration tests passing
- [ ] Coverage >90% across all modules
- [ ] Performance targets verified
- [ ] All documentation complete
- [ ] Ready for framework integration (75.9)

---

## Performance Targets

- **Commit Analyzer:** <30 seconds
- **Structure Analyzer:** <30 seconds
- **Diff Calculator:** <45 seconds
- **Clustering:** <10 seconds
- **Assignment:** <5 seconds
- **End-to-end Pipeline:** <120 seconds (2 minutes) for 13+ branches

---

## Done Definition

Task 75.8 is done when:
1. All 8 subtasks marked complete
2. 40+ tests passing (unit, integration, performance)
3. Coverage >90% across all modules
4. Performance targets verified and documented
5. Test reports generated
6. Complete testing documentation
7. Ready for framework integration (75.9) and deployment (100)
