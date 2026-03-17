# Quickstart: Orchestration Core

## Installation

```bash
pip install -r requirements.txt
python dev.py --install-completion
```

## Basic Usage (Humans)

### Analyze Conflicts
Compare two branches without touching your working tree:
```bash
python dev.py analyze feature-branch main
```

### Plan a Rebase
Generate a topologically sorted rebase plan:
```bash
python dev.py plan-rebase --branch feature-branch
```

### Install Hooks
Setup constitutional git hooks:
```bash
python dev.py install-hooks
```

## Agentic Usage (AI Agents)

All commands support the `--json` flag for machine-parseable output.

### Headless Conflict Analysis
```bash
python dev.py analyze branch-a branch-b --json
```

### Automated Sync
```bash
python dev.py sync --json --answers '{"sync_all": true}'
```

### CI Governance Check
```bash
python dev.py analyze --const --json --quiet
```

## Global Options

- `--json`: Output results in structured JSON.
- `--dry-run`: Show intended actions without executing.
- `--enable-remote`: Allow operations that affect remote branches (e.g., push).
- `--quiet`: Minimal output, ideal for piping and token-saving.
- `--answers`: Pre-answer interactive prompts via JSON string.
