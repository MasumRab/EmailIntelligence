# Phase 9: Multi-Loop Verification

**Purpose:** Verify all fixes across 9 verification loops.
**Steps:** 9
**Dependencies:** All implementation phases complete

---

## Loop 1: File Existence & Size

```bash
echo "=== LOOP 1: FILE EXISTENCE ==="
for f in AGENTS.md CLAUDE.md AGENT.md .ruler/AGENTS.md .ruler/ruler.toml .claude/hooks.yaml rulesync.jsonc; do
  echo -n "$f: "
  test -f "$f" && echo "EXISTS ($(wc -c < "$f") bytes)" || echo "MISSING"
done
for d in .roo .cursor .windsurf .trae .kiro .kilo .claude; do
  echo -n "$d/mcp.json: "
  test -s "$d/mcp.json" && echo "OK" || echo "EMPTY/MISSING"
done
for f in GEMINI.md QWEN.md .gemini/JULES_TEMPLATE.md docs/SCIENTIFIC_BRANCH_DOCS.md; do
  echo -n "$f: "
  test -f "$f" && echo "EXISTS" || echo "MISSING"
done
python3 - <<'PY'
import json, os
d = json.load(open('.github/instructions/tools-manifest.json'))
m = {i['id']: i for i in d['instructions']}
for path, key in [('IFLOW.md', 'model_context_iflow'), ('CRUSH.md', 'model_context_crush'), ('LLXPRT.md', 'model_context_llxprt')]:
    status = m.get(key, {}).get('status')
    if os.path.isfile(path):
        print(f'{path}: RESTORED')
    else:
        print(f'{path}: {status or "UNSET"}')
PY
```

---

## Loop 2: Content Correctness

```bash
echo "=== LOOP 2: CONTENT CORRECTNESS ==="
echo -n "Conflict markers: "
grep -c '<<<<<<\|======\|>>>>>>' CLAUDE.md 2>/dev/null || echo "0"
echo -n "Prisma refs: "
grep -rl "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ .kilo/rules/ 2>/dev/null | wc -l
echo -n "TypeScript-only: "
grep -rl "Use TypeScript for all new code" .cursor/rules/ .clinerules/ .github/ 2>/dev/null | wc -l
echo -n "cerebras-mcp: "
grep -rl "cerebras-mcp" .clinerules/ .cursor/rules/ 2>/dev/null | wc -l
echo -n "windsurf,windsurf: "
grep -c "windsurf,windsurf" .windsurf/rules/dev_workflow.md 2>/dev/null || echo "0"
echo -n "Placeholder keys: "
grep -rl "YOUR_.*_HERE" .windsurf/mcp.json .kilo/mcp.json 2>/dev/null | wc -l
```

---

## Loop 3: MCP Config Consistency

```bash
echo "=== LOOP 3: MCP CONSISTENCY ==="
canonical=$(python3 -c "import json; d=json.load(open('.mcp.json')); print(d['mcpServers']['task-master-ai']['command'])")
for f in .roo/mcp.json .cursor/mcp.json .claude/mcp.json .windsurf/mcp.json .trae/mcp.json .kilo/mcp.json; do
  cmd=$(python3 -c "import json; d=json.load(open('$f')); print(d['mcpServers']['task-master-ai']['command'])" 2>/dev/null)
  echo -n "$f command: "
  [ "$cmd" = "$canonical" ] && echo "MATCH" || echo "MISMATCH ($cmd)"
done
```

---

## Loop 4: Ruler Distribution

```bash
echo "=== LOOP 4: RULER DISTRIBUTION ==="
ruler apply --project-root . --dry-run 2>&1 | grep -c "Applying" || echo "0"
```

---

## Loop 5: RuleSync Targets

```bash
echo "=== LOOP 5: RULESYNC TARGETS ==="
python3 -c "import json; d=json.load(open('rulesync.jsonc')); print('Targets:', len(d.get('targets', [])))"
```

---

## Loop 6: Ruler dry-run

```bash
echo "=== LOOP 6: RULER DRY-RUN ==="
ruler apply --project-root . --dry-run 2>&1 | head -10
```

---

## Loop 7: RuleSync --check CI

```bash
echo "=== LOOP 7: RULESYNC CHECK ==="
rulesync generate --check 2>&1
```

---

## Loop 8: Agent RuleZ debug scenarios

```bash
echo "=== LOOP 8: AGENT RULEZ DEBUG ==="
/tmp/rulez/rulez debug --config .claude/hooks.yaml --event "Bash:git push --force origin main"
/tmp/rulez/rulez debug --config .claude/hooks.yaml --event "Bash:git commit -m 'test'"
```

---

## Loop 9: Agent Content Accuracy

```bash
echo "=== LOOP 9: AGENT CONTENT VERIFICATION ==="
bash scripts/verify-agent-content.sh
```

**PASS:** `Claimed & Stale: 0` and `Undocumented: 0`
**If stale:** Update `.ruler/AGENTS.md` with accurate directory descriptions, run `ruler apply`, re-run this loop.

---

## Final Gate

```bash
echo "=== FINAL GATE ==="
echo "All loops (1–9) must pass. Review output above."
```
