# Documentation Index

**For:** Solo Developer  
**Updated:** December 11, 2025  
**Quick Navigation:** Jump to what you need

---

## Getting Started (5 minutes)

Start here if you're new or need to set up:

1. **[README.md](./README.md)** - What is EmailIntelligence?
2. **[INSTALLATION.md](./INSTALLATION.md)** - Environment setup
3. **[Agents Setup](./AGENTS.md)** - Configure your AI tools (Claude, Gemini, etc.)

→ **Next:** Go to [Daily Development](#daily-development) or
[SINGLE_USER_WORKFLOW.md](./SINGLE_USER_WORKFLOW.md)

---

## Daily Development

### Common Tasks

| Task                                   | Document                                                                          |
| -------------------------------------- | --------------------------------------------------------------------------------- |
| **Switch between branches**            | [Branch Switching Guide](./docs/guides/branch_switching_guide.md)                 |
| **Understand how orchestration works** | [Orchestration Quick Reference](./ORCHESTRATION_HOOKS_QUICK_REFERENCE.md)         |
| **See current project status**         | [Current State Documentation](./ORCHESTRATION_TOOLS_FINAL_STATE_DOCUMENTATION.md) |
| **View upcoming work**                 | [Outstanding Todos](./OUTSTANDING_TODOS.md)                                       |

### Workflows

- **[Git Workflow Guide](./docs/git_workflow_plan.md)** - How to structure your work
- **[Orchestration Process](./ORCHESTRATION_PROCESS_GUIDE.md)** - How hooks and scripts work

→ **New to daily development?** Read [SINGLE_USER_WORKFLOW.md](./SINGLE_USER_WORKFLOW.md) (your
practical guide)

---

## Deep Dives (Understanding the Architecture)

When you need to understand how things work under the hood:

### Core Architecture

- **[Submodule Migration Guide](./docs/SUBMODULE_MIGRATION_GUIDE.md)** - Why .taskmaster is a Git
  submodule
- **[Orchestration Summary](./docs/orchestration_summary.md)** - How orchestration-tools branch
  works
- **[Git Workflow Plan](./docs/git_workflow_plan.md)** - Detailed workflows and procedures

→ **Quick overview?** See
[ORCHESTRATION_HOOKS_QUICK_REFERENCE.md](./ORCHESTRATION_HOOKS_QUICK_REFERENCE.md)

### Current State

- **[Final State Documentation](./ORCHESTRATION_TOOLS_FINAL_STATE_DOCUMENTATION.md)** - Complete
  status of orchestration-tools
- **[Branch Protection Analysis](./BRANCH_PROTECTION_AND_WORKFLOW_ANALYSIS.md)** - GitHub setup
  details

### Verification & Security

- **[Agent Files Audit](./AGENT_FILES_AUDIT.md)** - Inventory of 20 agent directories and 19 config
  files
- **[Security Audit](./AGENT_CONFIGURATION_SECURITY_AUDIT.md)** - Verification that zero secrets are
  exposed

---

## Agent Integration

Configure and use your preferred AI tools:

| Agent             | Document                                            |
| ----------------- | --------------------------------------------------- |
| **Claude Code**   | [CLAUDE.md](./CLAUDE.md)                            |
| **Google Gemini** | [GEMINI.md](./GEMINI.md)                            |
| **Alibaba Qwen**  | [QWEN.md](./QWEN.md)                                |
| **Crush**         | [CRUSH.md](./CRUSH.md)                              |
| **IFLOW**         | [IFLOW.md](./IFLOW.md)                              |
| **LLXPRT**        | [LLXPRT.md](./LLXPRT.md)                            |
| **All Agents**    | [AGENTS.md](./AGENTS.md) - Master integration guide |

→ **Start here:** [AGENTS.md](./AGENTS.md) for complete agent setup

---

## Troubleshooting

### Common Issues

| Problem                            | Solution                                                                                                                              |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Branch switching not working**   | See [Emergency Procedures](./PHASE3_ROLLBACK_OPTIONS.md)                                                                              |
| **Hooks not executing**            | See [Hook Reference](./ORCHESTRATION_HOOKS_QUICK_REFERENCE.md#troubleshooting)                                                        |
| **Submodule (.taskmaster) issues** | See [Submodule Migration Guide](./docs/SUBMODULE_MIGRATION_GUIDE.md#troubleshooting)                                                  |
| **Git merge conflicts**            | See [Git Workflow Plan](./docs/git_workflow_plan.md) or [SINGLE_USER_WORKFLOW.md](./SINGLE_USER_WORKFLOW.md#handling-merge-conflicts) |

### Emergency Help

- **[Emergency Procedures & Rollback Options](./PHASE3_ROLLBACK_OPTIONS.md)** - How to recover from
  issues
- **[Hook Troubleshooting](./ORCHESTRATION_HOOKS_QUICK_REFERENCE.md)** - Debug hook problems
- **[Single-User Workflow Troubleshooting](./SINGLE_USER_WORKFLOW.md#troubleshooting-common-issues)**
  - Daily workflow issues

---

## Reference Materials

Detailed information for specific components:

### Orchestration & Git Hooks

- **[Orchestration Hooks Quick Reference](./ORCHESTRATION_HOOKS_QUICK_REFERENCE.md)** - All 5 hooks
  at a glance
- **[Hook Behavior Matrix](./ORCHESTRATION_HOOKS_QUICK_REFERENCE.md#branch-behavior-matrix)** - What
  each hook does on each branch
- **[Orchestration Strategies](./docs/ORCHESTRATION_PUSH_STRATEGIES.md)** - How changes propagate

### Branch Management

- **[Branch Propagation Policy](./BRANCH_PROTECTION_AND_WORKFLOW_ANALYSIS.md)** - Merge rules and
  file ownership
- **[Propagation Setup](./BRANCH_PROTECTION_AND_WORKFLOW_ANALYSIS.md)** - Current GitHub workflow
  setup

### CI/CD & Deployment

- **[CI/CD Recommendations](./docs/cicd_recommendations.md)** - GitHub Actions setup

### Scripts & Tools

- **[Scripts Inventory](./scripts/SCRIPTS_INVENTORY.md)** - Complete registry of 100+ scripts
- **[Markdown Tools](./scripts/markdown/README.md)** - Markdown linting and formatting guide
- **[Script Dependencies](./scripts/DEPENDENCIES.md)** - All system, npm, and Python requirements
- **[Sync Status](./scripts/SCRIPTS_SYNC_STATUS.md)** - Which scripts are on which branches
- **[Scripts Directory](./scripts/README.md)** - Scripts folder navigation and contributing

---

## Quick Command Reference

### Branch Operations

```bash
# Switch to orchestration-tools
git checkout orchestration-tools

# Switch to development branch
git checkout scientific

# Update .taskmaster submodule
git submodule update --init --recursive
```

### Hook Management

```bash
# Install/update hooks
bash scripts/install-hooks.sh

# Verify hooks are working
ls -la .git/hooks/
```

### Script Management

```bash
# Format and lint all markdown
bash scripts/markdown/lint-and-format.sh --fix --all

# Check markdown without modifying
bash scripts/markdown/lint-and-format.sh --check --all

# Standardize all links to ./ prefix
bash scripts/markdown/standardize-links.sh --fix --all

# Verify all dependencies are installed
python scripts/verify-dependencies.py

# Test script sync across branches
bash scripts/test-script-sync.sh
```

### Orchestration Changes

```bash
# On orchestration-tools, after commit:
# post-commit hook will ask: "Propagate changes? (y/N):"
# Answer yes to propagate to all branches
```

---

## File Ownership & Organization

### Root-Level Documentation Files (20 essential files)

| Category              | Files                                                                                                                    |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Project Overview**  | README.md, INSTALLATION.md                                                                                               |
| **Documentation**     | DOCUMENTATION_INDEX.md (this file)                                                                                       |
| **Agent Integration** | AGENTS.md, CLAUDE.md, GEMINI.md, QWEN.md, CRUSH.md, IFLOW.md, LLXPRT.md                                                  |
| **Orchestration**     | ORCHESTRATION_HOOKS_QUICK_REFERENCE.md, ORCHESTRATION_PROCESS_GUIDE.md, ORCHESTRATION_TOOLS_FINAL_STATE_DOCUMENTATION.md |
| **Branch Management** | BRANCH_PROTECTION_AND_WORKFLOW_ANALYSIS.md                                                                               |
| **Audits & Security** | AGENT_FILES_AUDIT.md, AGENT_CONFIGURATION_SECURITY_AUDIT.md                                                              |
| **Emergency**         | PHASE3_ROLLBACK_OPTIONS.md                                                                                               |
| **Tracking**          | OUTSTANDING_TODOS.md                                                                                                     |

### docs/ Directory Structure

```
docs/
├── core/                           # Essential architecture docs
│   ├── SUBMODULE_MIGRATION_GUIDE.md
│   ├── orchestration_summary.md
│   └── git_workflow_plan.md
├── guides/                         # How-to guides
│   ├── branch_switching.md
│   └── workflow_and_review_process.md
├── reference/                      # Reference material
│   ├── ORCHESTRATION_PUSH_STRATEGIES.md
│   └── cicd_recommendations.md
└── archived/                       # Old/completed work
    ├── old_workflow_docs/
    └── completed_work/
```

---

## How to Use This Index

### I want to...

**...set up my environment** → [INSTALLATION.md](INSTALLATION.md)

**...understand how branches work** → [Orchestration Summary](docs/core/orchestration_summary.md)

**...know what hooks do** → [Hook Quick Reference](ORCHESTRATION_HOOKS_QUICK_REFERENCE.md)

**...switch branches safely** → [Branch Switching Guide](docs/guides/branch_switching.md)

**...configure my AI agent** → [AGENTS.md](AGENTS.md)

**...see project status** →
[Final State Documentation](ORCHESTRATION_TOOLS_FINAL_STATE_DOCUMENTATION.md)

**...troubleshoot an issue** → [Emergency Procedures](PHASE3_ROLLBACK_OPTIONS.md)

**...understand the submodule architecture** →
[Submodule Migration Guide](docs/core/SUBMODULE_MIGRATION_GUIDE.md)

**...find and use project scripts** → [Scripts Inventory](scripts/SCRIPTS_INVENTORY.md)

**...format markdown documentation** → [Markdown Tools](scripts/markdown/README.md)

**...check script dependencies** → [Script Dependencies](scripts/DEPENDENCIES.md)

---

## Documentation Map

```
EmailIntelligence Project Documentation

Getting Started (5 min)
├── README.md
├── INSTALLATION.md
└── AGENTS.md

Daily Development
├── Branch Switching Guide
├── Hook Reference
└── Workflow Guide

Architecture Understanding
├── Submodule Migration Guide
├── Orchestration Summary
└── Git Workflow Plan

Troubleshooting
├── Emergency Procedures
└── Specific Issue Guides

Reference
├── Orchestration Strategies
├── Branch Policy
└── CI/CD Setup
```

---

## Key Principles

### Branch System

- **orchestration-tools**: Infrastructure and hooks (no .taskmaster)
- **scientific/main**: Development environment (includes .taskmaster submodule)
- **Hooks**: Automatically handle branch-specific behavior

### Git Submodules

- **.taskmaster** is a native Git submodule
- Only exists on development branches
- Auto-initialized via post-checkout hook
- Updated via post-merge hook

### Agents

- 14+ AI agents supported (Claude, Gemini, Kiro, Qwen, etc.)
- Context-controlled per branch
- Zero secrets exposed (using environment variables)

---

## Documentation Status

✅ **Orchestration:** Complete and verified  
✅ **Agent Integration:** All 20 directories present  
✅ **Branch Management:** Policies and rules documented  
✅ **Security:** Zero secrets, environment variables used  
✅ **Workflows:** All procedures documented  
✅ **Troubleshooting:** Emergency procedures documented

---

## Quick Stats

| Metric                          | Value |
| ------------------------------- | ----- |
| Root documentation files (kept) | 20    |
| Archived documentation files    | 22    |
| docs/ subdirectories            | 4     |
| Agent directories supported     | 20    |
| Git hooks                       | 5     |
| Key principles                  | 3     |

---

## Contact & Support

This is a **solo project** - no team support.

For questions about documentation:

- Check [Emergency Procedures](PHASE3_ROLLBACK_OPTIONS.md) first
- Review relevant section in this index
- Check archived documentation if needed

---

**Last Updated:** December 11, 2025  
**Status:** Single-User Optimized  
**Navigation:** This is your starting point
