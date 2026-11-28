# Taskmaster Extraction — S10

**Repository**: MasumRab/EmailIntelligence  
**Branch**: extract/taskmaster (from origin/main)  
**Date**: 2026-11-11

---

## Source: taskmaster branch (633b774ab)

### Inventory

| Category | Count | Notes |
|----------|-------|-------|
| `tasks/` markdown files | 212 | Task specifications |
| `taskmaster_cli.py` | 1 | Official CLI (11829 bytes) |
| `.taskmaster/` | empty | Charter not in this tree |
| `scripts/taskmaster_runner.py` | 1 | Runner utility (from taskmaster branch) |
| `task_scripts/taskmaster_common.py` | 1 | Common utilities (from taskmaster branch) |

### Charter Location

The `.taskmaster` charter lives **only on the taskmaster branch** as a submodule pointing at the repo's own `taskmaster` branch. It is invisible from `main` until `git submodule update --init`.

---

## Extraction Plan

### Create: `extract/taskmaster` from `origin/main`

**Copy from taskmaster branch:**
1. `tasks/` → `tasks/` (212 files, preserving structure)
2. `taskmaster_cli.py` → `taskmaster_cli.py` (CLI entry point)
3. `scripts/taskmaster_runner.py` → `scripts/taskmaster_runner.py` (runner)
4. `task_scripts/taskmaster_common.py` → `task_scripts/taskmaster_common.py` (utilities)

**Do NOT copy:**
- `.agent_memory`, `.beads`, `.gemini`, `.iflow`, `.qwen` — IDE state
- `archive/`, `complexity_reports/`, `reports/` — historical
- `state.json` — runtime state
- `templates/` — template files
- `guidance/` — guidance files
- `emailintelligence_cli.py` — separate CLI
- `BACKLOG_MANAGEMENT_MODEL.md`, `BRANCH_MANAGEMENT_MODEL.md` — governance (stay in taskmaster branch)

### Make Runnable

**Proof command**: 
```bash
python3 taskmaster_cli.py list --tasks-dir tasks
```
Expected: Lists 212 parsed tasks from markdown files.

**Alternative proof** (if tasks.json needed):
```bash
python3 taskmaster_cli.py parse-prd --tasks-dir tasks --output tasks/tasks.json
python3 taskmaster_cli.py list --tasks-dir tasks
```

---

## Excluded Files (with reasons)

| Pattern | Reason |
|---------|--------|
| `archive/**` | Historical/archive only |
| `complexity_reports/**` | Generated reports |
| `reports/**` | Generated reports |
| `state.json` | Runtime state, not source |
| `templates/**` | Templates, not tasks |
| `guidance/**` | Guidance docs |
| `.agent_memory`, `.beads`, `.gemini`, `.iflow`, `.qwen` | IDE/tooling state |
| `emailintelligence_cli.py` | Separate CLI, not taskmaster |
| `BACKLOG_MANAGEMENT_MODEL.md` | Governance for taskmaster branch |
| `BRANCH_MANAGEMENT_MODEL.md` | Governance for taskmaster branch |
| `*.md` in root (except AGENTS.md, README.md) | Branch-specific docs |

---

## Deliverables

1. **Branch**: `extract/taskmaster` (pushed)
2. **PR**: Draft PR with `--base main`
3. **Report**: File count, proof command output, SHA
