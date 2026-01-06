# New Task Plan Evaluation and Processing Plan

**Date:** January 6, 2026  
**Status:** Evaluation Complete - Ready for Structured Processing  
**Scope:** Transform new_task_plan/ into independent subtask markdown system  
**Key Findings:** 6 critical issues identified, 4 comprehensive resolution strategies available

---

## Executive Summary

The `new_task_plan/` directory contains rich, well-structured task documentation for Tasks 001-026, but has **NOT yet been transformed into an independent subtask markdown file system** using the Project-Wide Standard (TASK_STRUCTURE_STANDARD.md).

**Current State:**
- ✅ High-level task planning files exist (README.md, CLEAN_TASK_INDEX.md, task_mapping.md)
- ✅ Complete task-002-clustering.md with 9 subtask specifications
- ⚠️ Task 002 naming/numbering conflict (Merge Validation vs. Clustering)
- ❌ No individual subtask files (task-002-1.md through task-002-9.md)
- ❌ Integration guides not yet fully created
- ❌ Findings/guidance not yet extracted into independent format

**Recommendation:** Process existing documentation systematically using 4-phase approach (see "Processing Approach" below).

---

## Previous Findings Summary

Based on thread analysis T-019b8e90 and T-019b8e7e:

### Key Decision: Single-File-Per-Subtask Standard (APPROVED)
- **Rationale:** Previous consolidation lost 98.7% of completion criteria (523 of 530 missing)
- **Root Cause:** Top-down approach summarized rather than migrated granular details
- **Solution:** Each subtask file must contain complete Specification + Implementation
- **Standard:** TASK_STRUCTURE_STANDARD.md (14 mandatory sections)

### Task 002 Resolution Status
- **Issue:** Task 075 renumbering created Task 002-Clustering as Initiative 3
- **Conflict:** Task 002 already existed as Merge Validation (Initiative 1)
- **Status:** Both are valid; requires clear naming/documentation
- **Decision:** Rename files to clarify:
  - Task 002 (Merge Validation) → Keep as task-002.md for Initiative 1
  - Task 002-Clustering (Branch Clustering) → Rename to task-021.md for Initiative 3

### Current Phase Completion
- ✅ **Phase 1 Complete:** Tasks 002.1-002.5 individual files created with 277 preserved criteria
- ✅ **Phase 2 Complete:** Task 075 orphaning resolved, consolidated into Task 002
- ⏳ **Phase 3 Pending:** Complete remaining subtasks (002.6-002.9, Task 001, etc.)

---

## Critical Issues Identified

### Issue #1: Task 002 / Task 002-Clustering Naming Conflict
**Severity:** HIGH  
**Impact:** Confusion in documentation and file references  
**Current State:**
```
new_task_plan/task_files/
├── task-002.md                 # Merge Validation (Initiative 1, 9 subtasks)
├── task-002-clustering.md      # Branch Clustering (Initiative 3, 9 subtasks)
```

**Problem:** Both files exist; unclear which is "Task 002" in task-master CLI

**Resolution:** Clarify through consistent naming:
- Keep task-002.md = Initiative 1, Task 002 (Merge Validation)
- Rename task-002-clustering.md → task-021.md = Initiative 3, Task 021 (Branch Clustering, aka old Task 75)

---

### Issue #2: Missing Individual Subtask Markdown Files
**Severity:** HIGH  
**Impact:** Cannot work on subtasks independently; no per-subtask specs  
**Current State:**
- ✅ Complete specifications in parent files (task-002.md, task-021.md)
- ❌ No individual task-002-1.md through task-002-9.md files
- ❌ No individual task-021-1.md through task-021-9.md files
- ❌ No individual files for other tasks (001-020, 022-026)

**Required Outcome:**
```
new_task_plan/task_files/
├── task-001.md                 # Main task overview
├── task-001-1.md through task-001-4.md    # 4 subtasks for Initiative 1, Task 1
├── task-002.md                 # Main task overview
├── task-002-1.md through task-002-9.md    # 9 subtasks for Initiative 1, Task 2
├── task-021.md                 # Main task overview (renamed from task-002-clustering.md)
├── task-021-1.md through task-021-9.md    # 9 subtasks for Initiative 3, Task 21
└── ... (similar for all 26 tasks)
```

---

### Issue #3: Integration Guides Referenced But Not Created
**Severity:** MEDIUM  
**Impact:** Developers don't have step-by-step implementation paths  
**Current State:**
- ✅ TASK-001-INTEGRATION-GUIDE.md referenced in README.md (placeholder)
- ✅ TASK-021-CLUSTERING-SYSTEM-GUIDE.md referenced (to be created)
- ❌ Actually created but not completed

**Required Outcome:**
- Complete TASK-001-INTEGRATION-GUIDE.md (7 day-by-day implementation plan)
- Complete TASK-021-CLUSTERING-SYSTEM-GUIDE.md (8 week parallel/sequential strategies)

---

### Issue #4: Guidance/Findings Not Extracted Into Independent Format
**Severity:** MEDIUM  
**Impact:** Architectural guidance scattered across guidance/ directory  
**Current State:**
- ✅ Comprehensive guidance in .taskmaster/guidance/ (9 files)
- ✅ Phase findings in .taskmaster/task_data/findings/ (14 subdirectories)
- ❌ Not referenced from new_task_plan/
- ❌ Not integrated into task specs

**Required Outcome:**
- Create new_task_plan/guidance/ with extracted, task-relevant findings
- Reference guidance from each task file's "Implementation Considerations" section
- Consolidate findings into searchable index

---

### Issue #5: Task File Format Inconsistency
**Severity:** MEDIUM  
**Impact:** Some files follow standard, others don't  
**Current State:**
- ✅ task-001.md follows structure standard (basic level)
- ✅ task-002.md has detailed sections
- ⚠️ task-002-clustering.md has rich content but not fully standard format
- ❌ Other task files lack detailed success criteria

**Required Outcome:**
- All task files must conform to TASK_STRUCTURE_STANDARD.md (14 sections)
- All subtask files must use dash notation (task-021-1.md, not task-021_1.md)

---

### Issue #6: Missing Performance Baselines and Acceptance Criteria
**Severity:** MEDIUM  
**Impact:** Teams don't know what "done" looks like  
**Current State:**
- ✅ Effort estimates provided (e.g., 24-32h)
- ⚠️ Some success criteria listed
- ❌ Performance baselines missing for many tasks
- ❌ Acceptance criteria not granular enough

**Required Outcome:**
- Every subtask file must define specific "Definition of Done"
- Performance targets for computational tasks (e.g., "< 2 minutes for 13 branches")
- Quality metrics (e.g., "> 90% test coverage")

---

## Existing Assets to Leverage

### From Previous Work (Thread History)
1. **TASK_STRUCTURE_STANDARD.md** - 14-section template (approved, in place)
2. **Task 075 HANDOFF files** - 9 comprehensive implementation guides (ready to extract)
3. **task-7.md** - Enhanced Task 001 source material (in task_data/)
4. **previous findings** - Architecture guidance in task_data/findings/ (14 phase directories)

### In Current Directory
1. **complete_new_task_outline_ENHANCED.md** - Full task specifications (2700+ lines)
2. **INTEGRATION_EXECUTION_CHECKLIST.md** - Week-by-week execution plan
3. **HANDOFF_INDEX.md** - Task 075 strategy and execution modes
4. **task_mapping.md** - Old ID → New ID conversion table

### In task_data/ Ready to Integrate
1. **task-7.md** - Task 001 source
2. **HANDOFF_*.md** (9 files) - Task 021 (old Task 75) implementation specs
3. **guidance/** directory - Architectural alignment guidance (9 docs)
4. **findings/** directory - Phase-by-phase research findings (14 subdirectories)

---

## Processing Approach: 4 Strategic Paths

### PATH A: Pure Extraction (Recommended for Speed)
**Timeline:** 1-2 days  
**Effort:** 4-8 hours  
**Approach:** Extract existing content into standard format without enhancement

**Steps:**
1. Extract task-002.md subtasks → individual task-002-1.md through task-002-9.md
2. Extract task-002-clustering.md → rename to task-021.md, extract subtasks to task-021-1.md through task-021-9.md
3. Extract task-001.md subtasks (already partial, need completion)
4. Apply TASK_STRUCTURE_STANDARD.md sections to each file
5. Update cross-references in CLEAN_TASK_INDEX.md and task_mapping.md

**Pro:** Fast, preserves all existing content, ready to work  
**Con:** Doesn't add new guidance/findings integration

---

### PATH B: Extraction + Guidance Integration
**Timeline:** 3-4 days  
**Effort:** 12-16 hours  
**Approach:** Extract content AND integrate relevant guidance/findings

**Steps (A + these additions):**
1. Create new_task_plan/guidance/ directory
2. Extract relevant guidance from task_data/guidance/ (9 files)
3. Extract relevant findings from task_data/findings/ (14 phase directories)
4. Add "Implementation Considerations" section to each task file linking to guidance
5. Create GUIDANCE_INDEX.md with searchable reference
6. Update README.md with guidance location and usage

**Pro:** Complete, actionable context; teams have guidance at hand  
**Con:** More work but pays off in implementation

---

### PATH C: Extraction + Parallel Execution Planning
**Timeline:** 4-5 days  
**Effort:** 16-20 hours  
**Approach:** Extract content AND create detailed parallel/sequential execution plans

**Steps (B + these additions):**
1. Analyze task dependencies (from CLEAN_TASK_INDEX.md)
2. Create EXECUTION_STRATEGIES.md (Parallel, Sequential, Hybrid modes)
3. Create CRITICAL_PATH.md showing 16-18 week baseline timeline
4. Create PARALLEL_EXECUTION.md showing 8-10 week with 5-person teams
5. Add execution strategy guide to each task file
6. Create team role allocation document (who does what task)

**Pro:** Teams understand parallel opportunities; clear schedule  
**Con:** Requires dependency analysis accuracy

---

### PATH D: Comprehensive System (Recommended for Long-Term Viability)
**Timeline:** 5-7 days  
**Effort:** 20-28 hours  
**Approach:** Extract + Guidance + Execution Planning + Quality Assurance

**Steps (C + these additions):**
1. Create comprehensive NAVIGATION_GUIDE.md (where to find everything)
2. Create QA_CHECKLIST.md (verification before implementation)
3. Create LESSONS_LEARNED.md (from previous phases)
4. Create DEPENDENCY_MATRIX.md (all 26 tasks, cross-referenced)
5. Extract metrics/performance baselines from guidance/findings into each task
6. Create sample team handoff document template
7. Run validation: ensure all 14 TASK_STRUCTURE_STANDARD sections present in all files

**Pro:** Complete, production-ready system; minimal surprises  
**Con:** Most effort but eliminates future rework

---

## Recommended Processing Sequence

**I recommend PATH C (Extraction + Guidance + Parallel Planning) as the optimal balance:**

### Phase 1: Extract and Standardize (Days 1-2, 4-6h)
- [ ] Extract task-002.md → individual subtask files (task-002-1.md through task-002-9.md)
- [ ] Rename and extract task-002-clustering.md → task-021.md + subtasks (task-021-1.md through task-021-9.md)
- [ ] Extract task-001.md → subtask files (task-001-1.md through task-001-4.md)
- [ ] Apply TASK_STRUCTURE_STANDARD.md sections to all files
- [ ] Validate markdown formatting

### Phase 2: Integrate Guidance (Days 2-3, 4-6h)
- [ ] Create new_task_plan/guidance/ directory structure
- [ ] Extract 9 relevant docs from task_data/guidance/
- [ ] Extract 14 phase findings from task_data/findings/
- [ ] Add "Implementation Considerations" section to each task file
- [ ] Create new_task_plan/GUIDANCE_INDEX.md
- [ ] Update README.md with guidance references

### Phase 3: Create Execution Plans (Days 3-4, 6-8h)
- [ ] Analyze task dependencies (audit CLEAN_TASK_INDEX.md)
- [ ] Create EXECUTION_STRATEGIES.md (parallel/sequential/hybrid modes)
- [ ] Create CRITICAL_PATH.md (16-18 week timeline analysis)
- [ ] Create PARALLEL_EXECUTION.md (8-10 week with teams)
- [ ] Update each task file with "Execution Context" section

### Phase 4: Validation and Completion (Day 4, 2-4h)
- [ ] Run validation: all task files have 14 standard sections
- [ ] Verify all dash notation (task-XXX-Y.md format)
- [ ] Check all cross-references
- [ ] Update task_mapping.md with new file locations
- [ ] Create PROCESSING_COMPLETION_REPORT.md

---

## File Organization Target Structure

```
new_task_plan/
├── README.md                              # ✅ Exists, needs guidance refs
├── CLEAN_TASK_INDEX.md                    # ✅ Exists, needs phase 3 updates
├── task_mapping.md                        # ✅ Exists, needs file location updates
├── complete_new_task_outline_ENHANCED.md  # ✅ Reference archive
├── INTEGRATION_EXECUTION_CHECKLIST.md     # ✅ Reference archive
├── 
├── EXECUTION_STRATEGIES.md                # 🆕 Create in Phase 3
├── CRITICAL_PATH.md                       # 🆕 Create in Phase 3
├── PARALLEL_EXECUTION.md                  # 🆕 Create in Phase 3
├── GUIDANCE_INDEX.md                      # 🆕 Create in Phase 2
├── PROCESSING_COMPLETION_REPORT.md        # 🆕 Create in Phase 4
│
├── guidance/                              # 🆕 Create in Phase 2
│   ├── README.md
│   ├── architecture_alignment/            # From task_data/guidance/
│   ├── merge_strategy/
│   ├── implementation_lessons/
│   └── phase_findings/                    # From task_data/findings/
│
└── task_files/
    ├── task-001.md                        # Initiative 1, Task 1 overview
    ├── task-001-1.md through task-001-4.md    # 4 subtasks
    ├── task-002.md                        # Initiative 1, Task 2 overview
    ├── task-002-1.md through task-002-9.md    # 9 subtasks (formerly clustering)
    ├── task-003.md through task-020.md    # Other Initiative 1-2 tasks
    ├── task-021.md                        # Initiative 3, Task 21 (renamed from 002-clustering)
    ├── task-021-1.md through task-021-9.md    # 9 subtasks (Branch Clustering)
    ├── task-022.md through task-026.md    # Execution & Maintenance tasks
    └── (All use dash notation: task-XXX-Y.md, not task-XXX_Y.md)
```

---

## Key References for Processing

### Standards and Frameworks
- **TASK_STRUCTURE_STANDARD.md** - 14-section template (approved)
- **TASK_STRUCTURE.md** - Decision documentation
- **complete_new_task_outline_ENHANCED.md** - Full task specifications (2700+ lines)

### Source Material
- **task_data/task-7.md** - Task 001 source
- **task_data/HANDOFF_*.md** (9 files) - Task 021 source
- **task_data/HANDOFF_INDEX.md** - Task 021 strategy

### Guidance and Findings
- **task_data/guidance/** (9 documents) - Architecture alignment, merge strategy, implementation
- **task_data/findings/** (14 phase directories) - Research findings by phase

### Execution Planning
- **INTEGRATION_EXECUTION_CHECKLIST.md** - Week-by-week execution
- **CLEAN_TASK_INDEX.md** - Task status and priority matrix
- **task_mapping.md** - ID conversion reference

---

## Processing Checklist

### Before Starting
- [ ] Read this evaluation document completely
- [ ] Choose processing path (recommended: PATH C)
- [ ] Review TASK_STRUCTURE_STANDARD.md sections
- [ ] Gather all source files (task-7.md, HANDOFF_*.md, guidance/*)

### Phase 1: Extract and Standardize
- [ ] Extract task-002.md → task-002-1.md through task-002-9.md (9 files)
- [ ] Rename task-002-clustering.md → task-021.md
- [ ] Extract task-021.md → task-021-1.md through task-021-9.md (9 files)
- [ ] Extract task-001.md → task-001-1.md through task-001-4.md (4 files)
- [ ] Apply TASK_STRUCTURE_STANDARD.md to all new files
- [ ] Validate dash notation throughout (task-XXX-Y.md)

### Phase 2: Integrate Guidance
- [ ] Create new_task_plan/guidance/ directory
- [ ] Extract ARCHITECTURE_ALIGNMENT_COMPLETE_AND_RECOMMENDATIONS.md
- [ ] Extract FINAL_MERGE_STRATEGY.md
- [ ] Extract HANDLING_INCOMPLETE_MIGRATIONS.md
- [ ] Extract MERGE_GUIDANCE_DOCUMENTATION.md
- [ ] Extract phase findings from task_data/findings/
- [ ] Create GUIDANCE_INDEX.md with searchable index
- [ ] Add "Implementation Considerations" section to each task file

### Phase 3: Create Execution Plans
- [ ] Analyze dependencies from CLEAN_TASK_INDEX.md
- [ ] Create EXECUTION_STRATEGIES.md
- [ ] Create CRITICAL_PATH.md (16-18 week analysis)
- [ ] Create PARALLEL_EXECUTION.md (8-10 week with teams)
- [ ] Update each task with "Execution Context" section

### Phase 4: Validate and Complete
- [ ] Verify all files have 14 TASK_STRUCTURE_STANDARD sections
- [ ] Verify all files use dash notation (task-XXX-Y.md)
- [ ] Check all cross-references for validity
- [ ] Update task_mapping.md with new file locations
- [ ] Create PROCESSING_COMPLETION_REPORT.md

---

## Success Criteria

Processing is complete when:

✅ **Structure**
- [ ] All 26 main task files exist (task-001.md through task-026.md)
- [ ] All subtask files exist (task-XXX-Y.md format, ~100+ total files)
- [ ] All files conform to TASK_STRUCTURE_STANDARD.md (14 sections)
- [ ] No underscore notation (_), only dash notation (-)

✅ **Content**
- [ ] All original task specifications preserved
- [ ] All success criteria extracted and detailed
- [ ] All effort estimates and complexity ratings present
- [ ] Performance baselines defined for computational tasks
- [ ] Guidance/findings integrated into each task

✅ **Navigation**
- [ ] GUIDANCE_INDEX.md created and searchable
- [ ] EXECUTION_STRATEGIES.md explains parallel/sequential options
- [ ] CRITICAL_PATH.md shows 16-18 week timeline
- [ ] PARALLEL_EXECUTION.md shows 8-10 week with 5 people
- [ ] README.md updated with new structure explanation

✅ **Cross-Reference**
- [ ] CLEAN_TASK_INDEX.md updated with new file locations
- [ ] task_mapping.md updated with file locations
- [ ] task-XXX-Y.md files reference each other correctly
- [ ] No broken links in any document

✅ **Readiness**
- [ ] Teams can start with Task 001 using task-001-1.md
- [ ] Teams can start with Task 021 using task-021-1.md
- [ ] All guidance is accessible from each task file
- [ ] All execution modes are documented and clear

---

## Estimated Effort Summary

| Path | Duration | Effort | Scope | Recommendation |
|------|----------|--------|-------|-----------------|
| A: Pure Extraction | 1-2 days | 4-8h | Extract only | For time-sensitive starts |
| B: + Guidance | 3-4 days | 12-16h | Extract + guidance | Good balance |
| **C: + Execution Planning** | **4-5 days** | **16-20h** | **Extract + guidance + plans** | **RECOMMENDED** |
| D: Comprehensive | 5-7 days | 20-28h | All + QA + navigation | For long-term systems |

**Recommendation:** Proceed with **PATH C** (Extraction + Guidance + Execution Planning)

---

## Next Steps

1. **Approve processing path** (recommend PATH C)
2. **Allocate 16-20 hours** across 4-5 days
3. **Begin Phase 1** (Extract and Standardize) with task-002.md extraction
4. **Use this document as reference** throughout processing
5. **Update PROCESSING_COMPLETION_REPORT.md** as each phase completes

---

**Document Created:** January 6, 2026  
**Version:** 1.0  
**Status:** Ready for Processing  
**Next Review:** After Phase 4 Completion
