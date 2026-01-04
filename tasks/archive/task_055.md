# Task ID: 55

**Title:** Develop Automated Error Detection Scripts for Merges

**Status:** pending

**Dependencies:** 54

**Priority:** high

**Description:** Implement scripts to automatically detect and flag common merge-related errors such as merge artifacts (<<<<<<<, =======, >>>>>>>), garbled text/encoding issues, missing imports, and accidentally deleted modules after a branch alignment operation.

**Details:**

Create Python scripts to analyze changed files post-merge/rebase. 
1.  **Merge Artifacts:** Use `git diff --check` or `grep -E '^(<<<<<<<|=======|>>>>>>>)'` in changed files to find uncleaned merge markers. 
2.  **Garbled Text/Encoding:** Implement checks for common encoding errors. Files can be opened with `utf-8` and fallbacks (e.g., `errors='replace'`) and then checked for replacement characters or patterns indicating malformed text. Consider using `chardet` for initial encoding detection if files are not strictly UTF-8. 
3.  **Missing Imports:** For Python files, parse the AST (`ast` module) to extract import statements and verify that the imported modules/packages exist in the current environment or codebase. For other languages (if applicable), use `grep` or language-specific parsers to identify import/require statements and check for corresponding file paths. 
4.  **Accidentally Deleted Modules:** Compare the file list before and after alignment using `git diff --name-only --diff-filter=D` to identify deleted files. For modules, check if any deleted files were part of an active import path. The scripts should log findings and, if possible, suggest corrective actions. Output should be concise for a single developer.

**Test Strategy:**

Create test branches with deliberate merge conflicts, garbled text (e.g., inserting non-UTF8 chars), removing an imported file, and introducing un-resolved merge markers. Run the developed scripts on these branches and verify that all error types are correctly identified and reported. Ensure false positives are minimized.

## Subtasks

### 55.1. Develop Merge Artifact and Deleted Module Detection

**Status:** pending  
**Dependencies:** None  

Create Python scripts to efficiently detect uncleaned merge markers (<<<<<<<, =======, >>>>>>>) within changed files and identify accidentally deleted modules post-merge or rebase operations.

**Details:**

Implement detection for merge artifacts using 'git diff --check' or 'grep -E '^(<<<<<<<|=======|>>>>>>>)' on staged/changed files. For deleted modules, compare the file list before and after alignment using 'git diff --name-only --diff-filter=D' to identify deleted files and check if any were part of an active import path.

### 55.2. Implement Garbled Text and Initial Import Statement Extraction

**Status:** pending  
**Dependencies:** 55.1  

Develop functionality to detect garbled text/encoding issues in changed files and perform initial extraction of import statements from Python files, paying special attention to potential issues from a 'backend' to 'src' migration.

**Details:**

For garbled text, iterate through changed files. Attempt to open files with 'utf-8' encoding and 'errors='replace''. Subsequently, check the content for common replacement characters (e.g., '') that indicate encoding errors. Consider using 'chardet' for more robust encoding detection for non-UTF-8 files. For Python files, use regular expressions or simple string parsing to extract 'import' and 'from ... import' statements to build a list of potential module dependencies. Specifically note any imports referencing 'backend' paths.

### 55.3. Consolidate Error Detection and Implement Comprehensive Import Validation

**Status:** pending  
**Dependencies:** 55.1, 55.2  

Integrate all previously developed error detection mechanisms into a single, robust Python script. This includes performing comprehensive AST-based import validation for Python files, ensuring safe execution, and providing clear, actionable reporting, specifically for `backend` to `src` migration-related import issues.

**Details:**

Combine the detection logic for merge artifacts, deleted modules, garbled text, and import issues. For Python files, use the 'ast' module to parse the Abstract Syntax Tree (AST) to accurately extract all import statements. For each extracted import, verify if the module or package exists in the current environment or codebase. Validate that 'backend' imports are either correctly migrated to 'src' paths or flagged as missing if they still point to non-existent 'backend' locations. Implement safety measures to ensure the script does not perform Git operations that could lead to wrong-branch pushes. The script should output a concise report of all detected errors, including file paths, error types, and suggested corrective actions.
