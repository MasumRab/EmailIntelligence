# 🚀 Quick Permission Fixes

## One-Line Fixes for Common Problems

### 🔧 Fix Everything at Once

```bash
# Most comprehensive - run this first
./scripts/fix-permissions.sh

# Check without fixing (dry-run)
./scripts/fix-permissions.sh --check

# Verbose output
./scripts/fix-permissions.sh --verbose
```

---

## ⚡ Quick Fixes by Problem

### Problem: "permission denied" on hooks

```bash
./scripts/install-hooks.sh --force
```

### Problem: Can't run setup script

```bash
chmod +x setup/setup_environment_wsl.sh setup/setup_environment_system.sh
bash setup/setup_environment_wsl.sh
```

### Problem: Can't activate environment

```bash
chmod +x setup/activate_env.sh setup/activate_system.sh
./setup/activate_env.sh
```

### Problem: Script execution fails

```bash
# Fix all scripts at once
chmod +x scripts/*.sh

# Or fix specific script
chmod +x scripts/your_script.sh
./scripts/your_script.sh
```

### Problem: Can't read file

```bash
# Make readable (e.g., GEMINI.md)
chmod 644 GEMINI.md
cat GEMINI.md
```

### Problem: Permission denied on directory

```bash
# Fix directory access
chmod 755 dirname

# Fix recursively
chmod -R 755 scripts/ setup/
```

---

## 📋 Checklist After Clone/Pull

```bash
# Step 1: Fix all permissions
./scripts/fix-permissions.sh

# Step 2: Install/update hooks
./scripts/install-hooks.sh --force

# Step 3: Activate environment
./setup/activate_env.sh

# Step 4: Verify everything works
echo "✓ Ready to develop!"
```

---

## 🎯 Most Used Commands

| Need | Command |
|------|---------|
| Fix all permissions | `./scripts/fix-permissions.sh` |
| Fix hooks | `./scripts/install-hooks.sh --force` |
| Make file executable | `chmod +x file` |
| Make readable | `chmod 644 file` |
| Fix directory | `chmod 755 dir` |
| Check before fixing | `./scripts/fix-permissions.sh --check` |
| Activate environment | `./setup/activate_env.sh` |

---

## ✅ Test It Works

After running fixes:

```bash
# Should all succeed
ls -la .git/hooks/pre-commit     # Should show rwx
./scripts/install-hooks.sh       # Should complete
./setup/activate_env.sh          # Should show "activated"
python --version                 # Should show version
```

---

## 🆘 Still Having Issues?

```bash
# Run verbose check
./scripts/fix-permissions.sh --verbose

# Check Git filemode setting
git config core.filemode
# Should output: true

# List all files with wrong permissions
./scripts/fix-permissions.sh --check --verbose
```

See **FILE_ACCESS_GUIDE.md** for detailed troubleshooting.

---

## 💡 Remember

- **Hooks** need to be executable (755)
- **Scripts** need to be executable (755)
- **Data files** just need to be readable (644)
- **Directories** need execute permission (755)
- **API keys/secrets** should be restricted (600)

Run `./scripts/fix-permissions.sh` when in doubt! 🎯
