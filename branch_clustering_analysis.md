# Detailed Branch Clustering Analysis

## Overview
This analysis clusters the local branches by date (based on last commit dates) and content (based on actual file content differences from git diff stats). The analysis reveals extensive divergence from main branch, with most branches showing massive deletions across multiple file categories.

## Date-Based Clustering

### Early November (Nov 2-7)
- **feature/merge-clean** (Nov 2): Moderate changes focused on merge operations
- **feature/backend-to-src-migration** (Nov 7): Extensive backend restructuring

### Mid November (Nov 8)
- **clean-launch-refactor**: Major cleanup and refactoring (2125 commits)
- **docs/comprehensive-documentation**: Documentation overhaul (1851 commits)
- **feature-notmuch-tagging-1**: Feature development with tagging (796 commits)
- **fix-orchestration-tools-deps**: Dependency fixes (2127 commits)
- **pr-179** & **pr-179-new**: PR implementation (772 commits each)
- **remove-deprecated-markers**: Cleanup operations (1393 commits)

### Late November (Nov 9-10)
- **taskmaster** (Nov 9): Focused new feature (15 commits)
- **001-implement-planning-workflow** (Nov 10): Major workflow implementation (1498 commits)
- **main** (Nov 10): Base branch (1405 commits)
- **orchestration-tools** (Nov 10): Tool development (1543 commits)
- **scientific** (Nov 10): Scientific features (1872 commits)
- **test-hook-debug** (Nov 10): Debugging work (1401 commits)

## Content-Based Clustering (Based on Diff Analysis)

### Extensive Multi-Category Cleanup Branches
These branches show 100+ files changed, predominantly deletions across all major categories:
- **Config Files**: .context-control/, .github/instructions/, .flake8, .pylintrc, package.json, etc.
- **Documentation**: 50+ .md files including README, guides, reports
- **Code Files**: Python (.py), TypeScript (.ts), JavaScript (.js) across src/, modules/, server/
- **Scripts**: 100+ files in scripts/ directory
- **Models**: ML models and configurations
- **Client**: Frontend files in client/
- **Data**: Database and data files
- **Infrastructure**: Docker, nginx, monitoring configs

Include: 001-implement-planning-workflow, clean-launch-refactor, docs-cleanup, docs/comprehensive-documentation, feature-notmuch-tagging-1, feature/backend-to-src-migration, feature/merge-clean, fix-orchestration-tools-deps, main, orchestration-tools, pr-179, pr-179-new, remove-deprecated-markers, scientific, test-hook-debug

### Focused Specialized Branches
- **taskmaster**: Minimal changes (15 commits) focused on .continue/ model/prompt/rule files and core profiles

## Detailed Diff Content Categories

### Dominant Change Patterns
1. **Massive Deletions**: Most branches show extensive file removals, suggesting cleanup or divergence from main
2. **Config Management**: All branches modify .context-control/profiles/ files
3. **Documentation Updates**: Significant changes to .md files across branches
4. **Code Refactoring**: Changes to core Python/TypeScript codebases
5. **Script Management**: Extensive modifications to automation scripts
6. **Model Cleanup**: Removal/replacement of ML models and data

### Change Volume Analysis
- **High Volume**: 1400-2200 commits, 100+ files changed (most branches)
- **Low Volume**: <100 commits, <20 files changed (taskmaster)

### File Type Distribution
- **Markdown (.md)**: 30-50% of changes (documentation)
- **Python (.py)**: 20-30% of changes (backend logic)
- **JSON/YAML**: 10-15% of changes (configuration)
- **TypeScript/JavaScript**: 10-15% of changes (frontend/client)
- **Other**: Scripts, binaries, images (remaining)

## Key Insights
- All branches share a common base (first commit ~2025-06-13), with activity concentrated in November 2025
- High activity on Nov 8 (7 branches) and Nov 10 (5 branches)
- Most branches represent major divergences from main with extensive cleanup operations
- Content differences reveal a pattern of removing accumulated files rather than adding features
- The extensive changes suggest branches may be separate development streams or cleanup efforts
- Taskmaster stands out as a focused, minimal-change branch compared to the massive overhauls in others
- Shared config file modifications indicate some level of coordination across branches
- The predominance of deletions over additions suggests these branches are pruning main's accumulated content