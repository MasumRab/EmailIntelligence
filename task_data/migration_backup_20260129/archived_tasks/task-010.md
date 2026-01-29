# Task ID: 010

**Title:** Develop Feature Branch Identification and Categorization Tool

**Status:** pending

**Dependencies:** 007

**Priority:** medium

**Description:** Create a Python tool to automatically identify active feature branches, analyze their Git history, and suggest the optimal primary branch target (main, scientific, or orchestration-tools) based on codebase similarity and shared history.

**Details:**

The tool should use `GitPython` or direct `git` CLI commands to:
1.  List all remote feature branches: `git branch -r --list 'origin/feature-*'`. 
2.  For each feature branch, determine its common ancestor with `main`, `scientific`, and `orchestration-tools` using `git merge-base`. 
3.  Analyze `git log --oneline <common_ancestor>..<feature_branch>` and `git log --oneline <common_ancestor>..<primary_branch>` to find shared history depth and divergent changes. 
4.  Calculate codebase similarity (e.g., by comparing file hashes or a simpler heuristic like shared file paths) between the feature branch and each potential primary target. This could involve comparing `git ls-tree -r <branch>` outputs or `git diff --stat` from the common ancestor. 
5.  Suggest the most suitable primary target based on criteria like the longest shared history, fewest divergent changes, or highest codebase similarity. 
6.  Output a categorized list of feature branches, e.g., a JSON or CSV file, with suggested primary targets and a confidence score or rationale. This tool should be command-line executable.

**Test Strategy:**

Create a test repository with several feature branches diverging from `main`, `scientific`, and `orchestration-tools` at different points, with varying degrees of shared history and divergence. Manually determine the correct primary target for each. Run the tool and compare its output categorization against the manual assessment. Verify that it correctly identifies complex branches (e.g., `feature-notmuch*`) if they have significantly divergent histories or unique dependencies.

---

## Overview/Purpose

Develop a Python tool that automatically identifies active feature branches, analyzes their Git history, and suggests optimal integration targets (main, scientific, orchestration-tools) based on codebase similarity and shared history.

**Scope:** Feature branch identification, Git history analysis, target suggestion
**Focus:** Automated branch categorization with confidence scoring
**Value Proposition:** Streamlines branch alignment by providing data-driven target recommendations

---

## Success Criteria

Task 010 is complete when:

### Functional Requirements
- [ ] Lists all remote feature branches
- [ ] Determines common ancestors with primary branches
- [ ] Analyzes shared history and divergence
- [ ] Calculates codebase similarity metrics
- [ ] Suggests optimal integration targets
- [ ] Outputs categorized branch list (JSON/CSV)
- [ ] Provides confidence scores and rationale
- [ ] Detects destructive merge artifacts
- [ ] Identifies content mismatches
- [ ] Evaluates backend→src migration status

### Non-Functional Requirements
- [ ] Tool execution time: <30 seconds for 50 branches
- [ ] Code coverage: >90%
- [ ] Error handling: Comprehensive
- [ ] Output format: Standardized JSON/CSV

### Quality Gates
- [ ] Unit tests pass for all components
- [ ] Integration tests pass with Git operations
- [ ] Code review approved
- [ ] Documentation complete

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 007: Branch alignment framework
- [ ] Git repository with feature branches
- [ ] Python 3.8+ environment
- [ ] GitPython library installed

### Blocks (What This Task Unblocks)
- [ ] Task 016: Branch alignment operations
- [ ] Task 017: Merge operations
- [ ] Task 022+: All downstream alignment operations

### External Dependencies
- [ ] Python 3.8+
- [ ] Git 2.20+
- [ ] GitPython library

### Assumptions & Constraints
- [ ] Git history accessible
- [ ] Feature branches follow naming convention
- [ ] Primary branches (main, scientific, orchestration-tools) exist

---

## Subtasks

### 007.1. Implement Destructive Merge Artifact Detection for Feature Branches

**Status:** pending  
**Dependencies:** None  

Extend the feature branch analysis to identify potential destructive merge artifacts (e.g., '<<<<<<<', '=======', '>>>>>>>' markers) within the feature branch itself or in its comparison against a potential merge target. This will flag branches that are already 'broken' or indicate poor merging practices that would result in destructive artifacts.

**Details:**

Utilize `git diff --check` or `grep -E '^(<<<<<<<|=======|>>>>>>>)'` patterns on the feature branch's files compared to its common ancestor or potential merge target. Incorporate this detection into the overall branch analysis, flagging branches exhibiting such patterns. The presence of such artifacts should contribute to a lower confidence score or a specific 'merge_artifact_detected' flag in the tool's output.

### 007.2. Develop Logic for Detecting Content Mismatches in Similarly Named Branches

**Status:** pending  
**Dependencies:** 007.1  

Create a mechanism to compare feature branches, especially those with similar naming conventions (e.g., 'feature-scientific-X', 'feature-main-Y'), to their proposed primary targets. This logic should identify significant content differences that suggest incorrect merging or rebase history, beyond typical divergence, indicating a likely mis-merge or mis-rebase due to naming discrepancies.

**Details:**

Building upon the existing codebase similarity logic (point 4 in the parent task), specifically focus on identifying cases where a feature branch named for one primary target shows higher similarity to another primary target, or significant divergence from its expected target. This could involve enhanced diff analysis, file hash comparisons, or structural comparisons (e.g., directory layouts) across relevant parts of the codebase to quantify content misalignment. The output should include a 'content_mismatch_alert' or a specific rationale for such a detection.

### 007.3. Integrate Backend-to-Src Migration Status Analysis

**Status:** pending  
**Dependencies:** 007.1, 007.2  

Add a specific analysis step to evaluate the backend→src migration status within each feature branch. This involves checking for the presence, absence, or modification patterns of files/directories related to the migration, assessing if the migration is complete, incomplete, or in an inconsistent state.

**Details:**

Define clear criteria for a 'migrated' state (e.g., `backend/` directory is empty or removed, all relevant files moved to `src/` or specific files existing/missing in new `src/` locations). For each feature branch, analyze its directory structure and file contents using `git ls-tree -r <branch>` or `git diff <common_ancestor>..<feature_branch>` outputs to determine the migration status against a defined baseline. Categorize branches as 'migrated', 'partially migrated', 'not migrated', or 'inconsistent' based on these checks. This status should be a distinct field in the tool's output for each branch.

---

## Specification Details

### Technical Interface
```
FeatureBranchAnalyzer:
  - __init__(repo_path: str)
  - list_feature_branches() -> List[str]
  - analyze_branch(branch: str) -> dict
  - suggest_target(branch: str) -> dict
  - detect_merge_artifacts(branch: str) -> dict
  - detect_content_mismatch(branch: str, target: str) -> dict
  - check_migration_status(branch: str) -> str
  - generate_report() -> dict
```

### Data Models
```python
class BranchAnalysis:
  branch_name: str
  common_ancestors: dict
  shared_history: dict
  divergence: dict
  similarity_scores: dict
  suggested_target: str
  confidence_score: float
  merge_artifacts: List[str]
  content_mismatch: bool
  migration_status: str

class ReportOutput:
  branches: List[BranchAnalysis]
  summary: dict
  timestamp: str
```

### Business Logic
1. List all remote feature branches
2. For each branch:
   - Determine common ancestors with primary branches
   - Analyze shared history and divergence
   - Calculate codebase similarity
   - Suggest optimal target based on metrics
   - Detect merge artifacts
   - Check for content mismatches
   - Evaluate migration status
3. Generate comprehensive report
4. Output in JSON or CSV format

---

## Implementation Guide

### Approach
Implement Python tool using GitPython for Git operations, with modular analysis components for history, similarity, and migration status.

Rationale: GitPython provides robust Git interface, modular architecture allows for easy extension, confidence scoring provides actionable insights.

### Code Structure
```
scripts/
  feature_branch_analyzer.py
  analyzers/
    git_history.py
    codebase_similarity.py
    merge_artifacts.py
    migration_status.py
tests/
  test_analyzers/
  test_feature_branch_analyzer.py
```

### Key Implementation Steps
1. Implement merge artifact detection (007.1)
2. Implement content mismatch detection (007.2)
3. Implement migration status analysis (007.3)
4. Create main analyzer orchestration
5. Implement target suggestion logic
6. Generate report output
7. Write unit and integration tests

### Integration Points
- Git repository access
- Task 007: Branch alignment framework
- GitPython library
- Output JSON/CSV files

---

## Configuration Parameters

### Required Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| repo_path | str | "." | Path to Git repository |
| branch_pattern | str | "origin/feature-*" | Pattern for feature branches |
| primary_branches | list | ["main", "scientific", "orchestration-tools"] | Primary branch targets |

### Environmental Variables
| Variable | Required | Description |
|----------|----------|-------------|
| GIT_REPO_PATH | no | Path to Git repository |
| FEATURE_BRANCH_PATTERN | no | Pattern for feature branches |

---

## Performance Targets

### Response Time
- List branches: <5 seconds
- Analyze single branch: <2 seconds
- Analyze 50 branches: <30 seconds
- Generate report: <5 seconds

### Resource Utilization
- Memory: <200MB
- Disk I/O: Moderate (Git operations)
- CPU: Moderate (similarity calculations)

### Scalability
- Support up to 100 feature branches
- Support large repositories (>10k commits)
- Support complex branch histories

---

## Testing Strategy

### Unit Tests
- Git history analyzer: 15+ test cases
- Codebase similarity analyzer: 15+ test cases
- Merge artifact detector: 10+ test cases
- Content mismatch detector: 10+ test cases
- Migration status analyzer: 10+ test cases

### Integration Tests
- Full analysis workflow: 5+ test scenarios
- Git operations integration: 5+ scenarios
- Output format validation: 3+ scenarios

### Edge Case Tests
- No feature branches: Handle gracefully
- Complex branch histories: Analyze correctly
- Merge artifacts: Detect all markers
- Inconsistent migration: Flag appropriately

---

## Common Gotchas & Solutions

### Gotcha 1: Branch names with slashes

```python
# WRONG
branch_name.split('/')[1]  # Fails on complex names

# RIGHT
branch_name.replace('origin/', '')  # Remove prefix safely
```

### Gotcha 2: Git merge-base fails on unrelated branches

```python
# WRONG
merge_base = repo.merge_base(branch_a, branch_b)  # Crashes

# RIGHT
try:
    merge_base = repo.merge_base(branch_a, branch_b)
except GitCommandError:
    merge_base = None  # Handle unrelated branches
```

### Gotcha 3: Similarity calculation slow on large repos

```python
# WRONG
for file in all_files:  # Sequential processing
    calculate_similarity(file)

# RIGHT
# Sample representative files
sample_files = random.sample(all_files, min(100, len(all_files)))
for file in sample_files:  # Process subset
    calculate_similarity(file)
```

---

## Integration Checkpoint

**When to move to downstream tasks:**

- [ ] All 3 subtasks complete
- [ ] Merge artifact detection operational
- [ ] Content mismatch detection working
- [ ] Migration status analysis functional
- [ ] Target suggestions accurate
- [ ] Tests pass (>90% coverage)
- [ ] Integration with Task 007 verified
- [ ] Code review approved
- [ ] Documentation complete

---

## Done Definition

Task 010 is done when:

1. ✅ All 3 subtasks marked complete
2. ✅ Merge artifact detection operational
3. ✅ Content mismatch detection working
4. ✅ Migration status analysis functional
5. ✅ Target suggestions accurate
6. ✅ Unit tests pass (>90% coverage)
7. ✅ Integration tests pass
8. ✅ Code review approved
9. ✅ Integration with Task 007 verified
10. ✅ Commit: "feat: implement feature branch identification tool"
11. ✅ All success criteria checkboxes marked complete

---

## Next Steps

1. Test tool with various branch scenarios
2. Validate target suggestion accuracy
3. Optimize performance for large repositories
4. Document usage and outputs
5. Move to downstream tasks when validated

---
