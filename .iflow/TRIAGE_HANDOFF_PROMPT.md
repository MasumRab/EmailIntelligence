## Comprehensive .taskmaster Triage, Large File Decomposition & Documentation Cleanup

You are working in `/home/masum/github/EmailIntelligence` on branch `004-guided-workflow`. The `.taskmaster` directory is a Git worktree on the `taskmaster` branch. Commit changes via: `cd .taskmaster && git add -A && git commit && git push`

### MANDATORY FIRST READ
- `.taskmaster/.iflow/predictions/report-20250106.md` — 26 predicted issues (6 CRITICAL, 12 HIGH, 8 MEDIUM)
- `.taskmaster/.iflow/understand/architecture.md` — architecture analysis (28,003 LOC, 88 scripts)
- `.taskmaster/.iflow/understand/enhanced_architecture.md` — enhanced analysis (997 files, 63MB)
- `.taskmaster/.iflow/TODO_ORGANIZATION_REPORT.md` — 948 marker matches, only 2 actionable
- `.taskmaster/docs/BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md` — D1-D10 invariants

### CRITICAL CONTEXT: The tasks/ Migration Was Reversed

The iFlow predictions report (Jan 6, 2026) describes a `tasks/` → `new_task_plan/` migration as in-progress. **This migration was abandoned.** Here is the actual timeline:

- `71afb4b6`: Phase 2 copied 9 tasks to `new_task_plan/task_files/`
- `f686015c`: Phase 4-5 deprecated `tasks/`, added `DEPRECATION_NOTICE.md`
- `67295077`: **REVERSED** — deleted `new_task_plan/task_files/`, restructured tasks back, then later commits moved everything back to `tasks/`
- **Current state**: `new_task_plan/` does NOT exist on disk. `tasks/` has 230 files and `tasks/tasks.json`. `tasks/` IS the active source of truth.

**Therefore**: Any prediction referencing `new_task_plan/` as the target or `tasks/` as deprecated is STALE. Do NOT attempt to resume the migration. Instead, verify that all scripts correctly reference `tasks/` and `tasks/tasks.json`.

---

### PHASE 1: Validate Script References (predictions report items)

**1.1 — Verify all task_scripts/ and scripts/ reference tasks/ correctly**
- The predictions report flagged 7+ scripts referencing `../tasks/tasks.json` — since tasks/ still exists, these may be fine
- Audit every `*.py` in `task_scripts/` and `scripts/` for path references
- Check: do any still reference `new_task_plan/`? (would be broken)
- Check: do `../` relative paths resolve correctly from their execution context?
- List findings as: `file:line | path_referenced | status (valid/broken/stale)`

**1.2 — taskmaster_common.py import chain**
- Located at `task_scripts/taskmaster_common.py` (390 lines)
- 7 scripts import from it: `compare_task_files.py`, `list_tasks.py`, `next_task.py`, `search_tasks.py`, `show_task.py`, and others
- Verify every importer resolves the import correctly from its execution directory
- Check for `sys.path` hacks or `../` path manipulation in each importer
- List findings as: `file | import_method | resolves (yes/no)`

**1.3 — JSON file references**
- `tasks/tasks.json` is the canonical location (3.75MB)
- Search all Python files for references to `tasks.json`, `non_alignment_tasks.json`, or any other JSON data files
- Confirm each reference points to the correct current location
- Flag any referencing `new_task_plan/` (broken) or using hardcoded absolute paths

**1.4 — Hardcoded `../` path audit (SE-1, impact 82/100)**
- Run: `grep -rn '\.\.\/' task_scripts/ scripts/ --include="*.py"`
- For each hit, determine if the relative path resolves correctly given the file's location
- Flag any path traversal that exits the `.taskmaster/` boundary (security risk)
- Create a manifest: `file:line | relative_path | resolves_to | valid (yes/no/security_risk)`

---

### PHASE 2: Decompose Large Python Files

These 4 files exceed 1000 lines and cannot be properly analyzed as monoliths. Break each into logical modules.

**2.1 — `scripts/enhance_branch_analysis_tasks_for_prd_accuracy.py` (2,106 lines)**
- Read the file and identify logical sections (classes, major functions, data blocks)
- Create an analysis file: `.taskmaster/.iflow/understand/large_file_analysis/enhance_branch_analysis.md`
- Document: purpose, all classes/functions with line ranges, dependencies, proposed split plan
- If the file has clearly separable concerns (e.g., data loading, analysis, output generation), split into modules under `scripts/branch_analysis/` with an `__init__.py`
- If the file is a one-shot script unlikely to be reused, document its structure but do NOT split — just add a table of contents comment at the top

**2.2 — `emailintelligence_cli.py` (1,745 lines)**
- This is the main CLI entry point — likely has many subcommands
- Read and document all command handlers, their line ranges, and dependencies
- Create analysis: `.taskmaster/.iflow/understand/large_file_analysis/emailintelligence_cli.md`
- Proposed split: extract each command group into `src/cli/` modules, keep `emailintelligence_cli.py` as thin dispatcher
- Do NOT execute the split — only document the plan with exact line ranges and proposed target files

**2.3 — `task_scripts/merge_task_manager.py` (1,495 lines)**
- Read and identify: classes, merge strategies, validation logic, I/O handling
- Create analysis: `.taskmaster/.iflow/understand/large_file_analysis/merge_task_manager.md`
- Document: what merges what, which functions are entry points vs helpers, nesting depth (reported as 6 levels max)
- Proposed split plan: separate merge logic, validation, and CLI interface

**2.4 — `archive/task_data_historical/branch_clustering_implementation.py` (1,459 lines)**
- This is in archive/ — it's historical but still imported by `test_refactoring_modes.py`
- Read and document the 5 analyzer classes: `CommitHistoryAnalyzer`, `CodebaseStructureAnalyzer`, `DiffDistanceCalculator`, `BranchClusterer`, `IntegrationTargetAssigner`
- Create analysis: `.taskmaster/.iflow/understand/large_file_analysis/branch_clustering.md`
- For each class: document purpose, methods, line ranges, external dependencies
- Check if `test_refactoring_modes.py` import still works: `python -c "from archive.task_data_historical.branch_clustering_implementation import *" 2>&1`
- Proposed split: one file per analyzer class under `src/analysis/`

**For each analysis file, use this template:**
```markdown
# Large File Analysis: {filename}
**Lines:** {count}
**Location:** {path}
**Last modified:** {git log date}

## Purpose
{1-2 sentence description}

## Structure
| Section | Lines | Type | Description |
|---------|-------|------|-------------|
| {name} | {start}-{end} | class/function/data | {description} |

## Dependencies
- Imports: {list}
- Imported by: {list}
- File I/O: {list of paths read/written}

## Proposed Decomposition
| Current Section | Target File | Rationale |
|----------------|-------------|-----------|
| {section} | {proposed_path} | {why} |

## Risks
- {risk of splitting}
- {backward compatibility concerns}
```

---

### PHASE 3: Documentation Audit & Cleanup

**3.1 — Stale migration references**
- The predictions report, `DEPRECATION_NOTICE.md`, `PROJECT_STATUS_SUMMARY.md`, `CURRENT_DOCUMENTATION_MAP.md`, and any docs created during the aborted migration still reference `new_task_plan/` as the target
- Search: `grep -ri "new_task_plan" .taskmaster/ --include="*.md" -l`
- For each file found: either update to reference `tasks/` or add a note that the migration was reversed
- Delete `tasks/DEPRECATION_NOTICE.md` if it still exists (tasks/ is NOT deprecated)

**3.2 — Submodule/worktree contradictions (D1-D2 violations)**
- Search: `grep -ri "submodule" .taskmaster/ --include="*.md" -l` (exclude archive/)
- Search: `grep -ri "gitmodules" .taskmaster/ --include="*.md" -l` (exclude archive/)
- Search: `grep -ri "must not.*gitignore\|should not.*gitignore" .taskmaster/ --include="*.md" -l`
- For each non-archive hit: fix to say worktree, not submodule; fix to say `.taskmaster/` IS in `.gitignore`
- Cross-reference against D1-D10 in the non-regression guide

**3.3 — Content duplication detection**
- Find markdown files with suspiciously similar names (e.g., `ARCHIVE_MANIFEST.md` in multiple locations, `README.md` duplicates)
- Check `archive/` for files that are exact copies of root-level files
- For each pair: determine which is canonical, flag the other for deletion or add a pointer
- Run: `find .taskmaster/ -name "*.md" -not -path "*/.git/*" | xargs md5sum | sort | uniq -w32 -d` to find exact duplicates

**3.4 — File structure issues**
- Files over 500 lines: `find .taskmaster/ -name "*.md" -not -path "*/.git/*" -exec wc -l {} + | awk '$1 > 500' | sort -rn`
- Files under 10 lines: `find .taskmaster/ -name "*.md" -not -path "*/.git/*" -exec wc -l {} + | awk '$1 < 10 && $1 > 0' | sort -n`
- For oversized files: recommend splitting or flag sections that belong elsewhere
- For undersized files: recommend merging into parent doc or deletion
- Check for broken internal markdown links: `grep -rn '\[.*\](.*\.md)' .taskmaster/ --include="*.md"` then verify each target exists

**3.5 — Stale phase references**
- The consolidation was a 7-phase plan. Phases 1-5 were partially executed, then reversed at commit `67295077`
- Find all docs referencing "Phase 6" or "Phase 7" as upcoming work — these are stale
- Find docs referencing "consolidation status: 2/7" or similar — update to reflect current reality
- Find `PHASE_1_STATUS_SUMMARY.md`, `CONSOLIDATION_COMPLETION_REPORT.md`, or similar — archive or update

**3.6 — AGENTS.md accuracy**
- Verify `.taskmaster/AGENTS.md` directory structure section matches actual current structure
- Verify script lists in `scripts/README.md` and `task_scripts/README.md` match actual files
- Verify any index files (`ORCHESTRATION_DOCS_INDEX.md`, `CURRENT_DOCUMENTATION_MAP.md`) have correct links

---

### PHASE 4: TODO & Tech Debt Verification

**4.1 — Verify semantic_merger.py fix**
- Check `src/resolution/semantic_merger.py` around line 219
- Confirm the `ast.literal_eval` list/dict merge implementation is still in place (fixed Jan 6, 2026)
- If missing or reverted, flag as CRITICAL regression

**4.2 — Clean deprecated TODO examples**
- In `OLD_TASK_NUMBERING_DEPRECATED.md` lines 153-161: mark the 4 TODO examples clearly as `# DEPRECATED EXAMPLE — not actionable`

**4.3 — Test coverage gap documentation**
- List all files in `.taskmaster/tests/`
- Document what exists and what's missing
- Do NOT write new tests — just document

---

### PHASE 5: Predictions Report Update

**5.1 — Update the predictions report**
Create `.taskmaster/.iflow/predictions/report-20250106-STATUS-UPDATE.md` with:
- For each of the 26 predictions: current status (validated/false_positive/stale/remediated/still_at_risk)
- Mark all `new_task_plan/` predictions as STALE with explanation
- Mark path-related predictions against current `tasks/` structure
- Note which large files were analyzed in Phase 2
- Recalculate overall risk score based on current state

---

### PHASE 6: Create Triage Summary

Create `.taskmaster/.iflow/TRIAGE_REPORT.md` containing:

1. **Migration status clarification** — tasks/ is canonical, new_task_plan/ migration was reversed, with commit evidence
2. **Broken references manifest** — every broken path/import found with file:line and status
3. **Documentation violations** — every doc contradicting D1-D10 with corrections applied
4. **Duplication map** — file pairs with duplicated content and resolution
5. **Structure issues** — oversized, undersized, misplaced sections, broken links
6. **Large file decomposition plans** — summary of Phase 2 analysis with proposed splits
7. **Stale content** — files referencing abandoned migration or outdated phases
8. **Tech debt backlog** — items documented but not fixed (with severity from predictions report)
9. **Actions taken** — every file modified with 1-line description

### COMMIT
```bash
cd .taskmaster
git add -A
git commit -m "triage: comprehensive .iflow issue remediation, large file analysis, doc cleanup

- Validated script references against current tasks/ structure
- Analyzed 4 large Python files (2106/1745/1495/1459 lines) with decomposition plans
- Fixed stale new_task_plan/ references (migration was reversed at 67295077)
- Fixed submodule→worktree doc contradictions per D1-D10
- Identified content duplications and structural issues
- Updated predictions report with current status
- Created comprehensive triage report"
git push
```

### RULES
- Fix documentation issues directly (stale references, contradictions, broken links)
- Do NOT fix code architecture issues — only document them in analysis files
- Do NOT move or refactor Python files — only analyze and create decomposition plans
- Do NOT resume the tasks/ → new_task_plan/ migration — it was intentionally reversed
- Do NOT modify files outside `.taskmaster/`
- If `.taskmaster/.gitignore` blocks `*_GUIDE.md` or `*_REPORT.md`, use `git add -f`
- Work phases sequentially: complete each fully before starting the next
