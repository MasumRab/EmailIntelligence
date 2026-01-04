# Code Formatting Guide

This document describes the code formatting setup for the Task Master project.

## Formatters Used

### Black (Python Code Formatter)
- **Version:** 24.2.0
- **Purpose:** Automatic code formatting with consistent style
- **Configuration:** `pyproject.toml` (line-length=100)
- **Key Features:**
  - Enforces PEP 8 style
  - Consistent quotes (double quotes preferred)
  - Proper spacing and indentation
  - Automatic line wrapping

### Ruff (Fast Python Linter)
- **Version:** 0.14.3
- **Purpose:** Fast linting and code quality checks
- **Configuration:** `pyproject.toml`
- **Key Features:**
  - Replaces flake8, isort, pyupgrade
  - Very fast performance
  - Auto-fixes many issues
  - Type checking integration

### Flake8 (Legacy Linter)
- **Purpose:** Backward compatibility
- **Configuration:** `.flake8`
- **Status:** Being phased out in favor of Ruff

## Configuration Files

### pyproject.toml
Centralized configuration for Black and Ruff:
```toml
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311', 'py312']

[tool.ruff]
line-length = 100
target-version = "py38"
```

### .flake8
Legacy configuration (max-line-length=100):
```ini
[flake8]
max-line-length = 100
exclude = .git,__pycache__,build,dist
ignore = E203, W503
```

### .pre-commit-config.yaml
Pre-commit hooks for automatic formatting:
- Black (code formatter)
- Ruff (linter and formatter)
- File validation (JSON, YAML, TOML)
- Large file detection

## Usage

### Manual Formatting

**Apply formatting to all Python files:**
```bash
./scripts/format_code.sh
```

**Check formatting without making changes:**
```bash
./scripts/format_code.sh --check
```

**Apply Black only:**
```bash
python3 -m black task_scripts/ scripts/ task_data/branch_clustering_implementation.py
```

**Apply Ruff only:**
```bash
python3 -m ruff check --fix task_scripts/ scripts/ task_data/branch_clustering_implementation.py
```

### Pre-commit Hooks

**Install pre-commit hooks:**
```bash
pip install pre-commit
pre-commit install
```

**Run pre-commit hooks manually:**
```bash
pre-commit run --all-files
```

**Skip pre-commit hooks for a single commit:**
```bash
git commit --no-verify -m "message"
```

## Formatting Rules

### Black Style Guide

**Quotes:**
- Use double quotes for strings: `"string"` instead of `'string'`
- Use triple double quotes for docstrings: `"""docstring"""`

**Spacing:**
- Two blank lines before top-level classes and functions
- One blank line before method definitions
- Spaces around operators: `x = 1 + 2`
- No spaces inside brackets: `list[1, 2, 3]`

**Line Length:**
- Maximum 100 characters (configured in pyproject.toml)
- Black automatically wraps long lines

**Imports:**
- Group imports: standard library, third-party, local
- Use `from typing import ...` for type hints
- Sort imports alphabetically

### Ruff Style Guide

**Linting Rules:**
- **E**: pycodestyle errors
- **W**: pycodestyle warnings
- **F**: pyflakes (unused imports, undefined variables)
- **I**: isort (import sorting)
- **N**: pep8-naming (conventions)
- **UP**: pyupgrade (modern Python syntax)
- **B**: flake8-bugbear (common bugs)
- **C4**: flake8-comprehensions (comprehension simplification)
- **SIM**: flake8-simplify (code simplification)

**Ignored Rules:**
- `E203`: whitespace before ':' (conflicts with Black)
- `E501`: line too long (handled by Black)

## Development Workflow

### Before Committing

1. **Format your code:**
   ```bash
   ./scripts/format_code.sh
   ```

2. **Check for issues:**
   ```bash
   ./scripts/format_code.sh --check
   ```

3. **Review changes:**
   ```bash
   git diff
   ```

4. **Commit:**
   ```bash
   git add .
   git commit -m "message"
   ```

### Pre-commit Hooks (Recommended)

Pre-commit hooks automatically format your code before each commit:

```bash
# Install hooks
pre-commit install

# Make a commit (hooks run automatically)
git add .
git commit -m "message"
```

## Common Issues

### Issue: Black reformats my code

**Solution:** This is expected! Black enforces a consistent style. Accept the changes.

### Issue: Ruff finds errors I can't auto-fix

**Solution:** Some issues require manual fixing:
- `E722`: Replace bare `except` with `except Exception:`
- `F841`: Remove unused variables
- `B007`: Use `_` for unused loop variables

### Issue: Line length exceeds 100 characters

**Solution:** Black will automatically wrap long lines. If you need to keep a line long, use Black's `# noqa: E501` comment.

### Issue: Conflicts between Black and Flake8

**Solution:** We ignore `E203` and `W503` in flake8 to avoid conflicts with Black.

## IDE Integration

### VS Code

**Settings (.vscode/settings.json):**
```json
{
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=100"],
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.linting.ruffArgs": ["--fix"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

**Extensions:**
- Black Formatter
- Ruff

### PyCharm

**Settings:**
1. Go to Settings → Tools → External Tools
2. Add Black as an external tool
3. Configure to run on save

## Performance

**Formatting Speed:**
- Black: ~0.5s for 30 files
- Ruff: ~0.1s for 30 files
- Combined: <1s for full project

**Recommendation:** Use pre-commit hooks for automatic formatting with minimal impact.

## Maintenance

**Update Formatters:**
```bash
pip install --upgrade black ruff pre-commit
pre-commit autoupdate
```

**Update Configuration:**
- Modify `pyproject.toml` for Black/Ruff settings
- Modify `.flake8` for legacy flake8 settings
- Modify `.pre-commit-config.yaml` for pre-commit hooks

## Troubleshooting

### Black not found
```bash
pip install black
```

### Ruff not found
```bash
pip install ruff
```

### Pre-commit not working
```bash
pip install pre-commit
pre-commit install
```

### Formatting not applied
```bash
# Check if file is excluded
grep -r "exclude" pyproject.toml

# Force format specific file
python3 -m black <file>
```

## Resources

- [Black Documentation](https://black.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [PEP 8 Style Guide](https://pep8.org/)

## Summary

✅ **Black**: Automatic code formatting (line-length=100)
✅ **Ruff**: Fast linting with auto-fix
✅ **Pre-commit**: Automatic formatting before commits
✅ **Configuration**: Centralized in `pyproject.toml`
✅ **Workflow**: Run `./scripts/format_code.sh` before commits

**Key Principle:** Let the formatters handle the style. Focus on writing clean, readable code, and let Black and Ruff handle the formatting details.