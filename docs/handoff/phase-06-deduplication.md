# Phase 6: Content Deduplication

**Purpose:** Remove duplicate content across tool directories.
**Steps:** 6
**Dependencies:** Phase 5 complete

---

## Issues to Fix

| Directory | Issue | File Count | Lines |
|-----------|-------|------------|-------|
| `.kilo/` | MCP empty + Prisma refs | 2 | ~100 |
| `.github/instructions/` | Prisma + TypeScript-only | 3 | ~150 |
| `.clinerules/` | cerebras-mcp references | 2 | ~80 |
| `.cursor/rules/` | TypeScript-only | 2 | ~60 |
| `*_deep.md` files | Duplicates | 6 | 1960 |
| `tools-manifest.json` | Stale Tier 2 file status | 1 | ~50 |

---

## Step 6.1 — Fix .kilo/ MCP + Prisma refs

**Files:** `.kilo/mcp.json`, `.kilo/rules/*.md`

1. Populate `.kilo/mcp.json` with standard MCP template (see Phase 1)
2. Replace Prisma references with Python/SQLAlchemy examples

---

## Step 6.2 — Fix .github/instructions/ Prisma + TypeScript-only

**Files:** `.github/instructions/*.md`

1. Find: `Use TypeScript for all new code`
2. Replace: `Use Python for backend, TypeScript for frontend`

1. Find: `prisma` references
2. Replace: SQLAlchemy equivalent

---

## Step 6.3 — Fix cerebras-mcp CLAUDE.md files

**Files:** `.clinerules/*.md`, `.cursor/rules/*.md`

1. Find: `cerebras-mcp` references
2. Replace: `task-master-ai` (actual MCP in use)

---

## Step 6.4 — Fix TypeScript-only Cursor rules

**Files:** `.cursor/rules/*.mdc`

1. Find: `Use TypeScript for all new code`
2. Replace: `Use Python 3.11+ for backend, TypeScript for frontend`

---

## Step 6.5 — Remove _deep duplicate files

**Files to delete:**
```
.clinerules/cline_rules_deep.md
.windsurf/rules/windsurf_rules_deep.md
.roo/rules/roo_rules_deep.md
.trae/rules/trae_rules_deep.md
.kiro/steering/kiro_rules_deep.md
.kilo/rules/kilo_rules_deep.md
```

```bash
rm .clinerules/*_deep.md
rm .windsurf/rules/*_deep.md
rm .roo/rules/*_deep.md
rm .trae/rules/*_deep.md
rm .kiro/steering/*_deep.md
rm .kilo/rules/*_deep.md
```

---

## Step 6.6 — Reconcile Tier 2 file status in tools-manifest.json

**File:** `.github/instructions/tools-manifest.json`

Do NOT remove Tier 2 file references blindly.

Update manifest entries so they match Phase 5 outcomes:

- `GEMINI.md` — remains a root Tier 2 file when present
- `QWEN.md` — remains a root Tier 2 file when present
- `IFLOW.md` — set `status: "configured"` if restored, otherwise `status: "not_on_branch"`
- `CRUSH.md` — set `status: "configured"` if restored, otherwise `status: "not_on_branch"`
- `LLXPRT.md` — set `status: "configured"` if restored, otherwise `status: "not_on_branch"`

Also update discovery/config notes so Gemini and Qwen do not contradict the live runtime settings.

---

## Gate Check

```bash
echo "=== PHASE 6 GATE CHECK ==="
echo -n "_deep files remaining: "
find . -name "*_deep.md" 2>/dev/null | wc -l
echo -n "Prisma refs in tool rules: "
grep -rl "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ .kilo/rules/ 2>/dev/null | wc -l
echo -n "TypeScript-only in Cursor: "
grep -r "Use TypeScript for all new code" .cursor/rules/ 2>/dev/null | wc -l
echo -n "Tier 2 manifest unresolved: "
python3 -c "import json, os; d=json.load(open('.github/instructions/tools-manifest.json')); m={i['id']: i for i in d['instructions']}; print(sum(1 for p,k in [('IFLOW.md','model_context_iflow'),('CRUSH.md','model_context_crush'),('LLXPRT.md','model_context_llxprt')] if not os.path.isfile(p) and m.get(k, {}).get('status') != 'not_on_branch'))"
```

**Expected:** All `0`
