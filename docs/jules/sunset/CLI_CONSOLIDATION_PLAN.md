# CLI Consolidation Analysis — S11

**Date**: 2026-11-11  
**Source Branches**: 
- main (16 files)
- orchestration-tools (44 files + 16 in src/cli.bak_main)
- consolidate/cli-unification (53 files)

---

## Command Inventory by Tree

### main (16 files)
| File | Command | Test Coverage |
|------|---------|---------------|
| align_command.py | align | tests/cli/test_align_command.py |
| analyze_command.py | analyze | tests/cli/test_cli_commands.py |
| analyze_history_command.py | analyze-history | tests/cli/test_cli_commands.py |
| factory.py | (dispatcher) | — |
| git/branch_health.py | git branch-health | ? |
| git/conflicts.py | git conflicts | ? |
| identify_command.py | identify | tests/cli/test_identify_command.py |
| integration.py | integration | ? |
| interface.py | (base) | — |
| plan_rebase_command.py | plan-rebase | ? |
| registry.py | (registry) | — |
| resolve_command.py | resolve | ? |
| validate_command.py | validate | ? |
| state.py | (state) | — |
| main.py | (entry) | — |

### orchestration-tools (44 files + 16 bak_main)
**Unique commands** (not in main):
| File | Command | Test? | Notes |
|------|---------|-------|-------|
| agent/rule_sync.py | rule-sync | No | New |
| agent/scaffold.py | agent-scaffold | No | New |
| analysis/code_audit.py | code-audit | tests/cli/commands/task/test_cluster_branches.py* | New |
| analysis/compare.py | compare | No | New |
| analysis/import_audit.py | import-audit | No | New |
| analysis/validate.py | analysis-validate | No | New |
| git/align.py | git align | No | New |
| git/analyze.py | git analyze | No | New |
| git/auto_resolve.py | git auto-resolve | No | New |
| git/discover.py | git discover | No | New |
| git/history.py | git history | No | New |
| git/merge_semantic.py | git merge-semantic | No | New |
| git/merge_smart.py | git merge-smart | No | New |
| git/pr_extract.py | git pr-extract | No | New |
| git/rebase.py | git rebase | No | New |
| git/resolve.py | git resolve | No | New |
| git/stash_resolve.py | git stash-resolve | No | New |
| task/analyze_tasks.py | task analyze | No | New |
| task/cluster_branches.py | task cluster | tests/cli/commands/task/test_cluster_branches.py | New |
| task/engine/branch_clustering.py | (engine) | No | New |
| task/engine/validation_framework.py | (engine) | No | New |
| task/list_tasks.py | task list | No | New |
| task/taskmaster.py | taskmaster | No | New |
| infra/backup.py | infra-backup | No | New |
| infra/deploy.py | infra-deploy | No | New |
| infra/install_tools.py | infra-install-tools | No | New |
| infra/verify.py | infra-verify | No | New |
| automation/mcp_sync.py | automation-mcp-sync | No | New |
| automation/monitor.py | automation-monitor | No | New |
| guide.py | guide | tests/integration/test_cli_guides.py | New |
| ide.py | ide | No | New |
| integration.py | integration | Duplicate? | — |
| validate_command.py | validate | Duplicate? | — |

**bak_main (16 files)** — appears to be main's src/cli copied here:
| File | Status |
|------|--------|
| integration.py.bak_main | Backup of main's integration.py |

### consolidate/cli-unification (53 files)
**All commands** (superset of orchestration-tools + more):
| Category | Files | Tests |
|----------|-------|-------|
| Agent | agent/rule_sync.py, agent/scaffold.py | None |
| Analysis | analysis/code_audit.py, analysis/compare.py, analysis/import_audit.py, analysis/validate.py | test_cluster_branches.py* |
| Automation | automation/mcp_sync.py, automation/monitor.py | None |
| Docs | docs/__init__.py | None |
| Git | git/align.py, git/analyze.py, git/auto_resolve.py, git/branch_health.py, git/conflicts.py, git/discover.py, git/history.py, git/merge_semantic.py, git/merge_smart.py, git/pr_extract.py, git/rebase.py, git/resolve.py, git/stash_resolve.py, git/topology.py, git/verify_merge.py | None |
| Guide/IDE | guide.py, ide.py | test_cli_guides.py |
| Infra | infra/backup.py, infra/deploy.py, infra/install_tools.py, infra/verify.py | None |
| Integration | integration.py | None |
| Task | task/analyze_tasks.py, task/cluster_branches.py, task/engine/branch_clustering.py, task/engine/validation_framework.py, task/list_tasks.py, task/taskmaster.py | test_cluster_branches.py |
| Core | commands/__init__.py, factory.py, git/__init__.py, interface.py, main.py, registry.py, services/nlp.py, state.py, task/__init__.py | test_cli_contracts.py, test_cli.py |

**Unique to consolidate** (not in orchestration-tools):
| File | Command | Test |
|------|---------|------|
| docs/__init__.py | docs | None |
| git/topology.py | git topology | None |
| git/verify_merge.py | git verify-merge | None |
| services/nlp.py | (service) | None |

---

## Deduplication Plan

### Commands EXISTING in main (keep as-is, 13 commands)
1. align → align_command.py ✅ tested
2. analyze → analyze_command.py ✅ tested
3. analyze-history → analyze_history_command.py ✅ tested
4. git branch-health → git/branch_health.py ❓
5. git conflicts → git/conflicts.py ❓
6. identify → identify_command.py ✅ tested
7. integration → integration.py ❓
8. plan-rebase → plan_rebase_command.py ❓
9. resolve → resolve_command.py ❓
10. validate → validate_command.py ❓
11. factory, registry, state, interface, main.py — infrastructure

### Commands UNIQUE to orchestration-tools/consolidate (port to extract/cli-consolidated)

| Priority | Command | Source | Test Exists? | Dependencies | Status |
|----------|---------|--------|--------------|--------------|--------|
| **Tier 1: Core Git/Task** | | | | | |
| 1 | git align | OT + consolidate | No | — | PORT |
| 2 | git analyze | OT + consolidate | No | — | PORT |
| 3 | git auto-resolve | OT + consolidate | No | — | PORT |
| 4 | git discover | OT + consolidate | No | — | PORT |
| 5 | git history | OT + consolidate | No | — | PORT |
| 6 | git merge-semantic | OT + consolidate | No | — | PORT |
| 7 | git merge-smart | OT + consolidate | No | — | PORT |
| 8 | git pr-extract | OT + consolidate | No | — | PORT |
| 9 | git rebase | OT + consolidate | No | — | PORT |
| 10 | git resolve | OT + consolidate | No | — | PORT |
| 11 | git stash-resolve | OT + consolidate | No | — | PORT |
| 12 | git topology | consolidate only | No | — | PORT |
| 13 | git verify-merge | consolidate only | No | — | PORT |
| 14 | task analyze | OT + consolidate | No | — | PORT |
| 15 | task cluster | OT + consolidate | ✅ test_cluster_branches.py | .taskmaster/ | PORT |
| 16 | task list | OT + consolidate | No | — | PORT |
| 17 | taskmaster | OT + consolidate | No | .taskmaster/ | PORT |
| **Tier 2: Analysis/Infra** | | | | | |
| 18 | code-audit | OT + consolidate | No | AST | PORT |
| 19 | compare | OT + consolidate | No | — | PORT |
| 20 | import-audit | OT + consolidate | No | — | PORT |
| 21 | analysis-validate | OT + consolidate | No | — | PORT |
| 22 | infra-backup | OT + consolidate | No | — | PORT |
| 23 | infra-deploy | OT + consolidate | No | — | PORT |
| 24 | infra-install-tools | OT + consolidate | No | — | PORT |
| 25 | infra-verify | OT + consolidate | No | — | PORT |
| **Tier 3: Agent/Automation** | | | | | |
| 26 | rule-sync | OT + consolidate | No | .agent/rules/ | PORT |
| 27 | agent-scaffold | OT + consolidate | No | ~/.gemini/ | PORT |
| 26 | automation-mcp-sync | OT + consolidate | No | MCP | PORT |
| 27 | automation-monitor | OT + consolidate | No | — | PORT |
| 28 | guide | OT + consolidate | ✅ test_cli_guides.py | — | PORT |
| 29 | ide | OT + consolidate | No | — | PORT |
| **Blocked/Deferred** | | | | | |
| 30 | docs | consolidate only | No | — | DEFER (low value) |

---

## Refactoring Requirements for Compatibility

### 1. Import Path Normalization
- **main** uses flat: `from .align_command import AlignCommand`
- **consolidate** uses nested: `from .commands.analysis.code_audit import AnalyzeCodeCommand`
- **Action**: Update `src/cli/commands/__init__.py` to re-export all commands with consistent flat paths

### 2. Dispatcher Integration
- **main**: `src/cli/commands/factory.py` has `COMMAND_REGISTRY` dict
- **consolidate**: Same file but expanded registry
- **Action**: Merge registries, deduplicate by command name; use consolidate's as base

### 3. Test Coverage — CRITICAL
- **Only 3 commands have tests**: task cluster, guide, (align/analyze/identify in main)
- **27 commands have NO tests** — must write tests before porting
- **Action**: For each command, either:
  - Copy test from consolidate branch (if exists)
  - Write minimal test (import + instantiation + help)
  - Mark as BLOCKED until test added

### 4. Dependency Isolation
| Module | Used By | Action |
|--------|---------|--------|
| `src/cli/services/nlp.py` | code-audit, analyze_tasks | Make optional import; fallback to stub |
| `src/cli/task/engine/branch_clustering.py` | task cluster, taskmaster | Internal — port with command |
| `src/cli/task/engine/validation_framework.py` | task cluster, taskmaster | Internal — port with command |
| `.taskmaster/` modules | task cluster, taskmaster | Check if submodule init'd; skip if not |
| MCP client | automation-mcp-sync | Make optional; skip if not installed |

### 5. Entry Point
- **main**: `src/cli/main.py` with typer app (13 commands)
- **consolidate**: `src/cli/main.py` expanded (53 commands)
- **Action**: Use consolidate's main.py as base; register all ported commands

### 6. Command Interface Compatibility
- **main** commands: inherit from `Command` base in `interface.py`
- **consolidate** commands: same base but may have different `add_arguments` signatures
- **Action**: Verify all ported commands implement `execute(args)` and `add_arguments(parser)`

---

## Test Writing Template

For each untested command, create test in `tests/cli/commands/<category>/test_<command>.py`:

```python
"""Test for <command> command."""
import pytest
from src.cli.commands.<category>.<command> import <CommandClass>

def test_<command>_instantiation():
    """Test command can be instantiated."""
    cmd = <CommandClass>()
    assert cmd.name == "<command>"
    assert cmd.description

def test_<command>_help(capsys):
    """Test command help output."""
    from argparse import ArgumentParser
    parser = ArgumentParser()
    cmd = <CommandClass>()
    cmd.add_arguments(parser)
    # Parse --help
    with pytest.raises(SystemExit):
        parser.parse_args(["--help"])
    captured = capsys.readouterr()
    assert "<command>" in captured.out

# If command has dependencies, test with mocks
def test_<command>_execute_mock():
    """Test command execute with mocked deps."""
    cmd = <CommandClass>()
    # Set mocked dependencies
    cmd.set_dependencies({"security_validator": Mock()})
    # Execute with minimal args
    result = await cmd.execute(Namespace())
    assert result in (0, 1)  # Success or expected failure
```

---

## Next Steps (S11 Deliverable → S12 Execution)

### S11 Output: This Plan (`docs/jules/sunset/CLI_CONSOLIDATION_PLAN.md`)

### S12 Session Prompt:
```text
Repository: MasumRab/EmailIntelligence. Base: main.

Execute the CLI consolidation plan from docs/jules/sunset/CLI_CONSOLIDATION_PLAN.md:

1. Create extract/cli-consolidated from origin/main
2. For each Tier 1 → Tier 3 command:
   a. Copy file from consolidate/cli-unification
   b. Normalize imports to flat structure
   c. Write/copy test (tests/cli/commands/<cat>/test_<cmd>.py)
   d. Run test to verify
   e. Commit: "feat(cli): add <command> command"
3. Update src/cli/commands/__init__.py registry (merge, deduplicate)
4. Update src/cli/main.py to register all commands
5. Run full suite after each batch
6. Push branch, open draft PR with --base main

Blocked commands: document import chain in CLI_CONSOLIDATION_REPORT.md
Deferred: docs command (low value)

Deliverables:
- PR with ported commands
- docs/jules/sunset/CLI_CONSOLIDATION_REPORT.md with:
  * Commands ported / blocked / deferred
  * Test results per command
  * Import dependency map
  * Registry diff
```
