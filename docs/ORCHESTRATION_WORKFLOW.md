# Orchestration Workflow: Centralized on orchestration-tools

**Effective Date:** 2025-11-10
**Previous Model:** Distributed (main branch sync)
**New Model:** Centralized (orchestration-tools as single source of truth)

---

## Architecture Change

### Before (Contaminated Model)
```
main (app code + orchestration files)
  ↓ sync ↓
orchestration-tools (app code + orchestration files)
  ↓ sync ↓
feature branches (app code + orchestration files)

❌ Problem: Main is central point, contamination spreads
```

### After (Centralized Model)
```
orchestration-tools (ONLY: setup/, deployment/, config/, scripts/hooks/)
  ↓ one-way sync ↓
  ├─ main (app code only: src/, client/, plugins/)
  ├─ scientific (app code only)
  ├─ feature/* (app code + local orchestration changes)
  └─ other branches

✓ Clean: orchestration-tools is exclusive source of truth
```

---

## Key Changes

### 1. GitHub Workflows (Updated)

**extract-orchestration-changes.yml**
- Line 58: Changed comparison from `origin/main` → `origin/orchestration-tools`
- Line 78: Changed base branch from `main` → `orchestration-tools`
- PR comments: Updated to reference orchestration-tools as source of truth

**Rationale:**
- Orchestration changes now extracted against orchestration-tools baseline
- Prevents main branch contamination
- orchestration-tools-changes → orchestration-tools → other branches (unidirectional)

### 2. Branch Hierarchy (Established)

| Branch | Purpose | Can modify orchestration files? |
|--------|---------|--------------------------------|
| orchestration-tools | Central source of truth | ✓ YES (authoritative) |
| orchestration-tools-changes | Aggregates agent pushes | ✓ YES (staging) |
| main | Application code | ✗ NO (read-only for orchestration) |
| feature/* | Feature development | ✓ YES (with intent marker) |
| scientific | Scientific branch | ✗ NO (read-only) |

### 3. Sync Direction (One-Way)

```
orchestration-tools (authoritative)
    ↓ sync only
all other branches
```

- **orchestration-tools → main:** Sync on demand via PR
- **orchestration-tools → feature branches:** Sync on demand via cherry-pick
- **main → orchestration-tools:** ✗ BLOCKED (pre-merge-abort hook)
- **feature → orchestration-tools:** Promotion via orchestration-tools-changes branch

---

## Workflow: Updating Orchestration Files

### Developer on Feature Branch
1. Make orchestration changes locally (setup/, deployment/, etc.)
2. Mark as intentional: `scripts/orchestration-intent.sh mark file.sh`
3. Push to feature branch: `git push origin feature-name`

### Agent/Automation
1. Detect orchestration changes
2. Extract to orchestration-tools-changes (GitHub Actions)
3. Debounce aggregates multiple pushes (5-second wait)
4. Single PR created: orchestration-tools-changes → orchestration-tools

### Approval
1. Review PR on orchestration-tools
2. Merge when ready (or cherry-pick selective files)
3. All branches can sync from orchestration-tools

### Sync to Other Branches
1. On main: `git pull origin orchestration-tools` (cherry-pick only specific files)
2. On feature: `git merge orchestration-tools` (selective, respecting intent markers)
3. On scientific: Manual review + merge (if compatible)

---

## Pre-Merge Hook: Block Contamination

**File:** `.git/hooks/pre-merge-abort`

Prevents `main → orchestration-tools` merges:
```bash
$ git merge main
fatal: Forbidden merge detected
This would contaminate orchestration-tools
```

**Allowed merges:**
- `orchestration-tools-changes → orchestration-tools` ✓
- Any branch → orchestration-tools (via PR review) ✓
- orchestration-tools → other branches ✓

---

## Validation Tools

### Check Context Purity
```bash
./scripts/validate-orchestration-context.sh
# Exit 0 = clean, 1 = contaminated
```

### Checks Performed
- No src/, client/, plugins/ on orchestration-tools
- No AGENTS.md, CRUSH.md, GEMINI.md, IFLOW.md, LLXPRT.md
- setup/launch.sh has no recursive references
- setup/launch.py exists and is valid

---

## Migration from Old Model

### If You're on main
1. orchestration files ARE present (contamination from 421317c)
2. Ignore them (read-only for orchestration purposes)
3. Use orchestration-tools for authority

### If You're on orchestration-tools
1. Clean state after `git revert 421317c`
2. All orchestration files present and authoritative
3. Sync orchestration-tools updates to other branches as needed

### If You're on feature branch
1. Orchestration files may exist locally (intentional changes)
2. Mark as intentional with scripts/orchestration-intent.sh
3. Agent will extract to orchestration-tools-changes automatically

---

## FAQ

**Q: Can I modify setup/launch.py on main?**
A: Yes, but changes won't be synchronized to orchestration-tools. Make changes on orchestration-tools or feature branch and promote.

**Q: What if I accidentally merge main → orchestration-tools?**
A: pre-merge-abort hook blocks it. If already merged, `git revert` the merge commit.

**Q: How do branches get orchestration updates?**
A: Manually cherry-pick from orchestration-tools, or use: `git merge -X theirs orchestration-tools` (for full merge).

**Q: Can I test orchestration changes on feature branch first?**
A: Yes! Mark with intent marker, test, then promote via orchestration-tools-changes.

---

## Implementation Checklist

- [x] Revert contamination commit 421317c
- [x] Update extract-orchestration-changes.yml (main → orchestration-tools)
- [x] Create pre-merge-abort hook
- [x] Create validate-orchestration-context.sh
- [ ] Activate pre-merge-abort hook in all local repos
- [ ] Document in README / CONTRIBUTING
- [ ] Update branch protection rules on GitHub
- [ ] Train team on new workflow

