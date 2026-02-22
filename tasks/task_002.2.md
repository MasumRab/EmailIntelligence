# Task 002.2: CodebaseStructureAnalyzer

**Status:** Ready for Implementation
**Priority:** High
**Effort:** 28-36 hours
**Complexity:** 7/10
**Dependencies:** None

---

## Overview/Purpose

Implement the `CodebaseStructureAnalyzer` class that measures codebase structure similarity between branches. This is a Stage One analyzer — one of three independent components (002.1, 002.2, 002.3) that feed into the clustering pipeline (Task 002.4).

**Scope:** CodebaseStructureAnalyzer class only
**No dependencies** — can start immediately
**Parallel with:** Task 002.1 (CommitHistoryAnalyzer), Task 002.3 (DiffDistanceCalculator)

---

## Success Criteria

Task 002.2 is complete when:

### Core Functionality
- [ ] `CodebaseStructureAnalyzer` class accepts `repo_path` (str) and `main_branch` (str, default "main")
- [ ] `analyze(branch_name)` maps directory/file structure for branch vs. main
- [ ] Computes exactly 4 normalized metrics in [0, 1] range
- [ ] Returns properly formatted dict with all required fields
- [ ] Handles all edge cases (empty branch, deletion-only branch, large new module)
- [ ] Output matches JSON schema exactly

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <2 seconds per branch analysis
- [ ] Code quality: PEP 8 compliant, Google-style docstrings

### Integration Readiness
- [ ] Output compatible with Task 002.4 (BranchClusterer) downstream requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Development environment configured (Python 3.8+)
- [ ] Test infrastructure in place (pytest)
- [ ] Access to a git repository with multiple branches for testing

### Blocks (What This Task Unblocks)
- Task 002.4 (BranchClusterer) — consumes this analyzer's output

### External Dependencies
- Python 3.8+ (built-in `os`, `pathlib` for path operations)
- GitPython or subprocess for git commands

---

## Sub-subtasks Breakdown

### 002.2.1: Design Metric System
**Effort:** 2-3 hours | **Depends on:** None

Define 4 core metrics with mathematical formulas. Document Jaccard similarity approach for directories, file addition ratio inversion, core module stability scoring, and namespace isolation clustering. Define weighting scheme (0.30/0.25/0.25/0.20, sum = 1.0).

### 002.2.2: Set Up Git Tree Extraction
**Effort:** 4-5 hours | **Depends on:** 002.2.1

Extract full directory tree for both main and branch using `git ls-tree -r --name-only`. Extract file changes using `git diff main...BRANCH --name-status`. Parse added/modified/deleted files.

### 002.2.3: Implement Directory Similarity Metric
**Effort:** 4-5 hours | **Depends on:** 002.2.2

Compute Jaccard similarity of directory sets between main and branch. Extract unique directory prefixes from file paths. Handle empty directory sets.

### 002.2.4: Implement File Additions Metric
**Effort:** 3-4 hours | **Depends on:** 002.2.2

Count new files via `git diff --diff-filter=A`. Compute ratio new_files / total_files. Invert: `max(0, 1 - ratio)`. Fewer additions = higher score.

### 002.2.5: Implement Core Module Stability Metric
**Effort:** 4-5 hours | **Depends on:** 002.2.2

Check CORE_MODULES list against modified/deleted files. Apply penalty scoring: deletion = 0.5, modifications = -0.1 per 5 changes, else 1.0.

### 002.2.6: Implement Namespace Isolation Metric
**Effort:** 4-5 hours | **Depends on:** 002.2.2

Group new files by directory prefix. Calculate clustering coefficient (0-1). Isolated = files clustered in few directories, not scattered.

### 002.2.7: Aggregate, Test, and Document
**Effort:** 6-8 hours | **Depends on:** 002.2.3–002.2.6

Weight and aggregate all 4 metrics. Write 8+ unit tests. Validate output schema. Write docstrings.

---

## Specification Details

### Class Interface

```python
class CodebaseStructureAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main")
    def analyze(self, branch_name: str) -> dict
```

### Metrics Definitions

| Metric | Weight | Formula | Notes |
|--------|--------|---------|-------|
| `directory_similarity` | 30% | `\|dirs_main ∩ dirs_branch\| / \|dirs_main ∪ dirs_branch\|` | Jaccard similarity |
| `file_additions` | 25% | `max(0, 1 - new_files / total_files_branch)` | Inverted ratio |
| `core_module_stability` | 25% | Penalty-based: deletion=0.5, mods=-0.1/5, else=1.0 | Core module preservation |
| `namespace_isolation` | 20% | Clustering coefficient of new files by directory | Isolation scoring |

### Algorithm Details

**Directory Similarity (Jaccard):**
```
dirs_main = set of all directories in main
dirs_branch = set of all directories in branch
similarity = |intersection| / |union|
```

**File Additions:**
```
new_files = files added (git diff filter=A)
total_files_branch = total files in branch
addition_ratio = new_files / total_files_branch
metric = max(0, 1 - addition_ratio)
```

**Core Module Stability:**
```
If any core module is deleted: score = 0.5
If core module files modified: apply penalty (0.1 per 5 modifications)
Else: score = 1.0 (high stability)
```

**Namespace Isolation:**
```
Group new files by directory prefix
Calculate clustering coefficient (0-1)
Isolated = files clustered in few directories, not scattered
```

### Output JSON Schema

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

## Implementation Guide

### Step 1: Repository Validation
```python
def __init__(self, repo_path: str, main_branch: str = "main"):
    if not os.path.exists(os.path.join(repo_path, ".git")):
        raise ValueError(f"Not a git repository: {repo_path}")
    self.repo_path = repo_path
    self.main_branch = main_branch
```

### Step 2: Tree Extraction
```python
def _get_file_tree(self, ref: str) -> set:
    output = self._run_git("ls-tree", "-r", "--name-only", ref)
    return set(output.splitlines())

def _get_dir_tree(self, ref: str) -> set:
    files = self._get_file_tree(ref)
    return {str(Path(f).parent) for f in files if "/" in f}
```

### Step 3: File Change Extraction
```python
def _get_changes(self, branch_name: str) -> dict:
    added = self._run_git("diff", f"{self.main_branch}...{branch_name}", "--diff-filter=A", "--name-only")
    modified = self._run_git("diff", f"{self.main_branch}...{branch_name}", "--diff-filter=M", "--name-only")
    deleted = self._run_git("diff", f"{self.main_branch}...{branch_name}", "--diff-filter=D", "--name-only")
    return {"added": added.splitlines(), "modified": modified.splitlines(), "deleted": deleted.splitlines()}
```

### Step 4: Implement Each Metric
Follow formulas in the Algorithm Details section for `_directory_similarity`, `_file_additions`, `_core_module_stability`, `_namespace_isolation`.

### Step 5: Aggregation
```python
def analyze(self, branch_name: str) -> dict:
    metrics = {
        "directory_similarity": self._directory_similarity(branch_name),
        "file_additions": self._file_additions(branch_name),
        "core_module_stability": self._core_module_stability(branch_name),
        "namespace_isolation": self._namespace_isolation(branch_name),
    }
    weights = [0.30, 0.25, 0.25, 0.20]
    aggregate = sum(m * w for m, w in zip(metrics.values(), weights))
    return {"branch_name": branch_name, "metrics": metrics, "aggregate_score": round(aggregate, 3), ...}
```

---

## Configuration & Defaults

```python
DIRECTORY_SIMILARITY_WEIGHT = 0.30
FILE_ADDITIONS_WEIGHT = 0.25
CORE_MODULE_STABILITY_WEIGHT = 0.25
NAMESPACE_ISOLATION_WEIGHT = 0.20

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

MAX_NEW_FILES_RATIO = 0.50  # Warn if > 50% new files
```

Load via `config/task_002_clustering.yaml` or constructor parameters.

---

## Typical Development Workflow

```bash
git checkout -b feature/002.2-codebase-structure-analyzer
# Implement class in src/analyzers/codebase_structure.py
# Write tests in tests/test_codebase_structure.py
pytest tests/test_codebase_structure.py -v --cov=src/analyzers/codebase_structure
# Verify output schema against specification
python -c "from src.analyzers.codebase_structure import CodebaseStructureAnalyzer; print(CodebaseStructureAnalyzer('.').analyze('main'))"
git add -A && git commit -m "feat: complete Task 002.2 CodebaseStructureAnalyzer"
```

---

## Integration Handoff

**Downstream:** Task 002.4 (BranchClusterer) consumes the output dict directly.

**Contract:** The `analyze()` return dict must contain exactly the keys shown in the Output JSON Schema. Task 002.4 reads `metrics` and `aggregate_score`.

**Parallel with:** Task 002.1 (CommitHistoryAnalyzer), Task 002.3 (DiffDistanceCalculator) — no cross-dependencies.

---

## Common Gotchas & Solutions

**Gotcha 1: Empty directory sets cause ZeroDivisionError in Jaccard**
```python
# WRONG
similarity = len(intersection) / len(union)  # union can be empty

# RIGHT
if not union:
    return 1.0  # Identical empty trees
similarity = len(intersection) / len(union)
```

**Gotcha 2: File paths with spaces or special characters**
```python
# WRONG
files = output.split("\n")  # Assumes clean paths

# RIGHT
files = [f.strip() for f in output.splitlines() if f.strip()]
```

**Gotcha 3: Core module detection with partial matches**
```python
# WRONG
if "src" in filepath:  # Matches "resource", "description"

# RIGHT
if any(filepath.startswith(mod) for mod in CORE_MODULES):
```

**Gotcha 4: Branch with only deletions**
```python
# total_files_branch could be 0 if everything deleted
total_files = max(1, len(branch_files))
```

---

## Integration Checkpoint

**When to move to Task 002.4 (BranchClusterer):**

- [ ] All 7 sub-subtasks complete
- [ ] Unit tests passing (>95% coverage)
- [ ] Output matches specification exactly
- [ ] No validation errors on test data
- [ ] Performance targets met (<2s per branch)
- [ ] Edge cases handled correctly
- [ ] Code review approved
- [ ] Commit message: `feat: complete Task 002.2 CodebaseStructureAnalyzer`

---

## Done Definition

Task 002.2 is done when:

1. All 7 sub-subtasks marked complete
2. Unit tests pass (>95% coverage) on CI/CD
3. Code review approved
4. Outputs match specification exactly
5. Output schema validation passes
6. Documentation complete and accurate
7. Performance benchmarks met (<2s per branch)
8. Ready for hand-off to Task 002.4
9. Commit: `feat: complete Task 002.2 CodebaseStructureAnalyzer`
10. All success criteria checkboxes marked complete

---

## Provenance

- **Primary source:** HANDOFF_75.2_CodebaseStructureAnalyzer.md (archived: task_data/migration_backup_20260129/task_data_original/archived/handoff_archive_task75/)
- **Structure standard:** TASK_STRUCTURE_STANDARD.md (approved January 6, 2026)
- **ID mapping:** 75.2 → 002.2 (migration performed January 29, 2026)
- **Test cases:** 5 scenarios from HANDOFF_75.2 (Minor feature, Refactoring, Large new module, Core rewrite, Deletion-heavy)
- **Algorithm details:** 4 formulas from HANDOFF_75.2 Algorithm Details section
- **CORE_MODULES list:** 8 entries from HANDOFF_75.2

## Performance Targets

[Performance targets to be defined]


## Testing Strategy

[Testing strategy to be defined]


## Next Steps

[Next steps to be defined]
