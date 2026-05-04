# Phase 7: Hierarchical Structure

**Purpose:** Create directory-level AGENTS.md files for path-scoped rules.
**Steps:** 3
**Dependencies:** Phase 6 complete

---

## Step 7.1 — Verify .ruler/AGENTS.md as root source

```bash
test -f .ruler/AGENTS.md && echo "ROOT SOURCE: EXISTS" || echo "ROOT SOURCE: MISSING"
```

The `.ruler/AGENTS.md` should be the canonical source distributed to all tools.

---

## Step 7.2 — Create subdirectory AGENTS.md files

Create AGENTS.md in directories with high complexity (score > 15):

| Directory | Score | Create AGENTS.md? |
|-----------|-------|-------------------|
| `src/core/` | 20+ | YES |
| `src/backend/` | 18+ | YES |
| `client/` | 15+ | YES |
| `modules/` | 12 | NO |
| `scripts/` | 10 | NO |

**Template for subdirectory AGENTS.md:**

```markdown
# [Directory Name] — AI Agent Context

## Purpose
[What this directory contains]

## Key Files
- `file1.py` — [Description]
- `file2.py` — [Description]

## Patterns
- [Pattern 1]
- [Pattern 2]

## Tests
`pytest tests/[directory]/`
```

---

## Step 7.3 — Deduplicate: child files never repeat parent

**Rule:** Subdirectory AGENTS.md files should NOT repeat content from `.ruler/AGENTS.md`.

**Check:**
```bash
# Extract unique content from child
grep -vf .ruler/AGENTS.md src/core/AGENTS.md
```

Should show only directory-specific content.

---

## Gate Check

```bash
echo "=== PHASE 7 GATE CHECK ==="
test -f .ruler/AGENTS.md && echo "Root AGENTS.md: PASS" || echo "Root AGENTS.md: FAIL"
test -f src/core/AGENTS.md && echo "src/core/AGENTS.md: EXISTS" || echo "src/core/AGENTS.md: NOT CREATED"
test -f src/backend/AGENTS.md && echo "src/backend/AGENTS.md: EXISTS" || echo "src/backend/AGENTS.md: NOT CREATED"
```
