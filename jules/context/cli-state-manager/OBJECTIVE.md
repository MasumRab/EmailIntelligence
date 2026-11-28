# Objective

Extract and restore the standalone CLI state manager and git analysis commands (`branch_health` and `conflicts`) that were built in feature branches but are missing on `main`, enabling core CLI infrastructure.

## Verifiable End State Checklist

- [ ] `src/cli/state.py` exists and exposes `CLIStateManager`.
- [ ] `src/cli/commands/git/branch_health.py` exists and exposes `BranchHealthCommand`.
- [ ] `src/cli/commands/git/conflicts.py` exists and exposes `ConflictsCommand`.
- [ ] A verification script can import all three components successfully without errors.
