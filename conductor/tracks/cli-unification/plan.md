# Implementation Plan: CLI Unification

## Milestone 0: Discovery & Inventory (Active Growth)
- [x] Task 0.1: Initial remote branch triage (taskmaster, orchestration-tools, scientific)
- [x] Task 0.2: Identify core logic patterns (AST vs Shell)
- [x] Task 0.3: Map MCP and Agent Skill fragments across branches (Ported to docs/inventory/)
- [x] Task 0.4: Rigorous DNA Scan (logic-compare) of all remote scripts (Completed via logic-compare command)

## Milestone 1: Foundation (Completed)
- [x] Task 1.1: SOLID Architecture Framework (Factory/Registry)
- [x] Task 1.2: Shell Script Domain Organization (`scripts/shell/`)
- [x] Task 1.3: Constitutional Analysis Fixes & Relative Import Resolution

## Milestone 2: Task & Workflow Domain (Expanded Discovery)
- [x] Task 2.1: Port `taskmaster_cli.py` core logic (d447ee6)
- [x] Task 2.2: Wrap `task_complexity_analyzer.py` and `list_tasks.py` (a8fc47f)
- [x] Task 2.3: Integrate `branch_clustering_implementation.py` (9d8e171)
- [x] Task 2.4: Port missing `TaskDeduplicator` logic from `orchestration-tools` (Implemented in task-generate)
- [x] Task 2.5: Integrate `backlog/relationships` logic for task linking (Implemented in task-analyze)

## Milestone 3: Git & Plumbing Domain (Expanded Discovery)
- [x] Task 3.1: Port `intelligent_merger.py` (a380c89)
- [x] Task 3.2: Port `handle_stashes.sh` logic (01863e3)
- [x] Task 3.3: Implement `orch-extract` command (af1418f)
- [x] Task 3.4: Port `find_lost_files` and dangling commit recovery logic (Implemented in analyze-history)

## Milestone 4: Analysis & Semantic Domain
- [x] Task 4.1: Integrate `NLPEngine` as a service dependency (d1ccd56)
- [x] Task 4.2: Port codebase and import audit tools (176709f)
- [x] Task 4.3: Implement `ImportAuditCommand` auto-fix (--fix) logic (Implemented in import-audit --fix)

## Milestone 5: Infrastructure & Automation Domain
- [x] Task 5.1: Port `deploy.sh` and `backup.sh` logic (ed16ce6)
- [x] Task 5.2: Wrap monitoring tools (e43407a)
- [x] Task 5.3: Consolidate `mcp.json` templates (e0a1cfc)
- [x] Task 5.4: Implement project-specific agent scaffolding (47debbf)

- [ ] Task: Conductor - User Manual Verification 'Rigorous CLI Unification'
