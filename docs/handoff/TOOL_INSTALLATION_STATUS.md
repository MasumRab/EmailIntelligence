# Tool Installation Status

**Checked:** 2026-04-09

---

## Ruler (intellectronica/ruler)

| Status | Detail |
|--------|--------|
| **Installed** | ✅ YES |
| **Version** | v0.3.38 |
| **Location** | `/home/masum/.local/share/mise/installs/node/22.22.2/bin/ruler` |
| **Config** | `.ruler/ruler.toml` (exists), `.ruler/AGENTS.md` (33 lines) |
| **Commands** | `ruler apply`, `ruler init`, `ruler revert` |
| **Integration** | Phase 3 of handoff |

**Verified:**
```bash
ruler --version  # 0.3.38
ruler apply --project-root . --dry-run  # Works
```

---

## Agent-Rules-Kit (tecnomanu/agent-rules-kit)

| Status | Detail |
|--------|--------|
| **Installed** | ✅ YES (just installed) |
| **Version** | v3.8.1 |
| **Location** | `/home/masum/.local/share/mise/installs/node/22.22.2/bin/agent-rules-kit` |
| **In PATH** | ✅ YES |
| **Mode** | Interactive CLI (use `--auto-install` for non-interactive) |

**CLI Flags Available:**
```bash
agent-rules-kit --stack=react --version=18 --ide=claude --global --auto-install
```

**Known limitation:** No `--version` or `--help` flags (starts interactive mode). Use `--auto-install` to skip prompts.

**Integration:** Documented in Phase 0 (Option B) with full CLI reference

---

## RuleSync

| Status | Detail |
|--------|--------|
| **Installed** | ✅ YES |
| **Version** | v7.27.0 |
| **Location** | `/home/masum/.local/share/mise/installs/npm-rulesync/7.27.0/bin/rulesync` |
| **Config** | `rulesync.jsonc` (exists in project) |
| **Integration** | Phase 2/8 of handoff |

**Verified:**
```bash
rulesync --version  # 7.27.0
rulesync generate --check  # Works
```

---

## Related Tools (in mise)

| Tool | Version | Purpose | Status |
|------|---------|---------|--------|
| `ast-grep` | 0.42.0 | AST-based code search/rewrite | ✅ Installed (pipx) |
| `semgrep` | 1.157.0 | Security analysis, AST patterns | ✅ Installed (pipx) |
| `ck` (ck-search) | 0.7.0 | Semantic code search (CLI: `ck`) | ✅ Installed (npm) |
| `agent-browser` | 0.23.4 | Browser automation for AI agents | ✅ Installed |
| `agent-skills-cli` | 1.1.7 | Skills management | ✅ Installed |
| `pi-coding-agent` | 0.64.0 | Alternative coding agent | ✅ Installed |
| `task-master-ai` | 0.43.1 | Task management | ✅ Installed |

### AST-Based Code Search Tools (Already Installed)

**Prefer these over PAMPA for code search:**

```bash
# ast-grep — AST pattern matching (v0.42.0)
ast-grep run 'if ($COND) { $BODY }' --lang python
ast-grep scan --config sgrep.yml

# semgrep — Security and linting (v1.157.0)
semgrep --config=auto .
semgrep --config p/python

# grep-ast — AST-aware grep
npx grep-ast "function $NAME($PARAMS)" --lang typescript
```

---

## Summary

| Tool | Installed | In PATH | Config Ready | Handoff Phase |
|------|-----------|---------|--------------|---------------|
| **Ruler** | ✅ v0.3.38 | ✅ YES | ✅ `.ruler/ruler.toml` | Phase 3 |
| **Agent-Rules-Kit** | ✅ v3.8.1 | ✅ YES | N/A (content generator) | Phase 0 Option B |
| **RuleSync** | ✅ v7.27.0 | ✅ YES | ✅ `rulesync.jsonc` | Phase 2/8 |
| **Agent RuleZ** | ✅ v2.3.0 | ✅ YES | ⬜ Pending | Phase 4 |
| **ast-grep** | ✅ v0.42.0 | ✅ YES | N/A | AST search |
| **semgrep** | ✅ v1.157.0 | ✅ YES | N/A | Security analysis |
| **ck** (ck-search) | ✅ v0.7.0 | ✅ YES | N/A | Semantic search |

---

## No Further Action Required

All three tools are now **properly integrated and preinstalled**:

1. **Ruler** — Apply with `ruler apply --project-root .`
2. **Agent-Rules-Kit** — Run with `agent-rules-kit --stack=... --auto-install`
3. **RuleSync** — Check with `rulesync generate --check`

---

## Using Agent-Rules-Kit (Example)

```bash
# Generate React rules for Claude
agent-rules-kit --stack=react --version=18 --ide=claude --global --auto-install

# Copy to Ruler source
cat CLAUDE.md >> .ruler/AGENTS.md && rm CLAUDE.md

# Apply Ruler
ruler apply --project-root .
```
