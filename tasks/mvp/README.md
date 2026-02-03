# MVP Task Set (Separated)

## ⛔ AGENT WARNING: DO NOT MERGE WITH PARENT TASKS

This folder contains **EmailIntelligence MVP** tasks - a **SEPARATE PROJECT**.

| Rule | Directive |
|------|-----------|
| **DO NOT** | Merge this content into `../task_001-028.md` |
| **DO NOT** | Rewrite alignment tasks as email processing tasks |
| **DO NOT** | Use Epic A/B/C definitions for Tasks 002/003/004 |
| **SEE** | [PROJECT_IDENTITY.md](../../PROJECT_IDENTITY.md) for authoritative guidance |

---

## Project Separation

| Location | Project | Purpose |
|----------|---------|---------|
| `tasks/*.md` | Branch Alignment | Git clustering, merge automation, validation |
| `tasks/mvp/` | EmailIntelligence MVP | Email processing, threading, intelligence |

These are **two separate products**. Historical planning documents may conflate them, but the canonical decision is to keep them separate.

---

## MVP Feature Definition (What "Done" Means)

### Input
One mailbox source (Gmail API OR IMAP):
- Incremental sync with cursor/UID tracking
- Handle HTML + text bodies
- Extract headers, threading metadata

### Processing (3-5 signals only)
1. **Threading**: Reconstruct conversations (Message-ID / In-Reply-To / References)
2. **Entity Extraction**: Participants, domains, subject normalization
3. **Classification**: "action required", "FYI", "spam/marketing" (heuristic rules OK)
4. **Basic Clustering** (optional Week 4): Sender/org/topic grouping
5. **Lightweight Summary**: Per-thread summary (rule-based)

### Output
- **Storage**: SQLite/Postgres (minimal schema: emails, threads, labels, results)
- **UI Surface**: Local web view or CLI (list threads, view details, search by sender/subject/tag)
- **Quality**: Parser tests, pipeline idempotency tests, golden fixtures

---

## Proposed Epic Structure (15 tasks, 0.5-2 days each)

### Epic A: Ingest + Normalize (Week 1-2)
- **A1** (0.5d): Mailbox source selection + API/IMAP setup
- **A2** (1.5d): Robust email parser (headers, bodies, threading headers)
- **A3** (1d): Persistence layer (schema + migrations)
- **A4** (0.5d): CLI for sync + inspect (debugging surface)

### Epic B: Intelligence (Week 2-3)
- **B1** (1d): Thread reconstruction + conversation view
- **B2** (1.5d): Signal extraction (participants, orgs, action classification)
- **B3** (1d): Idempotent reprocessing + result storage
- **B4** (0.5d): Search/filter API (sender, domain, tags, action-required)

### Epic C: Present + Polish (Week 3-4)
- **C1** (1d): Web UI or TUI (thread list + details)
- **C2** (0.5d): Structured logging + error reporting
- **C3** (1.5d): Tests (parser, pipeline idempotency, sync regressions)
- **C4** (0.5d): Packaging + README (single "run locally" command)

**Total**: 15 tasks, ~10 days at realistic velocity = 2 weeks development + 1-2 weeks for iteration

---

## Files in This Folder

| File | Purpose |
|------|---------|
| [EPIC_DEFINITIONS.md](EPIC_DEFINITIONS.md) | Full Epic A/B/C specs, feature definitions, effort estimates |
| [MVP_TODO.md](MVP_TODO.md) | Task checklist for MVP implementation |
| README.md | This file - scope warnings and project separation rules |

---

## Source References
- [EPIC_DEFINITIONS.md](EPIC_DEFINITIONS.md) - **Authoritative for MVP scope**
- [PROJECT_IDENTITY.md](../../PROJECT_IDENTITY.md) - **Authoritative for project identity**
- `ORACLE_RECOMMENDATION_TODO.md` (historical proposal - extracted here)
