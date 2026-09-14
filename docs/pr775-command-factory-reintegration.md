# PR 775: Command/Factory Launcher Reintegration Plan

## Purpose

PR 775 must restore and repair the command/factory launcher infrastructure before it is merged. The local launch-fix branch introduced an intended command-oriented interface, but PR 775's cleanup removed the active launcher wiring while retaining much of the command implementation. This document records the regression analysis and the implementation contract for reintegration.

This is a **semantic reintegration plan**, not a request to copy the local `setup/launch.py` wholesale and not a request for a blanket branch merge.

## Executive finding

The command/factory architecture was an intended improvement:

```text
CLI command
  -> argparse subparser
  -> normalized Namespace
  -> command factory
  -> command object
  -> validate / execute
  -> centralized cleanup
```

PR 775 retained the command modules but removed the active route from `setup/launch.py`. The result is an internally inconsistent launcher:

- command modules remain in `setup/commands/`;
- `command_factory.py` remains available;
- documentation still advertises positional commands;
- the launcher no longer creates `args.command` or calls the factory;
- command-specific lifecycle and cleanup are therefore bypassed.

The correct action is to **restore and fix** the architecture, not remove it.

## Confirmed regressions to repair before merge

### 1. Dispatcher removed from `setup/launch.py`

The local implementation contained:

```python
subparsers = parser.add_subparsers(dest="command")
```

and dispatched named commands through `_execute_command()` and `get_command_factory()`.

PR 775 replaced this with flat flags and a legacy handler:

```python
if args.check or args.critical_files or args.env_check:
    return _execute_check_command(args)

return _handle_legacy_args(args)
```

There is no equivalent route for `setup`, `run`, or `test` positional commands.

**Required behavior:** support both interfaces during migration:

```text
python setup/launch.py setup
python setup/launch.py run --dev
python setup/launch.py test --unit
python setup/launch.py check
```

and existing legacy flags such as:

```text
python setup/launch.py --setup
python setup/launch.py --check
python setup/launch.py --critical-files
python setup/launch.py --env-check
```

Both forms must normalize into one canonical `argparse.Namespace` before execution.

### 2. Command lifecycle is not restored

The dispatcher must create commands through the existing factory and guarantee cleanup:

```python
command = factory.create_command(command_name, args)
if command is None:
    return 2
try:
    return command.execute()
finally:
    command.cleanup()
```

The implementation must not call cleanup from multiple competing layers. Cleanup must be idempotent so that command cleanup, launcher `finally`, signal handling, and `atexit` cannot double-terminate processes or hide the original exit status.

### 3. Container initialization was disconnected

The local launcher called:

```python
initialize_all_services(get_container())
```

PR 775 retains `setup/container.py` but no longer connects it to the launcher.

**Required behavior:** initialize the container once after parsing/normalization and before commands that require services. Pure help or validation-only paths may skip service initialization. Initialization must not be repeated merely because both legacy and command dispatch layers are present.

### 4. `TestCommand` imports a missing symbol

`setup/commands/test_command.py` imports `handle_test_stage` from `setup.test_stages`, but `setup/test_stages.py` does not define that function. It defines the `TestStages` class and `test_stages` instance.

**Required behavior:** choose one setup-facing test API and use it from both the command and legacy paths. Preferred options are:

- add a small `handle_test_stage(args) -> bool` adapter in `setup/test_stages.py`; or
- change `TestCommand` to call the canonical `test_stages` object directly.

Do not make `setup/launch.py` and `setup/commands/test_command.py` use different test-stage implementations.

### 5. Test results are discarded

The PR launcher calls `handle_test_stage(args)` and then returns success without inspecting the result.

**Required behavior:** a failed test stage must produce a nonzero process exit code. The adapter should return `bool` or an explicit result object, and the dispatcher should convert that into the documented exit status.

### 6. Service startup has two owners

PR 775 contains:

```text
setup/launch.py:start_services()
setup/services.py:start_services()
```

`RunCommand` imports `setup.services.start_services`, so launcher-only fixes are bypassed by command execution.

**Required behavior:** make `setup/services.py` the canonical service owner because command classes already import it. The launcher function should either delegate to it as a compatibility wrapper or be removed only after all callers are redirected.

All service callers must share:

- service availability checks;
- project-configured paths;
- API URL construction;
- process registration;
- process return values;
- cleanup semantics.

### 7. `setup.services.start_backend()` is currently a no-op

The PR implementation validates the Python executable and host but does not call `subprocess.Popen()` before returning.

**Required behavior:** implement backend startup in the canonical service module. The entrypoint must be obtained from authoritative project configuration; do not guess between stale `backend/...` and active `src/backend/...` layouts. The function must:

```text
construct command
  -> launch process
  -> register process exactly once
  -> return process handle
```

### 8. Process manager ownership is duplicated

PR 775 introduces a launcher-local process manager while `setup/utils.py` already owns a shared `process_manager`.

**Required behavior:** use one process manager, preferably `setup.utils.process_manager`. Every `start_*` function must return the process it starts after registration. The manager must make cleanup idempotent and tolerate already-exited processes.

### 9. Project configuration fails at import time

PR 775 contains self-referential assignments:

```python
_README_MD = _README_MD
_MAIN_PY = _MAIN_PY
```

These raise `NameError` while importing `setup.project_config`.

**Required correction:**

```python
_README_MD = "README.md"
_MAIN_PY = "main.py"
```

This must be fixed before testing any command or service path because services import project configuration.

### 10. Project paths and conflict checks are stale

PR configuration and launcher checks refer to paths such as:

```text
backend/python_backend
backend/python_nlp
backend/server-ts
```

while substantial active code exists under `src/backend/...`.

The PR conflict checker also skips nonexistent files instead of reporting a missing required path.

**Required behavior:** project configuration is the single source of truth. Required paths must report missing configuration/path errors; only genuinely optional services may be skipped. Conflict checking must distinguish:

```text
required path missing
optional path missing
file scanned and clean
file scanned and conflict detected
```

### 11. Test-stage modules are split

The launcher imports `deployment.test_stages`, while the command path imports `setup.test_stages`. They differ in executable selection, test scope, and environment assumptions.

**Required behavior:** create or standardize a setup-facing adapter used by both the launcher and `TestCommand`. Keep deployment-specific behavior in `deployment.test_stages`; do not make the setup launcher depend on deployment-only `uv run` assumptions.

### 12. Python policy is contradictory

Current policies disagree:

```text
setup/launch.py: Python 3.12–3.13
setup/validation.py: Python 3.11–3.12
setup/pyproject.toml: >=3.11
CI: Python 3.12
```

**Required behavior:** select one supported range and align launcher checks, shared validation, metadata, CI, and documentation. Do not leave Python 3.11 metadata-supported but launcher-rejected, or Python 3.13 launcher-accepted but shared-validation-rejected.

## Dependency and packaging findings

The following files are unchanged between the local branch and PR 775:

```text
setup/requirements.txt
setup/requirements-dev.txt
```

No requirements-file restoration is required. The dependency regressions are in installation behavior and project metadata:

1. The launcher directly installs `torch`, `torchvision`, and `torchaudio`, but metadata declares only `torch`.
2. The launcher changed from a fuller editable/dev installation to `uv pip install -e .`, which can omit optional groups.
3. The `full` optional dependency is self-referential through `emailintelligence[...]`.

Before merge:

- define explicit `core`, `dev`, and `full` profiles;
- install the intended profile from the launcher;
- declare every directly required Torch package or remove undeclared direct installs;
- replace the self-referential `full` extra with direct supported composition;
- ensure the selected profile covers runtime imports represented in `setup/requirements.txt`.

## Command contracts

### `Command` base contract

Every command must provide:

```text
validate_args() -> bool
execute() -> int
cleanup() -> None
get_description() -> str
```

The base class should make cleanup safe to call more than once. `execute()` must not silently swallow deterministic configuration errors.

### Factory contract

`CommandFactory.create_command(name, args)` must:

- return the correct command class for every supported command;
- return `None` for an unknown command;
- never perform command execution itself;
- accept the normalized Namespace shape;
- expose available commands for help/documentation generation.

The factory mapping must remain the single command registry; do not duplicate command-name dispatch in `setup/launch.py`.

### Launcher dispatch contract

The launcher should follow this order:

```text
parse CLI
  -> normalize positional/legacy arguments
  -> handle help/version-only requests
  -> validate command/arguments
  -> initialize container if required
  -> factory.create_command()
  -> command.execute()
  -> command.cleanup() exactly once
```

Legacy handlers may remain for backward compatibility, but they must delegate to the same canonical service, validation, environment, test-stage, and process-manager modules.

### `run` contract

`RunCommand` must:

1. call `validate_args()`;
2. prepare the selected environment;
3. validate configured services;
4. call canonical `setup.services.start_services()`;
5. keep the process alive only when invoked as a foreground command;
6. handle interrupt/shutdown;
7. clean up via the shared process manager;
8. return a deterministic exit code.

It must not import a second service implementation or leave cleanup to accidental interpreter exit.

### `test` contract

`TestCommand` must:

1. call `validate_args()`;
2. select requested stages;
3. invoke the setup-facing canonical test adapter;
4. return failure when any requested stage fails;
5. preserve coverage/debug/continue-on-error semantics;
6. never import a symbol that does not exist.

### `check` contract

`CheckCommand` and legacy `--check` flags must share:

- critical-file discovery;
- project layout validation;
- merge-conflict marker scanning;
- environment validation;
- exit-code behavior.

## Implementation sequence

Implement in this order to avoid repairing callers before their dependencies are valid:

1. Fix `setup/project_config.py` constants and establish authoritative project paths.
2. Consolidate `setup/utils.py`, `setup/environment.py`, and `setup/validation.py` ownership.
3. Make `setup/services.py` canonical and implement backend startup/process returns.
4. Standardize the setup-facing test-stage adapter.
5. Normalize command and legacy CLI arguments.
6. Restore subparsers and factory dispatch in `setup/launch.py`.
7. Reconnect container initialization.
8. Repair command lifecycle and idempotent cleanup.
9. Correct dependency profiles, Torch metadata, Python policy, and Ruff suppressions.
10. Repair PR-only application and workflow regressions separately.

Do not use blanket `ours`, `theirs`, restore, reset, or wholesale file replacement to perform this work.

## Verification gate before PR merge

The PR must not merge until all of the following are demonstrated:

### CLI surface

```bash
python setup/launch.py --help
python setup/launch.py setup --help
python setup/launch.py run --help
python setup/launch.py test --help
python setup/launch.py check --help
```

Both positional commands and supported legacy flags must parse successfully.

### Factory coverage

For every registered command:

- the factory creates the expected class;
- invalid command names produce a controlled nonzero result;
- command cleanup runs on success and failure;
- no command imports a nonexistent symbol.

### Service lifecycle

Using mocked subprocesses or a safe dry-run seam:

- backend startup reaches `Popen`;
- every started process is registered once;
- process handles are returned;
- cleanup is idempotent;
- command and legacy paths use the same service owner.

### Test failure propagation

A controlled failing test-stage result must produce a nonzero launcher/command exit code. A successful stage must produce zero.

### Configuration

- importing `setup.project_config` succeeds;
- required configured paths are validated;
- stale/missing required paths are reported;
- conflict markers are detected in configured critical files.

### Dependency policy

- selected installation profile resolves without self-reference;
- direct runtime dependencies are represented in metadata;
- launcher, metadata, CI, and documentation agree on Python support.

### Runtime regressions outside launcher

Before merge, separately verify and repair:

- `EmailSourceNode` implements the abstract `execute()` contract;
- `HTTPException` status codes are not converted into generic 500 responses;
- CI/security checks do not silently swallow required failures;
- frontend checks run from the correct working directory;
- root/client dependency audits inspect the correct lockfiles and trees.

## Merge decision

PR 775 should be treated as **not merge-ready** until the command/factory infrastructure is restored and the above contracts are satisfied. The desired result is:

```text
PR 775 valid cleanup
  + restored command/factory dispatch
  + canonical shared lifecycle modules
  + container initialization
  + correct service/test ownership
  + explicit dependency/profile policy
  + failure propagation
  - duplicate implementations
  - stale paths
  - invalid constants
  - self-referential extras
  - swallowed failures
```
