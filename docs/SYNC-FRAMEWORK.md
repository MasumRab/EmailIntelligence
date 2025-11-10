# Sync Framework Review & Updated Options

## Current Sync Framework Overview

### How It Works Today

```
┌─────────────────────────────────────────────────────────────┐
│                    CURRENT ARCHITECTURE                     │
└─────────────────────────────────────────────────────────────┘

orchestration-tools branch (Source of Truth)
    ↓
    Git Hooks (Local)
    ├─ post-checkout: Sync when switching branches
    ├─ post-merge: Sync when pulling/merging
    ├─ post-push: Detect changes, warn developer
    ├─ post-commit: Prompt if on orchestration-tools
    └─ pre-commit: Validation
    ↓
    All other branches (auto-sync setup files)
```

### Current Hooks Flow

**post-checkout hook:**
```bash
Developer: git checkout feature/auth
    ↓
Hook detects branch != orchestration-tools
    ↓
Syncs: setup/, deployment/, scripts/lib/, configs
    ↓
Result: feature/auth has latest orchestration files
```

**post-merge hook:**
```bash
Developer: git pull origin main
    ↓
Merge happens
    ↓
post-merge triggers
    ↓
Syncs orchestration files from orchestration-tools
    ↓
Result: Merged files + latest setup/deployment
```

**post-push hook:**
```bash
Developer: git push origin feature/auth (with setup changes)
    ↓
Hook checks: orchestration files changed?
    ↓
YES → print warning + attempt draft PR creation
NO → just exit
```

### Current Strengths

✓ **Automatic propagation** - Setup files stay in sync without developer action  
✓ **Simple for app developers** - No special workflow needed  
✓ **Local validation** - Hooks run before push  
✓ **Recursive prevention** - Avoids infinite loops  
✓ **Worktree aware** - Different behavior for subtree vs worktree setups  

### Current Weaknesses

✗ **No remote validation** - Changes go to remote before detection  
✗ **Can be bypassed** - `DISABLE_ORCHESTRATION_CHECKS=1` skips hooks  
✗ **Silent failures** - If gh CLI unavailable, no PR created  
✗ **Post-push only** - Detection happens after push  
✗ **No extraction** - Orchestration changes stay mixed with app code  
✗ **Manual workflow** - Developers must use reverse_sync script  

---

## New Framework with Single `orchestration-tools-changes` Branch

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│               NEW SIMPLIFIED ARCHITECTURE                   │
└─────────────────────────────────────────────────────────────┘

Feature Branch (any branch except orchestration-tools)
    ↓
Developer commits both app + setup changes normally
    ↓
git push origin feature/auth
    ↓
GitHub Actions Trigger (on push to non-orchestration-tools)
    │
    ├─ Detects: orchestration files changed?
    │
    ├─ YES:
    │   ├─ Checkout orchestration-tools-changes
    │   ├─ Extract ONLY orchestration files from feature/auth
    │   ├─ Squash into single commit with summary
    │   ├─ Force push to orchestration-tools-changes
    │   ├─ Post comment on PR: "Orchestration extracted to..."
    │   └─ Developer reviews when ready
    │
    └─ NO: Exit silently
    
    ↓

orchestration-tools-changes branch (Always latest extraction)
    ├─ Contains only orchestration files
    ├─ Has squashed, summarized commits
    ├─ Ready to review/PR to orchestration-tools
    └─ Replaces post-push hook detection
    
    ↓

Developer/Maintainer: Reviews & decides when to merge
    
    ├─ Option A: Merge to orchestration-tools immediately
    │  └─ All branches sync on next pull/checkout
    │
    └─ Option B: Hold for more testing/batching
       └─ orchestration-tools-changes keeps latest extraction
```

---

## Comparison: Current vs New

| Aspect | Current Framework | New Framework |
|--------|------------------|---|
| **Detection** | Local post-push hook | GitHub Actions (remote) |
| **Extraction** | Manual reverse_sync script | Automatic GitHub Actions |
| **Storage** | Mixed in feature branch | Separate orchestration-tools-changes |
| **Squashing** | Manual (developer) | Automatic |
| **Summary** | None | Auto-generated summary |
| **PR Creation** | Auto-draft (if gh CLI) | Manual (developer decides) |
| **Can Be Bypassed** | YES (disable hooks) | NO (Actions always run) |
| **Visibility** | Post-push warning | PR comment notification |
| **Branches** | orchestration/* (if using) | Single orchestration-tools-changes |
| **Maintainer Workflow** | Manage multiple orch PRs | Review single branch, cherry-pick PRs |

---

## Updated Options for Single-Branch Approach

### Option 1: GitHub Actions Only (Recommended)

**What happens:**
```
Feature branch pushed with setup changes
    ↓
GitHub Actions extracts to orchestration-tools-changes (force push)
    ↓
Comment on PR: "Orchestration changes extracted to orchestration-tools-changes"
    ↓
When ready: Developer/Maintainer creates PR to orchestration-tools
    ↓
Merge → orchestration-tools updated
    ↓
All branches sync on next pull/checkout
```

**Files affected:**
- Create: `.github/workflows/extract-orchestration-changes.yml`
- Keep: `scripts/extract-orchestration-changes.sh` (backup)
- Modify: Post-push hook can be simplified/removed

**Workflow YAML:**
```yaml
name: Extract Orchestration Changes
on:
  push:
    branches-ignore:
      - orchestration-tools
      - orchestration-tools-changes
    paths:
      - 'setup/**'
      - 'deployment/**'
      - 'scripts/lib/**'
      - '.flake8'
      - 'pyproject.toml'
      # ... all orchestration patterns

jobs:
  extract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract & Push
        run: |
          # Extract logic here
          # Force push to orchestration-tools-changes
      
      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({...})
```

**Pros:**
- ✓ Fully automatic
- ✓ Can't be bypassed
- ✓ Runs consistently
- ✓ No developer action needed

**Cons:**
- ✗ GitHub Actions maintenance
- ✗ Force push complexity
- ✗ Credential handling for push

---

### Option 2: GitHub Actions + Auto-Create Draft PR

**What happens:**
```
Feature branch pushed with setup changes
    ↓
GitHub Actions extracts & creates draft PR to orchestration-tools
    ↓
Comment: "Draft PR created: #123 → orchestration-tools"
    ↓
Developer/Maintainer reviews draft PR directly
    ↓
Approve & merge → all branches sync
```

**Pros:**
- ✓ Even more automated
- ✓ Direct path to merge
- ✓ Automatic review process

**Cons:**
- ✗ Many draft PRs accumulate
- ✗ Noise in PR list
- ✗ Force push + PR creation more complex
- ✗ Draft might become stale

**Not recommended** - adds complexity without clear benefit.

---

### Option 3: Local Script + GitHub Actions Validation

**What happens:**
```
Developer can manually extract locally:
    ./scripts/extract-orchestration-changes.sh feature/auth
    ↓
GitHub Actions ALSO extracts automatically
    ↓
If both try: GitHub Actions overwrites (latest wins)
    ↓
Result: Dual system, Actions is fallback + enforcer
```

**Pros:**
- ✓ Local control when needed
- ✓ GitHub Actions as safety net
- ✓ Flexibility

**Cons:**
- ✗ Confusing with two extraction methods
- ✗ Potential conflicts/overwrites
- ✗ Not simpler

**Not recommended** - adds confusion.

---

## Recommended: Option 1 (GitHub Actions Only)

### Implementation Steps

1. **Create GitHub Actions workflow**
   - `.github/workflows/extract-orchestration-changes.yml`
   - Triggers on push to any branch except orchestration-tools
   - Checks for orchestration file changes
   - If changed: extract → squash → force push to orchestration-tools-changes

2. **Keep local script as backup**
   - `scripts/extract-orchestration-changes.sh`
   - For manual extraction if Actions fails
   - For local development/testing

3. **Simplify post-push hook**
   - Can be removed entirely (Actions replaces it)
   - Or keep as additional warning (redundant but safe)

4. **Update post-checkout/post-merge hooks**
   - No changes needed
   - Continue syncing from orchestration-tools

5. **Update documentation**
   - Explain new workflow
   - Point to orchestration-tools-changes
   - Show when/how to PR to orchestration-tools

### Developer Workflow

```
1. Work on feature normally
   git checkout -b feature/auth-improvements
   nano src/auth.py
   nano setup/setup_environment_system.sh
   git commit -m "feat: add MFA support"
   git push origin feature/auth-improvements

2. GitHub Actions automatically extracts
   (no developer action needed)

3. See in PR comments:
   "✅ Orchestration changes extracted to orchestration-tools-changes"

4. When ready to merge orchestration changes:
   git checkout orchestration-tools
   git pull origin orchestration-tools
   git merge --squash orchestration-tools-changes
   git commit -m "chore: merge orchestration changes from feature/auth-improvements"
   git push origin orchestration-tools

5. All branches sync on next pull/checkout
```

### Independent Setup Development (Hooks Disabled)

If you need to work on setup files independently without automatic syncing:

```
1. Disable hooks:
   ./scripts/disable-hooks.sh

2. Modify setup files directly:
   nano setup/setup_environment_system.sh
   git add setup/
   git commit -m "setup: customize setup for this branch"

3. When hooks are disabled:
   - post-checkout WILL NOT sync orchestration-tools files
   - post-merge WILL NOT sync orchestration-tools files
   - orchestration-tools-changes branch will still extract your changes on push
   - This prevents overwriting your customizations

4. Re-enable hooks when done:
   ./scripts/enable-hooks.sh

5. Hooks resume automatic syncing from orchestration-tools on next pull/checkout
```

---

## Implementation Plan

### Phase 1: Setup (This Week)
- [ ] Create GitHub Actions workflow
- [ ] Test on orchestration-tools-changes branch
- [ ] Document workflow

### Phase 2: Validation (Next Week)
- [ ] Test extraction on real feature branches
- [ ] Verify notifications work
- [ ] Ensure no overwrites/conflicts

### Phase 3: Simplification (Later)
- [ ] Remove/simplify post-push hook (if needed)
- [ ] Clean up documentation
- [ ] Train team on new workflow

---

## Migration Path

**For existing development:**

```
If orchestration changes already on branches:
    1. Run local extraction script
       ./scripts/extract-orchestration-changes.sh feature/branch
    
    2. Review extracted changes
       git show orchestration/feature-name
    
    3. Force push to orchestration-tools-changes
       git checkout orchestration/feature-name
       git push -f origin orchestration-tools-changes
    
    4. Actions continue from there
```

---

## Questions to Answer

Before implementing Option 1:

1. Should GitHub Actions create the orchestration-tools-changes branch if it doesn't exist?
2. Should we require PR to orchestration-tools be from orchestration-tools-changes specifically?
3. Should we add CI/CD checks BEFORE orchestration-tools-changes is created?
4. Should orchestration-tools-changes be a protected branch?

---

## Related

- Current: `scripts/hooks/post-push`, `post-checkout`, `post-merge`
- New: `.github/workflows/extract-orchestration-changes.yml`
- Backup: `scripts/extract-orchestration-changes.sh`
- Documentation: `docs/ORCHESTRATION.md`
