# Task 75.2: CodebaseStructureAnalyzer Implementation

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
- No internal dependencies on other Task 75.x components
- Output feeds into **Task 75.4 (BranchClusterer)**

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
4. Pass output to Task 75.4 integration point
5. Cross-check directory similarity with known repos

**Parallel tasks ready:** 75.1, 75.3 (no dependencies)
