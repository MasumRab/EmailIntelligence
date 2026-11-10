# Task 014.5: Integrate Visual Diff Tools

**Status:** specified
**Priority:** high
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** 014.4

---

## Overview/Purpose

A visual diff is optional tooling, and the requirement here is that the framework degrades cleanly
when it is absent -- CI and a headless session must not be blocked by a missing GUI tool.

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 014.4

### Blocks (What This Task Unblocks)
- [ ] To be defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 014.5
- **Title**: Integrate Visual Diff Tools
- **Status**: pending
- **Priority**: high
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The configured difftool is read from git config (`git config --get diff.tool`), not hard-coded, so
   the framework honours the operator's choice.
2. When no difftool is configured or the tool is not on `PATH`, the framework prints the command to
   configure one and continues; it does not fail the run.
3. Invocation is `git difftool --dir-diff` with an explicit `--no-prompt` or an equivalent single-shot
   mode, so an interactive tool cannot hang a batch run.
4. The tool's exit status is reported but does not change the pipeline's verdict; viewing is not
   resolving.

## Implementation Guide

Implement in the guide subcommand. Check availability before invoking:

```bash
git config --get diff.tool; echo "exit=$?"
command -v meld || command -v kdiff3 || echo "no difftool on PATH"
git difftool --dir-diff --no-prompt <base> <head>
```

Test the absent-tool path by unsetting `diff.tool` and confirming the run continues with a message.


### 014.5. Integrate Visual Diff Tools

**Effort:** 6-8 hours
**Depends on:** 014.4

**Steps:**
1. Create visual diff tool interface
2. Implement tool detection and configuration
3. Add tool-specific command generation
4. Create fallback mechanisms for tool failures
5. Add user preference configuration

**Success Criteria:**
- [ ] Visual diff tool interface implemented
- [ ] Tool detection and configuration operational
- [ ] Tool-specific commands generated
- [ ] Fallback mechanisms functional
- [ ] User preferences configurable

---


## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

## Performance Targets

- **Effort Range**: TBD
- **Complexity Level**: TBD

## Testing Strategy

Test strategy to be defined

## Common Gotchas & Solutions

- [ ] No common gotchas identified

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

## Done Definition

### Completion Criteria
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated

## Next Steps

- [ ] Next steps to be defined
