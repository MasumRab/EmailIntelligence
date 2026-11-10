# Task 003.4: Integrate Validation Into CI Pipeline

**Status:** specified
**Priority:** high
**Effort:** 2-3 hours
**Complexity:** 4/10
**Dependencies:** 003.2

---

## Overview/Purpose

Add validation script as a mandatory pre-merge check in the CI/CD pipeline.

## Success Criteria

- [ ] CI runs validation on every PR
- [ ] Failed validation blocks merge
- [ ] Branch protection enforced
- [ ] Clear error messages in CI output

## Prerequisites & Dependencies

### Required Before Starting
- [ ] No external prerequisites

### Blocks (What This Task Unblocks)
- [ ] No specific blocks defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 003.4
- **Title**: Integrate Validation Into CI Pipeline
- **Status**: specified
- **Priority**: high
- **Effort**: 2-3 hours
- **Complexity**: 4/10

### Requirements
1. The validation runs as a step in the `test` job of `.github/workflows/ci.yml`, before the test
   run, so a missing critical file stops the job early.
2. The step does not end in `|| true`. The current `test` job runs `pytest ... || true` and
   `bandit ... || true`, which throws away the exit code; a new gate must not repeat that.
3. The step's dependencies are installed before it runs, or it imports only the standard library.
4. A failing validation is distinguishable in the job log from a failing test.
5. The gate is demonstrated by deleting a critical file on a scratch branch and observing a red job.

## Implementation Guide

Edit `.github/workflows/ci.yml`, job `test`. Add the step after checkout and setup, before
`uv run pytest`:

```yaml
- name: Validate critical files
  run: python scripts/validation/validate_critical_files.py
```

Prove it with `gh run view <id> --log` on a branch where a critical file was removed.


## Purpose

Add validation script as a mandatory pre-merge check in the CI/CD pipeline.

---

## Details

Configure GitHub Actions to run validation on all pull requests before merging.

### Steps

1. **Update CI configuration**
   - Edit `.github/workflows/pull_request.yml`
   - Add validation job

2. **Configure job settings**
   - Trigger on PR open/update
   - Run validation script
   - Fail build on validation error

3. **Set branch protection**
   - Require validation check to pass
   - Configure in GitHub settings

4. **Test CI integration**

---

## Test Strategy

- Create test PR with missing file
- Verify CI fails
- Add missing file
- Verify CI passes

---

## Implementation Notes

### GitHub Actions Workflow

```yaml
name: Critical File Validation

on:
  pull_request:
    branches: [main, scientific]

jobs:
  validate-critical-files:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Run Critical File Validation
        run: |
          python scripts/validate_critical_files.py
```

### Branch Protection Settings

| Setting | Value |
|---------|-------|
| Require status checks | validate-critical-files |
| Require branches up to date | Yes |
| Restrict who can push | As needed |

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 003.5**: Document and Communicate Validation Process
**Priority:** high
**Effort:** 2-3 hours
**Complexity:** 4/10
**Dependencies:** 003.2
**Created:** 2026-01-06
**Parent:** Task 003: Develop and Integrate Pre-merge Validation Scripts

---

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
- Create test PR with missing file
- Verify CI fails
- Add missing file
- Verify CI passes

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
