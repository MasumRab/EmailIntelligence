# UX/DX Requirements Checklist: Orchestration Core

**Purpose**: Validate that the User Experience (CLI) and Developer Experience (API/JSON) requirements are clear, comprehensive, and consistent.
**Created**: 2026-01-14
**Feature**: [004-guided-workflow](../spec.md)

## Interactive Clarity (CLI)

- [x] CHK001 Are the specific prompts for the "Interactive Rebase" (US3) defined (e.g., "Pick/Squash/Drop")? [Clarity, Spec §US3]
- [x] CHK002 Is the "Multi-select" interface for Sync (FR-016) described in enough detail to implement (e.g., "Checkboxes", "Filterable")? [Clarity, FR-016]
- [x] CHK003 Are success/failure messages defined for all key workflows? [Completeness]
- [x] CHK004 Is the usage of "Rich" panels/tables specified for complex data (e.g., Conflict Reports)? [Clarity, FR-011]
- [x] CHK005 Are default values for all interactive prompts documented? [Completeness]

## Headless Comprehensiveness (DX)

- [x] CHK006 Is the JSON schema for the "Violation Report" (FR-015) explicitly defined (fields, types)? [Completeness, FR-015]
- [x] CHK007 Are exit codes specified for all failure modes (e.g., 0=Success, 1=Error, 2=Conflict)? [Completeness, Contracts]
- [x] CHK008 Is the format of the `--answers` JSON input (FR-012) documented with a schema? [Completeness, FR-012]
- [x] CHK009 Are "Token-Saver" requirements (FR-011) specific about *what* to suppress (colors, animations, spinners)? [Clarity, FR-011]

## Consistency & Standards

- [x] CHK010 Do all subcommands follow a consistent `verb-noun` or `noun-verb` pattern (e.g., `plan-rebase` vs `analyze`)? [Consistency, Spec Requirements]
- [x] CHK011 Are command-line arguments (flags) consistent across subcommands (e.g., `--json` is available everywhere)? [Consistency, FR-009]
- [x] CHK012 Is the terminology for "Conflicts" (Ours/Theirs/Base) consistent between the CLI output and the JSON schema? [Consistency, Data Model]

## Error Handling & Guidance

- [x] CHK013 Are troubleshooting hints specified for common errors (e.g., "Git lock file exists")? [Usability]
- [x] CHK014 Is the behavior defined when `dev.py` is run outside a git repository? [Edge Case, Context]
- [x] CHK015 Are requirements defined for validating the `tasks.md` format before execution? [Robustness, FR-008]

## Notes
- Use this checklist to ensure the `dev.py` interface is "batteries included" and frustration-free.
- If a requirement is missing (e.g. "What is the exit code for a partial sync?"), add it to the spec.
