# Agent Guidelines Quick Reference

**For navigating the three comprehensive documents about agent consistency issues.**

---

## 📋 Document Overview

### 1. **BRANCH_AGENT_GUIDELINES_SUMMARY.md**
**What**: Analysis of current state and consistency issues  
**Who Should Read**: Anyone wanting to understand what's inconsistent and why  
**Key Content**:
- Current context control profiles for all 3 branches
- Detailed breakdown of all 8 inconsistency issues
- Severity and impact assessment
- Verification checklist

**Time to Read**: 15-20 minutes  
**Action After Reading**: Decide if issues matter for your work

---

### 2. **AGENT_GUIDELINES_RESOLUTION_PLAN.md**
**What**: Root cause analysis + 6-week implementation plan  
**Who Should Read**: Project leads, branch maintainers, implementers  
**Key Content**:
- 8 root causes with evidence and timeline
- 5 implementation phases
- 28 specific tasks with effort estimates
- Success criteria and risk mitigation
- Responsible party assignments (to be filled)

**Time to Read**: 30-40 minutes (or 10 min for executive summary)  
**Action After Reading**: Assign tasks and begin Phase 1

---

### 3. **This Document**
**What**: Navigation guide to the other two documents  
**Who Should Read**: Everyone (you're reading it)  
**Content**:
- Quick lookup tables
- Issue-to-document mapping
- Timeline overview
- Common questions answered

**Time to Read**: 5 minutes

---

## 🎯 Quick Lookup by Use Case

### "I'm an agent working on orchestration-tools"
1. Read: BRANCH_AGENT_GUIDELINES_SUMMARY.md → Section "Orchestration-Tools Profile"
2. Understand: Which files you can access
3. Check: Your context limitations
4. Action: Follow orchestration-tools AGENTS.md (once updated in Phase 2)

**Read Time**: 5 min

---

### "I'm an agent working on scientific"
1. Read: BRANCH_AGENT_GUIDELINES_SUMMARY.md → Section "Scientific Profile" 
2. Issue Alert: Task Master scope ambiguous (Issue #5)
3. Check: AGENTS.md_ROOT_CAUSE → Task Master integration status
4. Action: Once Phase 2.3 completes, scientific AGENTS.md will have Task Master section

**Read Time**: 10 min

---

### "I'm fixing the consistency issues"
1. Read: AGENT_GUIDELINES_RESOLUTION_PLAN.md → Full document
2. Understand: Root causes (section starts at "Branch Divergence Without Synchronization")
3. Implement: Follow Phase 1 (weeks 1-2) → Phase 5 (weeks 5-6)
4. Assign: Fill in "Responsible Parties" table
5. Track: Use Phase timeline to manage schedule

**Read Time**: 40 min + 61 hours implementation

---

### "I'm adding a new branch (feature branch)"
1. Read: AGENT_GUIDELINES_RESOLUTION_PLAN.md → Task 3.2
2. Learn: How to create profiles for feature branches
3. Action: Once Phase 3 completes, follow `.specify/AGENT_GUIDELINES_FRAMEWORK.md`
4. Reference: Create profile matching parent branch pattern

**Read Time**: 15 min

---

### "I updated context control profiles and need to update docs"
1. Read: AGENT_GUIDELINES_RESOLUTION_PLAN.md → Task 4.1
2. Reference: `.specify/AGENT_DOCS_UPDATE_CHECKLIST.md` (created in Phase 4)
3. Action: Follow checklist for which files to update
4. Validation: Use `scripts/verify-agent-docs-consistency.sh` (created in Phase 4.3)

**Read Time**: 10 min

---

### "I'm a project manager tracking this effort"
1. Read: AGENT_GUIDELINES_RESOLUTION_PLAN.md → Section "Implementation Timeline" 
2. Reference: Phase breakdown and effort estimates (61 hours total)
3. Plan: Allocate team across 6-week timeline
4. Monitor: Track milestone completion per phase

**Read Time**: 5 min

---

## 📊 Key Numbers at a Glance

| Metric | Value |
|--------|-------|
| Consistency Issues Identified | 8 |
| Root Causes | 8 |
| Branches Affected | 3 (orchestration-tools, main, scientific) |
| Implementation Phases | 5 |
| Total Tasks | 28 |
| Total Effort | ~61 hours |
| Elapsed Time | ~6 weeks (parallel work) |
| Critical Severity Issues | 1 (Task Master scope) |
| High Severity Issues | 1 (File access control) |

---

## 🚨 Critical Issues Summary

### Issue #1: Task Master Scope Ambiguity 🔴
- **Problem**: Scientific agents don't know if Task Master is available
- **Solution**: Phase 2.3 adds Task Master section to scientific AGENTS.md
- **ETA**: Week 3
- **Impact**: Without this, scientific agents can't use centralized task management

### Issue #2: File Access Control Inconsistency 🟡
- **Problem**: Protected files not explicitly listed in context profiles
- **Solution**: Phase 3.1 consolidates settings; Phase 3.3 explains in AGENTS.md
- **ETA**: Week 4
- **Impact**: Agents may see files they shouldn't, or miss files they need

### Others (Medium Severity)
- Context contamination guidance missing from orchestration-tools (Phase 2.2)
- Code style guidance missing from orchestration-tools (Phase 2.2)
- Claude vs. non-Claude guidance separated (Phase 3.4)
- Profile coverage gaps for feature branches (Phase 3.2)
- Agent settings redundancy (Phase 3.1)

---

## 📅 Phase Completion Timeline

```
Today (Nov 12)
│
Week 1-2: Foundation ────────────────┐
Week 2-3: Reconciliation ───────────┬┤
Week 3-4: Access Control ──────────┬┤
Week 4-5: Maintenance ────────────┬┤
Week 5-6: Validation ───────────┬┤
│                                    │
└────────────────── Target: Nov 30 ──┘

Key Milestones:
- Nov 15 (End Week 1): Phase 1 framework complete
- Nov 22 (End Week 2): All AGENTS.md updated
- Nov 29 (End Week 4): Access control & MCP integrated
- Nov 30 (End Week 6): Full validation + sign-off
```

---

## ✅ How to Know Resolution Is Complete

When ALL of these are true, the inconsistency issues are resolved:

1. ✅ All 8 original issues marked "RESOLVED" in BRANCH_AGENT_GUIDELINES_SUMMARY.md
2. ✅ All AGENTS.md files include: Task Master, code style, context contamination prevention
3. ✅ Context control profiles tested and working (Phase 5.1)
4. ✅ Task Master verified on all applicable branches (Phase 5.2)
5. ✅ Update checklist prevents future divergence (Phase 4.1)
6. ✅ Verification script passes with no divergence warnings (Phase 4.3)
7. ✅ Agent implementation guide available (Phase 5.4)
8. ✅ All responsible parties signed off (Phase 5.5)

---

## 🔗 Related Documents (After Resolution)

These documents will be created during implementation:

- `.specify/AGENT_GUIDELINES_FRAMEWORK.md` (Phase 1)
- `.context-control/README.md` (Phase 1)
- `CODING_STANDARDS.md` (Phase 1)
- `CONTEXT_CONTROL_AND_CONTAMINATION_PREVENTION.md` (Phase 1)
- `.specify/templates/AGENTS.md.template` (Phase 2)
- `AGENT_BRANCH_SELECTION_GUIDE.md` (Phase 2)
- `MCP_INTEGRATION_GUIDE.md` (Phase 3)
- `.specify/AGENT_DOCS_UPDATE_CHECKLIST.md` (Phase 4)
- `scripts/verify-agent-docs-consistency.sh` (Phase 4)
- `docs/CONTEXT_PROFILE_TEST_REPORT.md` (Phase 5)
- `docs/TASK_MASTER_INTEGRATION_TEST.md` (Phase 5)
- `AGENT_IMPLEMENTATION_GUIDE.md` (Phase 5)

---

## ❓ FAQ

**Q: Do I need to read all three documents?**  
A: No. Read SUMMARY for issues, PLAN for implementation details, REFERENCE (this) for navigation.

**Q: When will this be fixed?**  
A: If team starts now, completion target is November 30, 2025 (6 weeks).

**Q: What if I'm not involved in the resolution?**  
A: Check your branch and read just the "Quick Lookup" section above.

**Q: Can we do this faster?**  
A: Possibly. Tasks in same phase can run in parallel. Critical path is ~2 weeks minimum.

**Q: What happens if we do nothing?**  
A: Agents will get inconsistent guidance, leading to confusion and potential errors. Branch divergence will continue.

**Q: How much developer time is required?**  
A: ~61 hours total. Can be distributed across team. Roughly 8-10 hours per week for 6-7 weeks.

**Q: Will this break anything?**  
A: No. It's documentation only. Context control profiles will be tested before deployment.

---

## 📞 Getting Help

- **Understanding Issues**: Read BRANCH_AGENT_GUIDELINES_SUMMARY.md
- **Understanding Root Causes**: Read "Root Cause Analysis" in AGENT_GUIDELINES_RESOLUTION_PLAN.md
- **Implementing Phase X**: Read Phase X section in AGENT_GUIDELINES_RESOLUTION_PLAN.md
- **Adding New Branch**: See Phase 3.2 (Task 3.2)
- **Updating Docs**: See Phase 4 (Maintenance)
- **Verifying Success**: See Phase 5 (Validation & Documentation)

---

## 📝 Document Control

| Document | Purpose | Read Time | Audience |
|----------|---------|-----------|----------|
| BRANCH_AGENT_GUIDELINES_SUMMARY.md | What's wrong | 15-20 min | Everyone |
| AGENT_GUIDELINES_RESOLUTION_PLAN.md | How to fix | 30-40 min | Implementers |
| AGENT_GUIDELINES_QUICK_REFERENCE.md | Navigation | 5 min | Everyone (you are here) |

---

**Last Updated**: 2025-11-12  
**Status**: ACTIVE - Ready for Team Review

