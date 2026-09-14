# EmailIntelligence CLI Retirement Plan

## Current State & Gap Analysis
`emailintelligence_cli.py` is the legacy monolith that currently hard-entangles CLI routing with the `src.resolution` engine logic.
It suffers from `NameError` and missing references out-of-the-box due to structural drift, making it unmaintainable.

## Migration Strategy
The capabilities within the monolith will be entirely subsumed by the unified `src/cli/main.py` entrypoint and the `CommandRegistry`.

### Capability Mapping
- `setup-resolution` -> `src/cli/commands/resolve_command.py` (via unified Dependency Injection)
- `analyze-constitutional` / `analyze-governance` -> `src/cli/commands/analyze_command.py`
- `develop-spec-kit-strategy` -> Migrates to the Resolution Planner under `src/resolution/` bound via `CommandFactory`
- `align-content` / `auto-resolve` -> `src/cli/commands/git/align.py` & `auto_resolve.py`
- `validate-resolution` -> `src/cli/commands/validate_command.py`

### Dependency Injection Boundary
Instead of direct imports inside the CLI script, all resolution-engine integration will occur strictly through `create_default_dependencies()` in `src/cli/commands/integration.py`. This factory will inject the `ConflictDetector`, `ResolutionPlanner`, and `AutoResolver` into the instantiated commands, completely isolating the CLI from the backend implementation details.

## Final Action
Once all domain commands are verified portable and functional via `python src/cli/main.py`, `emailintelligence_cli.py` will be safely deleted.
