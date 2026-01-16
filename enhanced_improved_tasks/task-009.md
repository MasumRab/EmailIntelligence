# Task ID: 009

**Status:** Ready for Implementation
**Priority:** High
**Effort:** 28-40 hours
**Complexity:** 8/10
**Dependencies:** 004, 006, 007, 012, 013, 014, 015, 022

---

## Purpose

Implement the core orchestrator for multistage branch alignment operations that coordinates with specialized tasks for backup/safety (Task 012), conflict resolution (Task 013), validation (Task 014), and rollback/recovery (Task 015). This task serves as the main entry point for the alignment process while delegating specialized operations to dedicated tasks.

**Scope:** Core alignment orchestration only
**Blocks:** Task 010 (Complex branch alignment), Task 011 (Validation integration)

---

## Success Criteria

Task 009 is complete when:

### Core Functionality
- [ ] Optimal primary target determination integration operational
- [ ] Environment setup and safety checks coordinated with Task 012
- [ ] Branch switching and fetching logic operational
- [ ] Core rebase initiation coordinated with specialized tasks
- [ ] Conflict detection and resolution coordinated with Task 013
- [ ] Post-rebase validation coordinated with Task 014
- [ ] Rollback mechanisms coordinated with Task 015
- [ ] Progress tracking and reporting functional

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <15 seconds for orchestration operations
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

### Integration Readiness
- [ ] Compatible with Task 010 requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 004 (Git operations framework) complete
- [ ] Task 006 (Backup/restore mechanism) complete
- [ ] Task 007 (Feature branch identification) complete
- [ ] Task 012 (Branch backup and safety) complete
- [ ] Task 013 (Conflict detection and resolution) complete
- [ ] Task 014 (Validation and verification) complete
- [ ] Task 015 (Rollback and recovery) complete
- [ ] Task 022 (Architectural migration) complete
- [ ] GitPython or subprocess for git commands available
- [ ] Test infrastructure in place

### Blocks (What This Task Unblocks)
- Task 010 (Complex branch alignment)
- Task 011 (Validation integration)

### External Dependencies
- Python 3.8+
- GitPython or subprocess for git commands
- Specialized tasks (012, 013, 014, 015)

---

## Subtasks Breakdown

### 009.1: Integrate Optimal Primary Target Determination
**Effort:** 2-3 hours
**Depends on:** None

Develop logic to receive and validate the optimal primary branch target (e.g., main, scientific, orchestration-tools) for the feature branch, likely from Task 007.

**Details:**
The Python script will take the feature branch name and its determined primary target as input. This subtask focuses on how this input is consumed and validated against known primary branches. Leverage outputs from Task 007's categorization tool.

**Success Criteria:**
- [ ] Optimal primary target received from Task 007
- [ ] Target validated against known primary branches
- [ ] Invalid targets handled gracefully
- [ ] Input validation comprehensive

---

### 009.2: Coordinate Initial Environment Setup and Safety Checks
**Effort:** 3-4 hours
**Depends on:** 009.1

Before any Git operations, coordinate safety checks with Task 012 (Branch Backup and Safety).

**Details:**
Coordinate with Task 012 to ensure a clean working directory and valid repository state, preventing unintended data loss or conflicts. This subtask focuses on orchestrating the safety validation rather than implementing it directly.

**Success Criteria:**
- [ ] Coordination with Task 012 implemented
- [ ] Working directory validated
- [ ] Repository state verified
- [ ] Safety checks completed before proceeding

---

### 009.3: Coordinate Local Feature Branch Backup
**Effort:** 3-4 hours
**Depends on:** 009.2

Coordinate with Task 012 (Branch Backup and Safety) to create a temporary backup of the feature branch's current state before initiating any rebase operations.

**Details:**
Delegate the backup creation to Task 012's BranchBackupManager. This ensures the backup mechanism is handled by the specialized task while Task 009 coordinates the overall process.

**Success Criteria:**
- [ ] Coordination with Task 012 implemented
- [ ] Backup created before Git operations
- [ ] Backup verification completed
- [ ] Backup reference stored for potential rollback

---

### 009.4: Implement Branch Switching Logic
**Effort:** 2-3 hours
**Depends on:** 009.3

Write the Python code to programmatically switch the local Git repository to the specified feature branch.

**Details:**
Utilize `GitPython`'s `repo.git.checkout(feature_branch_name)` or `subprocess.run(['git', 'checkout', feature_branch_name], cwd=repo_path, check=True)`.

**Success Criteria:**
- [ ] Branch switching implemented with GitPython
- [ ] Error handling for invalid branch names
- [ ] Successful checkout confirmed
- [ ] Branch state verified after switching

---

### 009.5: Implement Remote Primary Branch Fetch Logic
**Effort:** 2-3 hours
**Depends on:** 009.4

Develop the code to fetch the latest changes from the determined primary target branch (`git fetch origin <primary_target>`).

**Details:**
Use `GitPython`'s `repo.remote('origin').fetch(primary_target_name)` or `subprocess.run(['git', 'fetch', 'origin', primary_target_name], cwd=repo_path, check=True)`. Include error handling for network issues or non-existent remotes/branches.

**Success Criteria:**
- [ ] Remote fetch implemented with GitPython
- [ ] Error handling for network issues
- [ ] Fetch verification completed
- [ ] Primary branch updates retrieved

---

### 009.6: Coordinate Core Rebase Initiation with Specialized Tasks
**Effort:** 4-5 hours
**Depends on:** 009.5

Coordinate the command execution for initiating the Git rebase operation, leveraging specialized tasks for complex operations.

**Details:**
Execute `subprocess.run(['git', 'rebase', f'origin/{primary_target_name}'], cwd=repo_path, check=True, capture_output=True, text=True)` or `repo.git.rebase(f'origin/{primary_target_name}')`. Capture output for status and potential conflict detection. Coordinate with Task 013 for advanced rebase strategies.

**Success Criteria:**
- [ ] Rebase initiation coordinated
- [ ] Output captured for status analysis
- [ ] Conflict detection prepared
- [ ] Error handling implemented

---

### 009.7: Coordinate Conflict Detection and Resolution
**Effort:** 4-5 hours
**Depends on:** 009.6

Coordinate with Task 013 (Conflict Detection and Resolution) when the rebase operation encounters conflicts.

**Details:**
Delegate conflict detection and resolution to Task 013's ConflictDetectionResolver. This subtask focuses on orchestrating the handoff to the specialized conflict resolution task rather than implementing conflict handling directly.

**Success Criteria:**
- [ ] Coordination with Task 013 implemented
- [ ] Conflict detection handoff operational
- [ ] Resolution guidance provided
- [ ] Resolution status monitored

---

### 009.8: Coordinate Post-Rebase Validation
**Effort:** 3-4 hours
**Depends on:** 009.7

Coordinate with Task 014 (Validation and Verification) to perform automated checks to validate the integrity and correctness of the rebased feature branch.

**Details:**
Delegate validation to Task 014's ValidationVerificationFramework. This ensures comprehensive and consistent validation procedures.

**Success Criteria:**
- [ ] Coordination with Task 014 implemented
- [ ] Validation procedures executed
- [ ] Integrity checks completed
- [ ] Validation results processed

---

### 009.9: Coordinate Rollback to Backup Mechanism
**Effort:** 3-4 hours
**Depends on:** 009.6

Coordinate with Task 015 (Rollback and Recovery) to revert the feature branch to its pre-alignment backup state if a rebase operation ultimately fails or is aborted by the user.

**Details:**
Delegate rollback operations to Task 015's RollbackRecoveryMechanisms. This ensures reliable and consistent rollback procedures.

**Success Criteria:**
- [ ] Coordination with Task 015 implemented
- [ ] Rollback procedures available
- [ ] Backup restoration functional
- [ ] Rollback status tracked

---

### 009.10: Develop Progress Tracking and User Feedback
**Effort:** 2-3 hours
**Depends on:** 009.6, 009.7, 009.8

Add clear progress indicators and descriptive messages throughout the alignment process to keep the user informed.

**Details:**
Implement logging statements for each major step: fetching, checking out branch, initiating rebase, detecting conflicts, etc. Coordinate with specialized tasks to provide unified progress reporting.

**Success Criteria:**
- [ ] Progress indicators implemented
- [ ] User feedback provided at each step
- [ ] Unified reporting coordinated
- [ ] Status updates timely and informative

---

## Specification

### Module Interface

```python
class CoreAlignmentOrchestrator:
    def __init__(self, repo_path: str, config_path: str = None)
    def align_branch(self, feature_branch: str, primary_target: str) -> AlignmentResult
    def coordinate_with_task_012_safety(self, branch_name: str) -> SafetyCheckResult
    def coordinate_with_task_013_conflicts(self, branch_name: str) -> ConflictResolutionResult
    def coordinate_with_task_014_validation(self, branch_name: str) -> ValidationResult
    def coordinate_with_task_015_rollback(self, branch_name: str, backup_ref: str) -> RollbackResult
```

### Output Format

```json
{
  "alignment_operation": {
    "operation_id": "align-20260112-120000-001",
    "feature_branch": "feature/auth-system",
    "primary_target": "main",
    "status": "completed",
    "start_time": "2026-01-12T12:00:00Z",
    "end_time": "2026-01-12T12:05:00Z",
    "duration_seconds": 300
  },
  "coordinated_tasks": {
    "task_012_safety": {
      "status": "completed",
      "backup_created": "feature-auth-system-backup-20260112-120000",
      "safety_checks_passed": true
    },
    "task_013_conflicts": {
      "status": "completed",
      "conflicts_detected": 2,
      "conflicts_resolved": 2,
      "resolution_time_seconds": 120
    },
    "task_014_validation": {
      "status": "completed",
      "validation_passed": true,
      "issues_found": 0
    },
    "task_015_rollback": {
      "status": "not_needed",
      "backup_preserved": true
    }
  },
  "alignment_result": {
    "success": true,
    "commits_aligned": 15,
    "new_ancestor_commit": "a1b2c3d4e5f6",
    "linear_history_maintained": true
  },
  "performance_metrics": {
    "total_time_seconds": 300,
    "breakdown": {
      "safety_checks": 5,
      "backup_creation": 8,
      "rebase_operation": 180,
      "conflict_resolution": 120,
      "validation": 15,
      "cleanup": 2
    }
  }
}
```

---

## Implementation Guide

### 009.6: Coordinate Core Rebase Initiation with Specialized Tasks

**Objective:** Coordinate the core rebase operation with specialized tasks

**Detailed Steps:**

1. Prepare rebase command with proper error handling
   ```python
   def coordinate_rebase_initiation(self, feature_branch: str, primary_target: str) -> RebaseResult:
       try:
           # Switch to feature branch first
           self.repo.git.checkout(feature_branch)

           # Fetch latest from primary target
           self.repo.remote('origin').fetch(primary_target)

           # Execute rebase operation
           result = self.repo.git.rebase(f'origin/{primary_target}',
                                        capture_output=True,
                                        with_extended_output=True)

           # Check if rebase completed successfully
           if result.returncode == 0:
               return RebaseResult(
                   success=True,
                   output=result.stdout,
                   rebase_in_progress=False,
                   conflicts_resolved=0
               )
           else:
               # Check if it's a conflict (return code 1 is often conflicts)
               if 'CONFLICT' in result.stderr or self.repo.is_dirty(untracked_files=True):
                   return RebaseResult(
                       success=False,
                       output=result.stdout,
                       error=result.stderr,
                       rebase_in_progress=True,  # Conflicts to resolve
                       conflicts_resolved=0
                   )
               else:
                   # Actual error
                   return RebaseResult(
                       success=False,
                       output=result.stdout,
                       error=result.stderr,
                       rebase_in_progress=False,
                       conflicts_resolved=0
                   )
       except GitCommandError as e:
           return RebaseResult(
               success=False,
               output="",
               error=str(e),
               rebase_in_progress=False,
               conflicts_resolved=0
           )
   ```

2. Coordinate with Task 013 for conflict resolution
   ```python
   def handle_rebase_conflicts(self, feature_branch: str) -> ConflictResolutionResult:
       # Detect conflicts
       unmerged_blobs = self.repo.index.unmerged_blobs()
       conflicted_files = list(unmerged_blobs.keys())

       if not conflicted_files:
           return ConflictResolutionResult(
               conflicts_detected=False,
               files_affected=[],
               resolution_status="no_conflicts"
           )

       # Coordinate with Task 013 for conflict resolution
       conflict_resolver = Task013ConflictDetectorResolver(self.repo.working_dir)
       resolution_result = conflict_resolver.resolve_conflicts(
           branch_name=feature_branch,
           conflicted_files=conflicted_files
       )

       return resolution_result
   ```

3. Implement proper error handling
   ```python
   def safe_rebase_operation(self, feature_branch: str, primary_target: str) -> SafeRebaseResult:
       original_branch = self.repo.active_branch.name

       try:
           # Ensure we're on the right branch
           if original_branch != feature_branch:
               self.repo.git.checkout(feature_branch)

           # Fetch latest from target
           self.repo.remote('origin').fetch(primary_target)

           # Attempt rebase
           rebase_result = self.coordinate_rebase_initiation(feature_branch, primary_target)

           # If conflicts occurred, handle them
           if not rebase_result.success and rebase_result.rebase_in_progress:
               conflict_result = self.handle_rebase_conflicts(feature_branch)
               rebase_result.conflicts_resolved = conflict_result.conflicts_resolved

               # If conflicts were resolved, continue rebase
               if conflict_result.resolution_status == "completed":
                   try:
                       self.repo.git.rebase('--continue')
                       rebase_result.success = True
                       rebase_result.rebase_in_progress = False
                   except GitCommandError:
                       # If continue fails, we might need to abort
                       pass

           return SafeRebaseResult(
               rebase_result=rebase_result,
               original_branch=original_branch,
               operation_successful=rebase_result.success
           )
       except Exception as e:
           # Ensure we return to original branch on error
           if self.repo.active_branch.name != original_branch:
               self.repo.git.checkout(original_branch)
           raise e
   ```

4. Test with various rebase scenarios

**Testing:**
- Successful rebases should complete properly
- Conflicts should be detected and handled
- Error conditions should be handled gracefully
- Branch state should be preserved appropriately

**Performance:**
- Must complete in <5 seconds for typical rebases
- Memory: <10 MB per operation

---

## Configuration Parameters

Create `config/task_009_alignment_orchestration.yaml`:

```yaml
alignment:
  primary_targets: ["main", "scientific", "orchestration-tools"]
  rebase_timeout_minutes: 10
  conflict_resolution_enabled: true
  validation_after_rebase: true
  rollback_on_failure: true
  progress_reporting: true

coordination:
  task_012_integration: true
  task_013_integration: true
  task_014_integration: true
  task_015_integration: true
  safety_check_timeout_seconds: 30
  validation_timeout_seconds: 60

rebase:
  strategy: "rebase"  # rebase, merge, cherry-pick
  preserve_merges: false
  autosquash: false
  git_command_timeout_seconds: 30
```

Load in code:
```python
import yaml

with open('config/task_009_alignment_orchestration.yaml') as f:
    CONFIG = yaml.safe_load(f)

# Use: CONFIG['alignment']['primary_targets']
```

---

## Performance Targets

### Per Component
- Branch switching: <1 second
- Remote fetch: <2 seconds
- Rebase initiation: <3 seconds
- Conflict coordination: <5 seconds
- Memory usage: <15 MB per operation

### Scalability
- Handle repositories with 10,000+ commits
- Support multiple concurrent alignment operations
- Efficient for large file repositories

### Quality Metrics
- No timeouts on standard hardware
- Consistent performance across repository sizes
- Reliable coordination with specialized tasks

---

## Testing Strategy

### Unit Tests

Minimum 8 test cases:

```python
def test_optimal_target_integration():
    # Optimal target determination should integrate properly

def test_safety_check_coordination():
    # Coordination with Task 012 safety checks should work

def test_backup_coordination():
    # Coordination with Task 012 backup should work

def test_rebase_initiation_coordination():
    # Coordination of rebase initiation should work

def test_conflict_resolution_coordination():
    # Coordination with Task 013 should work

def test_validation_coordination():
    # Coordination with Task 014 should work

def test_rollback_coordination():
    # Coordination with Task 015 should work

def test_performance():
    # Operations complete within performance targets
```

### Integration Tests

After all subtasks complete:

```python
def test_full_alignment_orchestration():
    # Verify 009 output is compatible with Task 010 input

def test_alignment_integration():
    # Validate orchestration works with real repositories
```

### Coverage Target
- Code coverage: > 95%
- All edge cases covered
- All error paths tested

---

## Common Gotchas & Solutions

**Gotcha 1: Branch state management during rebase**
```python
# WRONG
not tracking original branch state during rebase operations

# RIGHT
save original branch state and restore if needed
```

**Gotcha 2: Conflict detection**
```python
# WRONG
only checking return code to detect conflicts

# RIGHT
check both return code and repository state for conflicts
```

**Gotcha 3: Coordination with specialized tasks**
```python
# WRONG
tight coupling with specialized task implementations

# RIGHT
loose coupling through well-defined interfaces
```

**Gotcha 4: Error propagation**
```python
# WRONG
not properly propagating errors from specialized tasks

# RIGHT
proper error handling and propagation from all coordinated tasks
```

---

## Integration Checkpoint

**When to move to Task 010 (Complex alignment):**

- [ ] All 10 subtasks complete
- [ ] Unit tests passing (>95% coverage)
- [ ] Core alignment orchestration working
- [ ] No validation errors on test data
- [ ] Performance targets met (<15s for operations)
- [ ] Integration with specialized tasks validated
- [ ] Code review approved
- [ ] Commit message: "feat: complete Task 009 Core Alignment Orchestration"

---

## Done Definition

Task 009 is done when:

1. ✅ All 10 subtasks marked complete
2. ✅ Unit tests pass (>95% coverage) on CI/CD
3. ✅ Code review approved
4. ✅ Outputs match specification exactly
5. ✅ Output schema validation passes
6. ✅ Documentation complete and accurate
7. ✅ Performance benchmarks met
8. ✅ Ready for hand-off to Task 010
9. ✅ Commit: "feat: complete Task 009 Core Alignment Orchestration"
10. ✅ All success criteria checkboxes marked complete

---

## Next Steps

1. **Immediate:** Implement subtask 009.1 (Integrate Optimal Target Determination)
2. **Week 1:** Complete subtasks 009.1 through 009.5
3. **Week 2:** Complete subtasks 009.6 through 009.10
4. **Week 2:** Write and test unit tests (target: >95%)
5. **Week 2:** Code review
6. **Week 2:** Ready for Task 010 (Complex alignment)

**Reference:** See IMPLEMENTATION_INDEX.md for team coordination
**Priority:** High
**Effort:** 28-40 hours
**Complexity:** 8/10
**Dependencies:** 004, 006, 007, 012, 013, 014, 015, 022

---

## Purpose

Implement the core orchestrator for multistage branch alignment operations that coordinates with specialized tasks for backup/safety (Task 012), conflict resolution (Task 013), validation (Task 014), and rollback/recovery (Task 015). This task serves as the main entry point for the alignment process while delegating specialized operations to dedicated tasks.

**Scope:** Core alignment orchestration only
**Blocks:** Task 010 (Complex branch alignment), Task 011 (Validation integration)

---

## Success Criteria

Task 009 is complete when:

### Core Functionality
- [ ] Optimal primary target determination integration operational
- [ ] Environment setup and safety checks coordinated with Task 012
- [ ] Branch switching and fetching logic operational
- [ ] Core rebase initiation coordinated with specialized tasks
- [ ] Conflict detection and resolution coordinated with Task 013
- [ ] Post-rebase validation coordinated with Task 014
- [ ] Rollback mechanisms coordinated with Task 015
- [ ] Progress tracking and reporting functional

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <15 seconds for orchestration operations
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

### Integration Readiness
- [ ] Compatible with Task 010 requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 004 (Git operations framework) complete
- [ ] Task 006 (Backup/restore mechanism) complete
- [ ] Task 007 (Feature branch identification) complete
- [ ] Task 012 (Branch backup and safety) complete
- [ ] Task 013 (Conflict detection and resolution) complete
- [ ] Task 014 (Validation and verification) complete
- [ ] Task 015 (Rollback and recovery) complete
- [ ] Task 022 (Architectural migration) complete
- [ ] GitPython or subprocess for git commands available
- [ ] Test infrastructure in place

### Blocks (What This Task Unblocks)
- Task 010 (Complex branch alignment)
- Task 011 (Validation integration)

### External Dependencies
- Python 3.8+
- GitPython or subprocess for git commands
- Specialized tasks (012, 013, 014, 015)

---

## Subtasks Breakdown

### 009.1: Integrate Optimal Primary Target Determination
**Effort:** 2-3 hours
**Depends on:** None

Develop logic to receive and validate the optimal primary branch target (e.g., main, scientific, orchestration-tools) for the feature branch, likely from Task 007.

**Details:**
The Python script will take the feature branch name and its determined primary target as input. This subtask focuses on how this input is consumed and validated against known primary branches. Leverage outputs from Task 007's categorization tool.

**Success Criteria:**
- [ ] Optimal primary target received from Task 007
- [ ] Target validated against known primary branches
- [ ] Invalid targets handled gracefully
- [ ] Input validation comprehensive

---

### 009.2: Coordinate Initial Environment Setup and Safety Checks
**Effort:** 3-4 hours
**Depends on:** 009.1

Before any Git operations, coordinate safety checks with Task 012 (Branch Backup and Safety).

**Details:**
Coordinate with Task 012 to ensure a clean working directory and valid repository state, preventing unintended data loss or conflicts. This subtask focuses on orchestrating the safety validation rather than implementing it directly.

**Success Criteria:**
- [ ] Coordination with Task 012 implemented
- [ ] Working directory validated
- [ ] Repository state verified
- [ ] Safety checks completed before proceeding

---

### 009.3: Coordinate Local Feature Branch Backup
**Effort:** 3-4 hours
**Depends on:** 009.2

Coordinate with Task 012 (Branch Backup and Safety) to create a temporary backup of the feature branch's current state before initiating any rebase operations.

**Details:**
Delegate the backup creation to Task 012's BranchBackupManager. This ensures the backup mechanism is handled by the specialized task while Task 009 coordinates the overall process.

**Success Criteria:**
- [ ] Coordination with Task 012 implemented
- [ ] Backup created before Git operations
- [ ] Backup verification completed
- [ ] Backup reference stored for potential rollback

---

### 009.4: Implement Branch Switching Logic
**Effort:** 2-3 hours
**Depends on:** 009.3

Write the Python code to programmatically switch the local Git repository to the specified feature branch.

**Details:**
Utilize `GitPython`'s `repo.git.checkout(feature_branch_name)` or `subprocess.run(['git', 'checkout', feature_branch_name], cwd=repo_path, check=True)`.

**Success Criteria:**
- [ ] Branch switching implemented with GitPython
- [ ] Error handling for invalid branch names
- [ ] Successful checkout confirmed
- [ ] Branch state verified after switching

---

### 009.5: Implement Remote Primary Branch Fetch Logic
**Effort:** 2-3 hours
**Depends on:** 009.4

Develop the code to fetch the latest changes from the determined primary target branch (`git fetch origin <primary_target>`).

**Details:**
Use `GitPython`'s `repo.remote('origin').fetch(primary_target_name)` or `subprocess.run(['git', 'fetch', 'origin', primary_target_name], cwd=repo_path, check=True)`. Include error handling for network issues or non-existent remotes/branches.

**Success Criteria:**
- [ ] Remote fetch implemented with GitPython
- [ ] Error handling for network issues
- [ ] Fetch verification completed
- [ ] Primary branch updates retrieved

---

### 009.6: Coordinate Core Rebase Initiation with Specialized Tasks
**Effort:** 4-5 hours
**Depends on:** 009.5

Coordinate the command execution for initiating the Git rebase operation, leveraging specialized tasks for complex operations.

**Details:**
Execute `subprocess.run(['git', 'rebase', f'origin/{primary_target_name}'], cwd=repo_path, check=True, capture_output=True, text=True)` or `repo.git.rebase(f'origin/{primary_target_name}')`. Capture output for status and potential conflict detection. Coordinate with Task 013 for advanced rebase strategies.

**Success Criteria:**
- [ ] Rebase initiation coordinated
- [ ] Output captured for status analysis
- [ ] Conflict detection prepared
- [ ] Error handling implemented

---

### 009.7: Coordinate Conflict Detection and Resolution
**Effort:** 4-5 hours
**Depends on:** 009.6

Coordinate with Task 013 (Conflict Detection and Resolution) when the rebase operation encounters conflicts.

**Details:**
Delegate conflict detection and resolution to Task 013's ConflictDetectionResolver. This subtask focuses on orchestrating the handoff to the specialized conflict resolution task rather than implementing conflict handling directly.

**Success Criteria:**
- [ ] Coordination with Task 013 implemented
- [ ] Conflict detection handoff operational
- [ ] Resolution guidance provided
- [ ] Resolution status monitored

---

### 009.8: Coordinate Post-Rebase Validation
**Effort:** 3-4 hours
**Depends on:** 009.7

Coordinate with Task 014 (Validation and Verification) to perform automated checks to validate the integrity and correctness of the rebased feature branch.

**Details:**
Delegate validation to Task 014's ValidationVerificationFramework. This ensures comprehensive and consistent validation procedures.

**Success Criteria:**
- [ ] Coordination with Task 014 implemented
- [ ] Validation procedures executed
- [ ] Integrity checks completed
- [ ] Validation results processed

---

### 009.9: Coordinate Rollback to Backup Mechanism
**Effort:** 3-4 hours
**Depends on:** 009.6

Coordinate with Task 015 (Rollback and Recovery) to revert the feature branch to its pre-alignment backup state if a rebase operation ultimately fails or is aborted by the user.

**Details:**
Delegate rollback operations to Task 015's RollbackRecoveryMechanisms. This ensures reliable and consistent rollback procedures.

**Success Criteria:**
- [ ] Coordination with Task 015 implemented
- [ ] Rollback procedures available
- [ ] Backup restoration functional
- [ ] Rollback status tracked

---

### 009.10: Develop Progress Tracking and User Feedback
**Effort:** 2-3 hours
**Depends on:** 009.6, 009.7, 009.8

Add clear progress indicators and descriptive messages throughout the alignment process to keep the user informed.

**Details:**
Implement logging statements for each major step: fetching, checking out branch, initiating rebase, detecting conflicts, etc. Coordinate with specialized tasks to provide unified progress reporting.

**Success Criteria:**
- [ ] Progress indicators implemented
- [ ] User feedback provided at each step
- [ ] Unified reporting coordinated
- [ ] Status updates timely and informative

---

## Specification

### Module Interface

```python
class CoreAlignmentOrchestrator:
    def __init__(self, repo_path: str, config_path: str = None)
    def align_branch(self, feature_branch: str, primary_target: str) -> AlignmentResult
    def coordinate_with_task_012_safety(self, branch_name: str) -> SafetyCheckResult
    def coordinate_with_task_013_conflicts(self, branch_name: str) -> ConflictResolutionResult
    def coordinate_with_task_014_validation(self, branch_name: str) -> ValidationResult
    def coordinate_with_task_015_rollback(self, branch_name: str, backup_ref: str) -> RollbackResult
```

### Output Format

```json
{
  "alignment_operation": {
    "operation_id": "align-20260112-120000-001",
    "feature_branch": "feature/auth-system",
    "primary_target": "main",
    "status": "completed",
    "start_time": "2026-01-12T12:00:00Z",
    "end_time": "2026-01-12T12:05:00Z",
    "duration_seconds": 300
  },
  "coordinated_tasks": {
    "task_012_safety": {
      "status": "completed",
      "backup_created": "feature-auth-system-backup-20260112-120000",
      "safety_checks_passed": true
    },
    "task_013_conflicts": {
      "status": "completed",
      "conflicts_detected": 2,
      "conflicts_resolved": 2,
      "resolution_time_seconds": 120
    },
    "task_014_validation": {
      "status": "completed",
      "validation_passed": true,
      "issues_found": 0
    },
    "task_015_rollback": {
      "status": "not_needed",
      "backup_preserved": true
    }
  },
  "alignment_result": {
    "success": true,
    "commits_aligned": 15,
    "new_ancestor_commit": "a1b2c3d4e5f6",
    "linear_history_maintained": true
  },
  "performance_metrics": {
    "total_time_seconds": 300,
    "breakdown": {
      "safety_checks": 5,
      "backup_creation": 8,
      "rebase_operation": 180,
      "conflict_resolution": 120,
      "validation": 15,
      "cleanup": 2
    }
  }
}
```

---

## Implementation Guide

### 009.6: Coordinate Core Rebase Initiation with Specialized Tasks

**Objective:** Coordinate the core rebase operation with specialized tasks

**Detailed Steps:**

1. Prepare rebase command with proper error handling
   ```python
   def coordinate_rebase_initiation(self, feature_branch: str, primary_target: str) -> RebaseResult:
       try:
           # Switch to feature branch first
           self.repo.git.checkout(feature_branch)

           # Fetch latest from primary target
           self.repo.remote('origin').fetch(primary_target)

           # Execute rebase operation
           result = self.repo.git.rebase(f'origin/{primary_target}',
                                        capture_output=True,
                                        with_extended_output=True)

           # Check if rebase completed successfully
           if result.returncode == 0:
               return RebaseResult(
                   success=True,
                   output=result.stdout,
                   rebase_in_progress=False,
                   conflicts_resolved=0
               )
           else:
               # Check if it's a conflict (return code 1 is often conflicts)
               if 'CONFLICT' in result.stderr or self.repo.is_dirty(untracked_files=True):
                   return RebaseResult(
                       success=False,
                       output=result.stdout,
                       error=result.stderr,
                       rebase_in_progress=True,  # Conflicts to resolve
                       conflicts_resolved=0
                   )
               else:
                   # Actual error
                   return RebaseResult(
                       success=False,
                       output=result.stdout,
                       error=result.stderr,
                       rebase_in_progress=False,
                       conflicts_resolved=0
                   )
       except GitCommandError as e:
           return RebaseResult(
               success=False,
               output="",
               error=str(e),
               rebase_in_progress=False,
               conflicts_resolved=0
           )
   ```

2. Coordinate with Task 013 for conflict resolution
   ```python
   def handle_rebase_conflicts(self, feature_branch: str) -> ConflictResolutionResult:
       # Detect conflicts
       unmerged_blobs = self.repo.index.unmerged_blobs()
       conflicted_files = list(unmerged_blobs.keys())

       if not conflicted_files:
           return ConflictResolutionResult(
               conflicts_detected=False,
               files_affected=[],
               resolution_status="no_conflicts"
           )

       # Coordinate with Task 013 for conflict resolution
       conflict_resolver = Task013ConflictDetectorResolver(self.repo.working_dir)
       resolution_result = conflict_resolver.resolve_conflicts(
           branch_name=feature_branch,
           conflicted_files=conflicted_files
       )

       return resolution_result
   ```

3. Implement proper error handling
   ```python
   def safe_rebase_operation(self, feature_branch: str, primary_target: str) -> SafeRebaseResult:
       original_branch = self.repo.active_branch.name

       try:
           # Ensure we're on the right branch
           if original_branch != feature_branch:
               self.repo.git.checkout(feature_branch)

           # Fetch latest from target
           self.repo.remote('origin').fetch(primary_target)

           # Attempt rebase
           rebase_result = self.coordinate_rebase_initiation(feature_branch, primary_target)

           # If conflicts occurred, handle them
           if not rebase_result.success and rebase_result.rebase_in_progress:
               conflict_result = self.handle_rebase_conflicts(feature_branch)
               rebase_result.conflicts_resolved = conflict_result.conflicts_resolved

               # If conflicts were resolved, continue rebase
               if conflict_result.resolution_status == "completed":
                   try:
                       self.repo.git.rebase('--continue')
                       rebase_result.success = True
                       rebase_result.rebase_in_progress = False
                   except GitCommandError:
                       # If continue fails, we might need to abort
                       pass

           return SafeRebaseResult(
               rebase_result=rebase_result,
               original_branch=original_branch,
               operation_successful=rebase_result.success
           )
       except Exception as e:
           # Ensure we return to original branch on error
           if self.repo.active_branch.name != original_branch:
               self.repo.git.checkout(original_branch)
           raise e
   ```

4. Test with various rebase scenarios

**Testing:**
- Successful rebases should complete properly
- Conflicts should be detected and handled
- Error conditions should be handled gracefully
- Branch state should be preserved appropriately

**Performance:**
- Must complete in <5 seconds for typical rebases
- Memory: <10 MB per operation

---

## Configuration Parameters

Create `config/task_009_alignment_orchestration.yaml`:

```yaml
alignment:
  primary_targets: ["main", "scientific", "orchestration-tools"]
  rebase_timeout_minutes: 10
  conflict_resolution_enabled: true
  validation_after_rebase: true
  rollback_on_failure: true
  progress_reporting: true

coordination:
  task_012_integration: true
  task_013_integration: true
  task_014_integration: true
  task_015_integration: true
  safety_check_timeout_seconds: 30
  validation_timeout_seconds: 60

rebase:
  strategy: "rebase"  # rebase, merge, cherry-pick
  preserve_merges: false
  autosquash: false
  git_command_timeout_seconds: 30
```

Load in code:
```python
import yaml

with open('config/task_009_alignment_orchestration.yaml') as f:
    CONFIG = yaml.safe_load(f)

# Use: CONFIG['alignment']['primary_targets']
```

---

## Performance Targets

### Per Component
- Branch switching: <1 second
- Remote fetch: <2 seconds
- Rebase initiation: <3 seconds
- Conflict coordination: <5 seconds
- Memory usage: <15 MB per operation

### Scalability
- Handle repositories with 10,000+ commits
- Support multiple concurrent alignment operations
- Efficient for large file repositories

### Quality Metrics
- No timeouts on standard hardware
- Consistent performance across repository sizes
- Reliable coordination with specialized tasks

---

## Testing Strategy

### Unit Tests

Minimum 8 test cases:

```python
def test_optimal_target_integration():
    # Optimal target determination should integrate properly

def test_safety_check_coordination():
    # Coordination with Task 012 safety checks should work

def test_backup_coordination():
    # Coordination with Task 012 backup should work

def test_rebase_initiation_coordination():
    # Coordination of rebase initiation should work

def test_conflict_resolution_coordination():
    # Coordination with Task 013 should work

def test_validation_coordination():
    # Coordination with Task 014 should work

def test_rollback_coordination():
    # Coordination with Task 015 should work

def test_performance():
    # Operations complete within performance targets
```

### Integration Tests

After all subtasks complete:

```python
def test_full_alignment_orchestration():
    # Verify 009 output is compatible with Task 010 input

def test_alignment_integration():
    # Validate orchestration works with real repositories
```

### Coverage Target
- Code coverage: > 95%
- All edge cases covered
- All error paths tested

---

## Common Gotchas & Solutions

**Gotcha 1: Branch state management during rebase**
```python
# WRONG
not tracking original branch state during rebase operations

# RIGHT
save original branch state and restore if needed
```

**Gotcha 2: Conflict detection**
```python
# WRONG
only checking return code to detect conflicts

# RIGHT
check both return code and repository state for conflicts
```

**Gotcha 3: Coordination with specialized tasks**
```python
# WRONG
tight coupling with specialized task implementations

# RIGHT
loose coupling through well-defined interfaces
```

**Gotcha 4: Error propagation**
```python
# WRONG
not properly propagating errors from specialized tasks

# RIGHT
proper error handling and propagation from all coordinated tasks
```

---

## Integration Checkpoint

**When to move to Task 010 (Complex alignment):**

- [ ] All 10 subtasks complete
- [ ] Unit tests passing (>95% coverage)
- [ ] Core alignment orchestration working
- [ ] No validation errors on test data
- [ ] Performance targets met (<15s for operations)
- [ ] Integration with specialized tasks validated
- [ ] Code review approved
- [ ] Commit message: "feat: complete Task 009 Core Alignment Orchestration"

---

## Done Definition

Task 009 is done when:

1. ✅ All 10 subtasks marked complete
2. ✅ Unit tests pass (>95% coverage) on CI/CD
3. ✅ Code review approved
4. ✅ Outputs match specification exactly
5. ✅ Output schema validation passes
6. ✅ Documentation complete and accurate
7. ✅ Performance benchmarks met
8. ✅ Ready for hand-off to Task 010
9. ✅ Commit: "feat: complete Task 009 Core Alignment Orchestration"
10. ✅ All success criteria checkboxes marked complete

---

## Next Steps

1. **Immediate:** Implement subtask 009.1 (Integrate Optimal Target Determination)
2. **Week 1:** Complete subtasks 009.1 through 009.5
3. **Week 2:** Complete subtasks 009.6 through 009.10
4. **Week 2:** Write and test unit tests (target: >95%)
5. **Week 2:** Code review
6. **Week 2:** Ready for Task 010 (Complex alignment)

**Reference:** See IMPLEMENTATION_INDEX.md for team coordination
**Dependencies:** 004, 006, 007, 012, 013, 014, 015, 022

---

## Purpose

Implement the core orchestrator for multistage branch alignment operations that coordinates with specialized tasks for backup/safety (Task 012), conflict resolution (Task 013), validation (Task 014), and rollback/recovery (Task 015). This task serves as the main entry point for the alignment process while delegating specialized operations to dedicated tasks.

**Scope:** Core alignment orchestration only
**Blocks:** Task 010 (Complex branch alignment), Task 011 (Validation integration)

---

## Success Criteria

Task 009 is complete when:

### Core Functionality
- [ ] Optimal primary target determination integration operational
- [ ] Environment setup and safety checks coordinated with Task 012
- [ ] Branch switching and fetching logic operational
- [ ] Core rebase initiation coordinated with specialized tasks
- [ ] Conflict detection and resolution coordinated with Task 013
- [ ] Post-rebase validation coordinated with Task 014
- [ ] Rollback mechanisms coordinated with Task 015
- [ ] Progress tracking and reporting functional

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <15 seconds for orchestration operations
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

### Integration Readiness
- [ ] Compatible with Task 010 requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 004 (Git operations framework) complete
- [ ] Task 006 (Backup/restore mechanism) complete
- [ ] Task 007 (Feature branch identification) complete
- [ ] Task 012 (Branch backup and safety) complete
- [ ] Task 013 (Conflict detection and resolution) complete
- [ ] Task 014 (Validation and verification) complete
- [ ] Task 015 (Rollback and recovery) complete
- [ ] Task 022 (Architectural migration) complete
- [ ] GitPython or subprocess for git commands available
- [ ] Test infrastructure in place

### Blocks (What This Task Unblocks)
- Task 010 (Complex branch alignment)
- Task 011 (Validation integration)

### External Dependencies
- Python 3.8+
- GitPython or subprocess for git commands
- Specialized tasks (012, 013, 014, 015)

---

## Subtasks Breakdown

### 009.1: Integrate Optimal Primary Target Determination
**Effort:** 2-3 hours
**Depends on:** None

Develop logic to receive and validate the optimal primary branch target (e.g., main, scientific, orchestration-tools) for the feature branch, likely from Task 007.

**Details:**
The Python script will take the feature branch name and its determined primary target as input. This subtask focuses on how this input is consumed and validated against known primary branches. Leverage outputs from Task 007's categorization tool.

**Success Criteria:**
- [ ] Optimal primary target received from Task 007
- [ ] Target validated against known primary branches
- [ ] Invalid targets handled gracefully
- [ ] Input validation comprehensive

---

### 009.2: Coordinate Initial Environment Setup and Safety Checks
**Effort:** 3-4 hours
**Depends on:** 009.1

Before any Git operations, coordinate safety checks with Task 012 (Branch Backup and Safety).

**Details:**
Coordinate with Task 012 to ensure a clean working directory and valid repository state, preventing unintended data loss or conflicts. This subtask focuses on orchestrating the safety validation rather than implementing it directly.

**Success Criteria:**
- [ ] Coordination with Task 012 implemented
- [ ] Working directory validated
- [ ] Repository state verified
- [ ] Safety checks completed before proceeding

---

### 009.3: Coordinate Local Feature Branch Backup
**Effort:** 3-4 hours
**Depends on:** 009.2

Coordinate with Task 012 (Branch Backup and Safety) to create a temporary backup of the feature branch's current state before initiating any rebase operations.

**Details:**
Delegate the backup creation to Task 012's BranchBackupManager. This ensures the backup mechanism is handled by the specialized task while Task 009 coordinates the overall process.

**Success Criteria:**
- [ ] Coordination with Task 012 implemented
- [ ] Backup created before Git operations
- [ ] Backup verification completed
- [ ] Backup reference stored for potential rollback

---

### 009.4: Implement Branch Switching Logic
**Effort:** 2-3 hours
**Depends on:** 009.3

Write the Python code to programmatically switch the local Git repository to the specified feature branch.

**Details:**
Utilize `GitPython`'s `repo.git.checkout(feature_branch_name)` or `subprocess.run(['git', 'checkout', feature_branch_name], cwd=repo_path, check=True)`.

**Success Criteria:**
- [ ] Branch switching implemented with GitPython
- [ ] Error handling for invalid branch names
- [ ] Successful checkout confirmed
- [ ] Branch state verified after switching

---

### 009.5: Implement Remote Primary Branch Fetch Logic
**Effort:** 2-3 hours
**Depends on:** 009.4

Develop the code to fetch the latest changes from the determined primary target branch (`git fetch origin <primary_target>`).

**Details:**
Use `GitPython`'s `repo.remote('origin').fetch(primary_target_name)` or `subprocess.run(['git', 'fetch', 'origin', primary_target_name], cwd=repo_path, check=True)`. Include error handling for network issues or non-existent remotes/branches.

**Success Criteria:**
- [ ] Remote fetch implemented with GitPython
- [ ] Error handling for network issues
- [ ] Fetch verification completed
- [ ] Primary branch updates retrieved

---

### 009.6: Coordinate Core Rebase Initiation with Specialized Tasks
**Effort:** 4-5 hours
**Depends on:** 009.5

Coordinate the command execution for initiating the Git rebase operation, leveraging specialized tasks for complex operations.

**Details:**
Execute `subprocess.run(['git', 'rebase', f'origin/{primary_target_name}'], cwd=repo_path, check=True, capture_output=True, text=True)` or `repo.git.rebase(f'origin/{primary_target_name}')`. Capture output for status and potential conflict detection. Coordinate with Task 013 for advanced rebase strategies.

**Success Criteria:**
- [ ] Rebase initiation coordinated
- [ ] Output captured for status analysis
- [ ] Conflict detection prepared
- [ ] Error handling implemented

---

### 009.7: Coordinate Conflict Detection and Resolution
**Effort:** 4-5 hours
**Depends on:** 009.6

Coordinate with Task 013 (Conflict Detection and Resolution) when the rebase operation encounters conflicts.

**Details:**
Delegate conflict detection and resolution to Task 013's ConflictDetectionResolver. This subtask focuses on orchestrating the handoff to the specialized conflict resolution task rather than implementing conflict handling directly.

**Success Criteria:**
- [ ] Coordination with Task 013 implemented
- [ ] Conflict detection handoff operational
- [ ] Resolution guidance provided
- [ ] Resolution status monitored

---

### 009.8: Coordinate Post-Rebase Validation
**Effort:** 3-4 hours
**Depends on:** 009.7

Coordinate with Task 014 (Validation and Verification) to perform automated checks to validate the integrity and correctness of the rebased feature branch.

**Details:**
Delegate validation to Task 014's ValidationVerificationFramework. This ensures comprehensive and consistent validation procedures.

**Success Criteria:**
- [ ] Coordination with Task 014 implemented
- [ ] Validation procedures executed
- [ ] Integrity checks completed
- [ ] Validation results processed

---

### 009.9: Coordinate Rollback to Backup Mechanism
**Effort:** 3-4 hours
**Depends on:** 009.6

Coordinate with Task 015 (Rollback and Recovery) to revert the feature branch to its pre-alignment backup state if a rebase operation ultimately fails or is aborted by the user.

**Details:**
Delegate rollback operations to Task 015's RollbackRecoveryMechanisms. This ensures reliable and consistent rollback procedures.

**Success Criteria:**
- [ ] Coordination with Task 015 implemented
- [ ] Rollback procedures available
- [ ] Backup restoration functional
- [ ] Rollback status tracked

---

### 009.10: Develop Progress Tracking and User Feedback
**Effort:** 2-3 hours
**Depends on:** 009.6, 009.7, 009.8

Add clear progress indicators and descriptive messages throughout the alignment process to keep the user informed.

**Details:**
Implement logging statements for each major step: fetching, checking out branch, initiating rebase, detecting conflicts, etc. Coordinate with specialized tasks to provide unified progress reporting.

**Success Criteria:**
- [ ] Progress indicators implemented
- [ ] User feedback provided at each step
- [ ] Unified reporting coordinated
- [ ] Status updates timely and informative

---

## Specification

### Module Interface

```python
class CoreAlignmentOrchestrator:
    def __init__(self, repo_path: str, config_path: str = None)
    def align_branch(self, feature_branch: str, primary_target: str) -> AlignmentResult
    def coordinate_with_task_012_safety(self, branch_name: str) -> SafetyCheckResult
    def coordinate_with_task_013_conflicts(self, branch_name: str) -> ConflictResolutionResult
    def coordinate_with_task_014_validation(self, branch_name: str) -> ValidationResult
    def coordinate_with_task_015_rollback(self, branch_name: str, backup_ref: str) -> RollbackResult
```

### Output Format

```json
{
  "alignment_operation": {
    "operation_id": "align-20260112-120000-001",
    "feature_branch": "feature/auth-system",
    "primary_target": "main",
    "status": "completed",
    "start_time": "2026-01-12T12:00:00Z",
    "end_time": "2026-01-12T12:05:00Z",
    "duration_seconds": 300
  },
  "coordinated_tasks": {
    "task_012_safety": {
      "status": "completed",
      "backup_created": "feature-auth-system-backup-20260112-120000",
      "safety_checks_passed": true
    },
    "task_013_conflicts": {
      "status": "completed",
      "conflicts_detected": 2,
      "conflicts_resolved": 2,
      "resolution_time_seconds": 120
    },
    "task_014_validation": {
      "status": "completed",
      "validation_passed": true,
      "issues_found": 0
    },
    "task_015_rollback": {
      "status": "not_needed",
      "backup_preserved": true
    }
  },
  "alignment_result": {
    "success": true,
    "commits_aligned": 15,
    "new_ancestor_commit": "a1b2c3d4e5f6",
    "linear_history_maintained": true
  },
  "performance_metrics": {
    "total_time_seconds": 300,
    "breakdown": {
      "safety_checks": 5,
      "backup_creation": 8,
      "rebase_operation": 180,
      "conflict_resolution": 120,
      "validation": 15,
      "cleanup": 2
    }
  }
}
```

---

## Implementation Guide

### 009.6: Coordinate Core Rebase Initiation with Specialized Tasks

**Objective:** Coordinate the core rebase operation with specialized tasks

**Detailed Steps:**

1. Prepare rebase command with proper error handling
   ```python
   def coordinate_rebase_initiation(self, feature_branch: str, primary_target: str) -> RebaseResult:
       try:
           # Switch to feature branch first
           self.repo.git.checkout(feature_branch)

           # Fetch latest from primary target
           self.repo.remote('origin').fetch(primary_target)

           # Execute rebase operation
           result = self.repo.git.rebase(f'origin/{primary_target}',
                                        capture_output=True,
                                        with_extended_output=True)

           # Check if rebase completed successfully
           if result.returncode == 0:
               return RebaseResult(
                   success=True,
                   output=result.stdout,
                   rebase_in_progress=False,
                   conflicts_resolved=0
               )
           else:
               # Check if it's a conflict (return code 1 is often conflicts)
               if 'CONFLICT' in result.stderr or self.repo.is_dirty(untracked_files=True):
                   return RebaseResult(
                       success=False,
                       output=result.stdout,
                       error=result.stderr,
                       rebase_in_progress=True,  # Conflicts to resolve
                       conflicts_resolved=0
                   )
               else:
                   # Actual error
                   return RebaseResult(
                       success=False,
                       output=result.stdout,
                       error=result.stderr,
                       rebase_in_progress=False,
                       conflicts_resolved=0
                   )
       except GitCommandError as e:
           return RebaseResult(
               success=False,
               output="",
               error=str(e),
               rebase_in_progress=False,
               conflicts_resolved=0
           )
   ```

2. Coordinate with Task 013 for conflict resolution
   ```python
   def handle_rebase_conflicts(self, feature_branch: str) -> ConflictResolutionResult:
       # Detect conflicts
       unmerged_blobs = self.repo.index.unmerged_blobs()
       conflicted_files = list(unmerged_blobs.keys())

       if not conflicted_files:
           return ConflictResolutionResult(
               conflicts_detected=False,
               files_affected=[],
               resolution_status="no_conflicts"
           )

       # Coordinate with Task 013 for conflict resolution
       conflict_resolver = Task013ConflictDetectorResolver(self.repo.working_dir)
       resolution_result = conflict_resolver.resolve_conflicts(
           branch_name=feature_branch,
           conflicted_files=conflicted_files
       )

       return resolution_result
   ```

3. Implement proper error handling
   ```python
   def safe_rebase_operation(self, feature_branch: str, primary_target: str) -> SafeRebaseResult:
       original_branch = self.repo.active_branch.name

       try:
           # Ensure we're on the right branch
           if original_branch != feature_branch:
               self.repo.git.checkout(feature_branch)

           # Fetch latest from target
           self.repo.remote('origin').fetch(primary_target)

           # Attempt rebase
           rebase_result = self.coordinate_rebase_initiation(feature_branch, primary_target)

           # If conflicts occurred, handle them
           if not rebase_result.success and rebase_result.rebase_in_progress:
               conflict_result = self.handle_rebase_conflicts(feature_branch)
               rebase_result.conflicts_resolved = conflict_result.conflicts_resolved

               # If conflicts were resolved, continue rebase
               if conflict_result.resolution_status == "completed":
                   try:
                       self.repo.git.rebase('--continue')
                       rebase_result.success = True
                       rebase_result.rebase_in_progress = False
                   except GitCommandError:
                       # If continue fails, we might need to abort
                       pass

           return SafeRebaseResult(
               rebase_result=rebase_result,
               original_branch=original_branch,
               operation_successful=rebase_result.success
           )
       except Exception as e:
           # Ensure we return to original branch on error
           if self.repo.active_branch.name != original_branch:
               self.repo.git.checkout(original_branch)
           raise e
   ```

4. Test with various rebase scenarios

**Testing:**
- Successful rebases should complete properly
- Conflicts should be detected and handled
- Error conditions should be handled gracefully
- Branch state should be preserved appropriately

**Performance:**
- Must complete in <5 seconds for typical rebases
- Memory: <10 MB per operation

---

## Configuration Parameters

Create `config/task_009_alignment_orchestration.yaml`:

```yaml
alignment:
  primary_targets: ["main", "scientific", "orchestration-tools"]
  rebase_timeout_minutes: 10
  conflict_resolution_enabled: true
  validation_after_rebase: true
  rollback_on_failure: true
  progress_reporting: true

coordination:
  task_012_integration: true
  task_013_integration: true
  task_014_integration: true
  task_015_integration: true
  safety_check_timeout_seconds: 30
  validation_timeout_seconds: 60

rebase:
  strategy: "rebase"  # rebase, merge, cherry-pick
  preserve_merges: false
  autosquash: false
  git_command_timeout_seconds: 30
```

Load in code:
```python
import yaml

with open('config/task_009_alignment_orchestration.yaml') as f:
    CONFIG = yaml.safe_load(f)

# Use: CONFIG['alignment']['primary_targets']
```

---

## Performance Targets

### Per Component
- Branch switching: <1 second
- Remote fetch: <2 seconds
- Rebase initiation: <3 seconds
- Conflict coordination: <5 seconds
- Memory usage: <15 MB per operation

### Scalability
- Handle repositories with 10,000+ commits
- Support multiple concurrent alignment operations
- Efficient for large file repositories

### Quality Metrics
- No timeouts on standard hardware
- Consistent performance across repository sizes
- Reliable coordination with specialized tasks

---

## Testing Strategy

### Unit Tests

Minimum 8 test cases:

```python
def test_optimal_target_integration():
    # Optimal target determination should integrate properly

def test_safety_check_coordination():
    # Coordination with Task 012 safety checks should work

def test_backup_coordination():
    # Coordination with Task 012 backup should work

def test_rebase_initiation_coordination():
    # Coordination of rebase initiation should work

def test_conflict_resolution_coordination():
    # Coordination with Task 013 should work

def test_validation_coordination():
    # Coordination with Task 014 should work

def test_rollback_coordination():
    # Coordination with Task 015 should work

def test_performance():
    # Operations complete within performance targets
```

### Integration Tests

After all subtasks complete:

```python
def test_full_alignment_orchestration():
    # Verify 009 output is compatible with Task 010 input

def test_alignment_integration():
    # Validate orchestration works with real repositories
```

### Coverage Target
- Code coverage: > 95%
- All edge cases covered
- All error paths tested

---

## Common Gotchas & Solutions

**Gotcha 1: Branch state management during rebase**
```python
# WRONG
not tracking original branch state during rebase operations

# RIGHT
save original branch state and restore if needed
```

**Gotcha 2: Conflict detection**
```python
# WRONG
only checking return code to detect conflicts

# RIGHT
check both return code and repository state for conflicts
```

**Gotcha 3: Coordination with specialized tasks**
```python
# WRONG
tight coupling with specialized task implementations

# RIGHT
loose coupling through well-defined interfaces
```

**Gotcha 4: Error propagation**
```python
# WRONG
not properly propagating errors from specialized tasks

# RIGHT
proper error handling and propagation from all coordinated tasks
```

---

## Integration Checkpoint

**When to move to Task 010 (Complex alignment):**

- [ ] All 10 subtasks complete
- [ ] Unit tests passing (>95% coverage)
- [ ] Core alignment orchestration working
- [ ] No validation errors on test data
- [ ] Performance targets met (<15s for operations)
- [ ] Integration with specialized tasks validated
- [ ] Code review approved
- [ ] Commit message: "feat: complete Task 009 Core Alignment Orchestration"

---

## Done Definition

Task 009 is done when:

1. ✅ All 10 subtasks marked complete
2. ✅ Unit tests pass (>95% coverage) on CI/CD
3. ✅ Code review approved
4. ✅ Outputs match specification exactly
5. ✅ Output schema validation passes
6. ✅ Documentation complete and accurate
7. ✅ Performance benchmarks met
8. ✅ Ready for hand-off to Task 010
9. ✅ Commit: "feat: complete Task 009 Core Alignment Orchestration"
10. ✅ All success criteria checkboxes marked complete

---

## Next Steps

1. **Immediate:** Implement subtask 009.1 (Integrate Optimal Target Determination)
2. **Week 1:** Complete subtasks 009.1 through 009.5
3. **Week 2:** Complete subtasks 009.6 through 009.10
4. **Week 2:** Write and test unit tests (target: >95%)
5. **Week 2:** Code review
6. **Week 2:** Ready for Task 010 (Complex alignment)

**Reference:** See IMPLEMENTATION_INDEX.md for team coordination
**Effort:** TBD
**Complexity:** TBD

## Overview/Purpose
[Purpose to be defined]

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 004, 006, 007, 012, 013, 014, 015, 022

---

## Purpose

Implement the core orchestrator for multistage branch alignment operations that coordinates with specialized tasks for backup/safety (Task 012), conflict resolution (Task 013), validation (Task 014), and rollback/recovery (Task 015). This task serves as the main entry point for the alignment process while delegating specialized operations to dedicated tasks.

**Scope:** Core alignment orchestration only
**Blocks:** Task 010 (Complex branch alignment), Task 011 (Validation integration)

---

## Success Criteria

Task 009 is complete when:

### Core Functionality
- [ ] Optimal primary target determination integration operational
- [ ] Environment setup and safety checks coordinated with Task 012
- [ ] Branch switching and fetching logic operational
- [ ] Core rebase initiation coordinated with specialized tasks
- [ ] Conflict detection and resolution coordinated with Task 013
- [ ] Post-rebase validation coordinated with Task 014
- [ ] Rollback mechanisms coordinated with Task 015
- [ ] Progress tracking and reporting functional

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <15 seconds for orchestration operations
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

### Integration Readiness
- [ ] Compatible with Task 010 requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 004 (Git operations framework) complete
- [ ] Task 006 (Backup/restore mechanism) complete
- [ ] Task 007 (Feature branch identification) complete
- [ ] Task 012 (Branch backup and safety) complete
- [ ] Task 013 (Conflict detection and resolution) complete
- [ ] Task 014 (Validation and verification) complete
- [ ] Task 015 (Rollback and recovery) complete
- [ ] Task 022 (Architectural migration) complete
- [ ] GitPython or subprocess for git commands available
- [ ] Test infrastructure in place

### Blocks (What This Task Unblocks)
- Task 010 (Complex branch alignment)
- Task 011 (Validation integration)

### External Dependencies
- Python 3.8+
- GitPython or subprocess for git commands
- Specialized tasks (012, 013, 014, 015)

---

## Subtasks Breakdown

### 009.1: Integrate Optimal Primary Target Determination
**Effort:** 2-3 hours
**Depends on:** None

Develop logic to receive and validate the optimal primary branch target (e.g., main, scientific, orchestration-tools) for the feature branch, likely from Task 007.

**Details:**
The Python script will take the feature branch name and its determined primary target as input. This subtask focuses on how this input is consumed and validated against known primary branches. Leverage outputs from Task 007's categorization tool.

**Success Criteria:**
- [ ] Optimal primary target received from Task 007
- [ ] Target validated against known primary branches
- [ ] Invalid targets handled gracefully
- [ ] Input validation comprehensive

---

### 009.2: Coordinate Initial Environment Setup and Safety Checks
**Effort:** 3-4 hours
**Depends on:** 009.1

Before any Git operations, coordinate safety checks with Task 012 (Branch Backup and Safety).

**Details:**
Coordinate with Task 012 to ensure a clean working directory and valid repository state, preventing unintended data loss or conflicts. This subtask focuses on orchestrating the safety validation rather than implementing it directly.

**Success Criteria:**
- [ ] Coordination with Task 012 implemented
- [ ] Working directory validated
- [ ] Repository state verified
- [ ] Safety checks completed before proceeding

---

### 009.3: Coordinate Local Feature Branch Backup
**Effort:** 3-4 hours
**Depends on:** 009.2

Coordinate with Task 012 (Branch Backup and Safety) to create a temporary backup of the feature branch's current state before initiating any rebase operations.

**Details:**
Delegate the backup creation to Task 012's BranchBackupManager. This ensures the backup mechanism is handled by the specialized task while Task 009 coordinates the overall process.

**Success Criteria:**
- [ ] Coordination with Task 012 implemented
- [ ] Backup created before Git operations
- [ ] Backup verification completed
- [ ] Backup reference stored for potential rollback

---

### 009.4: Implement Branch Switching Logic
**Effort:** 2-3 hours
**Depends on:** 009.3

Write the Python code to programmatically switch the local Git repository to the specified feature branch.

**Details:**
Utilize `GitPython`'s `repo.git.checkout(feature_branch_name)` or `subprocess.run(['git', 'checkout', feature_branch_name], cwd=repo_path, check=True)`.

**Success Criteria:**
- [ ] Branch switching implemented with GitPython
- [ ] Error handling for invalid branch names
- [ ] Successful checkout confirmed
- [ ] Branch state verified after switching

---

### 009.5: Implement Remote Primary Branch Fetch Logic
**Effort:** 2-3 hours
**Depends on:** 009.4

Develop the code to fetch the latest changes from the determined primary target branch (`git fetch origin <primary_target>`).

**Details:**
Use `GitPython`'s `repo.remote('origin').fetch(primary_target_name)` or `subprocess.run(['git', 'fetch', 'origin', primary_target_name], cwd=repo_path, check=True)`. Include error handling for network issues or non-existent remotes/branches.

**Success Criteria:**
- [ ] Remote fetch implemented with GitPython
- [ ] Error handling for network issues
- [ ] Fetch verification completed
- [ ] Primary branch updates retrieved

---

### 009.6: Coordinate Core Rebase Initiation with Specialized Tasks
**Effort:** 4-5 hours
**Depends on:** 009.5

Coordinate the command execution for initiating the Git rebase operation, leveraging specialized tasks for complex operations.

**Details:**
Execute `subprocess.run(['git', 'rebase', f'origin/{primary_target_name}'], cwd=repo_path, check=True, capture_output=True, text=True)` or `repo.git.rebase(f'origin/{primary_target_name}')`. Capture output for status and potential conflict detection. Coordinate with Task 013 for advanced rebase strategies.

**Success Criteria:**
- [ ] Rebase initiation coordinated
- [ ] Output captured for status analysis
- [ ] Conflict detection prepared
- [ ] Error handling implemented

---

### 009.7: Coordinate Conflict Detection and Resolution
**Effort:** 4-5 hours
**Depends on:** 009.6

Coordinate with Task 013 (Conflict Detection and Resolution) when the rebase operation encounters conflicts.

**Details:**
Delegate conflict detection and resolution to Task 013's ConflictDetectionResolver. This subtask focuses on orchestrating the handoff to the specialized conflict resolution task rather than implementing conflict handling directly.

**Success Criteria:**
- [ ] Coordination with Task 013 implemented
- [ ] Conflict detection handoff operational
- [ ] Resolution guidance provided
- [ ] Resolution status monitored

---

### 009.8: Coordinate Post-Rebase Validation
**Effort:** 3-4 hours
**Depends on:** 009.7

Coordinate with Task 014 (Validation and Verification) to perform automated checks to validate the integrity and correctness of the rebased feature branch.

**Details:**
Delegate validation to Task 014's ValidationVerificationFramework. This ensures comprehensive and consistent validation procedures.

**Success Criteria:**
- [ ] Coordination with Task 014 implemented
- [ ] Validation procedures executed
- [ ] Integrity checks completed
- [ ] Validation results processed

---

### 009.9: Coordinate Rollback to Backup Mechanism
**Effort:** 3-4 hours
**Depends on:** 009.6

Coordinate with Task 015 (Rollback and Recovery) to revert the feature branch to its pre-alignment backup state if a rebase operation ultimately fails or is aborted by the user.

**Details:**
Delegate rollback operations to Task 015's RollbackRecoveryMechanisms. This ensures reliable and consistent rollback procedures.

**Success Criteria:**
- [ ] Coordination with Task 015 implemented
- [ ] Rollback procedures available
- [ ] Backup restoration functional
- [ ] Rollback status tracked

---

### 009.10: Develop Progress Tracking and User Feedback
**Effort:** 2-3 hours
**Depends on:** 009.6, 009.7, 009.8

Add clear progress indicators and descriptive messages throughout the alignment process to keep the user informed.

**Details:**
Implement logging statements for each major step: fetching, checking out branch, initiating rebase, detecting conflicts, etc. Coordinate with specialized tasks to provide unified progress reporting.

**Success Criteria:**
- [ ] Progress indicators implemented
- [ ] User feedback provided at each step
- [ ] Unified reporting coordinated
- [ ] Status updates timely and informative

---

## Specification

### Module Interface

```python
class CoreAlignmentOrchestrator:
    def __init__(self, repo_path: str, config_path: str = None)
    def align_branch(self, feature_branch: str, primary_target: str) -> AlignmentResult
    def coordinate_with_task_012_safety(self, branch_name: str) -> SafetyCheckResult
    def coordinate_with_task_013_conflicts(self, branch_name: str) -> ConflictResolutionResult
    def coordinate_with_task_014_validation(self, branch_name: str) -> ValidationResult
    def coordinate_with_task_015_rollback(self, branch_name: str, backup_ref: str) -> RollbackResult
```

### Output Format

```json
{
  "alignment_operation": {
    "operation_id": "align-20260112-120000-001",
    "feature_branch": "feature/auth-system",
    "primary_target": "main",
    "status": "completed",
    "start_time": "2026-01-12T12:00:00Z",
    "end_time": "2026-01-12T12:05:00Z",
    "duration_seconds": 300
  },
  "coordinated_tasks": {
    "task_012_safety": {
      "status": "completed",
      "backup_created": "feature-auth-system-backup-20260112-120000",
      "safety_checks_passed": true
    },
    "task_013_conflicts": {
      "status": "completed",
      "conflicts_detected": 2,
      "conflicts_resolved": 2,
      "resolution_time_seconds": 120
    },
    "task_014_validation": {
      "status": "completed",
      "validation_passed": true,
      "issues_found": 0
    },
    "task_015_rollback": {
      "status": "not_needed",
      "backup_preserved": true
    }
  },
  "alignment_result": {
    "success": true,
    "commits_aligned": 15,
    "new_ancestor_commit": "a1b2c3d4e5f6",
    "linear_history_maintained": true
  },
  "performance_metrics": {
    "total_time_seconds": 300,
    "breakdown": {
      "safety_checks": 5,
      "backup_creation": 8,
      "rebase_operation": 180,
      "conflict_resolution": 120,
      "validation": 15,
      "cleanup": 2
    }
  }
}
```

---

## Implementation Guide

### 009.6: Coordinate Core Rebase Initiation with Specialized Tasks

**Objective:** Coordinate the core rebase operation with specialized tasks

**Detailed Steps:**

1. Prepare rebase command with proper error handling
   ```python
   def coordinate_rebase_initiation(self, feature_branch: str, primary_target: str) -> RebaseResult:
       try:
           # Switch to feature branch first
           self.repo.git.checkout(feature_branch)

           # Fetch latest from primary target
           self.repo.remote('origin').fetch(primary_target)

           # Execute rebase operation
           result = self.repo.git.rebase(f'origin/{primary_target}',
                                        capture_output=True,
                                        with_extended_output=True)

           # Check if rebase completed successfully
           if result.returncode == 0:
               return RebaseResult(
                   success=True,
                   output=result.stdout,
                   rebase_in_progress=False,
                   conflicts_resolved=0
               )
           else:
               # Check if it's a conflict (return code 1 is often conflicts)
               if 'CONFLICT' in result.stderr or self.repo.is_dirty(untracked_files=True):
                   return RebaseResult(
                       success=False,
                       output=result.stdout,
                       error=result.stderr,
                       rebase_in_progress=True,  # Conflicts to resolve
                       conflicts_resolved=0
                   )
               else:
                   # Actual error
                   return RebaseResult(
                       success=False,
                       output=result.stdout,
                       error=result.stderr,
                       rebase_in_progress=False,
                       conflicts_resolved=0
                   )
       except GitCommandError as e:
           return RebaseResult(
               success=False,
               output="",
               error=str(e),
               rebase_in_progress=False,
               conflicts_resolved=0
           )
   ```

2. Coordinate with Task 013 for conflict resolution
   ```python
   def handle_rebase_conflicts(self, feature_branch: str) -> ConflictResolutionResult:
       # Detect conflicts
       unmerged_blobs = self.repo.index.unmerged_blobs()
       conflicted_files = list(unmerged_blobs.keys())

       if not conflicted_files:
           return ConflictResolutionResult(
               conflicts_detected=False,
               files_affected=[],
               resolution_status="no_conflicts"
           )

       # Coordinate with Task 013 for conflict resolution
       conflict_resolver = Task013ConflictDetectorResolver(self.repo.working_dir)
       resolution_result = conflict_resolver.resolve_conflicts(
           branch_name=feature_branch,
           conflicted_files=conflicted_files
       )

       return resolution_result
   ```

3. Implement proper error handling
   ```python
   def safe_rebase_operation(self, feature_branch: str, primary_target: str) -> SafeRebaseResult:
       original_branch = self.repo.active_branch.name

       try:
           # Ensure we're on the right branch
           if original_branch != feature_branch:
               self.repo.git.checkout(feature_branch)

           # Fetch latest from target
           self.repo.remote('origin').fetch(primary_target)

           # Attempt rebase
           rebase_result = self.coordinate_rebase_initiation(feature_branch, primary_target)

           # If conflicts occurred, handle them
           if not rebase_result.success and rebase_result.rebase_in_progress:
               conflict_result = self.handle_rebase_conflicts(feature_branch)
               rebase_result.conflicts_resolved = conflict_result.conflicts_resolved

               # If conflicts were resolved, continue rebase
               if conflict_result.resolution_status == "completed":
                   try:
                       self.repo.git.rebase('--continue')
                       rebase_result.success = True
                       rebase_result.rebase_in_progress = False
                   except GitCommandError:
                       # If continue fails, we might need to abort
                       pass

           return SafeRebaseResult(
               rebase_result=rebase_result,
               original_branch=original_branch,
               operation_successful=rebase_result.success
           )
       except Exception as e:
           # Ensure we return to original branch on error
           if self.repo.active_branch.name != original_branch:
               self.repo.git.checkout(original_branch)
           raise e
   ```

4. Test with various rebase scenarios

**Testing:**
- Successful rebases should complete properly
- Conflicts should be detected and handled
- Error conditions should be handled gracefully
- Branch state should be preserved appropriately

**Performance:**
- Must complete in <5 seconds for typical rebases
- Memory: <10 MB per operation

---

## Configuration Parameters

Create `config/task_009_alignment_orchestration.yaml`:

```yaml
alignment:
  primary_targets: ["main", "scientific", "orchestration-tools"]
  rebase_timeout_minutes: 10
  conflict_resolution_enabled: true
  validation_after_rebase: true
  rollback_on_failure: true
  progress_reporting: true

coordination:
  task_012_integration: true
  task_013_integration: true
  task_014_integration: true
  task_015_integration: true
  safety_check_timeout_seconds: 30
  validation_timeout_seconds: 60

rebase:
  strategy: "rebase"  # rebase, merge, cherry-pick
  preserve_merges: false
  autosquash: false
  git_command_timeout_seconds: 30
```

Load in code:
```python
import yaml

with open('config/task_009_alignment_orchestration.yaml') as f:
    CONFIG = yaml.safe_load(f)

# Use: CONFIG['alignment']['primary_targets']
```

---

## Performance Targets

### Per Component
- Branch switching: <1 second
- Remote fetch: <2 seconds
- Rebase initiation: <3 seconds
- Conflict coordination: <5 seconds
- Memory usage: <15 MB per operation

### Scalability
- Handle repositories with 10,000+ commits
- Support multiple concurrent alignment operations
- Efficient for large file repositories

### Quality Metrics
- No timeouts on standard hardware
- Consistent performance across repository sizes
- Reliable coordination with specialized tasks

---

## Testing Strategy

### Unit Tests

Minimum 8 test cases:

```python
def test_optimal_target_integration():
    # Optimal target determination should integrate properly

def test_safety_check_coordination():
    # Coordination with Task 012 safety checks should work

def test_backup_coordination():
    # Coordination with Task 012 backup should work

def test_rebase_initiation_coordination():
    # Coordination of rebase initiation should work

def test_conflict_resolution_coordination():
    # Coordination with Task 013 should work

def test_validation_coordination():
    # Coordination with Task 014 should work

def test_rollback_coordination():
    # Coordination with Task 015 should work

def test_performance():
    # Operations complete within performance targets
```

### Integration Tests

After all subtasks complete:

```python
def test_full_alignment_orchestration():
    # Verify 009 output is compatible with Task 010 input

def test_alignment_integration():
    # Validate orchestration works with real repositories
```

### Coverage Target
- Code coverage: > 95%
- All edge cases covered
- All error paths tested

---

## Common Gotchas & Solutions

**Gotcha 1: Branch state management during rebase**
```python
# WRONG
not tracking original branch state during rebase operations

# RIGHT
save original branch state and restore if needed
```

**Gotcha 2: Conflict detection**
```python
# WRONG
only checking return code to detect conflicts

# RIGHT
check both return code and repository state for conflicts
```

**Gotcha 3: Coordination with specialized tasks**
```python
# WRONG
tight coupling with specialized task implementations

# RIGHT
loose coupling through well-defined interfaces
```

**Gotcha 4: Error propagation**
```python
# WRONG
not properly propagating errors from specialized tasks

# RIGHT
proper error handling and propagation from all coordinated tasks
```

---

## Integration Checkpoint

**When to move to Task 010 (Complex alignment):**

- [ ] All 10 subtasks complete
- [ ] Unit tests passing (>95% coverage)
- [ ] Core alignment orchestration working
- [ ] No validation errors on test data
- [ ] Performance targets met (<15s for operations)
- [ ] Integration with specialized tasks validated
- [ ] Code review approved
- [ ] Commit message: "feat: complete Task 009 Core Alignment Orchestration"

---

## Done Definition

Task 009 is done when:

1. ✅ All 10 subtasks marked complete
2. ✅ Unit tests pass (>95% coverage) on CI/CD
3. ✅ Code review approved
4. ✅ Outputs match specification exactly
5. ✅ Output schema validation passes
6. ✅ Documentation complete and accurate
7. ✅ Performance benchmarks met
8. ✅ Ready for hand-off to Task 010
9. ✅ Commit: "feat: complete Task 009 Core Alignment Orchestration"
10. ✅ All success criteria checkboxes marked complete

---

## Next Steps

1. **Immediate:** Implement subtask 009.1 (Integrate Optimal Target Determination)
2. **Week 1:** Complete subtasks 009.1 through 009.5
3. **Week 2:** Complete subtasks 009.6 through 009.10
4. **Week 2:** Write and test unit tests (target: >95%)
5. **Week 2:** Code review
6. **Week 2:** Ready for Task 010 (Complex alignment)

**Reference:** See IMPLEMENTATION_INDEX.md for team coordination

### Blocks (What This Task Unblocks)
- [ ] None specified

### External Dependencies
- [ ] None

## Sub-subtasks Breakdown

# No subtasks defined

## Specification Details

### Task Interface
- **ID**: 009
- **Title**: Core Multistage Primary-to-Feature Branch Alignment

**Status:** Ready for Implementation
**Priority:** High
**Effort:** 28-40 hours
**Complexity:** 8/10
**Dependencies:** 004, 006, 007, 012, 013, 014, 015, 022

---

## Purpose

Implement the core orchestrator for multistage branch alignment operations that coordinates with specialized tasks for backup/safety (Task 012), conflict resolution (Task 013), validation (Task 014), and rollback/recovery (Task 015). This task serves as the main entry point for the alignment process while delegating specialized operations to dedicated tasks.

**Scope:** Core alignment orchestration only
**Blocks:** Task 010 (Complex branch alignment), Task 011 (Validation integration)

---

## Success Criteria

Task 009 is complete when:

### Core Functionality
- [ ] Optimal primary target determination integration operational
- [ ] Environment setup and safety checks coordinated with Task 012
- [ ] Branch switching and fetching logic operational
- [ ] Core rebase initiation coordinated with specialized tasks
- [ ] Conflict detection and resolution coordinated with Task 013
- [ ] Post-rebase validation coordinated with Task 014
- [ ] Rollback mechanisms coordinated with Task 015
- [ ] Progress tracking and reporting functional

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <15 seconds for orchestration operations
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

### Integration Readiness
- [ ] Compatible with Task 010 requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 004 (Git operations framework) complete
- [ ] Task 006 (Backup/restore mechanism) complete
- [ ] Task 007 (Feature branch identification) complete
- [ ] Task 012 (Branch backup and safety) complete
- [ ] Task 013 (Conflict detection and resolution) complete
- [ ] Task 014 (Validation and verification) complete
- [ ] Task 015 (Rollback and recovery) complete
- [ ] Task 022 (Architectural migration) complete
- [ ] GitPython or subprocess for git commands available
- [ ] Test infrastructure in place

### Blocks (What This Task Unblocks)
- Task 010 (Complex branch alignment)
- Task 011 (Validation integration)

### External Dependencies
- Python 3.8+
- GitPython or subprocess for git commands
- Specialized tasks (012, 013, 014, 015)

---

## Subtasks Breakdown

### 009.1: Integrate Optimal Primary Target Determination
**Effort:** 2-3 hours
**Depends on:** None

Develop logic to receive and validate the optimal primary branch target (e.g., main, scientific, orchestration-tools) for the feature branch, likely from Task 007.

**Details:**
The Python script will take the feature branch name and its determined primary target as input. This subtask focuses on how this input is consumed and validated against known primary branches. Leverage outputs from Task 007's categorization tool.

**Success Criteria:**
- [ ] Optimal primary target received from Task 007
- [ ] Target validated against known primary branches
- [ ] Invalid targets handled gracefully
- [ ] Input validation comprehensive

---

### 009.2: Coordinate Initial Environment Setup and Safety Checks
**Effort:** 3-4 hours
**Depends on:** 009.1

Before any Git operations, coordinate safety checks with Task 012 (Branch Backup and Safety).

**Details:**
Coordinate with Task 012 to ensure a clean working directory and valid repository state, preventing unintended data loss or conflicts. This subtask focuses on orchestrating the safety validation rather than implementing it directly.

**Success Criteria:**
- [ ] Coordination with Task 012 implemented
- [ ] Working directory validated
- [ ] Repository state verified
- [ ] Safety checks completed before proceeding

---

### 009.3: Coordinate Local Feature Branch Backup
**Effort:** 3-4 hours
**Depends on:** 009.2

Coordinate with Task 012 (Branch Backup and Safety) to create a temporary backup of the feature branch's current state before initiating any rebase operations.

**Details:**
Delegate the backup creation to Task 012's BranchBackupManager. This ensures the backup mechanism is handled by the specialized task while Task 009 coordinates the overall process.

**Success Criteria:**
- [ ] Coordination with Task 012 implemented
- [ ] Backup created before Git operations
- [ ] Backup verification completed
- [ ] Backup reference stored for potential rollback

---

### 009.4: Implement Branch Switching Logic
**Effort:** 2-3 hours
**Depends on:** 009.3

Write the Python code to programmatically switch the local Git repository to the specified feature branch.

**Details:**
Utilize `GitPython`'s `repo.git.checkout(feature_branch_name)` or `subprocess.run(['git', 'checkout', feature_branch_name], cwd=repo_path, check=True)`.

**Success Criteria:**
- [ ] Branch switching implemented with GitPython
- [ ] Error handling for invalid branch names
- [ ] Successful checkout confirmed
- [ ] Branch state verified after switching

---

### 009.5: Implement Remote Primary Branch Fetch Logic
**Effort:** 2-3 hours
**Depends on:** 009.4

Develop the code to fetch the latest changes from the determined primary target branch (`git fetch origin <primary_target>`).

**Details:**
Use `GitPython`'s `repo.remote('origin').fetch(primary_target_name)` or `subprocess.run(['git', 'fetch', 'origin', primary_target_name], cwd=repo_path, check=True)`. Include error handling for network issues or non-existent remotes/branches.

**Success Criteria:**
- [ ] Remote fetch implemented with GitPython
- [ ] Error handling for network issues
- [ ] Fetch verification completed
- [ ] Primary branch updates retrieved

---

### 009.6: Coordinate Core Rebase Initiation with Specialized Tasks
**Effort:** 4-5 hours
**Depends on:** 009.5

Coordinate the command execution for initiating the Git rebase operation, leveraging specialized tasks for complex operations.

**Details:**
Execute `subprocess.run(['git', 'rebase', f'origin/{primary_target_name}'], cwd=repo_path, check=True, capture_output=True, text=True)` or `repo.git.rebase(f'origin/{primary_target_name}')`. Capture output for status and potential conflict detection. Coordinate with Task 013 for advanced rebase strategies.

**Success Criteria:**
- [ ] Rebase initiation coordinated
- [ ] Output captured for status analysis
- [ ] Conflict detection prepared
- [ ] Error handling implemented

---

### 009.7: Coordinate Conflict Detection and Resolution
**Effort:** 4-5 hours
**Depends on:** 009.6

Coordinate with Task 013 (Conflict Detection and Resolution) when the rebase operation encounters conflicts.

**Details:**
Delegate conflict detection and resolution to Task 013's ConflictDetectionResolver. This subtask focuses on orchestrating the handoff to the specialized conflict resolution task rather than implementing conflict handling directly.

**Success Criteria:**
- [ ] Coordination with Task 013 implemented
- [ ] Conflict detection handoff operational
- [ ] Resolution guidance provided
- [ ] Resolution status monitored

---

### 009.8: Coordinate Post-Rebase Validation
**Effort:** 3-4 hours
**Depends on:** 009.7

Coordinate with Task 014 (Validation and Verification) to perform automated checks to validate the integrity and correctness of the rebased feature branch.

**Details:**
Delegate validation to Task 014's ValidationVerificationFramework. This ensures comprehensive and consistent validation procedures.

**Success Criteria:**
- [ ] Coordination with Task 014 implemented
- [ ] Validation procedures executed
- [ ] Integrity checks completed
- [ ] Validation results processed

---

### 009.9: Coordinate Rollback to Backup Mechanism
**Effort:** 3-4 hours
**Depends on:** 009.6

Coordinate with Task 015 (Rollback and Recovery) to revert the feature branch to its pre-alignment backup state if a rebase operation ultimately fails or is aborted by the user.

**Details:**
Delegate rollback operations to Task 015's RollbackRecoveryMechanisms. This ensures reliable and consistent rollback procedures.

**Success Criteria:**
- [ ] Coordination with Task 015 implemented
- [ ] Rollback procedures available
- [ ] Backup restoration functional
- [ ] Rollback status tracked

---

### 009.10: Develop Progress Tracking and User Feedback
**Effort:** 2-3 hours
**Depends on:** 009.6, 009.7, 009.8

Add clear progress indicators and descriptive messages throughout the alignment process to keep the user informed.

**Details:**
Implement logging statements for each major step: fetching, checking out branch, initiating rebase, detecting conflicts, etc. Coordinate with specialized tasks to provide unified progress reporting.

**Success Criteria:**
- [ ] Progress indicators implemented
- [ ] User feedback provided at each step
- [ ] Unified reporting coordinated
- [ ] Status updates timely and informative

---

## Specification

### Module Interface

```python
class CoreAlignmentOrchestrator:
    def __init__(self, repo_path: str, config_path: str = None)
    def align_branch(self, feature_branch: str, primary_target: str) -> AlignmentResult
    def coordinate_with_task_012_safety(self, branch_name: str) -> SafetyCheckResult
    def coordinate_with_task_013_conflicts(self, branch_name: str) -> ConflictResolutionResult
    def coordinate_with_task_014_validation(self, branch_name: str) -> ValidationResult
    def coordinate_with_task_015_rollback(self, branch_name: str, backup_ref: str) -> RollbackResult
```

### Output Format

```json
{
  "alignment_operation": {
    "operation_id": "align-20260112-120000-001",
    "feature_branch": "feature/auth-system",
    "primary_target": "main",
    "status": "completed",
    "start_time": "2026-01-12T12:00:00Z",
    "end_time": "2026-01-12T12:05:00Z",
    "duration_seconds": 300
  },
  "coordinated_tasks": {
    "task_012_safety": {
      "status": "completed",
      "backup_created": "feature-auth-system-backup-20260112-120000",
      "safety_checks_passed": true
    },
    "task_013_conflicts": {
      "status": "completed",
      "conflicts_detected": 2,
      "conflicts_resolved": 2,
      "resolution_time_seconds": 120
    },
    "task_014_validation": {
      "status": "completed",
      "validation_passed": true,
      "issues_found": 0
    },
    "task_015_rollback": {
      "status": "not_needed",
      "backup_preserved": true
    }
  },
  "alignment_result": {
    "success": true,
    "commits_aligned": 15,
    "new_ancestor_commit": "a1b2c3d4e5f6",
    "linear_history_maintained": true
  },
  "performance_metrics": {
    "total_time_seconds": 300,
    "breakdown": {
      "safety_checks": 5,
      "backup_creation": 8,
      "rebase_operation": 180,
      "conflict_resolution": 120,
      "validation": 15,
      "cleanup": 2
    }
  }
}
```

---

## Implementation Guide

### 009.6: Coordinate Core Rebase Initiation with Specialized Tasks

**Objective:** Coordinate the core rebase operation with specialized tasks

**Detailed Steps:**

1. Prepare rebase command with proper error handling
   ```python
   def coordinate_rebase_initiation(self, feature_branch: str, primary_target: str) -> RebaseResult:
       try:
           # Switch to feature branch first
           self.repo.git.checkout(feature_branch)

           # Fetch latest from primary target
           self.repo.remote('origin').fetch(primary_target)

           # Execute rebase operation
           result = self.repo.git.rebase(f'origin/{primary_target}',
                                        capture_output=True,
                                        with_extended_output=True)

           # Check if rebase completed successfully
           if result.returncode == 0:
               return RebaseResult(
                   success=True,
                   output=result.stdout,
                   rebase_in_progress=False,
                   conflicts_resolved=0
               )
           else:
               # Check if it's a conflict (return code 1 is often conflicts)
               if 'CONFLICT' in result.stderr or self.repo.is_dirty(untracked_files=True):
                   return RebaseResult(
                       success=False,
                       output=result.stdout,
                       error=result.stderr,
                       rebase_in_progress=True,  # Conflicts to resolve
                       conflicts_resolved=0
                   )
               else:
                   # Actual error
                   return RebaseResult(
                       success=False,
                       output=result.stdout,
                       error=result.stderr,
                       rebase_in_progress=False,
                       conflicts_resolved=0
                   )
       except GitCommandError as e:
           return RebaseResult(
               success=False,
               output="",
               error=str(e),
               rebase_in_progress=False,
               conflicts_resolved=0
           )
   ```

2. Coordinate with Task 013 for conflict resolution
   ```python
   def handle_rebase_conflicts(self, feature_branch: str) -> ConflictResolutionResult:
       # Detect conflicts
       unmerged_blobs = self.repo.index.unmerged_blobs()
       conflicted_files = list(unmerged_blobs.keys())

       if not conflicted_files:
           return ConflictResolutionResult(
               conflicts_detected=False,
               files_affected=[],
               resolution_status="no_conflicts"
           )

       # Coordinate with Task 013 for conflict resolution
       conflict_resolver = Task013ConflictDetectorResolver(self.repo.working_dir)
       resolution_result = conflict_resolver.resolve_conflicts(
           branch_name=feature_branch,
           conflicted_files=conflicted_files
       )

       return resolution_result
   ```

3. Implement proper error handling
   ```python
   def safe_rebase_operation(self, feature_branch: str, primary_target: str) -> SafeRebaseResult:
       original_branch = self.repo.active_branch.name

       try:
           # Ensure we're on the right branch
           if original_branch != feature_branch:
               self.repo.git.checkout(feature_branch)

           # Fetch latest from target
           self.repo.remote('origin').fetch(primary_target)

           # Attempt rebase
           rebase_result = self.coordinate_rebase_initiation(feature_branch, primary_target)

           # If conflicts occurred, handle them
           if not rebase_result.success and rebase_result.rebase_in_progress:
               conflict_result = self.handle_rebase_conflicts(feature_branch)
               rebase_result.conflicts_resolved = conflict_result.conflicts_resolved

               # If conflicts were resolved, continue rebase
               if conflict_result.resolution_status == "completed":
                   try:
                       self.repo.git.rebase('--continue')
                       rebase_result.success = True
                       rebase_result.rebase_in_progress = False
                   except GitCommandError:
                       # If continue fails, we might need to abort
                       pass

           return SafeRebaseResult(
               rebase_result=rebase_result,
               original_branch=original_branch,
               operation_successful=rebase_result.success
           )
       except Exception as e:
           # Ensure we return to original branch on error
           if self.repo.active_branch.name != original_branch:
               self.repo.git.checkout(original_branch)
           raise e
   ```

4. Test with various rebase scenarios

**Testing:**
- Successful rebases should complete properly
- Conflicts should be detected and handled
- Error conditions should be handled gracefully
- Branch state should be preserved appropriately

**Performance:**
- Must complete in <5 seconds for typical rebases
- Memory: <10 MB per operation

---

## Configuration Parameters

Create `config/task_009_alignment_orchestration.yaml`:

```yaml
alignment:
  primary_targets: ["main", "scientific", "orchestration-tools"]
  rebase_timeout_minutes: 10
  conflict_resolution_enabled: true
  validation_after_rebase: true
  rollback_on_failure: true
  progress_reporting: true

coordination:
  task_012_integration: true
  task_013_integration: true
  task_014_integration: true
  task_015_integration: true
  safety_check_timeout_seconds: 30
  validation_timeout_seconds: 60

rebase:
  strategy: "rebase"  # rebase, merge, cherry-pick
  preserve_merges: false
  autosquash: false
  git_command_timeout_seconds: 30
```

Load in code:
```python
import yaml

with open('config/task_009_alignment_orchestration.yaml') as f:
    CONFIG = yaml.safe_load(f)

# Use: CONFIG['alignment']['primary_targets']
```

---

## Performance Targets

### Per Component
- Branch switching: <1 second
- Remote fetch: <2 seconds
- Rebase initiation: <3 seconds
- Conflict coordination: <5 seconds
- Memory usage: <15 MB per operation

### Scalability
- Handle repositories with 10,000+ commits
- Support multiple concurrent alignment operations
- Efficient for large file repositories

### Quality Metrics
- No timeouts on standard hardware
- Consistent performance across repository sizes
- Reliable coordination with specialized tasks

---

## Testing Strategy

### Unit Tests

Minimum 8 test cases:

```python
def test_optimal_target_integration():
    # Optimal target determination should integrate properly

def test_safety_check_coordination():
    # Coordination with Task 012 safety checks should work

def test_backup_coordination():
    # Coordination with Task 012 backup should work

def test_rebase_initiation_coordination():
    # Coordination of rebase initiation should work

def test_conflict_resolution_coordination():
    # Coordination with Task 013 should work

def test_validation_coordination():
    # Coordination with Task 014 should work

def test_rollback_coordination():
    # Coordination with Task 015 should work

def test_performance():
    # Operations complete within performance targets
```

### Integration Tests

After all subtasks complete:

```python
def test_full_alignment_orchestration():
    # Verify 009 output is compatible with Task 010 input

def test_alignment_integration():
    # Validate orchestration works with real repositories
```

### Coverage Target
- Code coverage: > 95%
- All edge cases covered
- All error paths tested

---

## Common Gotchas & Solutions

**Gotcha 1: Branch state management during rebase**
```python
# WRONG
not tracking original branch state during rebase operations

# RIGHT
save original branch state and restore if needed
```

**Gotcha 2: Conflict detection**
```python
# WRONG
only checking return code to detect conflicts

# RIGHT
check both return code and repository state for conflicts
```

**Gotcha 3: Coordination with specialized tasks**
```python
# WRONG
tight coupling with specialized task implementations

# RIGHT
loose coupling through well-defined interfaces
```

**Gotcha 4: Error propagation**
```python
# WRONG
not properly propagating errors from specialized tasks

# RIGHT
proper error handling and propagation from all coordinated tasks
```

---

## Integration Checkpoint

**When to move to Task 010 (Complex alignment):**

- [ ] All 10 subtasks complete
- [ ] Unit tests passing (>95% coverage)
- [ ] Core alignment orchestration working
- [ ] No validation errors on test data
- [ ] Performance targets met (<15s for operations)
- [ ] Integration with specialized tasks validated
- [ ] Code review approved
- [ ] Commit message: "feat: complete Task 009 Core Alignment Orchestration"

---

## Done Definition

Task 009 is done when:

1. ✅ All 10 subtasks marked complete
2. ✅ Unit tests pass (>95% coverage) on CI/CD
3. ✅ Code review approved
4. ✅ Outputs match specification exactly
5. ✅ Output schema validation passes
6. ✅ Documentation complete and accurate
7. ✅ Performance benchmarks met
8. ✅ Ready for hand-off to Task 010
9. ✅ Commit: "feat: complete Task 009 Core Alignment Orchestration"
10. ✅ All success criteria checkboxes marked complete

---

## Next Steps

1. **Immediate:** Implement subtask 009.1 (Integrate Optimal Target Determination)
2. **Week 1:** Complete subtasks 009.1 through 009.5
3. **Week 2:** Complete subtasks 009.6 through 009.10
4. **Week 2:** Write and test unit tests (target: >95%)
5. **Week 2:** Code review
6. **Week 2:** Ready for Task 010 (Complex alignment)

**Reference:** See IMPLEMENTATION_INDEX.md for team coordination
- **Status**: Ready for Implementation
**Priority:** High
**Effort:** 28-40 hours
**Complexity:** 8/10
**Dependencies:** 004, 006, 007, 012, 013, 014, 015, 022

---

## Purpose

Implement the core orchestrator for multistage branch alignment operations that coordinates with specialized tasks for backup/safety (Task 012), conflict resolution (Task 013), validation (Task 014), and rollback/recovery (Task 015). This task serves as the main entry point for the alignment process while delegating specialized operations to dedicated tasks.

**Scope:** Core alignment orchestration only
**Blocks:** Task 010 (Complex branch alignment), Task 011 (Validation integration)

---

## Success Criteria

Task 009 is complete when:

### Core Functionality
- [ ] Optimal primary target determination integration operational
- [ ] Environment setup and safety checks coordinated with Task 012
- [ ] Branch switching and fetching logic operational
- [ ] Core rebase initiation coordinated with specialized tasks
- [ ] Conflict detection and resolution coordinated with Task 013
- [ ] Post-rebase validation coordinated with Task 014
- [ ] Rollback mechanisms coordinated with Task 015
- [ ] Progress tracking and reporting functional

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <15 seconds for orchestration operations
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

### Integration Readiness
- [ ] Compatible with Task 010 requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 004 (Git operations framework) complete
- [ ] Task 006 (Backup/restore mechanism) complete
- [ ] Task 007 (Feature branch identification) complete
- [ ] Task 012 (Branch backup and safety) complete
- [ ] Task 013 (Conflict detection and resolution) complete
- [ ] Task 014 (Validation and verification) complete
- [ ] Task 015 (Rollback and recovery) complete
- [ ] Task 022 (Architectural migration) complete
- [ ] GitPython or subprocess for git commands available
- [ ] Test infrastructure in place

### Blocks (What This Task Unblocks)
- Task 010 (Complex branch alignment)
- Task 011 (Validation integration)

### External Dependencies
- Python 3.8+
- GitPython or subprocess for git commands
- Specialized tasks (012, 013, 014, 015)

---

## Subtasks Breakdown

### 009.1: Integrate Optimal Primary Target Determination
**Effort:** 2-3 hours
**Depends on:** None

Develop logic to receive and validate the optimal primary branch target (e.g., main, scientific, orchestration-tools) for the feature branch, likely from Task 007.

**Details:**
The Python script will take the feature branch name and its determined primary target as input. This subtask focuses on how this input is consumed and validated against known primary branches. Leverage outputs from Task 007's categorization tool.

**Success Criteria:**
- [ ] Optimal primary target received from Task 007
- [ ] Target validated against known primary branches
- [ ] Invalid targets handled gracefully
- [ ] Input validation comprehensive

---

### 009.2: Coordinate Initial Environment Setup and Safety Checks
**Effort:** 3-4 hours
**Depends on:** 009.1

Before any Git operations, coordinate safety checks with Task 012 (Branch Backup and Safety).

**Details:**
Coordinate with Task 012 to ensure a clean working directory and valid repository state, preventing unintended data loss or conflicts. This subtask focuses on orchestrating the safety validation rather than implementing it directly.

**Success Criteria:**
- [ ] Coordination with Task 012 implemented
- [ ] Working directory validated
- [ ] Repository state verified
- [ ] Safety checks completed before proceeding

---

### 009.3: Coordinate Local Feature Branch Backup
**Effort:** 3-4 hours
**Depends on:** 009.2

Coordinate with Task 012 (Branch Backup and Safety) to create a temporary backup of the feature branch's current state before initiating any rebase operations.

**Details:**
Delegate the backup creation to Task 012's BranchBackupManager. This ensures the backup mechanism is handled by the specialized task while Task 009 coordinates the overall process.

**Success Criteria:**
- [ ] Coordination with Task 012 implemented
- [ ] Backup created before Git operations
- [ ] Backup verification completed
- [ ] Backup reference stored for potential rollback

---

### 009.4: Implement Branch Switching Logic
**Effort:** 2-3 hours
**Depends on:** 009.3

Write the Python code to programmatically switch the local Git repository to the specified feature branch.

**Details:**
Utilize `GitPython`'s `repo.git.checkout(feature_branch_name)` or `subprocess.run(['git', 'checkout', feature_branch_name], cwd=repo_path, check=True)`.

**Success Criteria:**
- [ ] Branch switching implemented with GitPython
- [ ] Error handling for invalid branch names
- [ ] Successful checkout confirmed
- [ ] Branch state verified after switching

---

### 009.5: Implement Remote Primary Branch Fetch Logic
**Effort:** 2-3 hours
**Depends on:** 009.4

Develop the code to fetch the latest changes from the determined primary target branch (`git fetch origin <primary_target>`).

**Details:**
Use `GitPython`'s `repo.remote('origin').fetch(primary_target_name)` or `subprocess.run(['git', 'fetch', 'origin', primary_target_name], cwd=repo_path, check=True)`. Include error handling for network issues or non-existent remotes/branches.

**Success Criteria:**
- [ ] Remote fetch implemented with GitPython
- [ ] Error handling for network issues
- [ ] Fetch verification completed
- [ ] Primary branch updates retrieved

---

### 009.6: Coordinate Core Rebase Initiation with Specialized Tasks
**Effort:** 4-5 hours
**Depends on:** 009.5

Coordinate the command execution for initiating the Git rebase operation, leveraging specialized tasks for complex operations.

**Details:**
Execute `subprocess.run(['git', 'rebase', f'origin/{primary_target_name}'], cwd=repo_path, check=True, capture_output=True, text=True)` or `repo.git.rebase(f'origin/{primary_target_name}')`. Capture output for status and potential conflict detection. Coordinate with Task 013 for advanced rebase strategies.

**Success Criteria:**
- [ ] Rebase initiation coordinated
- [ ] Output captured for status analysis
- [ ] Conflict detection prepared
- [ ] Error handling implemented

---

### 009.7: Coordinate Conflict Detection and Resolution
**Effort:** 4-5 hours
**Depends on:** 009.6

Coordinate with Task 013 (Conflict Detection and Resolution) when the rebase operation encounters conflicts.

**Details:**
Delegate conflict detection and resolution to Task 013's ConflictDetectionResolver. This subtask focuses on orchestrating the handoff to the specialized conflict resolution task rather than implementing conflict handling directly.

**Success Criteria:**
- [ ] Coordination with Task 013 implemented
- [ ] Conflict detection handoff operational
- [ ] Resolution guidance provided
- [ ] Resolution status monitored

---

### 009.8: Coordinate Post-Rebase Validation
**Effort:** 3-4 hours
**Depends on:** 009.7

Coordinate with Task 014 (Validation and Verification) to perform automated checks to validate the integrity and correctness of the rebased feature branch.

**Details:**
Delegate validation to Task 014's ValidationVerificationFramework. This ensures comprehensive and consistent validation procedures.

**Success Criteria:**
- [ ] Coordination with Task 014 implemented
- [ ] Validation procedures executed
- [ ] Integrity checks completed
- [ ] Validation results processed

---

### 009.9: Coordinate Rollback to Backup Mechanism
**Effort:** 3-4 hours
**Depends on:** 009.6

Coordinate with Task 015 (Rollback and Recovery) to revert the feature branch to its pre-alignment backup state if a rebase operation ultimately fails or is aborted by the user.

**Details:**
Delegate rollback operations to Task 015's RollbackRecoveryMechanisms. This ensures reliable and consistent rollback procedures.

**Success Criteria:**
- [ ] Coordination with Task 015 implemented
- [ ] Rollback procedures available
- [ ] Backup restoration functional
- [ ] Rollback status tracked

---

### 009.10: Develop Progress Tracking and User Feedback
**Effort:** 2-3 hours
**Depends on:** 009.6, 009.7, 009.8

Add clear progress indicators and descriptive messages throughout the alignment process to keep the user informed.

**Details:**
Implement logging statements for each major step: fetching, checking out branch, initiating rebase, detecting conflicts, etc. Coordinate with specialized tasks to provide unified progress reporting.

**Success Criteria:**
- [ ] Progress indicators implemented
- [ ] User feedback provided at each step
- [ ] Unified reporting coordinated
- [ ] Status updates timely and informative

---

## Specification

### Module Interface

```python
class CoreAlignmentOrchestrator:
    def __init__(self, repo_path: str, config_path: str = None)
    def align_branch(self, feature_branch: str, primary_target: str) -> AlignmentResult
    def coordinate_with_task_012_safety(self, branch_name: str) -> SafetyCheckResult
    def coordinate_with_task_013_conflicts(self, branch_name: str) -> ConflictResolutionResult
    def coordinate_with_task_014_validation(self, branch_name: str) -> ValidationResult
    def coordinate_with_task_015_rollback(self, branch_name: str, backup_ref: str) -> RollbackResult
```

### Output Format

```json
{
  "alignment_operation": {
    "operation_id": "align-20260112-120000-001",
    "feature_branch": "feature/auth-system",
    "primary_target": "main",
    "status": "completed",
    "start_time": "2026-01-12T12:00:00Z",
    "end_time": "2026-01-12T12:05:00Z",
    "duration_seconds": 300
  },
  "coordinated_tasks": {
    "task_012_safety": {
      "status": "completed",
      "backup_created": "feature-auth-system-backup-20260112-120000",
      "safety_checks_passed": true
    },
    "task_013_conflicts": {
      "status": "completed",
      "conflicts_detected": 2,
      "conflicts_resolved": 2,
      "resolution_time_seconds": 120
    },
    "task_014_validation": {
      "status": "completed",
      "validation_passed": true,
      "issues_found": 0
    },
    "task_015_rollback": {
      "status": "not_needed",
      "backup_preserved": true
    }
  },
  "alignment_result": {
    "success": true,
    "commits_aligned": 15,
    "new_ancestor_commit": "a1b2c3d4e5f6",
    "linear_history_maintained": true
  },
  "performance_metrics": {
    "total_time_seconds": 300,
    "breakdown": {
      "safety_checks": 5,
      "backup_creation": 8,
      "rebase_operation": 180,
      "conflict_resolution": 120,
      "validation": 15,
      "cleanup": 2
    }
  }
}
```

---

## Implementation Guide

### 009.6: Coordinate Core Rebase Initiation with Specialized Tasks

**Objective:** Coordinate the core rebase operation with specialized tasks

**Detailed Steps:**

1. Prepare rebase command with proper error handling
   ```python
   def coordinate_rebase_initiation(self, feature_branch: str, primary_target: str) -> RebaseResult:
       try:
           # Switch to feature branch first
           self.repo.git.checkout(feature_branch)

           # Fetch latest from primary target
           self.repo.remote('origin').fetch(primary_target)

           # Execute rebase operation
           result = self.repo.git.rebase(f'origin/{primary_target}',
                                        capture_output=True,
                                        with_extended_output=True)

           # Check if rebase completed successfully
           if result.returncode == 0:
               return RebaseResult(
                   success=True,
                   output=result.stdout,
                   rebase_in_progress=False,
                   conflicts_resolved=0
               )
           else:
               # Check if it's a conflict (return code 1 is often conflicts)
               if 'CONFLICT' in result.stderr or self.repo.is_dirty(untracked_files=True):
                   return RebaseResult(
                       success=False,
                       output=result.stdout,
                       error=result.stderr,
                       rebase_in_progress=True,  # Conflicts to resolve
                       conflicts_resolved=0
                   )
               else:
                   # Actual error
                   return RebaseResult(
                       success=False,
                       output=result.stdout,
                       error=result.stderr,
                       rebase_in_progress=False,
                       conflicts_resolved=0
                   )
       except GitCommandError as e:
           return RebaseResult(
               success=False,
               output="",
               error=str(e),
               rebase_in_progress=False,
               conflicts_resolved=0
           )
   ```

2. Coordinate with Task 013 for conflict resolution
   ```python
   def handle_rebase_conflicts(self, feature_branch: str) -> ConflictResolutionResult:
       # Detect conflicts
       unmerged_blobs = self.repo.index.unmerged_blobs()
       conflicted_files = list(unmerged_blobs.keys())

       if not conflicted_files:
           return ConflictResolutionResult(
               conflicts_detected=False,
               files_affected=[],
               resolution_status="no_conflicts"
           )

       # Coordinate with Task 013 for conflict resolution
       conflict_resolver = Task013ConflictDetectorResolver(self.repo.working_dir)
       resolution_result = conflict_resolver.resolve_conflicts(
           branch_name=feature_branch,
           conflicted_files=conflicted_files
       )

       return resolution_result
   ```

3. Implement proper error handling
   ```python
   def safe_rebase_operation(self, feature_branch: str, primary_target: str) -> SafeRebaseResult:
       original_branch = self.repo.active_branch.name

       try:
           # Ensure we're on the right branch
           if original_branch != feature_branch:
               self.repo.git.checkout(feature_branch)

           # Fetch latest from target
           self.repo.remote('origin').fetch(primary_target)

           # Attempt rebase
           rebase_result = self.coordinate_rebase_initiation(feature_branch, primary_target)

           # If conflicts occurred, handle them
           if not rebase_result.success and rebase_result.rebase_in_progress:
               conflict_result = self.handle_rebase_conflicts(feature_branch)
               rebase_result.conflicts_resolved = conflict_result.conflicts_resolved

               # If conflicts were resolved, continue rebase
               if conflict_result.resolution_status == "completed":
                   try:
                       self.repo.git.rebase('--continue')
                       rebase_result.success = True
                       rebase_result.rebase_in_progress = False
                   except GitCommandError:
                       # If continue fails, we might need to abort
                       pass

           return SafeRebaseResult(
               rebase_result=rebase_result,
               original_branch=original_branch,
               operation_successful=rebase_result.success
           )
       except Exception as e:
           # Ensure we return to original branch on error
           if self.repo.active_branch.name != original_branch:
               self.repo.git.checkout(original_branch)
           raise e
   ```

4. Test with various rebase scenarios

**Testing:**
- Successful rebases should complete properly
- Conflicts should be detected and handled
- Error conditions should be handled gracefully
- Branch state should be preserved appropriately

**Performance:**
- Must complete in <5 seconds for typical rebases
- Memory: <10 MB per operation

---

## Configuration Parameters

Create `config/task_009_alignment_orchestration.yaml`:

```yaml
alignment:
  primary_targets: ["main", "scientific", "orchestration-tools"]
  rebase_timeout_minutes: 10
  conflict_resolution_enabled: true
  validation_after_rebase: true
  rollback_on_failure: true
  progress_reporting: true

coordination:
  task_012_integration: true
  task_013_integration: true
  task_014_integration: true
  task_015_integration: true
  safety_check_timeout_seconds: 30
  validation_timeout_seconds: 60

rebase:
  strategy: "rebase"  # rebase, merge, cherry-pick
  preserve_merges: false
  autosquash: false
  git_command_timeout_seconds: 30
```

Load in code:
```python
import yaml

with open('config/task_009_alignment_orchestration.yaml') as f:
    CONFIG = yaml.safe_load(f)

# Use: CONFIG['alignment']['primary_targets']
```

---

## Performance Targets

### Per Component
- Branch switching: <1 second
- Remote fetch: <2 seconds
- Rebase initiation: <3 seconds
- Conflict coordination: <5 seconds
- Memory usage: <15 MB per operation

### Scalability
- Handle repositories with 10,000+ commits
- Support multiple concurrent alignment operations
- Efficient for large file repositories

### Quality Metrics
- No timeouts on standard hardware
- Consistent performance across repository sizes
- Reliable coordination with specialized tasks

---

## Testing Strategy

### Unit Tests

Minimum 8 test cases:

```python
def test_optimal_target_integration():
    # Optimal target determination should integrate properly

def test_safety_check_coordination():
    # Coordination with Task 012 safety checks should work

def test_backup_coordination():
    # Coordination with Task 012 backup should work

def test_rebase_initiation_coordination():
    # Coordination of rebase initiation should work

def test_conflict_resolution_coordination():
    # Coordination with Task 013 should work

def test_validation_coordination():
    # Coordination with Task 014 should work

def test_rollback_coordination():
    # Coordination with Task 015 should work

def test_performance():
    # Operations complete within performance targets
```

### Integration Tests

After all subtasks complete:

```python
def test_full_alignment_orchestration():
    # Verify 009 output is compatible with Task 010 input

def test_alignment_integration():
    # Validate orchestration works with real repositories
```

### Coverage Target
- Code coverage: > 95%
- All edge cases covered
- All error paths tested

---

## Common Gotchas & Solutions

**Gotcha 1: Branch state management during rebase**
```python
# WRONG
not tracking original branch state during rebase operations

# RIGHT
save original branch state and restore if needed
```

**Gotcha 2: Conflict detection**
```python
# WRONG
only checking return code to detect conflicts

# RIGHT
check both return code and repository state for conflicts
```

**Gotcha 3: Coordination with specialized tasks**
```python
# WRONG
tight coupling with specialized task implementations

# RIGHT
loose coupling through well-defined interfaces
```

**Gotcha 4: Error propagation**
```python
# WRONG
not properly propagating errors from specialized tasks

# RIGHT
proper error handling and propagation from all coordinated tasks
```

---

## Integration Checkpoint

**When to move to Task 010 (Complex alignment):**

- [ ] All 10 subtasks complete
- [ ] Unit tests passing (>95% coverage)
- [ ] Core alignment orchestration working
- [ ] No validation errors on test data
- [ ] Performance targets met (<15s for operations)
- [ ] Integration with specialized tasks validated
- [ ] Code review approved
- [ ] Commit message: "feat: complete Task 009 Core Alignment Orchestration"

---

## Done Definition

Task 009 is done when:

1. ✅ All 10 subtasks marked complete
2. ✅ Unit tests pass (>95% coverage) on CI/CD
3. ✅ Code review approved
4. ✅ Outputs match specification exactly
5. ✅ Output schema validation passes
6. ✅ Documentation complete and accurate
7. ✅ Performance benchmarks met
8. ✅ Ready for hand-off to Task 010
9. ✅ Commit: "feat: complete Task 009 Core Alignment Orchestration"
10. ✅ All success criteria checkboxes marked complete

---

## Next Steps

1. **Immediate:** Implement subtask 009.1 (Integrate Optimal Target Determination)
2. **Week 1:** Complete subtasks 009.1 through 009.5
3. **Week 2:** Complete subtasks 009.6 through 009.10
4. **Week 2:** Write and test unit tests (target: >95%)
5. **Week 2:** Code review
6. **Week 2:** Ready for Task 010 (Complex alignment)

**Reference:** See IMPLEMENTATION_INDEX.md for team coordination
- **Priority**: High
**Effort:** 28-40 hours
**Complexity:** 8/10
**Dependencies:** 004, 006, 007, 012, 013, 014, 015, 022

---

## Purpose

Implement the core orchestrator for multistage branch alignment operations that coordinates with specialized tasks for backup/safety (Task 012), conflict resolution (Task 013), validation (Task 014), and rollback/recovery (Task 015). This task serves as the main entry point for the alignment process while delegating specialized operations to dedicated tasks.

**Scope:** Core alignment orchestration only
**Blocks:** Task 010 (Complex branch alignment), Task 011 (Validation integration)

---

## Success Criteria

Task 009 is complete when:

### Core Functionality
- [ ] Optimal primary target determination integration operational
- [ ] Environment setup and safety checks coordinated with Task 012
- [ ] Branch switching and fetching logic operational
- [ ] Core rebase initiation coordinated with specialized tasks
- [ ] Conflict detection and resolution coordinated with Task 013
- [ ] Post-rebase validation coordinated with Task 014
- [ ] Rollback mechanisms coordinated with Task 015
- [ ] Progress tracking and reporting functional

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <15 seconds for orchestration operations
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

### Integration Readiness
- [ ] Compatible with Task 010 requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 004 (Git operations framework) complete
- [ ] Task 006 (Backup/restore mechanism) complete
- [ ] Task 007 (Feature branch identification) complete
- [ ] Task 012 (Branch backup and safety) complete
- [ ] Task 013 (Conflict detection and resolution) complete
- [ ] Task 014 (Validation and verification) complete
- [ ] Task 015 (Rollback and recovery) complete
- [ ] Task 022 (Architectural migration) complete
- [ ] GitPython or subprocess for git commands available
- [ ] Test infrastructure in place

### Blocks (What This Task Unblocks)
- Task 010 (Complex branch alignment)
- Task 011 (Validation integration)

### External Dependencies
- Python 3.8+
- GitPython or subprocess for git commands
- Specialized tasks (012, 013, 014, 015)

---

## Subtasks Breakdown

### 009.1: Integrate Optimal Primary Target Determination
**Effort:** 2-3 hours
**Depends on:** None

Develop logic to receive and validate the optimal primary branch target (e.g., main, scientific, orchestration-tools) for the feature branch, likely from Task 007.

**Details:**
The Python script will take the feature branch name and its determined primary target as input. This subtask focuses on how this input is consumed and validated against known primary branches. Leverage outputs from Task 007's categorization tool.

**Success Criteria:**
- [ ] Optimal primary target received from Task 007
- [ ] Target validated against known primary branches
- [ ] Invalid targets handled gracefully
- [ ] Input validation comprehensive

---

### 009.2: Coordinate Initial Environment Setup and Safety Checks
**Effort:** 3-4 hours
**Depends on:** 009.1

Before any Git operations, coordinate safety checks with Task 012 (Branch Backup and Safety).

**Details:**
Coordinate with Task 012 to ensure a clean working directory and valid repository state, preventing unintended data loss or conflicts. This subtask focuses on orchestrating the safety validation rather than implementing it directly.

**Success Criteria:**
- [ ] Coordination with Task 012 implemented
- [ ] Working directory validated
- [ ] Repository state verified
- [ ] Safety checks completed before proceeding

---

### 009.3: Coordinate Local Feature Branch Backup
**Effort:** 3-4 hours
**Depends on:** 009.2

Coordinate with Task 012 (Branch Backup and Safety) to create a temporary backup of the feature branch's current state before initiating any rebase operations.

**Details:**
Delegate the backup creation to Task 012's BranchBackupManager. This ensures the backup mechanism is handled by the specialized task while Task 009 coordinates the overall process.

**Success Criteria:**
- [ ] Coordination with Task 012 implemented
- [ ] Backup created before Git operations
- [ ] Backup verification completed
- [ ] Backup reference stored for potential rollback

---

### 009.4: Implement Branch Switching Logic
**Effort:** 2-3 hours
**Depends on:** 009.3

Write the Python code to programmatically switch the local Git repository to the specified feature branch.

**Details:**
Utilize `GitPython`'s `repo.git.checkout(feature_branch_name)` or `subprocess.run(['git', 'checkout', feature_branch_name], cwd=repo_path, check=True)`.

**Success Criteria:**
- [ ] Branch switching implemented with GitPython
- [ ] Error handling for invalid branch names
- [ ] Successful checkout confirmed
- [ ] Branch state verified after switching

---

### 009.5: Implement Remote Primary Branch Fetch Logic
**Effort:** 2-3 hours
**Depends on:** 009.4

Develop the code to fetch the latest changes from the determined primary target branch (`git fetch origin <primary_target>`).

**Details:**
Use `GitPython`'s `repo.remote('origin').fetch(primary_target_name)` or `subprocess.run(['git', 'fetch', 'origin', primary_target_name], cwd=repo_path, check=True)`. Include error handling for network issues or non-existent remotes/branches.

**Success Criteria:**
- [ ] Remote fetch implemented with GitPython
- [ ] Error handling for network issues
- [ ] Fetch verification completed
- [ ] Primary branch updates retrieved

---

### 009.6: Coordinate Core Rebase Initiation with Specialized Tasks
**Effort:** 4-5 hours
**Depends on:** 009.5

Coordinate the command execution for initiating the Git rebase operation, leveraging specialized tasks for complex operations.

**Details:**
Execute `subprocess.run(['git', 'rebase', f'origin/{primary_target_name}'], cwd=repo_path, check=True, capture_output=True, text=True)` or `repo.git.rebase(f'origin/{primary_target_name}')`. Capture output for status and potential conflict detection. Coordinate with Task 013 for advanced rebase strategies.

**Success Criteria:**
- [ ] Rebase initiation coordinated
- [ ] Output captured for status analysis
- [ ] Conflict detection prepared
- [ ] Error handling implemented

---

### 009.7: Coordinate Conflict Detection and Resolution
**Effort:** 4-5 hours
**Depends on:** 009.6

Coordinate with Task 013 (Conflict Detection and Resolution) when the rebase operation encounters conflicts.

**Details:**
Delegate conflict detection and resolution to Task 013's ConflictDetectionResolver. This subtask focuses on orchestrating the handoff to the specialized conflict resolution task rather than implementing conflict handling directly.

**Success Criteria:**
- [ ] Coordination with Task 013 implemented
- [ ] Conflict detection handoff operational
- [ ] Resolution guidance provided
- [ ] Resolution status monitored

---

### 009.8: Coordinate Post-Rebase Validation
**Effort:** 3-4 hours
**Depends on:** 009.7

Coordinate with Task 014 (Validation and Verification) to perform automated checks to validate the integrity and correctness of the rebased feature branch.

**Details:**
Delegate validation to Task 014's ValidationVerificationFramework. This ensures comprehensive and consistent validation procedures.

**Success Criteria:**
- [ ] Coordination with Task 014 implemented
- [ ] Validation procedures executed
- [ ] Integrity checks completed
- [ ] Validation results processed

---

### 009.9: Coordinate Rollback to Backup Mechanism
**Effort:** 3-4 hours
**Depends on:** 009.6

Coordinate with Task 015 (Rollback and Recovery) to revert the feature branch to its pre-alignment backup state if a rebase operation ultimately fails or is aborted by the user.

**Details:**
Delegate rollback operations to Task 015's RollbackRecoveryMechanisms. This ensures reliable and consistent rollback procedures.

**Success Criteria:**
- [ ] Coordination with Task 015 implemented
- [ ] Rollback procedures available
- [ ] Backup restoration functional
- [ ] Rollback status tracked

---

### 009.10: Develop Progress Tracking and User Feedback
**Effort:** 2-3 hours
**Depends on:** 009.6, 009.7, 009.8

Add clear progress indicators and descriptive messages throughout the alignment process to keep the user informed.

**Details:**
Implement logging statements for each major step: fetching, checking out branch, initiating rebase, detecting conflicts, etc. Coordinate with specialized tasks to provide unified progress reporting.

**Success Criteria:**
- [ ] Progress indicators implemented
- [ ] User feedback provided at each step
- [ ] Unified reporting coordinated
- [ ] Status updates timely and informative

---

## Specification

### Module Interface

```python
class CoreAlignmentOrchestrator:
    def __init__(self, repo_path: str, config_path: str = None)
    def align_branch(self, feature_branch: str, primary_target: str) -> AlignmentResult
    def coordinate_with_task_012_safety(self, branch_name: str) -> SafetyCheckResult
    def coordinate_with_task_013_conflicts(self, branch_name: str) -> ConflictResolutionResult
    def coordinate_with_task_014_validation(self, branch_name: str) -> ValidationResult
    def coordinate_with_task_015_rollback(self, branch_name: str, backup_ref: str) -> RollbackResult
```

### Output Format

```json
{
  "alignment_operation": {
    "operation_id": "align-20260112-120000-001",
    "feature_branch": "feature/auth-system",
    "primary_target": "main",
    "status": "completed",
    "start_time": "2026-01-12T12:00:00Z",
    "end_time": "2026-01-12T12:05:00Z",
    "duration_seconds": 300
  },
  "coordinated_tasks": {
    "task_012_safety": {
      "status": "completed",
      "backup_created": "feature-auth-system-backup-20260112-120000",
      "safety_checks_passed": true
    },
    "task_013_conflicts": {
      "status": "completed",
      "conflicts_detected": 2,
      "conflicts_resolved": 2,
      "resolution_time_seconds": 120
    },
    "task_014_validation": {
      "status": "completed",
      "validation_passed": true,
      "issues_found": 0
    },
    "task_015_rollback": {
      "status": "not_needed",
      "backup_preserved": true
    }
  },
  "alignment_result": {
    "success": true,
    "commits_aligned": 15,
    "new_ancestor_commit": "a1b2c3d4e5f6",
    "linear_history_maintained": true
  },
  "performance_metrics": {
    "total_time_seconds": 300,
    "breakdown": {
      "safety_checks": 5,
      "backup_creation": 8,
      "rebase_operation": 180,
      "conflict_resolution": 120,
      "validation": 15,
      "cleanup": 2
    }
  }
}
```

---

## Implementation Guide

### 009.6: Coordinate Core Rebase Initiation with Specialized Tasks

**Objective:** Coordinate the core rebase operation with specialized tasks

**Detailed Steps:**

1. Prepare rebase command with proper error handling
   ```python
   def coordinate_rebase_initiation(self, feature_branch: str, primary_target: str) -> RebaseResult:
       try:
           # Switch to feature branch first
           self.repo.git.checkout(feature_branch)

           # Fetch latest from primary target
           self.repo.remote('origin').fetch(primary_target)

           # Execute rebase operation
           result = self.repo.git.rebase(f'origin/{primary_target}',
                                        capture_output=True,
                                        with_extended_output=True)

           # Check if rebase completed successfully
           if result.returncode == 0:
               return RebaseResult(
                   success=True,
                   output=result.stdout,
                   rebase_in_progress=False,
                   conflicts_resolved=0
               )
           else:
               # Check if it's a conflict (return code 1 is often conflicts)
               if 'CONFLICT' in result.stderr or self.repo.is_dirty(untracked_files=True):
                   return RebaseResult(
                       success=False,
                       output=result.stdout,
                       error=result.stderr,
                       rebase_in_progress=True,  # Conflicts to resolve
                       conflicts_resolved=0
                   )
               else:
                   # Actual error
                   return RebaseResult(
                       success=False,
                       output=result.stdout,
                       error=result.stderr,
                       rebase_in_progress=False,
                       conflicts_resolved=0
                   )
       except GitCommandError as e:
           return RebaseResult(
               success=False,
               output="",
               error=str(e),
               rebase_in_progress=False,
               conflicts_resolved=0
           )
   ```

2. Coordinate with Task 013 for conflict resolution
   ```python
   def handle_rebase_conflicts(self, feature_branch: str) -> ConflictResolutionResult:
       # Detect conflicts
       unmerged_blobs = self.repo.index.unmerged_blobs()
       conflicted_files = list(unmerged_blobs.keys())

       if not conflicted_files:
           return ConflictResolutionResult(
               conflicts_detected=False,
               files_affected=[],
               resolution_status="no_conflicts"
           )

       # Coordinate with Task 013 for conflict resolution
       conflict_resolver = Task013ConflictDetectorResolver(self.repo.working_dir)
       resolution_result = conflict_resolver.resolve_conflicts(
           branch_name=feature_branch,
           conflicted_files=conflicted_files
       )

       return resolution_result
   ```

3. Implement proper error handling
   ```python
   def safe_rebase_operation(self, feature_branch: str, primary_target: str) -> SafeRebaseResult:
       original_branch = self.repo.active_branch.name

       try:
           # Ensure we're on the right branch
           if original_branch != feature_branch:
               self.repo.git.checkout(feature_branch)

           # Fetch latest from target
           self.repo.remote('origin').fetch(primary_target)

           # Attempt rebase
           rebase_result = self.coordinate_rebase_initiation(feature_branch, primary_target)

           # If conflicts occurred, handle them
           if not rebase_result.success and rebase_result.rebase_in_progress:
               conflict_result = self.handle_rebase_conflicts(feature_branch)
               rebase_result.conflicts_resolved = conflict_result.conflicts_resolved

               # If conflicts were resolved, continue rebase
               if conflict_result.resolution_status == "completed":
                   try:
                       self.repo.git.rebase('--continue')
                       rebase_result.success = True
                       rebase_result.rebase_in_progress = False
                   except GitCommandError:
                       # If continue fails, we might need to abort
                       pass

           return SafeRebaseResult(
               rebase_result=rebase_result,
               original_branch=original_branch,
               operation_successful=rebase_result.success
           )
       except Exception as e:
           # Ensure we return to original branch on error
           if self.repo.active_branch.name != original_branch:
               self.repo.git.checkout(original_branch)
           raise e
   ```

4. Test with various rebase scenarios

**Testing:**
- Successful rebases should complete properly
- Conflicts should be detected and handled
- Error conditions should be handled gracefully
- Branch state should be preserved appropriately

**Performance:**
- Must complete in <5 seconds for typical rebases
- Memory: <10 MB per operation

---

## Configuration Parameters

Create `config/task_009_alignment_orchestration.yaml`:

```yaml
alignment:
  primary_targets: ["main", "scientific", "orchestration-tools"]
  rebase_timeout_minutes: 10
  conflict_resolution_enabled: true
  validation_after_rebase: true
  rollback_on_failure: true
  progress_reporting: true

coordination:
  task_012_integration: true
  task_013_integration: true
  task_014_integration: true
  task_015_integration: true
  safety_check_timeout_seconds: 30
  validation_timeout_seconds: 60

rebase:
  strategy: "rebase"  # rebase, merge, cherry-pick
  preserve_merges: false
  autosquash: false
  git_command_timeout_seconds: 30
```

Load in code:
```python
import yaml

with open('config/task_009_alignment_orchestration.yaml') as f:
    CONFIG = yaml.safe_load(f)

# Use: CONFIG['alignment']['primary_targets']
```

---

## Performance Targets

### Per Component
- Branch switching: <1 second
- Remote fetch: <2 seconds
- Rebase initiation: <3 seconds
- Conflict coordination: <5 seconds
- Memory usage: <15 MB per operation

### Scalability
- Handle repositories with 10,000+ commits
- Support multiple concurrent alignment operations
- Efficient for large file repositories

### Quality Metrics
- No timeouts on standard hardware
- Consistent performance across repository sizes
- Reliable coordination with specialized tasks

---

## Testing Strategy

### Unit Tests

Minimum 8 test cases:

```python
def test_optimal_target_integration():
    # Optimal target determination should integrate properly

def test_safety_check_coordination():
    # Coordination with Task 012 safety checks should work

def test_backup_coordination():
    # Coordination with Task 012 backup should work

def test_rebase_initiation_coordination():
    # Coordination of rebase initiation should work

def test_conflict_resolution_coordination():
    # Coordination with Task 013 should work

def test_validation_coordination():
    # Coordination with Task 014 should work

def test_rollback_coordination():
    # Coordination with Task 015 should work

def test_performance():
    # Operations complete within performance targets
```

### Integration Tests

After all subtasks complete:

```python
def test_full_alignment_orchestration():
    # Verify 009 output is compatible with Task 010 input

def test_alignment_integration():
    # Validate orchestration works with real repositories
```

### Coverage Target
- Code coverage: > 95%
- All edge cases covered
- All error paths tested

---

## Common Gotchas & Solutions

**Gotcha 1: Branch state management during rebase**
```python
# WRONG
not tracking original branch state during rebase operations

# RIGHT
save original branch state and restore if needed
```

**Gotcha 2: Conflict detection**
```python
# WRONG
only checking return code to detect conflicts

# RIGHT
check both return code and repository state for conflicts
```

**Gotcha 3: Coordination with specialized tasks**
```python
# WRONG
tight coupling with specialized task implementations

# RIGHT
loose coupling through well-defined interfaces
```

**Gotcha 4: Error propagation**
```python
# WRONG
not properly propagating errors from specialized tasks

# RIGHT
proper error handling and propagation from all coordinated tasks
```

---

## Integration Checkpoint

**When to move to Task 010 (Complex alignment):**

- [ ] All 10 subtasks complete
- [ ] Unit tests passing (>95% coverage)
- [ ] Core alignment orchestration working
- [ ] No validation errors on test data
- [ ] Performance targets met (<15s for operations)
- [ ] Integration with specialized tasks validated
- [ ] Code review approved
- [ ] Commit message: "feat: complete Task 009 Core Alignment Orchestration"

---

## Done Definition

Task 009 is done when:

1. ✅ All 10 subtasks marked complete
2. ✅ Unit tests pass (>95% coverage) on CI/CD
3. ✅ Code review approved
4. ✅ Outputs match specification exactly
5. ✅ Output schema validation passes
6. ✅ Documentation complete and accurate
7. ✅ Performance benchmarks met
8. ✅ Ready for hand-off to Task 010
9. ✅ Commit: "feat: complete Task 009 Core Alignment Orchestration"
10. ✅ All success criteria checkboxes marked complete

---

## Next Steps

1. **Immediate:** Implement subtask 009.1 (Integrate Optimal Target Determination)
2. **Week 1:** Complete subtasks 009.1 through 009.5
3. **Week 2:** Complete subtasks 009.6 through 009.10
4. **Week 2:** Write and test unit tests (target: >95%)
5. **Week 2:** Code review
6. **Week 2:** Ready for Task 010 (Complex alignment)

**Reference:** See IMPLEMENTATION_INDEX.md for team coordination
- **Effort**: N/A
- **Complexity**: N/A

## Implementation Guide



## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

## Performance Targets

- **Effort Range**: TBD
- **Complexity Level**: TBD

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


## Common Gotchas & Solutions

- [ ] [Common issues and solutions to be documented]

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

## Done Definition

### Completion Criteria
- [ ] All success criteria checkboxes marked complete
- [ ] Code quality standards met (PEP 8, documentation)
- [ ] Performance targets achieved
- [ ] All subtasks completed
- [ ] Integration checkpoint criteria satisfied

## Next Steps

- [ ] No next steps specified
- [ ] Additional steps to be defined


<!-- EXTENDED_METADATA
END_EXTENDED_METADATA -->
