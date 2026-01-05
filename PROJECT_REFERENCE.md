# Branch Alignment Project - Single Reference Document

**Created:** 2026-01-04  
**Status:** Active Development  
**Purpose:** Consolidated reference for all project goals, tasks, and documentation

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Goals & Objectives](#2-goals--objectives)
3. [Current System Structure](#3-current-system-structure)
4. [Key Issues Identified](#4-key-issues-identified)
5. [Logging System Design](#5-logging-system-design)
6. [Task Files Overview](#6-task-files-overview)
7. [Documentation Structure](#7-documentation-structure)
8. [Implementation Roadmap](#8-implementation-roadmap)
9. [Validation & Testing](#9-validation--testing)
10. [Next Steps](#10-next-steps)

---

## 1. Project Overview

### What This Project Does

The Branch Alignment Project establishes a comprehensive framework for aligning feature branches with their target primary branches (main, scientific, orchestration-tools) using a systematic 6-phase approach.

### Key Components

| Component | Description | Location |
|-----------|-------------|----------|
| **Task Files** | 20 task files defining the alignment workflow | `new_task_plan/task_files/` |
| **TOML Plan** | 6-phase structured task plan | `tasks/archive/toml_task_plan.md` |
| **Logging System** | Hybrid markdown + JSON logging for findings | `task_data/findings/` |
| **Documentation** | Comprehensive guides and references | `new_task_plan/*.md` |

### Current State

- **20 task files** created (001-020)
- **6-phase structure** defined in TOML
- **Logging infrastructure** partially implemented
- **Documentation** needs synchronization

---

## 2. Goals & Objectives

### Primary Goals

| Goal | Priority | Status |
|------|----------|--------|
| Create task progress logging system | Critical | In Progress |
| Track parameters, decisions, outcomes | Critical | Pending |
| Fix documentation inconsistencies | High | Pending |
| Align TOML and new_task_plan structures | High | Pending |
| Enable future task speedups | Medium | Planned |

### Specific Objectives

1. **Capture Findings**
   - Record parameters at each checkpoint
   - Document decisions and rationale
   - Track outcomes and metrics
   - Enable pattern identification

2. **Enable Speedups**
   - Document what worked/didn't work
   - Provide reference for similar future tasks
   - Track performance metrics

3. **Maintain Consistency**
   - Align TOML (6-phase) and new_task_plan (4-initiative) structures
   - Synchronize documentation
   - Fix broken references

---

## 3. Current System Structure

### new_task_plan Directory Structure

```
new_task_plan/
├── task_files/              # 20 task files (001-020)
│   ├── task-001.md         # Framework Strategy Definition
│   ├── task-002.md         # Create Comprehensive Merge Validation Framework
│   ├── task-003.md         # Develop Pre-merge Validation Scripts
│   ├── task-004.md         # Establish Core Branch Alignment Framework
│   ├── task-005.md         # Develop Automated Error Detection Scripts
│   ├── task-006.md         # Implement Branch Backup and Restore Mechanism
│   ├── task-007.md         # Develop Feature Branch Identification Tool
│   ├── task-008.md         # Automate Changes Summary and Checklist Generation
│   ├── task-009.md         # Create Post-Alignment File Resolution List
│   ├── task-010.md         # Develop Core Primary-to-Feature Alignment Logic
│   ├── task-011.md         # Implement Strategies for Complex Branches
│   ├── task-012.md         # Integrate Validation into Alignment Workflow
│   ├── task-013.md         # Orchestrate Branch Alignment Workflow
│   ├── task-014.md         # Establish End-to-End Testing for Framework
│   ├── task-015.md         # Finalize and Publish Documentation
│   ├── task-016.md         # Execute Scientific Branch Recovery
│   ├── task-017.md         # Align All Orchestration-Tools Branches
│   ├── task-018.md         # Implement Regression Prevention Safeguards
│   ├── task-019.md         # Scan and Resolve Merge Conflicts
│   └── task-020.md         # Refine launch.py Dependencies
│
├── CLEAN_TASK_INDEX.md      # Task index with status tracking
├── LOGGING_GUIDE.md         # How to log task progress
├── LOGGING_SYSTEM_PLAN.md   # Detailed logging implementation plan
├── README.md                # Project overview
├── task_mapping.md          # Old-to-new task mapping
├── INTEGRATION_EXECUTION_CHECKLIST.md
├── TASK_DEPENDENCY_VISUAL_MAP.md
├── TASK-001-INTEGRATION-GUIDE.md
├── TASK-002-CLUSTERING-SYSTEM-GUIDE.md
├── TASK-002-SEQUENTIAL-EXECUTION-FRAMEWORK.md
├── WEEK_1_FINAL_SUMMARY.md
├── INDEX_AND_GETTING_STARTED.md
├── COMPREHENSIVE_DEPENDENCY_FRAMEWORK.md
├── RENUMBERING_021_TO_002_STATUS.md
├── RENUMBERING_DECISION_TASK_021.md
└── complete_new_task_outline_ENHANCED.md
```

### TOML Phase Structure

| Phase | Tasks | Focus |
|-------|-------|-------|
| **1: Foundation** | 1.1-1.5 | Pre-flight checks and validation setup |
| **2: Assessment** | 2.1-2.4 | Branch identification and clustering |
| **3: Build Framework** | 3.1-3.7 | Create alignment tools and scripts |
| **4: Execution** | 4.1-4.5 | Perform alignment operations |
| **5: Finalization** | 5.1-5.4 | PR creation and documentation |
| **6: Maintenance** | 6.1-6.4 | Ongoing stability and monitoring |

### new_task_plan Initiative Structure

| Initiative | Tasks | Focus |
|------------|-------|-------|
| **1: Foundational** | 001-003 | Validation framework |
| **2: Build Core** | 004-015 | Tool development |
| **3: Execution** | 016-017 | Using the framework |
| **4: Maintenance** | 018-020 | Ongoing upkeep |

---

## 4. Key Issues Identified

### Critical Issues

| Issue | Location | Impact | Fix Required |
|-------|----------|--------|--------------|
| Missing Assessment Phase | new_task_plan | No equivalent for TOML 2.1-2.4 | Add tasks 021-024 |
| Missing Finalization Phase | new_task_plan | No equivalent for TOML 5.1-5.4 | Add tasks 025-028 |
| Broken `backlog/` reference | task-002.md | Non-existent file | Remove reference |
| Deprecated `tasks.json` | Multiple docs | System needs cleanup | Remove references |

### Documentation Inconsistencies

| Issue | Files Affected | Status |
|-------|----------------|--------|
| `tasks.json` references | 10+ files in new_task_plan/ | Needs cleanup |
| `backlog/` links | task-002.md | Needs fix |
| Old task numbering (75-79) | docs/branch_alignment/ | Needs update |
| Missing files | docs/branch_alignment/INDEX.md references 9 non-existent files | Needs fix |

### Structure Mismatches

| TOML Phase | new_task_plan Initiative | Alignment |
|------------|-------------------------|-----------|
| 1: Foundation | Initiative 1 | Partial |
| 2: Assessment | Part of Initiative 2 | **MISSING** |
| 3: Build | Initiative 2 | Matches |
| 4: Execution | Initiative 3 | Partial |
| 5: Finalization | Part of Initiative 2 | **MISSING** |
| 6: Maintenance | Initiative 4 | Matches |

---

## 5. Logging System Design

### Hybrid Approach

**Inline Markdown** (in task files):
```markdown
### X.X.N: Log Findings

**Parameters:** Git command used, branch count, feature types
**Decision:** Used merge-base over diff for performance
**Outcome:** 450ms per branch, acceptable for N<50 branches
**Log to:** `task_data/findings/{phase}/{file}.json`
```

**External JSON** (in `task_data/findings/`):
```json
{
  "task_id": "3.1.4",
  "timestamp": "2026-01-04T12:00:00Z",
  "phase": "phase3_build",
  "parameters": {"git_cmd": "merge-base", "branches": 23},
  "decision": "Used merge-base over diff for performance",
  "outcome": {"duration_ms": 450, "status": "acceptable"},
  "findings": {"pattern": null, "recommendation": null}
}
```

### Directory Structure

```
task_data/findings/
├── phase1_foundational/    # Foundation tasks (001-003)
│   ├── git_tooling.json
│   ├── validation_command.json
│   ├── linting_tools.json
│   ├── primary_backups.json
│   └── branch_protection.json
│
├── phase2_assessment/       # Assessment tasks (007-009)
│   ├── branch_features.json
│   ├── target_assignments.json
│   ├── clustering_results.json
│   └── priority_scores.json
│
├── phase3_build/           # Build tasks (004-006, 010-015)
│   ├── error_detection.json
│   ├── validation_framework.json
│   ├── backup_mechanism.json
│   ├── branch_id_tool.json
│   ├── alignment_logic.json
│   ├── complex_handler.json
│   └── workflow_orchestration.json
│
├── phase4_execution/        # Execution tasks (016-017)
│   ├── checklist_loading.json
│   ├── main_alignments.json
│   ├── scientific_alignments.json
│   ├── orchestration_alignments.json
│   └── complex_branches.json
│
├── phase5_finalization/     # Finalization tasks (014-015)
│   ├── branch_collection.json
│   ├── changes_summaries.json
│   ├── pr_outcomes.json
│   └── checklist_updates.json
│
└── phase6_maintenance/      # Maintenance tasks (018-020)
    ├── regression_prevention.json
    ├── conflict_scan.json
    ├── dependency_reviews.json
    └── documentation_updates.json
```

### JSON Schema

| Field | Type | Description |
|-------|------|-------------|
| `task_id` | string | e.g., "3.1.4" |
| `timestamp` | ISO 8601 | When entry was created |
| `phase` | string | e.g., "phase3_build" |
| `parameters` | object | Inputs, configs, thresholds |
| `decision` | object | Choice made + rationale |
| `outcome` | object | Result, metrics, success/failure |
| `findings` | object | Patterns, recommendations |

### Task-Phase Mapping

| Task | Phase | Log File | Subtasks |
|------|-------|----------|----------|
| 001-003 | phase1_foundational | 5 files | 1 each |
| 004-006 | phase3_build | 3 files | 1 each |
| 007-009 | phase2_assessment | 4 files | 2 each |
| 010-015 | phase3_build | 5 files | 2 each |
| 016-017 | phase4_execution | 4 files | 2 each |
| 018-020 | phase6_maintenance | 4 files | 2 each |

**Total:** 29 tasks, ~35 logging subtasks

---

## 6. Task Files Overview

### Task Status Summary

| Status | Count | Tasks |
|--------|-------|-------|
| pending | 17 | 001-006, 008-011, 013-020 |
| in-progress | 1 | 007 |
| blocked | 2 | 003, 018, 020 |
| deferred | 2 | 017, 019 |

### Key Task Details

| Task | Title | Priority | Status |
|------|-------|----------|--------|
| 001 | Framework Strategy Definition | high | pending |
| 002 | Create Comprehensive Merge Validation Framework | high | pending |
| 003 | Develop Pre-merge Validation Scripts | high | blocked |
| 004 | Establish Core Branch Alignment Framework | high | pending |
| 005 | Develop Automated Error Detection Scripts | high | pending |
| 006 | Implement Branch Backup and Restore Mechanism | high | pending |
| 007 | Develop Feature Branch Identification Tool | medium | in-progress |
| 008 | Automate Changes Summary and Checklist Generation | medium | pending |
| 009 | Create Post-Alignment File Resolution List | high | pending |
| 010 | Develop Core Primary-to-Feature Alignment Logic | high | pending |

---

## 7. Documentation Structure

### Key Documentation Files

| File | Purpose | Status |
|------|---------|--------|
| `PROJECT_REFERENCE.md` | This consolidated reference | ✅ Created |
| `ENHANCED_VALIDATION_PLAN.md` | Validation and cleanup plan | ✅ Created |
| `LOGGING_GUIDE.md` | How to log task progress | ✅ Created |
| `LOGGING_SYSTEM_PLAN.md` | Detailed implementation plan | ✅ Created |
| `CLEAN_TASK_INDEX.md` | Task index with status | ✅ Created |
| `README.md` | Project overview | ✅ Created |
| `task_mapping.md` | Old-to-new task mapping | ✅ Created |
| `COMPLETE_NEW_TASK_OUTLINE_ENHANCED.md` | Full task details | ✅ Created |

### Scripts Available

| Script | Purpose | Status |
|--------|---------|--------|
| `scripts/query_findings.py` | Query findings by phase/task/date | ✅ Created |
| `scripts/markdownlint_check.py` | Validate markdown structure | ✅ Created |

### External References

| Reference | Status |
|-----------|--------|
| `mdl` (markdownlint) | ✅ Available |
| `tasks/archive/toml_task_plan.md` | ✅ Authoritative source |

---

## 8. Implementation Roadmap

### Phase 1: Infrastructure Setup (Day 1)

| Step | Action | Output |
|------|--------|--------|
| 1.1 | Create `task_data/findings/` directories | 6 phase directories ✅ |
| 1.2 | Create `LOGGING_GUIDE.md` | Documentation file ✅ |
| 1.3 | Create `scripts/query_findings.py` | Query utility ✅ |
| 1.4 | Create `.gitkeep` files | Enable git tracking ✅ |

### Phase 2: Fix Broken References (Day 2)

| Step | Action | Output |
|------|--------|--------|
| 2.1 | Remove `backlog/` from task-002.md | Clean reference |
| 2.2 | Remove `tasks.json` from CLEAN_TASK_INDEX.md | Updated index |
| 2.3 | Archive old formatted task files | Cleanup new_task_plan |

### Phase 3: Add Logging to Tasks (Days 3-5)

| Step | Action | Tasks Modified |
|------|--------|----------------|
| 3.1 | Add logging subtasks to Foundation tasks | 001-003 |
| 3.2 | Add logging subtasks to Build tasks | 004-015 |
| 3.3 | Add logging subtasks to Execution tasks | 016-017 |
| 3.4 | Add logging subtasks to Maintenance tasks | 018-020 |

### Phase 4: Documentation Updates (Day 6)

| Step | Action | Output |
|------|--------|--------|
| 4.1 | Update CLEAN_TASK_INDEX.md | Remove deprecated refs |
| 4.2 | Update AGENTS.md | Document logging commands |
| 4.3 | Update CLAUDE.md | Include logging workflow |

### Phase 5: Testing & Validation (Day 7)

| Step | Action | Output |
|------|--------|--------|
| 5.1 | Test query_findings.py script | Verified queries |
| 5.2 | Validate all JSON logs | Schema compliance |
| 5.3 | Review task file changes | Consistency check |

---

## 9. Validation & Testing

### Available Tools

| Tool | Command | Purpose |
|------|---------|---------|
| `mdl` | `mdl <file.md>` | Markdown linting |
| `python` | `python scripts/query_findings.py --phase <phase>` | Query findings |
| `python` | `python scripts/compress_progress.py --compress --source <dir>` | Compress findings |
| `python` | `python scripts/compress_progress.py --verify --archive <file>` | Verify archives |
| `shell` | `bash scripts/markdownlint_check.py --fix` | Validate structure |

### Validation Commands

```bash
# Query all assessment phase findings
python scripts/query_findings.py --phase phase2_assessment

# Query specific task findings
python scripts/query_findings.py --task 3.1.4

# Query by date range
python scripts/query_findings.py --from 2026-01-01 --to 2026-01-31

# Get summary statistics
python scripts/query_findings.py --stats

# Compress findings for storage
python scripts/compress_progress.py --compress --source task_data/findings/phase_001_framework_strategy --destination task_data/compressed

# Verify compressed archive
python scripts/compress_progress.py --verify --archive task_data/compressed/progress_all_20260104_213539.tar.gz

# Check markdown structure
mdl new_task_plan/task_files/task-001.md

# Validate and fix issues
python scripts/markdownlint_check.py --fix
```

### Success Criteria

| Criterion | Measure |
|-----------|---------|
| All 20 tasks have logging subtasks | 20 tasks × 1-2 logging subtasks |
| All log files accessible | `task_data/findings/` populated |
| Queries work | `query_findings.py` returns results |
| Broken references fixed | 0 `backlog/`, `tasks.json` refs |
| Documentation updated | AGENTS.md, CLAUDE.md updated |

---

## 10. Next Steps

### Immediate Actions

1. **Review this reference document** - Confirm understanding of project state
2. **Begin Phase 3** - Add logging subtasks to tasks
3. **Fix broken references** - Remove `backlog/` and `tasks.json` refs
4. **Test logging system** - Run `query_findings.py` to verify

### Questions for Clarification

| Question | Options |
|----------|---------|
| Which numbering system is authoritative? | A: new_task_plan (001-020), B: TOML (1.1-4.4) |
| Add missing Assessment/Finalization phases? | A: Yes, B: No, defer to future |
| Scope of documentation updates? | A: All tasks, B: Critical only |

### Quick Reference Commands

```bash
# List all task files
ls new_task_plan/task_files/task-*.md

# Check task status
grep "Status:" new_task_plan/task_files/task-*.md

# Run validation
python scripts/query_findings.py --stats

# View project structure
tree new_task_plan/ -L 2
```

---

## Appendix A: File Locations

| File | Location |
|------|----------|
| This reference document | `/home/masum/github/PR/.taskmaster/PROJECT_REFERENCE.md` |
| Enhanced validation plan | `/home/masum/github/PR/.taskmaster/ENHANCED_VALIDATION_PLAN.md` |
| Logging system plan | `/home/masum/github/PR/.taskmaster/new_task_plan/LOGGING_SYSTEM_PLAN.md` |
| Logging guide | `/home/masum/github/PR/.taskmaster/new_task_plan/LOGGING_GUIDE.md` |
| Query script | `/home/masum/github/PR/.taskmaster/scripts/query_findings.py` |
| Task files | `/home/masum/github/PR/.taskmaster/new_task_plan/task_files/` |
| TOML plan | `/home/masum/github/PR/.taskmaster/tasks/archive/toml_task_plan.md` |
| Findings directory | `/home/masum/github/PR/.taskmaster/task_data/findings/` |

### A.1 Archive Locations

Excessive documentation has been archived to `tasks/archive/documentation/`:

| Subdirectory | Contents |
|--------------|----------|
| `analysis/` | ARCHITECTURE_ANALYSIS.md, TASK_DIRECTORY_ANALYSIS.md, etc. |
| `integration/` | INTEGRATION_VISUAL_GUIDE.md, HANDOFF_INTEGRATION_*.md, etc. |
| `migration/` | MIGRATION_VISUAL_WORKFLOW.md, MIGRATION_SUMMARY.txt, etc. |
| `planning/` | WEEK_1_*.md, PLAN_SUMMARY.md, etc. |
| `task_specific/` | TASK_7_ENHANCEMENT_*.md, TASK_75_IMPROVEMENTS.md, etc. |
| `reports/` | COMPLETE_ANALYSIS_EXECUTIVE_SUMMARY.md, etc. |

**Total archived:** 34 files

---

## Appendix B: Task Numbering Reference

| TOML | new_task_plan | Purpose |
|------|---------------|---------|
| 1.1-1.5 | 001-003 | Foundation |
| 2.1-2.4 | 007-009 | Assessment |
| 3.1-3.7 | 004-006, 010-015 | Build Framework |
| 4.1-4.5 | 016-017 | Execution |
| 5.1-5.4 | 014-015 | Finalization |
| 6.1-6.4 | 018-020 | Maintenance |

---

## Appendix C: Quick Reference

| Component | Status | Action |
|-----------|--------|--------|
| Task files (001-020) | ✅ Created | Add logging subtasks |
| Logging directories | ✅ Created | Populate with findings |
| Query script | ✅ Created | Use for validation |
| Documentation | ⚠️ Partial | Cleanup complete, refs updated |
| Broken links | 🔴 Fixed | Removed `backlog/` refs |

### C.1 Project Root File Count

| Metric | Before | After |
|--------|--------|-------|
| Markdown files in root | ~100+ | 51 |
| Archived documentation | 0 | 34 |
| Key files kept | - | 17 |

### C.2 Archive Statistics

| Category | Files Archived |
|----------|----------------|
| Analysis | 4 |
| Integration | 6 |
| Migration | 5 |
| Planning | 5 |
| Task-specific | 5 |
| Reports | 5 |
| **Total** | **34** |

---

**End of Reference Document**

For questions or updates, refer to the section numbers above or check the specific documentation files listed in Appendix A.
