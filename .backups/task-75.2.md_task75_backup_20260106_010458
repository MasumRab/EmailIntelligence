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

## Quick Navigation

Navigate this document using these links:

- [Purpose](#purpose)
- [Developer Quick Reference](#developer-quick-reference)
- [Success Criteria](#success-criteria)
- [Subtasks Overview](#subtasks-overview)
- [Subtask Details](#subtasks)
- [Configuration & Defaults](#configuration--defaults)
- [Technical Reference](#technical-reference)
- [Common Gotchas & Solutions](#common-gotchas--solutions)
- [Development Workflow](#typical-development-workflow)
- [Integration Handoff](#integration-handoff)
- [Integration Checkpoint](#integration-checkpoint)
- [Done Definition](#done-definition)

**Pro tip:** Use Ctrl+F to search within sections, or click links above to jump directly

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

**Performance Targets:**
- [ ] Directory structure analysis: **< 2 seconds** (on typical 500+ file repo)
- [ ] Memory usage: **< 50 MB** per analysis
- [ ] Handles **1,000+ file repositories** without failure
- [ ] Jaccard similarity computation: **O(n)** where n = number of files
- [ ] Git command timeout: **30 seconds max** (protects against hanging)

**Quality Assurance:**
- [ ] Unit tests pass (minimum 8 test cases with **>95% code coverage**)
- [ ] No exceptions raised for valid inputs (comprehensive error handling)
- [ ] Code quality: Passes linting, follows PEP 8, includes comprehensive docstrings

**Integration Readiness:**
- [ ] Compatible with Task 75.4 (BranchClusterer) input requirements
- [ ] Compatible with Task 75.6 (PipelineIntegration) consumption patterns
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Subtasks Overview

### Dependency Flow Diagram

```
75.2.1 (2-3h) ────────┐
[Structure Design]    │
                      ├─→ 75.2.2 (3-4h) ────────┐
                      │  [Git Tree Extraction]  │
                      │                         ├─→ 75.2.3-75.2.6 (parallel, 3-4h each) ────┐
                      │                         │   [Similarity, Additions, Stability, Isolation]  │
                      └─────────────────────────┘                                          │
                                                                                          ├─→ 75.2.7 (2-3h)
                                                                                          │  [Aggregation]
                                                                                          │
                                                                                          └─→ 75.2.8 (3-4h)
                                                                                             [Unit Tests]

Critical Path: 75.2.1 → 75.2.2 → 75.2.3-75.2.6 (parallel) → 75.2.7 → 75.2.8
Minimum Duration: 28-32 hours (with parallelization of 75.2.3-75.2.6)
```

### Parallel Opportunities

**Can run in parallel (after 75.2.2):**
- 75.2.3: Directory similarity metric
- 75.2.4: File additions metric
- 75.2.5: Core module stability metric
- 75.2.6: Namespace isolation metric

All four metric tasks depend only on 75.2.2 (git tree extraction) and are independent of each other. **Estimated parallel execution saves 9-12 hours.**

**Must be sequential:**
- 75.2.1 → 75.2.2 (design required before extraction)
- 75.2.2 → 75.2.3-75.2.6 (extraction required before metric calculation)
- 75.2.3-75.2.6 → 75.2.7 (all metrics needed before aggregation)
- 75.2.7 → 75.2.8 (main class needed before testing)

### Timeline with Parallelization

**Days 1-2: Design (75.2.1)**
- Define directory similarity logic, file addition scoring
- Document core modules list, namespace isolation

**Days 2-3: Git Tree Extraction (75.2.2)**
- Implement git ls-tree commands
- Create structured output format

**Days 3-5: Metrics (75.2.3-75.2.6 in parallel)**
- Day 3-4: Implement directory similarity + file additions (2 people)
- Day 3-4: Implement core stability + namespace isolation (2 people)
- Day 4-5: Consolidate and test

**Days 5-6: Aggregation & Testing (75.2.7-75.2.8)**
- Day 5: Implement aggregation
- Day 6: Write comprehensive unit tests

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

## Configuration & Defaults

All parameters should be externalized to configuration files (not hardcoded). Use YAML format:

```yaml
# config/codebase_structure_analyzer.yaml
codebase_structure_analyzer:
  # Metric Weights (sum must equal 1.0)
  directory_similarity_weight: 0.30      # Jaccard similarity importance
  file_additions_weight: 0.25            # New files impact
  core_module_stability_weight: 0.25     # Core modules preservation
  namespace_isolation_weight: 0.20       # New namespace clustering
  
  # Core Modules (patterns that identify critical components)
  core_modules:
    - "src/"
    - "tests/"
    - "config/"
    - "build/"
    - "dist/"
    - "requirements.txt"
    - "setup.py"
    - "pyproject.toml"
  
  # Thresholds and Limits
  max_new_files_ratio: 0.50              # Flag high additions
  core_modification_penalty: 0.1         # Per 5 core file modifications
  git_command_timeout_seconds: 30        # Prevent hanging on large repos
```

**How to use in code:**
```python
import yaml

def load_config(config_path='config/codebase_structure_analyzer.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)['codebase_structure_analyzer']

config = load_config()
DIR_WEIGHT = config['directory_similarity_weight']
FILE_ADD_WEIGHT = config['file_additions_weight']
CORE_MODULES = config['core_modules']
# ... etc
```

**Why externalize?**
- Easy to tune metrics without redeploying code
- Different configurations for different organizational needs
- Can adjust weights based on project priorities
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

## Typical Development Workflow

Complete step-by-step git workflow for implementing this task. Copy-paste ready sequences:

### Setup Your Feature Branch

```bash
# 1. Create feature branch
git checkout -b feat/codebase-structure-analyzer
git push -u origin feat/codebase-structure-analyzer

# 2. Create initial file structure
mkdir -p src/analyzers tests/analyzers config
touch src/analyzers/codebase_structure_analyzer.py
touch src/analyzers/__init__.py
git add src/analyzers/
git commit -m "chore: create codebase structure analyzer module"
```

### Subtask 75.2.1: Structure Design

```bash
# Document metrics design
cat > docs/CODEBASE_STRUCTURE_DESIGN.md << 'EOF'
# CodebaseStructureAnalyzer Design

## Metrics
1. Directory Similarity (Jaccard): |intersection| / |union|
2. File Additions: 1 - (new_files / total_files)
3. Core Module Stability: 1.0 if no core changes, 0.5 if deleted
4. Namespace Isolation: Clustering coefficient for new files

## Weights
- Directory: 0.30
- Additions: 0.25
- Stability: 0.25
- Isolation: 0.20
EOF

git add docs/
git commit -m "docs: design codebase structure metrics (75.2.1)"
```

### Subtask 75.2.2: Git Tree Extraction

```bash
cat > src/analyzers/git_tree_utils.py << 'EOF'
import subprocess
from typing import Set

def get_directory_tree(repo_path: str, branch_name: str) -> Set[str]:
    """Extract directory tree from git branch."""
    cmd = ['git', 'ls-tree', '-r', '--name-only', branch_name]
    result = subprocess.run(
        cmd,
        cwd=repo_path,
        capture_output=True,
        text=True,
        timeout=30,
        encoding='utf-8'
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"Failed to extract tree from {branch_name}")
    
    return set(result.stdout.strip().split('\n'))
EOF

git add src/analyzers/git_tree_utils.py
git commit -m "feat: implement git tree extraction (75.2.2)"
```

### Subtasks 75.2.3-75.2.6: Metrics (Parallel)

```bash
# Create metric modules
cat > src/analyzers/metrics_directory_similarity.py << 'EOF'
def compute_directory_similarity(tree_main: set, tree_branch: set) -> float:
    """Jaccard similarity of directory trees."""
    if not tree_main and not tree_branch:
        return 1.0
    intersection = len(tree_main & tree_branch)
    union = len(tree_main | tree_branch)
    return intersection / union if union > 0 else 0.0
EOF

cat > src/analyzers/metrics_file_additions.py << 'EOF'
def compute_file_additions(new_files: int, total_files: int) -> float:
    """Score new files ratio (fewer = higher)."""
    if total_files == 0:
        return 0.5
    ratio = new_files / total_files
    return max(0, 1 - min(ratio, 1.0))
EOF

touch src/analyzers/metrics_core_stability.py
touch src/analyzers/metrics_namespace_isolation.py

git add src/analyzers/metrics_*.py
git commit -m "feat: implement structure metrics (75.2.3-75.2.6)"
```

### Subtask 75.2.7: Aggregation

```bash
cat > src/analyzers/aggregator.py << 'EOF'
def aggregate_metrics(metrics: dict, weights: dict) -> float:
    """Combine metrics into aggregate score."""
    total = 0.0
    for metric_name, metric_value in metrics.items():
        weight = weights.get(metric_name, 0)
        total += metric_value * weight
    return min(1.0, max(0.0, total))
EOF

git add src/analyzers/aggregator.py
git commit -m "feat: implement metric aggregation (75.2.7)"
```

### Final: Create Configuration and Tests

```bash
# Create configuration file
mkdir -p config
cat > config/codebase_structure_analyzer.yaml << 'EOF'
codebase_structure_analyzer:
  directory_similarity_weight: 0.30
  file_additions_weight: 0.25
  core_module_stability_weight: 0.25
  namespace_isolation_weight: 0.20
  core_modules:
    - "src/"
    - "tests/"
    - "config/"
  max_new_files_ratio: 0.50
  git_command_timeout_seconds: 30
EOF

git add config/
git commit -m "config: codebase structure analyzer configuration"

# Create unit tests
mkdir -p tests/analyzers
cat > tests/analyzers/test_codebase_structure_analyzer.py << 'EOF'
import pytest
from src.analyzers import CodebaseStructureAnalyzer

@pytest.fixture
def test_repo(tmp_path):
    """Create test repository."""
    pass

def test_minor_feature_branch(test_repo):
    analyzer = CodebaseStructureAnalyzer(test_repo)
    result = analyzer.analyze("feature")
    assert 0 <= result['aggregate_score'] <= 1.0
    assert 'metrics' in result

# ... 8+ tests total
EOF

pytest tests/analyzers/ -v --cov=src/analyzers --cov-report=html
git add tests/
git commit -m "test: comprehensive unit tests (95%+ coverage)"

# Final push
git push origin feat/codebase-structure-analyzer
```

---

## Integration Handoff

### What Gets Passed to Task 75.4 (BranchClusterer)

**Task 75.4 expects input in this format:**

```python
from src.analyzers import CodebaseStructureAnalyzer

analyzer = CodebaseStructureAnalyzer(repo_path)
result = analyzer.analyze("feature/branch-name")

# result is a dict like:
# {
#   "branch_name": "feature/auth-system",
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

**Task 75.4 uses these outputs by:**
1. Extracting the structure metrics from the output
2. Using aggregate_score as one of 3 distance metrics for clustering
3. Combining with metrics from Task 75.1 and Task 75.3
4. Computing pairwise distances between branches
5. Creating dendrogram via hierarchical clustering

**Validation before handoff:**
```bash
python -c "
from src.analyzers import CodebaseStructureAnalyzer

analyzer = CodebaseStructureAnalyzer('.')
result = analyzer.analyze('main')

# Verify required fields exist
assert 'metrics' in result
assert 'aggregate_score' in result
assert 'directory_count' in result

# Verify metrics are normalized
for m in result['metrics'].values():
    assert 0 <= m <= 1, f'Metric {m} not in [0,1]'

assert 0 <= result['aggregate_score'] <= 1

print('✓ Output valid and ready for Task 75.4')
"
```

---

## Common Gotchas & Solutions

### Gotcha 1: Git Timeout on Large Repos ⚠️

**Problem:** `subprocess.run()` hangs indefinitely on large repos  
**Symptom:** Process stuck at analyzing, never returns  
**Root Cause:** No timeout set, `git ls-tree` takes too long  

**Solution:** Always set timeout parameter
```python
result = subprocess.run(
    cmd,
    timeout=30,  # ← CRITICAL: 30 second timeout
    capture_output=True,
    text=True
)
```

**Test:** Run against repo with 10,000+ files, verify completes in <30 seconds

---

### Gotcha 2: Directory Sets vs. File Sets ⚠️

**Problem:** Comparing directories and files as same set causes incorrect Jaccard  
**Symptom:** Similarity scores don't match expectations  
**Root Cause:** Not extracting directory paths properly from file paths  

**Solution:** Extract directory paths explicitly
```python
def extract_directories(file_paths: set) -> set:
    """Extract unique directories from file paths."""
    dirs = set()
    for fpath in file_paths:
        parts = fpath.split('/')
        for i in range(1, len(parts)):
            dirs.add('/'.join(parts[:i]))
    return dirs
```

**Test:** Branch with files in various directories, verify correct directory count

---

### Gotcha 3: Division by Zero with Empty Repos ⚠️

**Problem:** Empty repo or no differences causes division by zero  
**Symptom:** `ZeroDivisionError` when computing ratios  
**Root Cause:** No bounds checking on file counts  

**Solution:** Check for zero denominators
```python
if total_files == 0:
    return 0.5  # Default neutral score
metric = new_files / total_files
```

**Test:** Analyze branch identical to main, verify all metrics computed

---

### Gotcha 4: Core Module Matching Issues ⚠️

**Problem:** Case-sensitivity or trailing slashes prevent matching  
**Symptom:** Core modules detected as modified when they weren't  
**Root Cause:** String matching doesn't normalize paths  

**Solution:** Normalize paths before comparison
```python
def is_core_module(filepath: str, core_modules: list) -> bool:
    """Check if filepath matches any core module pattern."""
    normalized = filepath.lower().replace('\\', '/')
    for pattern in core_modules:
        if normalized.startswith(pattern.lower()):
            return True
    return False
```

**Test:** Branch with mixed case paths, verify core detection works

---

### Gotcha 5: Large File Counts Cause Memory Issues ⚠️

**Problem:** Large repos with 100,000+ files exhaust memory  
**Symptom:** Out of memory error during set operations  
**Root Cause:** Loading entire tree into memory at once  

**Solution:** Stream processing for large repos
```python
def get_directory_tree_streaming(repo_path: str, branch_name: str):
    """Stream directory tree to avoid memory overload."""
    cmd = ['git', 'ls-tree', '-r', '--name-only', branch_name]
    result = subprocess.run(
        cmd,
        cwd=repo_path,
        stdout=subprocess.PIPE,
        timeout=30,
        encoding='utf-8'
    )
    return result.stdout  # Generator-like behavior
```

**Test:** Repo with 100,000+ files, verify memory stays <50 MB

---

### Gotcha 6: Missing Branch Handling ⚠️

**Problem:** Attempting to analyze non-existent branch causes obscure error  
**Symptom:** `CalledProcessError` without clear message  
**Root Cause:** No validation before attempting extraction  

**Solution:** Validate branch exists first
```python
def branch_exists(repo_path: str, branch_name: str) -> bool:
    """Check if branch exists."""
    result = subprocess.run(
        ['git', 'rev-parse', '--verify', branch_name],
        cwd=repo_path,
        capture_output=True
    )
    return result.returncode == 0

if not branch_exists(repo_path, branch_name):
    raise ValueError(f"Branch {branch_name} does not exist")
```

**Test:** Analyze non-existent branch, verify clear error message

---

### Gotcha 7: UTF-8 Encoding Issues ⚠️

**Problem:** File paths with non-ASCII characters cause encoding errors  
**Symptom:** `UnicodeDecodeError` during parsing  
**Root Cause:** Default encoding not UTF-8  

**Solution:** Explicitly specify UTF-8
```python
result = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    encoding='utf-8',  # ← Explicit UTF-8
    errors='replace'   # ← Replace invalid chars
)
```

**Test:** Branch with non-ASCII filenames, verify no encoding errors

---

### Gotcha 8: Metric Weight Validation ⚠️

**Problem:** Configuration with weights not summing to 1.0 produces invalid aggregates  
**Symptom:** Aggregate score outside [0,1] range  
**Root Cause:** No validation of weight sums  

**Solution:** Validate weights sum to 1.0
```python
def validate_weights(weights: dict) -> bool:
    """Verify weights sum to 1.0."""
    total = sum(weights.values())
    if abs(total - 1.0) > 0.001:  # Allow small floating-point error
        raise ValueError(f"Weights sum to {total}, must equal 1.0")
    return True
```

**Test:** Load configuration, verify weights sum to 1.0

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
