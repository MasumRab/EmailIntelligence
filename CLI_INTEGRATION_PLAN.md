# Plan: Integrating History Analysis & Rebase Automation into `eai.py`

## Objective
Extend the EmailIntelligence CLI (`eai.py`) to automate the sophisticated commit analysis and rebase planning described in `enhanced-commit-category-analysis.md` and `scientific-branch-rebase-todo-list.md`.

## 1. New Architecture Components

### A. History Analysis Module (`src/git/history.py`)
Responsible for parsing the raw git history and converting it into structured data.
*   **`GitLogParser`**:
    *   Executes `git log` with custom formatting.
    *   Parses output into `Commit` objects (hash, author, date, message, files_changed).
*   **`CommitClassifier`**:
    *   **Input**: `Commit` object.
    *   **Logic**:
        *   Parses Conventional Commits (e.g., `feat:`, `fix:`, `docs:`).
        *   Detects "Risk Keywords" (e.g., "security", "auth", "migration").
        *   Categorizes into: `Infrastructure`, `Feature`, `Fix`, `Docs`, `Refactor`.
    *   **Output**: `CommitCategory` enum and `RiskLevel`.

### B. Rebase Strategy Module (`src/strategy/reordering.py`)
Responsible for generating the optimized rebase plan.
*   **`RebasePlanner`**:
    *   **Input**: List of categorized `Commit` objects.

# Plan: Integrating History Analysis & Rebase Automation into `eai.py`

## Objective
Extend the EmailIntelligence CLI (`eai.py`) to automate the sophisticated commit analysis and rebase planning described in `enhanced-commit-category-analysis.md` and `scientific-branch-rebase-todo-list.md`.

## 1. New Architecture Components

### A. History Analysis Module (`src/analysis/history.py`)
Responsible for parsing the raw git history and converting it into structured data.
*   **`GitLogParser`**:
    *   Executes `git log` with custom formatting.
    *   Parses output into `Commit` objects (hash, author, date, message, files_changed).
*   **`CommitClassifier`**:
    *   **Input**: `Commit` object.
    *   **Logic**:
        *   Parses Conventional Commits (e.g., `feat:`, `fix:`, `docs:`).
        *   Detects "Risk Keywords" (e.g., "security", "auth", "migration").
        *   Categorizes into: `Infrastructure`, `Feature`, `Fix`, `Docs`, `Refactor`.
    *   **Output**: `CommitCategory` enum and `RiskLevel`.

### B. Rebase Strategy Module (`src/strategy/reordering.py`)
Responsible for generating the optimized rebase plan.
*   **`RebasePlanner`**:
    *   **Input**: List of categorized `Commit` objects.
    *   **Logic**:
        *   **Topological Sort**: Respects known dependencies (e.g., "Feature A" depends on "Infra B").
        *   **Priority Sort**: Security > Infrastructure > Features > Documentation.
        *   **Squash Detection**: Identifies "fixup" or "wip" commits that should be squashed into their parents.
    *   **Output**: A structured `RebasePlan`.

### C. CLI Integration (`src/cli/commands.py`)
Expose the new functionality to the user.
*   **New Command**: `analyze-history`
    *   **Arguments**:
        *   `--target-branch` (default: `origin/scientific`)
        *   `--output` (file path to save the analysis report)
    *   **Action**: Generates a detailed report of commit categories and risks.
*   **New Command**: `plan-rebase`
    *   **Arguments**:
        *   `--target-branch` (default: `origin/scientific`)
        *   `--output` (file path to save the todo list)
    *   **Action**: Runs analysis and generates the `scientific-branch-rebase-todo-list.md` automatically.

## 2. Implementation Steps

### Step 1: Implement Git History Parsing
Create `src/git/history.py` to handle `git log` interaction.
```python
class GitHistory:
    async def get_commits(self, range: str) -> List[Commit]:

        # git log --pretty=format:"%H|%s|%an|%ad" ...
        pass
```

### Step 2: Implement Commit Analysis
Create `src/analysis/commits.py` to implement the classification logic found in `enhanced-commit-category-analysis.md`.
```python
class CommitClassifier:
    def classify(self, commit: Commit) -> AnalysisResult:

        # Regex matching for "feat", "fix", "security"

        # Risk assessment logic
        pass
```

### Step 3: Implement Reordering Logic
Create `src/strategy/reordering.py` to implement the sorting rules defined in `scientific-branch-rebase-todo-list.md`.
```python
class RebasePlanner:
    def generate_plan(self, commits: List[Commit]) -> RebaseTodoList:

        # Sort by Category Priority

        # Group related features
        pass
```

### Step 4: Add CLI Command
Update `eai.py` and `src/cli/commands.py` to include the `analyze-history` and `plan-rebase` commands.

## 3. Usage Example

Once implemented, the user can run:

```bash

# Generate the analysis report
python eai.py analyze-history --target-branch scientific --output analysis_report.md

# Generate the rebase todo list
python eai.py plan-rebase --target-branch scientific --output rebase-todo.md
```

This transforms `eai.py` from a reactive conflict resolver into a proactive release management tool.
