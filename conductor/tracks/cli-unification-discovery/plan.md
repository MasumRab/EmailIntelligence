# Implementation Plan: Missing Functionality

## Milestone 0: Semantic Remote Discovery
- [x] Task 0.1: Implement `git-discover` command with semantic intent detection to find out-of-scope remote tooling.
- [x] Task 0.2: Integrate `NLPService` fuzzy matching to classify remote branch DNA against core EmailIntelligence scope.

## Milestone 1: Automated Normalization (Critical Infra)
- [x] Task 1.1: Implement `ImportAuditCommand` --fix logic for 'backend' vs 'src.backend' normalization using AST/LibCST.
- [x] Task 1.2: Implement robust path correction for consolidated scripts (Superceded by LibCST refactor).

## Milestone 2: Task Intelligence Porting
- [x] Task 2.1: Port `TaskDeduplicator` logic to `task-generate` command.
- [x] Task 2.2: Port relationship building logic to `task-analyze` command.

## Milestone 3: Repository Governance
- [x] Task 3.1: Port `ArchitecturalRuleEngine` concepts to `import-audit` (Contract Validator).
- [x] Task 3.2: Port dangling commit recovery scripts to `git-history` domain.

## Milestone 4: Agent & Performance Integration
- [x] Task 4.1: Integrate `AgentHealthMonitor` into `sys-monitor` command.
- [x] Task 4.2: Wrap `resource_monitor.py` advanced metrics into CLI services (`sys-monitor`).

## Phase: Review Fixes
- [x] Task: Apply review suggestions edf22565
