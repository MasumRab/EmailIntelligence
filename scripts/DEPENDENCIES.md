# Script Dependencies

**Date:** December 11, 2025  
**Purpose:** Document all dependencies required for scripts to function  
**Scope:** System, npm, Python, and individual script requirements

---

## System Requirements

Scripts in this project require certain system-level tools and versions:

| Requirement | Version | Purpose |
| --- | --- | --- |
| bash | 4.0+ | Shell scripting |
| python | 3.8+ | Python script execution |
| git | 2.20+ | Version control |
| npm | 6.0+ | JavaScript/Node package management |
| sed | GNU version | Text processing in link standardization |
| find | standard | File discovery and filtering |

**Verification Commands:**

```bash
# Check bash version
bash --version | head -1

# Check python version
python --version

# Check git version
git --version

# Check npm version
npm --version
```

---

## npm Packages

JavaScript and Node.js dependencies for markdown linting and formatting.

### Installation

```bash
# Install all npm dev dependencies
npm install --save-dev prettier markdownlint-cli

# Or use the provided package.json which already includes them
npm install
```

### Required Packages

| Package | Version | Purpose |
| --- | --- | --- |
| prettier | ^3.7.4 | Code/markdown formatter |
| markdownlint-cli | ^0.46.0 | Markdown linter |

### Current Status

**Already added to package.json** in devDependencies:
```json
{
  "devDependencies": {
    "prettier": "^3.7.4",
    "markdownlint-cli": "^0.46.0"
  }
}
```

### Used By

- `scripts/markdown/lint-and-format.sh` - Uses prettier and markdownlint-cli
- Git pre-commit hooks (optional) - Can validate markdown
- CI/CD pipelines (optional) - GitHub Actions integration

---

## Python Packages

Python dependencies from requirements-dev.txt.

### Key Dependencies

Core Python packages used across project scripts:

| Package | Purpose | Usage |
| --- | --- | --- |
| pytest | Testing framework | Run tests: `pytest` |
| black | Python code formatter | Format Python code |
| flake8 | Python linter | Lint Python code |
| mypy | Type checker | Check type hints |
| pylint | Code analysis | Code quality checks |

### Installation

```bash
# Using uv (recommended)
python launch.py --setup

# Or using pip
pip install -r requirements-dev.txt

# Or using poetry
poetry install
```

### Full Dependency List

See `requirements-dev.txt` in project root for complete list of dependencies.

---

## Script-Specific Dependencies

### Markdown Scripts

**Location:** `scripts/markdown/`

#### lint-and-format.sh

**Dependencies:**
- bash 4.0+
- npm 6.0+
- prettier ^3.7.4
- markdownlint-cli ^0.46.0
- Configuration: `.prettierrc`, `.markdownlintrc`

**Command:**
```bash
bash scripts/markdown/lint-and-format.sh [options] [files...]
```

#### standardize-links.sh

**Dependencies:**
- bash 4.0+
- sed (GNU version)
- find (standard)
- No npm/Python required

**Command:**
```bash
bash scripts/markdown/standardize-links.sh [options] [files...]
```

---

### Orchestration Scripts

**Location:** `scripts/hooks/`, `scripts/`

#### Post-Merge Hook

**Dependencies:**
- bash 4.0+
- git 2.20+
- .taskmaster submodule (git submodule)

**Purpose:** Auto-sync .taskmaster submodule after merges

#### Orchestration Control Scripts

**Dependencies:**
- bash 4.0+
- git 2.20+
- Other orchestration scripts (mutual dependencies)

**Examples:**
- `enable-all-orchestration.sh`
- `disable-all-orchestration.sh`
- `orchestration_status.sh`

---

### Documentation Scripts

**Location:** `scripts/docs_*.py`

#### docs_merge_strategist.py

**Dependencies:**
- Python 3.8+
- Standard library only (os, json, pathlib, re)
- No external packages required

**Command:**
```python
python scripts/docs_merge_strategist.py [options]
```

#### docs_content_analyzer.py

**Dependencies:**
- Python 3.8+
- Standard library only

**Command:**
```python
python scripts/docs_content_analyzer.py [options]
```

---

### Agent Scripts

**Location:** `scripts/agents/`

#### agent_registry.py

**Dependencies:**
- Python 3.8+
- Standard library (json, pathlib, dataclasses)
- Optional: configparser for config files

**Command:**
```python
from scripts.agents.agent_registry import AgentRegistry
registry = AgentRegistry()
```

---

### Validation Scripts

**Location:** `scripts/`

#### verify-dependencies.py

**Dependencies:**
- Python 3.8+
- Standard library (subprocess, sys)
- No external packages

**Command:**
```bash
python scripts/verify-dependencies.py
```

#### parallel_validator.py

**Dependencies:**
- Python 3.8+
- concurrent.futures (stdlib)
- No external packages

---

### Synchronization Scripts

**Location:** `scripts/`

#### sync-common-docs.sh

**Dependencies:**
- bash 4.0+
- git 2.20+
- rsync (may need installation)

**Command:**
```bash
bash scripts/sync-common-docs.sh
```

#### sync_common_docs.py

**Dependencies:**
- Python 3.8+
- Standard library (os, shutil, pathlib, json)

**Command:**
```bash
python scripts/sync_common_docs.py
```

---

### Task Management Scripts

**Location:** `scripts/task_creation/`

**Dependencies:**
- Python 3.8+
- Specific requirements vary by script
- See individual script headers for details

---

## Configuration Dependencies

Scripts rely on configuration files in the project root:

| File | Purpose | Used By |
| --- | --- | --- |
| `.prettierrc` | Prettier formatting config | lint-and-format.sh |
| `.markdownlintrc` | Markdownlint rules config | lint-and-format.sh |
| `.pylintrc` | Python linting config | pylint |
| `.flake8` | Flake8 config | flake8 |
| `pyproject.toml` | Python project config | black, pytest |
| `pytest.ini` | Pytest config | pytest |
| `setup.cfg` | Setup configuration | Various tools |

**Verification:**
```bash
# Check configuration files exist
ls -la .*rc *.ini *.toml *.cfg 2>/dev/null | grep -v "node_modules"
```

---

## Installation Quick Start

### Complete Setup

```bash
# 1. Install system dependencies (Ubuntu/Debian)
sudo apt-get install -y bash git python3 npm

# 2. Install npm packages
npm install

# 3. Install Python dependencies
python launch.py --setup

# 4. Verify installation
python scripts/verify-dependencies.py
```

### Minimal Setup (Markdown Only)

```bash
# For markdown scripts only
npm install --save-dev prettier markdownlint-cli

# Test markdown scripts
bash scripts/markdown/lint-and-format.sh --help
bash scripts/markdown/standardize-links.sh --help
```

### Development Setup

```bash
# Full development environment
python launch.py --setup

# Or with poetry
python launch.py --use-poetry --setup

# Check all linters
black --version
flake8 --version
mypy --version
pylint --version
```

---

## Dependency Verification

### Check All Dependencies

```bash
# Run dependency verification script
python scripts/verify-dependencies.py
```

### Manual Verification

```bash
# System tools
bash --version | head -1
python --version
git --version
npm --version

# npm packages (if installed)
npm list prettier markdownlint-cli

# Python packages
python -m pip list | grep -E "black|flake8|mypy|pylint|pytest"

# Configuration files
ls -la .prettierrc .markdownlintrc .flake8 .pylintrc
```

---

## Optional Dependencies

### CI/CD Integration

**GitHub Actions** - No additional dependencies required

### Pre-commit Hooks

**Tool:** pre-commit framework (optional)

```bash
# Install pre-commit framework (optional)
pip install pre-commit

# Create .pre-commit-config.yaml for hook definition
```

### Local Pre-commit Hook

**No external dependencies** - Uses existing bash scripts

```bash
# Manually create .git/hooks/pre-commit
bash scripts/install-hooks.sh
```

---

## Troubleshooting

### "npm: command not found"

**Solution:** Install Node.js and npm
```bash
# Ubuntu/Debian
sudo apt-get install -y nodejs npm

# macOS
brew install node
```

### "prettier: command not found"

**Solution:** Install npm packages
```bash
npm install --save-dev prettier markdownlint-cli
# Or
npm install
```

### "markdownlint: command not found"

**Solution:** Same as prettier
```bash
npm install --save-dev markdownlint-cli
```

### Python version conflicts

**Solution:** Verify Python version
```bash
python --version  # Should be 3.8+
# Or use python3 explicitly
python3 --version
python3 launch.py --setup
```

### Missing git hooks

**Solution:** Reinstall hooks
```bash
bash scripts/install-hooks.sh
```

---

## Dependency Updates

### Updating npm Packages

```bash
# Check for updates
npm outdated

# Update to latest compatible versions
npm update

# Update to latest versions (may break compatibility)
npm install --save-dev prettier@latest markdownlint-cli@latest
```

### Updating Python Packages

```bash
# Using uv (recommended)
python launch.py --update-deps

# Using pip
pip install --upgrade -r requirements-dev.txt

# Using poetry
poetry update
```

---

## Performance Impact

### Minimal Footprint

- Bash scripts: ~100 KB total
- Configuration files: ~2 KB total
- No runtime memory overhead

### npm Packages

- prettier: ~30 MB disk space
- markdownlint-cli: ~10 MB disk space
- Total node_modules: ~200 MB (approximate)

### Python Packages

- requirements-dev.txt: ~500 MB (including transitive deps)
- Can be reduced using requirements.txt (production only)

---

## Version Compatibility

### Supported Versions

| Component | Minimum | Tested | Recommended |
| --- | --- | --- | --- |
| bash | 4.0 | 5.0+ | 5.1+ |
| python | 3.8 | 3.10-3.12 | 3.11+ |
| git | 2.20 | 2.40+ | 2.45+ |
| npm | 6.0 | 9.0+ | 10.0+ |
| node | 12.0 | 18.0+ | 20.0+ |

---

## Related Documentation

- [SCRIPTS_INVENTORY.md](./SCRIPTS_INVENTORY.md) - Complete script registry
- [scripts/markdown/README.md](./markdown/README.md) - Markdown script guide
- [requirements-dev.txt](../requirements-dev.txt) - Python dependencies
- [package.json](../package.json) - npm dependencies
- [setup/](../setup/) - Setup and installation scripts

---

**Last Updated:** December 11, 2025  
**Status:** Production  
**Maintained By:** Script Management System
