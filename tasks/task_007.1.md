# Task 007.1: Detect Merge Conflict Markers in Feature Branches

**Status:** specified
**Priority:** medium
**Effort:** 3-4 hours
**Complexity:** 5/10
**Dependencies:** None

---

## Overview/Purpose

Detect merge conflict markers in feature branches to identify broken or poorly merged branches.

## Success Criteria

- [ ] Merge markers detected
- [ ] Branches flagged appropriately
- [ ] Confidence scores reduced
- [ ] Output includes artifact flags

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
- **ID**: 007.1
- **Title**: Detect Merge Conflict Markers in Feature Branches
- **Status**: specified
- **Priority**: medium
- **Effort**: 3-4 hours
- **Complexity**: 5/10

### Requirements
1. For each branch in the inventory, the scan reports files containing `<<<<<<<`, `=======` and
   `>>>>>>>` as a complete block.
2. A branch with any such file is reported as broken before any alignment attempt, with the count.
3. The scan runs against the branch's tree (`git grep <pattern> <branch>`), not the working tree, so
   the result does not depend on what is checked out.
4. Documentation files that quote markers in a fenced block are reported separately from source files.
5. The result is recorded in the inventory so the checklist can show it per row.

## Implementation Guide

Extend `scripts/detect_merge_markers.py` with a `--ref <branch>` mode using `git grep`:

```bash
git grep -n -E '^(<{7}|={7}|>{7})' <branch> -- '*.py' '*.ts' '*.tsx'
```

Require all three marker kinds in one file before calling it a conflict; a lone `<<<<<<<` is a
quotation.


## Purpose

Detect merge conflict markers in feature branches to identify broken or poorly merged branches.

---

## Details

Scan feature branches for merge artifacts that indicate broken state.

### Steps

1. **Scan for conflict markers**
   ```python
   def detect_merge_artifacts(branch_name):
       result = subprocess.run(
           ["git", "log", "--oneline", f"{branch_name}..main"],
           capture_output=True, text=True
       )
       # Analyze diff for markers
   ```

2. **Compare against merge targets**

3. **Flag branches with artifacts**

4. **Update confidence scores**

---

## Test Strategy

- Create branch with markers (should detect)
- Create branch without markers (should pass)
- Test on real branches

---

## Implementation Notes

### Artifact Detection

```python
def check_merge_artifacts(branch, base_branch):
    """Check for unresolved merge markers."""
    result = subprocess.run(
        ["git", "diff", f"{base_branch}..{branch}", "--name-only"],
        capture_output=True, text=True
    )
    
    artifacts = []
    for f in result.stdout.strip().split('\n'):
        if not f:
            continue
        path = Path(f)
        if path.exists():
            with open(path) as fp:
                content = fp.read()
                if '<<<<<<<' in content or '>>>>>>>' in content:
                    artifacts.append(f)
    
    return artifacts
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 008.2**: Detect Content Mismatches
**Priority:** medium
**Effort:** 3-4 hours
**Complexity:** 5/10
**Dependencies:** None
**Created:** 2026-01-06
**Parent:** Task 008: Develop Feature Branch Identification and Categorization Tool

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
- Create branch with markers (should detect)
- Create branch without markers (should pass)
- Test on real branches

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
