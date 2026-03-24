# Proposal: Python CLI Subprocess Abstraction

## 1. Executive Summary
Currently, several commands in the `EmailIntelligence` native CLI (`dev.py`) execute raw shell commands via `subprocess.run()`. This creates fragility, makes unit testing difficult, and tightly couples the logic to the host operating system. This plan proposes refactoring these calls into Abstract Service Interfaces injected via the existing Dependency Injection (DI) container.

## 2. Tooling & Installation Sources
*Per project guidelines, all tooling sources are explicitly defined below.*

*   **Python Standard Library**: `subprocess`, `abc` (Abstract Base Classes)
    *   *Source*: Native Python 3.11+ environment. No external installation required.
*   **Code Review Extension** (Used for validating the refactor)
    *   *Source*: Gemini Extension
    *   *Repository*: [https://github.com/gemini-cli-extensions/code-review](https://github.com/gemini-cli-extensions/code-review)
*   **Conductor Extension** (Used for tracking this plan)
    *   *Source*: Gemini Extension
    *   *Repository*: [https://github.com/gemini-cli-extensions/conductor](https://github.com/gemini-cli-extensions/conductor)

## 3. Implementation Plan

### Phase 1: Interface Definition
- [ ] Define `IShellExecutor` in `src/cli/services/interfaces.py`.
- [ ] Implement `StandardShellExecutor` wrapping `subprocess.run` with global timeout and error handling logic.

### Phase 2: Domain-Specific Services
- [ ] Create `GitOpsService` extending the shell executor for Git-specific commands.
- [ ] Create `LinterService` for executing ecosystem tools (Ruff, isort).

### Phase 3: Dependency Injection
- [ ] Update `src/cli/main.py` to instantiate `StandardShellExecutor`, `GitOpsService`, and `LinterService`.
- [ ] Inject these services into the `CommandRegistry` dependencies payload.

### Phase 4: Command Refactoring
- [ ] Refactor `ImportAuditCommand` to use `LinterService` instead of raw subprocess calls.
- [ ] Refactor `MergeSmartCommand` to use `GitOpsService` for fetching merge bases and file content.
- [ ] Refactor `GitDiscoverCommand` to use `GitOpsService` for branch traversal.

## 4. Verification Strategy
- Develop `MockShellExecutor` for the test suite.
- Verify that `pytest` can execute all CLI command logic without actually calling the host shell.
