# Rule Tests Structure

This directory contains TDD tests for ast-grep rules following Constitution II (TDD mandatory).

## Structure

```
rule-tests/
├── python/
│   ├── test_type_hints_required.py
│   ├── test_docstring_required.py
│   ├── test_no_print_statements.py
│   ├── test_logging_required.py
│   └── test_error_handling_required.py
├── typescript/
│   ├── test_no_ts_ignore.py
│   ├── test_no_any_type.py
│   ├── test_type_hints_preferred.py
│   └── test_strict_null_checks.py
└── architectural/
    └── test_no_logic_in_scripts.py
```

## Running Tests

```bash
# Run all rule tests
pytest rule-tests/ -v

# Run specific category
pytest rule-tests/python/ -v
pytest rule-tests/typescript/ -v
pytest rule-tests/architectural/ -v
```

## Test Pattern

Each test should:
1. Create a temporary file with violation code
2. Run ast-grep scan
3. Assert violations are detected
4. Clean up temporary file
