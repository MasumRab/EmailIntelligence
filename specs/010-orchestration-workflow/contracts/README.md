# Orchestration Workflow Contracts

## File Ownership Contract

This document defines which files belong to the orchestration-tools branch vs. application branches.

### Orchestration-Only Files (NEVER merge to app branches)

- `scripts/` — All orchestration scripts and utilities
- `scripts/lib/` — Shared shell libraries
- `scripts/hooks/` — Git hook source files

### Application-Only Files (NEVER in orchestration-tools)

- `src/` — Application source code
- `backend/` — Backend implementation
- `client/` — Frontend code
- `specs/` — Feature specifications
- `tests/` — Test suites
- `docs/` — Application documentation (except orchestration docs)

### Sync Protocol

Files in the sync scope are pushed from orchestration-tools → app branches via post-push hooks on orchestration-tools.

## Hook Version Contract

All hooks MUST include a version header:
```bash
# @hook-version: 1.2.0
```

The post-checkout hook verifies installed versions match canonical versions from orchestration-tools.
