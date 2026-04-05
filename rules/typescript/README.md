# TypeScript Constitutional Rules

This directory contains ast-grep rules to enforce Constitution TypeScript/React standards:

## Rules

- `no-ts-ignore.yaml` - Prohibits @ts-ignore comments
- `no-any-type.yaml` - Prohibits `any` type usage
- `type-hints-preferred.yaml` - Encourages explicit type annotations
- `strict-null-checks.yaml` - Detects potential null/undefined issues

## Usage

```bash
# Scan with TypeScript rules
ast-grep scan --config rules/typescript/

# Scan entire project
ast-grep scan --config sgconfig.yml
```

## Severity

All rules are set to `warning` level by default.
