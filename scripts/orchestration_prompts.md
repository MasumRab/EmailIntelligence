# Orchestration Scripts Prompts for LLM Agents

This document provides detailed, step-by-step prompts for naive/simple LLM agents to execute orchestration tasks. Each prompt includes context, steps, and validation.

## 1. Check Orchestration Changes

**Task**: Verify that changes in the current branch only affect orchestration-managed files.

**Prompt**:
```
You are an orchestration assistant. Your task is to check if the current working directory has any changes that are NOT in the list of orchestration-managed files.

Orchestration-managed files are:
- setup/launch.py
- setup/launch.bat
- setup/launch.sh
- scripts/sync_setup_worktrees.sh
- .flake8
- .pylintrc
- tsconfig.json
- package.json
- tailwind.config.ts
- vite.config.ts
- drizzle.config.ts
- components.json
- .gitignore
- .gitattributes

Steps:
1. Run: git diff --name-only
2. For each file in the output, check if it is in the orchestration-managed list above.
3. If any file is NOT in the list, report it as an error.
4. If all files are in the list or no changes, report success.

Output format:
- List any non-managed files found.
- Say "SUCCESS" if only managed files changed, "ERROR" if not.
```

## 2. Isolate Orchestration Changes

**Task**: Create a patch file containing only changes to orchestration-managed files from a source.

**Prompt**:
```
You are an orchestration assistant. Your task is to create a patch file with only the changes to orchestration-managed files from a given source.

Source can be a branch name (e.g., "main") or a path to a directory (e.g., "../worktree").

Orchestration-managed files are:
- setup/launch.py
- setup/launch.bat
- setup/launch.sh
- scripts/sync_setup_worktrees.sh
- .flake8
- .pylintrc
- tsconfig.json
- package.json
- tailwind.config.ts
- vite.config.ts
- drizzle.config.ts
- components.json
- .gitignore
- .gitattributes

Steps:
1. Determine if source is a directory path (check if it exists as directory) or a branch/commit.
2. For each orchestration-managed file:
   - If source is a directory: Compare the file in current dir vs source dir using git diff --no-index
   - If source is a branch: Get diff from git diff <source> -- <file>
3. Collect all diffs into a single patch file named "orchestration_changes_YYYYMMDD_HHMMSS.patch"
4. If no changes found, report that no patch was created.

Output: Confirmation of patch creation or no changes message.
```

## 3. Apply Orchestration Patch

**Task**: Apply a patch file containing orchestration changes to the current branch.

**Prompt**:
```
You are an orchestration assistant. Your task is to apply a patch file to the current Git repository.

Steps:
1. Check if the patch file exists.
2. Run: git apply --check <patch_file>
3. If check passes, run: git apply <patch_file>
4. Report success or any conflicts.

Output: Success message or error details.
```

## 4. Sync Orchestration Changes

**Task**: Combine isolation and application of orchestration changes from a source in one operation.

**Prompt**:
```
You are an orchestration assistant. Your task is to sync orchestration changes from a source by isolating them into a patch and applying it.

Source can be a branch or path.

Steps:
1. Isolate changes from source (see Isolate prompt).
2. If patch created, apply it (see Apply prompt).
3. Clean up patch file if desired.
4. Report completion.

Output: Sync result summary.
```

## 5. Install Git Hooks

**Task**: Install Git hooks from the orchestration-tools branch.

**Prompt**:
```
You are an orchestration assistant. Your task is to install Git hooks for orchestration.

Steps:
1. Run: bash scripts/install-hooks.sh --force --verbose
2. Check that hook files exist in .git/hooks/
3. Verify hooks are executable.

Output: Installation status.
```

## 6. Sync Setup Worktrees

**Task**: Synchronize setup files across worktrees.

**Prompt**:
```
You are an orchestration assistant. Your task is to sync setup files to other worktrees.

Steps:
1. Run: bash scripts/sync_setup_worktrees.sh --verbose
2. Monitor output for synced files.
3. Report any errors.

Output: Sync summary.
```

## 7. Reverse Sync Changes

**Task**: Pull approved changes from a feature branch into orchestration-tools.

**Prompt**:
```
You are an orchestration assistant. Your task is to reverse sync changes from a feature branch.

Arguments: <source_branch> <commit_sha>

Steps:
1. Validate branch and commit exist.
2. Run: bash scripts/reverse_sync_orchestration.sh <source_branch> <commit_sha> --dry-run
3. Review output, confirm if to proceed.
4. If confirmed, run without --dry-run.

Output: Sync result.
```

## 8. Check Orchestration Status

**Task**: Validate the health of the orchestration system.

**Prompt**:
```
You are an orchestration assistant. Your task is to check orchestration system status.

Steps:
1. Run: bash scripts/orchestration_status.sh
2. Review output for any errors or warnings.
3. Report system health.

Output: Status summary.
```

## General Guidelines for LLM Agents

- Always operate in the orchestration-tools branch unless specified otherwise.
- Use absolute paths when necessary.
- Report errors clearly with suggested fixes.
- Validate all actions before and after execution.
- Use verbose flags for detailed output.
- If unsure, ask for clarification rather than assume.
