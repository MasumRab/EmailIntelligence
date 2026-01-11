# Task 008.1: Implement Destructive Merge Artifact Detection

**Status:** pending
**Priority:** medium
**Effort:** 3-4 hours
**Complexity:** 5/10
**Dependencies:** None
**Created:** 2026-01-06
**Parent:** Task 008: Develop Feature Branch Identification and Categorization Tool

---

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

## Success Criteria

- [ ] Merge markers detected
- [ ] Branches flagged appropriately
- [ ] Confidence scores reduced
- [ ] Output includes artifact flags

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
