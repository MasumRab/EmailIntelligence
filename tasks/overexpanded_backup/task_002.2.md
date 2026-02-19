# Task 002.2: CodebaseStructureAnalyzer

**Status:** pending
**Priority:** high
**Effort:** 28-36 hours
**Complexity:** 8/10
**Dependencies:** None

---

## Overview/Purpose

Analyze the file structure and code organization of each feature branch to fingerprint its architectural characteristics.

---

## Quick Navigation

Navigate this document using these links:

- [Overview/Purpose](#overview/purpose)
- [Success Criteria](#success-criteria)
- [Prerequisites & Dependencies](#prerequisites--dependencies)
- [Sub-subtasks Breakdown](#sub-subtasks-breakdown)
- [Specification Details](#specification-details)
- [Implementation Guide](#implementation-guide)
- [Configuration & Defaults](#configuration--defaults)
- [Typical Development Workflow](#typical-development-workflow)
- [Integration Handoff](#integration-handoff)
- [Common Gotchas & Solutions](#common-gotchas--solutions)
- [Subtasks Overview](#subtasks-overview)
- [Integration Checkpoint](#integration-checkpoint)
- [Done Definition](#done-definition)

**Pro tip:** Use Ctrl+F to search within sections, or click links above to jump directly

---

## Success Criteria

- [ ] Module fingerprints directory structure
- [ ] Detects language and framework usage
- [ ] Maps import dependencies between modules
- [ ] Generates comparison scores against targets
- [ ] Unit tests cover structural analysis

---

<!-- IMPORTED_FROM: backup_task75/task-002.2.md -->
Task 002.2 is complete when:

**Core Functionality:**
- [ ] `CodebaseStructureAnalyzer` class accepts `repo_path` (str) and `branch_name` (str)
- [ ] Maps directory/file structure for target branch vs. main
- [ ] Computes 4 normalized metrics in [0,1] range
- [ ] Returns properly formatted dict with aggregate similarity score
- [ ] Handles all specified edge cases (empty branches, deletion-heavy branches)
- [ ] Output matches JSON schema exactly

**Performance Targets:**
- [ ] Directory tree extraction: **< 1 second** (on typical repository)
- [ ] Jaccard similarity calculation: **< 0.5 seconds** (for 1000+ directory comparison)
- [ ] Memory usage: **< 50 MB** per operation
- [ ] Handles **repositories with 10,000+ commits** without failure
- [ ] Directory similarity calculation: **O(n log n)** where n = number of directories
- [ ] Overall analysis: **< 2 seconds max**

**Quality Assurance:**
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

**Integration Readiness:**
- [ ] Compatible with Task 002.4 (BranchClusterer) input requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] No external prerequisites

### Blocks (What This Task Unblocks)
- [ ] No specific blocks defined

### External Dependencies
- [ ] No external dependencies

## Subtasks Overview

### Dependency Flow Diagram

```
TASK 002.2.1 (2-3h) ──────┐
[Design Structure Analysis] │
                           ├─→ TASK 002.2.2 (3-4h) ──────┐
                           │  [Git Tree Extraction]        │
                           │                              ├─→ TASKS 002.2.3-002.2.6 (parallel) ────┐
                           │                              │   [Metrics Implementation]              │
                           │                              │                                       ├─→ TASK 002.2.7 (2-3h)
                           └──────────────────────────────┘                                       │  [Aggregate & Format]
                                                                                                │
                                                                                                └─→ TASK 002.2.8 (3-4h)
                                                                                                   [Unit Tests]

Critical Path: TASK 002.2.1 → TASK 002.2.2 → TASKS 002.2.3-002.2.6 (parallel) → TASK 002.2.7 → TASK 002.2.8
Minimum Duration: 12-16 hours (with parallelization)
```

### Parallel Opportunities

**Can run in parallel (after TASK 002.2.2):**
- TASK 002.2.3: Implement Directory Similarity Metric
- TASK 002.2.4: Implement File Addition Metric
- TASK 002.2.5: Implement Core Module Stability Metric
- TASK 002.2.6: Implement Namespace Isolation Metric

All tasks depend only on [parent task] and are independent of each other. **Estimated parallel execution saves 6-8 hours.**

**Must be sequential:**
- TASK 002.2.1 → TASK 002.2.2 (need architecture before extraction)
- TASK 002.2.2 → TASKS 002.2.3-002.2.6 (need extraction before metrics)
- TASKS 002.2.3-002.2.6 → TASK 002.2.7 (need metrics before aggregation)
- TASK 002.2.7 → TASK 002.2.8 (need aggregation before testing)

### Timeline with Parallelization

**Days 1-2: [First Phase] (TASK 002.2.1-TASK 002.2.2)**
- TASK 002.2.1: Design Structure Analysis Architecture
- TASK 002.2.2: Implement Git Tree Extraction

**Days 2-3: [Parallel Phase] (TASKS 002.2.3-002.2.6 in parallel)**
- Days 2-3: TASK 002.2.3 + TASK 002.2.4 (2 people)
- Days 2-3: TASK 002.2.5 + TASK 002.2.6 (2 people)

**Days 3-4: [Integration Phase] (TASKS 002.2.7-002.2.8)**
- Day 3: TASK 002.2.7 (Aggregate & Output Formatting)
- Day 4: TASK 002.2.8 (Write Unit Tests)

---

## Sub-subtasks Breakdown

### 002.2.1: Design Structure Analysis Architecture
**Purpose:** Define how structure metrics will be calculated and combined
**Effort:** 3-4 hours

**Steps:**
1. Define the 4 core metrics with mathematical formulas
2. Document calculation approach for each metric
3. Create normalization strategy (ensure all metrics in [0,1] range)
4. Create weighting scheme: 0.30/0.25/0.25/0.20 (sum = 1.0)
5. Document edge case handling for each metric

**Success Criteria:**
- [ ] All 4 metrics clearly defined with formulas
- [ ] Calculation approach specified
- [ ] Normalization approach specified
- [ ] Weights documented
- [ ] Edge case handling documented

**Blocks:** 002.2.2, 002.2.3, 002.2.4, 002.2.5

---

### 002.2.2: Set Up Git Structure Extraction
**Purpose:** Create functions to extract directory/file structure from git repository
**Effort:** 4-5 hours
**Depends on:** 002.2.1

**Steps:**
1. Create utility functions for git command execution
2. Implement branch validation (check if branch exists)
3. Create directory tree extraction (get all directories/files on branch)
4. Create structure metadata extraction (types, hierarchy)
5. Add error handling (invalid branch, repo not found, git errors)

**Success Criteria:**
- [ ] Can execute git commands without errors
- [ ] Validates branch existence before processing
- [ ] Extracts directory/file structure with metadata
- [ ] Handles non-existent branches gracefully
- [ ] Returns structured data (sets of directories/files)

**Blocks:** 002.2.3, 002.2.4, 002.2.5

---

### 002.2.3: Implement Directory Similarity Metric
**Purpose:** Score how similar the branch's directory structure is to main
**Effort:** 3-4 hours
**Depends on:** 002.2.1, 002.2.2

**Steps:**
1. Extract directory sets from both main and branch
2. Calculate Jaccard similarity (intersection over union)
3. Define similarity baseline and scoring
4. Normalize to 0-1 range
5. Test with similar and different directory structures

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Identical structures score = 1.0
- [ ] Completely different structures score = 0.0
- [ ] Correctly handles single-directory branches
- [ ] Consistent calculation across test cases

---

### 002.2.4: Implement File Addition & Core Module Metrics
**Purpose:** Score new file additions and core module stability
**Effort:** 4-5 hours
**Depends on:** 002.2.1, 002.2.2

**Steps for file_additions:**
1. Extract file list from branch
2. Compare with main to identify new files
3. Calculate addition ratio (new files / total files)
4. Invert to score (fewer additions = higher score)
5. Normalize to 0-1 range

**Steps for core_module_stability:**
1. Define core modules list (configurable)
2. Check for core module deletions
3. Count modifications to core files
4. Apply penalties for changes
5. Return stability score

**Success Criteria:**
- [ ] File additions: Returns value in [0, 1] range
- [ ] File additions: No new files scores = 1.0, many additions score lower
- [ ] Core stability: Returns value in [0, 1] range
- [ ] Core stability: Deleted modules score ~0.5, preserved score ~1.0
- [ ] Handles edge cases (binary files, deletions)

---

### 002.2.5: Implement Namespace Isolation Metric
**Purpose:** Score how isolated new files are in their directory placement
**Effort:** 3-4 hours
**Depends on:** 002.2.1, 002.2.2

**Steps:**
1. Identify new files in branch
2. Group by directory prefix
3. Calculate isolation coefficient (grouped vs scattered)
4. Define isolation baseline (grouped = higher score)
5. Normalize to 0-1 range

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Grouped files (same directory) score higher than scattered
- [ ] Identifies namespace patterns correctly
- [ ] Handles single file additions
- [ ] Consistent scoring across test cases

---

### 002.2.6: Aggregate Metrics & Output Formatting
**Purpose:** Combine 4 metrics into single score and format output
**Effort:** 2-3 hours
**Depends on:** 002.2.3, 002.2.4, 002.2.5

**Steps:**
1. Define metric weights (sum to 1.0)
2. Create aggregation function (weighted sum)
3. Verify all metrics in [0,1] before aggregating
4. Format output dict (branch name, metrics dict, aggregate score, metadata)
5. Add timestamp

**Success Criteria:**
- [ ] Aggregate score = 0.30*m1 + 0.25*m2 + 0.25*m3 + 0.20*m4
- [ ] Returns value in [0, 1] range
- [ ] Output dict has all required fields
- [ ] Timestamp in ISO format
- [ ] No missing or extra fields

---

### 002.2.7: Write Unit Tests
**Purpose:** Verify CodebaseStructureAnalyzer works correctly
**Effort:** 3-4 hours
**Depends on:** 002.2.6

**Steps:**
1. Create test fixtures with various branch characteristics
2. Implement minimum 8 test cases
3. Implement mocking for git commands
4. Add performance tests
5. Generate coverage report (>95%)

**Success Criteria:**
- [ ] Minimum 8 comprehensive test cases
- [ ] All tests pass on CI/CD
- [ ] Code coverage >95%
- [ ] Edge cases covered
- [ ] Error handling tested
- [ ] Output validation includes JSON schema
- [ ] Performance tests meet <2 second requirement

---

### 002.2.8: Performance Optimization
**Purpose:** Optimize for large repositories and many files
**Effort:** 2-3 hours
**Depends on:** 002.2.7

**Steps:**
1. Profile current implementation
2. Identify bottlenecks in git operations
3. Optimize directory structure extraction
4. Add caching for repeated operations
5. Validate performance targets met

**Success Criteria:**
- [ ] Single branch analysis <2 seconds
- [ ] Memory usage <50MB per analysis
- [ ] Handles repositories with 10,000+ files
- [ ] No performance degradation with large inputs
- [ ] All tests still pass after optimization

---

## Specification Details

### Task Interface
- **ID**: 002.2
- **Title**: CodebaseStructureAnalyzer
- **Status**: pending
- **Priority**: high
- **Effort**: 28-36 hours
- **Complexity**: 8/10

### Requirements
**Core Requirements:**
- Python 3.8+ runtime environment
- Git installed and accessible from command line
- Access to local git repository with feature branches
- GitPython library or subprocess access for git commands
- YAML parser for configuration files

**Functional Requirements:**
- Must accept repository path and branch name as input parameters
- Must extract directory/file structure using git ls-tree commands
- Must compute 4 specific metrics with normalized values in [0,1] range
- Must return structured output matching JSON schema specification
- Must handle edge cases (non-existent branches, empty directories, binary files)

**Non-functional Requirements:**
- Performance: Complete analysis in under 2 seconds per branch
- Reliability: Handle all error conditions gracefully without crashing
- Scalability: Support repositories with up to 10,000+ files
- Maintainability: Follow PEP 8 standards with comprehensive docstrings
- Testability: Achieve >95% code coverage with unit tests

### Dependencies

**Blocked by:**
- [ ] Task 001 (project setup) - if applicable
- [ ] Development environment configured

**Blocks:**
- [ ] Task 002.4 (BranchClusterer) - requires output from this task
- [ ] Task 002.6 (PipelineIntegration) - depends on analyzer outputs

### Requirements

**Core Requirements:**
- Python 3.8+ runtime environment
- Git installed and accessible from command line
- Access to local git repository with feature branches
- GitPython library or subprocess access for git commands
- YAML parser for configuration files

**Functional Requirements:**
- Must accept repository path and branch name as input parameters
- Must extract directory/file structure using git ls-tree commands
- Must compute 4 specific metrics with normalized values in [0,1] range
- Must return structured output matching JSON schema specification
- Must handle edge cases (non-existent branches, empty directories, binary files)

**Non-functional Requirements:**
- Performance: Complete analysis in under 2 seconds per branch
- Reliability: Handle all error conditions gracefully without crashing
- Scalability: Support repositories with up to 10,000+ files
- Maintainability: Follow PEP 8 standards with comprehensive docstrings
- Testability: Achieve >95% code coverage with unit tests

## Implementation Guide

### Phase 1: Setup and Architecture (Days 1-2)
1. Create the basic class structure for `CodebaseStructureAnalyzer`
2. Implement repository validation and initialization
3. Set up configuration loading from YAML
4. Create the basic method signatures

### Phase 2: Git Structure Extraction (Days 2-3)
1. Implement git command execution with proper error handling
2. Extract directory/file structure using `git ls-tree` commands
3. Parse structure metadata (file types, directory hierarchy)
4. Handle edge cases (non-existent branches, binary files, large repos)

### Phase 3: Metric Implementation (Days 3-5)
1. Implement the 4 core metrics:
   - Directory similarity metric (Jaccard similarity of directory trees)
   - File additions metric (ratio of new files added)
   - Core module stability metric (preservation of critical modules)
   - Namespace isolation metric (grouping of new files in directories)
2. Ensure all metrics return values in [0,1] range
3. Add proper normalization and bounds checking

### Phase 4: Integration and Testing (Days 5-6)
1. Integrate all metrics into a weighted aggregation function
2. Format output according to specification
3. Write comprehensive unit tests (8+ test cases)
4. Perform performance testing to ensure <2s execution time

### Key Implementation Notes:
- Use subprocess with timeout for git commands to prevent hanging
- Implement proper error handling for all edge cases
- Ensure all metrics are normalized to [0,1] range
- Follow the configuration parameters specified in the Configuration section
- Add comprehensive logging and error reporting

<!-- IMPORTED_FROM: /home/masum/github/PR/.taskmaster/enhanced_improved_tasks/task-002-2.md -->

<!-- IMPORTED_FROM: /home/masum/github/PR/.taskmaster/task_data/archived/backups_archive_task002/task-002.2.md -->

# Task 002.2: CodebaseStructureAnalyzer

<!-- IMPORTED_FROM: /home/masum/github/PR/.taskmaster/task_data/archived/handoff_archive_task002/HANDOFF_002.2_CodebaseStructureAnalyzer.md -->

# Task 002.2: CodebaseStructureAnalyzer Implementation

## Quick Summary
Implement the `CodebaseStructureAnalyzer` class that measures codebase structure similarity between branches. This is a Stage One analyzer—no dependencies on other tasks in this batch.

**Effort:** 28-36 hours | **Complexity:** 7/10 | **Parallelizable:** Yes

---

## What to Build

A Python class `CodebaseStructureAnalyzer` that:
1. Maps directory/file structure for target branch vs. main
2. Computes 4 normalized metrics (0-1 scale)
3. Returns aggregated similarity score

### Class Signature
```python
class CodebaseStructureAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main")
    def analyze(self, branch_name: str) -> dict
```

---

## Metrics to Compute

| Metric | Weight | Description |
|--------|--------|-------------|
| `directory_similarity` | 30% | Jaccard similarity of directory trees (normalized 0-1) |
| `file_additions` | 25% | Ratio of new files added (capped at 1.0, then inverted: 1 - ratio) |
| `core_module_stability` | 25% | Preservation of core modules (src/*, tests/*, config) |
| `namespace_isolation` | 20% | Isolation score for new packages (files grouped by directory) |

All metrics normalized to `[0, 1]`.

---

## Input/Output Specification

### Input
- `branch_name` (str): Full branch name (e.g., "feature/auth-system")
- `repo_path` (str): Path to git repository

### Output (dict)
```json
{
  "branch_name": "feature/auth-system",
  "metrics": {
    "directory_similarity": 0.82,
    "file_additions": 0.68,
    "core_module_stability": 0.95,
    "namespace_isolation": 0.71
  },
  "aggregate_score": 0.794,
  "directory_count": 23,
  "file_count": 156,
  "new_files": 14,
  "modified_files": 28,
  "analysis_timestamp": "2025-12-22T10:35:00Z"
}
```

---

## Git Commands Reference

```bash
# Get full directory tree for branch
git ls-tree -r --name-only BRANCH_NAME

# Get full directory tree for main
git ls-tree -r --name-only main

# Get file changes between branches
git diff main...BRANCH_NAME --name-status

# Get file list by type (added/modified/deleted)
git diff main...BRANCH_NAME --diff-filter=A --name-only  # Added
git diff main...BRANCH_NAME --diff-filter=M --name-only  # Modified
git diff main...BRANCH_NAME --diff-filter=D --name-only  # Deleted
```

---

## Implementation Checklist

- [ ] Extract directory tree for both main and branch
- [ ] Implement Jaccard similarity for directory trees
- [ ] Calculate file addition ratio (new files / total files)
- [ ] Identify core modules (hardcoded list: src, tests, config, etc.)
- [ ] Check core module stability (no deletions, minimal additions)
- [ ] Calculate namespace isolation (clustering of new files)
- [ ] Normalize metrics to [0, 1]
- [ ] Weight and aggregate metrics
- [ ] Handle edge cases: empty branch, branch with only deletions
- [ ] Return dict matching output spec exactly
- [ ] Add docstrings (Google style)

---

## Core Modules List (Configurable)

```python
CORE_MODULES = [
    "src/",
    "tests/",
    "config/",
    "build/",
    "dist/",
    "requirements.txt",
    "setup.py",
    "pyproject.toml"
]
```

---

## Test Cases

1. **Minor feature branch**: 3 new files in `src/features/`, no core changes
2. **Refactoring branch**: 50% of files modified, directory structure preserved
3. **Large new module**: 20 new files in `src/orchestration/`, new directory
4. **Core rewrite**: Changes to `src/core/`, potential stability issue
5. **Deletion-heavy**: Removes files from main, should lower score

---

## Dependencies

- Python built-in `os` and `pathlib` for path operations
- `GitPython` or subprocess for git calls
- No internal dependencies on other Task 002.x components
- Output feeds into **Task 002.4 (BranchClusterer)**

---

## Configuration

Accept these parameters in `__init__` or config file:

```python
DIRECTORY_SIMILARITY_WEIGHT = 0.30
FILE_ADDITIONS_WEIGHT = 0.25
CORE_MODULE_STABILITY_WEIGHT = 0.25
NAMESPACE_ISOLATION_WEIGHT = 0.20
CORE_MODULES = ["src/", "tests/", "config/", ...]
MAX_NEW_FILES_RATIO = 0.50  # Warn if > 50% new files
```

---

## Algorithm Details

### Directory Similarity (Jaccard)
```
dirs_main = set of all directories in main
dirs_branch = set of all directories in branch
similarity = |intersection| / |union|
```

### File Additions
```
new_files = files added (git diff filter=A)
total_files_branch = total files in branch
addition_ratio = new_files / total_files_branch
metric = max(0, 1 - addition_ratio)  # Invert: fewer additions = higher score
```

### Core Module Stability
```
If any core module is deleted: score = 0.5
If core module files modified: apply penalty (0.1 per 5 modifications)
Else: score = 1.0 (high stability)
```

### Namespace Isolation
```
Group new files by directory prefix
Calculate clustering coefficient (0-1)
Isolated = files clustered in few directories, not scattered
```

---

## Next Steps After Completion

1. Unit test with 5+ branch fixtures
2. Integration test with real repo
3. Verify metrics sum to 0-1 range
4. Pass output to Task 002.4 integration point
5. Cross-check directory similarity with known repos

**Parallel tasks ready:** 002.1, 002.3 (no dependencies)

## Purpose
Create a reusable Python class that measures codebase structure similarity between branches. This is a Stage One analyzer with no dependencies on other tasks in this batch.

**Scope:** CodebaseStructureAnalyzer class only  
**Effort:** 28-36 hours | **Complexity:** 7/10  
**Status:** Ready for implementation  
**No dependencies** - can start immediately (parallel with 002.1, 002.3)

---

## Success Criteria

Task 002.2 is complete when:

**Core Functionality:**
- [ ] `CodebaseStructureAnalyzer` class accepts `repo_path` (str) and `branch_name` (str)
- [ ] Maps directory/file structure for target branch vs. main
- [ ] Computes 4 normalized metrics in [0,1] range
- [ ] Returns properly formatted dict with aggregate similarity score
- [ ] Handles all specified edge cases (empty branches, deletion-heavy branches)
- [ ] Output matches JSON schema exactly

**Quality Assurance:**
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <2 seconds per branch analysis
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

**Integration Readiness:**
- [ ] Compatible with Task 002.4 (BranchClusterer) input requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Metrics to Compute

| Metric | Weight | Description |
|--------|--------|-------------|
| `directory_similarity` | 30% | Jaccard similarity of directory trees |
| `file_additions` | 25% | Ratio of new files added (capped, inverted) |
| `core_module_stability` | 25% | Preservation of core modules |
| `namespace_isolation` | 20% | Isolation score for new packages |

All metrics normalized to [0, 1].

---

## Output Specification

```json
{
  "branch_name": "feature/auth-system",
  "metrics": {
    "directory_similarity": 0.82,
    "file_additions": 0.68,
    "core_module_stability": 0.95,
    "namespace_isolation": 0.71
  },
  "aggregate_score": 0.794,
  "directory_count": 23,
  "file_count": 156,
  "new_files": 14,
  "modified_files": 28,
  "analysis_timestamp": "2025-12-22T10:35:00Z"
}
```

---

## Subtasks

### 002.2.1: Design Structure Analysis Architecture
**Purpose:** Define similarity metrics and analysis approach  
**Effort:** 2-3 hours

**Steps:**
1. Design directory tree comparison logic
2. Define Jaccard similarity calculation
3. Document file addition scoring
4. Define core modules list
5. Design namespace isolation metric

**Success Criteria:**
- [ ] All metrics mathematically defined
- [ ] Calculation approach documented
- [ ] Core modules list specified
- [ ] Edge cases identified

---

### 002.2.2: Implement Git Tree Extraction
**Purpose:** Extract directory and file structure from git  
**Effort:** 3-4 hours

**Steps:**
1. Implement `git ls-tree` command execution
2. Extract directory tree for main branch
3. Extract directory tree for target branch
4. Parse output into structured format
5. Add error handling for invalid branches

**Success Criteria:**
- [ ] Extracts directory lists without error
- [ ] Returns structured data (lists of files/dirs)
- [ ] Handles non-existent branches
- [ ] Performance: <1 second per extraction

---

### 002.2.3: Implement Directory Similarity Metric
**Purpose:** Compute Jaccard similarity of directory trees  
**Effort:** 3-4 hours

**Steps:**
1. Extract directory sets from both branches
2. Implement Jaccard similarity formula
3. Normalize to [0,1] range
4. Test with various branch types
5. Document calculation approach

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Identical trees score = 1.0
- [ ] Completely different trees score = 0.0
- [ ] Calculation verified with test cases

---

### 002.2.4: Implement File Addition Metric
**Purpose:** Score ratio of new files added  
**Effort:** 3-4 hours

**Steps:**
1. Extract file changes using `git diff`
2. Identify newly added files
3. Calculate addition ratio
4. Invert to score (fewer additions = higher score)
5. Cap at 1.0 and normalize

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] No new files scores = 1.0
- [ ] 100% new files scores = 0.0
- [ ] Handles edge cases (empty repos)

---

### 002.2.5: Implement Core Module Stability Metric
**Purpose:** Preserve core modules (src/*, tests/*, config)  
**Effort:** 3-4 hours

**Steps:**
1. Define core modules list (configurable)
2. Check for core module deletions
3. Count modifications to core files
4. Apply penalties for changes
5. Return stability score

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Deleted core modules: score = 0.5
- [ ] No changes to core: score = 1.0
- [ ] Identifies all core module types

---

### 002.2.6: Implement Namespace Isolation Metric
**Purpose:** Score isolation of new packages/directories  
**Effort:** 3-4 hours

**Steps:**
1. Identify new files
2. Group by directory prefix
3. Calculate clustering coefficient
4. Score isolation (grouped = higher)
5. Normalize to [0,1]

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Grouped files score higher than scattered
- [ ] Identifies namespace patterns
- [ ] Handles single file additions

---

### 002.2.7: Aggregate Metrics & Output Formatting
**Purpose:** Combine metrics and format output  
**Effort:** 2-3 hours

**Steps:**
1. Define metric weights (sum to 1.0)
2. Create aggregation function
3. Verify all metrics in [0,1]
4. Format output dict with all required fields
5. Validate against JSON schema

**Success Criteria:**
- [ ] Aggregate score = weighted sum of metrics
- [ ] Returns value in [0, 1] range
- [ ] Output has all required fields
- [ ] Schema validation passes

---

### 002.2.8: Write Unit Tests
**Purpose:** Comprehensive test coverage  
**Effort:** 3-4 hours

**Steps:**
1. Create test fixtures with various branch types
2. Implement 8+ test cases
3. Mock git commands for reliable testing
4. Add performance tests
5. Generate coverage report (>95%)

**Success Criteria:**
- [ ] 8+ test cases implemented
- [ ] All tests pass
- [ ] Code coverage >95%
- [ ] Edge cases covered
- [ ] Performance tests pass

---

## Configuration & Defaults

All parameters should be externalized to configuration files (not hardcoded). Use YAML format:

```yaml
# config/codebase_structure_analyzer.yaml
codebase_structure_analyzer:
  # Metric Weights
  directory_similarity_weight: 0.30  # Weight for directory similarity metric
  file_additions_weight: 0.25        # Weight for file additions metric
  core_module_stability_weight: 0.25 # Weight for core module stability metric
  namespace_isolation_weight: 0.20   # Weight for namespace isolation metric

  # Core Modules
  core_modules:                      # List of core module paths
    - "src/"
    - "tests/"
    - "config/"
    - "build/"
    - "dist/"
    - "requirements.txt"
    - "setup.py"
    - "pyproject.toml"

  # Thresholds
  max_new_files_ratio: 0.50          # Warn if > 50% new files
```

**How to use in code:**
```python
import yaml

def load_config(config_path='config/codebase_structure_analyzer.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)['codebase_structure_analyzer']

config = load_config()
DIRECTORY_SIMILARITY_WEIGHT = config['directory_similarity_weight']
FILE_ADDITIONS_WEIGHT = config['file_additions_weight']
CORE_MODULE_STABILITY_WEIGHT = config['core_module_stability_weight']
NAMESPACE_ISOLATION_WEIGHT = config['namespace_isolation_weight']
CORE_MODULES = config['core_modules']
MAX_NEW_FILES_RATIO = config['max_new_files_ratio']
```

**Why externalize?**
- Easy to tune without redeploying code
- Different configurations for different environments (dev/test/prod)
- Can adjust thresholds based on organizational needs
- No code recompilation needed to adjust parameters

---

## Git Commands Reference

```bash
# Get full directory tree for branch
git ls-tree -r --name-only BRANCH_NAME

# Get file changes between branches
git diff main...BRANCH_NAME --name-status

# Get added files
git diff main...BRANCH_NAME --diff-filter=A --name-only

# Get modified files
git diff main...BRANCH_NAME --diff-filter=M --name-only

# Get deleted files
git diff main...BRANCH_NAME --diff-filter=D --name-only
```

---

## Typical Development Workflow

Complete step-by-step git workflow for implementing this task. Copy-paste ready sequences:

### Setup Your Feature Branch

```bash
# 1. Create and push feature branch
git checkout -b feat/codebase-structure-analyzer
git push -u origin feat/codebase-structure-analyzer

# 2. Create directory structure
mkdir -p src/analyzers tests/analyzers
touch src/analyzers/__init__.py
git add src/analyzers/
git commit -m "chore: create analyzers module structure"
```

### Subtask 002.2.1: Design Structure Analysis Architecture

```bash
# Create initial module file
cat > src/analyzers/codebase_structure_analyzer.py << 'EOF'
"""
Codebase Structure Analyzer Module
"""
class CodebaseStructureAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main"):
        self.repo_path = repo_path
        self.main_branch = main_branch

    def analyze(self, branch_name: str) -> dict:
        """Analyze codebase structure and return metrics."""
        pass
EOF

git add src/analyzers/codebase_structure_analyzer.py
git commit -m "feat: implement CodebaseStructureAnalyzer skeleton (Task 002.2)"
```

### Subtask 002.2.2: Implement Git Tree Extraction

```bash
# Update the analyzer to implement git tree extraction
cat >> src/analyzers/codebase_structure_analyzer.py << 'EOF'

    def _extract_git_tree(self, branch_name: str) -> tuple[set, set]:
        """Extract directory and file trees for a branch."""
        import subprocess
        import os
        from pathlib import Path

        os.chdir(self.repo_path)

        # Get full directory tree for branch
        result = subprocess.run([
            "git", "ls-tree", "-r", "--name-only", branch_name
        ], capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            raise Exception(f"Git command failed: {result.stderr}")

        files = result.stdout.strip().split('\n')
        directories = {os.path.dirname(f) for f in files if os.path.dirname(f)}

        return directories, set(files)
EOF

git add src/analyzers/codebase_structure_analyzer.py
git commit -m "feat: implement git tree extraction for CodebaseStructureAnalyzer (Task 002.2.2)"
```

[Repeat for each major subtask]

### Final Steps

```bash
# Create configuration file
mkdir -p config
cat > config/codebase_structure_analyzer.yaml << 'EOF'
codebase_structure_analyzer:
  # Metric Weights
  directory_similarity_weight: 0.30  # Weight for directory similarity metric
  file_additions_weight: 0.25        # Weight for file additions metric
  core_module_stability_weight: 0.25 # Weight for core module stability metric
  namespace_isolation_weight: 0.20   # Weight for namespace isolation metric

  # Core Modules
  core_modules:                      # List of core module paths
    - "src/"
    - "tests/"
    - "config/"
    - "build/"
    - "dist/"
    - "requirements.txt"
    - "setup.py"
    - "pyproject.toml"

  # Thresholds
  max_new_files_ratio: 0.50          # Warn if > 50% new files
EOF

git add config/
git commit -m "config: CodebaseStructureAnalyzer configuration parameters"

# Push to origin
git push origin feat/codebase-structure-analyzer

# Create pull request
gh pr create --title "Complete Task 002.2: CodebaseStructureAnalyzer" \
             --body "Implements CodebaseStructureAnalyzer with directory similarity, file additions, core module stability, and namespace isolation metrics"
```

---

## Integration Handoff

### What Gets Passed to Task 002.4 (Downstream Task)

**Task 002.4 expects input in this format:**

```python
from src.analyzers.codebase_structure_analyzer import CodebaseStructureAnalyzer

analyzer = CodebaseStructureAnalyzer(repo_path, main_branch)
result = analyzer.analyze(branch_name)

# result is a dict like:
# {
#   "branch_name": "feature/branch-name",
#   "metrics": {
#     "directory_similarity": 0.82,
#     "file_additions": 0.68,
#     "core_module_stability": 0.95,
#     "namespace_isolation": 0.71
#   },
#   "aggregate_score": 0.794,
#   "directory_count": 23,
#   "file_count": 156,
#   "new_files": 14,
#   "modified_files": 28,
#   "analysis_timestamp": "2025-12-22T10:35:00Z"
# }
```

**Task 002.4 uses these outputs by:**
1. Collects results from multiple analyzers (002.1, 002.2, 002.3)
2. Combines metrics using weighted approach (0.35×002.1 + 0.35×002.2 + 0.30×002.3)
3. Performs hierarchical clustering on combined metrics
4. Generates cluster assignments for each branch

**Validation before handoff:**
```bash
# Verify output matches specification
python -c "
from src.analyzers.codebase_structure_analyzer import CodebaseStructureAnalyzer
analyzer = CodebaseStructureAnalyzer('/path/to/repo')
result = analyzer.analyze('some-branch')

# Check required fields
assert 'branch_name' in result
assert 'metrics' in result
assert 'aggregate_score' in result

# Check value ranges/types
assert isinstance(result['aggregate_score'], float)
assert 0 <= result['aggregate_score'] <= 1

print('✓ Output valid and ready for Task 002.4')
"
```

---

## Common Gotchas & Solutions

### Gotcha 1: Git Command Timeout ⚠️

**Problem:** Git commands hang on large repositories with 10,000+ commits
**Symptom:** Process hangs for more than 30 seconds during git ls-tree
**Root Cause:** Git operations on very large repositories can take a long time

**Solution:** Add timeout to subprocess calls
```python
import subprocess
result = subprocess.run([
    "git", "ls-tree", "-r", "--name-only", branch_name
], capture_output=True, text=True, timeout=30)  # 30-second timeout
```

**Test:** Verify timeout handling works by testing with a temporarily large repository

---

### Gotcha 2: Directory vs File Path Confusion ⚠️

**Problem:** Mixing up directory paths with file paths in Jaccard similarity calculation
**Symptom:** Incorrect similarity scores due to comparing apples to oranges
**Root Cause:** Not properly separating directory structure from file structure

**Solution:** Explicitly separate directory and file operations
```python
def _extract_git_tree(self, branch_name: str) -> tuple[set, set]:
    """Extract directory and file trees for a branch."""
    # ... git command execution ...
    files = result.stdout.strip().split('\n')
    directories = {os.path.dirname(f) for f in files if os.path.dirname(f)}  # Only directories

    return directories, set(files)  # Return both separately
```

**Test:** Verify that directory similarity calculation only considers directory paths

---

### Gotcha 3: Core Module Pattern Matching ⚠️

**Problem:** Incorrectly identifying core modules due to fuzzy matching
**Symptom:** False positives or negatives in core module stability scoring
**Root Cause:** Using substring matching instead of path prefix matching

**Solution:** Use proper path prefix matching
```python
def _check_core_module_stability(self, files: set) -> float:
    """Check stability of core modules."""
    core_changes = 0
    for file in files:
        for core_pattern in CORE_MODULES:
            # Use path.startswith for accurate matching
            if file.startswith(core_pattern):
                core_changes += 1
                break  # Don't double-count
    # ... calculate stability score
```

**Test:** Verify that files like "src/utilities.py" match "src/" but "other_src/file.py" doesn't

---

### Gotcha 4: Memory Usage with Large Repositories ⚠️

**Problem:** High memory consumption when processing repositories with thousands of files
**Symptom:** Process killed by OS due to memory limits
**Root Cause:** Loading all file paths into memory at once

**Solution:** Process files in chunks or use generators
```python
def _process_large_repo(self, branch_name: str):
    """Process large repositories efficiently."""
    # Use git commands that output line by line
    # Process results incrementally instead of loading all at once
    # Consider using generators for memory efficiency
```

**Test:** Run on repositories of various sizes to ensure memory usage stays under 50MB

---

## Integration Checkpoint

**When to move to 002.4:**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification
- [ ] Accepts input from git repositories
- [ ] Ready for integration with other Stage One analyzers

---

## Done Definition

Task 002.2 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage)
3. Code review approved
4. Outputs match specification
5. Documentation complete
6. Ready for hand-off to Task 002.4

## Purpose

Analyze the file structure and code organization of each feature branch to fingerprint its architectural characteristics.

---

## Details

Implement a Python module that:
- Maps directory structure and file counts per branch
- Identifies language distribution (Python, JS, etc.)
- Detects module boundaries and import patterns
- Generates structural fingerprints for comparison
- Compares against known patterns for main/scientific/orchestration-tools

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Module fingerprints directory structure
- [ ] Detects language and framework usage
- [ ] Maps import dependencies between modules
- [ ] Generates comparison scores against targets
- [ ] Unit tests cover structural analysis

---

## Test Strategy

- Test with branches of varying complexity
- Verify structure detection accuracy
- Test import pattern extraction
- Validate comparison scoring

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation
**Priority:** high
**Effort:** 28-36 hours
**Complexity:** 8/10
**Dependencies:** None
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Analyze the file structure and code organization of each feature branch to fingerprint its architectural characteristics.

---

## Details

Implement a Python module that:
- Maps directory structure and file counts per branch
- Identifies language distribution (Python, JS, etc.)
- Detects module boundaries and import patterns
- Generates structural fingerprints for comparison
- Compares against known patterns for main/scientific/orchestration-tools

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Module fingerprints directory structure
- [ ] Detects language and framework usage
- [ ] Maps import dependencies between modules
- [ ] Generates comparison scores against targets
- [ ] Unit tests cover structural analysis

---

## Test Strategy

- Test with branches of varying complexity
- Verify structure detection accuracy
- Test import pattern extraction
- Validate comparison scoring

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation
**Dependencies:** None
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Analyze the file structure and code organization of each feature branch to fingerprint its architectural characteristics.

---

## Details

Implement a Python module that:
- Maps directory structure and file counts per branch
- Identifies language distribution (Python, JS, etc.)
- Detects module boundaries and import patterns
- Generates structural fingerprints for comparison
- Compares against known patterns for main/scientific/orchestration-tools

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Module fingerprints directory structure
- [ ] Detects language and framework usage
- [ ] Maps import dependencies between modules
- [ ] Generates comparison scores against targets
- [ ] Unit tests cover structural analysis

---

## Test Strategy

- Test with branches of varying complexity
- Verify structure detection accuracy
- Test import pattern extraction
- Validate comparison scoring

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation
**Effort:** TBD
**Complexity:** TBD

## Overview/Purpose
Implement a Python module that:
- Maps directory structure and file counts per branch
- Identifies language distribution (Python, JS, etc.)
- Detects module boundaries and import patterns
- Generates ...

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] None
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Analyze the file structure and code organization of each feature branch to fingerprint its architectural characteristics.

---

## Details

Implement a Python module that:
- Maps directory structure and file counts per branch
- Identifies language distribution (Python, JS, etc.)
- Detects module boundaries and import patterns
- Generates structural fingerprints for comparison
- Compares against known patterns for main/scientific/orchestration-tools

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Module fingerprints directory structure
- [ ] Detects language and framework usage
- [ ] Maps import dependencies between modules
- [ ] Generates comparison scores against targets
- [ ] Unit tests cover structural analysis

---

## Test Strategy

- Test with branches of varying complexity
- Verify structure detection accuracy
- Test import pattern extraction
- Validate comparison scoring

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation

### Blocks (What This Task Unblocks)
- [ ] None specified

### External Dependencies
- [ ] None

## Sub-subtasks Breakdown

# No subtasks defined

## Specification Details

### Task Interface
- **ID**: 
- **Title**: 
- **Status**: pending
**Priority:** high
**Effort:** 28-36 hours
**Complexity:** 8/10
**Dependencies:** None
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Analyze the file structure and code organization of each feature branch to fingerprint its architectural characteristics.

---

## Details

Implement a Python module that:
- Maps directory structure and file counts per branch
- Identifies language distribution (Python, JS, etc.)
- Detects module boundaries and import patterns
- Generates structural fingerprints for comparison
- Compares against known patterns for main/scientific/orchestration-tools

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Module fingerprints directory structure
- [ ] Detects language and framework usage
- [ ] Maps import dependencies between modules
- [ ] Generates comparison scores against targets
- [ ] Unit tests cover structural analysis

---

## Test Strategy

- Test with branches of varying complexity
- Verify structure detection accuracy
- Test import pattern extraction
- Validate comparison scoring

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation
- **Priority**: high
**Effort:** 28-36 hours
**Complexity:** 8/10
**Dependencies:** None
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Analyze the file structure and code organization of each feature branch to fingerprint its architectural characteristics.

---

## Details

Implement a Python module that:
- Maps directory structure and file counts per branch
- Identifies language distribution (Python, JS, etc.)
- Detects module boundaries and import patterns
- Generates structural fingerprints for comparison
- Compares against known patterns for main/scientific/orchestration-tools

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Module fingerprints directory structure
- [ ] Detects language and framework usage
- [ ] Maps import dependencies between modules
- [ ] Generates comparison scores against targets
- [ ] Unit tests cover structural analysis

---

## Test Strategy

- Test with branches of varying complexity
- Verify structure detection accuracy
- Test import pattern extraction
- Validate comparison scoring

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation
- **Effort**: N/A
- **Complexity**: N/A

## Implementation Guide

Implement a Python module that:
- Maps directory structure and file counts per branch
- Identifies language distribution (Python, JS, etc.)
- Detects module boundaries and import patterns
- Generates structural fingerprints for comparison
- Compares against known patterns for main/scientific/orchestration-tools

## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

## Performance Targets

- **Effort Range**: TBD
- **Complexity Level**: TBD

## Testing Strategy

### Unit Tests
- [ ] Tests cover core functionality
- [ ] Edge cases handled appropriately
- [ ] Performance benchmarks met

### Integration Tests
- [ ] Integration with dependent components verified
- [ ] End-to-end workflow tested
- [ ] Error handling verified

### Test Strategy Notes
- Test with branches of varying complexity
- Verify structure detection accuracy
- Test import pattern extraction
- Validate comparison scoring

## Common Gotchas & Solutions

- [ ] [Common issues and solutions to be documented]

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

## Done Definition

### Completion Criteria
- [ ] All success criteria checkboxes marked complete
- [ ] Code quality standards met (PEP 8, documentation)
- [ ] Performance targets achieved
- [ ] All subtasks completed
- [ ] Integration checkpoint criteria satisfied

## Next Steps

1. **Implementation Phase**: Begin with Phase 1 implementation focusing on class structure and architecture
2. **Unit Testing**: Develop comprehensive test suite with 8+ test cases covering all metrics
3. **Integration Testing**: Verify output compatibility with Task 002.4 (BranchClusterer) input requirements
4. **Performance Validation**: Confirm analysis completes in under 2 seconds per branch
5. **Code Review**: Submit for peer review ensuring PEP 8 compliance and comprehensive documentation
6. **Handoff Preparation**: Prepare for integration with Task 002.4 once implementation is complete
7. **Documentation**: Complete any remaining documentation gaps identified during implementation


<!-- EXTENDED_METADATA
END_EXTENDED_METADATA -->

## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

---

<!-- IMPORTED_FROM: backup_task75/task-002.2.md -->
- `DIRECTORY_SIMILARITY_WEIGHT` = 0.30
- `FILE_ADDITIONS_WEIGHT` = 0.25
- `CORE_MODULE_STABILITY_WEIGHT` = 0.25
- `NAMESPACE_ISOLATION_WEIGHT` = 0.20
- `CORE_MODULES` = ["src/", "tests/", "config/", ...]
- `MAX_NEW_FILES_RATIO` = 0.50

---

## Performance Targets

- **Effort Range**: 28-36 hours
- **Complexity Level**: 8/10

## Testing Strategy

### Unit Testing Approach
- **Minimum 8 test cases** covering all 4 metrics individually
- **Edge case testing** for new branches, empty directories, binary files
- **Performance testing** to ensure <2 second execution time
- **Code coverage** >95% across all functions and branches

### Test Cases to Implement

**Test Case 1: Normal Branch Analysis**
- Input: Branch with 156 files, 23 directories, 3 authors
- Expected: All metrics return values in [0,1], aggregate score calculated correctly
- Validation: Output matches JSON schema exactly

**Test Case 2: New Branch Analysis**
- Input: Branch with 2 files, 1 directory, 1 day old
- Expected: Appropriate scores for new branch (likely high isolation, low change metrics)
- Validation: No exceptions raised, proper handling of small datasets

**Test Case 3: Large Directory Structure**
- Input: Branch with 1000+ files, 100+ directories
- Expected: Performance under 2 seconds, no memory issues
- Validation: Proper timeout handling, memory usage <50MB

**Test Case 4: Binary File Branch**
- Input: Branch with binary files only
- Expected: Proper handling of binary files without errors
- Validation: Binary files filtered out gracefully

**Test Case 5: Non-existent Branch**
- Input: Branch name that doesn't exist
- Expected: Appropriate error handling without exception
- Validation: Returns error object or raises specific exception

**Test Case 6: Empty Directory Branch**
- Input: Branch with no files
- Expected: Proper handling of empty directory case
- Validation: No division-by-zero errors, valid output

**Test Case 7: Single File Branch**
- Input: Branch with only 1 file
- Expected: Proper handling of edge case for all metrics
- Validation: No calculation errors, valid output

**Test Case 8: High Directory Similarity**
- Input: Branch with structure nearly identical to main
- Expected: High directory similarity score (>0.9)
- Validation: Correctly identifies structural similarities

### Integration Testing
- Test with real repository fixtures
- Verify output compatibility with Task 002.4 (BranchClusterer)
- End-to-end pipeline validation
- Cross-validation with manual analysis

## Common Gotchas & Solutions

### Gotcha 1: Git Command Timeouts ⚠️
**Problem:** Git commands hang on large repositories with 10,000+ files
**Symptom:** Process hangs for more than 30 seconds during git ls-tree
**Root Cause:** Git operations on very large repositories can take a long time
**Solution:** Add timeout to subprocess calls
```python
import subprocess
result = subprocess.run([
    "git", "ls-tree", "-r", "--name-only", branch_name
], capture_output=True, text=True, timeout=30)  # 30-second timeout
```

### Gotcha 2: Directory Structure Parsing ⚠️
**Problem:** Directory parsing fails with unexpected formats
**Symptom:** ValueError when parsing directory structures
**Root Cause:** Git ls-tree output format varies depending on file types
**Solution:** Use robust directory parsing
```python
def parse_directory_structure(output):
    lines = output.strip().split('\n')
    directories = set()
    for line in lines:
        if line.strip():
            # Extract directory path from file path
            directory = '/'.join(line.split('/')[:-1])  # All but last element
            if directory:  # Only add non-empty directories
                directories.add(directory + '/')
    return directories
```

### Gotcha 3: Division by Zero ⚠️
**Problem:** Calculations fail when denominators are zero
**Symptom:** ZeroDivisionError during metric calculations
**Root Cause:** Not checking for zero values in denominators
**Solution:** Add checks for zero values
```python
def calculate_similarity(dirs_main, dirs_branch):
    intersection = len(dirs_main.intersection(dirs_branch))
    union = len(dirs_main.union(dirs_branch))
    if union == 0:
        return 0.0  # Prevent division by zero
    return intersection / union
```

### Gotcha 4: Bounds Checking for Metrics ⚠️
**Problem:** Metrics fall outside [0,1] range
**Symptom:** Values less than 0 or greater than 1 in metrics
**Root Cause:** Not clamping calculated values to valid range
**Solution:** Ensure all metrics are in [0,1] range
```python
def clamp(value, min_val=0, max_val=1):
    return max(min_val, min(max_val, value))

similarity_score = clamp(calculated_similarity)
```

### Gotcha 5: Binary Files in Directory Structure ⚠️
**Problem:** Binary files cause issues in structure analysis
**Symptom:** Errors when processing binary file paths
**Root Cause:** Binary files have different characteristics than text files
**Solution:** Filter out binary files during analysis
```python
def is_binary_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\x00' in chunk  # Null bytes typically indicate binary files
    except:
        return True  # If we can't read, assume binary to be safe
```

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

---

<!-- IMPORTED_FROM: backup_task75/task-002.2.md -->
**When to move to 002.4:**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification
- [ ] Accepts input from git repositories
- [ ] Ready for integration with other Stage One analyzers

---

## Done Definition

### Completion Criteria
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated

---

<!-- IMPORTED_FROM: backup_task75/task-002.2.md -->
Task 002.2 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage)
3. Code review approved
4. Outputs match specification
5. Documentation complete
6. Ready for hand-off to Task 002.4

## Next Steps

1. **Implementation Phase**: Begin with Phase 1 implementation focusing on class structure and architecture
2. **Unit Testing**: Develop comprehensive test suite with 8+ test cases covering all metrics
3. **Integration Testing**: Verify output compatibility with Task 002.4 (BranchClusterer) input requirements
4. **Performance Validation**: Confirm analysis completes in under 2 seconds per branch
5. **Code Review**: Submit for peer review ensuring PEP 8 compliance and comprehensive documentation
6. **Handoff Preparation**: Prepare for integration with Task 002.4 once implementation is complete
7. **Documentation**: Complete any remaining documentation gaps identified during implementation
