# New Task Plan Processing: Decision Summary

**Decision Date:** January 6, 2026  
**Status:** READY TO EXECUTE  
**Recommended Path:** C (Extraction + Guidance + Execution Planning)  
**Estimated Effort:** 16-20 hours over 4-5 days  

---

## What We're Doing

**Transform** new_task_plan/ from planning documents into an **independent, executable subtask markdown system** that teams can use immediately.

**Current State:**
- ✅ Planning documents exist (README.md, CLEAN_TASK_INDEX.md, task_mapping.md)
- ❌ Individual subtask files missing (task-002-1.md through task-002-9.md, etc.)
- ❌ Guidance not integrated into task specs
- ❌ No parallel execution planning

**Target State:**
- ✅ ~130+ individual task files (one per subtask)
- ✅ Each file follows TASK_STRUCTURE_STANDARD.md (14 sections)
- ✅ Guidance integrated (Implementation Considerations section)
- ✅ Execution strategies documented (parallel, sequential, hybrid)
- ✅ Teams can start immediately

---

## Critical Files to Process

### Files That Need Extraction (Phase 1)
| Source File | What's Inside | Extraction Needed |
|-------------|---------------|-------------------|
| task-002.md | 9 subtasks (Merge Validation) | Extract to task-002-1.md through task-002-9.md |
| task-002-clustering.md | 9 subtasks (Branch Clustering) | RENAME to task-021.md, extract to task-021-1.md through task-021-9.md |
| task-001.md | 4 subtasks (Framework) | Extract to task-001-1.md through task-001-4.md |
| Other task-*.md | Multiple subtasks each | Extract to individual task-XXX-Y.md files |

### Guidance Files to Integrate (Phase 2)
| Source | Location | Extract For |
|--------|----------|------------|
| ARCHITECTURE_ALIGNMENT_COMPLETE_AND_RECOMMENDATIONS.md | task_data/guidance/ | Task 001-003 (Foundational) |
| FINAL_MERGE_STRATEGY.md | task_data/guidance/ | Task 002-020 (Core Framework) |
| MERGE_GUIDANCE_DOCUMENTATION.md | task_data/guidance/ | Task 021 (Clustering) |
| Phase findings (14 directories) | task_data/findings/ | Add to "Implementation Considerations" |

### Planning Files to Create (Phase 3)
| New File | Purpose |
|----------|---------|
| EXECUTION_STRATEGIES.md | Explain Parallel, Sequential, Hybrid modes |
| CRITICAL_PATH.md | Show 16-18 week baseline timeline |
| PARALLEL_EXECUTION.md | Show 8-10 week with 5-person teams |
| GUIDANCE_INDEX.md | Searchable index of all guidance |

---

## The Task 002/Task 021 Naming Issue (RESOLVED)

**Problem:** Two tasks both called "Task 002"
- Task 002 = Merge Validation (Initiative 1) ← Keep this as task-002.md
- Task 002-Clustering = Branch Clustering (Initiative 3, old Task 75) ← Rename to task-021.md

**Solution:**
```
NEW FILE STRUCTURE:
task_files/
├── task-002.md                    # Initiative 1 Task 2 (Merge Validation)
├── task-002-1.md through task-002-9.md   # 9 subtasks
├── task-021.md                    # Initiative 3 Task 21 (Branch Clustering, old Task 75)
└── task-021-1.md through task-021-9.md   # 9 subtasks
```

This matches:
- tasks.json (task-master CLI) which has Task 2 (Merge) and Task 21 (Clustering renamed from 75)
- Old task IDs: Task 75 (old) → Task 21 (new clean numbering) → Task 002 (confusing) → back to Task 21 (clarified)

---

## The 4 Processing Phases

### Phase 1: Extract and Standardize (Days 1-2, 4-6h)
**Goal:** Convert parent task files into individual subtask files

**Deliverables:**
- [ ] task-002-1.md through task-002-9.md (9 files from task-002.md)
- [ ] task-021-1.md through task-021-9.md (9 files from renamed task-002-clustering.md)
- [ ] task-001-1.md through task-001-4.md (4 files from task-001.md)
- [ ] Similar for all other task files
- [ ] All files follow TASK_STRUCTURE_STANDARD.md (14 sections)
- [ ] All files use dash notation (task-XXX-Y.md, not task-XXX_Y.md)

**Key Template:** Each file must have these 14 sections:
```markdown
# Task XXX.Y: [Subtask Name]
## Status, Priority, Effort, Complexity, Dependencies
## Purpose
## Success Criteria (DETAILED - ALL original criteria preserved)
## Prerequisites & Dependencies
## What to Build (Specification)
## Implementation Guide (Step-by-step)
## Performance Baselines
## Test Cases & Validation
## Code Examples (if applicable)
## Edge Cases & Error Handling
## Integration Points
## Common Pitfalls
## References (links to related tasks, guidance)
## Progress Tracking (template for logging work)
```

---

### Phase 2: Integrate Guidance (Days 2-3, 4-6h)
**Goal:** Connect tasks to existing guidance/findings

**Deliverables:**
- [ ] Create new_task_plan/guidance/ directory structure
- [ ] Extract 9 guidance documents from task_data/guidance/
- [ ] Extract phase findings from task_data/findings/
- [ ] Add "Implementation Considerations" section to each task file
- [ ] Create new_task_plan/GUIDANCE_INDEX.md with:
  - Searchable index of all guidance documents
  - Links to relevant guidance for each task
  - Architecture patterns and lessons learned
- [ ] Update README.md with guidance references

**Output:**
```
new_task_plan/guidance/
├── README.md
├── architecture_alignment/
│   ├── HYBRID_APPROACH.md
│   ├── ARCHITECTURAL_PATTERNS.md
│   └── MERGE_PATTERNS.md
├── merge_strategy/
│   ├── FINAL_MERGE_STRATEGY.md
│   ├── HANDLING_INCOMPLETE_MIGRATIONS.md
│   └── CONFLICT_RESOLUTION.md
├── implementation_lessons/
│   ├── IMPLEMENTATION_SUMMARY.md
│   ├── BEST_PRACTICES.md
│   └── COMMON_PITFALLS.md
└── phase_findings/
    └── [14 phase directories with research findings]
```

---

### Phase 3: Create Execution Plans (Days 3-4, 6-8h)
**Goal:** Document how to execute all 26 tasks (serial vs. parallel)

**Deliverables:**
- [ ] **EXECUTION_STRATEGIES.md** - Explain 3 execution modes:
  - **Sequential:** 1 person, 6-8 weeks, do tasks one at a time
  - **Parallel:** 5 people, 8-10 weeks, 11 parallelizable tasks
  - **Hybrid:** 3 people, 10-12 weeks, some parallel some serial
  
- [ ] **CRITICAL_PATH.md** - Show dependency chain:
  - Task 001 → Task 002 → Tasks 003-020 → Tasks 022-026
  - 16-18 week baseline (sequential)
  - Identify which tasks are dependent (can't parallel)
  - Identify which are independent (can parallel)

- [ ] **PARALLEL_EXECUTION.md** - Team allocation:
  - Which 5 people do which tasks
  - Weekly sync points
  - Milestone dates
  - Risk areas

- [ ] Update each task file with "Execution Context" section:
  - Can this run in parallel? (Yes/No)
  - Can this start immediately? (Yes/No/After task X)
  - Which team member should own this?
  - What's the critical deadline?

---

### Phase 4: Validate and Complete (Day 4, 2-4h)
**Goal:** Ensure everything is complete and consistent

**Deliverables:**
- [ ] **Validation Report:**
  - All task files have 14 TASK_STRUCTURE_STANDARD sections
  - All files use dash notation (task-XXX-Y.md)
  - No broken links
  - All cross-references valid
  
- [ ] **Updated Cross-Reference Files:**
  - task_mapping.md: Add new file locations
  - CLEAN_TASK_INDEX.md: Note that subtask files now available
  - README.md: Explain new structure

- [ ] **PROCESSING_COMPLETION_REPORT.md:**
  - What was extracted
  - What was added
  - What's ready for teams
  - Known limitations/gaps

---

## How to Use This Document

1. **Read it completely first** (5 min)
2. **Choose your path** (should be Path C: Extraction + Guidance + Execution Planning)
3. **Follow the phases in order** (can't skip; each builds on previous)
4. **Use the templates in Phase 1** (14-section standard)
5. **Check off each deliverable** as you complete it
6. **Create PROCESSING_COMPLETION_REPORT.md** when done

---

## What SUCCESS Looks Like

### After Phase 1: Extract and Standardize (Days 1-2)
- ✅ 100+ individual task files exist (task-001-1.md, task-002-1.md, etc.)
- ✅ All files follow the 14-section template
- ✅ All files use dash notation (task-XXX-Y.md)
- ✅ team can open task-002-1.md and see everything needed for that subtask

### After Phase 2: Integrate Guidance (Days 2-3)
- ✅ Guidance documents are in new_task_plan/guidance/
- ✅ Each task file has "Implementation Considerations" section
- ✅ Teams know where to find relevant guidance
- ✅ GUIDANCE_INDEX.md helps search for answers

### After Phase 3: Create Execution Plans (Days 3-4)
- ✅ EXECUTION_STRATEGIES.md explains all 3 modes
- ✅ CRITICAL_PATH.md shows 16-18 week timeline
- ✅ PARALLEL_EXECUTION.md shows 8-10 week with teams
- ✅ Teams know which tasks can run in parallel and which must wait

### After Phase 4: Validate and Complete (Day 4)
- ✅ PROCESSING_COMPLETION_REPORT.md documents what was done
- ✅ No broken links, no missing sections, all cross-references valid
- ✅ System is complete and ready to hand off to development teams

---

## Key Dates and Milestones

| Date | Phase | Deliverable | Success Criteria |
|------|-------|-------------|-----------------|
| Jan 6 (Today) | 0 | Evaluation & Decision | ✅ COMPLETE |
| Jan 7-8 | 1 | Extract & Standardize | 100+ files, 14 sections each |
| Jan 9 | 2 | Integrate Guidance | guidance/ created, 9 docs extracted |
| Jan 9-10 | 3 | Execution Plans | 3 strategy docs created |
| Jan 10 | 4 | Validate & Complete | 100% validation passed |
| Jan 11 | -- | **READY FOR TEAMS** | **Development can begin** |

---

## References

### Standards
- TASK_STRUCTURE_STANDARD.md (14-section template)
- complete_new_task_outline_ENHANCED.md (full specs)

### Source Material
- task_data/task-7.md (Task 001)
- task_data/HANDOFF_*.md (Task 021 / old Task 75)

### Planning
- CLEAN_TASK_INDEX.md (current status)
- task_mapping.md (old ID → new ID)
- INTEGRATION_EXECUTION_CHECKLIST.md (execution plan)

### Full Evaluation
- NEW_TASK_PLAN_EVALUATION_AND_PROCESSING_PLAN.md (complete analysis)

---

**Ready to begin Phase 1? Start with extracting task-002.md → individual task-002-1.md through task-002-9.md files.**

---

**Document Version:** 1.0  
**Created:** January 6, 2026  
**Status:** APPROVED FOR EXECUTION  
**Recommended Path:** C (Extraction + Guidance + Execution Planning)
