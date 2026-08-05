# Branch Agent Guidelines Summary

**Status:** Superseded · **Last updated:** 2026-08-05
**Replaced by:** [`.github/BRANCH_PROTECTION_RULES.md`](.github/BRANCH_PROTECTION_RULES.md)

This file has been consolidated into `.github/BRANCH_PROTECTION_RULES.md` which covers:
- Forbidden operations (hard guard)
- Sanctioned transfer patterns (T1–T5)
- Branch charters
- Agent quick-reference

**Canonical source:** `.taskmaster/BRANCH_MANAGEMENT_MODEL.md`

---

## Legacy Content (for reference only — do not act on)

### Previous Branch Classifications (OUTDATED)
- **main**: Core application development and production stability
- **scientific**: FastAPI backend, email processing, AI analysis, and API routes
- **feature branches**: Development of specific features

**Note:** These classifications are incomplete. The full model is in `.taskmaster/BRANCH_MANAGEMENT_MODEL.md`.

### Previous Sync Procedures (OUTDATED)
- `scripts/sync_config_analysis.sh --quick` — check branch status
- `scripts/standardize_branch_config.sh --check` — standardize configs

**Note:** Use the sync scripts documented in `.taskmaster/BRANCH_MANAGEMENT_MODEL.md` (§4 Transfer Patterns).

### Previous Anti-Patterns (PARTIALLY OUTDATED)
- Never commit `.mcp.json` with real API keys ✅ Still valid
- Never hard-code secrets ✅ Still valid
- Never use `eval()` or `exec()` ✅ Still valid
- Missing: merge prevention rules, transfer patterns, branch charters → see `.github/BRANCH_PROTECTION_RULES.md`
