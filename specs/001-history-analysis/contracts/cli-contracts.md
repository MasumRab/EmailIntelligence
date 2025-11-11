# CLI Contracts: History Analysis

**Feature**: `001-history-analysis`
**Date**: 2025-11-11

This document defines the command-line interface for the History Analysis tool.

## Command: `history-analyzer`

The main entry point for the tool.

### Sub-command: `analyze`

Analyzes the commit history and generates a description of actions.

**Usage**:
```bash
history-analyzer analyze [OPTIONS] [REVISION_RANGE]
```

**Arguments**:

- `[REVISION_RANGE]` (optional): The commit or range of commits to analyze (e.g., `HEAD~5..HEAD`, a specific branch name, a single commit SHA). If not provided, it defaults to a reasonable range, like the last 10 commits on the current branch.

**Options**:

- `--output-format <FORMAT>`: The format for the output.
  - `text` (default): Human-readable plain text.
  - `json`: Machine-readable JSON, conforming to the ActionDescription data model.
  - `md`: Markdown format.
- `--output-file <PATH>`: Path to a file to write the output to. If not provided, prints to standard output.
- `--repo-path <PATH>`: Path to the Git repository. Defaults to the current working directory.

**Example**:
```bash
history-analyzer analyze main --output-format json --output-file analysis.json
```

### Sub-command: `verify`

Verifies the consistency of an existing action description against the repository history. This is more of a conceptual command that would be integrated into the `analyze` command's logic rather than a standalone user-facing command, as the analysis itself performs the consistency check.

The primary output of the `analyze` command will include the `is_consistent` and `discrepancy_notes` fields, effectively covering the verification user story.
