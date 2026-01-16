# Orchestration Documentation Index

Complete guide to all orchestration-related documentation and scripts.

---

## Quick Navigation

### 🚀 Just Want to Disable/Enable?
→ **[ORCHESTRATION_DISABLE_QUICK_REFERENCE.md](ORCHESTRATION_DISABLE_QUICK_REFERENCE.md)**

### 📚 Want Full Details?
→ **[ORCHESTRATION_DISABLE_BRANCH_SYNC.md](ORCHESTRATION_DISABLE_BRANCH_SYNC.md)**

### 🔧 Need Command Reference?
→ **[AGENTS.md](AGENTS.md)** (Orchestration Control Commands section)

---

## All Documentation Files

### Primary Documents (New)

| Document | Purpose | For Whom | Read Time |
|----------|---------|----------|-----------|
| **ORCHESTRATION_DISABLE_QUICK_REFERENCE.md** | Quick command reference | Everyone | 2 min |
| **ORCHESTRATION_DISABLE_BRANCH_SYNC.md** | Complete technical guide | Developers, Ops | 10 min |
| **ORCHESTRATION_IMPLEMENTATION_SUMMARY.md** | Implementation record | Team leads | 5 min |
| **ORCHESTRATION_DOCS_INDEX.md** | This index | Everyone | 3 min |

### Supporting Documents (Existing)

| Document | Purpose | Status |
|----------|---------|--------|
| **ORCHESTRATION_DISABLE_FLAG.md** | Original disable flag implementation guide | Reference |
| **ORCHESTRATION_CONTROL_MODULE.md** | Centralized control module architecture | Reference |
| **ORCHESTRATION_QUICK_DISABLE.md** | Original quick disable reference | Reference |
| **ORCHESTRATION_PROCESS_GUIDE.md** | Complete process workflow | Reference |
| **ORCHESTRATION_TEST_SUITE.md** | Testing documentation | Reference |

---

## Scripts

### Disable/Enable with Branch Sync (NEW)

```bash
# Disable everything with automatic branch sync and push
./scripts/disable-all-orchestration-with-branch-sync.sh

# Re-enable everything with automatic branch sync and push
./scripts/enable-all-orchestration-with-branch-sync.sh

# Same but without automatic push
./scripts/disable-all-orchestration-with-branch-sync.sh --skip-push
./scripts/enable-all-orchestration-with-branch-sync.sh --skip-push
```

**What they do:**
- ✅ Disable/restore git hooks
- ✅ Set/clear ORCHESTRATION_DISABLED environment variable
- ✅ Update branch profiles (.context-control/profiles/*.json)
- ✅ Create/remove .orchestration-disabled marker
- ✅ Commit and push changes to scientific and main branches

### Original Disable/Enable Scripts (Still Available)

```bash
# Original: Disable hooks and env var only (no branch sync)
./scripts/disable-all-orchestration.sh
./scripts/enable-all-orchestration.sh

# Hook-only control
./scripts/disable-orchestration-hooks.sh
./scripts/restore-orchestration-hooks.sh
```

---

## Recommended Reading Order

### For First-Time Users
1. Read: `ORCHESTRATION_DISABLE_QUICK_REFERENCE.md` (2 min)
2. Review: One-line commands in AGENTS.md (1 min)
3. Do: Run `./scripts/disable-all-orchestration-with-branch-sync.sh` (1 min)

### For Administrators
1. Read: `ORCHESTRATION_DISABLE_QUICK_REFERENCE.md` (2 min)
2. Read: `ORCHESTRATION_DISABLE_BRANCH_SYNC.md` (10 min)
3. Read: `ORCHESTRATION_IMPLEMENTATION_SUMMARY.md` (5 min)
4. Reference: `ORCHESTRATION_CONTROL_MODULE.md` as needed

### For Integration with Other Systems
1. Read: `ORCHESTRATION_CONTROL_MODULE.md` (centralized control)
2. Read: `ORCHESTRATION_DISABLE_BRANCH_SYNC.md` sections on integration
3. Reference: Existing orchestration guides as needed

---

## Quick Reference

### Disable Orchestration
```bash
./scripts/disable-all-orchestration-with-branch-sync.sh
```
- Sets ORCHESTRATION_DISABLED=true
- Disables all hooks
- Updates branch profiles
- Pushes to scientific and main

### Re-enable Orchestration
```bash
./scripts/enable-all-orchestration-with-branch-sync.sh
```
- Clears ORCHESTRATION_DISABLED
- Restores all hooks
- Updates branch profiles
- Pushes to scientific and main

### Verify Status
```bash
# Check if disabled
cat .env.local | grep ORCHESTRATION_DISABLED
ls -la .orchestration-disabled
ls .git/hooks/*.disabled

# Check profile status
cat .context-control/profiles/main.json | grep orchestration_disabled
```

---

## What Each Script Does

### disable-all-orchestration-with-branch-sync.sh

**Step 1:** Set environment variable
- Sets ORCHESTRATION_DISABLED=true in .env and .env.local
- Makes environment variable available immediately

**Step 2:** Disable git hooks
- Moves hooks from .git/hooks/* to .git/hooks/*.disabled
- Backs up originals to .git/hooks.backup-<timestamp>/

**Step 3:** Create marker file
- Creates .orchestration-disabled marker
- Adds to .gitignore to prevent tracking

**Step 4:** Update branch profiles
- Modifies .context-control/profiles/main.json
- Modifies .context-control/profiles/scientific.json
- Modifies .context-control/profiles/orchestration-tools.json
- Sets orchestration_disabled = true
- Sets orchestration_aware = false

**Step 5:** Commit and push
- Stages all changes
- Commits with descriptive message
- Pushes to current branch
- Pushes to scientific branch (if different)
- Pushes to main branch (if different)

### enable-all-orchestration-with-branch-sync.sh

**Step 1:** Clear environment variable
- Removes ORCHESTRATION_DISABLED from .env and .env.local

**Step 2:** Restore git hooks
- Moves hooks from .git/hooks/*.disabled back to .git/hooks/*
- Makes hooks executable again

**Step 3:** Remove marker file
- Deletes .orchestration-disabled

**Step 4:** Update branch profiles
- Modifies all profile files
- Sets orchestration_disabled = false
- Sets orchestration_aware = true

**Step 5:** Commit and push
- Stages all changes
- Commits with descriptive message
- Pushes to current, scientific, and main branches

---

## File Modifications

When you run these scripts, these files will be modified:

### Disabled
- `.env` and `.env.local` - ORCHESTRATION_DISABLED added/removed
- `.git/hooks/*` - Hooks disabled (*.disabled) or restored
- `.orchestration-disabled` - Created when disabled, removed when enabled
- `.context-control/profiles/*.json` - Orchestration status updated

### Created
- `.git/hooks.backup-<timestamp>/` - Hook backup directory
- `.orchestration-disabled` - Marker file (when disabling)

### Not Modified
- Source code files
- Tests
- Core functionality
- Other configuration

---

## Troubleshooting

### Can't find the scripts?
```bash
ls -la scripts/disable-all-orchestration*
ls -la scripts/enable-all-orchestration*
```

### Scripts aren't executable?
```bash
chmod +x scripts/disable-all-orchestration-with-branch-sync.sh
chmod +x scripts/enable-all-orchestration-with-branch-sync.sh
```

### Push failed?
```bash
# Check git status
git status

# Try pushing manually
git push origin scientific
git push origin main

# Or use --skip-push flag
./scripts/disable-all-orchestration-with-branch-sync.sh --skip-push
```

### Need more help?
See **Troubleshooting** section in `ORCHESTRATION_DISABLE_BRANCH_SYNC.md`

---

## Integration with AGENTS.md

The orchestration commands are documented in AGENTS.md under:
- **Orchestration Control Commands** section
- Lists all available scripts with descriptions
- Quick reference format

---

## Related Systems

### Orchestration Control Module
- File: `setup/orchestration_control.py`
- Purpose: Centralized control logic
- Usage: `from setup.orchestration_control import is_orchestration_enabled()`

### Branch Profiles
- Location: `.context-control/profiles/`
- Updated by: disable/enable scripts
- Contains: Orchestration status metadata

### Git Hooks
- Location: `.git/hooks/`
- Status: Disabled/restored by scripts
- Backed up: `.git/hooks.backup-<timestamp>/`

---

## Feature Comparison

| Feature | disable-all-orchestration.sh | disable-all-orchestration-with-branch-sync.sh |
|---------|------------------------------|----------------------------------------------|
| Disable hooks | ✅ | ✅ |
| Set ORCHESTRATION_DISABLED | ✅ | ✅ |
| Update branch profiles | ❌ | ✅ |
| Commit changes | ❌ | ✅ |
| Push to branches | ❌ | ✅ |
| Branch sync | ❌ | ✅ |

---

## Version History

### Version 1.0 (November 12, 2024)
- ✅ Initial implementation
- ✅ Branch sync with profile updates
- ✅ Automatic push to scientific and main
- ✅ Comprehensive documentation
- ✅ Quick reference guide

---

## Support Resources

1. **Quick answers?** → ORCHESTRATION_DISABLE_QUICK_REFERENCE.md
2. **Detailed info?** → ORCHESTRATION_DISABLE_BRANCH_SYNC.md
3. **Implementation details?** → ORCHESTRATION_IMPLEMENTATION_SUMMARY.md
4. **Command reference?** → AGENTS.md (Orchestration section)
5. **Troubleshooting?** → ORCHESTRATION_DISABLE_BRANCH_SYNC.md (Troubleshooting section)

---

## Key Takeaways

✅ **Two main scripts** - disable and enable with branch sync
✅ **Automatic push** - changes go to scientific and main branches
✅ **Profile updates** - orchestration status tracked in branch profiles
✅ **Fully documented** - comprehensive guides and quick reference
✅ **Production ready** - tested and safe to use

---

Last Updated: November 12, 2024
