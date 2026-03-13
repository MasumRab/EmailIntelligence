# Project Identity: Branch Alignment Tooling

**CRITICAL: READ BEFORE ANY MIGRATION OR RESTORATION**

**Last Updated**: 2026-02-27  
**Project Name**: Branch Alignment Tooling (NOT EmailIntelligence)

---

## This Repository Contains Branch Alignment Tasks

| Project | Location | Purpose | Status |
|---------|----------|---------|--------|
| **Branch Alignment** | `.taskmaster/tasks/task_001-028.md` | Git branch clustering, merge automation, validation | ACTIVE - Canonical |

---

## ⛔ MIGRATION RULES

### DO NOT:
- Rewrite alignment tasks (001-028) outside branch alignment scope
- Merge non-alignment content into alignment task files
- Treat historical pivot proposals as canonical for this project
- Confuse example files (e.g., `email_data.json`) with project purpose

### DO:
- Keep alignment tasks focused on: git, branches, merges, rebases, clustering, validation
- Reference this file before any task restructuring
- Understand that task files may reference example files (like `email_data.json`) as test cases for generic frameworks

---

## Task 002-004 Canonical Definitions

These are **Branch Alignment** tasks, not external pivots:

| Task | Canonical Purpose | NOT This |
|------|-------------------|----------|
| **002** | Branch Clustering System (git metrics, commit analysis, BranchClusterer) | ❌ Non-alignment scope |
| **003** | Pre-merge Validation Scripts (critical file checks - generic framework) | ❌ Non-alignment scope |
| **004** | Core Branch Alignment Framework (git hooks, local alignment) | ❌ Non-alignment scope |

### Understanding Example Files in Tasks

Tasks may reference specific files (e.g., `email_data.json`, `AGENTS.md`) as **examples** in generic frameworks:

**Example from Task 003:**
```python
# This is a GENERIC validation framework
CRITICAL_FILES = {
    "setup/commands/__init__.py": {...},
    "data/processed/email_data.json": {...},  # ← Example file, NOT project purpose
    "config/settings.json": {...},
}
```

**The task purpose is:** Build a validation script for ANY critical files  
**NOT:** Build email intelligence features

**How to tell the difference:**
- ✅ **Alignment task:** "Create validation script for critical files" (generic framework)
- ❌ **Non-alignment:** "Process emails for intelligence extraction" (specific to EmailIntelligence)

---

## Why This Confusion Exists

1. **Historical Context:** This Task Master system was originally created for the EmailIntelligence project
2. **Pivot Proposals:** `ORACLE_RECOMMENDATION_TODO.md` contains historical scope pivot proposals that were **not executed**
3. **Example Files:** Tasks use example files (like `email_data.json`) which can be mistaken for project purpose

**These proposals were NOT executed.** The canonical task set remains Branch Alignment.

---

## Decision Status

| Decision | Status | Resolution |
|----------|--------|------------|
| Project identity | ✅ DECIDED | Branch Alignment Tooling |
| Task 002-004 purpose | ✅ DECIDED | Branch clustering/validation/framework |
| Epic pivot proposals | ❌ REJECTED | Not applicable to this project |
| Example file usage | ✅ CLARIFIED | Generic frameworks use example files |

---

## For Future Agents

If you are performing:
- **Task restoration**: Restore alignment content only
- **Task augmentation**: Add alignment-related specs only
- **Migration work**: Do not cross-pollinate from non-alignment sources into `tasks/`
- **Content analysis**: Distinguish between generic frameworks (alignment) and specific feature implementations (non-alignment)

If you encounter pivot definitions, they are **historical proposals only** and should not override the canonical task definitions in `tasks/*.md`.

### Quick Test: Is This Task Alignment or Not?

**Ask these questions:**
1. Does the task build generic git/branch tooling? → ✅ Alignment
2. Does the task reference specific files as examples in a framework? → ✅ Alignment (likely)
3. Does the task implement EmailIntelligence-specific features? → ❌ Non-alignment
4. Does the task process emails for business logic? → ❌ Non-alignment

**Examples:**
- ✅ "Pre-merge validation script" → Alignment (generic safety framework)
- ✅ "Branch clustering system" → Alignment (git analysis)
- ❌ "Email sentiment analysis" → Non-alignment (EmailIntelligence feature)
- ❌ "Email data processing pipeline" → Non-alignment (EmailIntelligence feature)

---

**Last Updated**: 2026-02-27  
**Reason**: Prevent conflation of Branch Alignment and EmailIntelligence projects; clarify example file usage
