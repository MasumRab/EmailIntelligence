# Phase 4: Agent RuleZ Setup

**Purpose:** Configure runtime enforcement hooks.
**Steps:** 6
**Dependencies:** Phase 1 complete

---

## External Reference

- **Agent RuleZ GitHub:** https://github.com/SpillwaveSolutions/agent_rulez
- **Supported runtimes:** Claude Code, OpenCode, Gemini CLI, Codex CLI
- **Rule types:** Block, Inject, Run

---

## Step 4.1 — Install rulez binary

**Status:** ✅ ALREADY INSTALLED

```bash
# Verify installation
which rulez  # → ~/.local/bin/rulez
rulez --version  # → rulez 2.3.0
```

**Location:** `/home/masum/.local/bin/rulez` (v2.3.0)

If not installed, use:
```bash
# Option A: Download binary
curl -sL https://github.com/SpillwaveSolutions/agent_rulez/releases/latest/download/rulez-linux-x64 -o /tmp/rulez/rulez
chmod +x /tmp/rulez/rulez
sudo mv /tmp/rulez/rulez /usr/local/bin/

# Option B: Add to mise (recommended)
# mise use -g pipx:agent-rulez
```

---

## Step 4.2 — Create .claude/hooks.yaml

**File:** `.claude/hooks.yaml`
**Action:** CREATE

```yaml
version: "1.0"
settings:
  debug_logs: false
  fail_open: true
  script_timeout: 5

rules:
  # Block force push to main/master
  - name: block-force-push
    matchers:
      tools: [Bash]
      command_match: "git push.*(--force|-f).*(main|master)"
    actions:
      block: true
    metadata:
      priority: 100
      enabled: true

  # Block direct commits to main
  - name: block-main-commit
    matchers:
      tools: [Bash]
      command_match: "git commit.*main|master"
    actions:
      block: true
    metadata:
      priority: 90
      enabled: true

  # Inject context before file edits
  - name: inject-edit-context
    matchers:
      tools: [Edit, Write]
    actions:
      inject: "Before editing, verify file exists and you have read it."
    metadata:
      priority: 50
      enabled: true

  # Block secrets in code
  - name: block-secrets
    matchers:
      tools: [Edit, Write]
      content_match: "(api_key|secret|password|token)\\s*=\\s*['\"][^'\"]+['\"]"
    actions:
      block: true
    metadata:
      priority: 100
      enabled: true
```

---

## Step 4.3 — Validate hooks.yaml

```bash
/tmp/rulez/rulez validate --config .claude/hooks.yaml
```

**Expected:** `Valid configuration` or no errors

---

## Step 4.4 — Lint hooks.yaml

```bash
/tmp/rulez/rulez lint --config .claude/hooks.yaml
```

**Expected:** No overlapping matchers, no warnings

---

## Step 4.5 — Debug test: force push blocked

```bash
/tmp/rulez/rulez debug --config .claude/hooks.yaml --event "Bash:git push --force origin main"
```

**Expected:** `BLOCKED by rule: block-force-push`

---

## Step 4.6 — Debug test: normal commit allowed

```bash
/tmp/rulez/rulez debug --config .claude/hooks.yaml --event "Bash:git commit -m 'test'"
```

**Expected:** `ALLOWED` or no block

---

## Gate Check

```bash
echo "=== PHASE 4 GATE CHECK ==="
test -f .claude/hooks.yaml && echo "hooks.yaml: EXISTS" || echo "hooks.yaml: MISSING"
/tmp/rulez/rulez validate --config .claude/hooks.yaml && echo "VALIDATION: PASS" || echo "VALIDATION: FAIL"
```
