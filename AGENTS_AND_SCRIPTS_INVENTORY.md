# Agents and Scripts Inventory
**Repository:** EmailIntelligence  
**Date:** December 13, 2025  
**Purpose:** Complete listing of all agent configurations and scripts

---

## Agent Configurations Overview

### Total Agent Directories: 32
All agent directories are tracked in git on orchestration-tools branch.

---

## Agent Directory Structure

### IDE & Editor Configurations (6)
```
.claude/                    → Claude Code IDE configuration
.cursor/                    → Cursor IDE configuration
.gemini/                    → Google Gemini IDE configuration
.cline/                     → Cline IDE configuration
.vscode/                    → VS Code configuration
.zed/                       → Zed editor configuration
```

### Development Agents (4)
```
.roo/                       → Roo agent
.iflow/                     → iFlow agent
.crush/                     → Crush agent
.continue/                  → Continue agent
```

### Specialized Agents (4)
```
.agents/                    → Speckit agents collection (9 agents)
.specify/                   → Specify agent
.codebuddy/                 → CodeBuddy agent
.serena/                    → Serena agent
```

### Additional Agents (5)
```
.codex/                     → Codex agent
.qwen/                      → Qwen agent
.trae/                      → Trae agent
.windsurf/                  → Windsurf agent
.opencode/                  → OpenCode agent
```

### Infrastructure & Configuration (6)
```
.context-control/           → Context management
.rulesync/                  → RuleSync agent
.emailintelligence/         → Email Intelligence config
.github/                    → GitHub workflows & actions
.taskmaster/                → TaskMaster submodule
.taskmaster_/               → TaskMaster backup
```

### Support & Utilities (3)
```
.trunk/                     → Trunk agent/tools
.junie/                     → Junie agent
.kilocode/                  → Kilocode agent
.kilo/                      → Kilo agent
.kiro/                      → Kiro agent
.clinerules/                → Cline rules
```

---

## Agent Files Breakdown

### .agents/ (Speckit Commands - 9 agents)
```
.agents/commands/
├── speckit.analyze.md              → Analysis specifications
├── speckit.checklist.md            → Checklist generation
├── speckit.clarify.md              → Clarification commands
├── speckit.constitution.md         → Constitution specifications
├── speckit.implement.md            → Implementation specifications
├── speckit.plan.md                 → Planning specifications
├── speckit.specify.md              → Specification generation
├── speckit.tasks.md                → Task specifications
└── speckit.taskstoissues.md        → Task to issue conversion
```

### .claude/ (Claude Code Configuration)
```
.claude/
├── agents/
│   └── planner.md                  → Claude planner agent
├── commands/
│   └── review-pr.md                → PR review command
├── memories/
│   ├── CLAUDE.md                   → Claude memory
│   └── copilot-instructions.md     → Copilot integration
├── mcp.json                        → MCP configuration
├── settings.json                   → Claude settings
├── settings.local.json             → Local settings override
└── slash_commands.json             → Slash commands definition
```

### .cursor/ (Cursor IDE Configuration)
```
.cursor/
├── commands/
│   ├── review-pr.md
│   ├── speckit.analyze.md
│   ├── speckit.checklist.md
│   ├── speckit.clarify.md
│   ├── speckit.constitution.md
│   ├── speckit.implement.md
│   ├── speckit.plan.md
│   ├── speckit.specify.md
│   └── speckit.tasks.md
├── rules/
│   ├── CLAUDE.mdc                  → Claude rules (NEW in Phase 3)
│   ├── GEMINI.mdc                  → Gemini rules (NEW in Phase 3)
│   ├── copilot-instructions.mdc    → Copilot rules (NEW in Phase 3)
│   ├── cursor_rules.mdc            → Cursor rules
│   ├── overview.mdc                → Rules overview
│   ├── self_improve.mdc            → Self-improvement rules
│   └── taskmaster/
│       ├── dev_workflow.mdc        → Development workflow
│       └── taskmaster.mdc          → TaskMaster rules
├── mcp.json                        → MCP configuration
└── mcp.json.backup-1763794303111   → Backup configuration
```

### .gemini/ (Google Gemini Configuration)
```
.gemini/
├── commands/
│   ├── speckit.analyze.toml
│   ├── speckit.checklist.toml
│   ├── speckit.clarify.toml
│   ├── speckit.constitution.toml
│   ├── speckit.implement.toml
│   ├── speckit.plan.toml
│   ├── speckit.specify.toml
│   ├── speckit.taskstoissues.toml
│   └── speckit.tasks.toml
└── settings.json                   → Gemini settings
```

### .cline/ (Cline IDE Configuration)
```
.cline/
└── mcp.json                        → MCP configuration (NEW in Phase 3)
```

### Other Major Agent Directories
```
.github/
├── workflows/                      → GitHub Actions workflows
├── instructions/                   → GitHub instructions
└── [configuration files]

.context-control/
├── [context profiles]              → Context management profiles
├── [environment configs]
└── [context switching tools]

.rulesync/
├── [rule synchronization]          → Rule sync configuration
└── [sync protocols]

.taskmaster/                        → Git submodule
└── [task management system]
```

---

## Scripts Inventory

### Total Scripts: 100+

### Location: `/scripts/`

---

## Scripts by Category

### Core Infrastructure Scripts (Phase 1-3)
```
scripts/
├── markdown/
│   ├── lint-and-format.sh (178 lines)
│   │   └─ Format and lint markdown with prettier & markdownlint-cli
│   ├── standardize-links.sh (228 lines)
│   │   └─ Standardize markdown links to ./ prefix
│   └── README.md (387 lines)
│       └─ Markdown tools documentation
├── test-script-sync.sh (284 lines)
│   └─ Validate script synchronization across branches
├── verify-dependencies.py
│   └─ Check all system, npm, and Python dependencies
└── install-hooks.sh
    └─ Install git hooks for orchestration
```

### Orchestration & Hook Management
```
scripts/
├── enable-all-orchestration.sh       → Enable all hooks
├── disable-all-orchestration.sh      → Disable all hooks
├── restore-hooks.sh                  → Restore hook functionality
├── enable-hooks.sh                   → Enable specific hooks
├── orchestration_status.sh           → Check orchestration status
├── validate-orchestration-context.sh → Validate orchestration
├── cleanup_orchestration_preserve.sh → Safe cleanup
├── monitor_orchestration_changes_fixed.sh → Monitor changes
└── sync_orchestration_files.sh       → Sync orchestration files
```

### Git Hooks (Located in scripts/hooks/)
```
scripts/hooks/
├── post-checkout                     → Post-checkout hook
├── post-commit                       → Post-commit hook
├── post-merge                        → Post-merge hook (sync submodule)
├── pre-commit                        → Pre-commit validation
└── post-push                         → Post-push hook
```

### Stash Management
```
scripts/
├── stash_manager_optimized.sh        → Optimized stash manager
├── stash_analysis.sh                 → Analyze stashes
├── stash_details.sh                  → Show stash details
├── handle_stashes_optimized.sh       → Handle stash operations
├── interactive_stash_resolver.sh     → Interactive resolver
├── interactive_stash_resolver_optimized.sh → Optimized resolver
└── [stash utility scripts]
```

### Synchronization & Sync Scripts
```
scripts/
├── parallel_sync.py                  → Parallel synchronization
├── script_sync.py                    → Script synchronization
├── sync_prioritizer.py               → Priority-based sync
├── incremental_sync.py               → Incremental sync
├── validate-branch-propagation.sh    → Validate propagation
├── update-all-branches.sh            → Update all branches
├── sync_setup_worktrees.sh           → Sync worktree setup
└── distribute_alignment_scripts.sh   → Distribute scripts
```

### Validation & Verification
```
scripts/
├── parallel_validator.py             → Parallel validation
├── verify-agent-docs-consistency.sh  → Verify agent docs
├── validate-ide-agent-inclusion.sh   → Validate IDE agents
├── branch_analysis_check.sh          → Analyze branches
├── verify-dependencies.py            → Dependency verification
└── [validation utilities]
```

### Task Management & Completion Tracking
```
scripts/
├── task_completion_tracker.py        → Track task completion
├── task_dependency_resolver.py       → Resolve dependencies
├── goal_task_validator.py            → Validate goals
├── completion_predictor.py           → Predict completion
├── test_task_completion_tracker.py   → Test tracker
└── test_completion_predictor.py      → Test predictor
```

### Performance & Resource Monitoring
```
scripts/
├── resource_monitor.py               → Monitor resources
├── predictive_estimator.py           → Estimate metrics
├── bottleneck_detector.py            → Detect bottlenecks
├── token_optimization_monitor.py     → Monitor tokens
├── conflict_predictor.py             → Predict conflicts
├── test_resource_monitor.py          → Test monitor
├── test_predictive_estimator.py      → Test estimator
├── test_conflict_predictor.py        → Test predictor
└── [performance utilities]
```

### Advanced Utilities
```
scripts/
├── architectural_rule_engine.py      → Architectural rules
├── concurrent_review.py              → Concurrent review
├── event_driven_assigner.py          → Event assignment
├── atomic_commit_manager.py          → Atomic commits
├── maintenance_scheduler.py          → Schedule maintenance
├── context_contamination_monitor.py  → Monitor contamination
├── sync_orchestration_files.sh       → Sync files
└── [advanced tools]
```

### Cleanup & Maintenance
```
scripts/
├── cleanup.sh                        → General cleanup
├── cleanup_application_files.sh      → Clean app files
└── [cleanup utilities]
```

### Testing & Validation
```
scripts/
├── test_orchestration.sh             → Test orchestration
├── test_translation_pipeline.py      → Test translation
├── test_simple_translation.py        → Test simple translation
├── test_incremental_sync.py          → Test sync
├── test_maintenance_scheduler.py     → Test scheduler
├── test_onboarding_guide.py          → Test onboarding
├── test_doc_generation_template.py   → Test doc generation
└── test_concurrent_review.py         → Test reviews
```

### Bash Command Scripts
```
scripts/bash/
├── create-pr-resolution-spec.sh      → Create PR specs
├── pr-test-executor.sh               → Execute PR tests
├── task-creation-validator.sh        → Validate tasks
└── gh-pr-ci-integration.sh           → GitHub PR integration
```

### Currently Disabled Scripts
```
scripts/currently_disabled/
├── test_security_fixes.py            → Security tests
├── download_hf_models.py             → Download models
├── setup_linting.py                  → Setup linting
├── launch.sh                         → Launch script
├── launch.py                         → Python launcher
├── error_checking_prompt.py          → Error checking
├── test_enhanced_filtering.py        → Enhanced filtering
├── temp_email_nodes.py               → Email nodes
├── codebase_analysis.py              → Code analysis
├── temp_retrieve.py                  → Retrieve utility
```

### Libraries & Common Code
```
scripts/lib/
├── common.sh                         → Common bash functions
├── git_utils.sh                      → Git utilities
├── logging.sh                        → Logging functions
├── validation.sh                     → Validation functions
├── error_handling.sh                 → Error handling
└── stash_common.sh                   → Stash utilities
```

### Job Processing
```
scripts/
└── start_job_worker.py               → Start job worker
```

### Worktree & Branch Management
```
scripts/
├── distribute_alignment_scripts.sh   → Distribute scripts
├── update-all-branches.sh            → Update branches
├── sync_setup_worktrees.sh           → Setup worktrees
└── branch_rename_migration.py        → Migrate branches
```

---

## Statistics

| Category | Count |
|----------|-------|
| Agent Directories | 32 |
| Agent Configuration Files | 200+ |
| Total Scripts | 100+ |
| Bash Scripts (.sh) | ~50 |
| Python Scripts (.py) | ~40 |
| Currently Disabled | ~10 |
| Libraries | 6 |
| Markdown Tools | 3 |
| Documentation Files | 13+ |

---

## Key Scripts Summary

### Most Critical (Phase 1-3)
```
1. scripts/markdown/lint-and-format.sh
   → Formats markdown with prettier and lints with markdownlint-cli
   → Usage: bash scripts/markdown/lint-and-format.sh --help

2. scripts/test-script-sync.sh
   → Validates script synchronization across branches
   → Usage: bash scripts/test-script-sync.sh

3. scripts/verify-dependencies.py
   → Verifies all required dependencies are installed
   → Usage: python scripts/verify-dependencies.py
```

### Infrastructure Scripts
```
1. scripts/install-hooks.sh
   → Installs git hooks for automation

2. scripts/enable-all-orchestration.sh
   → Enables all orchestration hooks

3. scripts/disable-all-orchestration.sh
   → Disables orchestration hooks

4. scripts/orchestration_status.sh
   → Shows current orchestration status
```

### Advanced Synchronization
```
1. scripts/parallel_sync.py
   → Parallel sync operations

2. scripts/incremental_sync.py
   → Incremental synchronization

3. scripts/script_sync.py
   → Script-specific synchronization
```

---

## Agent Configuration Files Added in Phase 3

These files were tracked and committed in Phase 3:

```
✅ .cursor/rules/CLAUDE.mdc
   → Claude IDE rules configuration (NEW)

✅ .cursor/rules/GEMINI.mdc
   → Gemini IDE rules configuration (NEW)

✅ .cursor/rules/copilot-instructions.mdc
   → Copilot integration rules (NEW)

✅ .claude/memories/copilot-instructions.md
   → Claude memory for Copilot integration (NEW)

✅ .cline/mcp.json
   → Cline IDE MCP configuration (NEW)
```

---

## Script Organization

### By Language
- **Bash Scripts:** 50+ files in scripts/ and hooks/
- **Python Scripts:** 40+ files for advanced operations
- **Markdown Files:** 3 in markdown/ subdirectory

### By Purpose
- **Orchestration:** 10+ scripts for hook management
- **Synchronization:** 10+ scripts for sync operations
- **Validation:** 10+ scripts for verification
- **Performance:** 10+ scripts for monitoring
- **Task Management:** 10+ scripts for task operations
- **Testing:** 10+ test scripts
- **Utilities:** 20+ utility scripts

### By Status
- **Active:** 90+ production scripts
- **Disabled:** 10+ in currently_disabled/
- **Testing:** 15+ test files
- **Libraries:** 6 shared library files

---

## Finding Scripts

### Search by category
```bash
find scripts -name "*sync*"           # Sync scripts
find scripts -name "*orchestr*"       # Orchestration scripts
find scripts -name "*valid*"          # Validation scripts
find scripts -name "*monitor*"        # Monitoring scripts
```

### Search by language
```bash
find scripts -name "*.sh"             # Bash scripts
find scripts -name "*.py"             # Python scripts
find scripts -name "*.md"             # Documentation
```

### List all scripts
```bash
ls -la scripts/                       # Top-level scripts
find scripts -type f | sort           # All scripts sorted
```

---

## Documentation

### Available Guides
- `scripts/README.md` - Scripts directory guide
- `scripts/DEPENDENCIES.md` - Dependency requirements
- `scripts/markdown/README.md` - Markdown tools guide

### Phase 3 Documentation
- `ORCHESTRATION_TOOLS_PHASE3_COMPLETION.md` - Phase 3 completion
- `ORCHESTRATION_TOOLS_CLUSTER_SUMMARY.md` - Project overview
- `ORCHESTRATION_TOOLS_QUICK_REFERENCE.md` - Quick reference
- `ORCHESTRATION_TOOLS_INDEX.md` - Navigation guide

---

## Quick Access

### All Agent Directories
```bash
cd /home/masum/github/EmailIntelligenceGem
ls -d .*/    # List all agent directories
```

### All Scripts
```bash
cd /home/masum/github/EmailIntelligenceGem/scripts
find . -type f \( -name "*.sh" -o -name "*.py" \) | sort
```

### Agent Docs
```bash
cat AGENT_CONFIG_TRACKING_STATUS.md          # Agent config details
cat ORCHESTRATION_TOOLS_INDEX.md             # Complete index
```

---

**Last Updated:** December 13, 2025  
**Status:** Complete inventory  
**Total Agents:** 32 directories  
**Total Scripts:** 100+  
**Documentation:** Comprehensive
