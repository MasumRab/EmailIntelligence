# Task 011.3: Enforce Architecture Rules at the Pre-Alignment Stage

**Status:** specified
**Priority:** high
**Effort:** 4-5 hours
**Complexity:** 6/10
**Dependencies:** 011.1
**Created:** 2026-01-06
**Parent:** Task 011: Integrate Validation Framework into Multistage Alignment Workflow

## Sub-subtasks Breakdown

### 1.1: Execute Task
- Complete 011.3: Implement Architectural Enforcement Checks
- Verify completion
- Update status



---

## Purpose

Integrate static analysis tools to enforce architectural rules.

---

## Details

Configure ruff/flake8/mypy to check module boundaries and import rules.

### Implementation

```python
# scripts/architectural_checks.py
import subprocess
import sys

def run_architectural_checks():
    """Run all architectural enforcement checks."""
    checks = [
        ("ruff check src/", "Ruff check"),
        ("flake8 src/ --max-line-length=100", "Flake8"),
        ("mypy src/ --strict", "Type checking"),
    ]
    
    results = []
    for cmd, name in checks:
        result = subprocess.run(
            cmd.split(),
            capture_output=True,
            text=True
        )
        results.append((name, result.returncode == 0, result.stdout))
    
    return results

if __name__ == "__main__":
    success = run_architectural_checks()
    for name, passed, output in success:
        status = "PASS" if passed else "FAIL"
        print(f"{name}: {status}")
    sys.exit(0 if all(p[1] for p in success) else 1)
```

### Configuration Files

- `.ruff.toml` - Ruff configuration
- `.flake8` - Flake8 configuration
- `mypy.ini` - Type checking configuration

---

## Success Criteria

- [ ] Static analysis configured - Verification: [Method to verify completion]
- [ ] Module boundaries enforced - Verification: [Method to verify completion]
- [ ] Import rules defined - Implementation passes all validation checks and meets specified requirements - Verification: [Method to verify completion]
- [ ] CI integration working - Verification: [Method to verify completion]


---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 011.4**: Integrate Unit and Integration Tests

## Specification Details

### Task Interface
- **ID**: TBD
- **Title**: TBD
- **Status**: TBD
- **Priority**: TBD
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The pre-align stage runs the architecture check on the branch's tree, and a violation stops the
   stage before any file is modified.
2. The check reports the violating file and line, and the runner records them in the run state, so
   the operator can fix the branch without re-running the whole pipeline.
3. The stage distinguishes "new violation introduced by this branch" from "violation already present
   on the target": the second is reported and does not block, or every pre-existing branch would
   fail identically.
4. The comparison is made against the target's blob for the same path, not against a stored baseline
   that ages.

## Implementation Guide




## Prerequisites & Dependencies

### Required Before Starting
- [ ] No external prerequisites

### Blocks (What This Task Unblocks)
- [ ] No specific blocks defined

### External Dependencies
- [ ] No external dependencies

## Overview/Purpose

The architectural layer from 008.3 is a standalone script. This task is the point at which it is
actually useful: before the aligner touches a branch, so a branch that violates the import direction
is refused instead of merged and then repaired.

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
