# Phase 8: Tool Orchestration

**Purpose:** Define tool responsibility matrix and configure sync tools.
**Steps:** 4
**Dependencies:** Phase 7 complete

---

## Step 8.1 — Define tool responsibility matrix

| Tool | Responsibility | Config File |
|------|---------------|-------------|
| **Ruler** | Primary sync (TOML) | `.ruler/ruler.toml` |
| **RuleSync** | CI drift detection | `rulesync.jsonc` |
| **Agent RuleZ** | Runtime enforcement | `.claude/hooks.yaml` |

**Workflow:**
1. Edit `.ruler/AGENTS.md` for content changes
2. Run `ruler apply` to distribute
3. Run `rulesync generate --check` in CI
4. Agent RuleZ enforces at runtime

---

## Step 8.2 — Configure Ruler for canonical distribution

Ruler is already configured (Phase 3). Verify:

```bash
ruler apply --project-root . --dry-run
```

---

## Step 8.3 — Configure RuleSync for CI

**File:** `rulesync.jsonc`

Ensure targets include all active tools:

```json
{
  "targets": [
    "claudecode",
    "cursor",
    "cline",
    "roo",
    "kiro",
    "windsurf",
    "qwencode",
    "opencode",
    "geminicli",
    "agentsmd",
    "codexcli"
  ]
}
```

**CI Command:**
```bash
rulesync generate --check
```
Exit code 1 = drift detected (files out of sync)

---

## Step 8.4 — Verify Agent RuleZ runtime hooks

Agent RuleZ is configured (Phase 4). Test:

```bash
/tmp/rulez/rulez debug --config .claude/hooks.yaml --event "Bash:git push --force origin main"
```

**Expected:** `BLOCKED by rule: block-force-push`

---

## Gate Check

```bash
echo "=== PHASE 8 GATE CHECK ==="
test -f .ruler/ruler.toml && echo "Ruler config: PASS" || echo "Ruler config: FAIL"
test -f rulesync.jsonc && echo "RuleSync config: PASS" || echo "RuleSync config: FAIL"
test -f .claude/hooks.yaml && echo "Agent RuleZ config: PASS" || echo "Agent RuleZ config: FAIL"
```
