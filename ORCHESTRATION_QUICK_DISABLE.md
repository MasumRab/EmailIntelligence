# Quick: Disable Orchestration

## One-Line Disable

```bash
./scripts/disable-all-orchestration.sh
```

This:
- ✅ Sets `ORCHESTRATION_DISABLED=true` in `.env.local`
- ✅ Disables all git hooks (backs them up first)
- ✅ Creates `.orchestration-disabled` marker
- ✅ Adds to `.gitignore`

## One-Line Re-Enable

```bash
./scripts/enable-all-orchestration.sh
```

This:
- ✅ Clears `ORCHESTRATION_DISABLED` from `.env`
- ✅ Restores all git hooks from backup
- ✅ Removes `.orchestration-disabled` marker

---

## Alternative Methods

### Method 1: Environment Variable Only
```bash
export ORCHESTRATION_DISABLED=true
python launch.py run
```

### Method 2: Command-Line Flag (when implemented)
```bash
python launch.py run --disable-orchestration
```

### Method 3: Disable Only Git Hooks
```bash
./scripts/disable-orchestration-hooks.sh
# Work without hooks
./scripts/restore-orchestration-hooks.sh
```

### Method 4: Marker File Only
```bash
touch .orchestration-disabled
# Workflows check this file and skip
rm .orchestration-disabled
```

---

## Verification

Check if disabled:
```bash
cat .env.local | grep ORCHESTRATION_DISABLED
ls -la .orchestration-disabled
ls -la .git/hooks/*.disabled 2>/dev/null | head -3
```

Check if enabled:
```bash
ls -la .git/hooks/post-commit  # Should exist and be executable
grep -v "ORCHESTRATION_DISABLED" .env.local
```

---

## What Gets Disabled

✅ Git hooks:
- pre-commit
- post-commit
- post-merge
- post-checkout
- post-push

✅ Workflows:
- Setup synchronization
- Branch propagation
- File validation
- Conflict detection

❌ Unaffected:
- Git functionality itself
- File operations
- Tests
- Services

---

## For Development

Disable when:
- Working independently on a feature
- Testing without orchestration interference
- Debugging scripts
- Working offline

Re-enable when:
- Pushing to shared branches
- Collaborating with others
- Final testing before merge

---

## If You Get Stuck

**Hooks won't run after disable:**
```bash
./scripts/enable-all-orchestration.sh
```

**Hooks disabled but environment var still set:**
```bash
unset ORCHESTRATION_DISABLED
grep -v ORCHESTRATION_DISABLED .env.local > .env.tmp && mv .env.tmp .env.local
```

**Complete reset:**
```bash
rm -f .orchestration-disabled
rm -f .env.local
./scripts/restore-orchestration-hooks.sh
```

---

See full guide: `ORCHESTRATION_DISABLE_FLAG.md`
