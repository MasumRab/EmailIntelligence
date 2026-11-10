# Task 008.7: Integrate Security Scans (SAST and Dependency)

**Status:** specified
**Priority:** high
**Effort:** 3-4 hours
**Complexity:** 5/10
**Dependencies:** 008.1

---

## Overview/Purpose

Add security scanning to CI pipeline.

## Success Criteria

- [ ] SAST integrated
- [ ] Dependency scanning integrated
- [ ] Critical issues block merge
- [ ] Reports generated

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
- **ID**: 008.7
- **Title**: Integrate Security Scans (SAST and Dependency)
- **Status**: specified
- **Priority**: high
- **Effort**: 3-4 hours
- **Complexity**: 5/10

### Requirements
1. The gate runs `bandit` for Python and a dependency audit, and both exit codes are honoured. The
   existing `ci.yml` line is `uv run bandit -r src/ modules/ || true`, which makes every finding
   non-blocking; the new gate must not copy that suffix.
2. The bandit severity and confidence thresholds are stated (`--severity-level high` is the level
   the repository has actually been measured at), and the gate fails on findings at or above them.
3. The dependency audit covers the lockfile (`uv.lock`) and fails on a new advisory, comparing
   against a checked-in accepted-advisory list rather than an inline ignore.
4. Every suppression is a `# nosec B<id>` with a one-line reason; a bare `# nosec` is rejected by
   the requirement.

## Implementation Guide

Add the steps to `.github/workflows/merge-validation.yml`. Measure the current count first so the
gate can be set at a level that is red for new findings and not for the backlog.

```bash
uv run bandit -r src/ modules/ -f json -o reports/bandit.json --severity-level high
grep -n 'bandit' .github/workflows/ci.yml
```

Per [[ei-ci-gates-are-advisory-measured]], `--severity-level high` is the only threshold the codebase
currently passes.


## Purpose

Add security scanning to CI pipeline.

---

## Details

Integrate bandit (SAST) and safety (dependency scan).

### Security Scanning

```yaml
# In .github/workflows/merge-validation.yml
security-scan:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    
    - name: Run bandit
      run: |
        pip install bandit
        bandit -r src/ -f json -o bandit_report.json
    
    - name: Run safety
      run: |
        pip install safety
        safety check -r requirements.txt -o safety_report.json
    
    - name: Check results
      run: |
        if [ -n "$(cat bandit_report.json | jq '.results | length')" ]; then
          echo "Security issues found in bandit report"
          exit 1
        fi
```

### Configuration

- `.bandit` - Bandit configuration
- Safety checks: Critical/High only

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 008.8**: Consolidate Validation Results
**Priority:** high
**Effort:** 3-4 hours
**Complexity:** 5/10
**Dependencies:** 008.1
**Created:** 2026-01-06
**Parent:** Task 008: Create Comprehensive Merge Validation Framework

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
