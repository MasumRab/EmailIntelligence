# Quickstart: History Analysis Tool

**Feature**: `001-history-analysis`
**Date**: 2025-11-11

This guide provides instructions for installing and using the History Analysis tool.

## Installation

1.  **Prerequisites**: Ensure you have Python 3.11+ and Git 2.0+ installed on your system.

2.  **Clone the repository**:
    ```bash
    git clone https://github.com/MasumRab/EmailIntelligenceGem.git
    cd EmailIntelligenceGem
    ```

3.  **Set up the virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: The `requirements.txt` will be created in a later phase of development.)*

## Usage

The primary command is `history-analyzer`.

### Analyzing Commit History

To analyze the last 5 commits on your current branch and print the results to the console:

```bash
history-analyzer analyze HEAD~5..HEAD
```

### Specifying Output Format

You can get the output in JSON format, which is useful for scripting or integrating with other tools.

```bash
history-analyzer analyze main --output-format json
```

**Example JSON Output for a single commit**:
```json
{
  "commit_hexsha": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
  "title": "feat: Add user authentication endpoint",
  "narrative": "This commit introduces a new endpoint `/api/login` for user authentication. It adds the `auth_service.py` to handle password verification and token generation. The commit message aligns with the code changes, which primarily focus on adding new authentication logic and a corresponding API route.",
  "is_consistent": true,
  "discrepancy_notes": null
}
```

### Saving Output to a File

To save the analysis to a file named `analysis_report.md`:

```bash
history-analyzer analyze main --output-format md --output-file analysis_report.md
```

### Analyzing a Different Repository

You can specify the path to any local Git repository.

```bash
history-analyzer analyze --repo-path /path/to/another/repo
```
