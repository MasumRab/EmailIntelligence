# Task 007: Develop Feature Branch Identification and Categorization Tool

**Status:** pending
**Priority:** medium
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** 004

---


## Overview/Purpose

Create a Python tool to automatically identify active feature branches, analyze their Git history, and suggest the optimal primary branch target (main, scientific, or orchestration-tools) based on codebase similarity and shared history.

---

## Success Criteria

- [ ] [Success criteria to be defined]

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 004

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

## Sub-subtasks Breakdown

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

### Blocks (What This Task Unblocks)
- [ ] None specified

### External Dependencies
- [ ] None

---

## Specification Details

### Task Interface
- **ID**: 007
- **Title**: Develop Feature Branch Identification and Categorization Tool

**Status:** pending

**Dependencies:** 004

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

## Implementation Guide

### Content Comparison

```python
def get_file_structure(branch):
    """Get file structure for branch."""
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", branch],
        capture_output=True, text=True
    )
    return set(result.stdout.strip().split('\n'))

def calculate_similarity(branch1, branch2):
    """Calculate Jaccard similarity between branches."""
    files1 = get_file_structure(branch1)
    files2 = get_file_structure(branch2)
    
    intersection = files1 & files2
    union = files1 | files2
    
    if not union:
        return 0.0
    
    return len(intersection) / len(union)

def detect_content_mismatch(branch, expected_target):
    """Detect if branch content mismatches expected target."""
    actual_similarities = {
        "main": calculate_similarity(branch, "main"),
        "scientific": calculate_similarity(branch, "scientific"),
        "orchestration-tools": calculate_similarity(branch, "orchestration-tools"),
    }
    
    expected_similarity = actual_similarities.get(expected_target, 0)
    best_match = max(actual_similarities, key=actual_similarities.get)
    
    if best_match != expected_target:
        return {
            "mismatch": True,
            "expected": expected_target,
            "actual": best_match,
            "confidence": actual_similarities[expected_target],
            "best_match": best_match,
            "best_confidence": actual_similarities[best_match],
        }
    
    return {"mismatch": False}
```

---

## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

---

## Performance Targets

- **Effort Range**: TBD
- **Complexity Level**: TBD

---

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

---

## Common Gotchas & Solutions

- [ ] [Common issues and solutions to be documented]

---

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

---

## Done Definition

### Completion Criteria
- [ ] All success criteria checkboxes marked complete
- [ ] Code quality standards met (PEP 8, documentation)
- [ ] Performance targets achieved
- [ ] All subtasks completed
- [ ] Integration checkpoint criteria satisfied

---

## Next Steps

- [ ] No next steps specified
- [ ] Additional steps to be defined

---
