# Quickstart: Orchestration Core (`dev.py`)

The `dev.py` tool is your cockpit for high-rigor development workflows. It replaces manual git plumbing and script execution with a unified, safe interface.

## 1. Setup

Ensure you are in the repository root and have the environment active:

```bash
source .venv/bin/activate
python dev.py --help
```

### IDE Integration
Generate configuration files for your preferred editor:

```bash
# For VSCode (default)
python dev.py ide-init

# For Windsurf or Antigravity
python dev.py ide-init --target windsurf
python dev.py ide-init --target antigravity
```

## 2. Key Workflows

### Analyze Conflicts (In-Memory)
Check for conflicts between your branch and main without switching branches:

```bash
python dev.py analyze main
# Output: JSON report of conflicts (or "Clean" status)
```

### Plan Rebase
Generate a topologically sorted rebase plan for your complex feature branch:

```bash
python dev.py plan-rebase
# Output: List of commits in dependency order
```

### Interactive Rebase (Execute)
Apply the plan:
```bash
python dev.py rebase --apply
```

### Sync Tools
Update your local environment scripts from the canonical source (`origin/orchestration-tools`):

```bash
python dev.py sync
# Interactive: Select which scripts to update
```

### Install Hooks
Install constitutional enforcement hooks (safe backup of existing hooks):

```bash
python dev.py install-hooks
# Renames existing pre-commit to pre-commit.bak
```

### Headless Mode (CI/Agents)
Run any command with `--json` for machine-parsable output:

```bash
python dev.py analyze main --json
```

## 3. Configuration Rules

The tool enforces rules defined in `.specify/memory/constitution.md`.
- **No Logic in Scripts**: `.sh` files are for orchestration only.
- **Library-First**: Core logic must be in `src/core`.

Run a scan manually:
```bash
python dev.py analyze --const
```