# Task 011.8: Emit One Stage Report the Operator Can Read Mid-Run

**Status:** specified
**Priority:** high
**Effort:** 2-3 hours
**Complexity:** 4/10
**Dependencies:** 011.3, 011.4, 011.6, 011.7
**Created:** 2026-01-06
**Parent:** Task 011: Integrate Validation Framework into Multistage Alignment Workflow

## Sub-subtasks Breakdown

### 1.1: Execute Task
- Complete 011.8: Consolidate Validation Results and Reporting
- Verify completion
- Update status



---

## Purpose

Aggregate results from all validation layers into unified report.

---

## Details

Create validation consolidation script.

### Consolidation Script

```python
# scripts/consolidate_results.py
import json
import sys
from pathlib import Path

REPORTS = {
    "architectural": "reports/architectural.json",
    "tests": "reports/test_results.json",
    "performance": "reports/performance.json",
    "security": "reports/security.json",
}

def consolidate():
    """Combine all validation results."""
    results = {}
    
    for name, path in REPORTS.items():
        p = Path(path)
        if p.exists():
            results[name] = json.loads(p.read_text())
        else:
            results[name] = {"status": "not_run"}
    
    # Determine overall status
    all_pass = all(
        r.get("passed", False) 
        for r in results.values()
    )
    
    output = {
        "overall": "PASS" if all_pass else "FAIL",
        "results": results,
    }
    
    Path("reports/consolidated.json").write_text(
        json.dumps(output, indent=2)
    )
    
    return all_pass

if __name__ == "__main__":
    success = consolidate()
    sys.exit(0 if success else 1)
```

---

## Success Criteria

- [ ] Results consolidated - Verification: [Method to verify completion]
- [ ] Unified report generated - Verification: [Method to verify completion]
- [ ] Clear pass/fail status - Verification: [Method to verify completion]
- [ ] GitHub summary updated - Verification: [Method to verify completion]


---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 011.9**: Configure Branch Protection Rules

## Specification Details

### Task Interface
- **ID**: TBD
- **Title**: TBD
- **Status**: TBD
- **Priority**: TBD
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. Each stage appends a section to `reports/alignment-report.md`: stage name, start and end time,
   each check's status, and the first failure with its command.
2. The report is written incrementally -- flushed after each stage -- so an interrupted run leaves a
   readable file rather than an empty one.
3. Failures come first in each section, and the report names the exact command that reproduces the
   failure, so the operator can act without reading the runner's source.
4. The report links to the raw artifacts (`stage-junit.xml`, `branch-bandit.json`) by relative path.

## Implementation Guide




## Prerequisites & Dependencies

### Required Before Starting
- [ ] No external prerequisites

### Blocks (What This Task Unblocks)
- [ ] No specific blocks defined

### External Dependencies
- [ ] No external dependencies

## Overview/Purpose

A single-developer alignment runs for hours across stages. Without a report the operator learns what
happened only at the end, by which time the cheapest fix (stop and change order) is gone.

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
