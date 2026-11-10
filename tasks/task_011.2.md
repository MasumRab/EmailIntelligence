# Task 011.2: Wire Validation Into the Alignment Runner, Not a Second Workflow

**Status:** specified
**Priority:** high
**Effort:** 2-3 hours
**Complexity:** 4/10
**Dependencies:** None
**Created:** 2026-01-06
**Parent:** Task 011: Integrate Validation Framework into Multistage Alignment Workflow

## Sub-subtasks Breakdown

### 1.1: Execute Task
- Complete 011.2: Configure GitHub Actions Workflow and Triggers
- Verify completion
- Update status



---

## Purpose

Set up GitHub Actions workflow to trigger validation on PRs.

---

## Details

Create `.github/workflows/merge-validation.yml` with proper triggers.

### Workflow Configuration

```yaml
name: Merge Validation

on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run validation
        run: python scripts/run_validation.py
```

---

## Success Criteria

- [ ] Workflow file created - Implementation passes all validation checks and meets specified requirements - Verification: [Method to verify completion]
- [ ] Triggers on PR to main - Verification: [Method to verify completion]
- [ ] Python environment configured - Verification: [Method to verify completion]
- [ ] Placeholder for validation steps - Verification: [Method to verify completion]


---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 011.3**: Implement Architectural Enforcement

## Specification Details

### Task Interface
- **ID**: TBD
- **Title**: TBD
- **Status**: TBD
- **Priority**: TBD
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The runner invokes validation through one function,
   `scripts/alignment/validate_stage.run(stage)`, and the CI workflow and the local run call the same
   underlying scripts -- never two implementations of one check.
2. The function returns a structured result (`stage`, `check`, `status`, `exit_code`,
   `duration_s`), not a printed string, so the caller can branch on it.
3. A check that cannot run (missing tool, missing dependency) is `skipped` with the reason recorded,
   and a stage whose required check is `skipped` fails; only advisory checks may skip.
4. No check is invoked through `shell=True` with an interpolated string -- the argv is a list, because
   a branch name reaches these commands.

## Implementation Guide




## Prerequisites & Dependencies

### Required Before Starting
- [ ] No external prerequisites

### Blocks (What This Task Unblocks)
- [ ] No specific blocks defined

### External Dependencies
- [ ] No external dependencies

## Overview/Purpose

Group 008 builds `.github/workflows/merge-validation.yml` for pull requests. A single-developer
alignment run happens in a worktree before any PR exists, so the runner cannot depend on it: this
task is the in-process path, and the workflow is the CI mirror of the same checks.

## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

## Performance Targets

- **Effort Range**: TBD
- **Complexity Level**: TBD

## Testing Strategy

Test strategy to be defined

## Common Gotchas & Solutions

- [ ] No common gotchas identified

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

## Done Definition

### Completion Criteria
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
