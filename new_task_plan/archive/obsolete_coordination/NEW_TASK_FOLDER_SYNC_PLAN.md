# new_task_plan Folder Synchronization Plan

**Date:** January 4, 2026  
**Status:** Planning (post-WS2 renumbering)  
**Objective:** Sync new_task_plan documentation with actual task file structure and post-renumbering state

---

## Current State Assessment

### ✅ What's Complete (Post-WS2)

1. **Documentation files updated:**
   - COMPREHENSIVE_DEPENDENCY_FRAMEWORK.md - Task 021→002 renumbering applied ✅
   - TASK_DEPENDENCY_VISUAL_MAP.md - References updated ✅
   - TASK-002-CLUSTERING-SYSTEM-GUIDE.md - Created with 002 references ✅
   - TASK-002-SEQUENTIAL-EXECUTION-FRAMEWORK.md - Created with 002 references ✅

2. **Reference documents:**
   - task_mapping.md - NOW UPDATED with proper mapping ✅
   - CLEAN_TASK_INDEX.md - Exists, references Task 002 (needs clarification)

### ⚠️ What Needs Syncing

1. **task_files/ directory structure:**
   - ✅ task-001.md through task-020.md exist (001-020)
   - ❌ NO task-021.md or task-021-1.md through task-021-9.md (002-Clustering system files missing)
   - ❌ NO task-022.md through task-026.md (Execution/Maintenance files missing)

2. **task_mapping.md clarifications:**
   - ❌ Confusing dual Task 002 references (Initiative 1 Task 002 vs Clustering System Task 002)
   - ✅ NOW UPDATED: Clarified Initiative structure

3. **CLEAN_TASK_INDEX.md needs update:**
   - ❌ Still references "Task 021" in workflow section (line 149)
   - ❌ References tasks 022-023 without files existing
   - ❌ References tasks 024-026 without files existing

---

## Task Structure Explanation

### The Numbering Challenge

The project has a **complex numbering situation** that WS2 helped clarify:

**Initiative 1-2 (Main Framework):**
- Task 001: Framework Strategy (old Task 7)
- Task 002: Merge Validation (old Task 9) ← **This is Initiative 1**
- Task 003-026: Other main framework tasks

**Initiative 3 (Clustering System):**
- Task 002 (Clustering): Branch Clustering System (old Task 75) ← **This is a separate Initiative 3**
  - Subtasks: 002.1, 002.2, ... 002.9 (old 75.1-75.9)
  - Runs **parallel** with Task 001, feeds back to validate framework

**Initiative 4 (Execution):**
- Task 022: Scientific Branch Recovery (old Task 23)
- Task 023: Orchestration Tools Alignment (old Task 101)

**Initiative 5 (Maintenance):**
- Task 024: Regression Prevention (old Task 27)
- Task 025: Conflict Resolution (old Task 31)
- Task 026: Dependency Refinement (old Task 40)

### Why This Matters for Syncing

The task numbering reuses Task 002 for two different initiatives:
1. Task 002 = Initiative 1 task (Merge Validation, in main task sequence)
2. Task 002-Clustering = Initiative 3 task (Branch Clustering, runs parallel)

**Files should be organized as:**
```
task_files/
├── task-001.md ✅
├── task-002.md ✅ (Initiative 1: Merge Validation)
├── task-003.md through task-020.md ✅ (Initiative 1-2)
├── task-002-clustering.md (NEW - Initiative 3: Branch Clustering)
│   └── with subtask references 002.1-002.9
├── task-022.md (NEW - Initiative 4)
├── task-023.md (NEW - Initiative 4)
├── task-024.md (NEW - Initiative 5)
├── task-025.md (NEW - Initiative 5)
└── task-026.md (NEW - Initiative 5)
```

---

## Synchronization Tasks

### Phase 1: Documentation Clarification (HIGH PRIORITY)

**1.1: Update CLEAN_TASK_INDEX.md**

Current issues:
- Line 149: "Phase 3: Analysis & Clustering (021)" - should reference Task 002-Clustering
- Line 151: "1. Clustering system → 002 (parallel with Phase 2, enables Phases 4-5)" - correct but context unclear
- Lines 153-162: References to phases 022-026 correct, but these task files don't exist yet

Changes needed:
```
OLD (Line 149):
### Phase 3: Analysis & Clustering (021)

NEW:
### Phase 3: Analysis & Clustering (Task 002-Clustering, Initiative 3)
**Note:** This is a separate Task 002 from Initiative 1. It runs in parallel with Phase 2.
```

**1.2: Clarify Task 002 Dual Reference**

Add a note at top of CLEAN_TASK_INDEX.md:
```markdown
## ⚠️ Important: Task 002 Dual Reference

This project uses "Task 002" for **two different initiatives**:

1. **Task 002 (Merge Validation)** - Initiative 1 task (file: task-002.md)
2. **Task 002-Clustering** - Initiative 3 task (file: task-002-clustering.md) - runs parallel

Avoid confusion by using full names or adding initiative prefix.
```

**1.3: Update task_mapping.md (DONE)**
- ✅ Already updated with clarifications

---

### Phase 2: Create Missing Task Files (MEDIUM PRIORITY)

**2.1: Create Task 002-Clustering system file**

File: `task_files/task-002-clustering.md`

Should contain:
- 9 subtasks (002.1 through 002.9)
- Reference to TASK-002-CLUSTERING-SYSTEM-GUIDE.md for full details
- Stage breakdown (Stage One, Two, Three)
- Dependencies (parallel with Task 001)

**2.2: Create Execution Task Files**

Files needed:
- `task_files/task-022.md` - Scientific Branch Recovery
- `task_files/task-023.md` - Orchestration Tools Alignment

Content:
- Dependencies: Task 001, Task 002.9 (Clustering framework complete)
- Links to external guides if they exist
- Subtask structure

**2.3: Create Maintenance Task Files**

Files needed:
- `task_files/task-024.md` - Regression Prevention
- `task_files/task-025.md` - Conflict Resolution
- `task_files/task-026.md` - Dependency Refinement

Content:
- Dependencies: All previous tasks complete
- Can run in parallel with each other
- Links to specifications

---

### Phase 3: Verify Cross-References (LOW PRIORITY)

**3.1: Verify TASK-002-CLUSTERING-SYSTEM-GUIDE.md references**

Check:
- Line references to "21.1" through "21.9" (should reference 002.1-002.9)
- Consistency with TASK-002-SEQUENTIAL-EXECUTION-FRAMEWORK.md

**3.2: Verify dependency files**

Check:
- COMPREHENSIVE_DEPENDENCY_FRAMEWORK.md - ensure all Task 002 references are clear
- TASK_DEPENDENCY_VISUAL_MAP.md - ensure all task numbers are correct post-WS2

**3.3: Verify TASK-001-INTEGRATION-GUIDE.md (if it exists)**

Check:
- Week-by-week schedule references to Task 002 feedback
- Dependencies on Task 002.1-21.3 outputs

---

## Recommended Execution Order

1. **NOW:** Update CLEAN_TASK_INDEX.md (clarify Task 002 dual reference) ← HIGH PRIORITY
2. **NOW:** Create task-002-clustering.md (placeholder with structure) ← BLOCKS downstream understanding
3. **SOON:** Create task-022.md, task-023.md (execution tasks)
4. **SOON:** Create task-024.md, task-025.md, task-026.md (maintenance tasks)
5. **LATER:** Verify all cross-references in dependency documents

---

## Files to Create (Template)

### task-002-clustering.md Template

```markdown
# Task 002: Branch Clustering System (Initiative 3)

**Task ID:** 002-Clustering  
**Original ID:** Task 75  
**Status:** pending  
**Priority:** high  
**Initiative:** Advanced Analysis & Clustering (Initiative 3)  
**Sequence:** Parallel with Task 001  
**Duration:** 6-8 weeks (212-288h)  
**Parallelizable:** Yes (Stage One independent)

## Purpose

Advanced intelligent branch clustering and target assignment system. Analyzes commit history, codebase structure, and code differences to cluster branches and assign optimal integration targets.

## Detailed Guides

- **Full Guide:** [TASK-002-CLUSTERING-SYSTEM-GUIDE.md](./TASK-002-CLUSTERING-SYSTEM-GUIDE.md)
- **Sequential Execution:** [TASK-002-SEQUENTIAL-EXECUTION-FRAMEWORK.md](./TASK-002-SEQUENTIAL-EXECUTION-FRAMEWORK.md)

## Stage Breakdown

### Stage One: Parallel Analyzers (Weeks 1-2)
- 002.1: CommitHistoryAnalyzer (24-32h)
- 002.2: CodebaseStructureAnalyzer (28-36h)
- 002.3: DiffDistanceCalculator (32-40h)

### Stage Two: Clustering & Assignment (Weeks 3-4)
- 002.4: BranchClusterer (28-36h)
- 002.5: IntegrationTargetAssigner (24-32h)
- 002.6: PipelineIntegration (20-28h) [includes Task 007 merge]

### Stage Three: Outputs & Integration (Weeks 5-8)
- 002.7: VisualizationReporting (20-28h)
- 002.8: TestingSuite (24-32h)
- 002.9: FrameworkIntegration (16-24h)

## Success Criteria

- [ ] All 9 subtasks complete
- [ ] JSON outputs: categorized, clustered, enhanced orchestration
- [ ] 30+ tags per branch
- [ ] 90%+ test coverage
- [ ] Performance: 13 branches < 2 minutes
- [ ] Bidirectional feedback with Task 001 working

## Dependencies

**Must complete before:** Task 022, Task 023, Task 024, Task 025, Task 026

**Parallel with:** Task 001 (Framework Strategy)

**Feedback to:** Task 001 (real metrics validate framework assumptions)
```

### task-022.md Template

```markdown
# Task 022: Execute Scientific Branch Recovery

**Task ID:** 022  
**Original ID:** Task 23  
**Status:** pending  
**Priority:** high  
**Initiative:** Alignment Execution (Initiative 4)  
**Sequence:** After Task 001, Task 002.9  
**Duration:** 5-7 days (40-56h)

## Purpose

Execute the branch clustering and framework strategy on actual repository branches. Perform scientific branch recovery using outputs from Task 002 (Clustering) and Task 001 (Framework).

## Dependencies

- Task 001: Framework Strategy (REQUIRED)
- Task 002.9: FrameworkIntegration (REQUIRED)
- Task 004-015: Core framework tools (support)

## Success Criteria

- [ ] All target branches identified
- [ ] Recovery procedure executed
- [ ] Integration tests passing
- [ ] Documentation updated

## Subtasks

(To be defined based on actual implementation requirements)
```

---

## Verification Checklist

After completing syncing, verify:

- [ ] CLEAN_TASK_INDEX.md clarifies Task 002 dual reference
- [ ] task-002-clustering.md exists in task_files/
- [ ] task-022.md, task-023.md exist in task_files/
- [ ] task-024.md, task-025.md, task-026.md exist in task_files/
- [ ] All cross-references between files use consistent naming
- [ ] task_mapping.md accurately reflects new structure
- [ ] No broken links in documentation
- [ ] COMPREHENSIVE_DEPENDENCY_FRAMEWORK.md references are consistent

---

## Impact Assessment

**What this sync accomplishes:**

✅ Clarifies the complex Task 002 numbering situation  
✅ Documents complete Initiative 3 (Clustering) separately  
✅ Creates structure for Initiatives 4-5 (Execution & Maintenance)  
✅ Aligns documentation with actual task file organization  
✅ Enables clear task assignment and tracking  

**Risks if not done:**

❌ Confusion about Task 002 (two different uses)  
❌ Missing context for Clustering system work  
❌ Incomplete task tracking for Execution/Maintenance phases  
❌ Broken cross-references in dependency documents  

---

**Status:** Ready for execution  
**Priority:** HIGH (blocks clear task assignment)  
**Owner:** Task planning team  
**Timeline:** 2-3 hours to complete all phases
