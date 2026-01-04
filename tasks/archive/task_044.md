# Task ID: 44

**Title:** Standardize Dependency Management System

**Status:** pending

**Dependencies:** None

**Priority:** high

**Description:** Consolidate the mixed usage of `uv` and `Poetry` for dependency management into a single, consistent approach across the entire codebase to improve build reliability and developer experience.

**Details:**

Decide on a single tool (e.g., Poetry) for all dependency management. If `uv` is preferred for speed, document its usage alongside Poetry for specific scenarios (e.g., faster environment creation in CI). Migrate all `requirements.txt` or `uv.lock` files into a unified `pyproject.toml` structure. Update CI/CD pipelines and local development environment setup scripts (`launch.bat`, shell scripts) to exclusively use the chosen tool. Document the new dependency management process in `README.md` and `docs/developer_guide.md`.

### Tags:
- `work_type:refactoring`
- `work_type:tooling`
- `component:dependency-management`
- `scope:codebase-wide`
- `scope:developer-experience`
- `purpose:consistency`
- `purpose:reliability`

**Test Strategy:**

Verify that all project dependencies can be installed correctly using the new standardized approach. Run all existing tests after a clean dependency install to ensure no breaking changes were introduced. Test environment setup on different platforms (if applicable) to confirm consistency.

## Subtasks

### 44.1. Evaluate & Select Primary Dependency Management Tool and Configure pyproject.toml

**Status:** pending  
**Dependencies:** None  

Evaluate the existing usage of `uv` and `Poetry` across the codebase, including `requirements.txt` and `uv.lock` files, to select a single, primary dependency management tool. Establish a `pyproject.toml` file at the project root to host all dependency metadata and configuration for the chosen tool.

**Details:**

Analyze current project structure and usage of `uv` (e.g., `uv pip install`, `uv venv`) and `pip`/`Poetry` (e.g., `pip install -r requirements.txt`, `poetry add`). Consider factors like project complexity, team familiarity, and performance characteristics (especially for CI). If Poetry is chosen, initialize `pyproject.toml` with `poetry init` or manually create it. If `uv` is preferred for speed in specific scenarios (like CI), document its role alongside the primary tool. The `pyproject.toml` will serve as the single source of truth for dependencies.

### 44.2. Migrate Existing Dependencies to pyproject.toml

**Status:** pending  
**Dependencies:** 44.1  

Migrate all dependencies currently defined in `requirements.txt` files, `uv.lock` files, or implicitly managed by `uv` into the newly established `pyproject.toml` using the selected primary dependency management tool. Ensure all packages, versions, and dependency groups (development, production, etc.) are accurately reflected.

**Details:**

Identify all `requirements.txt` files and `uv.lock` files across the repository. For each identified dependency, add it to the `pyproject.toml` using the commands of the chosen tool (e.g., `poetry add <package>@<version> --group <group>`). Explicitly define development dependencies in `pyproject.toml`. After successful migration, remove all `requirements.txt` and `uv.lock` files from the codebase to enforce the single source of truth.

### 44.3. Update Workflows, Scripts, and Documentation for New Dependency Process

**Status:** pending  
**Dependencies:** None  

Modify all CI/CD pipeline configurations, local development environment setup scripts (e.g., `launch.bat`, various shell scripts), and project documentation (`README.md`, `docs/developer_guide.md`) to exclusively use the newly standardized dependency management tool and `pyproject.toml`.

**Details:**

Review and update all CI/CD pipeline scripts (e.g., `.github/workflows/*.yml`), local setup scripts, and any `Makefile` or similar build scripts to replace old dependency installation commands (`pip install -r`, `uv venv`, etc.) with commands for the chosen tool (e.g., `poetry install`). Update `README.md` and `docs/developer_guide.md` with detailed instructions on setting up the development environment, adding new dependencies, and managing existing ones using the standardized tool. Include guidelines for specific scenarios where `uv` might be used for speed, if applicable.
