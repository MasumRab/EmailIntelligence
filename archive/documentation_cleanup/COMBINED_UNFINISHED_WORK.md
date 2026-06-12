# Combined Unfinished Work — All Threads Consolidated

**Generated:** 2026-03-11
**Sources:** 8 threads spanning 2026-02-08 to 2026-03-09
**Supersedes:** `UNFINISHED_TASKS_CONSOLIDATED.md` (2026-02-21, partially completed)

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Completed (verified) |
| 🟡 | Partially done |
| ⬜ | Not started |
| ❌ | Blocked / requires external input |

---

## Project A: CASS Skill Migration (Stages 4-6 Remaining)

**Source threads:** T-019cadaa, T-019cc737, T-019cd0cb
**Location:** `~/.agents/skills/cass/`
**Completed:** Stages 1-3 (SKILL.md 949→70 lines, 8 task scripts, reference docs, archive)

### A1: Stage 4 — Eval Suite Runs 🟡

- ✅ `evals/evals.json` created (3 test cases)
- ⬜ Run with-skill eval (slim SKILL.md) — requires Task subagent
- ⬜ Run baseline eval (backup-v1/SKILL.md) — requires Task subagent
- ⬜ Compare: token usage, search quality, correct flag usage
- ⬜ Iterate SKILL.md if evals reveal gaps

### A2: Stage 5 — Description Optimizer 🟡

- ✅ `cass-workspace/trigger-eval.json` created (20 queries)
- ✅ Multi-backend support added (qwen eval, gemini improve)
- ⬜ Review 20 trigger queries with user via HTML template (needs browser)
- ⬜ Run optimization loop: `run_loop.py --eval-backend qwen --improve-backend gemini`
- ⬜ Update SKILL.md frontmatter description if optimizer suggests changes

### A3: Stage 6 — Cleanup ⬜

- ⬜ Delete `backup-v1/` after 2 weeks of successful use
- ⬜ Write `MIGRATION_COMPLETE.md` with before/after metrics
- ⬜ Remove `MIGRATION_TODO.md`

### A4: Remaining Python Scripts ⬜

- ⬜ `package_skill.py` — distributable `.skill` packaging (adapted from skill-creator)
- ⬜ `aggregate_benchmark.py` — statistical aggregation of eval results (mean, stddev)
- ⬜ `generate_report.py` — Markdown report from benchmark stats

### A5: Technical Investigations ⬜

- ⬜ Gemini headless mode policy denial workaround (can't use skill tool in eval)
- ⬜ iFlow stdout pollution interfering with JSON parsing
- ⬜ `quick_validate.py` path resolution bug (fails with absolute paths)

---

## Project B: PR/.taskmaster Repo Cleanup

**Source threads:** T-019c78fc, T-019c78ff, T-019c7e1c, T-019ca4a1
**Location:** `/home/masum/github/PR/.taskmaster/`

### B1: Root .md Cleanup 🟡

**Current:** 40 root .md files (target: ≤12)
**Previously done:** Task H (moved 96 files) but 28 extras have accumulated since.

Files to move to `docs/` or `archive/`:
- `AMP_DISCOVERY_GUIDE.md`, `AMP_VS_MULTI_AGENT_DISCREPANCY.md`
- `CASS_DISCOVERY_REPORT.md`, `CASS_INTEGRATION.md`
- `CK_MCP_INTEGRATION_COMPLETE.md`, `CK_SEMANTIC_SEARCH_ANALYSIS.md`
- `ENHANCEMENT_REVERSE_ENGINEERING_GUIDE.md`
- `MCP_SETUP_COMPLETE.md`, `MCP_SETUP_VERIFICATION.md`
- `MULTI_AGENT_REVIEW_COMPLETE.md`
- `PAST_WORK_ENHANCEMENT_ANALYSIS.md`
- `PRD_IMPROVEMENT_INVESTIGATION.md`, `PRD_INVESTIGATION_REPORT.md`
- `PROJECT_COMPLETION_REPORT.md`
- `QWEN_CLI_CONFIGURATION_COMPLETE.md`, `QWEN_MCP_QUICKSTART.md`
- `REGRESSION_ANALYSIS.md`, `RISK_MINIMIZATION_PLAN.md`
- `ROUNDTRIP_FIDELITY_TEST_RESULTS.md`
- `TASK_FLOW_CLI_INTEGRATION_ANALYSIS.md`
- `TASK_PRD_DIFF_COMPARISON.md`, `TASK_STATUS_VERIFICATION.md`
- `TASKMASTER_HANDOFF.md` (→ `docs/`)
- `generated_prd_all_tasks.md`, `generated_prd_from_tasks.md` (→ `archive/`)
- `test_generated_prd.md`, `test_roundtrip_prd.md` (→ `archive/`)
- `UNFINISHED_TASKS_CONSOLIDATED.md` (superseded by this file → `archive/`)

**Keep at root:** AGENT.md, AGENTS.md, CLAUDE.md, GEMINI.md, IFLOW.md, QWEN.md, README.md, QUICK_START.md, PROJECT_IDENTITY.md, OPTION_C_VISUAL_MAP.md, TASK_STRUCTURE_STANDARD.md, OLD_TASK_NUMBERING_DEPRECATED.md, this file

### B2: Placeholder & Duplicate File Cleanup ✅ DONE

- ✅ `task_008.10-19.md`, `task_009.1-7.md`, `task_009.8-30.md`, `task_010.1-10.md`, `task_010.11-30.md` — deleted
- ✅ `task_012.013.md` — deleted

### B3: Section Dedup in Tasks 010, 011, 012 ✅ DONE

- ✅ All three files now have 13 `##` sections each (compliant with 14-section standard)

### B4: TBD Metadata in Tasks 010, 011, 012 ✅ DONE

- ✅ task_010.md: Effort filled (56-72h)

### B5: Deduplicate task_002.x Files 🟡

**Current vs target line counts:**

| File | Current | Target | Delta |
|------|---------|--------|-------|
| task_002.3.md | 427 | ~400 | ~7% over |
| task_002.4.md | 579 | ~350 | ~65% over |
| task_002.5.md | 619 | ~400 | ~55% over |
| task_002.6.md | 688 | ~350 | ~97% over |
| task_002.7.md | 529 | ~350 | ~51% over |
| task_002.8.md | 557 | ~450 | ~24% over |
| task_002.9.md | 711 | ~500 | ~42% over |

**Action:** Scan for IMPORTED_FROM duplicates, repeated template boilerplate, empty placeholder sections.

### B6: Fix Legacy Dependency References (010, 011) ⬜

- ⬜ Verify whether `002.x` dependencies in task_010 and task_011 are genuine or stale
- ⬜ Cross-reference with `OPTION_C_VISUAL_MAP.md` and `docs/DEPENDENCY_OUTPUT_AUDIT.md`

### B7: Delete Orphaned Root Scripts 🟡

**Current state:** 3 scripts remain at root:
- `emailintelligence_cli.py` — modular version (imports `src.core.*`), review if needed
- `taskmaster_cli.py` — **keep** (canonical CLI)
- `test_mcp_setup.sh` — review if still useful

### B8: Git Housekeeping ⬜

```bash
git gc --aggressive --prune=now
git remote prune origin
git repack -a -d --depth=250 --window=250
```

---

## Project C: Taskmaster Branch & EmailIntelligence Integration

**Source threads:** T-019cd0cb, T-019cd11d
**Handoff doc:** `TASKMASTER_HANDOFF.md`

### C1: Orphan Branch Resolution ❌ DECISION NEEDED

The `taskmaster` branch in EmailIntelligence repo is an orphan (no common ancestor with `main`). Three options:
1. Cherry-pick valuable files from taskmaster to main
2. Create fresh integration branch from main, copy PR task files
3. **Abandon orphan** and use PR repo as source of truth

**Prerequisite:** User decision on strategy.

### C2: emailintelligence_cli.py Consolidation ❌ DECISION NEEDED

5 copies across 4 locations (main=1,754 lines, modular=1,745 lines). Need to:
- ⬜ Decide canonical version (monolithic `main` vs modular `.taskmaster`)
- ⬜ Check if `src/core/*` modules exist on `main` branch to support modular version
- ⬜ Reduce to 1 canonical copy

### C3: Task List Reconciliation ⬜

- 28 tasks in PR repo vs 72 tasks in taskmaster branch `tasks/tasks.json`
- ⬜ Determine which task set is authoritative
- ⬜ Merge unique tasks if needed

---

## Project D: MVP Pivot (Email Intelligence)

**Source threads:** T-019cd0cb, T-019cd11d
**Status:** Planning phase — no code written

### D1: Decision Points ❌ DECISIONS NEEDED

- ⬜ Mailbox source: Gmail API vs IMAP
- ⬜ Storage: SQLite vs Postgres
- ⬜ UI surface: CLI vs Web
- ⬜ ML classification: Heuristic vs ML (heuristic recommended)
- ⬜ Definition of Done for MVP tasks
- ⬜ Task sizing validation (≤ 2 days per task)

### D2: Epic A — Ingest + Normalize ⬜

- ⬜ A1: Mailbox source selection + API/IMAP setup
- ⬜ A2: Robust email parser (headers, bodies, threading)
- ⬜ A3: Persistence layer (schema + migrations)
- ⬜ A4: CLI for sync + inspect

### D3: Epic B — Intelligence ⬜

- ⬜ B1: Thread reconstruction + conversation view
- ⬜ B2: Signal extraction (participants, orgs, action classification)
- ⬜ B3: Idempotent reprocessing + result storage
- ⬜ B4: Search/filter API

### D4: Epic C — Present + Polish ⬜

- ⬜ C1: Web UI or TUI
- ⬜ C2: Structured logging + error reporting
- ⬜ C3: Tests (parser, pipeline, sync)
- ⬜ C4: Packaging + README

---

## Project E: PR Repo Task Framework (Tasks 001-028)

**Source threads:** T-019cd0cb, T-019cd11d
**Tier system from handoff:**

### E1: Tier 1 — Root Tasks (Unblocks Everything) ⬜

- ⬜ **Task 001**: Align Feature Branches Framework — define how 432 remote branches are categorized
- ⬜ **Task 007**: Branch Identification & Categorization Tool — Python tooling for branch analysis
- ⬜ **Task 011**: Merge Validation Framework — pre-merge safety checks

### E2: Tier 2 — Orphan & CLI Resolution ⬜

- ⬜ Taskmaster branch fate (see C1)
- ⬜ CLI consolidation (see C2)
- ⬜ Task list reconciliation (see C3)

### E3: Tier 3 — Framework-Dependent ⬜

- ⬜ **Task 002**: Branch Clustering System
- ⬜ **Task 005**: Automated Error Detection Scripts
- ⬜ **Task 006**: Pre-merge Validation Scripts
- ⬜ **Task 016**: Branch Backup & Safety Mechanisms

---

## Execution Priority

| Priority | Project | Items | Effort | Blockers |
|----------|---------|-------|--------|----------|
| **P0** | B1 | Root .md cleanup (40→12) | 30 min | None |
| **P0** | B7 | Delete orphaned root scripts | 10 min | None |
| **P1** | A1-A2 | CASS eval runs + optimizer | 2-3h | Task subagent, browser |
| **P1** | B5 | Dedup task_002.x files | 2-3h | None |
| **P2** | A3 | CASS cleanup (backup-v1 deletion) | 10 min | 2 weeks from 2026-03-07 |
| **P2** | B6 | Fix legacy deps in 010/011 | 20 min | None |
| **P2** | B8 | Git housekeeping | 10 min | After cleanups |
| **P3** | A4-A5 | CASS extra scripts + investigations | 4-6h | None |
| **P3** | C1-C3 | EmailIntelligence integration | 4-8h | User decisions |
| **P4** | D1-D4 | MVP pivot (Email Intelligence) | 40-80h | User decisions |
| **P4** | E1-E3 | PR task framework (001-028) | 200+h | C1-C3 resolution |

---

## Thread Reference Index

| Thread | Title | Date | Key Content |
|--------|-------|------|-------------|
| T-019c78fc | Find unfinished sessions (1) | 2026-02-20 | Initial unfinished task compilation |
| T-019c78ff | Consolidate unfinished tasks | 2026-02-20 | Created UNFINISHED_TASKS_CONSOLIDATED.md |
| T-019c7e1c | Option C restructuring | 2026-02-24 | Phase 1 quick wins, .md consolidation |
| T-019ca4a1 | Task deduplication progress | 2026-03-01 | Section dedup, compliance checking |
| T-019cadaa | CASS migration stages 3-5 | 2026-03-06 | Multi-backend eval, archive, evals.json |
| T-019cc6cc | Verify CASS capabilities | 2026-03-07 | Stage verification, script validation |
| T-019cc737 | CASS task-specific scripts | 2026-03-07 | 8 Python scripts, amp_or_cass.py |
| T-019cd0cb | CASS migration review | 2026-03-09 | Handoff doc, MVP pivot, branch investigation |
| T-019cd11d | Taskmaster handoff confirmed | 2026-03-09 | Final handoff, priority tiers |
