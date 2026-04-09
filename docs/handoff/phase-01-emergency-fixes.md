# Phase 1: Emergency Fixes

**Purpose:** Fix broken MCP configurations and merge conflicts.
**Steps:** 13
**Dependencies:** None (can run independently)

---

## MCP Config Template

All MCP files use this template:

```json
{
  "mcpServers": {
    "task-master-ai": {
      "type": "stdio",
      "command": "npm",
      "args": ["exec", "task-master-ai"],
      "env": {
        "GOOGLE_API_KEY": "${GOOGLE_API_KEY}",
        "GEMINI_API_KEY": "${GEMINI_API_KEY}",
        "XAI_API_KEY": "${XAI_API_KEY}",
        "OPENROUTER_API_KEY": "${OPENROUTER_API_KEY}",
        "MISTRAL_API_KEY": "${MISTRAL_API_KEY}",
        "OLLAMA_API_KEY": "${OLLAMA_API_KEY}",
        "GITHUB_API_KEY": "${GITHUB_API_KEY}"
      }
    }
  }
}
```

---

## Step 1.1 — Resolve CLAUDE.md merge conflict

**File:** `CLAUDE.md`
**Issue:** Git merge conflict markers present
**Action:** OVERWRITE with Claude-specific content (see original handoff lines 86-198)

**Verify:**
```bash
grep -c '<<<<<<\|======\|>>>>>>' CLAUDE.md
```
**Expected:** `0`

---

## Step 1.3 — Fix .roo/mcp.json

**File:** `.roo/mcp.json`
**Issue:** 0 bytes (empty)
**Action:** OVERWRITE with MCP config template

**Verify:**
```bash
python3 -c "import json; json.load(open('.roo/mcp.json')); print('VALID')"
```

---

## Step 1.5 — Fix .cursor/mcp.json

**File:** `.cursor/mcp.json`
**Issue:** 0 bytes (empty)
**Action:** OVERWRITE with MCP config template

**Verify:**
```bash
python3 -c "import json; json.load(open('.cursor/mcp.json')); print('VALID')"
```

---

## Step 1.7 — Fix .claude/mcp.json

**File:** `.claude/mcp.json`
**Issue:** 0 bytes (empty)
**Action:** OVERWRITE with MCP config template

**Verify:**
```bash
python3 -c "import json; json.load(open('.claude/mcp.json')); print('VALID')"
```

---

## Step 1.9 — Fix .windsurf/mcp.json

**File:** `.windsurf/mcp.json`
**Issue:** Placeholder keys like `YOUR_PERPLEXITY_API_KEY_HERE`
**Action:** OVERWRITE with MCP config template

**Verify:**
```bash
grep -c "YOUR_" .windsurf/mcp.json
```
**Expected:** `0`

---

## Step 1.11 — Create .trae/mcp.json

**File:** `.trae/mcp.json`
**Issue:** Does not exist (directory `.trae/` exists with `rules/` only)
**Action:** CREATE with MCP config template

**Verify:**
```bash
python3 -c "import json; json.load(open('.trae/mcp.json')); print('VALID')"
```

---

## Step 1.13 — Delete .rules file

**File:** `.rules`
**Issue:** Stale 417-line gitignored duplicate of AGENTS.md
**Action:** DELETE

```bash
rm .rules
```

**Verify:**
```bash
test ! -f .rules && echo "DELETED" || echo "STILL EXISTS"
```

---

## Gate Check

After completing all steps, run:

```bash
echo "=== PHASE 1 GATE CHECK ==="
for f in .roo/mcp.json .cursor/mcp.json .claude/mcp.json .windsurf/mcp.json .trae/mcp.json; do
  echo -n "$f: "
  python3 -c "import json; json.load(open('$f')); print('VALID')" 2>/dev/null || echo "INVALID"
done
echo -n "CLAUDE.md conflicts: "
grep -c '<<<<<<\|======\|>>>>>>' CLAUDE.md || echo "0"
echo -n ".rules exists: "
test -f .rules && echo "YES (FAIL)" || echo "NO (PASS)"
```

**All must pass before proceeding to Phase 2.**
