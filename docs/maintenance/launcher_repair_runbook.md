# Launcher Repair Runbook: Adaptive Recovery Framework

This runbook provides a structured approach for repairing, maintaining, and evolving the EmailIntelligence Unified Launcher (`setup/launch.py`). It emphasizes infrastructure integrity, conflict resolution, and automated validation.

---

## 1. The Infrastructure Core

The launcher's reliability depends on its ability to establish a stable execution environment even when the surrounding codebase is in a state of flux.

### ROOT_DIR & Path Integrity
All operations must be relative to the project root. The launcher establishes this using:
```python
# setup/launch.py
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
```
**Warning:** Do not move `setup/launch.py` without updating the `.parent` chain. If the script is relocated to the root, it should be `Path(__file__).resolve().parent`.

### sys.path Management
To ensure that project-wide modules (like `setup.utils`) are always importable:
```python
import sys
sys.path.insert(0, str(ROOT_DIR))
```

### Protected & Deferred Imports
To prevent "Bootstrap Paradoxes" (where the launcher fails to start because of a broken dependency it's meant to fix):
1.  **Optional Dependencies:** Wrap top-level imports in `try-except` blocks.
    ```python
    try:
        from dotenv import load_dotenv
        DOTENV_AVAILABLE = True
    except ImportError:
        DOTENV_AVAILABLE = False
    ```
2.  **Heavy/Unstable Modules:** Use "deferred imports" inside functions. This prevents the launcher from crashing on startup if a specific service or dependency (like `torch` or `nltk`) is missing.
    ```python
    def setup_dependencies(venv_path: Path):
        from setup.environment import setup_dependencies as env_setup_deps
        env_setup_deps(venv_path)
    ```

---

## 2. 3-Way Conflict Guide

When merging the `orchestration-tools` branch or other feature-heavy branches, conflicts in `setup/launch.py` are common.

### Global vs. Branch-Specific Logic
*   **Global Flags:** All shared launcher flags must be added in the `_add_Legacy Component - Maintained for Backward Compatibility_args(parser)` function to ensure backward compatibility.
*   **Feature Flags:** Branch-specific flags should be isolated to their own argument groups if possible.

### Automated Conflict Detection
Before running repairs, use the built-in validation tool to find unresolved Git markers:
```bash
python3 -c "from setup.validation import check_for_merge_conflicts; check_for_merge_conflicts()"
```
This utility scans critical files (defined in `setup/project_config.py`) for `<<<<<<<`, `=======`, and `>>>>>>>`.

### Resolution Strategy
1.  **Identify Infrastructure Changes:** Prioritize keeping the "Infrastructure Core" (imports, paths) clean.
2.  **Consolidate Args:** If two branches add similar flags, consolidate them in `_add_Legacy Component - Maintained for Backward Compatibility_args`.
3.  **Preserve the Dispatcher:** Ensure `main()` always points to `_handle_Legacy Component - Maintained for Backward Compatibility_args(args)`, which acts as the primary dispatcher.

---

## 3. Local Context Preservation

The launcher is designed to respect individual developer environments without polluting the global repository state.

### User Configuration Files
*   **`launch-user.env` (High Priority):** This file is loaded first. Use it for machine-specific overrides (e.g., custom database URLs, local API keys).
    *   *Note: This file is excluded via `.gitignore` (matching the `*.env` pattern) to prevent accidental commits of local secrets.*
*   **`.env` (Standard):** Used for project-wide defaults.

### Isolating Feature Blocks
When adding new feature logic:
1.  Check for the existence of local config before applying overrides.
2.  Use the `args.env_file` flag to allow users to specify custom environments without modifying the source code.
3.  Ensure that new flags default to "safe" values that don't interfere with existing `dev` or `test` stages.

---

## 4. Syntax & Validity Shield

After any repair or manual edit, you must verify the script's integrity before attempting execution.

### The `py_compile` Check
Run a byte-code compilation check to catch syntax errors, indentation issues, or missing imports:
```bash
python3 -m py_compile setup/launch.py
```
**Verification:** Ensure this command exits with a zero (0) exit code. If it throws an exception or returns a non-zero exit status, the script is broken and will fail to execute.

### Orchestration Validation
Run the full orchestration test suite to ensure broader system compatibility:
```bash
bash scripts/test_orchestration.sh
```
Specifically, look for the `[PASS] Setup File Syntax` result, which automates the `py_compile` check across all files in the `setup/` directory.

### Post-Repair Checklist
- [ ] `ROOT_DIR` resolves to the project root.
- [ ] No unresolved merge markers in `setup/launch.py`.
- [ ] `python3 -m py_compile setup/launch.py` returns 0.
- [ ] `launch-user.env` remains uncommitted and unaffected.
