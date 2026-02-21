# Unfinished Tasks — Consolidated & Exhaustive

**Generated:** 2026-02-21
**Source:** Thread T-019c78ff-c956-7748-8d21-053e978f4362 + fresh audit
**Scope:** All remaining cleanup, normalization, and compliance work

---

## Task A: Delete Redundant Backup/Intermediate Directories

**Priority:** HIGH — frees 1,311 files immediately
**Effort:** 15 minutes
**Risk:** LOW — all content is either in git history or canonical task files

### Directories to Remove

| Directory | Files | Reason |
|-----------|-------|--------|
| `task_data/migration_backup_20260129/` | 634 | Superseded by current task files; recoverable from git |
| `improved_tasks/` | 156 | Intermediate generation output; no unique content |
| `enhanced_improved_tasks/` | 156 | Intermediate generation output; no unique content |
| `restructured_tasks_14_section/` | 78 | Intermediate restructuring output |
| `.backups/` | 75 | Old automatic backups; superseded by `backups/` |
| `backups/` | 212 | Task markdown backups already moved here from tasks/ |

### Commands

```bash
rm -rf task_data/migration_backup_20260129
rm -rf improved_tasks
rm -rf enhanced_improved_tasks
rm -rf restructured_tasks_14_section
rm -rf .backups
rm -rf backups
```

### Verification

```bash
# Confirm removal
for d in task_data/migration_backup_20260129 improved_tasks enhanced_improved_tasks restructured_tasks_14_section .ck .backups backups; do
  [ -d "$d" ] && echo "STILL EXISTS: $d" || echo "OK: $d removed"
done
```

---

## Task B: Remove Placeholder Range Files from tasks/

**Priority:** HIGH — these are empty stubs that pollute task inventory
**Effort:** 5 minutes
**Risk:** NONE — they contain only "Untitled Task" boilerplate

### Files to Delete

| File | Content | Action |
|------|---------|--------|
| `tasks/task_008.10-19.md` | "Untitled Task" placeholder | DELETE |
| `tasks/task_009.1-7.md` | "Untitled Task" placeholder | DELETE |
| `tasks/task_009.8-30.md` | "Untitled Task" placeholder | DELETE |
| `tasks/task_010.1-10.md` | "Untitled Task" placeholder | DELETE |
| `tasks/task_010.11-30.md` | "Untitled Task" placeholder | DELETE |

### Commands

```bash
rm tasks/task_008.10-19.md
rm tasks/task_009.1-7.md
rm tasks/task_009.8-30.md
rm tasks/task_010.1-10.md
rm tasks/task_010.11-30.md
```

---

## Task C: Fix Duplicate File task_012.013.md

**Priority:** HIGH — causes numbering confusion
**Effort:** 5 minutes
**Risk:** LOW

### Problem

Two files exist with overlapping numbering:
- `task_012.013.md` — "Create Comprehensive Progress Reporting & Status Output Module" (deps: 012.6-012.11)
- `task_012.13.md` — "Develop Workflow State Persistence & Recovery Mechanisms" (deps: 012.1, 012.6)

### Action

Delete `task_012.013.md` (the zero-padded variant). The content differs — `012.13` is the canonical file per standard naming convention `task_XXX.Y.md`.

```bash
rm tasks/task_012.013.md
```

If the content from `012.013` is needed, merge its unique sections into `012.13` first.

---

## Task D: Deduplicate Section Bloat in Tasks 010, 011, 012

**Priority:** HIGH — these files have 2-3x duplicated `##` sections
**Effort:** 2-3 hours
**Risk:** MEDIUM — must preserve unique content within duplicated sections

### Problem

Current section counts (should be ~14 per the standard):
- `task_010.md`: 38 sections (many repeated 2-3x)
- `task_011.md`: 38 sections (same pattern)
- `task_012.md`: 33 sections (same pattern)

Duplicated sections include: `Overview/Purpose`, `Success Criteria`, `Prerequisites & Dependencies`, `Sub-subtasks Breakdown`, `Specification Details`, `Implementation Guide`, `Subtasks` (3x each), `Configuration Parameters` (2x), `Performance Targets` (2x), `Testing Strategy` (2x), `Common Gotchas & Solutions` (2x), `Integration Checkpoint` (2x), `Done Definition` (2x), `Next Steps` (2x).

### Action per File

1. Read the full file
2. Identify which copy of each duplicated section has the most complete content
3. Merge unique content from duplicates into the canonical section
4. Delete the duplicate sections
5. Reorder to match the 14-section standard from TASK_STRUCTURE_STANDARD.md

### Target Structure (14 sections)

```
# Task Header (with Status, Priority, Effort, Complexity, Dependencies)
## Purpose
## Success Criteria
## Prerequisites & Dependencies
## Sub-subtasks Breakdown
## Specification Details
## Implementation Guide
## Configuration Parameters
## Performance Targets
## Testing Strategy
## Common Gotchas & Solutions
## Integration Checkpoint
## Done Definition
## Next Steps
```

### Files

- `tasks/task_010.md` — 38 → 14 sections
- `tasks/task_011.md` — 38 → 14 sections
- `tasks/task_012.md` — 33 → 14 sections

---

## Task E: Fill TBD Metadata in Tasks 010, 011, 012

**Priority:** MEDIUM
**Effort:** 30 minutes
**Risk:** LOW

### Problem

These task headers have `TBD` for effort and complexity:

```
task_010.md: Effort: TBD, Complexity: TBD
task_011.md: Effort: TBD, Complexity: TBD
task_012.md: (check — likely also TBD)
```

### Action

Fill in estimates based on task scope and comparison with similar tasks:
- Task 010 (Multilevel Strategies): ~56-72h, 8/10
- Task 011 (Validation Integration): ~40-56h, 7/10
- Task 012 (Sequential Alignment Workflow): ~48-64h, 8/10

---

## Task F: Fix Legacy Dependency References in Tasks 010, 011

**Priority:** MEDIUM
**Effort:** 20 minutes
**Risk:** LOW

### Problem

- `task_010.md` dependencies: `005, 009, 012, 013, 014, 015, 016, 022, 002.1, 002.2, 002.3, 002.4`
  - References to subtask IDs `002.1-002.4` may be stale (these are clustering system subtasks, not dependencies for the alignment workflow)
- `task_011.md` dependencies: `005, 009, 010, 002.1, 002.3, 002.4`
  - Same issue with `002.x` references

### Action

1. Review whether 002.x dependencies are genuine (does Task 010 actually depend on CommitHistoryAnalyzer output?)
2. If yes, keep them. If they're artifacts of the old numbering system, remove them.
3. Cross-reference with `OPTION_C_VISUAL_MAP.md` dependency map and `docs/DEPENDENCY_OUTPUT_AUDIT.md`.

---

## Task G: Ensure 14-Section Standard Compliance Across All Tasks

**Priority:** MEDIUM
**Effort:** 4-6 hours (232 task files)
**Risk:** MEDIUM — needs scripted approach

### Problem

Many task files (especially subtasks) don't follow the 14-section standard. Some have:
- Missing sections (no `## Testing Strategy`, no `## Done Definition`)
- Extra non-standard sections
- Sections in wrong order

### Action

1. Write a compliance-checking script that:
   - Reads each `tasks/task_*.md` file
   - Checks for presence of required section headers
   - Reports missing/extra/out-of-order sections
2. Fix the most critical parent task files first (001-028)
3. Fix subtask files in priority order

### Script Output Format

```
task_010.md: FAIL — missing [Purpose, Done Definition], extra [Subtasks x3], duplicated [Success Criteria x2]
task_014.md: PASS — all 14 sections present
```

---

## Task H: Consolidate Root .md Files to docs/

**Priority:** MEDIUM
**Effort:** 1-2 hours
**Risk:** LOW — update any internal cross-references

### Problem

108 `.md` files at project root. Only ~12 should remain:
- `AGENTS.md`, `AGENT.md`, `CLAUDE.md`, `GEMINI.md`, `QWEN.md`, `IFLOW.md`
- `README.md`, `QUICK_START.md`, `PROJECT_IDENTITY.md`
- `OPTION_C_VISUAL_MAP.md`, `TASK_STRUCTURE_STANDARD.md`, `OLD_TASK_NUMBERING_DEPRECATED.md`

### Action

Move ~96 files to `docs/` (or `archive/` for truly obsolete ones):

#### Move to `docs/` (reference documentation)

```
ARCHITECTURE_AND_MD_ADJUSTMENT_GUIDE.md
BEST_PRACTICES_REVIEW_FRAMEWORK.md
BRANCH_ANALYSIS_*.md (4 files)
BRANCH_ISOLATION_GUIDELINES.md
CLI_CONSOLIDATION_*.md (2 files)
COMPREHENSIVE_CODE_REVIEW_REPORT.md
CONSOLIDATION_NEXT_STEPS.md
CONTENT_DUPLICATION_PREVENTION_GUIDELINES.md
CURRENT_DOCUMENTATION_MAP.md
CURRENT_SYSTEM_STATE_DIAGRAM.md
DEPENDENCY_CORRUPTION_FIX_PLAN.md
DOCUMENTATION_CLEANUP_COMPLETE.md
ENHANCED_ACCEPTANCE_CRITERIA_SUMMARY.md
ENHANCED_TASK_*.md (3 files)
FINAL_TASK_SPECIFICATION_IMPROVEMENTS_SUMMARY.md
FIRST_ORDER_PRD_IMPROVEMENTS_ANALYSIS.md
HANDOFF_*.md (2 files)
IMPROVEMENTS_TO_MAXIMIZE_PRD_ACCURACY.md
INITIALIZATION_SUMMARY.md
INVESTIGATION_SUMMARY_COMPLETE.md
MD_*.md (3 files)
MEMORY_API_FOR_TASKS.md
MIGRATION_STATUS_ANALYSIS.md
ORACLE_RECOMMENDATION_TODO.md
ORCHESTRATION_TOOLS_UPDATE_ANALYSIS.md
PERFECT_FIDELITY_PROCESS_DOCUMENTATION.md
PERFORMANCE_PROFILING_FRAMEWORK.md
PLACEHOLDER_BACKUP_MAPPING.md
PLANNING_TASK_UPDATES.md
PRD_GENERATION_IMPROVEMENTS_SUMMARY.md
PROJECT_STATE_CHECKLIST_RECOVERED.md
PROJECT_STATUS_SUMMARY.md
PROMPT_IMPROVEMENT_ANALYSIS.md
READ_THIS_FIRST_INVESTIGATION_INDEX.md
REORGANIZATION_PLAN_BRANCH_ANALYSIS_FORWARD.md
ROOT_DOCUMENTATION_CLEANUP_PLAN.md
ROUND_TRIP_*.md (2 files)
SCRIPTS_IN_TASK_WORKFLOW.md
SESSION_MANAGEMENT_IMPLEMENTATION.md
SLASH_COMMAND_*.md (2 files)
SUBTASK_MARKDOWN_TEMPLATE.md
SUMMARY_TASK_UPDATES.md
TASK_007_DEPRECATION_SUMMARY.md
TASK_DETAIL_IMPROVEMENTS_MAP.md
TASK_DISTANCE_MINIMIZATION_FRAMEWORK.md
TASK_EXPANSION_PLAN_BY_WEEK.md
TASK_IMPLEMENTATION_ANALYSIS_REPORT.md
TASK_REDESIGN_VERIFICATION.md
TASK_RESTRUCTURING_ANALYSIS_REPORT.md
TASK_SPECIFICATION_IMPROVEMENTS_SUMMARY.md
TASKMASTER_ANALYSIS_CONSOLIDATION_COMPLETE.md
TASKMASTER_CHANGES_REVIEW.md
TASKMASTER_COMPREHENSIVE_REVIEW_REPORT.md
TEMPLATE_MIGRATION_PATTERNS_AND_BLOCKERS.md
TEMPLATE_STRUCTURE_ANALYSIS.md
TOOLSET_DOCUMENTATION.md
UNFINISHED_TASKS_CONSOLIDATED.md (this file — keep at root until work done)
UPDATED_CONSOLIDATION_PLAN.md
```

#### Move to `archive/` (old PRD iterations, historical)

```
advanced_generated_prd_iteration_{1-5}.md
enhanced_generated_prd_iteration_{1-5}.md
generated_prd_iteration_{1-5}.md
generated_prd_multi.md
generated_prd.md
roundtrip_test_prd*.md (2 files)
test_enhanced_prd_output*.md (2 files)
task_spec_01{2-5}.md (4 files)
```

#### Delete (truly redundant)

```
ARCHIVE_INVESTIGATION_FINDINGS.md (if duplicate of SUMMARY)
ARCHIVE_INVESTIGATION_SUMMARY.md (if content in docs/)
EXECUTION_SUMMARY.txt
VERIFICATION_SUMMARY.txt
TASK_7_DELIVERY_SUMMARY.txt
TASK_7_ENHANCEMENT_SUMMARY.txt
TODO_STRUCTURE.txt
task_flow_diagram.txt
```

### Verification

After moving, update any cross-references in remaining root files that point to moved files.

---

## Task I: Deduplicate task_002.x Files

**Priority:** MEDIUM (previously high but already partially done)
**Effort:** 2-3 hours
**Risk:** MEDIUM — HANDOFF content must be preserved

### Current State

Files have been reduced from ~17,635 total lines to ~4,716 lines (73% reduction already achieved). But per UNIQUE_DELTAS_REPORT.md, the target is ~3,530 lines.

| File | Current Lines | Target | Remaining Reduction |
|------|--------------|--------|-------------------|
| task_002.1.md | 323 | ~350 | ✅ Already at target |
| task_002.2.md | 351 | ~380 | ✅ Already at target |
| task_002.3.md | 413 | ~400 | ~3% to trim |
| task_002.4.md | 570 | ~350 | ~39% to trim |
| task_002.5.md | 610 | ~400 | ~34% to trim |
| task_002.6.md | 679 | ~350 | ~48% to trim |
| task_002.7.md | 520 | ~350 | ~33% to trim |
| task_002.8.md | 548 | ~450 | ~18% to trim |
| task_002.9.md | 702 | ~500 | ~29% to trim |

### Action

For files 002.3-002.9, scan for:
1. Remaining `IMPORTED_FROM` block duplicates
2. Repeated template boilerplate (`## Purpose` / `## Details` / `## Guidance & Standards` blocks appearing multiple times)
3. Duplicate requirements blocks
4. Empty placeholder sections

---

## Task J: Integrate Task 75 Technical Specs into New Structure

**Priority:** LOW (deferred — not blocking MVP)
**Effort:** 4-6 hours
**Risk:** LOW

### Problem

Technical specifications (formulas, schemas, algorithms) from the original Task 75 HANDOFF documents should be verified as present in the corresponding task_002.x files.

### Action

1. Compare `backup_task75/HANDOFF_002.X_*.md` with current `tasks/task_002.X.md` files
2. Verify all formulas, class signatures, metric definitions, and config schemas are preserved
3. If anything is missing, copy it into the appropriate section of the current file

### Note

Per UNIQUE_DELTAS_REPORT.md, all unique content should already be in the canonical HANDOFF sources. This task is a verification pass, not a creation task.

---

## Task K: Implement Round-Trip Testing (MD ↔ tasks.json)

**Priority:** LOW (tooling improvement)
**Effort:** 3-4 hours
**Risk:** LOW

### Problem

No automated verification that `tasks/*.md` → `tasks.json` → `tasks/*.md` round-trips preserve all content.

### Action

1. Create `scripts/roundtrip_test.py` that:
   - Reads all task markdown files
   - Runs `python taskmaster_cli.py parse-prd --input tasks/` to generate tasks.json
   - Runs `task-master generate` to regenerate markdown from tasks.json
   - Compares original and regenerated markdown for content loss
2. Focus on: titles, dependencies, status, priority, effort, complexity
3. Report any fields that are lost in the round-trip (known issue: TaskEntity.toJSON() strips custom fields per GitHub Issue #1555)

---

## Task L: Git Housekeeping

**Priority:** LOW (do after Tasks A-C to maximize effect)
**Effort:** 10 minutes
**Risk:** NONE

### Commands

```bash
git gc --aggressive --prune=now
git remote prune origin
git repack -a -d --depth=250 --window=250
```

### Expected Impact

Reduces `.git/objects/` from ~3,500 loose objects to a compact pack file.

---

## Task M: Delete Orphaned Python/Shell Scripts at Root

**Priority:** LOW
**Effort:** 10 minutes
**Risk:** LOW — verify none are called by active workflows

### Files to Review

```
cleanup_and_record.py
compare_prd_approaches.py
demo_session_management.py
emailintelligence_cli.py
enhanced_prd_prompts.py
execute_phases_2_4.py
integrate_remaining_tasks.py
migrate_tasks.py
replace_placeholders.py
test_refactoring_modes.py
run_advanced_task_analysis.sh
run_complexity_analysis.sh
```

### Action

1. Check if any of these are referenced in `scripts/`, `AGENTS.md`, or task files
2. If not referenced → move to `archive/scripts/` or delete
3. Keep `taskmaster_cli.py` — it's the canonical CLI

---

## Execution Order

| Phase | Tasks | Time | Impact |
|-------|-------|------|--------|
| **Phase 1: Quick Wins** | A, B, C | 25 min | -1,316 files, fix naming |
| **Phase 2: Section Dedup** | D, E | 3 hours | Fix 3 worst task files |
| **Phase 3: Standards** | F, G | 5 hours | Dependency + compliance |
| **Phase 4: Consolidation** | H, I, M | 4 hours | Root cleanup, 002.x trim |
| **Phase 5: Tooling** | K, L | 4 hours | Round-trip tests, git gc |
| **Phase 6: Verification** | J | 5 hours | Tech spec audit |

**Total estimated effort: ~21 hours**

---

## Post-Completion Verification Checklist

- [ ] `find . -not -path './.git/*' -type f | wc -l` shows < 800 files
- [ ] `ls *.md | wc -l` shows ≤ 12 root .md files
- [ ] No task file has > 14 `## ` sections
- [ ] No task file has TBD in header metadata
- [ ] No placeholder "Untitled Task" files exist in tasks/
- [ ] No `task_012.013.md` duplicate exists
- [ ] `scripts/update_option_c_visual_map.py` runs cleanly
- [ ] `python taskmaster_cli.py parse-prd --input tasks/` succeeds
- [ ] Git working tree is clean and pushed
