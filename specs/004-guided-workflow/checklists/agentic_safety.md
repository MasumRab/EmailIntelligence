# Checklist: Agentic & Safety Requirements Quality (Orchestration Core)

## Purpose
This checklist serves as "Unit Tests for English" to validate the quality, clarity, and completeness of the agentic-first and safety requirements in the `004-guided-workflow` feature specification.

- **Status**: New
- **Created**: 2026-03-17
- **Scope**: Section XII (Agentic-First), Section XIII (Constitution First), and Safety Boundaries.

## Requirement Completeness (Agentic-First)

- [ ] CHK001 - Does every Functional Requirement (FR-001 to FR-057) include a specific JSON output schema or example? [Completeness, Spec §Requirements]
- [ ] CHK002 - Are explicit exit codes (0, 1, 2, 3+) defined for every command listed in the spec? [Completeness, Spec §Requirements]
- [ ] CHK003 - Does every User Story (US1 to US12) include a documented "Agent Interaction Flow"? [Completeness, Spec §2]
- [ ] CHK004 - Does every User Story include a documented "Failure Recovery Path" for AI agents? [Completeness, Spec §2]
- [ ] CHK005 - Are structured error response formats (`{code, message, details, hint}`) specified for all failure modes? [Completeness, Spec §Requirements]

## Requirement Clarity (Safety Boundaries)

- [ ] CHK006 - Is the list of Git operations gated by the `--enable-remote` flag explicitly specified? [Clarity, Gap]
- [ ] CHK007 - Is "ephemeral" quantified with a specific cleanup trigger (e.g., "immediately upon successful process exit")? [Clarity, Spec §Clarifications]
- [ ] CHK008 - Are the specific "prohibited patterns" for the AST scanner defined with measurable criteria? [Clarity, Spec §FR-004]
- [ ] CHK009 - Is the term "atomic write" defined with a specific implementation pattern (e.g., "write to temp + rename")? [Clarity, Spec §FR-014]
- [ ] CHK010 - Is the timeout threshold for "timeout awareness" quantified with default values (e.g., "30 seconds")? [Clarity, Spec §FR-057]

## Requirement Consistency

- [ ] CHK011 - Do the JSON schemas in the FRs align with the `contracts/cli-schema.json` base structure? [Consistency, Gap]
- [ ] CHK012 - Are the definitions of "Orchestration Core" and "Unified Cockpit" used consistently across all sections? [Consistency]
- [ ] CHK013 - Do the exit codes for conflict detection (FR-002) align with the global exit code policy in Section XII? [Consistency]

## Acceptance Criteria Quality

- [ ] CHK014 - Is the "95% accuracy" for the AST scanner (SC-005) measurable against a specific baseline or fixture set? [Measurability, Spec §Success Criteria]
- [ ] CHK015 - Can the "zero working-tree modification" constraint (SC-003) be objectively verified via Git status checks? [Measurability]
- [ ] CHK016 - Is the "under 5 seconds" performance target (SC-002) tied to a specific hardware or environment baseline? [Measurability, Gap]

## Edge Case & Exception Coverage

- [ ] CHK017 - Are requirements defined for when `.dev_state.json` is corrupted or unreadable? [Coverage, US7]
- [ ] CHK018 - Does the spec define the behavior when `ast-grep` or `gkg` external tools are missing from the PATH? [Edge Case, Gap]
- [ ] CHK019 - Are requirements specified for handling binary file conflicts in the JSON report? [Edge Case, Spec §Edge Cases]
- [ ] CHK020 - Does the spec define the rollback/cleanup behavior if a sync operation (US5) is interrupted mid-file? [Recovery, Gap]
