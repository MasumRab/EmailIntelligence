# Task 003.2: Develop Core Validation Script

**Status:** pending
**Priority:** high
**Effort:** 3-4 hours
**Complexity:** 5/10
**Dependencies:** 003.1
**Created:** 2026-01-06
**Parent:** Task 003: Develop and Integrate Pre-merge Validation Scripts

---

## Purpose

Implement the validation script that checks critical files for existence, integrity, and validity.

---

## Details

Create `scripts/validate_critical_files.py` that validates all critical files according to criteria from 003.1.

### Steps

1. **Create script structure**
   ```python
   #!/usr/bin/env python3
   import argparse
   import json
   import os
   from pathlib import Path
   ```

2. **Implement validation functions**
   - `check_exists(file_path)` - File exists
   - `check_not_empty(file_path)` - File has content
   - `check_json_valid(file_path)` - Valid JSON

3. **Load critical file configuration**

4. **Execute validation**

5. **Return exit codes**
   - 0: All checks pass
   - 1: One or more checks fail

6. **Log detailed errors**

---

## Success Criteria

- [ ] Script checks all critical files
- [ ] Returns correct exit codes
- [ ] Provides detailed error messages
- [ ] Handles missing files gracefully

---

## Test Strategy

- Test with all files present (should pass)
- Test with missing file (should fail, report file)
- Test with empty file (should fail)
- Test with malformed JSON (should fail)

---

## Implementation Notes

### Script Template

```python
#!/usr/bin/env python3
"""Validate critical files before merge."""

import argparse
import json
import sys
from pathlib import Path

def validate_file(path, criteria):
    """Validate a single file."""
    errors = []
    
    if criteria.get("check_exists") and not path.exists():
        errors.append(f"Missing: {path}")
    
    if criteria.get("check_empty") and path.exists():
        if path.stat().st_size == 0:
            errors.append(f"Empty: {path}")
    
    if criteria.get("check_json"):
        try:
            with open(path) as f:
                json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON: {path} - {e}")
    
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="critical_files.json")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    
    all_errors = []
    # Load config and validate...
    
    if all_errors:
        for err in all_errors:
            print(f"ERROR: {err}")
        sys.exit(1)
    
    print("All critical files validated successfully")
    sys.exit(0)

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

After completion, proceed to **Task 003.3**: Develop Tests for Validation Script
