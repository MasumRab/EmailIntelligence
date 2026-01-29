# Oracle Recommendation TODO - EmailIntelligence MVP Refactoring

**Status**: PENDING EXECUTION  
**Severity**: CRITICAL - Scope bloat + dependency corruption blocking development  
**Target Timeline**: 2-4 weeks (single developer)  
**Created**: 2026-01-29

---

## Executive Summary

**Current State**: 28 tasks, 2327-3179 hours (58-79 weeks), 25/28 with corrupted dependencies
**Target State**: 12-15 high-quality MVP tasks, 84-168 hours (2-4 weeks), email intelligence focused
**Action**: Hard cut Tasks 005-028 (git/branch alignment tooling), reframe 002-004 as product epics

**🔴 CRITICAL ARCHITECTURAL CHANGE**:
- **Task .md files** are the **canonical source** of task information
- **tasks.json** is ONLY for **perfect fidelity round-trip testing**
- **tasks.json should be EMPTY** - not the source of truth
- **All task specifications** (formulas, schemas, test cases) must be in .md files

**Root Cause**: Tasks drifted from EmailIntelligence to generic git branch management tooling
- Only 8 "email" references in 28 tasks
- 26 tasks mention validation (duplication)
- 10 tasks mention rollback (enterprise feature bloat)
- 90%+ effort on CI/CD orchestration, scaling, multi-team infrastructure

**🔴 CRITICAL ISSUES IDENTIFIED**:
1. **Task 75 technical specs NOT preserved in Task 002** (metric formulas, schemas, test cases lost)
2. **task-021.md exists** (should be deleted per OLD_TASK_NUMBERING_DEPRECATED.md)
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

### 2. 🔴 Task 021 Exists (Should Be Deleted)
**Affected**: `.taskmaster/tasks/task-021.md`
- **Problem**: task-021.md exists but violates OLD_TASK_NUMBERING_DEPRECATED.md
- **Expected**: Should have been renamed to task-002.md or deleted
- **Current Content**: "E2E Testing and Reporting"
- **Conflict**: Both task-002.md and task-021.md exist with different content
- **Action Required**: Delete task-021.md immediately

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
- **Action Required**: Empty tasks.json to `[]`, document .md as authoritative

### 6. Massive Scope (BLOCKER)
**Affected**: All 28 tasks
- 2327-3179 total hours
- Single developer realistic capacity: ~8 hours/day × 5 days × 4 weeks = 160 hours
- Current scope: **14.6x to 20x oversize**
- **Impact**: Project will never complete; morale destruction

### 7. Product Drift (STRATEGIC)
**Affected**: Tasks 005-028 (24 tasks)
- These are git branch alignment tooling, not email intelligence
- Feature examples: orchestration, scaling, multi-team RBAC, rollback systems
- Should be separate project or Phase 2+
- **Impact**: Building wrong product while correct one gets neglected

---

## CORE MVP TODO: What to Keep vs Eliminate

### ✅ KEEP: Reframe as Product Epics (2-4 weeks)
- **Task 002** → Epic A: Email Ingest + Normalize
- **Task 003** → Epic B: Intelligence Analysis + Clustering
- **Task 004** → Epic C: Presentation + Search UI

### ❌ ELIMINATE: Move Out of Scope (save 90%+ effort)
- **Tasks 005-028** (24 tasks): All git/branch alignment tooling
  - Delete from this project or create separate `emailintelligence-ops` repo
  - Keep backups in `.taskmaster/tasks/option_c_backup/`
  - Decision point: Spin out or archive?

---

## MVP Feature Definition (What "Done" Means)

### Input
One mailbox source (Gmail API OR IMAP):
- Incremental sync with cursor/UID tracking
- Handle HTML + text bodies
- Extract headers, threading metadata

### Processing (3-5 signals only)
1. **Threading**: Reconstruct conversations (Message-ID / In-Reply-To / References)
2. **Entity Extraction**: Participants, domains, subject normalization
3. **Classification**: "action required", "FYI", "spam/marketing" (heuristic rules OK)
4. **Basic Clustering** (optional Week 4): Sender/org/topic grouping
5. **Lightweight Summary**: Per-thread summary (rule-based)

### Output
- **Storage**: SQLite/Postgres (minimal schema: emails, threads, labels, results)
- **UI Surface**: Local web view or CLI (list threads, view details, search by sender/subject/tag)
- **Quality**: Parser tests, pipeline idempotency tests, golden fixtures

---

## Proposed Epic Structure (15 tasks, 0.5-2 days each)

### Epic A: Ingest + Normalize (Week 1-2)
- **A1** (0.5d): Mailbox source selection + API/IMAP setup
- **A2** (1.5d): Robust email parser (headers, bodies, threading headers)
- **A3** (1d): Persistence layer (schema + migrations)
- **A4** (0.5d): CLI for sync + inspect (debugging surface)

### Epic B: Intelligence (Week 2-3)
- **B1** (1d): Thread reconstruction + conversation view
- **B2** (1.5d): Signal extraction (participants, orgs, action classification)
- **B3** (1d): Idempotent reprocessing + result storage
- **B4** (0.5d): Search/filter API (sender, domain, tags, action-required)

### Epic C: Present + Polish (Week 3-4)
- **C1** (1d): Web UI or TUI (thread list + details)
- **C2** (0.5d): Structured logging + error reporting
- **C3** (1.5d): Tests (parser, pipeline idempotency, sync regressions)
- **C4** (0.5d): Packaging + README (single "run locally" command)

**Total**: 15 tasks, ~10 days at realistic velocity = 2 weeks development + 1-2 weeks for iteration

---

## Implementation Priorities

### Phase 1: Fix Task Structure & Preserve Technical Specs (THIS WEEK)
- [ ] **CRITICAL**: Task .md files are the canonical source (not tasks.json)
- [ ] Restore Task 75 technical specs to Task 002 subtasks (002.1-002.9):
  - Add metric formulas from HANDOFF_75.1-75.3 (commit_recency, commit_frequency, etc.)
  - Add input/output JSON schemas from all HANDOFF_75 files
  - Add clustering parameters from HANDOFF_75.4 (Ward's method, threshold 0.5)
  - Add tagging system from HANDOFF_75.5 (30+ tags by category)
  - Add test cases from HANDOFF_75.8
- [ ] Delete task-021.md (should not exist per OLD_TASK_NUMBERING_DEPRECATED.md)
- [ ] Fix dependency references: Change 005.* → 002.* in task-002 subtasks
- [ ] Create missing subtasks for tasks 005-007, 012-025
- [ ] Ensure all tasks follow 14-section standard

### Phase 2: Empty tasks.json for Round-Trip Testing (THIS WEEK)
- [ ] **CRITICAL**: tasks.json is ONLY for perfect fidelity round-trip testing
- [ ] Clear tasks.json to empty array `[]`
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

### Phase 4: Reframe Core Tasks as Product Epics (NEXT WEEK)
- [ ] **Focus**: EmailIntelligence MVP, not git/branch alignment
- [ ] Rewrite Task 002 as Epic A: Email Ingest + Normalize (4 subtasks)
- [ ] Rewrite Task 003 as Epic B: Intelligence Analysis (4 subtasks)
- [ ] Rewrite Task 004 as Epic C: Presentation + Search UI (4 subtasks)
- [ ] Validate all subtasks have complete technical specs
- [ ] Ensure total effort: 84-168 hours (2-4 weeks realistic)

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
- [ ] tasks.json is empty array `[]` (not source of truth)
- [ ] Round-trip test passes: .md → tasks.json → .md → 100% identical
- [ ] No data loss during .md → tasks.json conversion
- [ ] No field corruption during round-trip
- [ ] Documented as testing tool only

### For Scope Reduction
- [ ] Tasks 005-028 removed or moved to separate project
- [ ] Total effort estimate: 84-168 hours (2-4 weeks, not 2327+ hours)
- [ ] Product focus restored: "email" mentioned in all remaining tasks
- [ ] Git/branch alignment moved to separate project or archived

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

### Risk: task-021.md Exists (Should Be Deleted)
**Mitigation**:
- ✅ **IDENTIFIED**: task-021.md exists but violates OLD_TASK_NUMBERING_DEPRECATED.md
- **Action**: Delete task-021.md immediately
- **Reason**: Task 021 was intermediate numbering, should have been Task 002
- **Conflict**: Both task-002.md and task-021.md exist with different content

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

### Risk: MVP Still Too Large (15 tasks > 2-4 weeks)
**Mitigation**:
- If A/B/C epics still >20 hours each, cut to single mailbox source
- Defer clustering (B3) to Week 4 or Phase 2
- Use heuristic rules instead of ML for classification
- Cut "nice to have" features (C2 logging can be minimal)

### Risk: Core 002-004 Tasks Use Generic Descriptions
**Mitigation**:
- **Verified**: Current Task 002 has generic descriptions, missing technical specs
- **Action**: Restore exact technical specs from archived Task 75 files
- **Don't**: Copy-paste old definitions without verification
- **Do**: Rewrite with complete metric formulas, weights, schemas

---

## Backups & Safe Harbor

**Location**: `.taskmaster/tasks/option_c_backup/`
- Full copy of all 28 tasks before cutting Tasks 005-028
- Dated snapshot: 2026-01-29
- Use if pivoting back: `cp option_c_backup/task-*.md .`

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
3. **Delete task-021.md** (30 mins)
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
