# Task 75.2: CodebaseStructureAnalyzer

## Purpose
Create a reusable Python class that measures codebase structure similarity between branches. This is a Stage One analyzer with no dependencies on other tasks in this batch.

**Scope:** CodebaseStructureAnalyzer class only  
**Effort:** 28-36 hours | **Complexity:** 7/10  
**Status:** Ready for implementation  
**No dependencies** - can start immediately (parallel with 75.1, 75.3)

---

## Developer Quick Reference

### What to Build
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

### Metrics Overview
| Metric | Weight | Calculation |
|--------|--------|-------------|
| `directory_similarity` | 30% | Jaccard: \|intersection\| / \|union\| of directory sets |
| `file_additions` | 25% | Inverted: 1 - (new_files / total_files) |
| `core_module_stability` | 25% | Penalty-based: 1.0 if no changes, 0.5 if deleted |
| `namespace_isolation` | 20% | Clustering: files grouped in few dirs = higher |

**See HANDOFF_75.2_CodebaseStructureAnalyzer.md for full implementation guide.**

---

## Success Criteria

Task 75.2 is complete when:

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
- [ ] Compatible with Task 75.4 (BranchClusterer) input requirements
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

### 75.2.1: Design Structure Analysis Architecture
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

### Implementation Checklist (From HANDOFF)
- [ ] Define Jaccard similarity: |intersection| / |union| of directory sets
- [ ] Document file addition scoring: 1 - (new_files / total_files)
- [ ] Define core modules list (src/, tests/, config/, build/, dist/, etc.)
- [ ] Document core module stability: 1.0 if no changes, 0.5 if deleted
- [ ] Design namespace isolation: clustering coefficient for new files

---

### 75.2.2: Implement Git Tree Extraction
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

### Implementation Checklist (From HANDOFF)
- [ ] Use subprocess with timeout for git commands
- [ ] Implement `git ls-tree -r --name-only BRANCH_NAME` execution
- [ ] Extract both main and target branch directory trees
- [ ] Parse output into structured format (directory sets)
- [ ] Handle non-existent branches with clear error messages
- [ ] Cache directory tree results for performance

---

### 75.2.3: Implement Directory Similarity Metric
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

### Implementation Checklist (From HANDOFF)
- [ ] Extract directory sets from both branches
- [ ] Implement formula: |intersection| / |union|
- [ ] Handle edge case: empty directory set
- [ ] Verify score always in [0, 1] range
- [ ] Test with identical, partial, and completely different trees

---

### 75.2.4: Implement File Addition Metric
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

### Implementation Checklist (From HANDOFF)
- [ ] Use `git diff main...BRANCH_NAME --diff-filter=A --name-only` to get added files
- [ ] Calculate total files in branch
- [ ] Compute addition_ratio = new_files / total_files_branch
- [ ] Apply inversion: metric = 1 - addition_ratio
- [ ] Cap result at 1.0, floor at 0.0
- [ ] Handle division by zero (empty repo case)

---

### 75.2.5: Implement Core Module Stability Metric
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

### Implementation Checklist (From HANDOFF)
- [ ] Define CORE_MODULES list: ["src/", "tests/", "config/", "build/", "dist/", ...]
- [ ] Use `git diff main...BRANCH_NAME --diff-filter=D --name-only` to detect deletions
- [ ] Check if any deleted files match core modules → score = 0.5
- [ ] Count modified core module files
- [ ] Apply penalty: 0.1 per 5 modifications
- [ ] If no changes to core: score = 1.0
- [ ] Return final score in [0, 1] range

---

### 75.2.6: Implement Namespace Isolation Metric
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

### Implementation Checklist (From HANDOFF)
- [ ] Identify all new files using git diff filter=A
- [ ] Extract directory prefixes for each new file
- [ ] Group files by common directory prefix
- [ ] Calculate clustering coefficient (files in few dirs = high)
- [ ] Invert if needed: isolated = high score
- [ ] Handle single file case gracefully
- [ ] Normalize to [0, 1] range

---

### 75.2.7: Aggregate Metrics & Output Formatting
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

### Implementation Checklist (From HANDOFF)
- [ ] Verify all 4 metrics in [0, 1] range (add assertions)
- [ ] Implement weighted sum: 0.30*directory + 0.25*additions + 0.25*stability + 0.20*isolation
- [ ] Create output dict with all required fields
- [ ] Add ISO 8601 timestamp: datetime.utcnow().isoformat() + 'Z'
- [ ] Include metadata: directory_count, file_count, new_files, modified_files
- [ ] Round aggregate_score to 3 decimal places

---

### 75.2.8: Write Unit Tests
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

### Test Case Examples (From HANDOFF)

1. **test_minor_feature_branch**: 3 new files in `src/features/`, no core changes
   - Expected: directory_similarity ≥ 0.9, file_additions > 0.7, all metrics in [0,1]

2. **test_refactoring_branch**: 50% of files modified, directory structure preserved
   - Expected: directory_similarity = 1.0, file_additions = 1.0 (no new files), stability depends on cores

3. **test_large_new_module**: 20 new files in `src/orchestration/`, new directory
   - Expected: directory_similarity < 1.0, file_additions affected by ratio, isolation high

4. **test_core_rewrite**: Changes to `src/core/`, potential stability issue
   - Expected: core_module_stability < 1.0 due to modifications

5. **test_deletion_heavy_branch**: Removes files from main
   - Expected: Directory similarity may drop, file_additions unaffected (only adds)

6. **test_empty_branch**: Branch identical to main
   - Expected: All metrics ≈ 1.0, aggregate_score ≈ 1.0

7. **test_nonexistent_branch**: Attempt to analyze non-existent branch
   - Expected: Raise appropriate error with clear message

8. **test_performance**: Analyze branch with 1000+ files
   - Expected: Complete in <2 seconds, reasonable memory usage

---

## Configuration Parameters

- `DIRECTORY_SIMILARITY_WEIGHT` = 0.30
- `FILE_ADDITIONS_WEIGHT` = 0.25
- `CORE_MODULE_STABILITY_WEIGHT` = 0.25
- `NAMESPACE_ISOLATION_WEIGHT` = 0.20
- `CORE_MODULES` = ["src/", "tests/", "config/", ...]
- `MAX_NEW_FILES_RATIO` = 0.50

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

## Technical Reference (From HANDOFF)

### Algorithm Details

**Directory Similarity (Jaccard)**
```
dirs_main = set of all directories in main
dirs_branch = set of all directories in branch
similarity = |intersection| / |union|
```

**File Additions**
```
new_files = files added (git diff filter=A)
total_files_branch = total files in branch
addition_ratio = new_files / total_files_branch
metric = max(0, 1 - addition_ratio)  # Invert: fewer additions = higher score
```

**Core Module Stability**
```
If any core module is deleted: score = 0.5
If core module files modified: apply penalty (0.1 per 5 modifications)
Else: score = 1.0 (high stability)
```

**Namespace Isolation**
```
Group new files by directory prefix
Calculate clustering coefficient (0-1)
Isolated = files clustered in few directories, not scattered
```

### Core Modules List (Configurable)
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

### Dependencies & Parallel Tasks
- **No dependencies on other Task 75.x components** - can start immediately (parallel with 75.1, 75.3)
- **Output feeds into:** Task 75.4 (BranchClusterer)
- **External libraries:** GitPython or subprocess (git CLI)

---

## Integration Checkpoint

**When to move to 75.4:**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification
- [ ] Accepts input from git repositories
- [ ] Ready for integration with other Stage One analyzers

---

## Done Definition

Task 75.2 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage)
3. Code review approved
4. Outputs match specification
5. Documentation complete
6. Ready for hand-off to Task 75.4
