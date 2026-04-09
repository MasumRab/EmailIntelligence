# Phase 5: File Cleanup

**Purpose:** Relocate GEMINI.md and QWEN.md to proper structure.
**Steps:** 4
**Dependencies:** Phase 1 complete

---

## Step 5.1 — Relocate GEMINI.md

**Issue:** GEMINI.md contains Jules backlog template (not agent rules) in first 185 lines.
**Action:** Split into two files.

**Create:** `docs/jules-backlog-template.md` (lines 1-185)
**Keep:** `GEMINI.md` (lines 186+ only)

```bash
# Extract Jules content
head -185 GEMINI.md > docs/jules-backlog-template.md

# Keep only Gemini-specific content
tail -n +186 GEMINI.md > GEMINI.md.tmp && mv GEMINI.md.tmp GEMINI.md
```

---

## Step 5.2 — Relocate QWEN.md

**Issue:** QWEN.md contains session_manager content (not agent rules).
**Action:** Move to docs/

```bash
mv QWEN.md docs/qwen-session-manager.md
```

---

## Step 5.3 — Verify relocations

```bash
echo "=== FILE RELOCATION CHECK ==="
test -f docs/jules-backlog-template.md && echo "jules-backlog-template.md: EXISTS" || echo "MISSING"
test -f docs/qwen-session-manager.md && echo "qwen-session-manager.md: EXISTS" || echo "MISSING"
test -f GEMINI.md && echo "GEMINI.md: EXISTS" || echo "MISSING"
test -f QWEN.md && echo "QWEN.md: STILL IN ROOT (FAIL)" || echo "QWEN.md: REMOVED FROM ROOT (PASS)"
```

---

## Step 5.4 — Final verification

```bash
echo "=== PHASE 5 GATE CHECK ==="
wc -l GEMINI.md
# Should be less than original 350+ lines
grep -c "Jules" GEMINI.md || echo "0"
# Should be 0 (Jules content moved)
```

---

## Note

Gemini CLI auto-loads `GEMINI.md` from project root. Do NOT move it completely — only split the non-Gemini content.
