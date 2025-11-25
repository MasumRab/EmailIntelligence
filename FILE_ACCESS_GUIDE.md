# File Access Control Guide

## 🔓 Quick Reference: How to Enable File Access

| Scenario | Command | Effect |
|----------|---------|--------|
| **Make file executable** | `chmod +x filename` | Add execute permission (755 or 775) |
| **Make file readable** | `chmod +r filename` | Add read permission for all |
| **Make file writable** | `chmod +w filename` | Add write permission |
| **Restrict file (private)** | `chmod 600 filename` | Only owner can read/write |
| **Open directory** | `chmod 755 dirname` | All can read/execute directory |
| **Fix hook permissions** | `./scripts/install-hooks.sh --force` | Sync all hooks from remote |
| **Allow script execution** | `chmod +x script.sh` | Make shell script executable |
| **Open restricted file** | `chmod 644 GEMINI.md` | Make readable by group/others |

---

## 🎯 Common File Access Issues & Solutions

### 1. **Script Won't Execute** ❌

**Symptom:** `Permission denied` when running `./script.sh`

**Root Cause:** File lacks execute permission (644 instead of 755)

**Solutions:**

```bash
# Option A: Quick fix for single file
chmod +x script.sh
./script.sh

# Option B: Fix all shell scripts in directory
chmod +x scripts/*.sh

# Option C: Fix recursively
chmod -R +x scripts/

# Option D: Use the built-in hook installer
./scripts/install-hooks.sh --force
```

**Verify:**
```bash
ls -l script.sh
# Should show: -rwxr-xr-x (755) instead of -rw-r--r-- (644)
```

---

### 2. **Can't Read File** 📄

**Symptom:** `Permission denied` when trying to read `GEMINI.md`

**Current State:**
```
-rw------- 1 masum masum 15359 GEMINI.md
```

**Root Cause:** File is restricted to owner only (600 permissions)

**Solutions:**

```bash
# Option A: Make readable by group
chmod 640 GEMINI.md

# Option B: Make readable by everyone
chmod 644 GEMINI.md

# Option C: Make world-readable
chmod 644 GEMINI.md

# Verify:
cat GEMINI.md
# Should now work
```

**Understanding the modes:**
```
-rw------- (600) = owner only (read/write)
-rw-r----- (640) = owner + group can read
-rw-r--r-- (644) = everyone can read
-rwxr-xr-x (755) = everyone can read/execute
```

---

### 3. **Git Hooks Not Running** 🎣

**Symptom:** Pre-commit hooks never execute, even though files changed

**Root Cause:** Hooks lost execute permission

**Solutions:**

```bash
# Option A: Reinstall hooks from remote (recommended)
./scripts/install-hooks.sh --force

# Option B: Manually fix permissions
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/post-commit
chmod +x .git/hooks/post-checkout
chmod +x .git/hooks/post-merge
chmod +x .git/hooks/post-push

# Option C: Fix all hooks at once
chmod +x .git/hooks/*

# Verify:
ls -la .git/hooks/pre-commit
# Should show: -rwxr-xr-x (755)
```

---

### 4. **Directory Access Denied** 📁

**Symptom:** `Permission denied: cannot open directory`

**Root Cause:** Directory lacks execute permission (644 instead of 755)

**Solutions:**

```bash
# Option A: Fix single directory
chmod 755 dirname

# Option B: Fix directory and all contents
chmod -R 755 dirname

# Option C: Add execute without other changes
chmod +x dirname

# Verify:
ls -ld dirname
# Should show: drwxr-xr-x (755)
```

---

### 5. **Environment Scripts Won't Activate** 🐍

**Symptom:** `./activate_env.sh: Permission denied`

**Root Cause:** Activation scripts lack execute permission

**Solutions:**

```bash
# Fix activation scripts
chmod +x setup/activate_env.sh
chmod +x setup/activate_system.sh
chmod +x setup/wsl_config.sh

# Then activate
./setup/activate_env.sh

# Or run setup to recreate with correct permissions
bash setup/setup_environment_wsl.sh
```

---

## 🔧 Permission Modes Explained

### Standard Unix Permissions

```
chmod 755 = rwxr-xr-x = owner(rwx) group(rx) others(rx)
chmod 644 = rw-r--r-- = owner(rw) group(r) others(r)
chmod 600 = rw------- = owner(rw) only
chmod 700 = rwx------ = owner(rwx) only
chmod 777 = rwxrwxrwx = everyone can do anything (unsafe!)
```

### Numeric Breakdown

```
Position 1: Owner   (4=r, 2=w, 1=x)
Position 2: Group   (4=r, 2=w, 1=x)
Position 3: Others  (4=r, 2=w, 1=x)

Examples:
755 = 7(rwx) + 5(rx) + 5(rx)  = owner full, others read+execute
644 = 6(rw) + 4(r) + 4(r)     = owner read+write, others read only
700 = 7(rwx) + 0 + 0          = owner only
600 = 6(rw) + 0 + 0           = owner read+write only
```

### Letter Notation

```
u = user (owner)
g = group
o = others
a = all

+ = add permission
- = remove permission
= = set exactly

Examples:
chmod u+x file         # Add execute for owner
chmod go-r file        # Remove read from group+others
chmod a+r file         # Add read for everyone
chmod 644 file         # Set to rw-r--r--
```

---

## 📋 File Access Checklist

### Before Development Starts

- [ ] **Hooks are executable**: `ls -la .git/hooks/pre-commit` shows `rwx`
- [ ] **Setup scripts are executable**: `ls -la setup/*.sh` shows `rwx`
- [ ] **Scripts directory is accessible**: `ls -la scripts/` works
- [ ] **Environment file readable**: `cat .env.example` works

```bash
# Quick check script
echo "Checking file access..."
chmod +x .git/hooks/* 2>/dev/null || true
chmod +x setup/*.sh 2>/dev/null || true
chmod +x scripts/*.sh 2>/dev/null || true
echo "✓ File access verified"
```

### After Cloning Repository

```bash
git clone <repo>
cd <repo>

# Fix common permission issues
chmod +x scripts/install-hooks.sh
./scripts/install-hooks.sh --force

# Activate environment
./setup/activate_env.sh

# Run setup if needed
bash setup/setup_environment_wsl.sh
```

### During Development

```bash
# If you modify scripts
git add script.sh
git diff --cached --raw  # Check file mode

# If mode changes aren't tracked
git add --chmod=+x script.sh
git commit -m "Make script executable"
```

---

## 🔐 Restricted Files & When to Open Them

### Currently Restricted Files

| File | Current | Why | When to Open |
|------|---------|-----|--------------|
| `GEMINI.md` | `600` (owner only) | Configuration/secrets | When sharing config |
| `.env` (if exists) | `600` | Environment secrets | Never commit, keep private |
| `.mcp.json` | `644` (readable) | MCP configuration | Always needed |

### How to Open Restricted Files

```bash
# View a restricted file
cat GEMINI.md

# Make it readable by team
chmod 644 GEMINI.md

# Make it group-readable (safer for teams)
chmod 640 GEMINI.md

# Revert to restricted after sharing
chmod 600 GEMINI.md
```

### Security: When NOT to Open Files

```bash
# NEVER make these world-readable
.env              # Contains API keys
.ssh/             # Contains private keys
secrets/          # Contains credentials
*.key             # Private key files

# Safe to make readable
README.md
package.json
src/              # Source code (usually)
docs/             # Documentation
```

---

## 🎯 Automated Permission Management

### Built-in Scripts

#### 1. **Install Hooks** (Recommended)

```bash
# Fix all git hooks from remote orchestration-tools branch
./scripts/install-hooks.sh

# Force reinstall even if up-to-date
./scripts/install-hooks.sh --force

# Verbose output for debugging
./scripts/install-hooks.sh --verbose
```

**What it does:**
- Fetches hooks from `origin/orchestration-tools`
- Applies `chmod +x` to make them executable
- Validates installation
- Error handling and logging

#### 2. **Enable Hooks** (After Development)

```bash
# Re-enable hooks after independent development
./scripts/enable-hooks.sh

# What it does:
# - Moves hooks from .git/hooks.disabled/ back to .git/hooks/
# - Re-applies chmod +x
# - Resumes orchestration sync
```

#### 3. **Setup Environment** (Initial Setup)

```bash
# For WSL (Ubuntu)
bash setup/setup_environment_wsl.sh

# For system packages
bash setup/setup_environment_system.sh

# What it does:
# - Sets umask 022
# - Creates activation scripts with chmod +x
# - Installs dependencies
```

---

## 🚨 Troubleshooting Permission Issues

### Git Hook Permissions Lost

**Scenario:** After pulling/merging, hooks lost executable bit

**Fix:**
```bash
./scripts/install-hooks.sh --force
```

**Manual fix:**
```bash
find .git/hooks -type f ! -name "*.sample" -exec chmod +x {} \;
```

---

### Can't Execute Setup Script

**Scenario:** `bash setup/setup_environment_wsl.sh` still requires `bash` prefix

**Problem:** File not marked executable in git

**Fix:**
```bash
git add --chmod=+x setup/setup_environment_wsl.sh
git commit -m "Make setup script executable"
```

Or locally:
```bash
chmod +x setup/setup_environment_wsl.sh
```

---

### Permission Changes Not Committing

**Scenario:** `chmod +x script.sh` but `git status` doesn't show changes

**Reason:** Need to explicitly stage permission changes

**Fix:**
```bash
# Explicitly add with chmod flag
git add --chmod=+x script.sh

# Or configure git to track modes
git config core.filemode true

# Verify
git diff --cached --raw
# Should show :100644 100755
```

---

### Mixed Permissions After Merge

**Scenario:** Different files have different permissions after merge conflict

**Fix:**
```bash
# Reset to remote version
git checkout --theirs -- scripts/
chmod +x scripts/*.sh

# Or reinstall hooks
./scripts/install-hooks.sh --force

# Or enforce all permissions
bash -c 'chmod +x scripts/*.sh && chmod +x setup/*.sh && chmod +x .git/hooks/*'
```

---

## 🔄 Permission Sync Across Team

### When Pushing Changes

```bash
# Make sure permissions are correct before committing
chmod +x new_script.sh

# Stage with explicit mode
git add --chmod=+x new_script.sh

# Verify before commit
git diff --cached --raw | grep "^:100644 100755"

# Commit with note
git commit -m "feat: add new_script.sh with execute permissions"
```

### When Pulling Changes

```bash
# Pull normally
git pull

# Run hook installer to ensure all permissions correct
./scripts/install-hooks.sh --force

# If issues persist
chmod -R +x scripts/
chmod +x .git/hooks/*
```

---

## 📊 Current Project File Permissions

### Executable Files (755)

```
.git/hooks/post-checkout
.git/hooks/post-commit-setup-sync
.git/hooks/post-push
.git/hooks/pre-push
scripts/install-hooks.sh
scripts/enable-hooks.sh
setup/activate_env.sh (after setup)
setup/activate_system.sh (after setup)
setup/wsl_config.sh (after setup)
auto_sync_docs.py
scripts/agents/*.py
scripts/atomic_commit_manager.py
```

### Regular Files (644)

```
.env.example
.mcp.json
pyproject.toml
requirements.txt
setup/launch.py
All source code (src/, backend/, client/)
All documentation (*.md)
```

### Restricted Files (600)

```
GEMINI.md (owner only)
(Any .env files with secrets - never commit)
```

---

## ✅ Best Practices

### 1. Always Run Setup Scripts First

```bash
./scripts/install-hooks.sh --force
./setup/activate_env.sh
```

### 2. Don't Manually Create Scripts

Instead of creating shell scripts manually:

```bash
# ❌ Wrong
cat > new_script.sh << 'EOF'
#!/bin/bash
...
EOF

# ✅ Right
cat > new_script.sh << 'EOF'
#!/bin/bash
...
EOF
chmod +x new_script.sh
git add --chmod=+x new_script.sh
```

### 3. Use Git Hooks for Consistency

- Don't manually `chmod` every file
- Let hooks and scripts manage permissions
- Use `.git/hooks.disabled` if you need to bypass temporarily

### 4. Document Permission Requirements

Add to README:
```markdown
## Initial Setup

After cloning:
```bash
./scripts/install-hooks.sh --force
./setup/activate_env.sh
```
```

### 5. Commit Permission Changes

Always track permission changes in git:
```bash
# Before
git add script.sh
git diff --cached --raw  # Shows :100644 100644

# After
git reset script.sh
git add --chmod=+x script.sh
git diff --cached --raw  # Shows :100644 100755

# Commit
git commit -m "Make script executable"
```

---

## 🛠️ Quick Command Reference

```bash
# Make file executable
chmod +x filename

# Make file readable
chmod +r filename

# Make directory accessible
chmod 755 dirname

# Fix all hooks
./scripts/install-hooks.sh --force

# Fix directory recursively
chmod -R 755 dirname

# Fix all scripts
chmod +x scripts/*.sh
chmod +x setup/*.sh

# Check permissions
ls -la filename
stat filename

# Find all executable files
find . -type f -executable

# Find all files with wrong permissions
find . -name "*.sh" ! -perm /111

# Git track permission change
git add --chmod=+x filename

# Git check mode bits
git ls-files --stage | grep "^100"
```

---

## 📞 When to Seek Help

**Contact when:**
- Hooks won't execute after `./scripts/install-hooks.sh --force`
- Getting `Permission denied` on random files
- Permission changes not tracked in git
- Merge conflicts affecting permissions
- Can't access shared restricted files

**Include:**
```bash
# Provide this info:
pwd                      # Current directory
ls -la filename          # File permissions
git status               # Git status
git config core.filemode # Filemode setting
./scripts/install-hooks.sh --verbose 2>&1 | head -20
```

---

**Last Updated:** 2025-11-14  
**Scope:** Local file access management and permission troubleshooting
