# Phase 2-4 Decision Framework

**Created:** January 6, 2026  
**Purpose:** Evaluate and decide on approach for Phase 2 (Task 075 Retrofit), Phase 3 (Task 002.6-9 Migration), and Phase 4 (Remaining Tasks Retrofit)  
**Status:** Decision Pending

---

## Executive Summary

You have three distinct phases ahead with different scopes and effort profiles. Each phase has strategic choices that affect timeline, quality, and future maintainability.

### Phase Complexity Overview

| Phase | Task(s) | Size | Effort | Type | Dependency | Risk |
|-------|---------|------|--------|------|------------|------|
| 2 | Task 075 | 253 criteria across 5 subtasks | 2-3 weeks | Retrofit | None | Low |
| 3 | Task 002.6-9 | 253 criteria across 4 subtasks | 2-3 weeks | Migration | 002.5 complete | Medium |
| 4 | Tasks 001, 007, 079, 080, 083, 100, 101 | 300+ criteria across 7 tasks | 4-6 weeks | Retrofit | Varies | Medium-High |

**Total commitment:** 8-12 weeks full-time, or 4-6 months part-time

---

## Phase 2: Task 075 Retrofit

**What:** Rename task-75.X.md files to task_075.X.md and reformat to TASK_STRUCTURE_STANDARD.md template

**Current state:**
- 5 original files: task-75.1.md through task-75.5.md (with 253 success criteria)
- In archive: `/task_data/archived/backups_archive_task75/`
- Already analyzed/documented in ROOT_CAUSE_AND_FIX_ANALYSIS.md

### Approach Options

#### Option A: Shallow Retrofit (1 week)
**Do:** Rename files, add minimal formatting to match standard

**How:**
1. Rename task-75.1.md → task_075.1.md (preserve content as-is)
2. Add header, purpose, success criteria sections (extract from existing)
3. Keep implementation guides as-is (no rewriting)
4. Verify all 253 criteria preserved
5. Test compatibility with IMPLEMENTATION_INDEX.md

**Effort:** 40-50 hours (1 person, 1 week)

**Quality:** 6/10 - Minimum viable, preserves content, some standardization

**Pros:**
- Quick completion
- Preserves all criteria
- Creates working task files immediately
- Can start Task 002 implementation in parallel

**Cons:**
- Doesn't deeply apply standard template
- Implementation guides may stay scattered
- Next retrofit phase harder (cleanup debt)
- Integration with 002.X may need adjustment

---

#### Option B: Deep Retrofit (2-3 weeks)
**Do:** Full conversion to TASK_STRUCTURE_STANDARD.md template with all 14 sections

**How:**
1. Read original task-75.1-5.md files completely
2. Extract and organize 253 criteria into standard format
3. Restructure implementation guides into TASK_STRUCTURE_STANDARD.md format
4. Separate concerns: spec/steps/testing/gotchas into proper sections
5. Add Helper Tools (Optional) sections using template from 002.1.md
6. Comprehensive verification and cross-linking
7. Update IMPLEMENTATION_INDEX.md, add TASK_075_RETROFIT_COMPLETE.md

**Effort:** 80-120 hours (1-2 people, 2-3 weeks)

**Quality:** 9/10 - Full standard, well-organized, future-proof

**Pros:**
- Consistent with Task 002 structure
- Easier future retrofits (pattern established)
- All information centralized per task
- Prevents information scattering
- Cleaner integration with Phase 3 & 4

**Cons:**
- Longer timeline
- More upfront investment
- Requires detailed review of task-75 content
- May discover missing information

---

#### Option C: Hybrid Retrofit (1.5 weeks)
**Do:** Rename files + apply standard header/sections + keep existing implementation as-is

**How:**
1. Rename task-75.1.md → task_075.1.md
2. Add standard sections: Header, Purpose, Success Criteria, Prerequisites, Testing Strategy
3. Preserve existing sub-subtask breakdown and implementation guidance
4. Add Helper Tools template section
5. Quick verification pass (no deep rewrite)
6. Document migration status

**Effort:** 50-70 hours (1 person, 1.5 weeks)

**Quality:** 7.5/10 - Balanced standardization, preserves content, some cleanup

**Pros:**
- Moderate timeline
- Better than shallow, not as demanding as deep
- Preserves working content
- Can continue to Phase 3

**Cons:**
- Inconsistent with full template
- May still need Phase 5 cleanup
- Integration complexity medium

---

## Phase 3: Task 002.6-9 Migration

**What:** Migrate deferred tasks from task-75.6-9.md into new task_002.6.md through task_002.9.md with full structuring

**Current state:**
- Original specs in task-75.6-9.md (archived)
- 253 success criteria documented
- Deferred as Phase 3 work

**Dependency:** Task 002.5 (IntegrationTargetAssigner) must be complete

### Approach Options

#### Option A: Immediate Full Migration (2-3 weeks, start after Phase 1.5)
**Do:** Create task_002.6-9.md immediately after 002.5, using full TASK_STRUCTURE_STANDARD.md

**Timeline:**
- Week 3-4 of project: Phase 1.5 (1 week)
- Week 4-6: Phase 2 (Task 075, 2 weeks, parallel with 002.1-5 implementation)
- Week 6-8: Phase 3 (Task 002.6-9, 2 weeks, after 002.5 complete)

**Effort:** 80-100 hours (1-2 people, 2-3 weeks)

**Quality:** 9/10 - Full standard, immediate integration

**Pros:**
- All Task 002 tasks have consistent structure
- Can start Phase 4 earlier
- While 002.1-5 being implemented, Phase 3 docs ready
- Complete Task 002 story before Phase 4

**Cons:**
- 3 concurrent phase efforts demanding
- May conflict with 002.1-5 implementation schedule
- Requires deep understanding of Task 002 architecture

---

#### Option B: Deferred Migration (start after Phase 2, 2-3 weeks)
**Do:** Complete Phase 2 first, then migrate Task 002.6-9 with benefit of Phase 2 learnings

**Timeline:**
- Week 1: Phase 1.5 (Helper Tools)
- Week 1-2: Phase 2 (Task 075 retrofit) OR immediately parallel with 002.1-5 impl
- Week 2-6: Task 002.1-5 implementation
- Week 6-8: Phase 3 (Task 002.6-9 migration)

**Effort:** 80-100 hours (1 person, 2-3 weeks, deferred)

**Quality:** 9/10 - Benefits from Phase 2 learnings

**Pros:**
- Team focused on 002.1-5 implementation first
- Phase 2 retrofit establishes patterns for Phase 3
- Less context-switching
- Better understanding of TASK_STRUCTURE_STANDARD by team

**Cons:**
- Task 002.6-9 not ready for parallel work
- Longer total timeline
- May discover missing dependencies late

---

#### Option C: Lightweight Specs (start now, full later)
**Do:** Create task_002.6-9.md with minimal structure NOW (title + success criteria only), full standard formatting LATER in Phase 3 proper

**Timeline:**
- Now: Create lightweight task_002.6.md through task_002.9.md (2-3 hours)
- Weeks 1-6: Task 002.1-5 implementation (can reference 002.6-9 for integration points)
- Weeks 6-8: Full Phase 3 retrofit + integration

**Effort:** 3-5 hours now + 60-80 hours in Phase 3 (deferred)

**Quality:** 6/10 initially, 9/10 after Phase 3

**Pros:**
- Minimal upfront effort
- Docs exist for reference during 002.1-5 impl
- No blocking on full structure
- Can adjust based on 002.1-5 actual implementation

**Cons:**
- Incomplete docs during 002.1-5 work
- Developers work from incomplete specs
- Two-phase effort for one set of tasks
- May need rework based on 002.1-5 output

---

## Phase 4: Remaining Tasks Retrofit

**What:** Task 001, 007, 079, 080, 083, 100, 101 (7 tasks, 300+ criteria total)

**Current state:** Mostly existing as consolidated markdown files, need audit and restructuring

**Key Unknown:** Task 001 scope needs verification (appears to be massive)

### Approach Options

#### Option A: Full Retrofit (4-6 weeks)
**Do:** All 7 tasks converted to TASK_STRUCTURE_STANDARD.md with full 14 sections

**Effort:** 200-300 hours (2-3 people, 4-6 weeks)

**Quality:** 9/10 - Complete standardization, all preserved

**Pros:**
- Entire project standardized
- No scattered information across versions
- Prevents future consolidation problems
- Complete audit trail of all 600+ criteria

**Cons:**
- Significant effort
- Requires understanding diverse task domains
- May discover missing information across 7 tasks
- Tight coupling to Phase 2-3 completion

---

#### Option B: Selective Retrofit (2-4 weeks)
**Do:** 3 highest-priority tasks (need to verify which) get full retrofit, others get lightweight treatment

**Effort:** 100-150 hours (1-2 people, 2-4 weeks)

**Quality:** 7/10 - Mixed approach

**Pros:**
- Focuses effort on critical paths
- Reduces total work
- Still improves most important tasks
- Can defer less critical tasks

**Cons:**
- Inconsistent standardization
- Still leaves cleanup debt
- Must decide which 3 are "highest priority"

---

#### Option C: Defer Phase 4 (focus on Phase 2-3)
**Do:** Complete Phase 2-3 fully, then assess Phase 4 scope before committing

**Timeline:**
- Weeks 1-2: Phase 1.5 (Helper Tools) ✅
- Weeks 2-8: Phase 2-3 (Task 075 + Task 002.1-9) - **Focus here**
- Weeks 8+: Phase 4 (Remaining tasks) - **Decide later**

**Effort:** 0 hours now, decision after Phase 3

**Quality:** Allows proper assessment

**Pros:**
- No overcommitment now
- Can see actual work patterns from Phase 2-3
- Team feedback informs Phase 4 approach
- May discover Phase 4 not needed (if 002 tasks sufficient)

**Cons:**
- Defers cleanup indefinitely
- Remaining tasks stay in scattered state
- Risk of Phase 4 becoming "technical debt"

---

## Decision Matrix

### Which approach for each phase?

#### Phase 2 Decision (Task 075)

Choose based on your priorities:

| If You Want... | Choose |
|---|---|
| Quick progress on Task 002.1-5 impl | **Shallow Retrofit (A)** |
| Consistent template across all tasks | **Deep Retrofit (B)** |
| Balanced approach, good enough | **Hybrid Retrofit (C)** |
| Parallel work, minimize blocking | **Shallow or Hybrid** |
| Best future maintainability | **Deep Retrofit** |

**Recommendation:** **Shallow or Hybrid (A or C)**
- Allows Task 002.1-5 implementation to proceed immediately
- Can revisit Task 075 quality later if needed
- Pattern established from shallow/hybrid work informs Phase 3-4

---

#### Phase 3 Decision (Task 002.6-9)

Choose based on dependencies:

| If... | Choose |
|---|---|
| Want all Task 002 work together | **Immediate Full Migration (A)** |
| Want to learn from Phase 2 first | **Deferred Migration (B)** |
| Want minimal blocking | **Lightweight Specs (C)** |
| Developers need complete specs immediately | **Immediate Migration (A)** |
| Want flexibility to adjust based on impl | **Lightweight Specs (C)** |

**Recommendation:** **Deferred Migration (B)** or **Lightweight Specs (C)**
- B: Clean, sequential approach, learns from Phase 2
- C: Minimum viable docs now, full specs later
- Both support parallel Task 002.1-5 implementation

---

#### Phase 4 Decision (Tasks 001, 007, 079, etc.)

**Critical blocker:** Need to understand Task 001 scope first

| If Task 001 is... | Recommend |
|---|---|
| Small/simple | **Selective Retrofit (B)** - Task 001 + 2 others |
| Medium (2-3 subtasks) | **Selective Retrofit (B)** - Do 3-4 tasks |
| Large (5+ subtasks) | **Defer Phase 4 (C)** - Assess after Phase 2-3 |

**Recommendation:** **Defer Phase 4 (C)** until Task 001 scope verified

---

## Summary Table: My Recommended Approach

| Phase | Task | Recommendation | Effort | Timeline | Start |
|-------|------|---|---|---|---|
| 1.5 ✅ | Helper Tools | Complete | ✅ Done | ✅ Done | ✅ Done |
| 2 | Task 075 | **Shallow (A)** | 40-50h | 1 week | Parallel with 2.1-5 |
| 3 | Task 002.6-9 | **Lightweight Specs (C)** | 3-5h now | 1-2 hours | This week |
| 3 | Task 002.6-9 | Then **Full Migration (B)** | 60-80h later | 1.5-2 weeks | Week 6+ |
| 4 | Tasks 001, 007, etc | **Defer (C)** | 0h now | Decision later | After Phase 3 |

**Total 8-Week Plan:**
- Week 1: Phase 1.5 (Helper Tools) ✅ + Phase 3 Lightweight Specs (3-5h)
- Weeks 1-2 (parallel): Phase 2 (Task 075 Shallow, 40-50h)
- Weeks 2-6: Task 002.1-5 implementation (primary focus)
- Weeks 6-8: Phase 3 Full Migration (Task 002.6-9, 60-80h)
- Week 8+: Assess Phase 4 based on learnings

**Advantages:**
- Unblocks Task 002.1-5 implementation immediately
- Creates working Task 075 without delay
- Provides Task 002.6-9 specs for reference during 002.1-5 work
- Defer Phase 4 complexity until better understood
- Sequential execution = clear focus
- Reduces context-switching

---

## Your Decision: What Would You Like to Do?

I can help execute any of these combinations. Just let me know:

1. **Phase 2 (Task 075):** Which approach? (Shallow/Hybrid/Deep)
2. **Phase 3 (Task 002.6-9):** Which approach? (Immediate/Deferred/Lightweight now)
3. **Phase 4 (Remaining tasks):** Defer now? (Recommend yes until Task 001 scope clear)

Once you decide, I can:
- Start Phase 2 immediately (rename files, structure accordingly)
- Create Phase 3 lightweight specs (30 minutes)
- Audit Task 001 to inform Phase 4 decision (1-2 hours)

---

## Questions to Help Decide

1. **How soon do you need Task 002.6-9 available?**
   - This week (→ Lightweight Specs)
   - After 002.5 complete (→ Deferred Migration)
   - Immediately full (→ Immediate Full Migration)

2. **What's your team composition?**
   - 1 person total (→ Shallow, deferred phases)
   - 2-3 people total (→ Hybrid, parallel phases)
   - 4+ people total (→ Deep, all parallel)

3. **Is Task 001 scope known?**
   - Small (< 50 criteria) (→ Include in Phase 4)
   - Medium (50-200 criteria) (→ Include in Phase 4)
   - Unknown/large (→ Audit first, defer decision)

4. **How important is standardization?**
   - "Just get it done" (→ Shallow approaches)
   - "Consistency matters" (→ Deep approaches)
   - "Balanced" (→ Hybrid approaches)

**Once you answer these, I can give you a concrete action plan.**
