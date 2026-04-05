# Architectural Rules

This directory contains ast-grep rules for architectural enforcement:

## Rules

- `no-logic-in-scripts.yaml` - FR-004: Detects logic in forbidden paths (scripts/, scripts/lib/, scripts/hooks/)

## Constitution File Ownership Matrix

Per the Constitution:
- **Orchestration-only**: `scripts/`, `scripts/lib/`, `scripts/hooks/`
- **Orchestration-managed**: `setup/`, `docs/orchestration-workflow.md`, etc.
- **Branch-specific**: All application source code

## Usage

```bash
# Scan with architectural rules
ast-grep scan --config rules/architectural/

# Generate JSON violation report (FR-015)
ast-grep scan --config rules/architectural/ --format json > violation-report.json
```

## FR-015: JSON Violation Report

The output format includes:
- Rule: Rule identifier
- File: File path with violation
- Line: Line number
- Snippet: Code excerpt
