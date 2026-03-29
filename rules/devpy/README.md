# dev.py CLI Rules

This directory contains ast-grep rules specific to the dev.py unified developer cockpit:

## Rules

- `typer-commands.yaml` - Enforces typer CLI patterns
- `pydantic-models.yaml` - Enforces pydantic model usage for data validation
- `rich-output.yaml` - Enforces rich CLI output patterns

## Usage

```bash
# Scan with dev.py rules
ast-grep scan --config rules/devpy/

# Scan entire project
ast-grep scan --config sgconfig.yml
```

## Integration

These rules ensure dev.py follows the API-First design principle from the Constitution.
