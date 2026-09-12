# Agent File Consolidation: Current State of Plans

**Created:** 2026-05-24
**Branch:** orchestration-tools
**Status:** DECISION-NEEDED — multiple overlapping plans exist, none fully executed
**Purpose:** Document all consolidation approaches, their overlaps, contradictions, and current execution status for future decision-making

---

## Executive Summary

Agent file consolidation has been planned across four branches via at least **6 independent planning documents** and **14 handoff phases**. Despite extensive planning, **no consolidation plan has been fully executed**. The plans overlap, contradict each other, and span different time periods with different assumptions.

This document catalogs every plan, maps their overlaps and differences, records the current state of each agent file across branches, and identifies the key decisions that need to be made before any plan can proceed.

---

## Part 1: Agent File Inventory Across Branches

### 1.1 Root-Level Agent Files

| File | main | orchestration-tools | scientific | taskmaster | Content Purpose |
|------|------|---------------------|-----------|------------|----------------|
| `AGENTS.md` | ✅ | ✅ | ✅ | ✅ (+ `src/core/`, `tasks/` copies) | Universal agent guidance |
| `GEMINI.md` | ✅ | ✅ | ✅ | ✅ (+ `archive/` copy) | Gemini CLI + Jules template |
| `QWEN.md` | ✅ | ✅ | ✅ | ✅ | Qwen Code context |
| `IFLOW.md` | ✅ | ✅ (not on branch) | ✅ (has merge conflict markers) | ✅ | iFlow workflow context |
| `CRUSH.md` | ✅ | ✅ (gitignored/excluded) | ✅ (empty) | ❌ | Crush IDE instructions |
| `LLXPRT.md` | ✅ | ✅ (gitignored/excluded) | ✅ (empty) | ❌ | LLxPRT reasoning guide |
| `WARP.md` | ❌ | ❌ | ❌ | ❌ | Referenced in .gitignore but doesn't exist |
| `.mcp.json` | ✅ | ✅ | ❌ (deleted vs main) | ❌ | MCP server config |
| `AGENT.md` | ✅ | — | ✅ | ✅ | Amp import stub for .taskmaster/ |

### 1.2 Content Divergence Summary

| File | Divergence | Notes |
|------|-----------|-------|
| `AGENTS.md` | **HIGH** — completely different content per branch | main = build/lint/test + architecture; orchestration-tools = Task Master CLI; scientific = TypeScript style + context contamination |
| `GEMINI.md` | **MEDIUM** — dual-purpose on some branches | Lines 1-185 = Jules template, lines 186+ = Gemini CLI instructions |
| `QWEN.md` | **MEDIUM** — scientific docs vs agent instructions | Some branches have project context, others have Qwen-specific agent rules |
| `IFLOW.md` | **LOW** — unique content worth preserving | Has merge conflict markers on scientific branch |
| `CRUSH.md` | **LOW** — mostly duplicated by AGENTS.md | Per `COLLATED_AGENT_FILES_ANALYSIS.md`: no unique content |
| `LLXPRT.md` | **LOW** — mostly duplicated by AGENTS.md | Per `COLLATED_AGENT_FILES_ANALYSIS.md`: no unique content |
| `.mcp.json` | **MEDIUM** — different `alwaysAllow` entries | main has additions that orchestration-tools doesn't |

---

## Part 2: All Consolidation Plans Cataloged

### Plan A: AGENT_GUIDELINES_RESOLUTION_PLAN.md

**Location:** `taskmaster:docs/archive/large_docs/AGENT_GUIDELINES_RESOLUTION_PLAN.md` (also on main)
**Created:** 2025-11-12
**Status:** ACTIVE, HIGH priority — **UNFINISHED**
**Scope:** Cross-branch AGENTS.md synchronization

**Root causes identified:**
1. Branch divergence without synchronization
2. No shared documentation standard
3. Context control system added without full integration
4. Task Master implementation incomplete across branches
5. No enforcement of documentation updates
6. Missing configuration & convention documentation

**Planned phases:**

| Phase | Plan | Status |
|-------|------|--------|
| Phase 2 | Create master `AGENTS.md` template, update branch-specific versions | ❌ Not started |
| Phase 3 | Add profile documentation to `AGENTS.md`, create MCP integration guide | ❌ Not started |
| Phase 4 | Documentation update checklist, PR template, sync script | ❌ Not started |
| Phase 5 | Final consolidated docs, agent implementation guide | ❌ Not started |

**Key assumption:** A single master `AGENTS.md` template can serve all branches with branch-specific sections.

---

### Plan B: Handoff Phases 5-14 (orchestration-tools)

**Location:** `orchestration-tools:docs/handoff/phase-05` through `phase-14`
**Created:** 2026-03 to 2026-05
**Status:** Phases 1-4 complete, Phase 5+ partially done, Phase 14 just completed on main

**Phase execution status:**

| Phase | Doc | Focus | Status |
|-------|-----|-------|--------|
| 5 | `phase-05-file-cleanup.md` | Tier 2 root file policy | ⚠️ Partially done |
| 6 | `phase-06-deduplication.md` | Content dedup (tool dirs, manifests) | ❌ Not started |
| 7 | `phase-07-hierarchy.md` | Subdirectory-scoped AGENTS.md | ❌ Not started |
| 8 | (referenced) | — | Unknown |
| 9 | `phase-09-verification.md` | Verification layer | ❌ Not started |
| 10 | (referenced) | Reference material | Unknown |
| 11 | (referenced) | Remediation | Unknown |
| 12 | `phase-12-deep-agent-handoff.md` | Deep agent handoff for Phase 5/6/9 | ❌ Not started |
| 13 | `phase-13-smart-amp-deep-agent-autonomous-handoff.md` | Autonomous completion of all remaining | ❌ Not started |
| 14 | `phase-14-gitignore-unification.md` | Gitignore consolidation | ✅ Done on main (2026-05-24) |

**Key assumption:** CLI-first model with `.ruler/AGENTS.md` as canonical Tier 1 source, distributed via Ruler to all tools.

---

### Plan C: AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md

**Location:** `orchestration-tools:docs/AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md`
**Created:** 2026-04-06
**Status:** Audit complete, roadmap **UNFINISHED**

**Key findings:**
- 30 total issues (13 original + 17 additional)
- 11,092 duplicated lines across tool directories
- 15 files with wrong content
- 5 empty/broken MCP configs

**Roadmap items:**

| ID | Action | Status |
|----|--------|--------|
| T13 | Split `GEMINI.md` (Jules template → `.gemini/JULES_TEMPLATE.md`) | ❌ |
| T14 | Replace `QWEN.md` content with proper Tier 2 instructions | ❌ |
| T16 | Create `.ruler/` canonical config | ❌ |
| T18 | Create subdirectory `AGENTS.md` files (`src/core/`, `src/backend/`, `client/`) | ❌ |
| T21 | Configure Ruler for canonical distribution | ❌ |

**Key assumption:** Tool-specific rules should move from dotdirs to `.github/instructions/` as canonical source.

---

### Plan D: ACTUAL_AGENT_ECOSYSTEM.md

**Location:** `orchestration-tools:docs/handoff/ACTUAL_AGENT_ECOSYSTEM.md`
**Created:** 2026-04-10
**Status:** Classification complete, Phases 0-5 **MISALIGNED**

**Critical finding:** The actual workflow is CLI-first, not IDE-first. All prior phases assumed IDE-first prioritization.

**Tool classification:**

| Tier | Type | Tools |
|------|------|-------|
| Tier 1 | Primary CLI | Gemini, Qwen, OpenCode, AMP, Kilo |
| Tier 2 | Secondary CLI | Aider, Ra-aid, Goose, OMP, Letta, OpenHands |
| Tier 3 | Tertiary | **Crush, LLXPRT**, Pi, Shai, Parallel-AI, Mistral-Vibe, Agent-Deck |

**Key assumption:** CLI tools read root `AGENTS.md` via `settings.json contextFileName`. IDE tools use Ruler `output_path`. No merges between branches.

---

### Plan E: ORCHESTRATION_IDE_DISTRIBUTION_PLAN.md

**Location:** `orchestration-tools:docs/source-of-truth/orchestration/ORCHESTRATION_IDE_DISTRIBUTION_PLAN.md`
**Created:** 2025-11-17
**Status:** Active but **STALE** — pre-dates CLI-first correction

**Distribution matrix:**

| Files | Always Distribute | main | scientific |
|-------|-------------------|------|-----------|
| AGENTS.md | ✅ | ✅ variant per branch | ✅ variant per branch |
| CRUSH.md, LLXPRT.md, IFLOW.md | ✅ | ✅ | ✅ |
| QWEN.md, CLAUDE.md | ✅ | ✅ | ✅ |
| .mcp.json | ✅ standardized | ✅ | ✅ |
| .claude/, .cursor/, .windsurf/ | Conditional | ✅ | ✅ |
| Orchestration modules | Conditional | ✅ | ❌ |

**Key assumption:** orchestration-tools is the source branch for distributing agent files to main and scientific.

---

### Plan F: COLLATED_AGENT_FILES_ANALYSIS.md

**Location:** `orchestration-tools:docs/handoff/content-archive/COLLATED_AGENT_FILES_ANALYSIS.md`
**Created:** 2026-04-09
**Status:** Analysis complete, recommendations **NOT EXECUTED**

**Content verdicts:**

| File | Unique Content | Decision |
|------|---------------|----------|
| `IFLOW.md` | ✅ Project structure, AI models setup, iFlow CLI workflow | PRESERVE unique portions |
| `CRUSH.md` | ❌ All duplicated in AGENTS.md | ARCHIVE ONLY |
| `LLXPRT.md` | ❌ All duplicated in AGENTS.md | ARCHIVE ONLY |

---

## Part 3: Overlaps and Differences Between Plans

### 3.1 Where Plans Agree

| Topic | Consensus |
|-------|-----------|
| `AGENTS.md` is Tier 1 | All plans agree: `.ruler/AGENTS.md` = canonical shared content |
| `GEMINI.md` stays at root | Plans B, C agree: Gemini CLI auto-loads from root |
| `QWEN.md` stays at root | Plans B, C agree: session_manager.py reads from root |
| `IFLOW.md` has unique value | Plans C, F agree: preserve unique content |
| CRUSH.md / LLXPRT.md are low value | Plans D, F agree: mostly duplicated, archive candidates |
| Branch isolation | All plans agree: no merges between main/scientific/orchestration-tools |
| Distribution from orchestration-tools | Plans B, E agree: orchestration-tools is source for distribution |

### 3.2 Where Plans Contradict

| Topic | Plan A (Resolution Plan) | Plan B (Handoff Phases) | Plan D (Ecosystem) | Plan E (Distribution) |
|-------|-------------------------|----------------------|---------------------|----------------------|
| **AGENTS.md on orchestration-tools** | Create master template | `.ruler/AGENTS.md` is canonical source | CLI tools read root `AGENTS.md` | orchestration-tools distributes AGENTS.md |
| **CRUSH.md / LLXPRT.md** | Not addressed | Branch-specific, restore if used | Tier 3 tertiary tools | Always distribute to all branches |
| **Source of truth for AGENTS.md** | Single master template | `.ruler/AGENTS.md` | Root `AGENTS.md` (Ruler syncs) | orchestration-tools branch |
| **IDE vs CLI priority** | Not addressed (pre-dates finding) | IDE-first (pre-correction) | **CLI-first** (corrected) | IDE-first (stale) |
| **Tool-specific rules location** | Not addressed | `.github/instructions/` | Root `AGENTS.md` via Ruler | Dotdirs (`.claude/`, `.cursor/`, etc.) |
| **WARP.md** | Not addressed | Not addressed | Not addressed | Not addressed |

### 3.3 Critical Contradictions in Scripts

**`scripts/lib/orchestration-approval.sh`** says:
> `AGENTS.md` and `CRUSH.md` are **intentionally NOT synced** from orchestration-tools

**`docs/source-of-truth/orchestration/ORCHESTRATION_IDE_DISTRIBUTION_PLAN.md`** says:
> Distribute `AGENTS.md`, `CRUSH.md`, `LLXPRT.md` to main and scientific

**`docs/handoff/ACTUAL_AGENT_ECOSYSTEM.md`** says:
> CLI tools (AMP, Gemini, Qwen, OpenCode, Kilo) read root `AGENTS.md` via `settings.json contextFileName` — Ruler syncs it

**Resolution needed:** Which policy governs? The approval script, the distribution plan, or the ecosystem doc?

### 3.4 Stale vs Corrected Documents

| Document | Status | Why |
|----------|--------|-----|
| `ORCHESTRATION_IDE_DISTRIBUTION_PLAN.md` | **STALE** | Pre-dates CLI-first correction |
| `AGENT_INSTRUCTIONS_MANIFEST.md` | **STALE** | Says `GEMINI.md` "not yet created" but it exists on all branches |
| `orchestration-approval.sh` | **CONFLICTS** | Says AGENTS.md not synced; later docs say it should be |
| `AGENT_GUIDELINES_RESOLUTION_PLAN.md` | **STALE** | Pre-dates CLI-first finding; assumes single template approach |
| `ACTUAL_AGENT_ECOSYSTEM.md` | **CURRENT** | CLI-first classification, Phase 4 complete |
| `AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md` | **CURRENT** | Comprehensive audit with actionable roadmap |
| `COLLATED_AGENT_FILES_ANALYSIS.md` | **CURRENT** | Content-level analysis of IFLOW/CRUSH/LLXPRT |

---

## Part 4: Validation and Distribution Scripts

### 4.1 Scripts That Enforce Agent File Policy

| Script | Branch | What It Checks |
|--------|--------|---------------|
| `scripts/validate-ide-agent-inclusion.sh` | orchestration-tools | Tracked presence of AGENTS.md, CRUSH.md, LLXPRT.md, IFLOW.md, QWEN.md, .mcp.json |
| `scripts/verify-agent-content.sh` | orchestration-tools | Tier 1 content in `.ruler/AGENTS.md`; Tier 2 files |
| `scripts/verify-agent-docs-consistency.sh` | orchestration-tools | Compares AGENTS.md across branches |
| `scripts/validate-orchestration-context.sh` | orchestration-tools | Flags agent/context guidance as contamination on orchestration-tools |
| `scripts/distribute-orchestration-files.sh` | orchestration-tools | Main distribution entrypoint; supports `--sync-from-remote`, `--with-validation` |

### 4.2 Script Contradictions

| Script | Says | Conflicts With |
|--------|------|---------------|
| `orchestration-approval.sh` | AGENTS.md NOT synced | IDE Distribution Plan, ACTUAL_AGENT_ECOSYSTEM |
| `validate-orchestration-context.sh` | Agent files are contamination | IDE Distribution Plan (says distribute them) |
| `distribute-orchestration-files.sh` | Distributes all agent files | `orchestration-approval.sh` (blocks some) |

---

## Part 5: Decisions Required

Before any consolidation plan can proceed, these decisions must be made:

### D1: AGENTS.md Source of Truth
- **Option A:** Single master template (Plan A approach) — one template, branch-specific sections
- **Option B:** `.ruler/AGENTS.md` as canonical, distributed via Ruler (Plan B/D approach)
- **Option C:** Root `AGENTS.md` per branch, no canonical source, manual sync
- **Current state:** Option B is the latest direction but not fully executed

### D2: CRUSH.md and LLXPRT.md Disposition
- **Option A:** Archive on all branches (Plan F: no unique content)
- **Option B:** Keep tracked on main, gitignored elsewhere (current state)
- **Option C:** Restore on orchestration-tools and distribute (Plan E approach)
- **Current state:** Option B, but `.gitignore` exceptions keep them tracked on main

### D3: WARP.md
- **Option A:** Remove from `.gitignore` exceptions (file doesn't exist on any branch)
- **Option B:** Create the file if there's a future use case
- **Current state:** `!` exception in `.gitignore` on main for a non-existent file

### D4: `.mcp.json` Consistency
- **Option A:** Identical across all branches (Plan E: standardized)
- **Option B:** Branch-specific with documented differences
- **Current state:** Different `alwaysAllow` entries between main and orchestration-tools

### D5: Script Policy Resolution
- **Option A:** Update `orchestration-approval.sh` to allow AGENTS.md sync
- **Option B:** Update distribution plan to match approval script (no sync)
- **Option C:** Rewrite both to match CLI-first ecosystem model
- **Current state:** Scripts contradict each other

### D6: Stale Document Cleanup
- **Option A:** Mark stale docs with deprecation notices, keep for reference
- **Option B:** Move stale docs to `content-archive/`, replace with corrected versions
- **Option C:** Delete stale docs, keep only current ones
- **Current state:** Stale and current docs coexist without deprecation markers

---

## Part 6: Recommended Execution Order

If consolidation proceeds, this is the logical order based on dependencies:

1. **Resolve D1** (AGENTS.md source of truth) — blocks everything else
2. **Resolve D5** (script policy) — unblocks distribution
3. **Resolve D6** (stale docs) — prevents future confusion
4. **Execute Plan C roadmap** (T13-T21) — concrete, actionable items
5. **Resolve D2** (CRUSH/LLXPRT) — depends on D1
6. **Resolve D3** (WARP.md) — trivial cleanup
7. **Resolve D4** (.mcp.json) — independent
8. **Execute Plan B Phase 6** (dedup) — depends on D1, D5
9. **Execute Plan B Phase 7** (hierarchy) — depends on Phase 6
10. **Run Phase 9 verification** — validates everything

---

## Appendix A: Source Documents Referenced

| Document | Branch | Path |
|----------|--------|------|
| AGENT_GUIDELINES_RESOLUTION_PLAN.md | taskmaster, main | `docs/archive/large_docs/` |
| phase-05-file-cleanup.md | orchestration-tools | `docs/handoff/` |
| phase-06-deduplication.md | orchestration-tools | `docs/handoff/` |
| phase-07-hierarchy.md | orchestration-tools | `docs/handoff/` |
| phase-09-verification.md | orchestration-tools | `docs/handoff/` |
| phase-12-deep-agent-handoff.md | orchestration-tools | `docs/handoff/` |
| phase-13-smart-amp-deep-agent-autonomous-handoff.md | orchestration-tools | `docs/handoff/` |
| phase-14-gitignore-unification.md | orchestration-tools | `docs/handoff/` |
| AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md | orchestration-tools | `docs/` |
| ACTUAL_AGENT_ECOSYSTEM.md | orchestration-tools | `docs/handoff/` |
| COLLATED_AGENT_FILES_ANALYSIS.md | orchestration-tools | `docs/handoff/content-archive/` |
| ORCHESTRATION_IDE_DISTRIBUTION_PLAN.md | orchestration-tools | `docs/source-of-truth/orchestration/` |
| ORCHESTRATION_IDE_INCLUSION_SUMMARY.md | orchestration-tools | `docs/source-of-truth/orchestration/` |
| orchestration-approval.sh | orchestration-tools | `scripts/lib/` |
| distribute-orchestration-files.sh | orchestration-tools | `scripts/` |
| validate-ide-agent-inclusion.sh | orchestration-tools | `scripts/` |
| verify-agent-content.sh | orchestration-tools | `scripts/` |
| verify-agent-docs-consistency.sh | orchestration-tools | `scripts/` |
| validate-orchestration-context.sh | orchestration-tools | `scripts/` |
| COMBINED_UNFINISHED_WORK.md | taskmaster | root |
| TASKMASTER_HANDOFF.md | taskmaster | root |
| UNFINISHED_TASKS_CONSOLIDATED.md | main | `.taskmaster/` |
| READ_THIS_FIRST_INVESTIGATION_INDEX.md | main | `.taskmaster/docs/` |

## Appendix B: Tier Classification Cross-Reference

Three different tier systems exist across plans:

### B.1 Tool Tier System (ACTUAL_AGENT_ECOSYSTEM.md)
| Tier | Scope | Tools |
|------|-------|-------|
| Tier 1 | Primary CLI | Gemini, Qwen, OpenCode, AMP, Kilo |
| Tier 2 | Secondary CLI | Aider, Ra-aid, Goose, OMP, Letta, OpenHands |
| Tier 3 | Tertiary | Crush, LLXPRT, Pi, Shai, Parallel-AI, Mistral-Vibe, Agent-Deck |

### B.2 Content Tier System (Gap Analysis / Phase 5)
| Tier | Scope | Files |
|------|-------|-------|
| Tier 1 | Shared content | `.ruler/AGENTS.md` |
| Tier 2 | Tool-specific root files | GEMINI.md, QWEN.md, IFLOW.md, CRUSH.md, LLXPRT.md |
| Tier 3 | (not formally defined) | WARP.md, AGENT.md |

### B.3 Task Priority Tier System (TASKMASTER_HANDOFF.md)
| Tier | Scope | Description |
|------|-------|-------------|
| Tier 1 | Unblocks everything | Root tasks |
| Tier 2 | Resolve orphan branch | Branch-specific resolution |
| Tier 3 | After framework established | Framework-dependent tasks |
| Tier 4 | MVP pivot | Separate project |

**Note:** These three tier systems are independent and should not be conflated. Tool tiers classify AI coding tools. Content tiers classify agent instruction files. Task priority tiers classify work items.
