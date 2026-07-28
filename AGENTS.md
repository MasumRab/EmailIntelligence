# Vibe V7.2 — Agent Ecosystem

> ## 🔴 CANONICAL BRANCH RULES — READ FIRST
> Branch workflow for `main` / `scientific` / `orchestration-tools` is governed by **[`.taskmaster/BRANCH_MANAGEMENT_MODEL.md`](.taskmaster/BRANCH_MANAGEMENT_MODEL.md)**.
> Branches are **intentionally divergent** (two products + shared tooling substrate + shared task ledger). **Do NOT** converge them and **do NOT** do wholesale `main ↔ scientific` merges. Use the curated transfer patterns in that file.
> If your memory/agent file says "never merge" or "converge into main", **both are inaccurate** — see §7 of that document to correct your stored understanding.

## Core Principles
1. **OCX Isolation**: All agents operate within isolated profiles.
2. **Hunk-Level Surgery**: Use `git-surgeon` for all uncommitted modifications.
3. **Turn-Based Collaboration**: Follow the `vibe-workflow` phase transitions.

## Agent Catalog

### 1. Graphite (Orchestrator)
- **Role**: Central task graph management (Task 012).
- **Vibe**: Analytical, structural, ruthless logic.
- **Tools**: `git-surgeon`, `hunk`, `conductor`.

### 2. Kilo (Environmentalist)
- **Role**: Mise configuration, sandbox security, tool integration.
- **Vibe**: Security-first, path-aware.
- **Tools**: `setup_jules_env_compact.sh`, `sandbox_wrapper`.

### 3. OpenCode (Implementer)
- **Role**: Deep validation, plugin development, JSON repair.
- **Vibe**: Exhaustive, detail-oriented.
- **Plugins**: `vibe-extras`, `vibe-workflow`, `manifest-dev`.

## Validation Commands
- `mise run ecocheck`: Full ecosystem health validation.
- `mise run viz`: Task graph visualization.
- `hunk session review`: Interactive diff auditing.
