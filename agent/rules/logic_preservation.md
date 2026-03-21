---
name: logic-preservation-and-restoration
description: Mandatory workflow for ensuring 100% functional parity and preventing "mass deletion" regressions during porting.
---

# Logic Preservation & Restoration Workflow

This rule ensures that when porting legacy logic to the modular CLI, no previous functionality or "DNA" is lost.

## Mandatory Process

### 1. The Pre-Edit Audit
Before editing any file in `src/cli/commands/`:
- **Read Current**: Read the target file to identify logic already implemented.
- **Read Source**: Read the original script from the remote branch.
- **Map Gaps**: List exactly which functions/patterns are missing.

### 2. Surgical Implementation
- **Prefer `replace`**: Use the `replace` tool for targeted injections instead of `write_file` for the whole class.
- **Preserve Regex**: Never simplify regex patterns from the source; port them with 100% fidelity.
- **Maintain Metadata**: Ensure `source_file`, `priority`, and other metadata fields are never dropped.

### 3. The Forensic Verification (The Gatekeeper)
Before announcing completion:
- Run `python3 dev.py logic-compare <original_source> <new_implementation>`.
- If "Dropped Functions" > 0, you **MUST NOT** commit.
- You must surgically restore every dropped function until the parity is verified.

## Anti-Patterns to Avoid
- **Mass Overwrites**: Replacing an entire file and losing incremental work from previous turns.
- **Logic Stubs**: Using `print` or `return 0` where complex logic previously existed.
- **Name Collisions**: Forgetting to map `self._private_method` to the original `global_function` in the compare tool.
