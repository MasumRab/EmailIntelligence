# Data Model: Orchestration & Scientific Core

**Version**: 1.2.0 (Aligned with Scientific Branch)

## Core Entities

### 1. Session (`src.core.models.orchestration.Session`)
Tracks the state of a long-running developer workflow (CLI side).

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique session identifier |
| `workflow` | Enum | `rebase`, `analyze`, `sync`, `scientific_resolution` |
| `status` | Enum | `active`, `paused`, `completed`, `failed` |
| `context` | Dict | Arbitrary workflow data |

### 2. Conflict (`src.core.conflict_models.Conflict`)
**Source**: Scientific Branch (`emailintelligence_cli.py`)
Represents a merge conflict with semantic understanding.

| Field | Type | Description |
|-------|------|-------------|
| `file_path` | str | Relative file path |
| `conflict_type` | Enum | `content`, `structural`, `semantic` |
| `severity` | Enum | `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |
| `resolution_strategy` | str | Suggested fix strategy |

### 3. ResolutionPlan (`src.core.conflict_models.ResolutionPlan`)
**Source**: Scientific Branch
A structured plan for resolving complex conflicts.

| Field | Type | Description |
|-------|------|-------------|
| `conflicts` | List[Conflict] | Detected conflicts |
| `strategy` | Dict | Generated resolution strategy |
| `validation_result` | ValidationResult | Outcome of pre-merge checks |

### 4. ConstitutionalRule (`src.core.models.analysis.Rule`)
Config-driven rule definition (Orchestration/Scientific Shared).

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Unique Rule ID |
| `requirements` | List[Req] | Normative statements (MUST/SHOULD) |
| `compliance_score` | float | 0.0 to 1.0 score |

### 5. CLICommand (`setup.commands.command_interface.Command`)
Interface for all `launch.py` commands.

| Field | Type | Description |
|-------|------|-------------|
| `name` | str | Command trigger |
| `args` | Namespace | Parsed arguments |
| `execute()` | Method | Main logic |