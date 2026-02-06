# EmailIntelligence Task Workspace

Task management workspace for EmailIntelligence planning and migration work.

## Task Workspace Overview

### Canonical Task Source

- `tasks/` is the canonical source of task specifications.
- `tasks.json` is intentionally empty and used only for round-trip fidelity testing.
- Task files follow the 14-section standard in `TASK_STRUCTURE_STANDARD.md`.

### Backup and Archive Locations

- `backups/task_markdown_backups/` stores centralized task markdown backups.
- `backups/task_json/` stores JSON backup artifacts.
- `task_data/` and `archive/` contain historical sources and should not be treated as canonical.

### Current Status

- `tasks/` has been cleaned of backup files.
- Remaining work includes restoring missing tasks and normalizing all tasks to the 14-section format.
- Separate project materials live under `tasks/mvp/` and must not be merged into `tasks/`.

## References

- `ORACLE_RECOMMENDATION_TODO.md` for the migration TODO list.
- `TASK_STRUCTURE_STANDARD.md` for the required task format.
