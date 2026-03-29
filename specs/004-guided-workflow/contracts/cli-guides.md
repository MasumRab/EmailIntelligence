# CLI Contracts: Guided Workflows (dev.py)

## Command: `guide`

**Usage**: `python dev.py guide`

**Description**: Interactive wizard that assists developers in selecting the correct orchestration workflow (rebase, sync, align).

**Inputs**:
- `--json`: (Optional) Headless mode.
- `--answers`: (Optional) Pre-answer prompts.

**Outputs**:
- stdout (Default): Rich-styled interactive prompts.
- stdout (`--json`): `{"workflow": "rebase", "reason": "Branch is 5 commits behind main"}`

## Command: `align --batch`

**Usage**: `python dev.py align --batch`

**Description**: Executes the "Multi-Branch Chess" engine to determine optimal merge order across all PRs.

**Outputs**:
- stdout (`--json`): Returns a `MergeSchedule` object containing the topological sequence and conflict risks.

## Command: `resolve --template`

**Usage**: `python dev.py resolve --template <ID>`

**Description**: Applies a pre-validated resolution pattern to a known problematic commit (e.g., fixing an incorrect folder move).

**Outputs**:
- stdout (`--json`): `{"applied": true, "strategy": "path_realignment", "commit": "sha..."}`
