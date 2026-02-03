**Status**: PENDING EXECUTION  
**Severity**: CRITICAL - Scope bloat + dependency corruption blocking development  
**Target Timeline**: 2-4 weeks (single developer)  
**Created**: 2026-01-29
**Updated**: 2026-02-03

---

## ⛔ CRITICAL WARNING FOR AGENTS

> **THIS DOCUMENT CONTAINS HISTORICAL PROPOSALS THAT WERE REJECTED.**
>
> **THIS PIVOT WAS NOT EXECUTED.**
>
> | Fact | Value |
> |------|-------|
> | **Canonical Project** | Branch Alignment Tooling |
> | **Authoritative Guide** | [PROJECT_IDENTITY.md](PROJECT_IDENTITY.md) |
> | **Tasks 002-004** | Branch clustering/validation/framework |
>
> **DO NOT**: Rewrite alignment tasks outside branch alignment scope
> **DO**: Restore alignment-focused specs, maintain project separation

---

## Executive Summary

**Current State**: Canonical `tasks/` cleaned; backups centralized; alignment tasks restored and augmented with archives
**Target State**: Alignment-focused canonical task set under `tasks/` with full 14-section compliance
**Action**: Preserve alignment scope in `tasks/`; keep any MVP pivots in `tasks/mvp/` only

**🔴 CRITICAL ARCHITECTURAL CHANGE**:
- **Task .md files** are the **canonical source** of task information
- **tasks.json** is ONLY for **perfect fidelity round-trip testing**
- **tasks.json should be EMPTY** - not the source of truth
- **All task specifications** (formulas, schemas, test cases) must be in .md files

**Root Cause**: Tasks drifted from alignment scope into generic tooling bloat
- 26 tasks mention validation (duplication)
- 10 tasks mention rollback (enterprise feature bloat)
- 90%+ effort on CI/CD orchestration, scaling, multi-team infrastructure

**🔴 CRITICAL ISSUES IDENTIFIED**:
1. **Task 75 technical specs NOT preserved in Task 002** (metric formulas, schemas, test cases lost)
2. **Task 003/004 missing from canonical `tasks/`** (only backups exist)
3. **Dependency references wrong** (005.* instead of 002.* in task-002 subtasks)
4. **Missing subtasks** for tasks 005-007, 012-025

---

## Critical Issues to Address

### 1. 🔴 Task 75 Technical Specs NOT Preserved (BLOCKING)
**Affected**: Task 002 (should contain Task 75 content)
- **Problem**: Old Task 75 files (task-75.1.md through task-75.9.md) were deleted
- **Missing**: Exact metric formulas, weighting schemes, input/output schemas
- **Missing**: Git command references, clustering parameters, tagging system
- **Missing**: Detailed test cases from HANDOFF_75.8
- **Impact**: Cannot implement Task 002 without these technical specifications
- **Location**: Archived in `.taskmaster/task_data/archived/handoff_archive_task75/`
- **Action Required**: Restore all technical specs to task-002.1-002.9

### 2. 🔴 Task 003/004 Missing from Canonical Tasks
**Affected**: `.taskmaster/tasks/`
- **Problem**: Task 003 and 004 only exist in backup/working directories
- **Impact**: Canonical task set is incomplete; cannot execute planned epics
- **Action Required**: Restore task 003/004 (and subtasks) into `tasks/` using the 14-section standard

### 3. 🔴 Dependency References Wrong (BLOCKING)
**Affected**: task-002.1-002.9 subtasks
- **Problem**: Dependencies reference 005.* instead of 002.*
- **Example**: task-002.4 has "Dependencies: 005.1, 005.2, 005.3"
- **Should Be**: "Dependencies: 002.1, 002.2, 002.3"
- **Impact**: Incorrect dependency chain, blocks task expansion
- **Action Required**: Fix all 005.* → 002.* references

### 4. 🔴 Missing Subtasks (BLOCKING)
**Affected**: Tasks 005-007, 012-025
- **Problem**: Tasks 005-007 had subtasks (005-1 to 005-3, etc.) that were deleted
- **Problem**: Tasks 012-025 have no subtasks at all
- **Impact**: Tasks are too large (>2 days), violate single-dev discipline
- **Action Required**: Create missing subtasks following 14-section standard

### 5. Architecture Confusion: tasks.json vs .md Files
**Affected**: All task management operations
- **Problem**: Current approach treats tasks.json as source of truth
- **Required**: Task .md files are the canonical source
- **Required**: tasks.json should be empty, used only for round-trip testing
- **Action Required**: Confirm tasks.json remains empty and document .md as authoritative

### 6. Massive Scope (BLOCKER)
**Affected**: All 28 tasks
- 2327-3179 total hours
- Single developer realistic capacity: ~8 hours/day × 5 days × 4 weeks = 160 hours
- Current scope: **14.6x to 20x oversize**
- **Impact**: Project will never complete; morale destruction

### 7. Product Drift (STRATEGIC)
**Affected**: Tasks 005-028 (24 tasks)
- Feature examples: orchestration, scaling, multi-team RBAC, rollback systems
- Should be separate project or Phase 2+
- **Impact**: Building wrong product while correct one gets neglected

---

## Scope Notes

Do not recreate historical pivot content in this file. Alignment scope only.

---

## Implementation Priorities

### Phase 1: Fix Task Structure & Preserve Technical Specs (THIS WEEK)
- [x] **CRITICAL**: Task .md files are the canonical source (not tasks.json)
- [x] Cleaned `tasks/` of backup artifacts; centralized backups under `backups/`
- [x] Incremental augmentation completed using richest archive sources (additive only; no replacement)
- [x] Appended missing sections from secondary archives (improved/restructured/migration backups)
- [x] Third-pass archive import completed (Task 002 migration/quick-start archives)
- [x] Restore Task 75 technical specs to Task 002 subtasks (002.1-002.9):
  - Add metric formulas from HANDOFF_75.1-75.3 (commit_recency, commit_frequency, etc.)
  - Add input/output JSON schemas from all HANDOFF_75 files
  - Add clustering parameters from HANDOFF_75.4 (Ward's method, threshold 0.5)
  - Add tagging system from HANDOFF_75.5 (30+ tags by category)
  - Add test cases from HANDOFF_75.8
- [x] Restore canonical Task 003/004 files into `tasks/` with 14-section standard
- [x] Fix dependency references: Change 005.* → 002.* in task-002 subtasks (verified: no 005.* refs in task_002.*)
- [x] Create missing subtasks for tasks 005-007, 012-025 (where available in archives)
- [x] Create placeholder subtasks for tasks 026-028 (derived from main task subtask breakdown)
- [x] Ensure all tasks follow 14-section standard

---

## Decision Log (Next Set for Completion)

### 2026-02-02
- **Augmentation Source Priority**: Use `enhanced_improved_tasks/` as the richest source for incremental imports, then fall back to other archives if missing.
- **Merge Rule**: Additive-only append under existing sections (no replacements); provenance tracked with `<!-- IMPORTED_FROM: ... -->` markers.
- **Placement Rule**: Imported content is appended under `## Implementation Guide` to avoid disrupting existing section order.
- **Canonical Naming**: Keep underscore naming (`task_XXX.md`, `task_XXX.Y.md`) for canonical tasks.
- **Marker Retention**: Keep `IMPORTED_FROM` markers until the final audit/cleanup pass.
- **Secondary Archive Pass**: Allow imports from `task_data/migration_backup_20260129/current_tasks/`, `improved_tasks/`, and `restructured_tasks_14_section/` after `enhanced_improved_tasks/`.
- **Third-Pass Archives**: Include `task_data/archived/backups_archive_task75/`, `task_data/archived/handoff_archive_task75/`, `archive/task_context/`, `archive/project_docs/`, `archive/phase_planning/` for any remaining sections.

### Phase 2: Empty tasks.json for Round-Trip Testing (THIS WEEK)
- [x] **CRITICAL**: tasks.json is ONLY for perfect fidelity round-trip testing
- [x] tasks.json remains empty array `[]`
- [ ] Create round-trip test: .md → tasks.json → .md → verify identical
- [ ] Document round-trip fidelity requirements (100% field preservation)
- [ ] Test with sample tasks to ensure no data loss
- [ ] Do NOT use tasks.json as source of truth

### Phase 3: Eliminate Out-of-Scope Work (THIS WEEK)
- [ ] Create decision document: Keep Tasks 005-028 or move to separate project?
- [ ] If moving: Create `emailintelligence-ops` repo skeleton
- [ ] If archiving: Move to `.taskmaster/archive/` with metadata
- [ ] Keep Task 75 archived specs for reference
- [ ] Update documentation to reflect .md as canonical source

### Phase 4: Preserve Alignment Scope (COMPLETED)
- [x] Confirm `tasks/` remains alignment-only and MVP work stays in `tasks/mvp/`
- [x] Created PROJECT_IDENTITY.md as canonical project identity reference
- [x] Added agent warning block to ORACLE_RECOMMENDATION_TODO.md
- [x] Added project identity header to CLAUDE.md
- [x] Moved Epic A/B/C definitions to tasks/mvp/EPIC_DEFINITIONS.md

### Phase 5: Define Single-Dev Discipline (NEXT WEEK)
- [ ] Document: Task .md files are the canonical source of truth
- [ ] Document Definition of Done (DoD) for all tasks:
  - Must have complete technical specs (formulas, schemas, test cases)
  - Must have tests OR fixtures
  - Must be idempotent (where relevant)
  - Must have logging
  - Must have "how to run" documentation
- [ ] Document dependency rules (max 3 deps per task, no cycles)
- [ ] Document task sizing rules (max 2 days per task)
- [ ] Document round-trip fidelity requirements for tasks.json testing

---

## Success Criteria

### For Task Structure & Technical Specs Preservation
- [ ] Task .md files are the canonical source of all task information
- [ ] Task 75 technical specs fully preserved in Task 002 subtasks:
  - Metric formulas (commit_recency, commit_frequency, authorship_diversity, etc.)
  - Weighting schemes (25%, 20%, 20%, 20%, 15%)
  - Input/output JSON schemas (complete field specifications)
  - Git command references (exact commands for data extraction)
  - Clustering parameters (Ward's method, threshold 0.5, quality metrics)
  - Tagging system (30+ tags organized by category)
  - Detailed test cases (from HANDOFF_75.8)
- [ ] task-021.md deleted (does not exist)
- [ ] Dependency references fixed (005.* → 002.*)
- [ ] All tasks follow 14-section standard

### For tasks.json Round-Trip Testing
- [x] tasks.json is empty array `[]` (not source of truth)
- [ ] Round-trip test passes: .md → tasks.json → .md → 100% identical
- [ ] No data loss during .md → tasks.json conversion
- [ ] No field corruption during round-trip
- [ ] Documented as testing tool only

### For Scope Preservation
- [x] Alignment tasks remain intact in `tasks/`
- [x] MVP tasks remain isolated in `tasks/mvp/`
- [x] PROJECT_IDENTITY.md created as authoritative reference
- [x] Agent warnings added to prevent conflation

### For Quality
- [ ] All tasks have complete technical specs (no generic descriptions)
- [ ] All epic tasks have subtasks (no task >2 days)
- [ ] All dependencies are within epic OR justified with cross-epic link
- [ ] README clearly states MVP scope + Phase 2 boundary
- [ ] Task .md files are the authoritative source

---

## Risk Mitigations

### Risk: Task 75 Technical Specs Lost During Migration
**Mitigation**:
- ✅ **IDENTIFIED**: Task 75 specs are in archives but NOT integrated into Task 002
- **Action**: Restore all technical specs from HANDOFF_75.1-75.9 to Task 002 subtasks
- **Priority**: HIGH - This is blocking accurate implementation
- **Location of archived specs**: `.taskmaster/task_data/archived/handoff_archive_task75/`
- **Verification**: Task 002.1-002.9 have exact metric formulas, schemas, test cases

### Risk: Canonical Task Set Missing 003/004
**Mitigation**:
- ✅ **IDENTIFIED**: Task 003/004 only exist in backup/working directories
- **Action**: Restore into `tasks/` and normalize to 14-section standard
- **Reason**: Canonical alignment task set must be complete

### Risk: Dependency References Wrong (005→002)
**Mitigation**:
- ✅ **IDENTIFIED**: Current task-002 subtasks reference 005.* dependencies
- **Action**: Fix all 005.* → 002.* in task-002.1-002.9
- **Impact**: Blocks correct task dependency chain
- **Priority**: HIGH

### Risk: tasks.json Used as Source of Truth
**Mitigation**:
- ✅ **IDENTIFIED**: Current approach uses tasks.json as main source
- **Action**: Change architecture - .md files are canonical source
- **Action**: Empty tasks.json to `[]` for round-trip testing only
- **Documentation**: Update all references to .md as authoritative

### Risk: MVP Content Leaks Into Alignment Tasks
**Mitigation**:
- Keep MVP documentation in `tasks/mvp/` only
- Do not rewrite alignment tasks as MVP epics

### Risk: Core 002-004 Tasks Use Generic Descriptions
**Mitigation**:
- **Verified**: Current Task 002 had generic descriptions, missing technical specs
- **Action**: Restore exact technical specs from archived Task 75 files
- **Don't**: Introduce MVP scope into alignment tasks
- **Do**: Preserve alignment-specific formulas, weights, schemas

---

## Backups & Safe Harbor

**Location**: `.taskmaster/backups/task_markdown_backups/`
- Centralized task markdown backups (deduplicated from `tasks/`)
**Additional**: `.taskmaster/tasks/option_c_backup/` (if present)

**Git**: Option C commit hash (record for revert if needed)

---

## Next Actions

1. **Read this document in full → sign off on MVP scope** (1 hour)
2. **Restore Task 75 technical specs to Task 002** (CRITICAL - 2-3 hours):
   - Copy metric formulas from HANDOFF_75.1-75.3 to task-002.1-002.3
   - Copy schemas from all HANDOFF_75 files to task-002 subtasks
   - Copy clustering parameters from HANDOFF_75.4 to task-002.4
   - Copy tagging system from HANDOFF_75.5 to task-002.5
   - Copy test cases from HANDOFF_75.8 to task-002.8
3. **Restore canonical Task 003/004** (1-2 hours)
4. **Fix dependency references** (1 hour):
   - Change all 005.* → 002.* in task-002.1-002.9
   - Validate dependency chains
5. **Empty tasks.json for round-trip testing** (30 mins):
   - Set tasks.json to `[]`
   - Create round-trip test script
6. **Create decision document for Tasks 005-028** (1 hour)
7. **Validate task structure** (1 hour):
   - All tasks follow 14-section standard
   - All subtasks have complete technical specs
   - .md files are canonical source

**Total pre-development work**: ~8-10 hours (1-2 days)  
**Then**: 2-4 weeks building actual product

---

## 📋 Task 75 Technical Specs - Restoration Checklist

### Location: `.taskmaster/task_data/archived/handoff_archive_task75/`

### Task 75.1: CommitHistoryAnalyzer → task-002.1
**File:** `HANDOFF_75.1_CommitHistoryAnalyzer.md` (140 lines)

**Required Specs to Restore:**
- [ ] Metric formulas:
  - `commit_recency`: exp(-days_since_last_commit / 30)
  - `commit_frequency`: min(1.0, commits_per_week / 5.0)
  - `authorship_diversity`: 1.0 - (unique_authors / total_commits)
  - `merge_readiness`: based on conflict history
  - `stability_score`: inverse of commit churn
- [ ] Weighting scheme: 25%, 20%, 20%, 20%, 15%
- [ ] Input specification: branch_name (str), repo_path (str)
- [ ] Output schema: Complete JSON format with all fields
- [ ] Git command references:
  - `git log main..BRANCH_NAME --pretty=format:"%H|%ai|%an|%s"`
  - `git log main..BRANCH_NAME --pretty=format:"%H" | xargs -I {} git diff main...{} --stat`
  - `git merge-base main BRANCH_NAME`
- [ ] Test cases: Edge cases (0 commits, single commit, new branches)

### Task 75.2: CodebaseStructureAnalyzer → task-002.2
**File:** `HANDOFF_75.2_CodebaseStructureAnalyzer.md`

**Required Specs to Restore:**
- [ ] Metric formulas:
  - `directory_similarity`: Jaccard similarity of directory paths
  - `file_additions`: normalized count of new files
  - `core_module_stability`: based on changes to critical directories
  - `namespace_isolation`: based on module import patterns
- [ ] Weighting scheme: 30%, 25%, 25%, 20%
- [ ] Input/Output schemas
- [ ] Git command references for file analysis

### Task 75.3: DiffDistanceCalculator → task-002.3
**File:** `HANDOFF_75.3_DiffDistanceCalculator.md`

**Required Specs to Restore:**
- [ ] Metric formulas:
  - `code_churn`: lines added + deleted / total lines
  - `change_concentration`: entropy of file changes
  - `diff_complexity`: based on diff size and complexity
  - `integration_risk`: pattern-based risk scoring
- [ ] Weighting scheme: 25%, 25%, 25%, 25%
- [ ] Input/Output schemas
- [ ] Git command references for diff extraction

### Task 75.4: BranchClusterer → task-002.4
**File:** `HANDOFF_75.4_BranchClusterer.md` (257 lines)

**Required Specs to Restore:**
- [ ] Clustering algorithm: Hierarchical agglomerative clustering (Ward's method)
- [ ] Weighted formula: 35% commit history + 35% codebase + 30% diff distance
- [ ] Threshold: 0.5 (configurable)
- [ ] Quality metrics:
  - Silhouette score
  - Davies-Bouldin index
  - Calinski-Harabasz index
- [ ] Input schema: Complete analyzer outputs format
- [ ] Output schema: Complete clustering results format
- [ ] Cluster center calculation method

### Task 75.5: IntegrationTargetAssigner → task-002.5
**File:** `HANDOFF_75.5_IntegrationTargetAssigner.md` (343 lines)

**Required Specs to Restore:**
- [ ] Four-level decision hierarchy for target assignment
- [ ] 30+ descriptive tags per branch:
  - scope: core-feature, minor-feature, experiment, ...
  - risk_level: low-risk, medium-risk, high-risk, ...
  - complexity: simple, moderate, complex, ...
  - validation: testing-required-high, testing-required-medium, ...
- [ ] Tag catalog by category
- [ ] Integration target assignment logic
- [ ] Input schema: Cluster data from Task 75.4
- [ ] Output schema: Categorized branches with tags

### Task 75.6-75.9: Additional Components
**Files:** PipelineIntegration, VisualizationReporting, TestingSuite, FrameworkIntegration

**Required Specs to Restore:**
- [ ] Pipeline integration architecture
- [ ] Visualization and reporting formats
- [ ] Test suite specifications
- [ ] Framework integration requirements

---

## Documentation References

**Canonical Source:**
- Task .md files in `.taskmaster/tasks/` are the authoritative source
- All task specifications, formulas, schemas, test cases must be in .md files

**Archived References:**
- Task 75 specs: `.taskmaster/task_data/archived/handoff_archive_task75/`
- Task 75 backups: `.taskmaster/task_data/archived/backups_archive_task75/`

**Analysis Documents:**
- `TASK_RESTRUCTURING_ANALYSIS_REPORT.md` - Restructuring analysis
- `PLACEHOLDER_BACKUP_MAPPING.md` - Backup mapping
- `DEPENDENCY_CORRUPTION_FIX_PLAN.md` - Dependency fix plan
- `TASK_STRUCTURE_STANDARD.md` - 14-section standard

**Deprecated:**
- `OLD_TASK_NUMBERING_DEPRECATED.md` - Deprecation notice
- `guidance/TASK_NUMBERING_ANALYSIS.md` - Renumbering analysis

---

**Recommended**: Start with Task 75 technical specs restoration (Phase 1, Step 2).

---

## Alignment Task Migration & Restructuring Guides (Reference Only)

- `TASK_STRUCTURE_STANDARD.md` - Required 14-section task format
- `SUBTASK_MARKDOWN_TEMPLATE.md` - Full subtask template and section order
- `guidance/SUBTASK_EXPANSION_TEMPLATE.md` - Parent task expansion guide
- `TASK_EXPANSION_PLAN_BY_WEEK.md` - Weekly expansion and verification checks
- `MIGRATION_STATUS_ANALYSIS.md` - Current migration gaps and consistency issues
- `DEPENDENCY_CORRUPTION_FIX_PLAN.md` - Dependency repair plan for renumbering
- `OLD_TASK_NUMBERING_DEPRECATED.md` - Deprecated numbering notice
- `guidance/TASK_NUMBERING_ANALYSIS.md` - Renumbering analysis
