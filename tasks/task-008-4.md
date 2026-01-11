# Task 009.4: Integrate Existing Unit and Integration Tests

**Status:** pending
**Priority:** high
**Effort:** 3-4 hours
**Complexity:** 5/10
**Dependencies:** 009.1
**Created:** 2026-01-06
**Parent:** Task 009: Create Comprehensive Merge Validation Framework

---

## Purpose

Configure CI to execute full test suite and block on failures.

---

## Details

Add pytest execution to GitHub Actions workflow.

### Implementation

```yaml
# In .github/workflows/merge-validation.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          pytest src/ --cov --cov-report=xml --tb=short
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
```

### Test Configuration

- `pytest.ini` or `pyproject.toml` configuration
- Coverage threshold: 90%
- Fail-fast: enabled

---

## Success Criteria

- [ ] Tests run in CI
- [ ] Coverage reported
- [ ] Failures block merge
- [ ] Coverage threshold enforced

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 009.5**: Develop E2E Smoke Tests
