# Task 009.7: Coordinate Conflict Detection and Resolution

**Status:** Ready for Implementation
**Priority:** High
**Effort:** 4-5 hours
**Complexity:** 8/10
**Dependencies:** 009.6

---

## Overview/Purpose

Coordinate with Task 013 (Conflict Detection and Resolution) when the rebase operation encounters conflicts. This subtask delegates the complex process of conflict handling to a specialized module, ensuring robust and guided resolution within the `Core Multistage Primary-to-Feature Branch Alignment` (Task 009) orchestration.

**Scope:** Conflict resolution coordination only (delegates actual conflict handling).
**Blocks:** 009.8 (Coordinate Post-Rebase Validation)

---

## Success Criteria

Task 009.7 is complete when:

### Core Functionality
- [ ] Python function/method can identify when conflicts are present after a rebase.
- [ ] Successfully delegates conflict resolution to Task 013's specialized module.
- [ ] Interprets the result from Task 013 (e.g., conflicts resolved, aborted, manual intervention needed).
- [ ] Returns a structured result indicating the outcome of the conflict resolution attempt.

### Quality Assurance
- [ ] Unit tests pass (minimum 3 test cases for conflicts resolved, conflicts aborted, and no conflicts).
- [ ] No exceptions raised for valid inputs.
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings.

### Integration Readiness
- [ ] Input (repository state, conflicted files) is compatible with Task 013's module.
- [ ] Output (resolution status) is compatible with Task 009's overall orchestration flow.
- [ ] Error handling integrates with Task 009's overall error reporting.

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 009.6 (Coordinate Core Rebase Initiation with Specialized Tasks) complete – to provide the initial rebase result and indication of conflicts.
- [ ] Task 013 (Conflict Detection and Resolution) module available and functional.
- [ ] Access to a Git repository with feature branches designed to produce conflicts for testing.

### Blocks (What This Task Unblocks)
- Task 009.8 (Coordinate Post-Rebase Validation)

### External Dependencies
- Python 3.8+
- Task 013's `ConflictDetectionResolver` module.

---

## Sub-subtasks Breakdown

### 009.7.1: Design Conflict Coordination Function
**Effort:** 1 hour | **Depends on:** None

Define the function signature, inputs (repo path, feature branch, primary target, rebase result), and expected outputs (structured resolution result). Outline the interface with Task 013.

### 009.7.2: Detect Conflicts After Rebase
**Effort:** 1 hour | **Depends on:** 009.7.1

Implement logic to check the repository status (`git status` or `repo.index.unmerged_blobs()`) to confirm conflicts are truly present after rebase.

### 009.7.3: Delegate to Task 013 for Resolution
**Effort:** 2 hours | **Depends on:** 009.7.2

Call Task 013's `ConflictDetectionResolver.resolve_conflicts()` function, passing necessary context (repo path, conflicted files).

### 009.7.4: Interpret Resolution Outcome
**Effort:** 0.5 hours | **Depends on:** 009.7.3

Process the structured result returned by Task 013, translating it into a format suitable for Task 009's orchestration flow.

---

## Specification Details

### Function Signature

```python
from typing import NamedTuple
# Assuming Task 013 provides a similar result structure
class ConflictResolutionOutcome(NamedTuple):
    status: str # "resolved", "aborted", "manual_required"
    conflicts_resolved_count: int = 0
    message: str = ""

def coordinate_conflict_resolution(
    repo_path: str,
    feature_branch: str,
    primary_target: str
) -> ConflictResolutionOutcome:
    """
    Coordinates conflict detection and resolution with Task 013.

    Args:
        repo_path: Path to the local Git repository.
        feature_branch: The name of the feature branch being rebased.
        primary_target: The primary target branch.

    Returns:
        A ConflictResolutionOutcome namedtuple.
    """
```

### Git Command Usage (for conflict detection confirmation)

*   `git status --porcelain`
*   `repo.index.unmerged_blobs()` (GitPython)

---

## Implementation Guide

### Step 1: Initialize Task 013 Resolver (Mock for now)
```python
from git import Repo
from typing import NamedTuple
# Placeholder for Task 013's resolver
class MockConflictDetectionResolver:
    def __init__(self, repo_path: str):
        self.repo = Repo(repo_path)
    
    def resolve_conflicts(self, branch_name: str, conflicted_files: list[str]) -> 'ConflictResolutionOutcome':
        # Simulate resolution: in a real scenario, this would involve user interaction
        # or automated tools, eventually calling git rebase --continue or --abort.
        # For testing, we'll assume success for simplicity.
        print(f"  [MOCK] Resolving {len(conflicted_files)} conflicts on {branch_name}")
        # In a real scenario, this would likely involve git add <file> and git rebase --continue
        # For this test, we assume user/auto-resolution leads to continuation.
        try:
            # Simulate a successful continue if there were conflicts
            if conflicted_files:
                self.repo.git.rebase('--continue')
            return ConflictResolutionOutcome(status="resolved", conflicts_resolved_count=len(conflicted_files), message="Conflicts resolved via Task 013")
        except Exception as e:
            return ConflictResolutionOutcome(status="aborted", conflicts_resolved_count=0, message=f"Simulated conflict resolution failed: {e}")

# In coordinate_conflict_resolution function:
# conflict_resolver = Task013ConflictDetectionResolver(repo_path) # Actual Task 013
conflict_resolver = MockConflictDetectionResolver(repo_path) # Use mock for now
```

### Step 2: Implement Conflict Detection and Delegation
```python
def coordinate_conflict_resolution(
    repo_path: str,
    feature_branch: str,
    primary_target: str
) -> ConflictResolutionOutcome:
    repo = Repo(repo_path)
    
    # Identify conflicted files
    conflicted_files = []
    if repo.is_rebase_in_progress(): # Helper to check if rebase is active
        # Get actual unmerged files from git status
        status_output = repo.git.status('--porcelain')
        for line in status_output.splitlines():
            if line.startswith('UU ') or line.startswith('AU ') or line.startswith('UD '):
                conflicted_files.append(line[3:].strip()) # Extract file path

    if not conflicted_files:
        return ConflictResolutionOutcome(status="no_conflicts", conflicts_resolved_count=0, message="No conflicts detected")

    # Delegate to Task 013 (or mock)
    # The actual Task 013 module would be imported and instantiated here
    conflict_resolver = MockConflictDetectionResolver(repo_path) 
    resolution_outcome = conflict_resolver.resolve_conflicts(feature_branch, conflicted_files)
    
    return resolution_outcome
```

---

## Configuration Parameters

None specific to this subtask; inherited from Task 009 orchestration.

---

## Performance Targets

*   **Conflict detection and delegation:** < 1 second.
*   **Memory usage:** Minimal.

---

## Testing Strategy

### Unit Tests
*   Test when no conflicts are present (should return "no_conflicts").
*   Test when conflicts are present and `Task 013` (mocked) successfully resolves them.
*   Test when conflicts are present and `Task 013` (mocked) indicates an abortion or manual intervention.

---

## Common Gotchas & Solutions

*   **Gotcha:** Incorrectly assuming a `rebase_in_progress` means conflicts.
    *   **Solution:** Always check for actual unmerged files using `git status` or `repo.index.unmerged_blobs()`.
*   **Gotcha:** Tight coupling with Task 013's internal implementation details.
    *   **Solution:** Define a clear, stable interface (API) for Task 013's conflict resolution module and delegate via that interface.

---

## Integration Checkpoint

*   All sub-subtasks complete.
*   Unit tests pass.
*   Function correctly identifies conflicts and delegates to Task 013.

---

## Done Definition

Task 009.7 is done when:
1.  All sub-subtasks marked complete.
2.  Unit tests pass.
3.  Conflict detection and delegation logic is robust.
4.  Documentation (docstrings, comments) is clear.

---

## Next Steps

*   Proceed to Task 009.8 (Coordinate Post-Rebase Validation).