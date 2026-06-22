# Spec Merge Analysis — 000-integrated-specs + consolidate/cli-unification

**Analysis Date:** 2026-04-14  
**Analyzed By:** Qwen agent (smart-understand, smart-predict, smart-review)  
**Branches:** `origin/000-integrated-specs` vs `origin/consolidate/cli-unification`

---

## Executive Summary

Two branches contain spec content that must be merged into `000-integrated-specs` as the canonical spec hub:

| Metric | 000-integrated-specs | consolidate/cli-unification |
|--------|---------------------|---------------------------|
| **Spec Count** | 9 specs (004-012) | 15 specs + mapping |
| **Total Files** | ~70 | ~121 |
| **Last Updated** | 2026-01-13 | 2026-03-29 |
| **Unique Specs** | 6 specs (005, 008, 009, 010, 011, 012) | 8 specs (001, 003, 005, 006, 007, 008, 009, 010, 013) |
| **Overlapping Specs** | 3 specs (004, 006, 007) | 3 specs (004, 006, 013*) |

*Note: consolidate's 013-task-execution-layer maps to 000's 007-task-execution-layer (same topic).

**consolidate was not intended to have specs** — they were accidentally merged in during consolidation. Regardless, all specs from both branches must be merged into 000.

---

## Spec Inventory

### 000-integrated-specs (9 specs)

| ID | Title | Files | Status |
|----|-------|-------|--------|
| 004 | Guided CLI Workflows | 4 | Needs REPLACE with consolidate version |
| 005 | Orchestration Tools Verification | 9 | KEEP — unique to 000 |
| 006 | PR176 Integration Fixes | 4 | MERGE — minor path corrections |
| 007 | Task Execution Layer | 4 | MERGE with consolidate's 013 |
| 008 | Toolset Additive Analysis | 8 | KEEP — unique to 000 |
| 009 | Agent Context Control | 4 | KEEP — consolidate's 001/002 are empty |
| 010 | Rebase Analysis | 9 | KEEP — consolidate has 001/003 instead |
| 011 | Execution Layer Tasks PR | 4 | KEEP — unique to 000 |
| 012 | Unified Git Analysis | 9 | KEEP — consolidate has 003 version |

### consolidate/cli-unification (specs not intended here)

| ID | Title | Files | Status |
|----|-------|-------|--------|
| 001-agent-context-control | Agent context | 1 | SKIP — empty spec.md |
| 001-pr176-integration-fixes | PR176 via GitHub CLI | 14 | ADD — unique scope |
| 001-rebase-analysis | Rebase intent verification | 6 | MERGE content into 000's 010 |
| 002-agent-context-control | Agent context v2 | 1 | SKIP — empty spec.md |
| 003-rebase-analysis | Rebase analysis v2 | 6 | SKIP — exact duplicate of 001-rebase |
| 003-unified-git-analysis | Unified git analysis | 8 | MERGE content into 000's 012 |
| 004-guided-workflow | Orchestration Core (dev.py) | 23 | REPLACE 000's version |
| 005-cli-architecture | CLI factory pattern | 11 | ADD — HIGH VALUE, from scientific |
| 006-pr176-integration-fixes | PR176 (same as 000) | 4 | MERGE — path corrections |
| 006-unified-architecture | Architecture consolidation | 12 | ADD |
| 007-merge-guidance | Branch merge guidance | 8 | ADD |
| 007-task-execution-layer | — | 0 | — |
| 008-branch-comparison | Branch comparison | 7 | ADD |
| 008-toolset-additive-analysis | — | 0 | — |
| 009-agent-context-control | — | 0 | — |
| 009-implementation | Implementation framework | 9 | ADD |
| 010-orchestration-workflow | Workflow orchestration | 6 | ADD |
| 010-rebase-analysis | — | 0 | — |
| 011-execution-layer-tasks-pr | — | 0 | — |
| 012-unified-git-analysis | — | 0 | — |
| 013-task-execution-layer | Task execution v2 | 4 | MERGE into 000's 007 |
| WORK_TO_SPEC_MAPPING.md | Cross-reference | 1 | ADD |

---

## Drift Analysis — Critical Decision Conflicts

### C1: Entry Point — `dev.py` vs `launch.py`

| Decision | 000 Position | Consolidate Position | Resolution |
|----------|-------------|---------------------|------------|
| Orchestration entry point | `launch.py` with guided workflows | `dev.py` exclusive for dev-tools, `launch.py` forbidden | **Adopt consolidate** — separation of concerns |

### C2: Source Path — `setup/` vs `src/setup/`

| Decision | 000 Position | Consolidate Position | Resolution |
|----------|-------------|---------------------|------------|
| Setup directory | `setup/launch.py` | `src/setup/launch.py` | **Verify against actual codebase**, then apply consistently |

### C3: Architecture Target — Node Engine vs Simple CLI

| Decision | 000 Position | Consolidate Position | Resolution |
|----------|-------------|---------------------|------------|
| Backend target | Not specified | Node Engine (async, enterprise security) | **Complementary** — 000 is CLI layer, consolidate is backend layer |

### C4: CLI Framework — Simple vs Factory Pattern

| Decision | 000 Position | Consolidate Position | Resolution |
|----------|-------------|---------------------|------------|
| CLI architecture | No framework specified | Factory pattern, CommandFactory + Registry | **Adopt consolidate** — production-ready from scientific branch |

### C5: Merge Strategy — Manual vs Automated

| Decision | 000 Position | Consolidate Position | Resolution |
|----------|-------------|---------------------|------------|
| Branch merge approach | Manual guidance with checklists | Automated: `dev.py rebase --apply`, DAG, `git merge-tree` | **Adopt consolidate** — more rigorous |

### C6: Constitution Enforcement

| Decision | 000 Position | Consolidate Position | Resolution |
|----------|-------------|---------------------|------------|
| Rule enforcement | Not specified | AST-based scanning of constitution.md | **Adopt consolidate** — no conflict, valuable addition |

---

## Merge Decision Matrix

### REPLACE (consolidate strictly superior)

| File | Reason |
|------|--------|
| `specs/004-guided-workflow/spec.md` | 723 vs 48 lines — complete rewrite |
| `specs/004-guided-workflow/plan.md` | Detailed layered architecture |
| `specs/004-guided-workflow/tasks.md` | 40+ tasks vs ~30 |

### KEEP (000 is canonical)

| Spec | Files | Reason |
|------|-------|--------|
| 005-orchestration-verification | 9 | No consolidate equivalent |
| 008-toolset-additive | 8 | No consolidate equivalent |
| 009-agent-context-control | 4 | Consolidate's 001/002 are empty |
| 010-rebase-analysis | 9 | Has OpenAPI contract consolidate lacks |
| 011-execution-layer-tasks-pr | 4 | No consolidate equivalent |
| 012-unified-git-analysis | 9 | Consolidate has 003 version with same content |
| 006-pr176 (spec, plan, checklists) | 3 | Identical content |

### MERGE (both have unique value)

| File | Strategy |
|------|----------|
| `specs/006-pr176/tasks.md` | Apply 3 path corrections from consolidate |
| `specs/010-rebase-analysis/spec.md` | Add consolidate's clarification sessions |
| `specs/012-unified-git-analysis/spec.md` | Merge intent narrative content |
| `specs/007-task-execution-layer/` | Combine with consolidate's 013 |

### ADD (consolidate-only)

| Spec | Files |
|------|-------|
| 001-pr176-integration-fixes | 14 |
| 003-unified-git-analysis | 8 |
| 005-cli-architecture | 11 |
| 006-unified-architecture | 12 |
| 007-merge-guidance | 8 |
| 008-branch-comparison | 7 |
| 009-implementation | 9 |
| 010-orchestration-workflow | 6 |
| WORK_TO_SPEC_MAPPING.md | 1 |

### SKIP (empty/duplicate/backup)

| File | Reason |
|------|--------|
| `001-agent-context-control/spec.md` | Empty (0 bytes) |
| `002-agent-context-control/spec.md` | Empty (0 bytes) |
| `003-rebase-analysis/` | Exact duplicate of 001-rebase-analysis |
| `*.bak`, `*.pre-rewrite.bak` | Backup artifacts |

---

## Post-Merge Verification Checklist

- [ ] All 000-original specs still present (005, 007, 008, 009, 010, 011, 012)
- [ ] 004-guided-workflow replaced with consolidate version (minus backups)
- [ ] 006-pr176 tasks.md has verified paths
- [ ] No empty spec.md files
- [ ] No duplicate spec content
- [ ] All consolidate-only specs added
- [ ] WORK_TO_SPEC_MAPPING.md added
- [ ] Numbering consistent (004-012 existing, 013-021 new)
- [ ] Path references consistent across all specs
- [ ] Template path references consistent

---

## Final State After Merge

```
specs/
├── 004-guided-workflow/              ← REPLACED (20 files from consolidate)
├── 005-orchestration-verification/   ← KEEP (9 files, 000 original)
├── 006-pr176-integration-fixes/      ← MERGED (4 files, path corrections)
├── 007-task-execution-layer/         ← MERGED (000 + consolidate 013)
├── 008-toolset-additive-analysis/    ← KEEP (8 files, 000 original)
├── 009-agent-context-control/        ← KEEP (4 files, 000 original)
├── 010-rebase-analysis/              ← MERGED (000 + consolidate 001)
├── 011-execution-layer-tasks-pr/     ← KEEP (4 files, 000 original)
├── 012-unified-git-analysis/         ← MERGED (000 + consolidate 003)
├── 013-cli-architecture/             ← ADD (consolidate 005)
├── 014-unified-architecture/         ← ADD (consolidate 006)
├── 015-merge-guidance/               ← ADD (consolidate 007)
├── 016-branch-comparison/            ← ADD (consolidate 008)
├── 017-implementation/               ← ADD (consolidate 009)
├── 018-orchestration-workflow/       ← ADD (consolidate 010)
├── 019-pr176-github-cli/             ← ADD (consolidate 001)
└── WORK_TO_SPEC_MAPPING.md           ← ADD

Total: ~19 specs, ~190 files
```

---

*Analysis generated by Qwen agent multi-spec review*
