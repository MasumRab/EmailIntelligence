## 🔧 Orchestration Changes PR

### Description

<!-- Describe the changes to orchestration-managed files -->

### Type of Change

- [ ] 🐛 Bug fix in setup/deployment
- [ ] ✨ New feature for environment setup
- [ ] 📝 Documentation update
- [ ] 🔄 Refactoring setup/deployment
- [ ] 🚀 Performance improvement
- [ ] 🔐 Security/compatibility fix

### Files Modified

<!-- List orchestration-managed files changed in this PR -->

- [ ] `setup/` files
- [ ] `deployment/` files
- [ ] `scripts/` files
- [ ] Build configuration (tsconfig.json, package.json, etc.)
- [ ] Development configuration (.flake8, .pylintrc, pyproject.toml, etc.)
- [ ] Git configuration (.gitignore, .gitattributes)

### Impact Assessment

#### Branches Affected

This change affects which branches?

- [ ] All branches (most likely for setup files)
- [ ] Specific branches: _____________________
- [ ] Only orchestration-tools

#### Breaking Changes?

- [ ] No breaking changes
- [ ] Yes, breaking changes (describe below)

If breaking:
<!-- Explain what breaks and migration path -->

#### Compatibility

- [ ] Linux/WSL
- [ ] macOS
- [ ] Windows (native)
- [ ] Python 3.10+
- [ ] Node.js (specify version): _____________

Tested on:
- OS: _____________________
- Python version: _____________________
- Node version: _____________________

### Testing Performed

<!-- Describe the testing done locally before pushing -->

- [ ] Run setup script: `./setup/setup_environment_system.sh`
- [ ] Run launch system: `python setup/launch.py --help`
- [ ] Run affected tests: (specify tests)
- [ ] Manual validation on target system
- [ ] No new errors/warnings in logs
- [ ] Environment variables work correctly
- [ ] Dependencies install correctly

Test results:
<!-- Include test output or summary -->

### Review Checklist

- [ ] Code follows project style guidelines
- [ ] Comments added for complex logic
- [ ] No hardcoded paths or values
- [ ] Error handling is present
- [ ] Documentation updated if needed
- [ ] Changes don't break other branches

### Propagation Plan

Once merged to `orchestration-tools`, this change will:

1. Be available to all branches on next `git pull` / `git checkout`
2. Be automatically synced via post-checkout and post-merge hooks
3. Be applied via `./scripts/sync_setup_worktrees.sh` for worktree setups

Potential impact on existing branches:
<!-- Describe if developers need to take any action -->

### Additional Notes

<!-- Any additional context, gotchas, or notes for reviewers -->

### Reviewers

Please request review from:
- Orchestration maintainers
- Developers who frequently use the affected setup files

---

## 🤖 Auto-Generated Note

This PR was automatically created to ensure proper review of orchestration-managed files. These changes will propagate to all branches after merge, so careful review is essential.

### ⚠️ Important Reminders

- Do not merge draft PRs without full testing and approval
- All orchestration changes require review before merging
- Breaking changes require discussion with the team
- Test on multiple platforms if affecting setup/deployment
- Document any new environment variables or requirements
