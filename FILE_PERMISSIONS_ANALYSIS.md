# File Permissions Analysis: Local & Remote Setup

## 📋 Executive Summary

This project implements a **multi-layered permission system** that works across local development and remote CI/CD pipelines. File permissions are managed through:

1. **Git Core Configuration** - Tracks executable bits in repository
2. **Setup Scripts** - Enforce umask and chmod operations during initialization
3. **GitHub Actions** - Grant specific permissions for workflow operations
4. **Git Hooks** - Automatically enforce permission consistency

---

## 🔍 LOCAL FILE PERMISSIONS

### Current Local Setup (Ubuntu 24.04)

**Directory Permissions:**
```
drwxr-xr-x (755)  /home/masum/github/EmailIntelligenceGem/
drwxr-xr-x (755)  setup/
drwxr-xr-x (755)  src/
drwxr-xr-x (755)  backend/
drwxr-xr-x (755)  client/
drwxr-xr-x (755)  tests/
drwxr-xr-x (755)  deployment/
```

**Executable Files (100755 mode in Git):**

Scripts tracked as executable in Git index:

| File | Purpose |
|------|---------|
| `auto_sync_docs.py` | Documentation synchronization |
| `scripts/agents/*.py` | Agent health/performance monitoring |
| `scripts/atomic_commit_manager.py` | Git commit management |
| `scripts/bottleneck_detector.py` | Performance detection |
| `scripts/cleanup.sh` | Cleanup automation |
| `scripts/install-hooks.sh` | Git hook installation (permission enforcement) |
| `scripts/enable-hooks.sh` | Re-enable hooks |
| `.specify/scripts/bash/*.sh` | Custom bash utilities |

**Regular Files (100644 mode):**
```
-rw-r--r-- (644)  AGENTS.md
-rw-r--r-- (644)  .env.example
-rw-r--r-- (644)  pyproject.toml
-rw-r--r-- (644)  requirements.txt
-rw-r--r-- (644)  setup/launch.py
-rw------- (600)  GEMINI.md  (restricted file)
```

### Git Core Configuration

```bash
git config --list | grep filemode
# Output: core.filemode=true
```

**Significance:**
- ✅ **Enabled**: Git tracks file mode bits (executable permissions)
- ✅ **Consequence**: When files are cloned, executable bits are preserved
- ⚠️ **Limitation**: Requires fat32/FAT filesystems to be aware of this

### Git Index Tracking

```bash
git ls-files --stage | grep "^100755"
# 40+ files tracked with executable bit
```

The Git index preserves the file mode (100755 = executable, 100644 = regular):

```
100755 <commit-hash> <stage> auto_sync_docs.py
100755 <commit-hash> <stage> scripts/install-hooks.sh
100755 <commit-hash> <stage> scripts/enable-hooks.sh
100644 <commit-hash> <stage> setup/launch.py  # Regular file
100644 <commit-hash> <stage> .env.example
```

---

## ⚙️ LOCAL PERMISSION ENFORCEMENT MECHANISMS

### 1. Setup Environment Scripts

#### `setup/setup_environment_wsl.sh` (WSL-Optimized)

**File Permission Setup (Lines 364-373):**
```bash
# Set up proper file permissions for WSL
umask 022

# Create activation script and make it executable
cat > activate_env.sh << 'ACTIVATE_EOF'
...
ACTIVATE_EOF

chmod +x activate_env.sh

# Create WSL-specific configuration
cat > wsl_config.sh << 'WSL_EOF'
...
WSL_EOF

chmod +x wsl_config.sh
```

**What it does:**
- Sets **umask 022**: New files created with 644 (rw-r--r--), directories with 755 (rwxr-xr-x)
- Creates helper scripts with explicit `chmod +x`
- Ensures environment activation scripts are executable

#### `setup/setup_environment_system.sh` (System-Package Priority)

**Similar permission handling:**
```bash
chmod +x activate_system.sh
```

Creates a reusable activation script with proper execute permissions.

---

## 🔧 GIT HOOK PERMISSION ENFORCEMENT

### Git Hooks Installation System

**Two-Script Architecture:**

#### 1. `scripts/install-hooks.sh` - Primary Hook Installer

**Key Permission Operation (Line 109):**
```bash
# Checkout from remote branch
if git show "origin/$ORCHESTRATION_BRANCH:$hook_path" > "$git_hook_path" 2>/dev/null; then
    chmod +x "$git_hook_path"  # ← CRITICAL: Make hook executable
    log_info "Successfully installed hook: $hook_name"
    return 0
```

**Workflow:**
1. Fetches hooks from `orchestration-tools` branch (remote source of truth)
2. Checks out hook file to `.git/hooks/`
3. **Applies `chmod +x`** to make the hook executable
4. Validates installation

**Hooks Managed:**
- `pre-commit` - Runs before committing
- `post-commit` - Runs after commit
- `post-merge` - Runs after merge/pull
- `post-checkout` - Runs on branch switch
- `post-push` - Runs after push

#### 2. `scripts/enable-hooks.sh` - Re-enable After Development

**Permission Enforcement (Line 68):**
```bash
# Re-enable each hook
for hook in "${HOOKS[@]}"; do
    local disabled_path="$DISABLED_HOOKS_DIR/$hook"
    local hook_path="$HOOKS_DIR/$hook"

    if [[ -f "$disabled_path" ]]; then
        # Move hook back from disabled directory
        mv "$disabled_path" "$hook_path"
        chmod +x "$hook_path"  # ← Re-apply execute permission
        log_info "Re-enabled hook: $hook"
```

**Purpose:**
- Developers can disable hooks with `.git/hooks.disabled` directory
- When ready to resume orchestration sync, `enable-hooks.sh` re-activates them
- Explicitly re-applies execute permissions

### Hook Directory Structure

```
.git/
├── hooks/                      # Active hooks
│   ├── pre-commit (755)
│   ├── post-commit (755)
│   ├── post-checkout (755)
│   ├── post-merge (755)
│   └── post-push (755)
│
└── hooks.disabled/             # Temporarily disabled hooks
    ├── pre-commit (755)        # Backed up copies
    ├── post-commit (755)
    └── ... (others)
```

---

## 🚀 REMOTE PERMISSION SETUP (GitHub Actions)

### GitHub Actions Workflow: `extract-orchestration-changes.yml`

**Trigger:** When orchestration files change on non-main branches

#### Permission Block (Lines 36-38):

```yaml
permissions:
  contents: write          # Can read/write repository contents
  pull-requests: write     # Can comment on PRs
```

**What these permissions allow:**
- `contents: write` - Push changes to branches, create commits, manage files
- `pull-requests: write` - Post comments on PRs (for deployment notifications)

#### File Operations in Workflow:

**Extract Phase (Lines 124-131):**
```yaml
# Check out each orchestration file from source
for file in "${ORCH_FILES[@]}"; do
  if git show "$SOURCE_BRANCH:$file" >/dev/null 2>&1; then
    echo "Extracting: $file"
    git show "$SOURCE_BRANCH:$file" > "$file"  # ← File mode preserved by git show
    git add "$file"
  fi
done
```

**Key Points:**
- `git show` preserves file mode bits (including executable)
- Files extracted to `orchestration-tools-changes` branch retain their permissions
- `git add` stages files with their mode bits intact

**Push Phase (Lines 151-156):**
```yaml
- name: Force Push to Remote
  if: steps.detect.outputs.detected == 'true'
  run: |
    TARGET_BRANCH="orchestration-tools-changes"
    git push -f origin "$TARGET_BRANCH"
    echo "✓ Pushed to $TARGET_BRANCH"
```

- **Force push** (-f) preserves all file modes in the pushed commits
- Destination branch receives files with identical permissions as source

#### Orchestration Files Tracked (Lines 100-122):

```yaml
ORCH_FILES=(
  "setup/"                    # Entire setup directory
  "deployment/"               # Entire deployment directory
  "scripts/lib/"              # Script libraries
  "scripts/install-hooks.sh"  # Hook installer (executable)
  "scripts/sync_setup_worktrees.sh"
  "scripts/reverse_sync_orchestration.sh"
  "scripts/cleanup_orchestration.sh"
  ".flake8"                   # Linting config
  ".pylintrc"                 # Linting config
  "pyproject.toml"            # Project config
  "requirements.txt"          # Dependencies
  "requirements-dev.txt"      # Dev dependencies
  "uv.lock"                   # Lock file
  "tsconfig.json"             # TypeScript config
  "tailwind.config.ts"        # Tailwind config
  "vite.config.ts"            # Vite config
  "drizzle.config.ts"         # Database config
  "components.json"           # UI components config
  ".gitignore"                # Git ignore
  ".gitattributes"            # Git attributes (for permissions!)
  "launch.py"                 # Main launcher
)
```

---

## 🔗 How They Work Together

### Complete Permission Flow

```
┌─ Development Changes ─────────────────────────────────────────┐
│                                                                 │
│  1. Developer modifies setup/launch.py or scripts/install.sh   │
│                                                                 │
│  2. Git stages changes (file mode bits preserved in index)      │
│                                                                 │
│  3. Developer commits and pushes to feature branch              │
│                                                                 │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─ GitHub Actions Workflow ─────────────────────────────────────┐
│                                                                 │
│  1. Detects orchestration files changed                        │
│                                                                 │
│  2. Checks out files from source branch (permissions intact)   │
│                                                                 │
│  3. Pushes to orchestration-tools-changes (modes preserved)    │
│                                                                 │
│  4. (Later merged to orchestration-tools - canonical branch)   │
│                                                                 │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─ Distributed to All Branches ─────────────────────────────────┐
│                                                                 │
│  1. Git hooks in all branches detect updates                   │
│                                                                 │
│  2. post-checkout hook runs: scripts/install-hooks.sh          │
│                                                                 │
│  3. install-hooks.sh fetches latest hooks from orchestration   │
│                                                                 │
│  4. chmod +x applied to each hook (ensure executable)          │
│                                                                 │
│  5. Other scripts auto-synced with permissions from orchestr.  │
│                                                                 │
└───────────────────────────────────────────────────────────────┘
```

---

## 📊 Permission Summary Table

| Layer | Mechanism | Files Affected | How Applied |
|-------|-----------|-----------------|-------------|
| **Git Core** | core.filemode=true | All tracked files | Automatic via git config |
| **Git Index** | File mode bits (100755/100644) | Scripts & executables | Stored in git index |
| **Setup Scripts** | umask 022, chmod +x | activate_env.sh, wsl_config.sh | During environment setup |
| **Git Hooks** | install-hooks.sh chmod +x | .git/hooks/* | On post-checkout, post-merge |
| **GitHub Actions** | Workflow permissions block | contents: write, PR: write | At workflow execution time |
| **Remote Push** | git push preserves modes | All orchestration files | When extracting to orchestration-tools-changes |

---

## 🔐 Security Considerations

### Current Implementation

✅ **Strengths:**
1. **Automatic propagation** - Permissions flow through Git's native file mode tracking
2. **Centralized source of truth** - orchestration-tools branch is canonical
3. **Hook enforcement** - Automatic sync ensures consistency
4. **Multi-layer redundancy** - Multiple chmod operations ensure reliability

⚠️ **Limitations:**
1. **File mode bits only** - Doesn't handle umask across all systems
2. **WSL-specific** - wsl_config.sh sets umask 022 only in WSL
3. **Disabled hooks bypass** - Developers can disable hooks to bypass sync
4. **GitHub Actions permissions** - Limited to broad repository access

---

## 🛠️ Troubleshooting

### Hooks Not Executable After Clone

**Problem:** `.git/hooks/pre-commit` exists but isn't executable

**Solution:**
```bash
./scripts/install-hooks.sh --force
```

**Or manually:**
```bash
chmod +x .git/hooks/*
```

### Permission Mismatch After Merge

**Problem:** Some files lose execute bit after merge

**Solution:**
```bash
# Re-enable hooks to trigger orchestration sync
./scripts/enable-hooks.sh

# Manually sync
git checkout origin/orchestration-tools -- scripts/
chmod +x scripts/*.sh
```

### Setup Scripts Not Executable

**Problem:** `activate_env.sh` doesn't have execute bit

**Solution:**
```bash
chmod +x setup/activate_env.sh setup/wsl_config.sh
```

---

## 📝 Configuration Files

### `.gitattributes` (Currently Empty)

**Current state:** No entries

**Recommended enhancement** (not currently implemented):
```
*.sh           eol=lf
scripts/*.sh   eol=lf
setup/*.sh     eol=lf
```

This would enforce LF line endings on shell scripts regardless of OS.

### Git Configuration

**Key settings:**
```bash
core.filemode = true           # Track execute bits
core.autocrlf = input          # Convert CRLF to LF on commit
filter.lfs.required = true     # Git LFS enabled (for large files)
safe.directory = *             # Security setting
```

---

## 🎯 Implementation Status

### ✅ Implemented
- [x] Git file mode bit tracking (core.filemode=true)
- [x] Remote orchestration extraction (GitHub Actions)
- [x] Hook installation with chmod (install-hooks.sh)
- [x] Hook re-enablement (enable-hooks.sh)
- [x] Setup script chmod operations
- [x] umask configuration in WSL setup
- [x] Orchestration-tools branch as source of truth

### ⚠️ Partially Implemented
- [ ] .gitattributes line ending enforcement
- [ ] Comprehensive umask documentation
- [ ] Permission tests in CI/CD

### 📋 Not Implemented
- [ ] POSIX ACLs for advanced permissions
- [ ] SELinux security contexts
- [ ] Windows NTFS permission mapping

---

## 🔍 How to Verify

### Check Git Configuration
```bash
git config --list | grep filemode
# Should output: core.filemode=true
```

### List Executable Files
```bash
git ls-files --stage | grep "^100755"
```

### Check Local Permissions
```bash
stat setup/launch.py         # Should be 644
stat scripts/install-hooks.sh # Should be 755 (executable)
```

### Test Workflow
```bash
# Clone fresh repo
git clone <repo>
cd <repo>

# Check if hooks are executable
ls -la .git/hooks/pre-commit
# Should show: -rwxr-xr-x (or 755)

# If not, run:
./scripts/install-hooks.sh --force
```

---

## 📚 References

### Files Implementing Permission System

1. **setup/setup_environment_wsl.sh** - Lines 364-373 (umask, chmod)
2. **setup/setup_environment_system.sh** - Line 245 (chmod activation script)
3. **scripts/install-hooks.sh** - Line 109 (chmod hooks)
4. **scripts/enable-hooks.sh** - Line 68 (chmod hooks)
5. **.github/workflows/extract-orchestration-changes.yml** - Lines 36-38 (GH Actions permissions)

### Related Files

- `.git/config` - Git configuration (core.filemode)
- `.gitattributes` - Git attributes (empty, enhancement opportunity)
- `scripts/hooks/*` - Actual hook implementations
- `.git/hooks/` - Installed hooks directory

---

## 🚀 Recommendations for Improvements

### 1. Add .gitattributes Enforcement
```bash
# Add to .gitattributes
*.sh           eol=lf
scripts/*.sh   eol=lf
setup/*.sh     eol=lf
deployment/**  eol=lf
```

### 2. Add Permission Tests in CI/CD
```bash
# Check that all shell scripts are executable
git ls-files --stage | grep "^100755.*\.sh$"
```

### 3. Document Permission Requirements
Add to README:
```markdown
## File Permissions

This project uses Git's file mode tracking. To ensure proper execution:
1. Clone with: `git clone <repo>`
2. Run: `./scripts/install-hooks.sh`
3. Activate environment: `./setup/activate_env.sh` or `./setup/activate_system.sh`
```

### 4. Create Permission Verification Script
```bash
#!/bin/bash
# verify-permissions.sh

echo "Verifying file permissions..."
# Check hooks are executable
for hook in .git/hooks/{pre-commit,post-commit,post-checkout,post-merge,post-push}; do
    [[ -x "$hook" ]] || echo "ERROR: $hook is not executable"
done
```

---

**Last Updated:** 2025-11-14  
**Analysis Scope:** Local permissions + Remote GitHub Actions setup  
**Git Filemode:** Enabled (core.filemode=true)
