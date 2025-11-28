# Task ID: 4

**Title:** Backend Migration from 'backend' to 'src/backend'

**Status:** pending

**Dependencies:** 1 ✓

**Priority:** high

**Description:** Execute the complete structural migration of the legacy 'backend' package to the new modular architecture under 'src/backend'. This is a critical architectural improvement to modernize the codebase and enable further development.

**Details:**

1. Create a new branch from the main development branch after the code recovery (Task 1) is merged. 2. Physically move the entire `backend` directory into `src/` and rename it to `src/backend`. 3. Perform a project-wide find-and-replace to update all Python import statements from `from backend...` to `from src.backend...`. Use a tool like `sed`, `grep`, or an and an IDE's refactoring capabilities. 4. Update any configuration files that reference the old path. This includes `PYTHONPATH` definitions in Dockerfiles (`ENV PYTHONPATH="/app/src:$PYTHONPATH"`), `docker-compose.yml`, CI/CD pipeline scripts (e.g., `.github/workflows/ci.yml`), and potentially `pyproject.toml` if using editable installs. 5. After all tests pass, delete the original top-level `backend` directory. 6. Ensure `src/__init__.py` and `src/backend/__init__.py` exist to make them valid packages.

### Tags:
- `work_type:refactoring`
- `component:backend-core`
- `scope:architectural`
- `purpose:modernization`, `maintainability`

**Test Strategy:**

The primary validation method is comprehensive regression testing. Run the full existing test suite and ensure 100% of tests pass. Perform a manual smoke test of the application by starting it and hitting key API endpoints using Postman or cURL to confirm it is fully functional. The application's behavior must be identical to the pre-migration state. No new feature tests are required for this task.

## Subtasks

### 4.1. Move Backend Files to src/

**Status:** pending  
**Dependencies:** None  

Move all source code from the 'backend' directory to the new 'src/backend' directory. This is the first step in the migration process.

**Details:**

Physically move the entire `backend` directory from the project root into `src/` and rename it to `src/backend`. This foundational step establishes the new modular architecture.

### 4.2. Update Imports and References

**Status:** pending  
**Dependencies:** None  

Update all internal imports and external references throughout the codebase to reflect the new 'src/backend' path. This includes imports in both backend and frontend code.

**Details:**

Perform a project-wide find-and-replace to update all Python import statements from `from backend...` to `from src.backend...`. Utilize an IDE's refactoring capabilities or a tool like `sed` for this crucial update.

### 4.3. Update Configuration Files

**Status:** pending  
**Dependencies:** None  

Update any configuration files that reference the old path. This includes `PYTHONPATH` definitions in `Dockerfile`s (e.g., `ENV PYTHONPATH="/app/src:$PYTHONPATH"`), `docker-compose.yml`, CI/CD pipeline scripts (e.g., `.github/workflows/ci.yml`), and potentially `pyproject.toml` if using editable installs. Also, ensure `src/__init__.py` and `src/backend/__init__.py` exist to make them valid Python packages.

**Details:**

Update any configuration files that reference the old path. This includes `PYTHONPATH` definitions in `Dockerfile`s (e.g., `ENV PYTHONPATH="/app/src:$PYTHONPATH"`), `docker-compose.yml`, CI/CD pipeline scripts (e.g., `.github/workflows/ci.yml`), and potentially `pyproject.toml` if using editable installs. Also, ensure `src/__init__.py` and `src/backend/__init__.py` exist to make them valid Python packages.

### 4.4. Run and Fix Tests

**Status:** pending  
**Dependencies:** None  

Run the full test suite to ensure that the migration has not introduced any regressions. Fix any failing tests.

**Details:**

Execute the full existing test suite across the migrated codebase and ensure 100% of tests pass. Address any failures by debugging and correcting import paths, logic, or configuration mismatches introduced by the move. Perform a manual smoke test of the application by starting it and hitting key API endpoints using Postman or cURL to confirm it is fully functional.

### 4.5. Final Cleanup

**Status:** pending  
**Dependencies:** None  

Remove the original 'backend' directory from the project. This is the final step in the migration process.

**Details:**

After all tests pass and functional verification is complete, safely delete the original top-level `backend` directory. Ensure no lingering files or references remain that could cause confusion or issues.

### 4.6. Prepare Git environment and physically move backend directory

**Status:** pending  
**Dependencies:** 4.1  

Create a new feature branch from the main development branch and then physically move the entire 'backend' directory into 'src/' and rename it to 'src/backend'. Ensure the new directory structure is correctly established.

**Details:**

1. Create a new Git branch, e.g., 'feature/backend-to-src'. 2. Use file system commands (e.g., `mv backend src/backend`) to relocate the directory. 3. Ensure that 'src/' and 'src/backend/' have `__init__.py` files to be recognized as Python packages.

### 4.7. Update all Python import statements project-wide

**Status:** pending  
**Dependencies:** 4.6  

Perform a comprehensive find-and-replace operation across the entire project to update all Python import statements from 'from backend...' to 'from src.backend...'. This includes all Python source files and any scripts that might contain these imports.

**Details:**

Use an IDE's refactoring tools or command-line utilities like `grep -rl 'from backend' . | xargs sed -i 's/from backend/from src.backend/g'` for initial replacement. Manually review changes to catch any edge cases or incorrect replacements. Ensure relative imports within the moved 'backend' module are not inadvertently broken.

### 4.8. Modify configuration files to reflect new backend path

**Status:** pending  
**Dependencies:** 4.7  

Update all relevant configuration files that reference the old 'backend' path to point to the new 'src/backend' location. This includes environment variables, Docker configurations, CI/CD pipelines, and project metadata.

**Details:**

1. Update `PYTHONPATH` definitions in Dockerfiles (e.g., `ENV PYTHONPATH="/app/src:$PYTHONPATH"`). 2. Modify `docker-compose.yml` if it references specific backend services or paths. 3. Adjust CI/CD pipeline scripts (e.g., `.github/workflows/ci.yml`) for build, test, and deployment stages. 4. Review `pyproject.toml` or `setup.py` for editable installs or package discovery.

### 4.9. Execute comprehensive regression testing

**Status:** pending  
**Dependencies:** 4.8  

Run the full suite of automated tests (unit, integration, end-to-end) and perform manual smoke testing to ensure that the backend migration has not introduced any regressions or broken existing functionality.

**Details:**

1. Execute the entire existing automated test suite (e.g., `pytest`). 2. Achieve 100% test pass rate. 3. Perform a manual smoke test by starting the application locally. 4. Use tools like Postman or cURL to hit key API endpoints and verify expected responses and data integrity. 5. Monitor logs for any new errors or warnings.

### 4.10. Clean up old backend directory and finalize migration

**Status:** pending  
**Dependencies:** 4.9  

Once all tests pass and the application is confirmed to be fully functional in the new 'src/backend' structure, safely delete the original top-level 'backend' directory.

**Details:**

1. Double-check that no remaining code or configuration files explicitly reference the old 'backend' directory. 2. Remove the old `backend/` directory using `rm -rf backend/`. 3. Commit all changes to the feature branch and prepare for merging into the main development branch.

### 4.11. Detailed Inventory and Pre-Migration Backup

**Status:** pending  
**Dependencies:** None  

Create a detailed inventory of all files and their dependencies in the current 'backend' directory, map all 'backend' import statements across the codebase, identify all configuration files referencing 'backend' paths, and perform a complete backup of the current state before any changes are made.

**Details:**

1. Create a comprehensive list of all files and subdirectories within the current 'backend' directory. 2. Use `grep`, IDE search functions, or static analysis tools to systematically map all Python import statements that explicitly reference 'backend' (e.g., 'from backend.module', 'import backend.submodule') across the entire codebase. 3. Identify all configuration files that directly or indirectly reference paths related to the 'backend' directory. This includes `Dockerfile(s)`, `docker-compose.yml`, `pyproject.toml`, `requirements.txt`, `.env` files, `launch.py`, `setup` scripts, and CI/CD pipeline definitions (e.g., `.github/workflows/ci.yml`). 4. Create a full, verifiable backup of the entire repository's current state to ensure recoverability in case of unforeseen issues during the migration.

### 4.12. Relocate 'backend' to 'src/backend' and Update Primary Imports

**Status:** pending  
**Dependencies:** 4.11  

Physically move the 'backend' directory into 'src/', rename it to 'src/backend', ensure proper Python package structure, and systematically update all direct Python import statements across the codebase to reflect the new 'src.backend' path.

**Details:**

1. Create a new development branch specifically for this migration task. 2. Execute the physical move of the entire top-level `backend` directory into the `src/` directory. This should result in `src/backend`. 3. Verify that `src/__init__.py` and `src/backend/__init__.py` files exist to ensure both `src` and `src/backend` are recognized as Python packages. If not, create them. 4. Perform a project-wide find-and-replace operation to change all Python import statements from `from backend.` to `from src.backend.` and `import backend` to `import src.backend` (and similarly for submodules). Leverage IDE refactoring tools where possible for accuracy. 5. Perform initial verification by attempting to run simple Python scripts that import from the new `src.backend` structure to catch immediate syntax or path errors.

### 4.13. Adjust Configuration Files and Build Contexts for New Path

**Status:** pending  
**Dependencies:** 4.12  

Update all identified configuration files, Dockerfiles, and CI/CD pipelines to accurately reference the new 'src/backend' directory structure, ensuring that build processes, environment variables, and deployment scripts function correctly.

**Details:**

1. Modify all relevant `Dockerfile(s)` to adjust `PYTHONPATH` definitions (e.g., `ENV PYTHONPATH="/app/src:$PYTHONPATH"`) and update any `COPY`, `ADD`, or `WORKDIR` instructions that previously pointed to the old `backend` directory. 2. Update `docker-compose.yml` service definitions, specifically `build` contexts, image paths, and volume mounts, to correctly use the `src/backend` path. 3. Review and update `pyproject.toml` or `setup.py` if they contain explicit path references for package discovery or editable installs. 4. Adjust `requirements.txt` or any other dependency management files that might have path-based requirements. 5. Modify `.env` files or any custom environment configuration scripts that set paths. 6. Update all CI/CD pipeline configurations (e.g., `.github/workflows/ci.yml`) to ensure that build, test, and deployment jobs correctly locate and interact with the `src/backend` module.

### 4.14. Execute Full Regression Testing and Manual Feature Verification

**Status:** pending  
**Dependencies:** 4.13  

Perform comprehensive regression testing by running the entire automated test suite, including import validation tests. Additionally, manually verify critical application features to confirm that no functionality was broken by the migration.

**Details:**

1. Execute the complete automated regression test suite to identify any regressions introduced by the path changes. 2. Implement a dedicated verification script that systematically attempts to import all modules within `src/backend` and their key components, logging any import failures. 3. Perform thorough manual verification of critical application features. This includes starting the application, interacting with key API endpoints (e.g., using Postman, cURL, or UI), and confirming expected behavior for core functionalities (e.g., user authentication, data processing, key workflows). 4. Document any encountered import errors, runtime exceptions, or broken functionalities, including stack traces and relevant logs for debugging.

### 4.15. Post-Migration Cleanup and Documentation of Migration Process

**Status:** pending  
**Dependencies:** 4.14  

Upon successful completion of all testing and verification, remove the original 'backend' directory, and create comprehensive documentation detailing the migration process, including challenges encountered and resolutions, to serve as a future reference.

**Details:**

1. After all automated tests pass, and manual verification confirms full application functionality, delete the original top-level `backend` directory. 2. Update any remaining internal documentation, README files, or architectural diagrams that still refer to the old `backend` path. 3. Document the entire migration process, including the steps taken, specific tools or commands used, any significant issues or edge cases encountered, and their resolutions. This documentation should be placed in a designated project documentation section. 4. Confirm that the application continues to function correctly after the old directory removal.
