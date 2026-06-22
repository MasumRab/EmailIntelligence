# Spec Consolidation Plan — For 000-integrated-specs Branch

**Date:** 2026-04-14  
**Source:** Qwen agent multi-spec review analysis  
**Full Analysis:** `docs/handoff/spec-merge-analysis.md`

---

## Purpose

This branch (`000-integrated-specs`) is the **canonical spec hub**. All spec content from `consolidate/cli-unification` must be merged here. consolidate was not intended to have specs — they were accidentally merged in during consolidation — but the content is valuable and must be preserved.

---

## What's Coming In

### 13 New Specs from Consolidate (to be added)

| Source ID | Target ID | Title | Files | Priority |
|-----------|-----------|-------|-------|----------|
| 001-pr176 | 013 | PR176 via GitHub CLI | 14 | Medium |
| 003-unified-git | 014 | Git intent narratives | 8 | Medium |
| 005-cli-architecture | 015 | CLI factory pattern | 11 | **HIGH** — from scientific branch |
| 006-unified-architecture | 016 | Architecture consolidation | 12 | High |
| 007-merge-guidance | 017 | Branch merge guidance | 8 | Medium |
| 008-branch-comparison | 018 | Branch comparison framework | 7 | Medium |
| 009-implementation | 019 | Implementation framework | 9 | Medium |
| 010-orchestration-workflow | 020 | Workflow orchestration | 6 | Medium |
| WORK_TO_SPEC_MAPPING.md | — | Cross-reference | 1 | Low |

### 4 Existing Specs Getting Updates

| Spec ID | Change | Files Affected |
|---------|--------|---------------|
| 004-guided-workflow | **REPLACE** with consolidate version (723 lines vs 48) | spec.md, plan.md, tasks.md + 16 new files |
| 006-pr176-integration-fixes | 3 path corrections (`setup/` → `src/setup/`) | tasks.md (3 lines) |
| 007-task-execution-layer | Merge with consolidate's 013-task-execution | Up to 4 additional files |
| 010-rebase-analysis | Merge consolidate's 001-rebase content | spec.md (clarification sessions) |
| 012-unified-git-analysis | Merge consolidate's 003-unified-git content | spec.md (intent narratives) |

### 6 Specs Staying Unchanged

| Spec ID | Files | Reason |
|---------|-------|--------|
| 005-orchestration-verification | 9 | No consolidate equivalent |
| 008-toolset-additive | 8 | No consolidate equivalent |
| 009-agent-context-control | 4 | Consolidate's 001/002 are empty |
| 011-execution-layer-tasks-pr | 4 | No consolidate equivalent |

### Content NOT Being Merged

| Source | Reason |
|--------|--------|
| `001-agent-context-control/spec.md` | Empty (0 bytes) — 000's 009 has real content |
| `002-agent-context-control/spec.md` | Empty (0 bytes) |
| `003-rebase-analysis/` | Exact duplicate of 001-rebase-analysis |
| `*.bak`, `*.pre-rewrite.bak` | Backup artifacts |

---

## Architectural Drift — Decisions Being Changed

These are existing decisions on this branch that will be **overridden** by consolidate's content:

### Decision C1: Entry Point Change
- **Current:** `launch.py` is the orchestration entry point
- **Incoming:** `dev.py` is exclusive entry point, `launch.py` forbidden for dev-tools
- **Impact:** 004-guided-workflow spec will be completely rewritten
- **Rationale:** Separation of dev-tools from app runtime prevents circular dependencies

### Decision C4: CLI Framework Addition
- **Current:** No CLI framework specified — simple scripts
- **Incoming:** Factory pattern, CommandFactory + Registry, interface-based design
- **Impact:** New architecture guidance for all CLI-related specs
- **Rationale:** Production-ready patterns from scientific branch

### Decision C5: Merge Strategy Upgrade
- **Current:** Manual guidance with checklists
- **Incoming:** Automated: `dev.py rebase --apply`, DAG analysis, `git merge-tree`
- **Impact:** More rigorous merge methodology
- **Rationale:** In-memory conflict detection is safer than manual

---

## Execution Order

1. **Phase 1:** Create worktree, backup current specs
2. **Phase 2:** Replace 004-guided-workflow (consolidate version, minus backups)
3. **Phase 3:** Merge path corrections into 006-pr176 tasks.md
4. **Phase 4:** Merge content into 007, 010, 012
5. **Phase 5:** Add 9 new specs from consolidate
6. **Phase 6:** Verify, renumber, commit

## Verification

After merge, run:
```bash
# Verify no 000-original specs were lost
for spec in 005 008 009 011; do
  test -d "specs/$spec" && echo "OK: $spec" || echo "MISSING: $spec"
done

# Verify no empty specs
find specs/ -name "spec.md" -empty

# Verify no backup files
find specs/ -name "*.bak" -o -name "*.pre-rewrite.bak"

# Verify path consistency
grep -r "setup/" specs/ | grep -v "src/setup/"
```

---

*This document should be kept on the 000-integrated-specs branch to track what was merged and why.*
