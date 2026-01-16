# Hook Version Mismatch Issue - Root Cause Analysis

## Problem Description

The most common cause of hook-related errors is **version mismatches** between installed hooks and the canonical versions in the remote `orchestration-tools` branch.

## Root Cause: Local vs Remote Hook Installation

### The Problem
```bash
# OLD install-hooks.sh behavior:
cp scripts/hooks/* .git/hooks/  # Copies from LOCAL branch

# This causes issues when:
# 1. Developer modifies hooks in orchestration-tools
# 2. Commits changes to orchestration-tools locally
# 3. Switches to main branch
# 4. Runs install-hooks.sh → Installs LOCAL modified hooks
# 5. But remote orchestration-tools has DIFFERENT versions
# 6. Hook behavior becomes inconsistent across environments
```

### Why This Happens

1. **Local Branch State**: Hooks are copied from the current branch's `scripts/hooks/` directory
2. **Branch Switching**: When switching branches, `scripts/hooks/` may not exist or have different content
3. **Remote Divergence**: Local commits to orchestration-tools may not be pushed yet
4. **Environment Inconsistency**: Different developers/clones get different hook versions

## The Fix: Remote-First Installation

### New Behavior
```bash
# NEW install-hooks.sh behavior:
git show "origin/orchestration-tools:scripts/hooks/pre-commit" > .git/hooks/pre-commit

# Benefits:
# 1. Always installs from REMOTE canonical source
# 2. Consistent versions across all environments
# 3. Prevents local modifications from affecting installations
# 4. Fails safely if remote branch doesn't exist
```

### Implementation Details

#### 1. Remote Branch Validation
```bash
# Check if remote branch exists
if ! git ls-remote --exit-code --heads origin "$ORCHESTRATION_BRANCH"; then
    log_error "Remote branch $ORCHESTRATION_BRANCH not found"
    exit 1
fi
```

#### 2. Fetch Latest from Remote
```bash
# Ensure we have the latest remote data
git fetch origin "$ORCHESTRATION_BRANCH" --quiet
```

#### 3. Install from Remote Source
```bash
# Copy directly from remote branch
git show "origin/$ORCHESTRATION_BRANCH:$hook_path" > "$git_hook_path"
```

#### 4. Version Comparison
```bash
# Only update if remote version differs from installed
if ! git diff --quiet "origin/$ORCHESTRATION_BRANCH:$hook_path" "$git_hook_path"; then
    # Install new version
fi
```

## Error Prevention

### Common Error Scenarios Now Prevented

#### Scenario 1: Modified Local Hooks
```
Before: Local changes to scripts/hooks/pre-commit get installed everywhere
After:  Only remote canonical versions are installed
```

#### Scenario 2: Branch Switching Issues
```
Before: Switching to main installs main's (non-existent) hooks
After:  Always installs from orchestration-tools remote
```

#### Scenario 3: Unpushed Commits
```
Before: Local orchestration-tools changes affect installations
After:  Only pushed remote changes are used
```

## Verification Commands

### Check Installed Hook Versions
```bash
# See what version is currently installed
head -5 .git/hooks/pre-commit

# Compare with remote canonical version
git show origin/orchestration-tools:scripts/hooks/pre-commit | head -5
```

### Verify Installation Source
```bash
# This should show remote installation
./scripts/install-hooks.sh --verbose

# Output should show:
# [INFO] Installing Git hooks from remote orchestration-tools branch...
# [INFO] Installing hook: pre-commit
# [INFO] Updating hook: pre-commit
```

## Troubleshooting

### "Remote branch orchestration-tools not found"
**Cause**: Remote branch doesn't exist or isn't accessible
**Fix**: Check remote configuration and branch existence
```bash
git remote -v
git ls-remote --heads origin
```

### "Hook not found in remote orchestration-tools"
**Cause**: Hook file doesn't exist in remote branch
**Fix**: Ensure hooks are committed and pushed to orchestration-tools
```bash
git checkout orchestration-tools
ls scripts/hooks/
git push origin orchestration-tools
```

### Hook behavior inconsistent
**Cause**: Old locally-installed hooks still present
**Fix**: Force reinstall from remote
```bash
./scripts/install-hooks.sh --force --verbose
```

## Key Benefits

1. **Consistency**: All environments get identical hook versions
2. **Reliability**: No dependency on local branch state
3. **Safety**: Prevents accidental installation of modified hooks
4. **Debugging**: Clear logging shows installation source and process
5. **Recovery**: `--force` flag allows recovery from inconsistent states

## Migration Notes

- **Old installations**: May have locally-modified hooks
- **Migration path**: Run `./scripts/install-hooks.sh --force` to standardize
- **Backward compatibility**: Script works with or without remote access
- **Error handling**: Graceful degradation when remote is unavailable

This fix ensures that hook-related errors are eliminated by guaranteeing version consistency across all development environments.