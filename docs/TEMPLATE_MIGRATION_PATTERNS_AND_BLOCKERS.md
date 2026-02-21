# Template Migration Patterns & Blockers: What Archive Reveals

**Date:** January 6, 2026  
**Status:** Investigation complete  
**Purpose:** Synthesize archive findings into actionable patterns to avoid repeating failures

---

## Executive Summary

Archive investigation reveals a **repeating cycle of incomplete migrations**:

1. **Problem created** → Solution created → Solution never applied consistently → Problem persists
2. This has happened **3 times** in the past 2 weeks (Task 75 separation, consolidation loss, improvement template not applied)
3. **Current migration (TASK_STRUCTURE_STANDARD.md) is at risk of repeating** this pattern
4. **Prevention requires breaking the cycle** with explicit completion criteria and weekly verification

---

## The Repeating Cycle

### Cycle 1: Task 75 Structure (Dec 2025 - Jan 4, 2026)

**Problem Identified:** Documentation separated from implementation → 8-10 hours wasted per task

**Solution Created:** IMPROVEMENT_TEMPLATE.md with 6 new sections
- Quick Navigation
- Performance Baselines  
- Subtasks Overview
- Configuration & Defaults
- Development Workflow
- Integration Handoff

**Application Status:** ❌ Created but never applied
- Template completed Jan 4
- Would take 40-50 hours to apply systematically
- Timeline pressure caused focus to shift
- **Result:** Potential 100+ hours saved by application lost to inaction

### Cycle 2: Consolidation Attempt (Jan 5, 2026)

**Problem Identified:** Task 75 (9 files) too many to manage → Consolidate into Task 002

**Solution Attempted:** Merge into task_002.md + task_002-clustering.md

**Result:** ❌ Catastrophic failure
- 530 success criteria → 7 visible
- 98.7% data loss
- Problem: No verification step, no before/after comparison
- No one noticed until retroactive audit

### Cycle 3: Current Migration (Jan 6, 2026)

**Problem Identified:** Consolidation lost 98.7% of criteria → Need better structure

**Solution Created:** TASK_STRUCTURE_STANDARD.md (14 sections)
- Incorporates lessons from all previous attempts
- SUBTASK_MARKDOWN_TEMPLATE.md provided
- MIGRATION_STATUS_ANALYSIS.md describes gap (45% complete, inconsistent)

**Status:** ❓ At critical juncture
- All 11 tasks need expansion (40-50 hours)
- Only task-002-1 currently compliant
- No automatic application mechanism
- No weekly verification plan
- **Risk:** Becomes Cycle 4 (created but not applied)

---

## Root Causes of Migration Failure

### Root Cause 1: "Later" Never Arrives

**Pattern:**
- Month 1: Create template
- Month 2: "We'll apply it after current sprint"
- Month 3: "We'll apply it next quarter"
- Month 6: Template archived, never applied

**Evidence:**
- IMPROVEMENT_TEMPLATE.md (Jan 4) → Now (Jan 6) = 2 days of non-application
- Original task-75 files (Dec 2025) → Now (Jan 6) = 2+ weeks of living with separation problem

**Prevention:**
- ❌ Don't: "We'll apply this template later"
- ✅ Do: "Week 1 apply to files A-B, Week 2 apply to files C-D"
- ✅ Do: Build application into sprint as task, not as "cleanup"

### Root Cause 2: No Completion Verification

**Pattern:**
- Apply template to 1-2 files
- Assume it's "obvious" why others weren't updated
- No one verifies completeness
- Find out much later some files were skipped

**Evidence:**
- Consolidation loss: No one compared criteria count (530 → 7)
- task-002-1 compliant but 002-2 through 002-9 not → Gap discovered in audit
- IMPROVEMENT_TEMPLATE applied to 0 of 9 target files → Never noticed

**Prevention:**
- ❌ Don't: Assume files are correct without verification
- ✅ Do: Build verification checklist with measurable criteria
  - "All files have exactly 14 ## sections"
  - "All files are 350+ lines"
  - "No file is missing Implementation Guide section"

### Root Cause 3: Partial Application Looks Complete

**Pattern:**
- 1 file complies with standard (task-002-1.md) ✅
- Remaining 10 files don't (task-002-2 through 002-9, 001, 014, etc.) ❌
- Project assumes "migration is complete" because "at least one file is done"

**Evidence:**
- Current state: task-002-1 = 285 lines with all 14 sections
- Remaining tasks: 123-228 lines with 6-8 sections
- Gap undetected until audit

**Prevention:**
- ❌ Don't: Count "1 file done = migration complete"
- ✅ Do: Define "complete" as "ALL FILES compliant"
- ✅ Do: Use binary pass/fail checklist (0 or 11 files, nothing in between)

### Root Cause 4: No Blockage if Migration Skipped

**Pattern:**
- Alternative paths exist for developers
- Can work around missing structure
- No forcing function to apply standard

**Evidence:**
- Even if tasks 002-2-9 aren't expanded, developers can still work (though painfully)
- No build step blocks on non-compliance
- No code review requires section count

**Prevention:**
- ❌ Don't: Hope developers will use new structure
- ✅ Do: Make non-compliance a blocking issue
- ✅ Do: Add automated check: `./scripts/verify_task_structure.sh`
- ✅ Do: Require passing test for merge

---

## Critical Differences This Time (Positive Signs)

### Difference 1: Root Cause Documented

✅ This investigation (ARCHIVE_INVESTIGATION_FINDINGS.md) explains:
- Why Task 75 failed (separation cost 8-10 hrs per task)
- Why consolidation failed (no verification)
- Why IMPROVEMENT_TEMPLATE wasn't applied (timeline pressure)
- Patterns to avoid (3 cycles of incomplete migration)

**Previous attempts:** Created solution without documenting why problem existed

### Difference 2: All Lessons Consolidated

✅ TASK_STRUCTURE_STANDARD.md incorporates ALL previous template attempts:
- Quick Navigation (from IMPROVEMENT_TEMPLATE)
- Performance Targets (from IMPROVEMENT_TEMPLATE)  
- Development Workflow (from IMPROVEMENT_TEMPLATE)
- Gotchas & Solutions (from IMPROVEMENT_TEMPLATE)
- Implementation Guide (lessons from Task 75 separation)
- Configuration Parameters (from IMPROVEMENT_TEMPLATE)

**Previous attempts:** Each solution isolated; lessons not consolidated

### Difference 3: Explicit Migration Plan

✅ MIGRATION_STATUS_ANALYSIS.md provides:
- Specific files needing expansion (002-2 through 002-9)
- Effort estimate (40-50 hours for all 11 tasks)
- Weekly breakdown (4 tasks per week = 12.5 hours/week)
- Success metrics (each task 350+ lines with 14 sections)
- Verification checklist

**Previous attempts:** "Apply template when you have time" (= never)

### Difference 4: Template Ready to Apply

✅ SUBTASK_MARKDOWN_TEMPLATE.md provides:
- Copy-paste ready 14-section structure
- All placeholders marked `[...]`
- Instructions for each section
- Quick reference validation checklist

**Previous attempts:** Template created but required interpretation/customization

---

## The Blocker: Partial vs. Complete Compliance

### Current State (As of Jan 6, 2026)

| Task | File | Lines | Status | Gap |
|------|------|-------|--------|-----|
| 002-1 | task-002-1.md | 285 | ✅ Complete | None |
| 002-2 | task-002-2.md | 209 | ❌ Partial | 141-191 lines + 8 sections |
| 002-3 | task-002-3.md | 123 | ❌ Stub | 227-277 lines + 9 sections |
| 002-4 | task-002-4.md | 198 | ❌ Partial | 152-202 lines + 8 sections |
| 002-5 | task-002-5.md | 172 | ❌ Partial | 178-228 lines + 8 sections |
| 002-6 | task-002-6.md | 186 | ❌ Partial | 164-214 lines + 8 sections |
| 002-7 | task-002-7.md | 148 | ❌ Stub | 202-252 lines + 10 sections |
| 002-8 | task-002-8.md | 158 | ❌ Stub | 192-242 lines + 10 sections |
| 002-9 | task-002-9.md | 228 | ❌ Partial | 122-172 lines + 6 sections |
| 001 | task-001.md | ? | ? | ? |
| 014 | task-014.md | ? | ? | ? |
| 016 | task-016.md | ? | ? | ? |
| 017 | task-017.md | ? | ? | ? |

**Completion Percentage: 8.3% (1 of 11 files compliant)**

### The Blocker

As long as only task-002-1 is compliant:
- ✅ Can claim "standard is being applied"
- ❌ But 91.7% of tasks still don't follow it
- ❓ Next developer might think this is "acceptable partial compliance"
- ❌ Pattern repeats: Template created but not fully applied

**Solution:** Move completion bar to 100% (all 11 files) or 0% (none), nothing in between.

### Migration Checkpoint Definition

**INCOMPLETE Migration (current state):**
```
✅ task-002-1: Complete (285 lines, 14 sections)
❌ task-002-2: Partial (209 lines, 6 sections)  
❌ task-002-3: Stub (123 lines, 5 sections)
...
```
Status: 1/11 = 8.3% → NOT ACCEPTABLE

**COMPLETE Migration (required state):**
```
✅ task-002-1: Complete (285 lines, 14 sections)
✅ task-002-2: Complete (350+ lines, 14 sections)
✅ task-002-3: Complete (350+ lines, 14 sections)
...
✅ task-017: Complete (350+ lines, 14 sections)
```
Status: 11/11 = 100% → ACCEPTABLE

**NO MIDDLE GROUND** is allowed. Once migration starts, it must complete.

---

## Weekly Verification Checklist

To prevent this from becoming Cycle 4 (created but not applied), track weekly:

### Week 1 (Jan 6-12)

**Target Files:** task-002-2, task-002-3  
**Success Criteria:**
- [ ] task-002-2: `grep "^##" task-002-2.md | wc -l` = 14
- [ ] task-002-2: `wc -l task-002-2.md` ≥ 350
- [ ] task-002-3: `grep "^##" task-002-3.md | wc -l` = 14
- [ ] task-002-3: `wc -l task-002-3.md` ≥ 350
- [ ] Both files reviewed for content quality (not just length)
- [ ] Both files git committed with message "feat: expand task-XXX to standard"

**Status Check (Friday):**
- ✅ If all criteria met → Week 2 proceeds
- ❌ If any criteria not met → Escalate, extend Week 1

### Week 2 (Jan 13-19)

**Target Files:** task-002-4, task-002-5  
**Same verification as Week 1**

### Week 3 (Jan 20-26)

**Target Files:** task-002-6, task-002-7  
**Same verification as Week 1**

### Week 4 (Jan 27 - Feb 2)

**Target Files:** task-002-8, task-002-9  
**Same verification as Week 1**

### Week 5 (Feb 3-9)

**Target Files:** task-001, task-014, task-016, task-017  
**Same verification as Week 1 (may take full 5 days)**

**FINAL CHECKPOINT:**
```bash
# Verify ALL 11 files
for task in 001 002-1 002-2 002-3 002-4 002-5 002-6 002-7 002-8 002-9 014 016 017; do
  count=$(grep "^##" task-${task}.md | wc -l)
  lines=$(wc -l < task-${task}.md)
  echo "task-${task}: $count sections, $lines lines"
done

# Should show:
# task-001: 14 sections, 350+ lines
# task-002-1: 14 sections, 285+ lines  [already done]
# task-002-2: 14 sections, 350+ lines
# task-002-3: 14 sections, 350+ lines
# ... etc (all 11 files with 14 sections)
```

**If ALL pass:** Migration complete ✅ Mark in MIGRATION_STATUS_ANALYSIS.md  
**If ANY fail:** Cycle 4 has started ❌ Escalate immediately

---

## Preventing Cycle 4

### What Cycle 3 Needs to Succeed

1. **Commitment:** 40-50 hours allocated across 5 weeks (not "when we have time")
   - Not: "We'll get to this eventually"
   - Yes: "Week 1 = 2 tasks, Week 2 = 2 tasks, etc."

2. **Verification:** Weekly checklist with measurable criteria
   - Not: "Looks good to me"
   - Yes: `grep "^##" | wc -l` = 14 AND `wc -l` ≥ 350

3. **Blocking:** Prevent partial compliance
   - Not: "1 file done is better than 0"
   - Yes: "All 11 or nothing; 10/11 = not complete"

4. **Documentation:** Maintain audit trail
   - Each week: Record which files passed verification
   - Final week: Sign-off that all 11 files meet standard

5. **Archive Prevention:** Ensure this applies going forward
   - All NEW tasks MUST follow TASK_STRUCTURE_STANDARD.md from creation
   - Code review checklist must verify 14 sections present

### Preventing Future Template Loss

For any future standard/template created:

```
Standard Created → MUST DO
├── Document root cause (why standard needed)
├── Define scope (which files apply)
├── Create reusable template
├── Create gap analysis
├── Create migration checklist with effort estimates
├── Assign owner (named person accountable)
├── Schedule in sprint (not "someday")
├── Build weekly verification
├── Create final audit
├── Update archive documentation
└── Prevent checklist (ensure all future files use it)

IF ANY STEP SKIPPED → HIGH RISK OF BECOMING CYCLE N+1
```

---

## Archive Materials to Reuse

For this migration, leverage existing archive materials:

### From IMPROVEMENT_TEMPLATE.md
- Task-specific customization notes (Gotchas section content)
- Performance baseline examples
- Configuration structure (YAML format examples)
- Development workflow patterns

### From task-75.X.md original files
- All 530 success criteria (preserved in archive)
- Performance targets per component
- Implementation checklists
- Test case examples
- Git commands reference

### From HANDOFF_75.X_...md files
- Implementation guidance content
- Common gotchas (extract to Section 11)
- Code examples and patterns
- Configuration examples

**Recommendation:** When expanding tasks 002-2 through 002-9:
1. Reference archive version of task-75.2-75.9
2. Extract performance targets and gotchas
3. Pull implementation guidance from HANDOFF files
4. Verify no content is lost in expansion process

---

## Success Definition

This migration is **SUCCESSFUL** when:

✅ **Compliance:** All 11 task files meet TASK_STRUCTURE_STANDARD.md
- 14 sections per file (verified: `grep "^##" | wc -l = 14`)
- 350+ lines per file (verified: `wc -l ≥ 350`)
- All sections have substantive content (not placeholder text)

✅ **Completeness:** No information is lost from archive sources
- Original task-75 success criteria preserved
- IMPROVEMENT_TEMPLATE ideas integrated
- HANDOFF content incorporated

✅ **Quality Gate:** Migration followed verification checklist
- Weekly section-count verification
- Weekly line-count verification
- Content quality spot-checks
- Final audit sign-off

✅ **Prevention:** Prevents future incomplete migrations
- New task checklist includes TASK_STRUCTURE_STANDARD.md requirement
- Code review verifies section count and content
- Archive documentation prevents repeating same mistakes

✅ **Timeline:** Completed by Feb 9, 2026 (5 weeks)
- Week 1: 2 tasks
- Week 2: 2 tasks
- Week 3: 2 tasks
- Week 4: 2 tasks
- Week 5: 3 tasks

---

## Conclusion

The archive reveals a clear pattern: **Templates created but not applied consistently**.

This migration (TASK_STRUCTURE_STANDARD.md → all 11 task files) is the **3rd attempt** to fix this. It will become the **4th incomplete migration** unless:

1. ✅ Weekly verification prevents silent partial compliance
2. ✅ All-or-nothing checkpoint (11 files or 0, nothing between)
3. ✅ Named owner accountable for completion
4. ✅ Migration scheduled in sprint (not "someday")
5. ✅ Archive materials actively reused (not just referenced)

**Key Insight from Archive:** Templates + templates + templates ≠ applied standards.

**What's different this time:** This is the 3rd time we're learning this lesson. Let's not need a 4th.

---

**Status:** Recommendations ready for implementation  
**Next Step:** Execute Week 1 verification plan (task-002-2, task-002-3)  
**Owner:** [Assign name here]  
**Timeline:** 5 weeks (Jan 6 - Feb 9, 2026)

---

Last Updated: January 6, 2026  
Reference: ARCHIVE_INVESTIGATION_FINDINGS.md, MIGRATION_STATUS_ANALYSIS.md
