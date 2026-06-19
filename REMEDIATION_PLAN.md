# Task Repository Remediation Plan

**Created:** 2026-06-19
**Author:** Letta Code agent (agent-70cd3b53)
**Status:** Phase A complete; Phase B–D pending
**Location:** `.taskmaster/tasks/` (25 canonical tasks + 180 subtask files)
**Source docs:** `TASK_ANALYSIS_AND_GOTCHAS.md`, `DOCUMENTATION_TASK_MAP.md`

---

## Overview

The `.taskmaster/tasks/` directory contains 25 canonical task files and 180 subtask files for the Branch Alignment Tooling project. Multiple issues were identified through systematic audit (June 2026): off-by-one cross-references, content contamination from prior numbering eras, inflated effort estimates, overlapping task scopes, and disconnected dependency graphs.

Remediation is organized into four phases, ordered by risk and dependency:

| Phase | Focus | Risk | Depends on | Status |
|-------|-------|------|------------|--------|
| A | Mechanical fixes (no decisions) | Low | None | ✅ Complete |
| B | Decisions (user input required) | Medium | Phase A | ⏳ Pending |
| C | Structural reconnection | High | Phase B | ⏳ Pending |
| D | Cleanup & standards | Low | Phase C | ⏳ Pending |

**Guiding principle:** *Subtask-intent inversion* — subtasks are ground truth. Parent tasks should be fixed to match subtasks, not the reverse. (Exceptions: Task 005 where parent has real intent, Task 015 where subtasks are from a different task entirely.)

---

## Phase A: Mechanical Fixes ✅ COMPLETE

All items completed. No decisions were required; no task intent or instructions were changed — only reference hygiene.

| # | Item | What was done | Commit |
|---|------|---------------|--------|
| A1 | Task 008 numbering (9.x→8.x) | 56 refs renumbered across 10 files; zero-padded variants normalized (9.013→8.14, 9.016→8.18, 9.017→8.17, 9.003→8.19); duplicate subtask numbers fixed in parent | `32e4334e` |
| A2 | Task 009 cross-refs (off-by-one) | 57 replacements in parent + 6 in subtask files: 012→013 (backup), 013→014 (conflict), 014→015 (validation), 015→016 (rollback). Preserved correct refs at lines 63/70. | `17ec9e2e` |
| A3 | Task 012 label drift | "Task 008: Documentation Generation" → "Comprehensive Merge Validation Framework" | `32e4334e` |
| A4 | Task 015 phantom 27.x refs | 34 replacements: 27.1-27.10→015.1-015.10, 27.26→015.14, 27.28→015.13, Task 28→Task 022. Removed deleted task refs 26/27 from 015.1 deps. Fixed 015.013→015.14. | `17ec9e2e` |
| A5 | Dangling block-refs (024/025) | 024: removed "Blocks Task 026". 025: removed "Blocks Task 026/027" + replaced all body refs with "post-MVP future work" | `32e4334e` |
| A6 | Deflate Task 002 effort | 212-288hr→40-50hr, complexity 9/10→6/10 (3 locations) | `32e4334e` |
| A7 | Deflate Tasks 019-025 effort | 12-48hr→2-3hr (022: 3-4hr), complexity 5-9/10→3/10 (022: 4/10) | `32e4334e` |
| A8 | ~~task_021 intra-file corruption~~ | Already fixed in dedup commit `a25bfdbe` (2026-02-26) | N/A |
| A9 | Task 008 triple-hash headings | `### ###` → `###` (19 occurrences) | `16126ca4` |
| A10 | Task 010 dangling Task 027 ref | "Task 027" → "post-MVP future work" | `16126ca4` |
| A11 | Task 025.5 dangling Task 026 refs | "Task 026" → "post-MVP future work" (2 refs) | `16126ca4` |
| A12 | Task 024 Gen-2 naming format | `"task-023"` → `"task_023"` (2 files) | `16126ca4` |
| A13 | DOCUMENTATION_TASK_MAP.md restore | Restored from 12-line gutted version to 436-line full version | `16126ca4` |

**Submodule pointer:** `53adb534` on `origin/main`

---

## Phase B: Decisions Required ⏳ PENDING

Each item requires user decision before proceeding. The agent cannot resolve these mechanically — they involve judgment calls about task identity and scope boundaries.

### B1: Decide Task 015 Fate

**Current state:**
- Parent title: "Validation and Verification"
- Subtasks (015.1–015.16): Describe orchestration workflow — branch selection UI, queue management, sequential execution, integration of other tasks
- Subtask 015.2 (line 307): Describes post-rebase validation — matches parent title
- Subtasks were pasted from prior Task 27 (Gen-2 orchestration task)

**The problem:** The file contains TWO incompatible task descriptions:
1. Orchestration workflow (015.1–015.16, from old Task 27)
2. Validation/verification (015.2 at line 307, matches parent title)

**Options:**

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **B1a: Rewrite parent to match subtasks** | Rename 015 to "Sequential Branch Alignment Orchestration" | Follows subtask-intent inversion principle; subtasks are richer | Creates overlap with Task 012 (also orchestration); need to differentiate 012 vs 015 |
| **B1b: Rewrite subtasks to match parent** | Replace orchestration subtasks with validation content | Preserves task identity; no overlap with 012 | Discards detailed orchestration spec; need to write new validation subtasks from scratch |
| **B1c: Split into two tasks** | Extract orchestration subtasks to a new task or merge into 012; keep 015 as validation | Clean separation; both purposes preserved | Increases task count; need to decide where orchestration content goes |
| **B1d: Merge orchestration into Task 012** | Move 015.1-015.16 subtasks into 012 as additional subtasks; repurpose 015 as pure validation | Eliminates duplication; 012 is already the orchestrator | 012 already has its own subtasks; merging may create confusion |

**Recommendation:** B1c or B1d — the orchestration content belongs in/alongside Task 012, and Task 015 should be repurposed as validation (matching the pre-merge disposition where 015=validation is a real pre-merge concern).

**Impact if chosen:**
- B1a: Task 012 and 015 need clear boundary definition (which orchestration aspects belong where)
- B1b: Significant content loss; new validation subtasks needed
- B1c: New task number needed; or merge into 012
- B1d: Task 012 subtask count increases; 015 needs new validation content

---

### B2: Reassign Task 007 Subtasks

**Current state:**
- Parent title: "Develop Feature Branch Identification and Categorization Tool"
- Subtask 007.1: Destructive merge artifact detection
- Subtask 007.2: Content mismatch detection in similarly named branches
- Subtask 007.3: Backend-to-src migration status analysis

**The problem:** Subtasks describe error detection and migration analysis, NOT branch identification. They belong to Task 005 (error detection) or a migration-specific task.

**Options:**

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **B2a: Move 007.1/007.2 to Task 005** | Error detection subtasks belong with error detection task | Logical grouping; 005's subtasks are generic boilerplate that needs replacement anyway | 005 already has subtasks; need to integrate |
| **B2b: Move 007.3 to Task 022** | Migration analysis belongs with architectural migration | 022 already has migration step; natural fit | 022 is partially post-MVP |
| **B2c: Keep in 007, update parent title** | Rename 007 to match what subtasks actually do | Minimal disruption | Parent title "Feature Branch Identification" is accurate for the task's role in the pipeline; subtasks are the anomaly |
| **B2d: Split — 007.1/007.2→005, 007.3→022, write new 007 subtasks** | Most thorough fix | Each task gets correct content | Requires writing new branch identification subtasks for 007 |

**Recommendation:** B2d — move misplaced subtasks to their correct homes, then write new subtasks for 007 that match its actual pipeline role (branch identification and categorization).

**Impact:**
- Task 005 gains concrete error-detection subtasks (replacing generic boilerplate)
- Task 022 gains migration analysis context
- Task 007 needs new subtasks written for branch identification/categorization

---

### B3: Decide Task 006/013 Overlap

**Current state:**
- Task 006: "Branch Backup and Restore Mechanism"
- Task 013: "Branch Backup and Safety"
- Both cover backup/safety operations

**The problem:** Two tasks cover the same domain. Per pre-merge disposition (§5d), 013 should fold into 006.

**Options:**

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **B3a: Merge 013 into 006** | 013 subtasks become subtasks of 006; 013 becomes a stub/redirect | Eliminates duplication; single backup task | 006 already has subtasks; need to renumber |
| **B3b: Keep separate with clear boundary** | 006 = backup mechanism (create/restore backups); 013 = safety checks (pre-operation validation) | Clear separation of concerns | Need to verify subtasks actually split this way |
| **B3c: 013 as subtask of 006** | 013 becomes 006.4 (or similar); keeps its identity within 006 | Preserves 013 content; reduces task count | Changes task numbering; may break cross-refs |

**Recommendation:** B3b — check whether subtasks naturally split into "mechanism" vs "safety checks". If they don't, use B3a.

**Impact:**
- B3a: Task 013 file becomes stub/redirect; all cross-refs to 013 need updating
- B3b: Both tasks get clearer scope descriptions; no structural change
- B3c: Task numbering changes; cross-ref updates needed

---

### B4: Decide Task 011/017 Overlap

**Current state:**
- Task 011: "Integrate Validation Framework into Multistage Alignment Workflow"
- Task 017: "Validation Integration Framework"
- Both cover validation integration

**The problem:** Per pre-merge disposition, 017 folds into the 003→008→011 validation chain. But 017 may represent a distinct layer (plugin-level extensibility).

**Options:**

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **B4a: Merge 017 into 011** | 017 subtasks become subtasks of 011; 017 becomes stub/redirect | Eliminates duplication; single validation integration task | 011 already has subtasks |
| **B4b: Keep separate with clear boundary** | 011 = workflow-level integration (how validation runs during alignment); 017 = plugin-level extensibility (how to add new validation checks) | Preserves progressive layering (003→008→011→017) | Need to verify subtasks actually split this way |
| **B4c: 017 as subtask of 011** | 017 becomes 011.5 (or similar); keeps its identity within 011 | Preserves 017 content; reduces task count | Changes task numbering |

**Recommendation:** B4b — the progressive layering (basic→comprehensive→integrated→pluggable) is a real architectural pattern, not redundancy. Define clear boundaries and document them.

**Impact:**
- B4a: Task 017 file becomes stub/redirect; cross-refs need updating
- B4b: Both tasks get clearer scope descriptions; validation chain documented
- B4c: Task numbering changes

---

### B5: Define Validation Boundaries (003→008→011→017)

**Current state:** Four tasks form a progressive validation layer, but boundaries are unclear:
- Task 003: Pre-merge file validation (basic)
- Task 008: CI/CD merge validation framework (comprehensive)
- Task 011: Validation integration into alignment workflow (workflow-level)
- Task 017: Validation integration framework (plugin-level)

**Decision needed:** For each task, define:
1. What validation operations it owns (exclusive)
2. What it delegates to other layers
3. What its interface to the next layer is

**Output:** A `VALIDATION_LAYER_BOUNDARIES.md` document that:
- Maps each validation type to exactly one task
- Defines the interface between layers
- Specifies what a new validation check should implement at each layer
- Makes it clear where to add a new check (e.g., "file format validation → 003", "CI gate → 008", "workflow step → 011", "plugin hook → 017")

**This is not optional** — without clear boundaries, any implementation will create confusion about where validation logic belongs.

---

### B6: Decide Task 015/012 Overlap (if B1 chooses B1a or B1d)

**Only needed if B1 result keeps orchestration content in Task 015 or merges it into 012.**

**Current state:**
- Task 012: "Orchestrate Sequential Branch Alignment Workflow" — already the orchestrator
- Task 015: If renamed to orchestration, overlaps with 012

**Options:**

| Option | Description |
|--------|-------------|
| **B6a: 012 = high-level orchestration, 015 = implementation details** | 012 defines the workflow; 015 implements the specific components |
| **B6b: 012 = single-branch orchestration, 015 = multi-branch orchestration** | 012 handles one branch at a time; 015 handles the queue/priority system |
| **B6c: Merge 015 orchestration into 012** | 012 absorbs all orchestration; 015 repurposed |

**Recommendation:** B6c (if B1d chosen) or B6b (if B1a chosen). The distinction between "single-branch pipeline" and "multi-branch queue" is real but may not warrant separate tasks.

---

## Phase C: Structural Reconnection ⏳ PENDING (depends on Phase B)

These items modify the task dependency graph and task structure. They depend on Phase B decisions being finalized first.

### C1: Reconnect Task 002 Clustering to Core Pipeline

**Current state:** Task 002 (Branch Clustering System) is disconnected from the core pipeline. It has no "Depends on" or "Blocks" connections to Tasks 001, 007, 009, or 012.

**Action:**
- Add dependency: 002 → 007 (clustering needs branch identification output)
- Add blocking: 002 → 009/010 (alignment can use clustering to determine strategy)
- Add blocking: 002 → 012 (orchestrator can use clustering for priority assignment)
- Verify: Does 002's output (cluster assignments) actually feed into 009/010's strategy selection?

**Risk:** If 002's clustering is not actually used by downstream tasks, adding dependencies creates false coupling. Verify by reading 009/010 subtask content.

---

### C2: Reconnect Task 001 to Downstream Tasks

**Current state:** Task 001 ("Align and Architecturally Integrate Feature Branches") is the foundation task but its dependency connections are unclear.

**Action:**
- Verify 001's "Blocks" annotations point to 009/010/012
- Verify 001's "Depends on" annotations are correct
- Add missing connections

---

### C3: Reconnect Validation Chain (003→008→011→017)

**Current state:** The four validation tasks form a progressive layer but their dependency fields may not reflect this.

**Action:**
- Verify dependency chain: 003 → 008 → 011 → 017
- Add missing "Depends on" / "Blocks" annotations
- Reference the VALIDATION_LAYER_BOUNDARIES.md document (from B5)

---

### C4: Collapse Fake Sequential Tail (019–025)

**Current state:** Tasks 019–025 are marked as a sequential chain (019→020→021→...→025) but they are actually parallel post-MVP items that can be done independently.

**Action:**
- Change all "Depends on" fields in 019–025 to remove sequential dependencies
- Mark each as "Post-MVP / parallel" in status
- Add note: "These tasks are framework stubs. Actual effort is 2-3 hours each. Implement only when specific need arises."

---

### C5: Apply Pre-Merge Disposition (from §5d decision record)

**Current state:** The §5d decision record specifies how tasks 016-022 should be split between pre-merge and post-MVP, but the task files themselves don't reflect this.

**Action per task:**

| Task | Disposition | Action |
|------|-------------|--------|
| 016 (Rollback) | Merge into backup stage (006) | Add 016 subtasks as 006 subtasks; mark 016 as "merged into 006" |
| 017 (Validation Integration) | Fold into validate stage (003→008→011) | Depends on B4 decision; add to validation chain |
| 018 (E2E Testing) | New pre-merge test gate | Mark as pre-merge; add "Blocks" annotation for merge readiness |
| 020 (Documentation) | Split: changelog pre-merge, KB post-merge | Create subtask split: 020.1 (changelog/PR-summary, pre-merge) + 020.2 (KB/training, post-merge) |
| 021 (Maintenance) | Split: health probe pre-merge, scheduling post-merge | Create subtask split: 021.1 (health/diagnostic, optional pre-merge) + 021.2 (scheduling/alerting, post-merge) |
| 022 (Improvements) | Split: migration step is core, rest is post-merge | 022's migration step (012.15 backend→src/backend) is already wired as core dependency; mark rest as post-merge |

---

### C6: Restore Lost Task 002 Specifications

**Current state:** Task 002's subtask files (task_002.1 through task_002.9) are ~80% bloat with zero unique content (per UNIQUE_DELTAS_REPORT.md). The original detailed specs exist in `archive/task_data_historical/handoff_archive_task75/`.

**Action:**
- Extract meaningful specs from archive
- Rewrite task_002.1 through task_002.9 with concrete implementation steps
- Remove generic boilerplate sections

---

### C7: Finish Task 012.14/.15 Stubs

**Current state:** task_012.14.md and task_012.15.md are marked "TBD" with no real content.

**Action:**
- Write concrete implementation steps for each
- 012.14: Likely related to validation integration (from B4/B5)
- 012.15: Architectural migration step (backend→src/backend) — already referenced in 015.16

---

## Phase D: Cleanup & Standards ⏳ PENDING (depends on Phase C)

These are low-risk polishing items that should only be done after the structure is correct.

### D1: Clean Task 005 Subtasks

**Current state:** Task 005 subtasks are generic boilerplate (research, implement, integrate, document). Parent has real intent (AST import validation + merge artifact detection).

**Action:**
- Replace generic subtasks with concrete steps matching parent intent
- If B2a/B2d chosen: integrate 007.1/007.2 content as concrete subtasks

---

### D2: Fix new_task_plan/ References

**Current state:** 8 scripts + 15+ docs still reference `new_task_plan/` (per .iflow/TRIAGE_REPORT.md). This directory no longer exists.

**Action:**
- Find all references to `new_task_plan/` in scripts and docs
- Replace with current paths or remove if stale

---

### D3: Section Dedup (Tasks 010–012)

**Current state:** Tasks 010, 011, 012 have 33–38 sections each. TASK_STRUCTURE_STANDARD.md specifies 14 sections.

**Action:**
- Consolidate redundant sections
- Remove duplicate content
- Align with TASK_STRUCTURE_STANDARD.md format

---

### D4: Task 002.x Subtask Regeneration

**Current state:** 80% bloat, zero unique content per UNIQUE_DELTAS_REPORT.md.

**Action:**
- Depends on C6 (archive extraction)
- Rewrite each subtask file with clean template
- Remove boilerplate sections

---

### D5: Subtask-Level Effort Deflation

**Current state:** Subtask-level effort estimates in tasks 019–025 still show 4-6hr, 6-8hr, 8-10hr per subtask (inflated). Parent-level estimates were deflated in Phase A but subtask-level was not.

**Action:**
- For each subtask in 019–025, set effort to 30min-1hr
- For Task 002 subtasks, set effort based on actual scope (after C6)

---

### D6: Subtask Heading Format Standardization

**Current state:** Mixed formats — 296 subtask headings use period format (`### 004.1.`) and 151 use colon format (`### 004.1:`). TASK_STRUCTURE_STANDARD.md uses colon for sub-subtasks.

**Action:**
- Decide on single format (recommend period for subtasks, colon for sub-subtasks per standard)
- Apply consistently across all files

---

### D7: Supersede Stale Maps

**Current state:** `docs/CURRENT_DOCUMENTATION_MAP.md` points to `PROJECT_STATE_PHASE_3_READY.md` and `new_task_plan/` which no longer exist.

**Action:**
- Add superseded-by header to CURRENT_DOCUMENTATION_MAP.md
- Point to DOCUMENTATION_TASK_MAP.md as the current reference

---

### D8: parse-prd Sync

**Current state:** tasks.json was deleted (commit `c7bc3895`). If it needs to be regenerated for tooling compatibility:

**Action:**
- Run `python taskmaster_cli.py parse-prd --input tasks/` to regenerate
- Verify round-trip fidelity
- Only do this after all structural changes are complete (Phase C)

---

## Execution Order

```
Phase A ✅ (done)
    │
Phase B (decisions)
    ├── B1: Task 015 fate ─────────────────┐
    ├── B2: Task 007 subtask reassignment   │
    ├── B3: 006/013 overlap ───────────────┤  ← B3 and B4 can proceed
    ├── B4: 011/017 overlap ───────────────┤    in parallel
    ├── B5: Validation boundaries ─────────┤    (depends on B4)
    └── B6: 015/012 overlap ───────────────┘    (depends on B1)
    │
Phase C (structural, depends on B)
    ├── C1: Reconnect 002
    ├── C2: Reconnect 001
    ├── C3: Reconnect validation chain (depends on B5)
    ├── C4: Collapse fake tail
    ├── C5: Apply pre-merge disposition (depends on B3, B4)
    ├── C6: Restore 002 specs
    └── C7: Finish 012.14/.15 stubs
    │
Phase D (cleanup, depends on C)
    ├── D1: Clean 005 subtasks (depends on B2)
    ├── D2: Fix new_task_plan/ refs
    ├── D3: Section dedup
    ├── D4: 002.x regeneration (depends on C6)
    ├── D5: Subtask effort deflation
    ├── D6: Heading format standardization
    ├── D7: Supersede stale maps
    └── D8: parse-prd sync (after all changes)
```

---

## Pre-Merge Pipeline (Target State)

After all phases complete, the pre-merge pipeline should be:

```
007 (identify branches) → 006+016 (backup+rollback) → 009/010 (align) → 005 (error check) → 011+017 (validate) → 018 (E2E test) → 020.1 (changelog)
                                                                              ↑
                                                         022 (migration step, before alignment)
                                                         002 (clustering, optional input)
                                                         001 (foundation, feeds into all)
```

Orchestrated by: **012** (sequential workflow)

Post-MVP (parallel, no sequential chain):
- 019 (deployment), 020.2 (KB/training), 021.2 (scheduling), 023 (optimization), 024 (roadmap), 025 (scaling)

---

## Change Log

| Date | Phase | Item | Commit |
|------|-------|------|--------|
| 2026-06-08 | Pre-A | Delete tasks.json | `c7bc3895` |
| 2026-06-08 | Pre-A | Delete duplicate tasks 026-028 | `dcb242a4` |
| 2026-06-11 | Pre-A | Archive stale root docs | `bf33876f` |
| 2026-06-11 | Pre-A | Fix cross-references to archived files | `345f8670` |
| 2026-06-12 | Pre-A | Refresh counts + pre-merge disposition | `e4833db9` |
| 2026-06-12 | Pre-A | Fix source-of-truth claim + 022 exception | `1a09a52b` |
| 2026-06-13 | A | Phase A mechanical fixes (numbering, labels, refs, effort) | `32e4334e` |
| 2026-06-13 | A | Phase A high-complexity (009 cross-refs, 015 phantom refs) | `17ec9e2e` |
| 2026-06-19 | A | Restore doc map + remaining mechanical fixes | `16126ca4` |
