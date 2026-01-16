# Orchestration Approval - Quick Reference

## What's New

Orchestration hooks now ask for your approval before changing files. You control whether orchestration syncs your workspace.

## What You'll See

When orchestration would change files:

```
=== Orchestration File Updates ===
The following files will be updated from orchestration-tools:
  → .gitignore
  → requirements.txt
  
Proceed with orchestration synchronization? (y/n)
```

- Type `y` to approve and proceed
- Type `n` or anything else to deny and skip
- You have 30 seconds to respond

## Common Scenarios

| Scenario | Action | Result |
|----------|--------|--------|
| Happy with changes | Press `y` | Orchestration applies |
| Need to review first | Press `n` | Changes skipped, work preserved |
| In automated script | Set `ORCHESTRATION_APPROVAL_PROMPT=false` | Auto-applies without prompt |
| Want no orchestration | Use `DISABLE_ORCHESTRATION_CHECKS=1` | Hooks skip entirely |

## One-Liners

```bash
# Skip prompts for this command
ORCHESTRATION_APPROVAL_PROMPT=false git checkout main

# Disable all orchestration
DISABLE_ORCHESTRATION_CHECKS=1 git checkout main

# View approval history
cat .git/hooks/.orchestration_log

# Manually sync specific file
git checkout orchestration-tools -- .gitignore
```

## Key Points

✓ **Approval is required** - orchestration won't silently change files  
✓ **Your work is safe** - denials preserve local files  
✓ **Logged for audit** - all approvals/denials are recorded  
✓ **CI/CD friendly** - use env vars to skip prompts in automation  
✓ **Easy override** - manual sync available anytime  

## Why This Matters

Before: Orchestration hooks silently overwrote files during checkout/merge  
After: You get a clear list and choose to approve or reject the changes

This prevents:
- Accidental loss of local configuration
- Silent .taskmaster file overwrites
- Unexpected setup/deployment directory changes
- Hooks being installed without your knowledge

## Documentation

- Full guide: `docs/ORCHESTRATION_APPROVAL.md`
- Orchestration workflow: `ORCHESTRATION_PROCESS_GUIDE.md`
- Disable guide: `ORCHESTRATION_DISABLE_QUICK_REFERENCE.md`
