# EmailIntelligence MVP - Epic Definitions

**Project**: EmailIntelligence (SEPARATE from Branch Alignment)
**Location**: This folder (`tasks/mvp/`) only
**Status**: Planning phase

---

## ⛔ Scope Boundary

This is a **SEPARATE PROJECT** from Branch Alignment.

| This Project (MVP) | Parent Project (Alignment) |
|--------------------|----------------------------|
| Email processing | Git branch clustering |
| Mailbox sync | Merge automation |
| Thread intelligence | Pre-merge validation |
| Search/filter UI | Branch alignment framework |

**DO NOT** merge these epics into `../task_001-028.md`

---

## MVP Feature Definition

### Input
One mailbox source (Gmail API OR IMAP):
- Incremental sync with cursor/UID tracking
- Handle HTML + text bodies
- Extract headers, threading metadata

### Processing (3-5 signals only)
1. **Threading**: Reconstruct conversations (Message-ID / In-Reply-To / References)
2. **Entity Extraction**: Participants, domains, subject normalization
3. **Classification**: "action required", "FYI", "spam/marketing" (heuristic rules OK)
4. **Basic Clustering** (optional): Sender/org/topic grouping
5. **Lightweight Summary**: Per-thread summary (rule-based)

### Output
- **Storage**: SQLite/Postgres (minimal schema: emails, threads, labels, results)
- **UI Surface**: Local web view or CLI (list threads, view details, search by sender/subject/tag)
- **Quality**: Parser tests, pipeline idempotency tests, golden fixtures

---

## Epic Structure (15 tasks, 0.5-2 days each)

### Epic A: Ingest + Normalize (Week 1-2)
| Task | Effort | Description |
|------|--------|-------------|
| A1 | 0.5d | Mailbox source selection + API/IMAP setup |
| A2 | 1.5d | Robust email parser (headers, bodies, threading headers) |
| A3 | 1d | Persistence layer (schema + migrations) |
| A4 | 0.5d | CLI for sync + inspect (debugging surface) |

### Epic B: Intelligence (Week 2-3)
| Task | Effort | Description |
|------|--------|-------------|
| B1 | 1d | Thread reconstruction + conversation view |
| B2 | 1.5d | Signal extraction (participants, orgs, action classification) |
| B3 | 1d | Idempotent reprocessing + result storage |
| B4 | 0.5d | Search/filter API (sender, domain, tags, action-required) |

### Epic C: Present + Polish (Week 3-4)
| Task | Effort | Description |
|------|--------|-------------|
| C1 | 1d | Web UI or TUI (thread list + details) |
| C2 | 0.5d | Structured logging + error reporting |
| C3 | 1.5d | Tests (parser, pipeline idempotency, sync regressions) |
| C4 | 0.5d | Packaging + README (single "run locally" command) |

**Total**: 15 tasks, ~10 days at realistic velocity = 2 weeks development + 1-2 weeks iteration

---

## Definition of Done (MVP Tasks)

Each MVP task must have:
- [ ] Complete technical specs (schemas, APIs)
- [ ] Tests OR fixtures
- [ ] Idempotent behavior (where relevant)
- [ ] Logging
- [ ] "How to run" documentation

---

## Decision Points

| Decision | Options | Status |
|----------|---------|--------|
| Mailbox source | Gmail API vs IMAP | ❓ Pending |
| Storage | SQLite vs Postgres | ❓ Pending |
| UI surface | CLI vs Web | ❓ Pending |
| ML classification | Heuristic vs ML | ❓ Pending (recommend heuristic for MVP) |

---

## Source References

This content was extracted from:
- `ORACLE_RECOMMENDATION_TODO.md` (historical pivot proposal)
- Planning discussions in previous threads

**Authoritative for MVP scope**: This file
**Authoritative for project identity**: `../../PROJECT_IDENTITY.md`
