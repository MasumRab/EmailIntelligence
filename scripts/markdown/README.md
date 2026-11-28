# Markdown Cleanup Scripts

**Date:** December 11, 2025  
**Purpose:** Linting, formatting, and link standardization for Markdown documentation

## Overview

This directory contains scripts for maintaining markdown documentation quality:

- **Linting & Formatting:** Code style consistency using Prettier and Markdownlint
- **Link Standardization:** Convert relative links to consistent `./ ` prefix format
- **Validation:** Verify all markdown links resolve to actual files

## Scripts

### 1. lint-and-format.sh

Lints and formats markdown files using `prettier` and `markdownlint-cli`.

#### Dependencies

```bash
npm install --save-dev prettier markdownlint-cli
```

#### Usage

```bash
# Lint and format specific files
bash scripts/markdown/lint-and-format.sh DOCUMENTATION_INDEX.md SINGLE_USER_WORKFLOW.md

# Check all markdown files (read-only)
bash scripts/markdown/lint-and-format.sh --check --all

# Fix all markdown files
bash scripts/markdown/lint-and-format.sh --fix --all

# Get help
bash scripts/markdown/lint-and-format.sh --help
```

#### Options

- `--check` - Check only (report issues, don't modify)
- `--fix` - Apply fixes automatically (default)
- `--all` - Process all `.md` files in project
- `--help` - Show help message

#### Standards Applied

**From `.prettierrc`:**
- Line width: 100 characters (with exceptions for code/tables)
- Tab width: 2 spaces
- Prose wrap: Always (for markdown)
- Trailing comma: ES5 style
- Quote style: Double quotes

**From `.markdownlintrc`:**
- Line length: 100 characters max
- Heading spacing: Blanks required before/after
- List spacing: Blanks required before/after
- No hard tabs
- Consistent emphasis/strong style
- Consistent list markers
- Proper code block fencing

#### Configuration Files

Both configuration files are in the project root:

- `.prettierrc` - Prettier code formatter configuration
- `.markdownlintrc` - Markdownlint rules configuration

See project root for current settings.

### 2. standardize-links.sh

Converts relative markdown links to consistent `./ ` prefix format.

#### Usage

```bash
# Check specific file
bash scripts/markdown/standardize-links.sh --check DOCUMENTATION_INDEX.md

# Dry run on all files (show changes without applying)
bash scripts/markdown/standardize-links.sh --dry-run --all

# Apply fixes to all files
bash scripts/markdown/standardize-links.sh --fix --all

# Get help
bash scripts/markdown/standardize-links.sh --help
```

#### Options

- `--check` - Show what needs to change (no modifications)
- `--fix` - Apply changes (default behavior)
- `--dry-run` - Show changes that would be made
- `--all` - Process all `.md` files
- `--help` - Show help message

#### Link Patterns Fixed

**Root-level files:**
```markdown
BEFORE: [text](FILE.md)
AFTER:  [text](./FILE.md)
```

**Subdirectory files:**
```markdown
BEFORE: [text](docs/file.md)
AFTER:  [text](./docs/file.md)
```

**Broken paths:**
```markdown
BEFORE: [text](docs/core/FILE.md)
AFTER:  [text](./docs/FILE.md)
```

**Specific file updates:**
```markdown
BEFORE: [text](docs/guides/branch_switching.md)
AFTER:  [text](./docs/guides/branch_switching_guide.md)

BEFORE: [text](docs/guides/workflow_and_review_process.md)
AFTER:  [text](./docs/git_workflow_plan.md)
```

#### Link Validation

The script automatically:
- Creates backup copies before modifying
- Validates that link targets exist
- Reports warnings for missing references
- Preserves external URLs (http/https)
- Preserves section anchors

## Quick Start

### Step 1: Install Dependencies

```bash
npm install --save-dev prettier markdownlint-cli
```

### Step 2: Check Current Status

```bash
# Check linting
npx markdownlint "*.md"

# Check formatting
npx prettier --check "*.md"

# Check links
bash scripts/markdown/standardize-links.sh --check --all
```

### Step 3: Fix Issues

```bash
# Standardize links
bash scripts/markdown/standardize-links.sh --fix --all

# Format and lint
bash scripts/markdown/lint-and-format.sh --fix --all
```

## Integration

### Git Hooks

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Markdown linting check before commit
bash scripts/markdown/lint-and-format.sh --check --all || {
  echo "Markdown linting failed. Run: bash scripts/markdown/lint-and-format.sh --fix --all"
  exit 1
}
```

### CI/CD Pipeline

Add to GitHub Actions (`.github/workflows/lint.yml`):

```yaml
- name: Check Markdown Linting
  run: |
    npm install --save-dev prettier markdownlint-cli
    npx markdownlint "*.md" "docs/**/*.md"

- name: Check Markdown Formatting
  run: npx prettier --check "*.md" "docs/**/*.md"
```

### npm Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "lint:md": "markdownlint '*.md' 'docs/**/*.md'",
    "format:md": "prettier --write '*.md' 'docs/**/*.md'",
    "check:md": "prettier --check '*.md' 'docs/**/*.md'",
    "clean:md": "bash scripts/markdown/lint-and-format.sh --fix --all"
  }
}
```

Then run:

```bash
npm run lint:md      # Check linting
npm run check:md     # Check formatting
npm run format:md    # Apply formatting
npm run clean:md     # Full cleanup
```

## Results from December 11, 2025 Run

### Files Processed

- DOCUMENTATION_INDEX.md (327 lines, ~12 KB)
- SINGLE_USER_WORKFLOW.md (509 lines, ~13 KB)
- DOCUMENTATION_CONSOLIDATION_PLAN.md (409 lines, ~15 KB)
- SINGLE_USER_OPTIMIZATION_SUMMARY.md (445 lines, ~13 KB)

**Total:** 1,690 lines, ~53 KB

### Issues Fixed

- ✅ Line length violations (100-char limit)
- ✅ Blank lines around headings and lists
- ✅ Ordered list numbering
- ✅ Table formatting and spacing
- ✅ Code block fencing
- ✅ Relative link standardization (+30 links updated)

### Links Standardized

| Format | Count | Status |
| ------ | ----- | ------ |
| `./` prefix | 117 | ✅ Preferred |
| No prefix | 187 | ❌ Deprecated |
| `../` prefix | 4 | ✅ Valid |

### Validation Results

- ✅ All links validated
- ✅ No broken references
- ✅ All files pass markdownlint
- ✅ All files pass prettier

## Troubleshooting

### "prettier: command not found"

Install prettier:

```bash
npm install --save-dev prettier
```

### "markdownlint: command not found"

Install markdownlint-cli:

```bash
npm install --save-dev markdownlint-cli
```

### Scripts not executable

Make scripts executable:

```bash
chmod +x scripts/markdown/*.sh
```

### Link standardization issues

Run with dry-run first:

```bash
bash scripts/markdown/standardize-links.sh --dry-run --all
```

Review changes before applying:

```bash
bash scripts/markdown/standardize-links.sh --fix --all
```

## Best Practices

1. **Run before committing:**
   ```bash
   bash scripts/markdown/lint-and-format.sh --fix --all
   ```

2. **Use git hooks for automation:**
   - Pre-commit hook validates markdown
   - Auto-fixes minor formatting issues

3. **Keep configurations in sync:**
   - `.prettierrc` and `.markdownlintrc` define standards
   - Update these if standards change
   - All scripts respect these configurations

4. **Validate links regularly:**
   ```bash
   bash scripts/markdown/standardize-links.sh --check --all
   ```

5. **Use npm scripts:**
   - Easier to remember
   - Consistent across team
   - Can be automated

## Configuration

### Prettier Configuration

**File:** `.prettierrc`

```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "proseWrap": "always",
  "overrides": [
    {
      "files": "*.md",
      "options": {
        "proseWrap": "always",
        "printWidth": 100
      }
    }
  ]
}
```

### Markdownlint Configuration

**File:** `.markdownlintrc`

```json
{
  "default": true,
  "MD013": {
    "line_length": 100,
    "code_blocks": false,
    "code_lines": false,
    "tables": false
  },
  "MD024": false,
  "MD025": false,
  "MD033": false
}
```

## Related Documentation

- [MARKDOWN_LINTING_REPORT.md](../../MARKDOWN_LINTING_REPORT.md) - Detailed results
- [DOCUMENTATION_INDEX.md](../../DOCUMENTATION_INDEX.md) - Documentation navigation
- [SINGLE_USER_WORKFLOW.md](../../SINGLE_USER_WORKFLOW.md) - Development workflow

## Support

For issues or questions:

1. Check `.markdownlintrc` and `.prettierrc` in project root
2. Review MARKDOWN_LINTING_REPORT.md for detailed information
3. Run scripts with `--help` flag for usage info

---

**Last Updated:** December 11, 2025  
**Status:** Production Ready
