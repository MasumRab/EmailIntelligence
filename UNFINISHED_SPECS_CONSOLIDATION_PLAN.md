# Plan: Unfinished Specification Consolidation (End-to-End)

## Overview
This plan outlines the multi-phase strategy for identifying, organizing, and consolidating all unfinished technical specifications and partial implementations across the EmailIntelligence repository (excluding `004-*`). The goal is to migrate these orphaned artifacts into a unified structure based on the **Speckit Phase 0-2 Framework** found in branch `001-pr176-integration-fixes`.

---

## Phase 1: Forensic Spec Inventory & DNA Extraction
**Objective**: Identify every "Unfinished" spec fragment and its functional "DNA" across all branches.

### Tasks
- [x] **1.1 Global Spec Crawl**: Identify `specs/` directories and `.taskmaster/tasks/*.md` files (Completed via recent scans).
- [x] **1.2 Status Triage**: Filter for tasks/specs marked with `[ ]` (Pending) or `[~]` (In Progress) (Completed via recent grep).
- [ ] **1.3 Requirement Extraction**: Extract "Phase 0: Research" questions and answers from the `001-pr176` branch to serve as the baseline for cross-branch requirements.
- [x] **1.4 Rebase Discovery**: Isolate the 17 pending tasks (T001-T017) from `001-rebase-analysis` (Completed).

---

## Phase 2: Alignment with "Specify" target (00176 Branch)
**Objective**: Standardize all discovered fragments into the project's most mature 14-section format.

### Tasks
- [ ] **2.1 Template Application**: Apply the `001-pr176-integration-fixes` specification template to all legacy `specs/*.md` files.
- [ ] **2.2 Data Model Consolidation**: Merge the `data-model.md` from `001-rebase-analysis` (Commit/Intention models) with the PR integration models in `00176`.
- [ ] **2.3 Partial Implementation Mapping**: Identify `.py` or `.sh` files that correspond to these specs (e.g., `rebase_detector.py` stubs) and document their "Partial" status.

---

## Phase 3: Logic-to-Spec Gap Analysis
**Objective**: Verify if "Unfinished Specs" actually have existing implementation code in other branches.

### Tasks
- [ ] **3.1 DNA Match Run**: Use `dev.py logic-compare` to check if functions defined in "Unfinished Specs" are already implemented in `orchestration-tools` or `scientific`.
- [ ] **3.2 Implementation Verification**: For every `[x] COMPLETED` task found, verify that the corresponding code exists in the `src/` directory.
- [ ] **3.3 Dependency Audit**: Use `import-audit` to map the dependencies required by these unfinished specs.

---

## Phase 4: Scaffolding & Implementation Readiness
**Objective**: Prepare the unified CLI branch to receive the implementation of these specs.

### Tasks
- [ ] **4.1 Module Stubbing**: Create the missing service stubs identified in `001-rebase-analysis` (e.g., `src/services/rebase_analyzer.py`).
- [ ] **4.2 CLI Command Mapping**: Map every "High Priority" unfinished spec to a planned modular CLI command (e.g., `git-rebase-verify`).
- [ ] **4.3 Backlog Unification**: Use `task-generate` to merge all orphaned tasks into a single, unified `tasks.json`.

---

## Storage & Portability
- **Primary Source**: `agent/rules/` (for agent-led execution).
- **Plan Location**: `/home/masum/github/EmailIntelligenceGem/UNFINISHED_SPECS_CONSOLIDATION_PLAN.md`
- **Metadata**: Each spec must be tagged with its `source_branch` and `extraction_date`.

## Timeline & Priority
1. **Priority 1**: Rebase & Topology Specs (from `001-rebase-analysis`).
2. **Priority 2**: PR Resolution Framework (from `00176`).
3. **Priority 3**: Orchestration Logic (from `orchestration-tools`).
