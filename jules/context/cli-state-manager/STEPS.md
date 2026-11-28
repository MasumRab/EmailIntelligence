# Steps

## 1. Extract CLI State and Commands
- **Files to change:** 
  - `src/cli/state.py` (Create)
  - `src/cli/commands/git/branch_health.py` (Create)
  - `src/cli/commands/git/conflicts.py` (Create)
- **Diff budget:** 3 files created, 0 lines deleted.
- **Verification command:**
  ```bash
  python3 -c "import sys; sys.path.insert(0, '.'); from src.cli.state import CLIStateManager; from src.cli.commands.git.branch_health import BranchHealthCommand; from src.cli.commands.git.conflicts import ConflictsCommand; print('Success!')"
  ```
- **Expected output:** `Success!`
- **Done when:** The files exist, the verification script is red-on-main and green-on-branch (printing `Success!`), and it is committed and pushed cleanly.
