# Orchestration Method Recommendations

## Quick Comparison

### Current Approach: Git Hooks
- **Pros:** Simple, immediate feedback
- **Cons:** Requires setup on every machine, can be disabled, not centralized, hard to enforce
- **Verdict:** ❌ Not suitable for enforcing organizational standards

### Recommended Approach: GitHub Actions + Branch Protection

A multi-layered approach using GitHub's native features:

```
Layer 1: Prevention
├─ Branch Protection Rules (prevent bad merges)
└─ CODEOWNERS (require reviews)
                    ↓
Layer 2: Detection  
├─ Validation Workflow (every push)
└─ PR Status Checks (block invalid merges)
                    ↓
Layer 3: Resolution
├─ Automated Sync PRs (feature branch → orch-tools)
└─ Post-merge Propagation (orch-tools → other branches)
                    ↓
Layer 4: Reconciliation
└─ Scheduled Drift Detection (weekly audit)
```

---

## Why GitHub Actions Over Hooks?

| Aspect | Hooks | GitHub Actions |
|--------|-------|---|
| **Enforcement** | Developers can skip | Server-side, mandatory |
| **Visibility** | Silent, hidden | Visible in PR checks |
| **Reliability** | Varies by setup | 100% consistent |
| **Maintenance** | Distributed | Centralized |
| **Scale** | Hard at 10+ devs | Works for any size |
| **Debugging** | Local only | Visible logs in GitHub |
| **Cost** | Free (setup overhead) | Free (included quota) |

---

## Recommended Implementation

### Phase 1: Validation (Blocks bad state)
**Goal:** Prevent invalid agent file changes from being merged

```yaml
# .github/workflows/validate-agent-files.yml
- Runs on: every push, every PR
- Checks: File existence, format, required sections
- Blocks: Merges if validation fails
- Effort: 2-3 hours
```

**Benefits:**
- Immediate developer feedback
- Prevents broken state in any branch
- No PRs needed (just validation)

### Phase 2: Branch Protection (Enforces process)
**Goal:** Require review and approval for agent file changes

```
Branch Protection Rule:
├─ Require PR reviews (from CODEOWNERS)
├─ Require status checks pass (validation above)
├─ Dismiss stale reviews
└─ Require branches up to date before merge

CODEOWNERS:
├─ AGENTS.md → @orchestration-team
├─ AGENT.md → @orchestration-team
├─ All other agent files → @orchestration-team
```

**Benefits:**
- No enforcement setup needed on developer machines
- GitHub-native enforcement
- Visible to all team members

### Phase 3: Automated Sync (Reduces manual work)
**Goal:** Auto-create PRs when agent files change on feature branches

```yaml
# .github/workflows/sync-agent-files.yml
- Triggers: On push of agent files to non-orch-tools branches
- Action: Create PR to orchestration-tools
- Format: Clear, standardized PR with changeset
- Effort: 3-4 hours
```

**Benefits:**
- No developer needs to remember to create PR
- Standardized format
- Clear audit trail

### Phase 4: Post-merge Propagation (Completes the loop)
**Goal:** Automatically sync approved changes from orchestration-tools to other branches

```yaml
# .github/workflows/propagate-agent-files.yml
- Triggers: On successful merge to orchestration-tools
- Action: Create PRs to main, scientific (or auto-merge if approved)
- Format: Clear change notes
- Effort: 2-3 hours
```

**Benefits:**
- Changes propagate automatically
- All branches stay synchronized
- No manual sync needed

### Phase 5: Reconciliation (Catches drift)
**Goal:** Weekly audit to catch any out-of-sync state

```yaml
# .github/workflows/reconcile-agent-files.yml
- Triggers: Weekly (Monday 9 AM)
- Action: Compare all branches, report drift
- Result: Issue notification or auto-fix PR
- Effort: 2 hours
```

**Benefits:**
- Catches problems missed by other checks
- Early warning system
- Can be scheduled during low-activity times

---

## Implementation Timeline

```
Week 1-2: Validation + Branch Protection (MVP)
├─ Validate workflow (2-3h)
├─ CODEOWNERS + Protection rules (1h)
└─ Test on feature branch (1h)
└─ Status: Can prevent bad merges

Week 3-4: Automated Sync (Full automation)
├─ Sync workflow creation (3-4h)
├─ Post-merge propagation (2-3h)
└─ Integration testing (2h)
└─ Status: Fully automated pipeline

Week 5: Reconciliation + Cleanup (Robustness)
├─ Scheduled reconciliation (2h)
├─ Update documentation (2h)
├─ Remove git hook documentation (1h)
└─ Status: Production-ready, fully automated
```

---

## What Gets Removed/Updated

### Remove from AGENTS.md
```
❌ "Disabling Hooks" section (git hooks)
❌ "Pre-commit hook warns..." language
❌ Any references to local hook setup
```

### Add to AGENTS.md
```
✅ "GitHub Actions Enforcement" section
✅ "CODEOWNERS requirement" for agent files
✅ "PR requirements" when modifying agent files
✅ "Automated sync expectations"
```

### New Files Created
```
✅ .github/CODEOWNERS (defines who reviews agent files)
✅ .github/workflows/validate-agent-files.yml
✅ .github/workflows/sync-agent-files.yml (optional)
✅ .github/workflows/propagate-agent-files.yml (optional)
✅ .github/workflows/reconcile-agent-files.yml (optional)
```

### Git Hooks Archived (not deleted)
```
📦 scripts/hooks/ → rename to scripts/hooks.archived/
   (Keep for reference, document as deprecated)
```

---

## Cost-Benefit Analysis

### GitHub Actions
- **Cost:** Free (included in all plans, 3000 minutes/month free for private repos)
- **Setup:** One-time 10-15 hours of work
- **Maintenance:** ~1 hour/month for monitoring
- **ROI:** High - catches issues automatically for all developers

### Git Hooks
- **Cost:** Free (but hidden developer setup time)
- **Setup:** Each developer configures locally
- **Maintenance:** Nightmare - inconsistent across machines
- **ROI:** Low - easily bypassed, not enforced

---

## Decision Matrix

**Choose GitHub Actions if:**
- ✅ Want server-side enforcement (can't be disabled)
- ✅ Want visibility and audit trails
- ✅ Want consistency across all developers
- ✅ Team size > 5 people
- ✅ Care about operational reliability

**Choose Git Hooks if:**
- ✅ Solo development
- ✅ Trust team to follow process
- ✅ Low ceremony, maximum flexibility
- ✅ Minimal DevOps/CI resources

**For EmailIntelligence:** Use GitHub Actions

---

## Next Steps

1. **Review:** Agree on validation + branch protection as MVP
2. **Implement:** Create validation workflow (1 day)
3. **Test:** Run on feature branch (1 day)
4. **Deploy:** Enable branch protection (1 day)
5. **Iterate:** Add sync workflows in Phase 2

This gives you enforcement in 3 days without complex automation.
