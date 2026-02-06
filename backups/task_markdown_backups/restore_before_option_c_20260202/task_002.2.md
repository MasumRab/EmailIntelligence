# Task 002.2: CodebaseStructureAnalyzer

**Status:** pending
**Priority:** high
**Effort:** 28-36 hours
**Complexity:** 8/10
**Dependencies:** None
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

## Sub-subtasks Breakdown

### 1.1: Execute Task
- Complete 005.2: CodebaseStructureAnalyzer
- Verify completion
- Update status



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

## Test Strategy

- Test with branches of varying complexity
- Verify structure detection accuracy
- Test import pattern extraction
- Validate comparison scoring

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

**When to move to Task 002.4:**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification
- [ ] Accepts input from git repositories
- [ ] Ready for integration with other Stage One analyzers

---

## Notes for Implementer

**Technical Requirements:**
1. Use subprocess with timeout for git commands
2. Implement robust tree parsing logic
3. Handle large repositories (10,000+ files)
4. Ensure thread-safe operation
5. Cache tree results for performance

**Edge Cases (Must Handle):**
- Empty branches (no files)
- Deletion-heavy branches
- Binary files (skip content analysis)
- Very large files (>10MB)
- Mixed encoding files
- Symbolic links

**Performance Targets:**
- Directory extraction: <1 second
- Metric calculation: <1 second
- Total analysis: <2 seconds per branch
- Memory usage: <100MB per analysis

---

## Done Definition

Task 002.2 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage)
3. Code review approved
4. Outputs match specification
5. Documentation complete
6. Ready for hand-off to Task 002.4

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation

