# Task 005.1: Develop Merge Artifact and Deleted Module Detection

**Status:** pending
**Priority:** high
**Effort:** 3-4 hours
**Complexity:** 5/10
**Dependencies:** None
**Created:** 2026-01-06
**Parent:** Task 005: Develop Automated Error Detection Scripts for Merges

---

## Purpose

Create scripts to detect uncleaned merge markers and accidentally deleted modules.

---

## Details

Implement detection for common merge artifacts and track deleted files.

### Steps

1. **Detect merge markers**
   ```python
   def detect_merge_markers(changed_files):
       markers = []
       for f in changed_files:
           result = subprocess.run(
               ["grep", "-n", r"^\(<<<<<<<\|=======\|>>>>>>>\)", f],
               capture_output=True,
               text=True
           )
           if result.returncode == 0:
               markers.append((f, result.stdout))
       return markers
   ```

2. **Track deleted files**
   ```python
   def detect_deleted_files():
       result = subprocess.run(
           ["git", "diff", "--name-only", "--diff-filter=D"],
           capture_output=True,
           text=True
       )
       return result.stdout.strip().split('\n')
   ```

3. **Check if deleted modules were imported**

4. **Generate report**

---

## Success Criteria

- [ ] Merge markers detected in changed files
- [ ] Deleted files identified
- [ ] Module dependency check working
- [ ] Report generated

---

## Test Strategy

- Create test file with merge markers (should detect)
- Delete a file (should detect)
- Delete imported module (should flag)

---

## Implementation Notes

### Detection Script Structure

```python
#!/usr/bin/env python3
"""Detect merge artifacts and deleted modules."""

import subprocess
import sys
from pathlib import Path

def get_changed_files():
    """Get list of changed files."""
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        capture_output=True,
        text=True
    )
    return [f for f in result.stdout.strip().split('\n') if f]

def detect_merge_markers(files):
    """Find merge conflict markers."""
    artifacts = []
    for f in files:
        path = Path(f)
        if not path.exists():
            continue
        with open(path) as fp:
            for i, line in enumerate(fp, 1):
                if line.startswith(('<<<<<<<', '=======', '>>>>>>>')):
                    artifacts.append(f"{f}:{i}: {line.strip()}")
    return artifacts

def detect_deleted_files():
    """Find deleted files."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=D"],
        capture_output=True,
        text=True
    )
    return [f for f in result.stdout.strip().split('\n') if f]

def main():
    files = get_changed_files()
    artifacts = detect_merge_markers(files)
    deleted = detect_deleted_files()
    
    if artifacts:
        print("MERGE ARTIFACTS FOUND:")
        for a in artifacts:
            print(f"  {a}")
    
    if deleted:
        print("\nDELETED FILES:")
        for d in deleted:
            print(f"  {d}")
    
    sys.exit(1 if (artifacts or deleted) else 0)

if __name__ == "__main__":
    main()
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 005.2**: Implement Garbled Text Detection
