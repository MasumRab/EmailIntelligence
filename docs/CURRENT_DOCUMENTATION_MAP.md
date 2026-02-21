# Current Documentation Map (ACTIVE)

**Status:** Active documentation only  
**Date:** January 6, 2026  
**Purpose:** Guide readers to the right documentation

---

## 🎯 By Role: What To Read

### 👨‍💼 Project Manager / Scrum Master

**Essential (60 minutes):**
1. ✅ **README.md** (5 min) - Overview of project structure
2. ✅ **PROJECT_STATE_PHASE_3_READY.md** (30 min) - Current Phase 3 status, timeline, dependencies
3. ✅ **CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md** (25 min) - Next consolidation work

**For Planning:**
- Task dependencies: See PROJECT_STATE_PHASE_3_READY.md (section: Task Dependencies)
- Team resource needs: See PROJECT_STATE_PHASE_3_READY.md (section: Resource Requirements)
- Next steps: CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md (Phase 1-7 execution plan)

**Questions?**
- "What's the current status?" → PROJECT_STATE_PHASE_3_READY.md
- "How long will Phase 3 take?" → PROJECT_STATE_PHASE_3_READY.md (Timeline section)
- "What should I work on next?" → CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md

---

### 👨‍💻 Developer / Implementation Engineer

**Essential (45 minutes):**
1. ✅ **README.md** (5 min) - Overview
2. ✅ **TASK_STRUCTURE_STANDARD.md** (20 min) - Task format (required for understanding any task)
3. ✅ **PROJECT_STATE_PHASE_3_READY.md** (20 min) - Your specific task & dependencies

**Then Select Your Task:**
- **Phase 3 Tasks:** See `new_task_plan/task_files/task_007.md`, `new_task_plan/task_files/task_075.1-5.md`, `new_task_plan/task_files/task_079-083.md`
- **Find your task ID:** See PROJECT_STATE_PHASE_3_READY.md (Active Tasks section)

**Helper Tools (Optional):**
- Progress logging: MEMORY_API_FOR_TASKS.md
- Helper scripts: SCRIPTS_IN_TASK_WORKFLOW.md

**Questions?**
- "What's the task format?" → TASK_STRUCTURE_STANDARD.md
- "Which task should I start?" → PROJECT_STATE_PHASE_3_READY.md (Active Tasks)
- "How do I log progress?" → MEMORY_API_FOR_TASKS.md
- "Are there helper tools?" → SCRIPTS_IN_TASK_WORKFLOW.md

---

### 🏗️ Architect / Technical Lead

**Essential (90 minutes):**
1. ✅ **README.md** (5 min) - Overview
2. ✅ **PROJECT_STATE_PHASE_3_READY.md** (30 min) - Full Phase 3 scope, dependencies, risks
3. ✅ **TASK_STRUCTURE_STANDARD.md** (20 min) - Standard for all tasks
4. ✅ **NEW_TASK_PLAN_CONSOLIDATION_STRATEGY.md** (20 min) - Gap analysis & consolidation approach
5. ✅ **CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md** (15 min) - Implementation plan

**For Architecture Review:**
- Task specifications: `new_task_plan/task_files/task_007.md`, `new_task_plan/task_files/task_075.1-5.md`, `new_task_plan/task_files/task_079-083.md`
- Dependencies: PROJECT_STATE_PHASE_3_READY.md (Task Dependencies section)
- Quality standards: TASK_STRUCTURE_STANDARD.md (Success Criteria section)

**Questions?**
- "What's the overall architecture?" → PROJECT_STATE_PHASE_3_READY.md
- "What are the task dependencies?" → PROJECT_STATE_PHASE_3_READY.md
- "What are the quality standards?" → TASK_STRUCTURE_STANDARD.md
- "What consolidation work is needed?" → NEW_TASK_PLAN_CONSOLIDATION_STRATEGY.md

---

### 🤖 AI Agent / Context Provider

**Load These (For Full Context):**
1. ✅ **CLAUDE.md** - This is auto-loaded; contains Agent integration guide
2. ✅ **AGENT.md** - Agent instructions
3. ✅ **AGENTS.md** - System agent guidance

**Supplementary (As Needed):**
- Task details: /tasks/*.md (individual task files)
- Project state: PROJECT_STATE_PHASE_3_READY.md
- Task standard: TASK_STRUCTURE_STANDARD.md

**Remember:**
- `CLAUDE.md` is auto-loaded context
- Always check `PROJECT_STATE_PHASE_3_READY.md` for current scope
- Reference tasks by their actual file (`task_007.md`, not "task 7")

---

## 📚 By Document Type

### Configuration & Context
| Document | Purpose | Audience |
|----------|---------|----------|
| CLAUDE.md | Auto-loaded agent context | AI agents |
| AGENT.md | Agent task instructions | Agents & managers |
| AGENTS.md | System agent guidance | All agents |

### Current Project State
| Document | Purpose | Audience |
|----------|---------|----------|
| PROJECT_STATE_PHASE_3_READY.md | **Current phase status, tasks, timeline** | Everyone |
| README.md | Overview & navigation | Everyone |

### Task & Process Standards
| Document | Purpose | Audience |
|----------|---------|----------|
| TASK_STRUCTURE_STANDARD.md | **Standard format for all tasks** | Developers, architects |
| TASK_NUMBERING_DEPRECATION_PLAN.md | **Why old numbering (001-020) is deprecated** | Everyone (reference) |
| OLD_TASK_NUMBERING_DEPRECATED.md | **Do NOT use old task IDs** | Everyone (reference) |

### Implementation Plans
| Document | Purpose | Audience |
|----------|---------|----------|
| CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md | **Consolidate tasks to new_task_plan/** | Project leads |
| NEW_TASK_PLAN_CONSOLIDATION_STRATEGY.md | **Gap analysis & consolidation strategy** | Architects |

### Helper Tools & APIs
| Document | Purpose | Audience |
|----------|---------|----------|
| MEMORY_API_FOR_TASKS.md | Optional progress logging API | Developers (optional) |
| SCRIPTS_IN_TASK_WORKFLOW.md | Optional helper scripts | Developers (optional) |

---

## 🔍 Quick Lookup

### "I need to understand..."

| Topic | Read This | Time |
|-------|-----------|------|
| Current Phase 3 status | PROJECT_STATE_PHASE_3_READY.md | 30 min |
| How to format a task | TASK_STRUCTURE_STANDARD.md | 20 min |
| What task to work on | PROJECT_STATE_PHASE_3_READY.md → Active Tasks | 10 min |
| Task dependencies | PROJECT_STATE_PHASE_3_READY.md → Task Dependencies | 10 min |
| What's wrong with old numbering | TASK_NUMBERING_DEPRECATION_PLAN.md | 15 min |
| Consolidation work needed | CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md | 25 min |
| Why consolidation is needed | NEW_TASK_PLAN_CONSOLIDATION_STRATEGY.md | 25 min |
| How to track progress | MEMORY_API_FOR_TASKS.md | 15 min |
| Helper scripts available | SCRIPTS_IN_TASK_WORKFLOW.md | 10 min |

---

## 📍 Key Sections to Reference

### Task Selection
**Document:** PROJECT_STATE_PHASE_3_READY.md  
**Sections:**
- "Active Tasks (Phase 3 Only)" - Lists all 9 tasks
- "Task Dependencies (Implementation Order)" - Shows what depends on what
- "Implementation Guide Quick Start" - How to begin

### Task Format Standards
**Document:** TASK_STRUCTURE_STANDARD.md  
**Sections:**
- "Required Sections (In Order)" - All 14 sections every task must have
- "Apply This Standard To" - Which tasks follow this
- "Benefits" - Why we use this standard

### Current Project Status
**Document:** PROJECT_STATE_PHASE_3_READY.md  
**Sections:**
- "Current State Overview" - What's done, what's pending
- "Active Tasks (Phase 3 Only)" - The 9 tasks to implement
- "Task Dependencies" - What blocks what
- "Handoff Checklist for Implementation Team" - What to review before starting
- "Success Criteria for Phase 3" - What "done" means

---

## ⚠️ DO NOT Read (Archive These)

These documents are in `/archive/` because they're outdated:

| Document | Reason | Read Instead |
|----------|--------|--------------|
| PHASE_1_STATUS_SUMMARY.md | Historical phase | PROJECT_STATE_PHASE_3_READY.md |
| PROJECT_REFERENCE.md | Outdated task refs | PROJECT_STATE_PHASE_3_READY.md |
| TASK_NUMBERING_ISSUE_ANALYSIS.md | Superseded analysis | TASK_NUMBERING_DEPRECATION_PLAN.md |
| QUICK_START_ALL_PHASES.md | Old getting started | README.md |
| IMPLEMENTATION_DELIVERY_SUMMARY.md | Completed phase | PROJECT_STATE_PHASE_3_READY.md |
| START_HERE_INTEGRATION.md | Old integration guide | CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md |

**Tip:** If you find yourself reading something in `/archive/`, you're probably looking for a newer document in root.

---

## 🚀 Getting Started Checklist

### For New Team Members

1. ✅ Read README.md (5 min)
2. ✅ Read your role section above (15-30 min)
3. ✅ Read PROJECT_STATE_PHASE_3_READY.md (30 min)
4. ✅ Locate your task file in `/tasks/` (5 min)
5. ✅ Read TASK_STRUCTURE_STANDARD.md (20 min)
6. ✅ Read your specific task file (30 min)
7. ✅ Ask questions if unclear!

**Total Time:** ~2 hours to get fully oriented

---

## 📞 Questions Not Answered?

**"Where do I find X?"**
- Use Ctrl+F on this document to search

**"Is document Y current?"**
- If it's in root (not `/archive/`), it's current
- If it's in `/archive/`, it's historical reference only

**"Should I read this document?"**
- If it's in `/archive/`, check the Quick Lookup table above for the current version

**"Why was document X archived?"**
- See `/archive/README.md` (explains each category)

---

## 📋 Active Documentation Checklist

As of January 6, 2026, these documents are ACTIVE:

- ✅ CLAUDE.md
- ✅ AGENT.md
- ✅ AGENTS.md
- ✅ README.md
- ✅ PROJECT_STATE_PHASE_3_READY.md
- ✅ TASK_STRUCTURE_STANDARD.md
- ✅ CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md
- ✅ NEW_TASK_PLAN_CONSOLIDATION_STRATEGY.md
- ✅ TASK_NUMBERING_DEPRECATION_PLAN.md
- ✅ OLD_TASK_NUMBERING_DEPRECATED.md
- ✅ MEMORY_API_FOR_TASKS.md
- ✅ SCRIPTS_IN_TASK_WORKFLOW.md
- ✅ ROOT_DOCUMENTATION_CLEANUP_PLAN.md
- ✅ CURRENT_DOCUMENTATION_MAP.md (this file)

**Everything else is in `/archive/` (historical reference only)**

---

**Last Updated:** January 6, 2026  
**Documentation Status:** Clean and current ✅  
**Next Update:** After consolidation completion (NEW_TASK_PLAN_CONSOLIDATION_STRATEGY.md execution)
