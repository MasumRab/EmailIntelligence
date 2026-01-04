# Orchestration Disable/Enable - Quick Reference

## One-Line Commands

### Disable Everything (with branch sync)
```bash
./scripts/disable-all-orchestration-with-branch-sync.sh
```

### Re-enable Everything (with branch sync)
```bash
./scripts/enable-all-orchestration-with-branch-sync.sh
```

### Disable Without Pushing
```bash
./scripts/disable-all-orchestration-with-branch-sync.sh --skip-push
```

### Re-enable Without Pushing
```bash
./scripts/enable-all-orchestration-with-branch-sync.sh --skip-push
```

---

## What These Scripts Do

### Disable
- ✅ Disables all git hooks
- ✅ Sets `ORCHESTRATION_DISABLED=true`
- ✅ Updates branch profiles (main.json, scientific.json, orchestration-tools.json)
- ✅ Creates `.orchestration-disabled` marker
- ✅ Pushes changes to scientific and main branches

### Enable
- ✅ Restores all git hooks
- ✅ Clears `ORCHESTRATION_DISABLED` from env files
- ✅ Updates branch profiles back to enabled state
- ✅ Removes `.orchestration-disabled` marker
- ✅ Pushes changes to scientific and main branches

---

## Verify Status

```bash
# Check if disabled
cat .env.local | grep ORCHESTRATION_DISABLED
ls -la .orchestration-disabled

# Check if hooks are disabled
ls .git/hooks/*.disabled

# Check profile status
cat .context-control/profiles/main.json | grep orchestration_disabled
```

---

## When to Use

**Disable when:**
- Working independently without orchestration interference
- Testing without automatic workflows
- Debugging scripts
- Working offline
- Local feature development

**Re-enable when:**
- Pushing to shared branches
- Collaborating with others
- Final testing before merge
- Normal development resumption

---

## Options

- `--skip-push` - Don't automatically push to branches (use for manual review)

---

## Branches Affected

Changes automatically pushed to:
1. Current branch
2. `scientific` branch
3. `main` branch

---

## Key Files Modified

- `.env.local` - ORCHESTRATION_DISABLED variable
- `.orchestration-disabled` - Marker file
- `.context-control/profiles/*.json` - Branch profiles
- `.git/hooks/*` - Git hooks (disabled/restored)

---

## Recovery

If something goes wrong:

```bash
# Restore from git
git checkout HEAD -- .env.local
git checkout HEAD -- .context-control/profiles/

# Manually restore hooks
git checkout HEAD -- .git/hooks/
chmod +x .git/hooks/*

# Remove marker
rm -f .orchestration-disabled
```

---

## Related Commands

```bash
# Just disable hooks (no branch sync)
./scripts/disable-orchestration-hooks.sh

# Just restore hooks
./scripts/restore-orchestration-hooks.sh

# Original disable (no branch sync)
./scripts/disable-all-orchestration.sh

# Original enable (no branch sync)
./scripts/enable-all-orchestration.sh
```

---

See `ORCHESTRATION_DISABLE_BRANCH_SYNC.md` for complete documentation.
