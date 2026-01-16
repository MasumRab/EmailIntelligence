# Requirements Quality Checklist: backend_frontend

**Purpose**: Validate quality of requirements for both backend logic engines and CLI/IDE frontend components
**Created**: 2026-01-14
**Feature**: [specs/004-guided-workflow/spec.md](../spec.md)

## Requirement Completeness
- [ ] CHK001 - Are requirements defined for all `git merge-tree` failure modes (e.g., malformed trees, unsupported plumbing versions)? [Completeness, Gap]
- [ ] CHK002 - Is the structured JSON violation report schema (Rule, File, Line, Snippet) explicitly defined for US6? [Completeness, Spec §FR-015]
- [ ] CHK003 - Are rollback requirements defined for failed `dev.py sync` operations when overwriting local files? [Completeness, US5]
- [ ] CHK004 - Does the spec define how the AST Scanner handles multi-file dependencies during constitutional enforcement? [Completeness, US4]
- [ ] CHK005 - Are requirements specified for handling "Stale Session" TTLs in `.dev_state.json` to prevent recovery from obsolete Git states? [Completeness, US7]

## Requirement Clarity
- [ ] CHK006 - Is the "Token-Saver" mode quantified by specific character suppression rules or MIME-type equivalents? [Clarity, Spec §FR-011]
- [ ] CHK007 - Is the term "topological sorting" clarified with expected behavior for disconnected commit components? [Clarity, Spec §FR-003]
- [ ] CHK008 - Are the interactive multi-select criteria for `dev.py sync` explicitly defined (e.g., sorting by timestamp vs. directory)? [Clarity, Spec §FR-016]

## Requirement Consistency
- [ ] CHK009 - Do the Pydantic models in the data model align with the structured JSON report requirements in FR-015? [Consistency, Gap]
- [ ] CHK010 - Is the headless `--json` mode consistent across all subcommands, including those with mandatory interactive answers? [Consistency, Spec §FR-009]

## Acceptance Criteria Quality
- [ ] CHK011 - Can "100% accuracy" in SC-001 be objectively verified against complex non-linear Git histories? [Measurability, Spec §SC-001]
- [ ] CHK012 - Can the performance target of "<5 seconds" be measured in a standardized CI environment? [Measurability, Spec §SC-002]

## Scenario Coverage
- [ ] CHK013 - Are requirements defined for the "Diverged Remotes" edge case when performing history analysis? [Coverage, Spec §Edge Cases]
- [ ] CHK014 - Are requirements specified for "Disconnected/Headless" operation where no TTY is available? [Coverage, US6]
- [ ] CHK015 - Is the behavior specified for the `ide-init` command if an existing `.vscode/tasks.json` already contains user-defined tasks? [Coverage, FR-010]

## Non-Functional Requirements
- [ ] CHK016 - Are security requirements defined for the AST scanner to prevent malicious code injection via `constitution.md` custom rules? [Security, Gap]
- [ ] CHK017 - Is the "Atomic" nature of FR-014 quantified by filesystem sync (fsync) or transactional write requirements? [Reliability, FR-014]

## Ambiguities & Conflicts
- [ ] CHK018 - Does the "NO STUBS" requirement in FR-006 conflict with the need for test mocks in ephemeral repository isolation? [Conflict, FR-006]
- [ ] CHK019 - Is the distinction between "Logic in scripts/" and "Orchestration Tooling" defined clearly enough for the AST scanner to distinguish? [Ambiguity, US4]
- [ ] CHK020 - Does the `ide-init` command requirements specify support for IDEs other than VS Code? [Ambiguity, FR-010]
