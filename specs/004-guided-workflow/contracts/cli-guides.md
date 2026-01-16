# CLI Contracts: Guided Workflows

## Command: `guide-dev`

**Usage**: `python launch.py guide-dev`

**Description**: Guides the developer on which branch/workflow to use based on their intent.

**Inputs**:
- Interactive prompts (stdin): Selection between "Application Code" and "Shared Config".

**Outputs**:
- stdout: Guidance messages, warnings if on incorrect branch.

## Command: `guide-pr`

**Usage**: `python launch.py guide-pr`

**Description**: Guides the developer on the correct merge strategy.

**Inputs**:
- Interactive prompts (stdin): Selection between "Orchestration Change" and "Major Feature Merge".

**Outputs**:
- stdout: Guidance on `reverse_sync` vs `git merge`.
