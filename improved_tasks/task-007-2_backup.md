# Task 008.2: Develop Logic for Detecting Content Mismatches

**Status:** pending
**Priority:** medium
**Effort:** 4-5 hours
**Complexity:** 6/10
**Dependencies:** 008.1
**Created:** 2026-01-06
**Parent:** Task 008: Develop Feature Branch Identification and Categorization Tool

---

## Purpose

Detect when branch content doesn't match its naming convention's expected target.

---

## Details

Compare branch content against potential targets to identify misaligned branches.

### Steps

1. **Calculate similarity metrics**
   - File structure comparison
   - Directory layout analysis
   - Code pattern matching

2. **Compare against expected target**
   - If named feature-scientific-X, expect high similarity to scientific
   - Flag if actually more similar to main

3. **Generate mismatch alerts**

4. **Include rationale in output**

---

## Success Criteria

- [ ] Similarity calculations working
- [ ] Mismatches detected
- [ ] Alerts generated with rationale
- [ ] False positives minimized

---

## Test Strategy

- Create misnamed branch (should flag)
- Test on correctly named branches (should pass)
- Validate similarity calculations

---

## Implementation Notes

### Content Comparison

```python
def get_file_structure(branch):
    """Get file structure for branch."""
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", branch],
        capture_output=True, text=True
    )
    return set(result.stdout.strip().split('\n'))

def calculate_similarity(branch1, branch2):
    """Calculate Jaccard similarity between branches."""
    files1 = get_file_structure(branch1)
    files2 = get_file_structure(branch2)
    
    intersection = files1 & files2
    union = files1 | files2
    
    if not union:
        return 0.0
    
    return len(intersection) / len(union)

def detect_content_mismatch(branch, expected_target):
    """Detect if branch content mismatches expected target."""
    actual_similarities = {
        "main": calculate_similarity(branch, "main"),
        "scientific": calculate_similarity(branch, "scientific"),
        "orchestration-tools": calculate_similarity(branch, "orchestration-tools"),
    }
    
    expected_similarity = actual_similarities.get(expected_target, 0)
    best_match = max(actual_similarities, key=actual_similarities.get)
    
    if best_match != expected_target:
        return {
            "mismatch": True,
            "expected": expected_target,
            "actual": best_match,
            "confidence": actual_similarities[expected_target],
            "best_match": best_match,
            "best_confidence": actual_similarities[best_match],
        }
    
    return {"mismatch": False}
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 008.3**: Integrate Backend-to-Src Migration Analysis
