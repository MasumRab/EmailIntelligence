# Task 011.7: Fail the Stage on a New Security Finding, Not the Backlog

**Status:** specified
**Priority:** high
**Effort:** 3-4 hours
**Complexity:** 5/10
**Dependencies:** 011.1
**Created:** 2026-01-06
**Parent:** Task 011: Integrate Validation Framework into Multistage Alignment Workflow

## Sub-subtasks Breakdown

### 1.1: Execute Task
- Complete 011.7: Integrate Security Scans (SAST and Dependency)
- Verify completion
- Update status



---

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

## Success Criteria

- [ ] SAST integrated - Verification: [Method to verify completion]
- [ ] Dependency scanning integrated - Verification: [Method to verify completion]
- [ ] Critical issues block merge - Verification: [Method to verify completion]
- [ ] Reports generated - Verification: [Method to verify completion]


---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 011.8**: Consolidate Validation Results

## Specification Details

### Task Interface
- **ID**: TBD
- **Title**: TBD
- **Status**: TBD
- **Priority**: TBD
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The stage compares the branch's findings to the target's findings for the same rule set and fails
   only on findings that the branch introduced.
2. The comparison key is (rule id, file, line), so a finding that merely moved within a file is
   reported but does not block.
3. The full finding set is written to the run state, so the operator can see the backlog without
   re-running bandit.
4. Exit codes from `bandit` and the dependency audit are honoured individually, and neither is invoked
   with `|| true` -- unlike `.github/workflows/ci.yml:46`, which discards bandit's exit code.

## Implementation Guide




## Prerequisites & Dependencies

### Required Before Starting
- [ ] No external prerequisites

### Blocks (What This Task Unblocks)
- [ ] No specific blocks defined

### External Dependencies
- [ ] No external dependencies

## Overview/Purpose

The security layer from 008.7 has to be honest about the repository's existing findings: it currently
has a backlog, so a gate that fails on any finding fails on every branch. This task defines the
incremental test.

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
