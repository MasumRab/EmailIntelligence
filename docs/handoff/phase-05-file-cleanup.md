# Phase 5: Tier 2 Root Context Files

**Purpose:** Restore or explicitly account for tool-specific root context files that cannot be treated as dead duplicates.
**Steps:** 6
**Dependencies:** Phase 3 complete

---

## Phase Policy

`.ruler/AGENTS.md` is Tier 1 shared content. The files below are Tier 2 tool-specific root context files and must be handled explicitly:

- `GEMINI.md` — keep at root; split out the Jules template
- `QWEN.md` — keep at root; preserve scientific docs separately before replacing content
- `IFLOW.md` — branch-specific; restore if iFlow is used, otherwise mark `not_on_branch`
- `CRUSH.md` — branch-specific; restore only if Crush is used, otherwise mark `not_on_branch`
- `LLXPRT.md` — branch-specific; restore only if LLxPRT is used, otherwise mark `not_on_branch`

Do NOT silently collapse Tier 2 files into `AGENTS.md` without updating this phase and `.github/instructions/tools-manifest.json`.

---

## Step 5.1 — Split GEMINI.md, keep root Tier 2 file

**Issue:** `GEMINI.md` contains Jules backlog template content in lines 1-185 and Gemini CLI instructions in lines 186+.
**Action:** Extract the Jules template, but keep `GEMINI.md` at project root.

**Create:** `.gemini/JULES_TEMPLATE.md` (lines 1-185)
**Keep:** `GEMINI.md` (Gemini CLI instructions only)

```bash
mkdir -p .gemini
head -185 GEMINI.md > .gemini/JULES_TEMPLATE.md
tail -n +186 GEMINI.md > GEMINI.md.tmp && mv GEMINI.md.tmp GEMINI.md
```

**Why:** Gemini CLI auto-loads `GEMINI.md` from project root. Removing it loses Gemini-specific context.

---

## Step 5.2 — Preserve QWEN scientific docs, keep QWEN Tier 2 at root

**Issue:** `QWEN.md` currently contains scientific/session-manager material, not Qwen-specific agent instructions.
**Action:** Preserve the current content, then replace `QWEN.md` with Tier 2 Qwen instructions. Do NOT move `QWEN.md` out of root.

```bash
cp QWEN.md docs/SCIENTIFIC_BRANCH_DOCS.md
# Then overwrite QWEN.md with the reviewed Tier 2 Qwen instructions.
```

**Why:** `.taskmaster/.qwen/session_manager.py` and the prior tool hierarchy expect `QWEN.md` to remain at root.

---

## Step 5.3 — Restore IFLOW.md if iFlow is active on this branch

**Issue:** `IFLOW.md` is missing on the current branch, but the gap analysis identifies unique iFlow workflow content worth preserving.
**Action:**

1. If iFlow is actively used on this branch, restore `IFLOW.md` at root.
2. Best source: `~/github/EmailIntelligenceGem/IFLOW.md`.
3. Fallback: reconstruct from `docs/handoff/content-archive/ARCHIVED_IFLOW_WORKFLOW.md` and `docs/handoff/content-archive/ARCHIVED_AI_MODELS_SETUP.md`.
4. If iFlow is NOT used on this branch, do not delete references blindly; set the manifest status to `not_on_branch` in Phase 6.6.

---

## Step 5.4 — Decide CRUSH.md and LLXPRT.md branch policy explicitly

**Issue:** `CRUSH.md` and `LLXPRT.md` are branch-specific Tier 2 files. Their content is mostly duplicated by `AGENTS.md`, but their absence should be an explicit branch policy decision, not an accidental omission.

**Action:**

1. If Crush is used on this branch, restore `CRUSH.md` from `~/github/EmailIntelligenceGem/CRUSH.md`.
2. If LLxPRT is used on this branch, restore `LLXPRT.md` from `~/github/EmailIntelligenceGem/LLXPRT.md`.
3. If either tool is NOT used on this branch, leave the file absent and set the corresponding manifest status to `not_on_branch` in Phase 6.6.

**Note:** Because these files are gitignored, restoration requires intentional staging with `git add -f <file>` if they are committed.

---

## Step 5.5 — Verify Tier 2 root file policy

```bash
echo "=== PHASE 5 ROOT CONTEXT CHECK ==="
echo -n "GEMINI.md at root: "; test -f GEMINI.md && echo "EXISTS" || echo "MISSING"
echo -n "Jules template extracted: "; test -f .gemini/JULES_TEMPLATE.md && echo "EXTRACTED" || echo "MISSING"
echo -n "QWEN scientific docs preserved: "; test -f docs/SCIENTIFIC_BRANCH_DOCS.md && echo "PRESERVED" || echo "MISSING"
echo -n "QWEN.md at root: "; test -f QWEN.md && echo "EXISTS" || echo "MISSING"
```

---

## Step 5.6 — Final verification and manifest alignment

```bash
echo "=== PHASE 5 GATE CHECK ==="
echo -n "GEMINI.md lines: "; wc -l < GEMINI.md
echo -n "Jules refs in GEMINI.md: "; grep -c "Jules" GEMINI.md || echo "0"
python3 - <<'PY'
import json, os
data = json.load(open('.github/instructions/tools-manifest.json'))
instructions = {item['id']: item for item in data['instructions']}
for path, item_id in [
    ('IFLOW.md', 'model_context_iflow'),
    ('CRUSH.md', 'model_context_crush'),
    ('LLXPRT.md', 'model_context_llxprt'),
]:
    status = instructions.get(item_id, {}).get('status')
    if os.path.isfile(path):
        print(f'{path}: RESTORED')
    elif status == 'not_on_branch':
        print(f'{path}: NOT_ON_BRANCH')
    else:
        print(f'{path}: FAIL (missing without not_on_branch status)')
PY
```

---

## Notes

- `AGENTS.md` remains the shared Tier 1 foundation.
- `GEMINI.md`, `QWEN.md`, `IFLOW.md`, `CRUSH.md`, and `LLXPRT.md` are Tier 2 files with tool-specific or branch-specific responsibility.
- Phase 6.6 must reconcile `.github/instructions/tools-manifest.json` with whatever policy this phase applies.
- After completing this phase, run `bash scripts/verify-agent-content.sh` to confirm agent file claims match live branch state.
- If `.ruler/AGENTS.md` was updated, run `ruler apply` to redistribute, then re-run the verification script.
