# File Evaluation & Cleanup Plan - EmailIntelligenceAider

**Analysis Date:** 2026-03-25  
**Scope:** EmailIntelligenceAider root-level files  
**Total Files:** ~374 root-level files

---

## Scoring Methodology

Each file scored on:
- **D (Duplication):** Copies across EmailIntelligence projects (1-4 scale)
- **I (Importance):** Relevance to branch management task (1-5 scale)
- **S (Size):** File size impact (1-5 scale)
- **R (Relevance):** Current relevance (1-5 scale)

**Priority = (D × 0.3) + (I × 0.3) + (S × 0.2) + (R × 0.2)**

---

## Category 1: HIGH PRIORITY CLEANUP (Score > 3.5)

| File | Duplication | Importance | Size | Relevance | Score | Action |
|------|-------------|------------|------|-----------|-------|--------|
| `comprehensive_analysis_report.md` | 1 | 5 | 5 | 4 | **4.3** | KEEP - Active reference |
| `AGENT_GUIDELINES_RESOLUTION_PLAN.md` | 4 | 5 | 3 | 3 | **3.9** | CONSOLIDATE - Exists in 4 projects |
| `BRANCH_AGENT_GUIDELINES_SUMMARY.md` | 4 | 4 | 3 | 3 | **3.7** | CONSOLIDATE - Exists in 4 projects |
| `BLOCKER_ANALYSIS_INDEX.md` | 4 | 4 | 2 | 3 | **3.6** | CONSOLIDATE - Exists in 4 projects |
| `CONFIG_ANALYSIS.md` | 4 | 3 | 2 | 3 | **3.2** | CONSOLIDATE - Exists in 4 projects |
| `DEPENDENCY_BLOCKER_ANALYSIS.md` | 4 | 4 | 3 | 2 | **3.5** | CONSOLIDATE - Exists in 4 projects |

---

## Category 2: DUPLICATES TO CONSOLIDATE (Score 2.5-3.5)

| File | Duplication | Importance | Size | Relevance | Score | Action |
|------|-------------|------------|------|-----------|-------|--------|
| `BRANCH_PROPAGATION_IMPLEMENTATION_SUMMARY.md` | 2 | 3 | 3 | 2 | **2.7** | MERGE with similar |
| `ORCHESTRATION_TOOLS_ANALYSIS_SUMMARY.md` | 1 | 5 | 3 | 4 | **3.4** | KEEP - Main source |
| `GIT_HOOKS_BLOCKING_SUMMARY.md` | 3 | 4 | 2 | 3 | **3.2** | CONSOLIDATE |
| `FLAKE8_UNIFICATION_SUMMARY.md` | 3 | 2 | 1 | 1 | **2.1** | ARCHIVE - Obsolete |
| `CLEANUP_SUMMARY.md` | 2 | 2 | 1 | 1 | **1.9** | ARCHIVE |
| `FILE_PERMISSIONS_ANALYSIS.md` | 1 | 3 | 3 | 2 | **2.6** | KEEP |
| `CI_MIGRATION_ANALYSIS.md` | 1 | 2 | 1 | 1 | **1.6** | ARCHIVE |

---

## Category 3: PROJECT-SPECIFIC (Score < 2.5)

| File | Duplication | Importance | Size | Relevance | Score | Action |
|------|-------------|------------|------|-----------|-------|--------|
| `ORCHESTRATION_IDE_DISTRIBUTION_PLAN.md` | 1 | 4 | 2 | 3 | **3.0** | KEEP |
| `ORCHESTRATION_IDE_INCLUSION_SUMMARY.md` | 1 | 4 | 2 | 3 | **3.0** | KEEP |
| `SETUP_LAUNCH_RESTORATION_SUMMARY.md` | 1 | 3 | 1 | 2 | **2.3** | KEEP |
| `SCRIPTS_EXECUTION_COMPLETION_SUMMARY.md` | 1 | 3 | 2 | 2 | **2.5** | KEEP |
| `MODULAR_ORCHESTRATION_SYSTEM_SUMMARY.md` | 1 | 3 | 2 | 2 | **2.5** | KEEP |
| `CLI_ENHANCEMENT_SUMMARY.md` | 1 | 3 | 1 | 2 | **2.4** | KEEP |

---

## Category 4: OBSOLETE/ARCHIVE (Score < 2.0)

| File | Reason for Archival |
|------|---------------------|
| `STASH_FIXES_SUMMARY.md` | Old stash recovery - no longer relevant |
| `SESSION_SUMMARY_NOV20.md` | Session-specific, outdated |
| `TASKMASTER_SYNC_ANALYSIS.md` | Taskmaster config, local only |
| `SAFE_ACTION_PLAN.md` | Old action plan - superseded |
| `IMPLEMENTATION_CHECKLIST.md` | Old checklist - superseded |
| `CODE_RECOMMENDATIONS.md` | Old recommendations |
| `code_recommendations_raw.txt` | Raw data, redundant |
| `CLEANUP_CHECKLIST.md` | Duplicated in other docs |

---

## Content Duplication Matrix

### Files with 4+ Copies (Critical Consolidation Needed)
```
BRANCH_AGENT_GUIDELINES_SUMMARY.md     - 4 projects
BLOCKER_ANALYSIS_INDEX.md               - 4 projects  
CONFIG_ANALYSIS.md                      - 4 projects
DEPENDENCY_BLOCKER_ANALYSIS.md          - 6 projects ⚠️
```

### Files with 3 Copies (Medium Priority)
```
GIT_HOOKS_BLOCKING_SUMMARY.md           - 3 projects
FLAKE8_UNIFICATION_SUMMARY.md           - 3 projects
ORCHESTRATION_GITHUB_PROTECTION_SUMMARY - 3 projects
```

---

## Recommended Actions

### IMMEDIATE (Today)
1. **Create consolidated BRANCH_MASTER_PLAN.md** - Merge:
   - AGENT_GUIDELINES_RESOLUTION_PLAN.md
   - BRANCH_AGENT_GUIDELINES_SUMMARY.md
   - BLOCKER_ANALYSIS_INDEX.md
   - DEPENDENCY_BLOCKER_ANALYSIS.md

2. **Archive obsolete files** - Move to `archive/`:
   - STASH_FIXES_SUMMARY.md
   - SESSION_SUMMARY_NOV20.md
   - TASKMASTER_SYNC_ANALYSIS.md

### THIS WEEK
3. **Consolidate duplicate analysis files** - Create symlinks or references:
   - All 4 projects should reference ONE source of truth
   - Keep versions in sync

4. **Clean up temporary files**:
   - `.aider.chat.history.md` (2.2MB - should be gitignored)
   - `.aider.input.history` (124KB - should be gitignored)
   - `uv.lock` (should be in .gitignore)

### COMING WEEKS
5. **Organize by function**:
   - `/docs/branch/` - Branch management docs
   - `/docs/orchestration/` - Orchestration docs
   - `/docs/analysis/` - Analysis outputs (ALREADY DONE ✓)
   - `/archive/` - Obsolete docs

---

## File Organization Structure

```
EmailIntelligenceAider/
├── AGENTS.md                    ← Keep (root config)
├── CLAUDE.md                    ← Keep (root config)
├── README.md                    ← Keep
├── docs/
│   ├── analysis/               ← ✓ Already organized
│   │   ├── INDEX.md
│   │   ├── METRICS_STANDARD.md
│   │   ├── PROJECT_METRICS.json
│   │   └── ANALYSIS_COMPARISON_REPORT.md
│   ├── branch/                  ← NEW - Branch management
│   ├── orchestration/          ← NEW - Hook system
│   └── archive/                ← NEW - Obsolete files
├── scripts/                    ← Keep
├── archive/                    ← NEW - Move obsolete here
└── [root files]                ← Reduce by 50%
```

---

## Success Metrics

| Metric | Current | Target | Action |
|--------|---------|--------|--------|
| Root-level MD files | 13 | <6 | Archive 7 |
| Duplicate docs | 6 sets | 1 consolidated | Consolidate |
| Obsolete files | ~10 | 0 | Archive |
| Temp files in git | 3 | 0 | Add to .gitignore |

---

**Generated:** 2026-03-25
**Next Review:** After cleanup completion