# Implementation Plan: CLI Unification

## Milestone 0: Discovery & Inventory (Completed)
- [x] Task 0.1: Initial remote branch triage (taskmaster, orchestration-tools, scientific)
- [x] Task 0.2: Identify core logic patterns (AST vs Shell)
- [x] Task 0.3: Map MCP and Agent Skill fragments across branches (Ported to docs/inventory/)

## Milestone 1: Foundation (Completed)
- [x] Task 1.1: SOLID Architecture Framework (Factory/Registry)
- [x] Task 1.2: Shell Script Domain Organization (`scripts/shell/`)
- [x] Task 1.3: Constitutional Analysis Fixes & Relative Import Resolution

## Milestone 2: Task & Workflow Domain (Completed)
- [x] Task 2.1: Port `taskmaster_cli.py` core logic to `src/cli/commands/task/` (d447ee6)
- [x] Task 2.2: Wrap `task_complexity_analyzer.py` and `list_tasks.py` (a8fc47f)
- [x] Task 2.3: Integrate `branch_clustering_implementation.py` for repo analysis (9d8e171)

## Milestone 3: Git & Plumbing Domain (Completed)
- [x] Task 3.1: Port `intelligent_merger.py` to `git/merge-smart` (a380c89)
- [x] Task 3.2: Port `handle_stashes.sh` logic to `git/stash-resolve` (01863e3)
- [x] Task 3.3: Implement `pr` command group from `feat-v2.0-pr` branch (af1418f)

## Milestone 4: Analysis & Semantic Domain (Completed)
- [x] Task 4.1: Integrate `NLPEngine` as a service dependency for CLI (d1ccd56)
- [x] Task 4.2: Port `import_audit.py` and `codebase_analysis.py` to `analysis/` domain (176709f)
- [x] Task 4.3: Implement `CompareCommand` enhancements for JSON reporting (verified)

## Milestone 5: Infrastructure & Automation Domain (Completed)
- [x] Task 5.1: Port `deploy.sh` and `backup.sh` logic to `infra/` command group (ed16ce6)
- [x] Task 5.2: Wrap `bottleneck_detector.py` and `resource_monitor.py` (e43407a)
- [x] Task 5.3: Consolidate `mcp.json` templates and multi-agent configs (e0a1cfc)

- [x] Task: Conductor - User Manual Verification 'Incremental CLI Unification' (FINALIZED)
