# Task 011.4: Run the Unit and Integration Suite After Each Stage Merge

**Status:** specified
**Priority:** high
**Effort:** 3-4 hours
**Complexity:** 5/10
**Dependencies:** 011.1
**Created:** 2026-01-06
**Parent:** Task 011: Integrate Validation Framework into Multistage Alignment Workflow

## Sub-subtasks Breakdown

### 1.1: Execute Task
- Complete 011.4: Integrate Existing Unit and Integration Tests
- Verify completion
- Update status



---

## Purpose

Configure CI to execute full test suite and block on failures.

---

## Details

Add pytest execution to GitHub Actions workflow.

### Implementation

```yaml
# In .github/workflows/merge-validation.yml
jobs:
  test:
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
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          pytest src/ --cov --cov-report=xml --tb=short
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
```

### Test Configuration

- `pytest.ini` or `pyproject.toml` configuration
- Coverage threshold: 90%
- Fail-fast: enabled

---

## Success Criteria

- [ ] Tests run in CI
- [ ] Coverage reported - Verification: [Method to verify completion]
- [ ] Failures block merge - Verification: [Method to verify completion]
- [ ] Coverage threshold enforced - Verification: [Method to verify completion]


---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 011.5**: Develop E2E Smoke Tests

## Specification Details

### Task Interface
- **ID**: TBD
- **Title**: TBD
- **Status**: TBD
- **Priority**: TBD
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The suite runs after each stage's merge commits land, using the same path list CI uses
   (`tests/ src/ modules/`), so a green local run means a green CI run for the same tree.
2. A red suite does not auto-revert; the runner stops, records the failing test ids in the run state,
   and prints the backup path from task 006 so reverting is one command.
3. The stage writes per-test results (`--junitxml`) and records the failing ids, because "the suite
   failed" is not actionable and a count is not a diagnosis.
4. A test that fails on the target as well as on the branch is marked pre-existing and does not block,
   determined by running the same ids on the target ref.

## Implementation Guide




## Prerequisites & Dependencies

### Required Before Starting
- [ ] No external prerequisites

### Blocks (What This Task Unblocks)
- [ ] No specific blocks defined

### External Dependencies
- [ ] No external dependencies

## Overview/Purpose

The suite is the slowest check and the one most likely to be skipped under time pressure. This task
defines when it runs, what a red result means mid-alignment, and how the operator recovers without
losing the merge that caused it.

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
