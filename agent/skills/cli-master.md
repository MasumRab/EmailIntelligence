---
name: email-intelligence-cli-master
description: Rigorous use of the EmailIntelligence modular CLI tools for repository management, task automation, and codebase analysis.
---

# EmailIntelligence CLI Master Skill

Use this skill when performing repository-level operations, task management, or codebase audits using the unified `dev.py` CLI.

## Core Principles

- **Security First**: Always use the modular CLI commands as they have integrated `SecurityValidator`.
- **Domain Focus**: Use the correct domain-prefixed command (e.g., `git-analyze` for git tasks).
- **Verification**: Always run `env-verify` if the environment state is unknown.
- **Traceability**: Reference the Implementation Plan (`conductor/tracks/*/plan.md`) when completing tasks.

## Workflows

### 1. Conflict Resolution Workflow
1. Run `git-analyze` to identify the scope of conflicts.
2. Review the output strategies.
3. Use `merge-smart` for file-level semantic merging.
4. Run `code-validate` to ensure the resolution didn't break codebase standards.

### 2. Task Automation Workflow
1. Run `task-generate` to parse PRDs into `tasks.json`.
2. Use `task-list` to prioritize the next unit of work.
3. Perform implementation.
4. Use `logic-compare` to ensure no functionality was lost if porting logic.

### 3. System Maintenance
1. Use `sys-monitor` during heavy operations.
2. Run `code-audit` to identify technical debt or security risks in new code.
3. Use `mcp-sync` to keep your own (the agent's) tools updated across IDEs.

## Command Reference

| Domain | Command | Key Usage |
| :--- | :--- | :--- |
| **Git** | `git-analyze` | Branch conflict detection. |
| **Git** | `merge-smart` | Semantic 3-way merge. |
| **Task** | `task-generate` | PRD -> tasks.json. |
| **Analysis** | `code-validate` | Quality gating. |
| **Analysis** | `logic-compare` | AST-based feature matrix. |
| **Infra** | `env-verify` | Venv and package health. |
| **Automation** | `mcp-sync` | IDE tool synchronization. |
