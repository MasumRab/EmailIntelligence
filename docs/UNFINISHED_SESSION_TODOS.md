# Unfinished Session Todos (2026-02-20)

This file consolidates unfinished tasks captured in Amp sessions marked as unfinished or pending follow-up. It is a point-in-time snapshot for coordination.

## Source Threads

- T-019c1d02-b3ec-75b9-8fd6-cf4335f8b8c9 (Address unfinished handoffs and task migration)
- T-019c1ce0-a349-77ef-888c-4ff9ddbb79bd (Current state of confused tasks progress)
- T-019b8e85-03ea-73fe-8ca4-e4d25457523d (Recover missing task completion criteria from archived files)
- T-019c3b18-e238-739b-b8d1-d3da0e8feb75 (Finish alignment task documentation cleanup)
- T-94dd846a-04ed-4d81-95d8-97fa4b2c2cf5 (Review outstanding AMP session tasks)

## Consolidated Unfinished Tasks

### Task System Restoration (Task 75 -> Task 002)

- Restore Task 75 technical specs into task_002.1-002.9 from HANDOFF_75.* (metric formulas, schemas, clustering params, tagging system, test cases).
- Regenerate task_002.7 (VisualizationReporting), task_002.8 (TestingSuite), task_002.9 (FrameworkIntegration) using 14-section standard and HANDOFF sources.
- Deduplicate task_001 and align it to the 14-section standard.
- Fix corrupted dependencies in task_002.* where they reference 005.* instead of 002.*.

### Missing Task Files

- Restore missing task_003 and task_004 into tasks/ (choose authoritative backup source, normalize to 14-section standard).

### Alignment Task Documentation Cleanup

- Clean tasks/task_014.md, task_016.md, task_017.md, task_019.md (remove UNKNOWN headers, duplicate blocks, malformed Blocks lines).
- Resolve legacy dependencies in tasks 010/011 that still reference 075-078.
- Resolve Option C +3 mapping for tasks 016/017/019 and address overlap between 023-025 vs 026-028.
- Update OLD_TASK_NUMBERING_DEPRECATED.md to swap remaining 075.* references to 002.*.
- Refresh OPTION_C_VISUAL_MAP.md to reflect current 001-028 and note drift.

### Consolidation Phases 3-7

- Update documentation references to point to the canonical task source.
- Create deprecation notice for obsolete folders.
- Verify no broken references remain, remove accidental subdirectories.
- Communicate updated structure to the team.
- Final cleanup: delete old planning files and orphaned directories.

### 14-Section Compliance and Subtasks

- Add missing 14th section across non-compliant tasks (88 of 91 flagged).
- Create subtasks for Tasks 005-007 and 012-025 if they remain in scope.

### Archive and Data Cleanup

- Clean new_task_plan/task_files/ (remove task-001 through task-026 planning files).
- Archive or migrate task_data/ orphaned files and explain archive governance.
- Remove or archive remaining task-75.* files once migration is complete.

### Process and Governance

- Implement handoff protocol with explicit next-session start point.
- Add verification gates before declaring multi-phase work complete.
- Automate reference scanning for broken doc links.
- Assign file ownership for archival/cleanup approvals.

### MVP Pivot Tracking

- Review tasks/mvp/ content and decide whether to expand into 14-section tasks.

### Task Master Work (EmailIntelligenceAuto)

- Task 3 (Fix Email Processing Pipeline): complete subtasks 3.1-3.9.
- Task 7 (Merge Validation Framework): complete subtasks 7.1-7.9.
- Task 4: Refactor high-complexity modules.
- Task 5: Align feature branches with scientific.
- Task 6: Integrate feature-notmuch-tagging-1 with scientific.
- Task 8: Update setup subtree integration.
- Task 9: Align import-error-corrections branch.
- Task 10: Task management testing integration.
- hooks-implementation: update post-checkout/post-merge hooks to respect .git/hooks.disabled.
- hooks-validation: validate hooks disable/enable workflow.

## Pending Decisions

- Choose authoritative source priority for restoration (enhanced_improved_tasks vs backup_task75 vs handoff_task75 vs migration_backup_current).
- Choose conflict strategy: append/dedupe vs latest-source-wins.
- Decide placeholder policy for missing sections (TBD vs derive from backups).
- Decide scope of Tasks 005-028 (archive/spin-out vs active).
- Confirm dependency policy (cross-epic allowed? max dependency count?).

## Verification Checklist

- Confirm all 002.* subtasks contain ~530 total criteria after restoration.
- Confirm each subtask has a single, clean Purpose/Success/Done/Next section.
- Confirm dependencies are mapped to current IDs (no 075-078 references).
