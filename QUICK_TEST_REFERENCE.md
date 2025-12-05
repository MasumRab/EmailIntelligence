# Quick Test Reference - Atomic Test Execution

## Run Individual Test Modules (Fastest)

### AI/Gemini Tests (~2 seconds)
```bash
python -m pytest tests/unit/ai/test_gemini_client.py -v
```

### Dependency Analysis Tests (~2 seconds)
```bash
python -m pytest tests/unit/analysis/test_dependency.py -v
```

### Strategy Reordering Tests (~1 second)
```bash
python -m pytest tests/unit/test_strategy_reordering.py -v
```

### Strategy Flow Tests (~5 seconds, currently failing)
```bash
python -m pytest tests/unit/test_strategy_flow.py -v
```

## Run Single Tests (Sub-second)

```bash
# Test Gemini initialization
python -m pytest tests/unit/ai/test_gemini_client.py::test_init_success

# Test cycle detection
python -m pytest tests/unit/analysis/test_dependency.py::test_detect_cycles_simple_cycle

# Test rebase planning
python -m pytest tests/unit/test_strategy_reordering.py::test_generate_plan_grouping
```

## Run All New Feature Tests
```bash
python -m pytest tests/unit/ai/ tests/unit/analysis/ tests/unit/test_strategy_reordering.py -v
```

## Memory-Efficient Options

### Run with minimal output
```bash
python -m pytest tests/unit/ai/ -q
```

### Run with coverage (adds ~1-2s)
```bash
python -m pytest tests/unit/ai/ --cov=src/ai --cov-report=term-missing
```

### Stop on first failure
```bash
python -m pytest tests/unit/ -x
```

## Test Status Summary

✅ **Passing (13 tests)**:
- All AI/Gemini tests (5)
- All Dependency analysis tests (6)
- All Reordering tests (2)

❌ **Failing (3 tests)**:
- Strategy flow tests (model mismatch issue)

## Quick Verification

Run this to verify the working tests:
```bash
python -m pytest tests/unit/ai/ tests/unit/analysis/ tests/unit/test_strategy_reordering.py --tb=no -q
```

Expected output: `13 passed in ~5s`
