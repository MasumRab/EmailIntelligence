# Task 002.9: FrameworkIntegration

**Status:** Ready for Implementation
**Priority:** High
**Effort:** 16-24 hours
**Complexity:** 6/10
**Dependencies:** 002.1, 002.2, 002.3, 002.4, 002.5, 002.6, 002.7, 002.8

---

## Overview/Purpose

Integrate the complete branch clustering system into a unified public API, create downstream task integration bridges for Tasks 79, 80, 83, and 101, finalize configuration management, implement deployment validation, and ensure all components work together as a cohesive package. This is the final Stage Three component that wraps Tasks 002.1-002.8 into a production-ready framework.

**Scope:** `BranchClusteringFramework` class, downstream bridges, config management, deployment validation, package structure
**Deliverables:** 9 items (framework, bridges, config, validator, docs, sample config, package, validation report, version tag)

---

## Success Criteria

Task 002.9 is complete when:

### Core Functionality
- [ ] `BranchClusteringFramework` class integrates all components (002.1-002.8)
- [ ] `run()` orchestrates full pipeline end-to-end
- [ ] `analyze_branch()` performs single-branch analysis
- [ ] `get_branch_tags()` returns 30+ tags per branch
- [ ] `export_outputs()` generates all output files (3 JSON + 3 HTML) with path dict
- [ ] `validate_downstream_compatibility()` checks tag validity for Tasks 79, 80, 83, 101
- [ ] All 4 downstream bridges implemented and tested

### Quality Assurance
- [ ] Unit tests >90% coverage (verified by Task 002.8)
- [ ] Integration tests all passing
- [ ] Performance: 13 branches complete in <2 minutes, 50+ branches in <10 minutes
- [ ] Memory: peak usage <500 MB
- [ ] Caching functional and validated
- [ ] All visualizations render correctly
- [ ] Comprehensive docstrings on all public methods

### Integration Readiness
- [ ] Task 79 execution context bridge working with correct tag mappings
- [ ] Task 80 test intensity bridge working with correct tag mappings
- [ ] Task 83 test suite selection bridge working with correct tag mappings
- [ ] Task 101 orchestration filter bridge working with correct tag mappings
- [ ] Configuration system loads from YAML and validates
- [ ] Deployment validation passes all checks
- [ ] Package structure matches specification

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 002.1 (CommitHistoryAnalyzer) complete
- [ ] Task 002.2 (CodebaseStructureAnalyzer) complete
- [ ] Task 002.3 (DiffDistanceCalculator) complete
- [ ] Task 002.4 (BranchClusterer) complete
- [ ] Task 002.5 (IntegrationTargetAssigner) complete
- [ ] Task 002.6 (BranchClusteringPipeline) complete
- [ ] Task 002.7 (VisualizationReporting) complete
- [ ] Task 002.8 (TestingSuite) complete — all tests passing

### Blocks (What This Task Unblocks)
- Task 79 (Execution Context — Parallel/Serial Control)
- Task 80 (Validation Intensity Selection)
- Task 83 (Test Suite Selection)
- Task 101 (Orchestration Filtering)
- Deployment of branch clustering system

### External Dependencies
- Python 3.8+
- `scipy`, `scikit-learn`, `plotly`, `pandas`, `pyyaml`
- Optional: `pytest`, `pytest-cov` (for validation)

---

## Sub-subtasks Breakdown

### 002.9.1: BranchClusteringFramework Class
**Effort:** 4-5 hours
**Depends on:** None (all component code exists)

**Steps:**
1. Create `clustering_framework.py` in main package
2. Implement `__init__(self, repo_path: str, config: dict = None)` with config loading/validation
3. Implement `run(self, branches: list = None) -> dict` orchestrating full pipeline
4. Implement `analyze_branch(self, branch_name: str) -> dict` for single-branch analysis
5. Implement `get_branch_tags(self, branch_name: str) -> list` utility
6. Implement `export_outputs(self, output_dir: str) -> dict` with path management
7. Implement `validate_downstream_compatibility(self) -> dict` checking tag validity
8. Add comprehensive docstrings and logging at key checkpoints
9. Handle errors gracefully with informative messages

**Success Criteria:**
- [ ] All 6 public methods work end-to-end
- [ ] Config loading from dict or YAML file
- [ ] Errors produce clear messages, not stack traces

---

### 002.9.2: Downstream Integration Bridges
**Effort:** 4-5 hours
**Depends on:** 002.9.1

**Steps:**
1. Create `downstream_bridges.py` module
2. Implement Task 79 bridge: `get_execution_context_for_branch()`
3. Implement Task 80 bridge: `get_test_intensity_for_branch()`
4. Implement Task 83 bridge: `get_test_suites_for_branch()`
5. Implement Task 101 bridge: `passes_orchestration_filter()` and `filter_orchestration_branches()`
6. Test all mappings with sample tags
7. Add docstrings with examples
8. Document all tag-to-context mappings

**Success Criteria:**
- [ ] All 4 bridges return correct values for known tag sets
- [ ] Tag mapping tables match specification

---

### 002.9.3: Configuration Management
**Effort:** 2-3 hours
**Depends on:** 002.9.1

**Steps:**
1. Create `config_manager.py` module
2. Implement `ConfigurationManager.__init__(config_path: str = None)`
3. Implement `load_config() -> dict` from YAML
4. Implement `validate_config() -> bool` with schema checks
5. Implement `get_metric_weights() -> dict` and `get_analyzer_settings(analyzer_name) -> dict`
6. Add default configuration fallback
7. Support environment variable overrides
8. Create sample `clustering_config.yaml`

**Success Criteria:**
- [ ] YAML config loads correctly
- [ ] Validation catches missing/invalid fields
- [ ] Defaults work when no config file provided

---

### 002.9.4: Deployment Validation
**Effort:** 2-3 hours
**Depends on:** 002.9.1, 002.9.2

**Steps:**
1. Create `deployment_validator.py` module
2. Implement `DeploymentValidator.validate_all_components() -> dict`
3. Implement `validate_output_formats() -> dict`
4. Implement `validate_downstream_compatibility() -> dict`
5. Implement `validate_performance_targets() -> dict`
6. Implement `generate_validation_report() -> str`

**Success Criteria:**
- [ ] All validation methods return pass/fail with details
- [ ] Validation report human-readable

---

### 002.9.5: Package Structure and Final Integration
**Effort:** 4-5 hours
**Depends on:** 002.9.1, 002.9.2, 002.9.3, 002.9.4

**Steps:**
1. Organize package directory tree matching specification
2. Create/update all `__init__.py` files with proper exports
3. Run full system integration verification (see verification pseudocode)
4. Generate final validation report
5. Create setup.py/pyproject.toml with dependencies
6. Create requirements.txt
7. Add version metadata (1.0.0)
8. Run all tests one final time

**Success Criteria:**
- [ ] `from clustering import BranchClusteringFramework` works
- [ ] Full pipeline runs end-to-end from package imports
- [ ] All tests pass from installed package

---

## Specification Details

### BranchClusteringFramework Class Interface

```python
from .analyzers import CommitHistoryAnalyzer, CodebaseStructureAnalyzer, DiffDistanceCalculator
from .clustering import BranchClusterer
from .assignment import IntegrationTargetAssigner
from .pipeline import BranchClusteringPipeline
from .visualization import ClusteringVisualizer

class BranchClusteringFramework:
    def __init__(self, repo_path: str, config: dict = None)
    def run(self, branches: list = None) -> dict
    def analyze_branch(self, branch_name: str) -> dict
    def get_branch_tags(self, branch_name: str) -> list
    def export_outputs(self, output_dir: str) -> dict
    def get_visualization_paths(self) -> dict
    def validate_downstream_compatibility(self) -> dict
```

### Public API Usage Example

```python
framework = BranchClusteringFramework(repo_path="/path/to/repo")

results = framework.run(branches=["feature/auth", "feature/api"])

tags = framework.get_branch_tags("feature/auth")
# Returns: ["core-feature", "security-sensitive", "low-risk", ...]

paths = framework.export_outputs(output_dir="/path/to/outputs")
# Returns: {
#   "categorized_branches": "path/to/categorized_branches.json",
#   "clustered_branches": "path/to/clustered_branches.json",
#   "orchestration_branches": "path/to/enhanced_orchestration_branches.json",
#   "dendrogram": "path/to/dendrogram.html",
#   "dashboard": "path/to/dashboard.html",
#   "report": "path/to/report.html"
# }

compat = framework.validate_downstream_compatibility()
# Returns: {
#   "task_79_compatible": True,
#   "task_80_compatible": True,
#   "task_83_compatible": True,
#   "task_101_compatible": True,
#   "issues": []
# }
```

### Task 79 Bridge: Execution Context

```python
def get_execution_context_for_branch(branch_name: str) -> dict:
    tags = framework.get_branch_tags(branch_name)
    return {
        "branch": branch_name,
        "parallelizable": "orchestration-branch" not in tags,
        "serial_dependency_count": infer_from_tags(tags),
        "execution_priority": infer_priority(tags),
        "resource_hints": {
            "cpu": "high" if "complex" in tags else "normal",
            "memory": "high" if "massive-impact" in tags else "normal"
        }
    }
```

**Tag Mappings for Task 79:**

| Tag | Execution Context |
|-----|-------------------|
| `orchestration-branch` | serial (strict ordering) |
| `core-feature` | serial (careful sequencing) |
| `parallel-safe` | parallel |
| `active-development` | higher priority queue |
| Others | parallel-safe by default |

### Task 80 Bridge: Validation Intensity

```python
def get_test_intensity_for_branch(branch_name: str) -> str:
    tags = framework.get_branch_tags(branch_name)
    if "complex" in tags or "high-risk" in tags:
        return "high"
    elif "moderate" in tags or "medium-risk" in tags:
        return "medium"
    else:
        return "low"
```

**Tag Mappings for Task 80:**

| Tag | Test Intensity |
|-----|----------------|
| `simple` | low |
| `moderate` | medium |
| `complex` | high |
| `high-risk` | high |
| `medium-risk` | medium |
| `low-risk` | low |

### Task 83 Bridge: Test Suite Selection

```python
def get_test_suites_for_branch(branch_name: str) -> list:
    tags = framework.get_branch_tags(branch_name)
    suites = []
    if "testing-required-high" in tags:
        suites.extend(["unit", "integration", "e2e", "performance"])
    elif "testing-required-medium" in tags:
        suites.extend(["unit", "integration"])
    else:
        suites.append("smoke")
    if "orchestration-branch" in tags:
        suites.append("orchestration")
    if "security-sensitive" in tags:
        suites.append("security")
    return suites
```

**Tag Mappings for Task 83:**

| Tag | Test Suites |
|-----|-------------|
| `testing-required-high` | unit, integration, e2e, performance |
| `testing-required-medium` | unit, integration |
| `testing-optional` | smoke |
| `orchestration-branch` | +orchestration |
| `security-sensitive` | +security |
| `api-changes` | +api-contract |

### Task 101 Bridge: Orchestration Filtering

```python
def passes_orchestration_filter(branch_name: str) -> bool:
    tags = framework.get_branch_tags(branch_name)
    return "orchestration-branch" in tags

def filter_orchestration_branches(branches: list) -> list:
    return [b for b in branches if passes_orchestration_filter(b)]
```

**Tag Mappings for Task 101:**

| Tag | Include in Orchestration |
|-----|-------------------------|
| `orchestration-branch` | Yes |
| `devops` | Yes |
| Any other tag | No |

### ConfigurationManager Class

```python
class ConfigurationManager:
    def __init__(self, config_path: str = None)
    def load_config(self) -> dict
    def validate_config(self) -> bool
    def get_metric_weights(self) -> dict
    def get_analyzer_settings(self, analyzer_name: str) -> dict
```

### DeploymentValidator Class

```python
class DeploymentValidator:
    def validate_all_components(self) -> dict
    def validate_output_formats(self) -> dict
    def validate_downstream_compatibility(self) -> dict
    def validate_performance_targets(self) -> dict
    def generate_validation_report(self) -> str
```

### Package Directory Tree

```
clustering/
├── __init__.py
├── clustering_framework.py          # Main public API (this task)
├── config_manager.py                # Configuration loading (this task)
├── downstream_bridges.py            # Integration functions (this task)
├── deployment_validator.py          # Validation utilities (this task)
├── analyzers/
│   ├── __init__.py
│   ├── commit_history.py            # Task 002.1
│   ├── codebase_structure.py        # Task 002.2
│   └── diff_distance.py             # Task 002.3
├── clustering/
│   ├── __init__.py
│   └── branch_clusterer.py          # Task 002.4
├── assignment/
│   ├── __init__.py
│   └── integration_target.py        # Task 002.5
├── pipeline/
│   ├── __init__.py
│   └── orchestration.py             # Task 002.6
├── visualization/
│   ├── __init__.py
│   └── reporter.py                  # Task 002.7
├── tests/
│   ├── unit/                        # Task 002.8
│   ├── integration/                 # Task 002.8
│   └── conftest.py                  # Task 002.8
├── config/
│   └── clustering_config.yaml
├── docs/
│   ├── README.md
│   ├── INSTALLATION.md
│   ├── USAGE.md
│   ├── API_REFERENCE.md
│   ├── TAG_CATALOG.md
│   ├── INTEGRATION_GUIDE.md
│   ├── TROUBLESHOOTING.md
│   └── EXAMPLES.md
└── setup.py
```

### Final Integration Verification Pseudocode

```python
def verify_system_integration():
    from clustering import BranchClusteringFramework
    from clustering.downstream_bridges import (
        get_execution_context_for_branch,
        get_test_intensity_for_branch,
        get_test_suites_for_branch,
        passes_orchestration_filter
    )

    fw = BranchClusteringFramework(repo_path)
    results = fw.run(sample_branches)

    assert results['categorized_branches'] is not None
    assert results['clustered_branches'] is not None
    assert results['orchestration_branches'] is not None

    compat = fw.validate_downstream_compatibility()
    assert all(v for k, v in compat.items() if k != 'issues')

    for branch in sample_branches:
        tags = fw.get_branch_tags(branch)
        ctx_79 = get_execution_context_for_branch(branch)
        intensity_80 = get_test_intensity_for_branch(branch)
        suites_83 = get_test_suites_for_branch(branch)
        passes_101 = passes_orchestration_filter(branch)

    print("System integration complete and verified")
```

---

## Implementation Guide

### Step 1: Create clustering_framework.py
```python
class BranchClusteringFramework:
    def __init__(self, repo_path: str, config: dict = None):
        self.repo_path = repo_path
        self.config_manager = ConfigurationManager(config)
        self.config = self.config_manager.load_config()
        self._pipeline = None
        self._results = None

    def run(self, branches: list = None) -> dict:
        self._pipeline = BranchClusteringPipeline(
            self.repo_path, self.config)
        self._results = self._pipeline.run(branches)
        return self._results

    def analyze_branch(self, branch_name: str) -> dict:
        analyzers = [
            CommitHistoryAnalyzer(self.repo_path),
            CodebaseStructureAnalyzer(self.repo_path),
            DiffDistanceCalculator(self.repo_path)
        ]
        return {a.__class__.__name__: a.analyze(branch_name) for a in analyzers}
```

### Step 2: Create downstream_bridges.py
Implement each bridge function referencing framework instance. Each function takes a branch_name, retrieves tags via `framework.get_branch_tags()`, and maps tags to the appropriate downstream context.

### Step 3: Create config_manager.py
Load YAML config with `pyyaml`, validate required sections exist (metrics, commit_history, codebase_structure, diff_distance, clustering, assignment, framework), provide sensible defaults.

### Step 4: Create deployment_validator.py
Each validation method imports and instantiates components, runs a minimal test, and reports pass/fail.

### Step 5: Assemble Package
Create `__init__.py` with `from .clustering_framework import BranchClusteringFramework`. Create setup.py with install_requires listing all dependencies.

---

## Configuration & Defaults

### clustering_config.yaml

```yaml
metrics:
  commit_history_weight: 0.35
  codebase_structure_weight: 0.35
  diff_distance_weight: 0.30

commit_history:
  recency_window_days: 30
  weights:
    recency: 0.25
    frequency: 0.20
    authorship_diversity: 0.20
    merge_readiness: 0.20
    stability: 0.15

codebase_structure:
  core_modules: ["src/", "tests/", "config/"]
  weights:
    directory_similarity: 0.30
    file_additions: 0.25
    core_stability: 0.25
    namespace_isolation: 0.20

diff_distance:
  estimated_codebase_size: 5000
  max_expected_files: 50
  weights:
    code_churn: 0.30
    concentration: 0.25
    complexity: 0.25
    risk: 0.20
  risky_patterns:
    critical: ["config/", "core/", "__init__.py"]
    high: ["tests/", "requirements.txt"]
    medium: ["src/", "lib/"]
    low: ["docs/", "examples/"]

clustering:
  method: "hierarchical_agglomerative"
  linkage: "ward"
  distance_metric: "euclidean"
  threshold: 0.5

assignment:
  heuristic_threshold: 0.95
  affinity_threshold: 0.70
  consensus_threshold: 0.60
  default_target: "main"
  default_confidence: 0.65

framework:
  cache_enabled: true
  cache_dir: ".taskmaster/cache/"
  cache_retention_days: 7
  parallel_enabled: true
  max_workers: 4
  output_dir: ".taskmaster/outputs/"
  verbose_logging: false
```

---

## Typical Development Workflow

1. Create `clustering_framework.py` with `__init__` and `run()` — verify full pipeline executes
2. Add `analyze_branch()` and `get_branch_tags()` — verify single-branch path
3. Add `export_outputs()` — verify all files generated with correct paths
4. Create `downstream_bridges.py` — implement all 4 bridges
5. Test each bridge with known tag sets against mapping tables
6. Create `config_manager.py` — load YAML, validate, provide defaults
7. Create `deployment_validator.py` — implement all validation methods
8. Assemble package structure (move files, create `__init__.py` files)
9. Run `verify_system_integration()` pseudocode end-to-end
10. Run full test suite (`pytest tests/`) — all must pass
11. Generate validation report
12. Tag version 1.0.0

---

## Integration Handoff

### For Task 79 (Execution Context)
- Call `get_execution_context_for_branch(branch_name)` to get parallelizable flag, priority, and resource hints
- Tags `orchestration-branch` and `core-feature` force serial execution

### For Task 80 (Validation Intensity)
- Call `get_test_intensity_for_branch(branch_name)` → returns "high", "medium", or "low"
- Based on `complex`/`high-risk`/`moderate`/`medium-risk` tags

### For Task 83 (Test Suite Selection)
- Call `get_test_suites_for_branch(branch_name)` → returns list of suite names
- `testing-required-high` → full suite; `testing-optional` → smoke only
- Additional suites appended for `orchestration-branch`, `security-sensitive`, `api-changes`

### For Task 101 (Orchestration Filtering)
- Call `passes_orchestration_filter(branch_name)` → boolean
- Only `orchestration-branch` and `devops` tags pass the filter

---

## Common Gotchas & Solutions

**Gotcha 1: Circular imports between framework and bridges**
```python
# WRONG: downstream_bridges.py imports BranchClusteringFramework at module level
# RIGHT: Pass framework instance as parameter or use lazy imports
def get_execution_context_for_branch(framework, branch_name: str) -> dict:
    tags = framework.get_branch_tags(branch_name)
    ...
```

**Gotcha 2: Config file not found at runtime**
```python
# WRONG: Hardcoded path to clustering_config.yaml
# RIGHT: Search multiple locations with fallback
config_paths = [
    config_path,
    os.path.join(os.getcwd(), "clustering_config.yaml"),
    os.path.join(os.path.dirname(__file__), "config", "clustering_config.yaml")
]
```

**Gotcha 3: Missing tags for downstream compatibility**
```python
# WRONG: Assuming all branches have all tag categories
# RIGHT: validate_downstream_compatibility() checks for missing tag categories
required_categories = {"risk", "complexity", "testing", "scope"}
for branch in results:
    tag_categories = {categorize(t) for t in branch['tags']}
    missing = required_categories - tag_categories
    if missing:
        issues.append(f"{branch['name']} missing: {missing}")
```

**Gotcha 4: YAML config type coercion**
```python
# WRONG: threshold loaded as string "0.5" instead of float
# RIGHT: Validate types after loading
config = yaml.safe_load(f)
assert isinstance(config['clustering']['threshold'], (int, float))
```

**Gotcha 5: Package __init__.py missing re-exports**
```python
# WRONG: from clustering import BranchClusteringFramework fails
# RIGHT: Explicitly export in __init__.py
# clustering/__init__.py
from .clustering_framework import BranchClusteringFramework
from .downstream_bridges import (
    get_execution_context_for_branch,
    get_test_intensity_for_branch,
    get_test_suites_for_branch,
    passes_orchestration_filter
)
__all__ = ['BranchClusteringFramework', ...]
```

---

## Integration Checkpoint

**When to declare Task 002 complete:**

- [ ] All 5 sub-subtasks complete (002.9.1-002.9.5)
- [ ] `BranchClusteringFramework` runs full pipeline end-to-end
- [ ] All 4 downstream bridges return correct values
- [ ] Configuration loads from YAML and validates
- [ ] `DeploymentValidator` passes all checks
- [ ] Package structure matches specification
- [ ] `from clustering import BranchClusteringFramework` works
- [ ] All tests pass (`pytest tests/` exits 0)
- [ ] Performance: 13 branches < 2 minutes
- [ ] All downstream compatibility checks pass
- [ ] Code review approved
- [ ] Commit message: "feat: complete Task 002.9 FrameworkIntegration"

---

## Done Definition

Task 002.9 is done when:

1. All 5 sub-subtasks marked complete
2. `BranchClusteringFramework` public API fully functional (all 6 methods)
3. All 4 downstream bridges tested with sample tags
4. Configuration system loads, validates, and provides defaults
5. Deployment validation passes all checks
6. Package structure matches specification directory tree
7. Full integration verification pseudocode runs without assertion errors
8. All deliverables present:
   - `clustering_framework.py`
   - `downstream_bridges.py`
   - `config_manager.py`
   - `deployment_validator.py`
   - `clustering_config.yaml`
   - Complete package with `__init__.py` files
   - Validation report
   - Version tag 1.0.0
9. Code review approved
10. Task 002 (Branch Clustering System) declared complete

---

## Provenance

**Source:** HANDOFF_75.9_FrameworkIntegration
**Original Task ID:** 75.9
**Migrated To:** 002.9
**Migration Date:** 2026-01-29
**Consolidation:** All content from HANDOFF (Parts 1-8: Framework, Bridges, Config, Docs, Validation, Package, Integration, Success Criteria) preserved in 14-section standard format

---

## Next Steps

1. **Immediate:** Begin with sub-subtask 002.9.1 (Design Framework Architecture and Public API)
2. **Week 1:** Complete all 8 sub-subtasks with proper framework integration
3. **Week 1-2:** Implement downstream bridges for Tasks 79, 80, 83, 101
4. **Week 2:** Create comprehensive configuration management system
5. **Week 2:** Write documentation for all 6 documentation components
6. **Week 2-3:** Performance validation and deployment packaging
7. **Week 3:** Code review and final validation
8. **Upon completion:** Task 002 (Branch Clustering System) declared complete
9. **Parallel tasks:** Any downstream tasks can now begin implementation
