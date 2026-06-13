# `.taskmaster/` Documentation ↔ Task Map

**Generated:** 2026-06-11 · **Last verified:** 2026-06-13
**Scope:** Maps every documentation cluster in `.taskmaster/` to the task markdown files (`tasks/task_NNN.md`) it supports, and records the different approaches undertaken in this workspace.
**Source of truth caveat:** This repository's *real* project is **Branch Alignment Tooling**, not EmailIntelligence (see [`PROJECT_IDENTITY.md`](PROJECT_IDENTITY.md)). All 25 canonical tasks are git/branch alignment tasks.

---

## 1. Documentation Status — At a Glance

| Metric | Count | Notes |
|--------|-------|-------|
| Total `.md` files under `.taskmaster/` | **615** | Heavily sprawling; mostly process/meta docs |
| Canonical main tasks (`tasks/task_NNN.md`) | **25** (001–025) | + `task_002-clustering.md` companion guide |
| Subtask files (`tasks/task_NNN.M.md`) | **180** | |
| Active docs in `docs/` | **95** | Mix of current + stale |
| Guidance docs (`guidance/`) | **28** | Architecture/implementation guidance |
| Reports (`reports/`) | **10** | Analysis snapshots |
| Archived docs (`archive/`) | **184** | Historical; **do not treat as canonical** (+13 root files moved to `archive/documentation_cleanup/` on 2026-06-13) |

**Overall health:** ⚠️ **Cluttered and partially stale.**
- `tasks/` markdown is **canonical**; `tasks.json` is intentionally empty/absent (used only for round-trip fidelity tests).
- Several index docs are themselves **out of date** — e.g. [`docs/CURRENT_DOCUMENTATION_MAP.md`](docs/CURRENT_DOCUMENTATION_MAP.md) points to `PROJECT_STATE_PHASE_3_READY.md` and a `new_task_plan/` directory that **no longer exist**.
- The most current, trustworthy meta-references are [`TASK_ANALYSIS_AND_GOTCHAS.md`](TASK_ANALYSIS_AND_GOTCHAS.md) (2026-06-11), [`PROJECT_IDENTITY.md`](PROJECT_IDENTITY.md) (2026-02-27), [`AGENTS.md`](AGENTS.md), and [`tasks/AGENTS.md`](tasks/AGENTS.md).

---

## 2. Canonical Task Inventory (the `task_NNN.md` files)

The 25 tasks form a branch-alignment pipeline. They cluster into themes:

```diagram
╭──────────────────────────────────────────────────────────────╮
│ FOUNDATION         001 Align/integrate feature branches        │
│                    004 Core branch alignment framework         │
├──────────────────────────────────────────────────────────────┤
│ ANALYSIS           002 Branch clustering system (+clustering)   │
│                    007 Feature branch identification/categorize │
├──────────────────────────────────────────────────────────────┤
│ ERROR DETECTION    005 Automated error detection for merges     │
├──────────────────────────────────────────────────────────────┤
│ VALIDATION LAYERS  003 Pre-merge validation scripts (basic)     │
│   (progressive)    008 Merge validation framework (CI/CD)       │
│                    011 Validation → alignment workflow          │
│                    017 Validation integration framework (plugin)│
├──────────────────────────────────────────────────────────────┤
│ BACKUP / SAFETY    006 Branch backup & restore                  │
│                    013 Branch backup and safety                 │
│                    016 Rollback and recovery                    │
├──────────────────────────────────────────────────────────────┤
│ ALIGNMENT EXEC     009 Multistage primary→feature alignment     │
│                    010 Multilevel strategies (complex branches) │
├──────────────────────────────────────────────────────────────┤
│ ORCHESTRATION      012 Sequential branch alignment workflow     │
│                    015 *labelled "Validation" but is orchestr.* │
├──────────────────────────────────────────────────────────────┤
│ CONFLICTS          014 Conflict detection and resolution        │
├──────────────────────────────────────────────────────────────┤
│ TESTING            018 End-to-end testing and reporting         │
├──────────────────────────────────────────────────────────────┤
│ TAIL FRAMEWORKS    019 Deployment   020 Documentation           │
│  (over-specified)  021 Maintenance  022 Improvements            │
│                    023 Optimization 024 Roadmap  025 Scaling     │
╰──────────────────────────────────────────────────────────────╯
```

| Task file | Title | Cluster |
|-----------|-------|---------|
| [`task_001.md`](tasks/task_001.md) | Align and Architecturally Integrate Feature Branches | Foundation |
| [`task_002.md`](tasks/task_002.md) + [`task_002-clustering.md`](tasks/task_002-clustering.md) | Branch Clustering System (+ implementation guide) | Analysis |
| [`task_003.md`](tasks/task_003.md) | Pre-merge Validation Scripts | Validation (basic) |
| [`task_004.md`](tasks/task_004.md) | Core Branch Alignment Framework | Foundation |
| [`task_005.md`](tasks/task_005.md) | Automated Error Detection Scripts for Merges | Error detection |
| [`task_006.md`](tasks/task_006.md) | Branch Backup and Restore Mechanism | Backup/safety |
| [`task_007.md`](tasks/task_007.md) | Feature Branch Identification & Categorization | Analysis |
| [`task_008.md`](tasks/task_008.md) | Comprehensive Merge Validation Framework | Validation (CI/CD) |
| [`task_009.md`](tasks/task_009.md) | Core Multistage Primary-to-Feature Alignment | Alignment exec |
| [`task_010.md`](tasks/task_010.md) | Multilevel Strategies for Complex Branches | Alignment exec |
| [`task_011.md`](tasks/task_011.md) | Integrate Validation into Multistage Workflow | Validation (workflow) |
| [`task_012.md`](tasks/task_012.md) | Orchestrate Sequential Branch Alignment Workflow | Orchestration |
| [`task_013.md`](tasks/task_013.md) | Branch Backup and Safety | Backup/safety |
| [`task_014.md`](tasks/task_014.md) | Conflict Detection and Resolution | Conflicts |
| [`task_015.md`](tasks/task_015.md) | "Validation and Verification" ⚠️ *(subtasks = orchestration)* | Orchestration |
| [`task_016.md`](tasks/task_016.md) | Rollback and Recovery | Backup/safety |
| [`task_017.md`](tasks/task_017.md) | Validation Integration Framework | Validation (plugin) |
| [`task_018.md`](tasks/task_018.md) | End-to-End Testing and Reporting | Testing |
| [`task_019.md`](tasks/task_019.md) | Deployment and Release Management | Tail framework |
| [`task_020.md`](tasks/task_020.md) | Documentation and Knowledge Management | Tail framework |
| [`task_021.md`](tasks/task_021.md) | Maintenance and Monitoring | Tail framework |
| [`task_022.md`](tasks/task_022.md) | Improvements and Enhancements Framework | Tail framework |
| [`task_023.md`](tasks/task_023.md) | Optimization and Performance Tuning | Tail framework |
| [`task_024.md`](tasks/task_024.md) | Future Development and Roadmap | Tail framework |
| [`task_025.md`](tasks/task_025.md) | Scaling and Advanced Features | Tail framework |

> **Known data-integrity issues** (full detail in [`TASK_ANALYSIS_AND_GOTCHAS.md`](TASK_ANALYSIS_AND_GOTCHAS.md)):
> Task 008 subtasks mis-numbered `9.x`; Task 009 parent cross-refs off-by-one; Task 015 contaminated with Task-27 orchestration content + phantom `27.x` deps; Task 007 subtasks really belong to Task 005; Tasks 002 & 019–025 have inflated effort estimates.

---

## 3. Documentation → Task Mapping (by theme)

Most `.taskmaster` docs are **process/meta** (about *how* tasks are authored, validated, and synced) rather than tied to one task. The table below maps each documentation cluster to the task(s) it serves.

### 3a. Branch-alignment domain docs → specific tasks

| Document | Purpose | Corresponds to |
|----------|---------|----------------|
| [`docs/branch-alignment-framework-prd.txt`](docs/branch-alignment-framework-prd.txt) | The master PRD that **all 25 tasks** were parsed from | Tasks 001–025 (root source) |
| [`docs/master-prd.txt`](docs/master-prd.txt) | Top-level PRD pointer | Tasks 001–025 |
| [`docs/branch-alignment-aggregated-documentation.md`](docs/branch-alignment-aggregated-documentation.md) | Aggregated overview of the alignment system | 001, 004, 009, 012 |
| [`docs/branch_alignment_workflow.md`](docs/branch_alignment_workflow.md) | End-to-end alignment workflow | 009, 010, 012 |
| [`docs/BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md`](docs/BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md) | Prevent regressions during alignment | 001, 004, 009, 011 |
| [`docs/branch_alignment/`](docs/branch_alignment/) (8 files: SYSTEM_OVERVIEW, MULTI_AGENT_COORDINATION, COORDINATION_AGENT_SYSTEM, PRECALCULATION_PATTERNS, INDEX, README…) | Multi-agent orchestration of sequential alignment | **012**, 015 |
| [`docs/BRANCH_ANALYSIS_SUBTASKS_EXACT.md`](docs/BRANCH_ANALYSIS_SUBTASKS_EXACT.md), [`BRANCH_ANALYSIS_TASK_SPECIFICATIONS_IMPROVEMENTS_SUMMARY.md`](docs/BRANCH_ANALYSIS_TASK_SPECIFICATIONS_IMPROVEMENTS_SUMMARY.md), [`BRANCH_ANALYSIS_FORWARD_REORGANIZATION_SUMMARY.md`](docs/BRANCH_ANALYSIS_FORWARD_REORGANIZATION_SUMMARY.md), [`BRANCH_ANALYSIS_REORGANIZATION.md`](docs/BRANCH_ANALYSIS_REORGANIZATION.md), [`REORGANIZATION_PLAN_BRANCH_ANALYSIS_FORWARD.md`](docs/REORGANIZATION_PLAN_BRANCH_ANALYSIS_FORWARD.md) | Branch analysis / clustering spec work | **002**, 007 |
| [`docs/BRANCH_ISOLATION_GUIDELINES.md`](docs/BRANCH_ISOLATION_GUIDELINES.md) | No-merge isolation policy between main/scientific/orchestration-tools | 006, 013, 016 |
| [`docs/scientific_branch_conflict_resolution_plan.md`](docs/scientific_branch_conflict_resolution_plan.md) | Conflict-resolution strategy on scientific branch | **014** |
| [`docs/three_branch_architectural_comparison.md`](docs/three_branch_architectural_comparison.md) | Compare main/scientific/orchestration architectures | 001, 002 |
| [`docs/task_004_tuned_recommendations.md`](docs/task_004_tuned_recommendations.md) | Tuned recommendations for the core framework | **004** |
| [`guidance/implementation_lessons/task-002-clustering-guide.md`](guidance/implementation_lessons/task-002-clustering-guide.md) | Implementation lessons for clustering | **002** |
| [`reports/task75_techspec_verification.md`](reports/task75_techspec_verification.md), [`docs/TASK_007_DEPRECATION_SUMMARY.md`](docs/TASK_007_DEPRECATION_SUMMARY.md), [`docs/TASK_7_PURPOSE_CLARIFICATION.md`](docs/TASK_7_PURPOSE_CLARIFICATION.md), [`docs/TASK_INTERPRETATION_FINDING_TASK7.md`](docs/TASK_INTERPRETATION_FINDING_TASK7.md) | Task 7 purpose/deprecation history (legacy "Task 75/7") | **007** |
| [`complexity_reports/task-001-linting-errors.txt`](complexity_reports/task-001-linting-errors.txt) | Linting findings for task 001 work | **001** |
| [`reports/task-complexity-report.json`](reports/task-complexity-report.json) | Complexity scoring across tasks | All tasks |

### 3b. Process / meta docs → ALL tasks (task-authoring machinery)

| Document(s) | Purpose | Applies to |
|-------------|---------|-----------|
| [`TASK_STRUCTURE_STANDARD.md`](TASK_STRUCTURE_STANDARD.md) | The mandatory 14-section task format | All tasks |
| [`templates/enhanced_task_template.md`](templates/enhanced_task_template.md), [`docs/SUBTASK_MARKDOWN_TEMPLATE.md`](docs/SUBTASK_MARKDOWN_TEMPLATE.md), [`guidance/SUBTASK_EXPANSION_TEMPLATE.md`](guidance/SUBTASK_EXPANSION_TEMPLATE.md) | Authoring templates | All tasks/subtasks |
| [`docs/COMPLETE_TASK_WORKFLOW.md`](docs/COMPLETE_TASK_WORKFLOW.md), [`docs/TASK_WORKFLOW_INTEGRATION.md`](docs/TASK_WORKFLOW_INTEGRATION.md), [`docs/complete_tasks_flow.mmd`](docs/complete_tasks_flow.mmd), [`docs/iterative_tasks_flow.mmd`](docs/iterative_tasks_flow.mmd) | End-to-end task lifecycle | All tasks |
| [`docs/TASK_ENHANCEMENT_PROCEDURES.md`](docs/TASK_ENHANCEMENT_PROCEDURES.md), [`docs/ENHANCED_TASK_SPECIFICATIONS_SUMMARY.md`](docs/ENHANCED_TASK_SPECIFICATIONS_SUMMARY.md), [`ENHANCED_TASK_SPECIFICATIONS_ARCHITECTURAL_FOCUS_SUMMARY.md`](docs/ENHANCED_TASK_SPECIFICATIONS_ARCHITECTURAL_FOCUS_SUMMARY.md), [`FINAL_TASK_SPECIFICATION_IMPROVEMENTS_SUMMARY.md`](docs/FINAL_TASK_SPECIFICATION_IMPROVEMENTS_SUMMARY.md), [`TASK_SPECIFICATION_IMPROVEMENTS_SUMMARY.md`](docs/TASK_SPECIFICATION_IMPROVEMENTS_SUMMARY.md), [`ENHANCED_ACCEPTANCE_CRITERIA_SUMMARY.md`](docs/ENHANCED_ACCEPTANCE_CRITERIA_SUMMARY.md) | Spec-quality enhancement passes | All tasks |
| [`docs/TASK_METADATA_PRESERVATION_GUIDE.md`](docs/TASK_METADATA_PRESERVATION_GUIDE.md), [`reports/metadata_coverage_report.json`](reports/metadata_coverage_report.json) | Preserve custom fields stripped by Task Master | All tasks |
| [`docs/MEMORY_API_FOR_TASKS.md`](docs/MEMORY_API_FOR_TASKS.md) | Progress-logging API for agents | All tasks |
| [`docs/SCRIPTS_IN_TASK_WORKFLOW.md`](docs/SCRIPTS_IN_TASK_WORKFLOW.md), [`guidance/SCRIPTS_AND_TOOLS_INTEGRATION.md`](guidance/SCRIPTS_AND_TOOLS_INTEGRATION.md) | Helper-script catalogue | All tasks |
| [`guidance/TASK_DEPENDENCY_VISUAL_MAP.md`](guidance/TASK_DEPENDENCY_VISUAL_MAP.md), [`guidance/task_mapping.md`](guidance/task_mapping.md), [`guidance/reorganized_tasks.md`](guidance/reorganized_tasks.md), [`guidance/new_task_plan_renumbered.md`](guidance/new_task_plan_renumbered.md) | Dependency graph + renumbering maps | All tasks |
| [`docs/TASK_DETAIL_IMPROVEMENTS_MAP.md`](docs/TASK_DETAIL_IMPROVEMENTS_MAP.md), [`docs/TASK_CLASSIFICATION_SYSTEM.md`](docs/TASK_CLASSIFICATION_SYSTEM.md) | Task classification + improvement mapping | All tasks |

### 3c. PRD generation / round-trip fidelity → tasks↔PRD machinery

| Document(s) | Purpose | Relevance |
|-------------|---------|-----------|
| [`generated_prd_all_tasks.md`](archive/documentation_cleanup/generated_prd_all_tasks.md) (374 KB), [`generated_prd_from_tasks.md`](archive/documentation_cleanup/generated_prd_from_tasks.md), [`test_generated_prd.md`](archive/documentation_cleanup/test_generated_prd.md), [`test_roundtrip_prd.md`](archive/documentation_cleanup/test_roundtrip_prd.md) | PRDs reverse-engineered from the 25 task files | Tasks→PRD output (archived) |
| [`ROUNDTRIP_FIDELITY_TEST_RESULTS.md`](archive/documentation_cleanup/ROUNDTRIP_FIDELITY_TEST_RESULTS.md), [`docs/ROUND_TRIP_QUICK_REFERENCE.md`](docs/ROUND_TRIP_QUICK_REFERENCE.md), [`docs/ROUND_TRIP_SCRIPTS_SUMMARY.md`](docs/ROUND_TRIP_SCRIPTS_SUMMARY.md), [`docs/PERFECT_FIDELITY_PROCESS_DOCUMENTATION.md`](docs/PERFECT_FIDELITY_PROCESS_DOCUMENTATION.md) | Validate Tasks→PRD→Tasks fidelity | All tasks (QA) |
| [`PRD_IMPROVEMENT_INVESTIGATION.md`](archive/documentation_cleanup/PRD_IMPROVEMENT_INVESTIGATION.md), [`TASK_PRD_DIFF_COMPARISON.md`](archive/documentation_cleanup/TASK_PRD_DIFF_COMPARISON.md), [`docs/PRD_GENERATION_IMPROVEMENTS_SUMMARY.md`](docs/PRD_GENERATION_IMPROVEMENTS_SUMMARY.md), [`docs/IMPROVEMENTS_TO_MAXIMIZE_PRD_ACCURACY.md`](docs/IMPROVEMENTS_TO_MAXIMIZE_PRD_ACCURACY.md), [`docs/FIRST_ORDER_PRD_IMPROVEMENTS_ANALYSIS.md`](docs/FIRST_ORDER_PRD_IMPROVEMENTS_ANALYSIS.md) | Iterative PRD-accuracy improvement work | All tasks (QA) |
| [`archive/prd_iterations/`](archive/prd_iterations/) (22 files) | Historical PRD generation iterations | Archived QA |

### 3d. Data-integrity / contamination prevention → cross-cutting

| Document(s) | Purpose | Relevance |
|-------------|---------|-----------|
| [`docs/AGENTIC_CONTAMINATION_ANALYSIS.md`](docs/AGENTIC_CONTAMINATION_ANALYSIS.md), [`docs/CONTAMINATION_DOCUMENTATION_INDEX.md`](docs/CONTAMINATION_DOCUMENTATION_INDEX.md), [`docs/CONTAMINATION_INCIDENTS_SUMMARY.md`](docs/CONTAMINATION_INCIDENTS_SUMMARY.md) | Records of cross-task content contamination | 007, 008, 015 (corrupted tasks) |
| [`docs/CONTENT_DUPLICATION_PREVENTION_GUIDELINES.md`](docs/CONTENT_DUPLICATION_PREVENTION_GUIDELINES.md), [`docs/PREVENTION_FRAMEWORK.md`](docs/PREVENTION_FRAMEWORK.md) | Prevent duplication/corruption | All tasks |
| [`docs/MD_VALIDATION_REPORT.md`](docs/MD_VALIDATION_REPORT.md), [`docs/TASK_REDESIGN_VERIFICATION.md`](docs/TASK_REDESIGN_VERIFICATION.md), [`docs/PLACEHOLDER_BACKUP_MAPPING.md`](docs/PLACEHOLDER_BACKUP_MAPPING.md) | Markdown validation + backup mapping | All tasks |
| [`PROJECT_IDENTITY.md`](PROJECT_IDENTITY.md) | Asserts project = Branch Alignment, not EmailIntelligence | 002, 003, 004 (most-confused) |
| [`OLD_TASK_NUMBERING_DEPRECATED.md`](OLD_TASK_NUMBERING_DEPRECATED.md) | Old `task-001..020` numbering is dead | All tasks |

### 3e. Agent-config docs → AI agent context (not a single task)

| Document | Purpose |
|----------|---------|
| [`AGENTS.md`](AGENTS.md), [`AGENT.md`](AGENT.md), [`CLAUDE.md`](CLAUDE.md), [`GEMINI.md`](GEMINI.md), [`QWEN.md`](QWEN.md), [`IFLOW.md`](IFLOW.md) | Per-agent integration/instruction files (auto-loaded context) |
| [`README.md`](README.md), [`QUICK_START.md`](QUICK_START.md) | Workspace overview & quick start |
| [`guidance/README.md`](guidance/README.md), [`guidance/QUICK_REFERENCE_GUIDE.md`](guidance/QUICK_REFERENCE_GUIDE.md) | Guidance index |

### 3f. Status / handoff / unfinished-work trackers → project state

| Document | Purpose |
|----------|---------|
| [`TASKMASTER_HANDOFF.md`](archive/documentation_cleanup/TASKMASTER_HANDOFF.md) | Session handoff context (archived) |
| [`UNFINISHED_TASKS_CONSOLIDATED.md`](archive/documentation_cleanup/UNFINISHED_TASKS_CONSOLIDATED.md), [`COMBINED_UNFINISHED_WORK.md`](archive/documentation_cleanup/COMBINED_UNFINISHED_WORK.md), [`docs/UNFINISHED_SESSION_TODOS.md`](docs/UNFINISHED_SESSION_TODOS.md), [`tasks/UNIQUE_DELTAS_REPORT.md`](tasks/UNIQUE_DELTAS_REPORT.md) | Outstanding-work trackers (archived) |
| [`docs/PROJECT_STATUS_SUMMARY.md`](docs/PROJECT_STATUS_SUMMARY.md), [`docs/PROJECT_STATE_CHECKLIST_RECOVERED.md`](docs/PROJECT_STATE_CHECKLIST_RECOVERED.md) | Project status snapshots |
| [`OPTION_C_VISUAL_MAP.md`](archive/documentation_cleanup/OPTION_C_VISUAL_MAP.md), [`RISK_MINIMIZATION_PLAN.md`](archive/documentation_cleanup/RISK_MINIMIZATION_PLAN.md) | Strategy options + risk plan (archived) |
| [`reports/COMPREHENSIVE_DOCUMENTATION_ANALYSIS.md`](reports/COMPREHENSIVE_DOCUMENTATION_ANALYSIS.md), [`reports/MISSING_DOCUMENTS_RECOVERY_REPORT.md`](reports/MISSING_DOCUMENTS_RECOVERY_REPORT.md), [`reports/git_history_analysis.md`](reports/git_history_analysis.md), [`reports/AMP_*`](reports/) | Documentation/git forensic analysis |

### 3g. MVP docs — SEPARATE project (do NOT mix)

| Document | Purpose |
|----------|---------|
| [`tasks/mvp/README.md`](tasks/mvp/README.md), [`tasks/mvp/EPIC_DEFINITIONS.md`](tasks/mvp/EPIC_DEFINITIONS.md), [`tasks/mvp/MVP_TODO.md`](tasks/mvp/MVP_TODO.md) | EmailIntelligence MVP scope — **isolated from the 25 alignment tasks** |

---

## 4. Different Approaches / Initiatives Undertaken in This Folder

The documentation history shows several distinct (and sometimes competing) initiatives:

```diagram
╭─ APPROACH 1: Task numbering migration ────────────────────────╮
│ Old task-001..020  →  task_NNN.md (current)                    │
│ Docs: OLD_TASK_NUMBERING_DEPRECATED, archive/deprecated_      │
│ numbering/ (7 files), guidance/TASK_NUMBERING_ANALYSIS         │
╰───────────────────────────────────────────────────────────────╯
╭─ APPROACH 2: 14-section standardisation / retrofit ───────────╮
│ Normalise every task to TASK_STRUCTURE_STANDARD.md            │
│ Docs: archive/retrofit_work/ (6), TASK_RESTRUCTURING_ANALYSIS │
╰───────────────────────────────────────────────────────────────╯
╭─ APPROACH 3: Tasks⇄PRD round-trip fidelity ──────────────────╮
│ Reverse-engineer PRD from tasks, re-parse, diff               │
│ Docs: ROUND_TRIP_*, PERFECT_FIDELITY_*, archive/prd_iterations│
╰───────────────────────────────────────────────────────────────╯
╭─ APPROACH 4: Contamination cleanup & prevention ─────────────╮
│ Detect/fix cross-task content bleed (007/008/015)            │
│ Docs: CONTAMINATION_*, PREVENTION_FRAMEWORK, archive/cleanup_ │
│ work/ (9), archive/investigation_work/ (7)                    │
╰───────────────────────────────────────────────────────────────╯
╭─ APPROACH 5: Phase-based execution (1 → 1.5 → 2/4 → 3) ──────╮
│ Superseded; archived. Docs: archive/phase_planning/ (17)     │
╰───────────────────────────────────────────────────────────────╯
╭─ APPROACH 6: Integration / handoff orchestration ────────────╮
│ Multi-agent coordination + clustering integration            │
│ Docs: archive/integration_work/ (15), docs/branch_alignment/ │
│ archive/task_data_historical/ (handoff_archive_task002 …)    │
╰───────────────────────────────────────────────────────────────╯
╭─ APPROACH 7: Project-identity correction ────────────────────╮
│ Re-assert Branch Alignment ≠ EmailIntelligence; reject pivot │
│ Docs: PROJECT_IDENTITY.md, ORACLE_RECOMMENDATION_TODO.md     │
╰───────────────────────────────────────────────────────────────╯
```

| Subfolder of `archive/` | Files | Initiative it documents |
|-------------------------|-------|-------------------------|
| `deprecated_numbering/` | 7 | Approach 1 — old→new task IDs |
| `retrofit_work/` | 6 | Approach 2 — 14-section retrofit |
| `prd_iterations/` | 22 | Approach 3 — PRD round-trip |
| `cleanup_work/` | 9 | Approach 4 — contamination cleanup |
| `investigation_work/` | 7 | Approach 4 — root-cause investigations |
| `phase_planning/` | 17 | Approach 5 — phased execution |
| `integration_work/` | 15 | Approach 6 — integration/handoff |
| `task_data_historical/` | ~40 | Approach 6 — Task 002 handoffs, historical task data |
| `task_context/`, `task_specs/`, `project_docs/` | ~40 | Mixed historical task context |

---

## 5. Recommended Reading Order (current & trustworthy)

1. [`PROJECT_IDENTITY.md`](PROJECT_IDENTITY.md) — what this project actually is
2. [`TASK_ANALYSIS_AND_GOTCHAS.md`](TASK_ANALYSIS_AND_GOTCHAS.md) — known corruption & fixes (read before editing any task)
3. [`TASK_STRUCTURE_STANDARD.md`](TASK_STRUCTURE_STANDARD.md) — the 14-section format
4. [`AGENTS.md`](AGENTS.md) + [`tasks/AGENTS.md`](tasks/AGENTS.md) — workflow & sync protocol
5. Individual [`tasks/task_NNN.md`](tasks/) files for the work itself

> ⚠️ **Do not rely on** [`docs/CURRENT_DOCUMENTATION_MAP.md`](docs/CURRENT_DOCUMENTATION_MAP.md) — it references `PROJECT_STATE_PHASE_3_READY.md` and `new_task_plan/` which no longer exist. This document supersedes it.

---

## 5b. Drift Classification — Intentional vs. Not-In-Line-With-Tasks

"Out of date" splits into two kinds. **Intentional drift** = a deliberate, documented divergence where the doc *correctly* describes a by-design decision. **Unintentional drift** = a doc whose claims now *contradict the canonical `task_001–025.md` content* (phantom files, defunct schemes presented as "current", wrong counts/IDs).

### Three generations of task numbering (root cause of most drift)

```diagram
GEN 1 (planning)      GEN 2 ("Phase 3")            GEN 3 (CANONICAL, now)
task-001..020   ──▶   007, 075.1-5, 079-083  ──▶   task_001..025.md
new_task_plan/        new_task_plan/task_files/     tasks/ (flat)
hyphenated            "9 focused tasks"             underscore, 14-section
                      ↑ NEVER MATERIALIZED          ↑ actual reality
                      (no new_task_plan/ exists)
```
The Jan 6 cleanup docs deprecated **Gen 1** and declared **Gen 2** "current" — but Gen 2 was itself abandoned in favour of **Gen 3**. So those docs are *doubly* stale: they point forward to a scheme that never shipped.

### A. Intentional drift (doc correctly describes a by-design decision — leave as-is)

| Divergence | Where documented | Why it's intentional |
|------------|------------------|----------------------|
| `tasks.json` empty/absent while `tasks/*.md` is canonical | [`README.md`](README.md), [`tasks/AGENTS.md`](tasks/AGENTS.md) | Markdown-canonical design; JSON only for round-trip tests |
| Old `task-001..020` numbering abandoned | [`OLD_TASK_NUMBERING_DEPRECATED.md`](OLD_TASK_NUMBERING_DEPRECATED.md) | Deliberate consolidation/renumbering |
| Project re-identified Branch Alignment ≠ EmailIntelligence | [`PROJECT_IDENTITY.md`](PROJECT_IDENTITY.md) | Deliberate scope correction; pivot proposals *rejected* |
| `tasks/mvp/` kept separate from the 25 alignment tasks | [`PROJECT_IDENTITY.md`](PROJECT_IDENTITY.md), [`TASK_ANALYSIS_AND_GOTCHAS.md`](TASK_ANALYSIS_AND_GOTCHAS.md) | Different project; must not be merged |
| `taskmaster` branch is an orphan (no shared git history) | [`TASK_ANALYSIS_AND_GOTCHAS.md`](TASK_ANALYSIS_AND_GOTCHAS.md) | Deliberate isolation; integrate via cherry-pick only |
| No-merge isolation between main/scientific/orchestration-tools | [`docs/BRANCH_ISOLATION_GUIDELINES.md`](docs/BRANCH_ISOLATION_GUIDELINES.md) | Deliberate branch policy |

### B. Unintentional drift (contradicts actual `task_001–025` content — needs fixing)

| Stale claim | Found in | Reality in `tasks/` |
|-------------|----------|---------------------|
| "Current tasks = 007, 075.1-5, 079-083" / "exactly 9 tasks" | [`OLD_TASK_NUMBERING_DEPRECATED.md`](OLD_TASK_NUMBERING_DEPRECATED.md), [`docs/CURRENT_DOCUMENTATION_MAP.md`](docs/CURRENT_DOCUMENTATION_MAP.md) | **25 tasks** `task_001..025.md`; no 075/079-083 exist |
| Tasks live in `new_task_plan/task_files/` | both above | `new_task_plan/` **does not exist**; tasks are flat in `tasks/` |
| "Reference `PROJECT_STATE_PHASE_3_READY.md` for current state" | both above, [`OLD_TASK_NUMBERING_DEPRECATED.md`](OLD_TASK_NUMBERING_DEPRECATED.md) | File **does not exist anywhere** |
| Points to `NEW_TASK_PLAN_CONSOLIDATION_STRATEGY.md`, `CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md`, `TASK_NUMBERING_DEPRECATION_PLAN.md` | [`docs/CURRENT_DOCUMENTATION_MAP.md`](docs/CURRENT_DOCUMENTATION_MAP.md) | None exist |
| Header "12 active files" vs body "9 tasks" (self-contradiction) | [`OLD_TASK_NUMBERING_DEPRECATED.md`](OLD_TASK_NUMBERING_DEPRECATED.md) | Neither; 25 tasks |
| Hard-coded path `/home/masum/github/PR/.taskmaster/tasks/` | [`OLD_TASK_NUMBERING_DEPRECATED.md`](OLD_TASK_NUMBERING_DEPRECATED.md) | Repo is `…/remote/EmailIntelligence/` |
| "Documentation Status: Clean and current ✅" | [`docs/DOCUMENTATION_CLEANUP_COMPLETE.md`](docs/DOCUMENTATION_CLEANUP_COMPLETE.md), [`docs/CURRENT_DOCUMENTATION_MAP.md`](docs/CURRENT_DOCUMENTATION_MAP.md) | 615 md files; sprawl returned post-Jan-6 |
| "Phase 3" framing as the live phase | ~35 active docs (see grep list) incl. [`docs/PROJECT_STATUS_SUMMARY.md`](docs/PROJECT_STATUS_SUMMARY.md), [`docs/MIGRATION_STATUS_ANALYSIS.md`](docs/MIGRATION_STATUS_ANALYSIS.md), [`guidance/task_master_formatted_tasks.md`](guidance/task_master_formatted_tasks.md) | No phase model in canonical task set |
| "Task 013 — Conflict detection/resolution" | [`docs/CLI_TOOLS_INVENTORY.md`](docs/CLI_TOOLS_INVENTORY.md) | 013 = *Branch Backup & Safety*; 014 = conflict detection (off-by-one label drift) |

> **Corroboration:** [`.iflow/TRIAGE_REPORT.md`](.iflow/TRIAGE_REPORT.md) (2026-03-30) independently confirms this: `tasks/` is canonical (the Gen-2 `new_task_plan/` migration was **reversed at commit `67295077`**), 8 scripts still carry stale `new_task_plan/` references, and 15+ docs still reference the abandoned migration.

### C. Edge case — *partially* correct

[`OLD_TASK_NUMBERING_DEPRECATED.md`](OLD_TASK_NUMBERING_DEPRECATED.md) is **both**: its *intent* (kill `task-001..020`) is intentional and still valid, but its *replacement target* (Gen 2: 007/075/079-083 in `new_task_plan/`) is unintentional drift. Fix = keep the deprecation of Gen 1, rewrite the "current" half to point at `task_001..025.md`.

### Recommended remediation
1. Mark [`docs/CURRENT_DOCUMENTATION_MAP.md`](docs/CURRENT_DOCUMENTATION_MAP.md) superseded by this file (already noted in §5).
2. Patch the "current = 007/075/079-083 / new_task_plan / Phase 3" half of [`OLD_TASK_NUMBERING_DEPRECATED.md`](OLD_TASK_NUMBERING_DEPRECATED.md) to reference `task_001..025.md`.
3. Drop the "Phase 3" framing from active status docs, or move them to `archive/phase_planning/` alongside the rest of that initiative.

---

## 5c. Structural Integrity — Connections Lost During Expansion/Extrapolation

The numbers are throwaway; the **connections and structure** are what must survive. The good news (a correction to an earlier draft of this section): the **core MVP graph (tasks 001–012) is coherent and intact**. The corruption is **concentrated in three places**: the clustering subsystem (002), the over-extrapolated tail (013–025), and label/numbering drift.

> **Authoritative intended-structure doc:** [`docs/branch_alignment_workflow.md`](docs/branch_alignment_workflow.md) (2026-03-13) — a human-curated 4-layer model of the **10 key tasks**. Its layers match the *actual* multi-line `Dependencies` in the task files (verified).

### Core MVP dependency graph (001–012) — COHERENT ✓ (matches files + workflow doc)

```diagram
LAYER 1 (foundations, no deps):   001   003   004⭐   008
                                          │
LAYER 2 (need 004):        005 ── 006 ── 007   (all depend on 004)
                                          │
LAYER 3 (sequential):  009⭐(←004,006,007) ─▶ 010(←005,009) ─▶ 011(←005,009,010)
                                          │
LAYER 4 (capstone):    012⭐ (← 007, 008, 009, 010, 011)
```
- 003 and 008 declaring **no dependencies is intentional** (Layer-1 foundations), not orphaning.
- ⭐ keystones: 004 (foundation), 009 (engine), 012 (orchestrator).
- Runtime flow per branch (from the workflow doc): identify 007 → backup 006 → align 009/010 → error-check 005 → validate 011 → document.

### Where structure IS still corrupted (narrowed)

| Issue | Symptom in files | Mechanism |
|-------|------------------|-----------|
| **Clustering 002 disconnected** | 002 (+ 002.1–.9) not wired into the 10-task core; 007→004, not 007→002 | 002 imported from old "Task 75"; edges never re-attached |
| **Tail 013–025 over-extrapolated** | parents inflated to "comprehensive frameworks"; partly duplicate the core (013 backup ≈ 006; 014 conflict, 016 rollback, 017 validation overlap 005/008/011) | template extrapolation; the real MVP is 001–012 (per ORACLE TODO + workflow doc) |
| **Dependency *label* drift** | `task_012.md` lists "Task 008: **Documentation Generation**" — but 008 is the *Merge Validation Framework* | labels copied from a prior numbering; IDs right, names wrong |
| **Task 015 identity confusion** | parent="Validation"; subtasks=orchestration (27.x); workflow doc's runtime step e calls 015 "docs/changelog" | three different identities pasted over each other |
| **Subtask numbering** | 008 subtasks "9.x"; 015 "27.x" phantom; old 005.*→002.* refs | numbering generations layered without re-wiring |
| **Inflated effort/scope** | 002 ~40h shown as 212h; 019–025 2-3h shown as 20-48h | parents extrapolated into frameworks |
| **Lost technical specs** | 002 missing Task-75 metric formulas/schemas | dropped when subtasks imported/renumbered |

**Conclusion:** the original draft over-stated the damage. The **core pipeline intent survived in the actual dependency fields** (001–012 form a clean DAG). What was genuinely "lost/corrupted during expansion" is narrower: the **002 clustering subsystem got disconnected**, the **013–025 tail was extrapolated into bloated/duplicative frameworks**, and **labels/numbering drifted** across the renumberings.

> **⚠️ Live WIP correction (uncommitted, 2026-06-11):** `tasks/task_012.md` (modified), `tasks/task_012.15.md` (modified), and `tasks/task_012.14.md` (untracked) are in-progress edits actively *re-adding* lost connections:
> - **012.15** wires **orchestrator 012 → Task 022** (architectural migration `backend`→`src/backend` + factory injection), placed between backup (012.7) and alignment (012.8), feeding 009/010. → **Task 022 is NOT purely a trivial tail framework**; part of it is a real migration step the core pipeline depends on. Adjust the "INFRA 019–025 = trivial/parallel" claim accordingly for 022.
> - **012.14** wires **012 → maintenance documentation**.
> These stubs are mostly `TBD`; treat as evidence remediation is underway, not as finished structure.

### How to fix (structure-first, numbers-last)

1. **Adopt subtasks-as-ground-truth** (per [`TASK_ANALYSIS_AND_GOTCHAS.md`](TASK_ANALYSIS_AND_GOTCHAS.md)): rewrite parents to match subtask reality, not the reverse.
2. **Re-derive the dependency graph from semantics**, not from the degenerate declared edges. Encode the four clusters above (validation layering, backup/safety, core pipeline, orchestration) as actual `Dependencies`.
3. **Reconnect orphans**: wire 002→001/007, 001→009/010/012, and the 003→008→011→017 chain.
4. **Collapse the fake tail**: mark 019–025 as parallel post-MVP infrastructure (not a chain) and deflate their effort estimates. (The 2026-06-10 commit deleting duplicate tasks 026–028 already started this trimming.)
5. **Fix the known corruptions**: 008 renumber 9.x→8.x; 009 cross-refs off-by-one; 015 strip 27.x + decide validation-vs-orchestration; move 007.1–.3 to 005.
6. **Restore lost technical specs** from `archive/task_data_historical/archived/handoff_archive_task002/` into the 002 subtasks.
7. **Sync once, structurally**: edit markdown → `python taskmaster_cli.py parse-prd --input tasks/` so the graph is captured consistently; keep `tasks.json` empty otherwise.
8. **Publish one canonical structure doc** (this file) and supersede the stale maps so the corrected graph doesn't drift again.

### Recent recommendation docs to ingest (beyond the gotchas)

| Doc | Date | What to take from it | Caveat |
|-----|------|----------------------|--------|
| [`docs/ORACLE_RECOMMENDATION_TODO.md`](docs/ORACLE_RECOMMENDATION_TODO.md) | 2026-02 | **The primary remediation TODO** — scope bloat (14–20x oversize), dependency corruption (005.*→002.*), product drift, lost Task-75 specs | Contains a **rejected** EmailIntelligence pivot — ingest its *structural/scope* findings only, ignore the pivot |
| [`TASK_ANALYSIS_AND_GOTCHAS.md`](TASK_ANALYSIS_AND_GOTCHAS.md) | 2026-06-11 | Most recent synthesis; subtask-intent inversion + 8-step remediation order | Canonical — already ingested |
| [`docs/task_004_tuned_recommendations.md`](docs/task_004_tuned_recommendations.md) | 2026-03-13 | Repo-analysis-based recommendations for the core framework (004) | Task-004 specific |
| [`guidance/ARCHITECTURE_ALIGNMENT_COMPLETE_AND_RECOMMENDATIONS.md`](guidance/ARCHITECTURE_ALIGNMENT_COMPLETE_AND_RECOMMENDATIONS.md) | — | Architecture-level alignment recommendations | Cross-check against current tasks |
| [`docs/research/2025-11-28_create-a-detailed-summary-of-which-tasks-are-inten.md`](docs/research/2025-11-28_create-a-detailed-summary-of-which-tasks-are-inten.md) | 2025-11 | Captures **pre-corruption intent** (predecessor/successor relationships) | Uses old numbering — read for *intent*, not IDs |

---

## 5d. Pre-merge vs Post-merge & Post-MVP Disposition — DECISION RECORD

> **Status: decision record only (2026-06-13).** This section records the *intended* dispositions that the structure-first remediation (§5c "How to fix") should execute. **No canonical `task_NNN.md` dependency fields have been changed by this record.** Applying it is a separate, backup-gated work session (run `python scripts/task_metadata_manager.py backup --all` first).

### Change-pipeline tiers (priority order, by blast radius)

| Tier | Scope | Mutates flow? | Status |
|------|-------|---------------|--------|
| **0** | Doc-hygiene: count/date fixes in this map | No | ✅ this commit |
| **1** | This decision record (§5d) | No | ✅ this commit |
| **2** | Canonical `task_*.md` remediation (§5c steps) | **Yes** | ⛔ deferred — backup-gated |
| **3** | `parse-prd` sync + supersede stale maps | regenerates `tasks.json` | ⛔ after Tier 2 |

### Tasks mislabeled "tail" that hold pre-merge gate logic → integrate into the pre-merge workflow (Tier 2, step 2c)

Canonical runtime flow: *identify 007 → backup 006 → align 009/010 → error-check 005 → validate 011 → document*. These three tasks each declare **"Blocks: Task 010"** in their own files — evidence they were meant to run *before* the merge, not as a post-merge tail:

| Task | Pre-merge piece | Target slot |
|------|-----------------|-------------|
| **016 Rollback & Recovery** | verified restore-point + rollback capability before align runs | merge into **backup stage (006)** |
| **017 Validation Integration** | orchestrates error-detection + pre-merge + comprehensive validation *during* alignment | fold into **validate stage (003→008→011)** |
| **018 E2E Testing** | test *execution* must pass before merge lands | new **pre-merge test gate**; keep reporting post-merge |

Resulting pre-merge chain: **007 → 006+016 → 009/010 → 005 → 011+017 → 018(test) → 020(changelog)**, orchestrated by 012.

### Post-MVP / post-merge disposition for 019–025 (Tier 2, step 2d — collapse the fake tail)

| Task | Disposition | Rationale |
|------|-------------|-----------|
| **019 Deployment & Release** | post-merge; deflate from `High` | only relevant once a shippable artifact exists |
| **020 Documentation & Knowledge** | **split**: changelog/PR-summary → pre-merge; KB/training → post-merge | runtime flow's "document" step is pre-merge |
| **021 Maintenance & Monitoring** | **split**: health/diagnostic probe → optional pre-merge; scheduling/alerting → post-merge | readiness check vs ongoing ops |
| **022 Improvements & Enhancements** | post-merge **except** `012.15` `backend→src/backend` migration (a real core dependency) | keep migration; deflate framework bloat |
| **023 Optimization & Perf Tuning** | defer | premature optimization of an unbuilt pipeline |
| **024 Future Dev & Roadmap** | **park** | meta-planning; not merge-completion |
| **025 Scaling & Advanced Features** | **park** | large-repo/parallel/enterprise = post-production scale |

**Cleanup also required:** 024 "Blocks 026" and 025 "Blocks 026/027" are **dangling** — tasks 026–028 were deleted as duplicates (commit `7eaccfdd`). Drop these block-references during step 2d. Several tail tasks (023/024/025) also have malformed Success-Criteria blocks (prerequisites spliced into the checklist) to repair when deflating.

---

## 6. Scope Note

`.taskmaster/` contains **615 markdown files**. This map enumerates the **active** root, `docs/`, `guidance/`, `reports/`, and `tasks/` documentation individually, and summarises the **184 archived** files by initiative (Section 4) rather than line-by-line, since they are explicitly historical (`archive/README.md`) and not canonical.
