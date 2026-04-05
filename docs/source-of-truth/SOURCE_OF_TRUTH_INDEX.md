# Source of Truth - Consolidated Documentation Index

**Created:** 2026-03-25  
**Purpose:** Single source of truth for documentation that applies across all EmailIntelligence clones

---

## Category 1: IDENTICAL ACROSS ALL CLONES (80+ files)

These files are **identical** in all three projects (Aider, Auto, Gem) and should be maintained as the single source:

### Progress Tracking (Keep in `docs/source-of-truth/progress/`)
| File | MD5 | Status |
|------|-----|--------|
| `BLOCKER_ANALYSIS_INDEX.md` | fa46c4c68e | ✅ CONSOLIDATED |
| `PROGRESS_DASHBOARD.md` | 821ab4b49b | ✅ CONSOLIDATED |
| `PROGRESS_TRACKING.md` | c36038766b | ✅ CONSOLIDATED |
| `PROGRESS_TRACKING_README.md` | 91f38dd85f | ✅ CONSOLIDATED |

### Branch Management (Keep in `docs/source-of-truth/branch/`)
| File | MD5 | Status |
|------|-----|--------|
| `BRANCH_AGENT_GUIDELINES_SUMMARY.md` | 37ba11d6d | ✅ CONSOLIDATED |
| `BRANCH_PROPAGATION_IMPLEMENTATION_SUMMARY.md` | 2c78e001f | ✅ CONSOLIDATED |
| `BRANCH_UPDATE_PROCEDURE.md` | 5d587d452* | ⚠️ Note: Auto/Gem differ |
| `AGENT_GUIDELINES_RESOLUTION_PLAN.md` | 69eaa525c | ✅ CONSOLIDATED |
| `AGENT_GUIDELINES_QUICK_REFERENCE.md` | d7bd67444 | ✅ CONSOLIDATED |

### Orchestration (Keep in `docs/source-of-truth/orchestration/`)
| File | MD5 | Status |
|------|-----|--------|
| `ORCHESTRATION_TOOLS_ANALYSIS_SUMMARY.md` | (unique) | ✅ KEEP HERE |
| `GIT_HOOKS_BLOCKING_SUMMARY.md` | 273f3f18c | ✅ CONSOLIDATED |
| `ORCHESTRATION_IDE_INCLUSION_SUMMARY.md` | d0ffd88d7 | ✅ CONSOLIDATED |
| `ORCHESTRATION_IDE_DISTRIBUTION_PLAN.md` | 8f3467174 | ✅ CONSOLIDATED |
| `ORCHESTRATION_PROGRESS_SUMMARY.md` | 0d48ecd40 | ✅ CONSOLIDATED |
| `ORCHESTRATION_SYNC_GUIDE.md` | 5aa6cdcd7 | ✅ CONSOLIDATED |

### Stash/Recovery (Archive)
| File | MD5 | Status |
|------|-----|--------|
| `STASH_FIXES_SUMMARY.md` | de3786e13 | 🔴 ARCHIVE - Obsolete |
| `STASH_MANAGEMENT_ISSUES.md` | 022d1c22e | 🔴 ARCHIVE - Obsolete |

---

## Category 2: UNIQUE TO EACH CLONE (MUST STAY BRANCH-SPECIFIC)

These files **MUST remain branch-specific** because they contain project-specific content:

| File | Why Branch-Specific | Aider | Auto | Gem |
|------|---------------------|-------|------|-----|
| `AGENTS.md` | Project-specific instructions | ✅ | ✅ | ✅ |
| `CLAUDE.md` | Project-specific Claude config | ✅ | ✅ | ✅ |
| `GEMINI.md` | Project-specific Gemini config | ✅ | ✅ | ✅ |
| `CONFIG_ANALYSIS.md` | Analyzes each project's config | ✅ | ✅ | ✅ |
| `README.md` | Project-specific readme | ✅ | ✅ | ✅ |
| `OUTSTANDING_TODOS.md` | Project-specific tasks | ✅ | ⚠️ differs | ⚠️ differs |
| `TASKMASTER_BRANCH_CONVENTIONS.md` | Project-specific conventions | ✅ | ⚠️ differs | ⚠️ differs |

**Action Required:** When updating these files, update in ALL three projects separately.

---

## Category 3: PARTIALLY DIFFERENT (NEEDS ANALYSIS)

These files have some differences - need review:

| File | Aider MD5 | Auto/Gem MD5 | Issue |
|------|-----------|--------------|-------|
| `BRANCH_UPDATE_PROCEDURE.md` | 5d587d45 | 0281ae1a | Aider unique |
| `BRANCH_UPDATE_QUICK_START.md` | 7bae23bf | 469be914 | Aider unique |
| `OUTSTANDING_TODOS.md` | 49fb61fa | e9b8ed48 | Different |
| `TASKMASTER_BRANCH_CONVENTIONS.md` | afee8000 | 449c84c2 | Different |
| `ORCHESTRATION_TOOLS_REDESIGN.md` | d7c22384 | 14387294 | Different |

---

## File Count Summary

| Category | Count | Action |
|----------|-------|--------|
| Identical (Consolidated) | ~70 | Copy to source-of-truth |
| Unique (Branch-specific) | 5+ | Keep separate per project |
| Partially Different | 5 | Review individually |
| Obsolete | ~10 | Move to archive |

---

## Usage

**When updating identical files:**
1. Update the source-of-truth copy in `docs/source-of-truth/`
2. The orchestration hooks should propagate to other clones
3. Or manually copy to other projects

**When updating branch-specific files:**
1. Update in each project individually
2. These are intentionally different

---

**Last Updated:** 2026-03-25