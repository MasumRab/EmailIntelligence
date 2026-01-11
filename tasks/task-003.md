# Task ID: 003

**Title:** Develop and Integrate Pre-merge Validation Scripts

**Status:** pending

**Dependencies:** 11, 12, 13 ✓

**Priority:** high

**Description:** Create validation scripts to check for the existence of critical files before merges, preventing merge conflicts that cause data loss or missing files.

**Details:**

Identify a list of critical files (e.g., `setup/commands/__init__.py`, `AGENTS.md`, `data/processed/email_data.json` for core JSON data schemas) whose absence would lead to regressions. Develop a script (e.g., Python `scripts/validate_critical_files.py`, or Bash) that checks for the existence and perhaps basic integrity (e.g., non-empty, valid JSON). Integrate this script as a pre-merge hook or as a mandatory status check in the CI/CD pipeline (e.g., `.github/workflows/pull_request.yml`), ensuring it runs on every pull request before merging to critical branches.

### Tags:
- `work_type:script-development`
- `work_type:ci-cd`
- `component:pre-merge-checks`
- `component:file-integrity`
- `scope:devops`
- `scope:quality-assurance`
- `purpose:regression-prevention`
- `purpose:data-integrity`

**Test Strategy:**

Create a feature branch and intentionally delete one of the identified critical files. Open a Pull Request and verify that the pre-merge validation script detects the missing file and blocks the merge. Confirm that the script passes when all critical files are present and valid. Test the integration with the version control system's hook/check mechanism.

## Subtasks

### 19.1. Define critical files and validation criteria for pre-merge checks

**Status:** pending  
**Dependencies:** None  

Analyze the codebase to identify all critical files and directories whose absence or emptiness would cause regressions. Specify exact paths and define the validation logic (e.g., existence, non-empty, valid JSON schema for specific files).

**Details:**

Review project structure, specifically `setup/commands/`, `setup/container/`, `AGENTS.md`, `src/core/`, `config/`, and `data/` directories to pinpoint files like `setup/commands/__init__.py`, `setup/container/__init__.py`, `AGENTS.md`, core JSON data schemas (e.g., `data/processed/email_data.json`), configuration files, and any other crucial components. Create a definitive list of absolute or relative paths that must be checked. For JSON files, determine if basic parsing or full schema validation is required.

### 19.2. Develop core file existence and integrity validation script

**Status:** pending  
**Dependencies:** 19.1  

Implement a script (preferably Python for its robust file handling and JSON capabilities, or Bash for simplicity) that takes the defined list of critical files and criteria, then checks for their existence and basic integrity. The script must return a non-zero exit code on failure and a zero exit code on success.

**Details:**

Create a Python script, e.g., `scripts/validate_critical_files.py`. The script should iterate through the list of critical files identified in subtask 1. For each file, it must perform checks such as `os.path.exists()` (or equivalent for Bash), file size (`os.path.getsize() > 0`), and for designated JSON files (like `data/processed/email_data.json`), attempt to load them using `json.loads()` to ensure basic syntactic validity. Detailed error messages should be logged for any detected failures.

### 19.3. Develop unit and integration tests for validation script

**Status:** pending  
**Dependencies:** None  

Create a comprehensive suite of unit and integration tests to ensure the newly developed validation script correctly identifies missing or malformed critical files. These tests should cover both success and various failure scenarios.

**Details:**

For unit tests, mock file system operations to simulate various file states (e.g., missing, empty, malformed JSON). For integration tests, set up a temporary directory structure that mimics a simplified project with critical files. Run the validation script against this temporary structure with valid, missing, and invalid critical files, asserting the correct exit codes and error outputs.

### 19.4. Integrate validation script into CI/CD pipeline as a pre-merge check

**Status:** pending  
**Dependencies:** None  

Configure the project's CI/CD pipeline (e.g., GitHub Actions, GitLab CI, Jenkins) to execute the developed validation script as a mandatory status check for all pull requests targeting critical branches (e.g., `main`, `develop`) before merging is allowed.

**Details:**

Add a new job or step to the relevant CI configuration file, likely `.github/workflows/pull_request.yml`. This job must execute the validation script (e.g., `python scripts/validate_critical_files.py`). Configure the CI system to interpret a non-zero exit code from the script as a build failure, thereby blocking the pull request merge until all critical files are present and valid according to the defined criteria.

### 19.5. Document and communicate pre-merge validation process to the development team

**Status:** pending  
**Dependencies:** 19.4  

Create clear and concise documentation explaining the purpose, scope, functionality, and impact of the new pre-merge validation process. Effectively communicate these changes and their implications to the entire development team, including guidance on how to debug and resolve validation failures.

**Details:**

Update existing developer guidelines (e.g., `CONTRIBUTING.md`) or create a new document in `docs/dev_guides/pre_merge_checks.md` outlining the critical file checks. Include the full list of critical files being validated, an explanation of how the script operates, common scenarios for validation failures, and steps for developers to troubleshoot and rectify issues. Conduct a team announcement or brief meeting to ensure all developers are aware of and understand the new mandatory pre-merge checks.
