# Orchestration Approval System

The orchestration hooks now include a user approval system that prevents silent overwrites of local files. When orchestration-tools changes would affect your local workspace, you'll be prompted to approve the changes before they're applied.

## How It Works

When you perform git operations that trigger orchestration synchronization (checkout, merge, push), the system will:

1. **Detect Changes**: Scan for files that differ between your branch and orchestration-tools
2. **Display Summary**: Show exactly which files and directories would be updated
3. **Prompt for Approval**: Ask you to approve or deny the orchestration sync
4. **Log Decision**: Record your approval/denial for audit purposes

## User Approval Flow

### Interactive Mode (Default)

When in an interactive terminal, you'll see:

```
=== Orchestration File Updates ===
The following files will be updated from orchestration-tools:
  → scripts/install-hooks.sh
  → scripts/lib/orchestration-approval.sh
  → .gitignore
  → pyproject.toml

The following directories will be synchronized:
  → setup/ (all contents)
  → scripts/lib/ (all contents)

───────────────────────────────────────
Synchronize orchestration files from orchestration-tools branch?
───────────────────────────────────────
Proceed with orchestration synchronization? (y/n)
```

- Type `y` or `Y` to proceed with the synchronization
- Type anything else or press Enter to skip
- You have 30 seconds to respond before auto-skipping

### Non-Interactive Mode (CI/CD, Scripts)

When not in an interactive terminal (e.g., running in CI/CD):
- Orchestration proceeds automatically
- No prompt is displayed
- Changes are logged

## Controlling Approval Behavior

### Skip Approval Prompts

To bypass approval prompts for a specific command:

```bash
# Allow orchestration without prompting
ORCHESTRATION_APPROVAL_PROMPT=false git checkout my-branch
ORCHESTRATION_APPROVAL_PROMPT=false git merge origin/main
```

This is useful for:
- Automated scripts and CI/CD pipelines
- Unattended server operations
- When you've pre-approved orchestration changes

### Disable All Orchestration

To skip orchestration entirely (hooks don't run):

```bash
DISABLE_ORCHESTRATION_CHECKS=1 git checkout my-branch
```

## Critical: Protecting Copilot and Agent Instructions

The `.github/instructions/` directory contains Copilot and other GitHub agent instructions that are **critical for your development workflow**:

- `taskmaster.instructions.md` - Task Master AI instructions
- `dev_workflow.instructions.md` - Development workflow guidance
- `self_improve.instructions.md` - Self-improvement patterns
- `tools-manifest.json` - Tool configuration
- `vscode_rules.instructions.md` - VSCode-specific rules

**These files are synced automatically to prevent loss when switching branches.** The approval system ensures you're aware when they're being synchronized:

```
The following directories will be synchronized:
  → .github/instructions/ (all contents)

Copilot and agent instructions are critical—proceed with sync? (y/n)
```

If you deny the sync, your instructions are preserved, but you must manually sync them to stay current with orchestration-tools.

## Approval Log

All orchestration approvals are logged to `.git/hooks/.orchestration_log`:

```
[2024-11-17 15:32:10] [main] APPROVAL: GRANTED - post-merge orchestration sync
[2024-11-17 15:45:23] [scientific] APPROVAL: DENIED - orchestration sync
[2024-11-17 16:02:15] [orchestration-tools] APPROVAL: GRANTED - orchestration sync
```

View the log:
```bash
cat .git/hooks/.orchestration_log
```

## What Gets Synchronized

The orchestration system manages these file categories:

### Critical Files (Always Checked)
- Git hooks: `scripts/hooks/*`
- Configuration: `.gitignore`, `.gitattributes`, `.flake8`, `.pylintrc`
- Dependencies: `requirements.txt`, `requirements-dev.txt`, `pyproject.toml`, `uv.lock`
- Orchestration scripts: `scripts/install-hooks.sh`, `scripts/sync_setup_worktrees.sh`
- Documentation: `docs/orchestration-workflow.md`
- GitHub configuration: 
  - `.github/BRANCH_PROPAGATION_POLICY.md`
  - `.github/PROPAGATION_SETUP_CHECKLIST.md`
  - `.github/DOCUMENTATION_DISTRIBUTION_REPORT.md`
  - `.github/pull_request_templates/orchestration-pr.md`
- GitHub workflows (CI/CD):
  - `.github/workflows/extract-orchestration-changes.yml`
  - `.github/workflows/lint.yml`
  - `.github/workflows/test.yml`

### Directories (Full Sync)
- `setup/` - Setup configuration and environment files
- `deployment/` - Deployment configuration
- `scripts/lib/` - Shared shell libraries
- **`.github/instructions/`** - **CRITICAL: Copilot and GitHub agent instructions** (always synced to prevent loss)

### Protected Files (Never Synced)
- `.taskmaster/` - Task Master data (preserved for user work)
- `package-lock.json` - Environment-specific dependencies

## Handling Denials

If you deny orchestration synchronization:

1. Your local files are preserved as-is
2. The hook exits gracefully without errors
3. A log entry records the denial
4. You can manually sync later if needed:

```bash
# Manually apply orchestration changes
git checkout orchestration-tools -- scripts/hooks/
git checkout orchestration-tools -- .gitignore
```

Or force it through the next operation:
```bash
ORCHESTRATION_APPROVAL_PROMPT=false git checkout another-branch
```

## Examples

### Allow orchestration sync during code review
```bash
# You're satisfied with orchestration changes
git checkout feature-branch
# Prompt appears: approve with 'y'
```

### Skip for a quick context switch
```bash
# You're in a hurry and don't want orchestration
git checkout main
# Prompt appears: deny with 'n'
# Return and sync manually later when ready
```

### Automate in CI/CD
```bash
#!/bin/bash
# In CI/CD pipeline, skip prompts
export ORCHESTRATION_APPROVAL_PROMPT=false
git checkout main
git merge origin/develop
# Orchestration applies automatically
```

## Troubleshooting

### Hook Not Prompting

If you're not seeing approval prompts:

1. Check if running in interactive terminal:
   ```bash
   tty  # Shows device path if interactive
   ```

2. Check if env vars are blocking:
   ```bash
   echo $ORCHESTRATION_APPROVAL_PROMPT
   echo $DISABLE_ORCHESTRATION_CHECKS
   ```

3. Verify approval library is installed:
   ```bash
   ls -la scripts/lib/orchestration-approval.sh
   ```

### Approval Library Missing

If you see "orchestration-approval.sh not found":

```bash
# Checkout the missing library from orchestration-tools
git checkout orchestration-tools -- scripts/lib/orchestration-approval.sh
chmod +x scripts/lib/orchestration-approval.sh
```

### Log File Not Created

The log is created automatically in `.git/hooks/.orchestration_log`:

```bash
mkdir -p .git/hooks
touch .git/hooks/.orchestration_log
```

## Related Documentation

- `ORCHESTRATION_PROCESS_GUIDE.md` - Full orchestration workflow
- `ORCHESTRATION_DISABLE_QUICK_REFERENCE.md` - How to disable orchestration
- `.git/hooks/post-checkout` - Checkout hook implementation
- `.git/hooks/post-merge` - Merge hook implementation
