# Python Constitutional Rules

This directory contains ast-grep rules to enforce Constitution Python standards:

## Rules

- `type-hints-required.yaml` - Enforces type hints for all public functions
- `docstring-required.yaml` - Enforces Google-style docstrings for public functions
- `no-print-statements.yaml` - Prohibits print() in favor of logging
- `logging-required.yaml` - Requires logger setup in modules
- `error-handling-required.yaml` - Enforces proper error handling

## Usage

```bash
# Scan with Python rules
ast-grep scan --config rules/python/

# Scan entire project
ast-grep scan --config sgconfig.yml
```

## Severity

All rules are set to `warning` level by default. Change to `error` for CI enforcement.
