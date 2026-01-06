# Task 003.3: Develop Tests for Validation Script

**Status:** pending
**Priority:** high
**Effort:** 2-3 hours
**Complexity:** 5/10
**Dependencies:** 003.2
**Created:** 2026-01-06
**Parent:** Task 003: Develop and Integrate Pre-merge Validation Scripts

---

## Purpose

Create comprehensive test suite for the validation script to ensure reliability.

---

## Details

Develop unit and integration tests covering all validation scenarios.

### Steps

1. **Create test directory structure**
   ```
   tests/
   ├── unit/
   │   ├── test_validate_exists.py
   │   ├── test_validate_json.py
   │   └── test_cli.py
   ├── integration/
   │   └── test_full_validation.py
   └── fixtures/
       ├── valid/
       ├── missing/
       ├── empty/
       └── invalid/
   ```

2. **Write unit tests**
   - Mock file system operations
   - Test each validation function
   - Test edge cases

3. **Write integration tests**
   - Create temp directory with test files
   - Run full validation script
   - Verify exit codes and output

4. **Add to CI test suite**

---

## Success Criteria

- [ ] Unit tests cover all validation functions
- [ ] Integration tests verify full workflow
- [ ] Tests pass on clean repository
- [ ] Tests fail appropriately on invalid input

---

## Test Strategy

| Scenario | Input | Expected |
|----------|-------|----------|
| All valid | All files present | Exit 0 |
| Missing file | File removed | Exit 1, error message |
| Empty file | File truncated | Exit 1, error message |
| Invalid JSON | Corrupted JSON | Exit 1, error message |

---

## Implementation Notes

### Test Fixtures Structure

```
tests/fixtures/
├── valid/
│   ├── setup/commands/__init__.py
│   └── data/valid.json
├── missing/
│   └── (file referenced but not created)
├── empty/
│   └── setup/empty.py
└── invalid/
    └── data/broken.json
```

### Unit Test Example

```python
import pytest
from scripts.validate_critical_files import validate_file

def test_missing_file():
    assert validate_file(Path("/nonexistent"), {"check_exists": True}) == ["Missing: /nonexistent"]

def test_empty_file():
    with tempfile.NamedTemporaryFile() as f:
        assert validate_file(Path(f.name), {"check_empty": True}) == [f"Empty: {f.name}"]

def test_valid_json():
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w") as f:
        f.write('{"key": "value"}')
        assert validate_file(Path(f.name), {"check_json": True}) == []
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 003.4**: Integrate Validation into CI/CD
