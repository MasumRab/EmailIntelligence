# Task 002.2: CodebaseStructureAnalyzer

**Status:** Ready for Implementation  
**Priority:** High  
**Effort:** 28-36 hours  
**Complexity:** 7/10  
**Dependencies:** None - can start immediately  
**Blocks:** Task 002.4 (BranchClusterer)

---

## Purpose

Create a reusable Python class that measures codebase structure similarity between branches using directory and file analysis. This is a Stage One analyzer with no dependencies on other tasks.

**Scope:** CodebaseStructureAnalyzer class only  
**No dependencies** - can start immediately (parallel with 002.1, 002.3)  
**Parallelizable with:** Task 002.1 and Task 002.3

---

## Success Criteria

Task 002.2 is complete when:

### Core Functionality
- [ ] `CodebaseStructureAnalyzer` class accepts `repo_path` (str) and `branch_name` (str)
- [ ] Maps directory/file structure for target branch vs. main
- [ ] Computes exactly 4 normalized metrics in [0,1] range:
  - [ ] `directory_similarity` - Jaccard similarity of directory trees (30% weight)
  - [ ] `file_additions` - Ratio of new files added, inverted (25% weight)
  - [ ] `core_module_stability` - Preservation of core modules (25% weight)
  - [ ] `namespace_isolation` - Isolation score for new packages (20% weight)
- [ ] Returns properly formatted dict with aggregate similarity score
- [ ] Handles all specified edge cases:
  - [ ] Empty branches (no file changes)
  - [ ] Deletion-heavy branches
  - [ ] Binary file handling
  - [ ] Large file counts (1000+ files)
- [ ] Output matches JSON schema exactly

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% code coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <2 seconds per branch analysis
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings
- [ ] Memory: <50 MB per analysis
- [ ] All metrics verified in [0,1] range

### Integration Readiness
- [ ] Compatible with Task 002.4 (BranchClusterer) input requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate
- [ ] Handles core modules list from configuration

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Git installed and accessible via subprocess
- [ ] Python 3.8+ with subprocess module
- [ ] Test infrastructure in place
- [ ] Project structure created (src/analyzers/)

### Blocks (What This Task Unblocks)
- Task 002.4 (BranchClusterer) - requires output from this task

### External Dependencies
- Python subprocess (built-in)
- GitPython (optional)
- Standard library: datetime, json, typing

### No Dependency On
- Task 002.1 (CommitHistoryAnalyzer) - can start in parallel
- Task 002.3 (DiffDistanceCalculator) - can start in parallel

---

## Sub-subtasks

### 002.2.1: Design Structure Analysis Architecture
**Effort:** 2-3 hours  
**Depends on:** None

**Steps:**
1. Design directory tree comparison logic
2. Define Jaccard similarity calculation approach
3. Document file addition scoring approach
4. Define core modules list
5. Design namespace isolation metric calculation

**Success Criteria:**
- [ ] All metrics mathematically defined
- [ ] Calculation approach documented
- [ ] Core modules list specified (src/, tests/, config/, etc.)
- [ ] Edge cases identified

---

### 002.2.2: Implement Git Tree Extraction
**Effort:** 3-4 hours  
**Depends on:** 002.2.1

**Steps:**
1. Implement `git ls-tree` command execution
2. Extract directory tree for main branch
3. Extract directory tree for target branch
4. Parse output into structured format
5. Add error handling for invalid branches

**Success Criteria:**
- [ ] Extracts directory lists without error
- [ ] Returns structured data (lists of files/dirs)
- [ ] Handles non-existent branches gracefully
- [ ] Performance: <1 second per extraction

---

### 002.2.3: Implement Directory Similarity Metric
**Effort:** 3-4 hours  
**Depends on:** 002.2.1, 002.2.2

**Steps:**
1. Extract directory sets from both branches
2. Implement Jaccard similarity formula: |intersection| / |union|
3. Normalize to [0,1] range
4. Test with various branch types
5. Verify edge cases (identical, completely different)

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Identical trees score = 1.0
- [ ] Completely different trees score = 0.0
- [ ] Calculation verified with test cases
- [ ] Handles empty directory sets

---

### 002.2.4: Implement File Addition Metric
**Effort:** 3-4 hours  
**Depends on:** 002.2.1, 002.2.2

**Steps:**
1. Extract file changes using `git diff`
2. Identify newly added files
3. Calculate addition ratio (new_files / total_files)
4. Invert to score (fewer additions = higher score)
5. Cap at 1.0 and normalize

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] No new files scores = 1.0
- [ ] 100% new files scores = 0.0
- [ ] Handles edge cases (empty repos, single file)

---

### 002.2.5: Implement Core Module Stability Metric
**Effort:** 3-4 hours  
**Depends on:** 002.2.1, 002.2.2

**Steps:**
1. Define core modules list (configurable: src/, tests/, config/, build/, dist/)
2. Check for core module deletions
3. Count modifications to core files
4. Apply penalties for changes
5. Return stability score

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Deleted core modules: score = 0.5
- [ ] No changes to core: score = 1.0
- [ ] Identifies all core module types
- [ ] Handles missing core modules

---

### 002.2.6: Implement Namespace Isolation Metric
**Effort:** 3-4 hours  
**Depends on:** 002.2.1, 002.2.2

**Steps:**
1. Identify new files from branch
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
**Effort:** 2-3 hours  
**Depends on:** 002.2.3, 002.2.4, 002.2.5, 002.2.6

**Steps:**
1. Define metric weights (sum to 1.0): 0.30/0.25/0.25/0.20
2. Create aggregation function (weighted sum)
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
**Effort:** 3-4 hours  
**Depends on:** 002.2.7

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

## Specification

### Class Interface

```python
class CodebaseStructureAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main"):
        """Initialize analyzer with repository path."""
        
    def analyze(self, branch_name: str) -> dict:
        """Analyze codebase structure for a branch.
        
        Args:
            branch_name: Name of branch to analyze
            
        Returns:
            Dict with metrics, aggregate score, and metadata
        """
```

### Output Format

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

### Metrics Definitions

| Metric | Definition | Weight | Notes |
|--------|-----------|--------|-------|
| `directory_similarity` | Jaccard similarity of directory trees | 0.30 | |intersection| / |union| |
| `file_additions` | Inverted ratio of new files | 0.25 | 1 - (new_files / total_files) |
| `core_module_stability` | Preservation of core modules | 0.25 | Penalty for deletions/changes |
| `namespace_isolation` | Grouping of new packages | 0.20 | Higher if changes grouped |

---

## Implementation Guide

### 002.2.1: Design Structure Analysis Architecture

Define metrics:

```python
METRICS_CONFIG = {
    'directory_similarity': {
        'weight': 0.30,
        'formula': 'jaccard(dirs_main, dirs_branch)',
        'interpretation': '1.0 = identical, 0.0 = completely different'
    },
    'file_additions': {
        'weight': 0.25,
        'formula': '1 - (new_files / total_files_on_branch)',
        'max_ratio': 0.50,
        'interpretation': 'Higher = fewer new files'
    },
    'core_module_stability': {
        'weight': 0.25,
        'core_modules': ['src/', 'tests/', 'config/', 'build/', 'dist/'],
        'interpretation': 'Higher = core modules preserved'
    },
    'namespace_isolation': {
        'weight': 0.20,
        'formula': 'clustering_coefficient(new_files)',
        'interpretation': 'Higher = changes grouped together'
    }
}
```

### 002.2.2: Git Tree Extraction

```python
def get_directory_tree(repo_path: str, branch_name: str) -> Set[str]:
    """Extract directory tree from branch."""
    cmd = ['git', 'ls-tree', '-r', '--name-only', branch_name]
    output = subprocess.run(
        cmd,
        cwd=repo_path,
        capture_output=True,
        text=True,
        timeout=30
    ).stdout
    
    # Extract directories from file paths
    directories = set()
    for file_path in output.strip().split('\n'):
        if not file_path:
            continue
        # Add all parent directories
        parts = file_path.split('/')
        for i in range(len(parts)):
            directories.add('/'.join(parts[:i+1]))
    
    return directories
```

### 002.2.3: Directory Similarity (Jaccard)

```python
def calculate_directory_similarity(
    main_dirs: Set[str],
    branch_dirs: Set[str]
) -> float:
    """Jaccard similarity: |intersection| / |union|."""
    if not main_dirs and not branch_dirs:
        return 1.0  # Both empty = identical
    
    intersection = main_dirs & branch_dirs
    union = main_dirs | branch_dirs
    
    if not union:
        return 0.0
    
    jaccard = len(intersection) / len(union)
    return max(0.0, min(1.0, jaccard))
```

### 002.2.4: File Addition Metric

```python
def calculate_file_additions(
    repo_path: str,
    branch_name: str,
    main_branch: str = "main"
) -> float:
    """Score based on ratio of new files."""
    # Get added files
    cmd = ['git', 'diff', f'{main_branch}...{branch_name}', 
           '--diff-filter=A', '--name-only']
    added = subprocess.run(
        cmd, cwd=repo_path, capture_output=True, text=True, timeout=30
    ).stdout.strip().split('\n')
    added_count = len([f for f in added if f])
    
    # Get total files on branch
    cmd = ['git', 'ls-tree', '-r', '--name-only', branch_name]
    total = subprocess.run(
        cmd, cwd=repo_path, capture_output=True, text=True, timeout=30
    ).stdout.strip().split('\n')
    total_count = len([f for f in total if f])
    
    if total_count == 0:
        return 1.0
    
    ratio = added_count / total_count
    # Invert: more additions = lower score
    score = 1.0 - min(1.0, ratio)
    return max(0.0, min(1.0, score))
```

### 002.2.5: Core Module Stability

```python
CORE_MODULES = ['src/', 'tests/', 'config/', 'build/', 'dist/']

def calculate_core_module_stability(
    repo_path: str,
    branch_name: str,
    main_branch: str = "main",
    core_modules: List[str] = None
) -> float:
    """Check if core modules are preserved."""
    if core_modules is None:
        core_modules = CORE_MODULES
    
    # Get deleted files
    cmd = ['git', 'diff', f'{main_branch}...{branch_name}',
           '--diff-filter=D', '--name-only']
    deleted = subprocess.run(
        cmd, cwd=repo_path, capture_output=True, text=True, timeout=30
    ).stdout.strip().split('\n')
    
    # Check if any core modules were deleted
    core_deletions = [f for f in deleted 
                      if any(f.startswith(cm) for cm in core_modules)]
    
    if core_deletions:
        return 0.5  # Penalty for deletion
    
    return 1.0  # No deletions = stable
```

### 002.2.6: Namespace Isolation

```python
def calculate_namespace_isolation(
    repo_path: str,
    branch_name: str,
    main_branch: str = "main"
) -> float:
    """Score isolation of new files (grouped vs scattered)."""
    # Get added files
    cmd = ['git', 'diff', f'{main_branch}...{branch_name}',
           '--diff-filter=A', '--name-only']
    added = [f.strip() for f in subprocess.run(
        cmd, cwd=repo_path, capture_output=True, text=True, timeout=30
    ).stdout.strip().split('\n') if f.strip()]
    
    if not added:
        return 0.5  # No additions
    
    # Group by top-level directory
    directories = {}
    for file_path in added:
        top_dir = file_path.split('/')[0]
        directories[top_dir] = directories.get(top_dir, 0) + 1
    
    # Clustering coefficient: if all in one directory = 1.0
    if len(directories) == 1:
        return 1.0
    
    # Multiple directories: score based on distribution
    # More concentrated = higher score
    max_in_one_dir = max(directories.values())
    score = max_in_one_dir / len(added)
    
    return max(0.0, min(1.0, score))
```

### 002.2.7: Aggregation

```python
def aggregate_metrics(
    metrics: Dict[str, float],
    weights: Dict[str, float] = None
) -> float:
    """Combine 4 metrics with weights."""
    if weights is None:
        weights = {
            'directory_similarity': 0.30,
            'file_additions': 0.25,
            'core_module_stability': 0.25,
            'namespace_isolation': 0.20
        }
    
    # Verify all metrics in [0, 1]
    for metric, value in metrics.items():
        assert 0 <= value <= 1, f"{metric} = {value} out of range"
    
    # Weighted sum
    aggregate = sum(
        metrics[k] * weights[k]
        for k in metrics.keys()
    )
    
    return max(0.0, min(1.0, aggregate))
```

---

## Configuration Parameters

All parameters externalized in `config/task_002_clustering.yaml`:

```yaml
codebase_structure:
  directory_similarity_weight: 0.30
  file_additions_weight: 0.25
  core_module_stability_weight: 0.25
  namespace_isolation_weight: 0.20
  
  core_modules:
    - src/
    - tests/
    - config/
    - build/
    - dist/
  
  max_new_files_ratio: 0.50
  git_command_timeout_seconds: 30
```

---

## Performance Targets

### Per Component
- Single branch analysis: <2 seconds
- Memory usage: <50 MB per analysis
- Handle repositories with 500+ files

### Scalability
- 13 branches: <26 seconds
- 50 branches: <100 seconds

---

## Testing Strategy

### Unit Tests

Minimum 8 test cases:

```python
def test_directory_similarity_identical():
    """Identical trees should score = 1.0"""
    
def test_directory_similarity_different():
    """Completely different trees should score near 0.0"""
    
def test_directory_similarity_partial():
    """Partial overlap should score between 0.3-0.7"""
    
def test_file_additions_no_additions():
    """No new files should score = 1.0"""
    
def test_file_additions_many_additions():
    """Many new files should score < 0.5"""
    
def test_core_module_stability_preserved():
    """Core modules preserved should score = 1.0"""
    
def test_core_module_stability_deleted():
    """Core modules deleted should score = 0.5"""
    
def test_output_schema_validation():
    """Output matches required schema"""
```

### Coverage Target
- Code coverage: >95%
- All edge cases covered (empty repos, single file, etc.)
- All error paths tested

---

## Common Gotchas & Solutions

**Gotcha 1: Directory vs file set confusion**
```python
# WRONG
dirs = set(path.split('/')[0] for path in files)  # Only top level

# RIGHT
dirs = set()
for file_path in files:
    parts = file_path.split('/')
    for i in range(len(parts)):
        dirs.add('/'.join(parts[:i+1]))  # All levels
```

**Gotcha 2: Division by zero with empty repos**
```python
# WRONG
ratio = added_count / total_count  # Crashes if total = 0

# RIGHT
if total_count == 0:
    return 1.0  # No files = no additions (score = 1.0)
ratio = added_count / total_count
```

**Gotcha 3: Core module matching fails on case sensitivity**
```python
# WRONG
if path.startswith('SRC/'):  # Case matters

# RIGHT
normalized = path.lower()
if any(normalized.startswith(cm.lower()) for cm in CORE_MODULES):
    # Handle match
```

**Gotcha 4: Large file counts cause memory issues**
```python
# WRONG
all_files = output.split('\n')  # Loads all into memory

# RIGHT
for line in output.split('\n'):
    if line:
        process_line(line)  # Stream processing
```

---

## Integration Checkpoint

**When to move to Task 002.4:**

- [ ] All 8 sub-subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification
- [ ] Performance targets met (<2s per branch)
- [ ] Edge cases handled correctly
- [ ] Code review approved

---

## Done Definition

Task 002.2 is done when:

1. ✅ All 8 sub-subtasks marked complete
2. ✅ Unit tests pass (>95% coverage)
3. ✅ Code review approved
4. ✅ Outputs match specification
5. ✅ Documentation complete
6. ✅ Ready for Task 002.4
7. ✅ Commit: "feat: complete Task 002.2 CodebaseStructureAnalyzer"

---

## Next Steps

1. Implement sub-subtask 002.2.1 (Design Metric System)
2. Complete all 8 sub-subtasks (Week 1)
3. Write unit tests (target: >95% coverage)
4. Code review
5. Ready for Task 002.4

---

**Last Updated:** January 6, 2026  
**Consolidated from:** Task 75.2 (task-75.2.md) with 51 original success criteria preserved  
**Structure:** TASK_STRUCTURE_STANDARD.md
