# CLI Production Readiness Plan

This roadmap acts as the shared plan across all CLI-consolidation sessions to ensure `consolidate/cli-unification` becomes fully implemented and portable.

## The Goal
The canonical branch `consolidate/cli-unification` must contain a fully implemented, portable unified CLI. 
- All domain commands (git, task, analysis, infra, automation, agent) must be functional.
- Zero stubs.
- Portable: Importable into either `scientific` or `main`.
- CLI commands must NOT directly import branch-specific backend modules. All integration must occur through `create_default_dependencies`.

## Roadmap Tasks (Lane Assignments)

### Lane: Dependencies & Framework [OWNER: Dependencies Session]
1. **Fix Missing Dependencies**: Add `libcst`, `networkx`, `psutil` to `pyproject.toml` safely. *(COMPLETED: PR #838)*
2. **Resolve Argument Collisions**: Remove duplicate/conflicting `-f` and `--format` flag mappings across `import_audit.py`, `topology.py`, and `conflict_bisect.py`.
3. **Lazy Import Architecture**: Ensure commands like `import_audit` dynamically `import libcst` internally during `execute()`, not at the module level, preventing missing dependency crashes on environments that don't need those specific tools.

### Lane: AI Constitutional Reconstruction [OWNER: Architecture/AI Session]
1. **Patch `src/resolution/__init__.py`**: Fix dataclass ordering to prevent `NameError`.
2. **Dynamic Rule Loading**: Rewrite `_load_default_constitution` in `ConstitutionalEngine` to parse YAML constraints from `rules/` or `.agent/rules/` rather than returning a hardcoded `security-001` dummy rule.
3. **Wire `git-auto-resolve` Workflow**: Deprecate the monolithic `emailintelligence_cli.py`. Reconstruct its multi-phase workflow (`setup -> load rules -> strategy -> align -> validate`) securely within `src/cli/commands/git/auto_resolve.py` using injected `WorktreeManager` and `ConstitutionalEngine` dependencies.

### Lane: State & Workflow Persistence [OWNER: Framework Session]
1. **Wire State Handoff**: Inject `CLIState` into `AnalyzeCommand` and `ResolveCommand`.
2. **Test Context Continuity**: Write integration tests ensuring that running `git-analyze` on a specific branch naturally persists the target to `~/.cli_state.json`, allowing `git-resolve` to pick it up automatically.

### Lane: Orchestration Absorption [OWNER: Orchestration/Absorption Session]
1. **Absorb `launch.py` Flows**: Map `orchestration-tools`'s `setup/launch.py` environment bootstrapping logic. Do not duplicate it. Ensure the unified CLI can be invoked *as a shared service* by `launch.py` during system startups.
2. **Salvage Reporting Engines**: Adapt the HTML/JSON generation tools from `scripts/orchestration/align/cli.py` and `src/validation/reporting_engine.py` into a unified `cli workflow report` command.

### Lane: Portability Verification [OWNER: Architecture Session]
1. **Dependency Injection Audit**: Scan `src/cli/commands/` to ensure zero direct `import src.backend` or `import src.analysis` calls exist at module level.
2. **Main/Scientific CI Verification**: Validate that pulling `src/cli` into `main` passes all unit tests and successfully instantiates `create_default_dependencies()` using `main`'s backend layout.
