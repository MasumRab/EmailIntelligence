# Task 75.2: CodebaseStructureAnalyzer

## Purpose
Create a reusable Python class that measures codebase structure similarity between branches. This is a Stage One analyzer with no dependencies on other tasks in this batch.

**Scope:** CodebaseStructureAnalyzer class only  
**Effort:** 28-36 hours | **Complexity:** 7/10  
**Status:** Ready for implementation  
**No dependencies** - can start immediately (parallel with 75.1, 75.3)

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
