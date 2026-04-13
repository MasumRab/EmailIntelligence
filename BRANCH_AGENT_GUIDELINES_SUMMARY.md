# Branch-Specific Agent Guidelines Summary

**Document Version**: 1.0
**Last Updated**: 2026-03-26
**Status**: Active - Main Branch Configuration

---

## Branch Classification (EmailIntelligence)

### 1. **main** (Current Branch)
- **Purpose**: Core application development and production stability
- **Project Type**: `application`
- **Agent Scope**: Full access to application code, tests, and core configurations
- **Key Files**: `src/`, `tests/`, `client/`, `backend/`

### 2. **scientific**
- **Purpose**: FastAPI backend, email processing, AI analysis, and API routes
- **Project Type**: `backend-service`
- **Agent Scope**: Backend-specific code and services
- **Restrictions**: Should not have orchestration scripts or setup utilities

### 3. **feature branches**
- **Purpose**: Development of specific features
- **Project Type**: `feature`
- **Agent Scope**: Limited to specific feature code
- **Naming**: `feature/`, `fix/`, `enhance/`, `docs/`

---

## Context Control Profiles

### Main Branch Profile
```json
{
  "id": "main",
  "branch_patterns": ["main", "master"],
  "allowed_files": [
    "src/**", "tests/**", "docs/**", "*.md", "*.py", "*.sh",
    "*.yml", "*.yaml", "*.json", "setup.py", "pyproject.toml",
    "requirements*.txt", "uv.lock", ".github/**", "CLAUDE.md", "README.md",
    "client/**", "backend/**"
  ],
  "blocked_files": [
    ".git/**", "__pycache__/**", "*.pyc", ".pytest_cache/**",
    "node_modules/**", "scripts/hooks/**", ".context-control/**",
    ".specify/**", ".taskmaster/**"
  ],
  "max_context_length": 8192,
  "enable_code_execution": true,
  "enable_file_writing": true,
  "enable_shell_commands": true
}
```

---

## Sync Procedures

### Checking Branch Status
```bash
# Check all variants at once
bash scripts/sync_config_analysis.sh --quick

# Standardize configs across branches
bash scripts/standardize_branch_config.sh --check
```

### Syncing with Origin
```bash
# Check ahead/behind status
git branch -vv

# Pull if behind
git pull

# Push if ahead
git push
```

---

## Key Conventions

- **Test**: `pytest`
- **Format**: `black .`
- **Lint**: `flake8 .`
- **Type check**: `mypy .`
- **Dependency**: `uv` (default)
- **Line length**: 100 chars

---

## Anti-Patterns

- **NEVER** commit `.mcp.json` with real API keys
- **NEVER** hard-code secrets in source code
- **NEVER** use `eval()` or `exec()` (security risk)