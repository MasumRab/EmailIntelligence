# Branch Naming Standardization Guide

## Overview

This document outlines the standardized branch naming conventions for the EmailIntelligence project and provides guidance for migration from legacy naming patterns.

## Standardized Naming Conventions

### Branch Types

| Type | Pattern | Description | Examples |
|------|---------|-------------|----------|
| **Feature** | `feature/short-description` | New features and enhancements | `feature/email-filtering`, `feature/api-auth-v2` |
| **Bugfix** | `bugfix/short-description` | Bug fixes and patches | `bugfix/auth-validation`, `bugfix/123-memory-leak` |
| **Hotfix** | `hotfix/short-description` | Urgent production fixes | `hotfix/security-patch`, `hotfix/db-connection-crash` |
| **Refactor** | `refactor/short-description` | Code refactoring and restructuring | `refactor/workflow-engine`, `refactor/database-abstraction` |
| **Documentation** | `docs/short-description` | Documentation updates | `docs/api-reference`, `docs/setup-instructions` |

### Naming Guidelines

- **Format**: `{type}/{short-description}`
- **Case**: Lowercase only
- **Separators**: Use hyphens (-) within descriptions, not underscores (_)
- **Length**: Keep descriptions concise but descriptive (2-5 words max)
- **Issue References**: Include issue numbers when applicable: `bugfix/123-auth-validation`

### Examples of Good Branch Names

```bash
✅ feature/user-dashboard-redesign
✅ bugfix/api-timeout-handling
✅ refactor/database-connection-pooling
✅ docs/installation-guide-update
✅ hotfix/security-vulnerability-patch
```

### Examples of Poor Branch Names

```bash
❌ Feature/new-dashboard          # Wrong case, no separator
❌ fix_bug                        # Wrong format, no separator
❌ feature/new_dashboard_feature  # Underscores instead of hyphens
❌ my_fix_branch                  # Too generic, no type prefix
❌ feature/very_long_description_that_goes_on_and_on # Too long
```

## Migration from Legacy Patterns

### Legacy Patterns to Update

| Legacy Pattern | New Pattern | Example |
|----------------|-------------|---------|
| `feat/*` | `feature/*` | `feat/new-ui` → `feature/new-ui` |
| `fix/*` | `bugfix/*` | `fix/auth-bug` → `bugfix/auth-bug` |
| `feature-*` | `feature/*` | `feature-new-ui` → `feature/new-ui` |
| `fix-*` | `bugfix/*` | `fix-auth-bug` → `bugfix/auth-bug` |
| `bug-*` | `bugfix/*` | `bug-validation` → `bugfix/validation` |
| `doc-*` | `docs/*` | `doc-api-ref` → `docs/api-ref` |

## Migration Tools

### Automated Migration Script

Use the provided migration script to analyze and rename branches:

```bash
# Dry run - see what would be changed
python scripts/branch_rename_migration.py --dry-run

# Execute actual renaming
python scripts/branch_rename_migration.py --execute
```

### Manual Migration

For branches requiring manual review:

```bash
# Check current branch name
git branch --show-current

# Rename branch locally
git branch -m old-name new-name

# Update remote (if exists)
git push origin --delete old-name
git push -u origin new-name
```

## Implementation Timeline

### Phase 1: Documentation & Communication (Week 1)
- [x] Update CONTRIBUTING.md with new standards
- [x] Update documentation examples
- [x] Create migration script
- [ ] Communicate changes to team
- [ ] Update any CI/CD references

### Phase 2: Gradual Adoption (Weeks 2-4)
- [ ] New branches must follow new naming
- [ ] Existing branches can be renamed gradually
- [ ] Provide migration support for team members

### Phase 3: Enforcement (Week 5+)
- [ ] Implement branch name validation (if desired)
- [ ] Regular cleanup of legacy-named branches
- [ ] Update branch protection rules

## CI/CD Considerations

### Current CI/CD Setup
- **Triggers**: Only on `main` and `scientific` branches
- **No Pattern Matching**: CI/CD doesn't use glob patterns for branch names
- **Safe to Change**: Branch naming changes won't break CI/CD pipelines

### Future Enhancements
Consider adding branch name validation to CI/CD:
```yaml
- name: Validate branch name
  run: |
    BRANCH_NAME="${{ github.head_ref }}"
    if [[ ! $BRANCH_NAME =~ ^(feature|bugfix|hotfix|refactor|docs)/[a-z0-9-]+$ ]]; then
      echo "Branch name does not follow naming convention"
      exit 1
    fi
```

## FAQ

### Q: Do I need to rename existing branches?
**A:** Existing branches can remain with their current names and will continue to work. However, we encourage renaming during maintenance windows to maintain consistency.

### Q: What if my branch doesn't fit the standard categories?
**A:** If your work doesn't fit the standard categories, use `feature/` as the default prefix and choose the most appropriate description.

### Q: How do I handle branches with multiple types of changes?
**A:** If a branch contains multiple types of changes (e.g., bug fixes + features), use the primary change type or split into separate branches.

### Q: What about release branches?
**A:** Release branches can use patterns like `release/v1.2.3` or `hotfix/v1.2.4` and are exempt from the standard naming conventions.

### Q: How does this affect pull requests?
**A:** Pull request titles and descriptions should clearly indicate the type of change. The branch name provides additional context but doesn't replace proper PR documentation.

## Support

- **Migration Script**: `scripts/branch_rename_migration.py`
- **Documentation**: This guide and CONTRIBUTING.md
- **Team Communication**: Check Slack/Teams for announcements

## Related Documents

- [CONTRIBUTING.md](../CONTRIBUTING.md) - General contribution guidelines
- [branch_management_recommendations.md](../branch_management_recommendations.md) - Branch lifecycle management
- [BRANCH_ANALYSIS_REPORT.md](../BRANCH_ANALYSIS_REPORT.md) - Current branch analysis</content>
</xai:function_call">Let me create a simple branch name validation script that could be used in CI/CD or as a pre-commit hook. 

<xai:function_call name="create_file">
<parameter name="path">/home/masum/github/EmailIntelligence/scripts/validate_branch_name.py
