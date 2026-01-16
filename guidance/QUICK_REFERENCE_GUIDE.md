# EmailIntelligence CLI Integration & Architecture Alignment - Quick Reference

## Overview
Quick reference guide for integrating advanced CLI features with interface-based architecture and merging branches with different architectural approaches.

## CLI Integration Framework Commands

### Installation
```bash
# Install CLI features in minimal mode (core functionality only)
./.cli_framework/install.sh minimal

# Install CLI features in full mode (all features with dependencies)
./.cli_framework/install.sh full
```

### Safe Branch Merging
```bash
# Merge CLI features to another branch with backup creation
./.cli_framework/merge_to_branch.sh --target <branch_name> --mode <minimal|full>

# Examples:
./.cli_framework/merge_to_branch.sh --target main --mode minimal
./.cli_framework/merge_to_branch.sh --target scientific --mode full
```

## Key Architecture Components

### Interface-Based Design
- `src/core/interfaces.py` - Core interfaces (IConflictDetector, IConstitutionalAnalyzer, etc.)
- `src/core/exceptions.py` - Custom exception hierarchy
- `src/git/repository.py` - Repository operations wrapper

### CLI Enhancement Modules
- `emailintelligence_cli.py` - Enhanced CLI with constitutional analysis
- `src/resolution/auto_resolver.py` - Automatic conflict resolution
- `src/resolution/semantic_merger.py` - Semantic merging capabilities
- `src/analysis/constitutional/analyzer.py` - Constitutional analysis engine
- `src/strategy/generator.py` - Strategy generation
- `src/strategy/risk_assessor.py` - Risk assessment

## Merge Process Checklist

### Before Merging
- [ ] Create backup of target branch: `git branch backup-<branch_name>-$(date +%Y%m%d)`
- [ ] Analyze architectural differences between branches
- [ ] Identify core functionality that must be preserved
- [ ] Map import path dependencies
- [ ] Plan compatibility layer implementation

### During Merge
- [ ] Implement factory pattern for service compatibility
- [ ] Create adapter layers for different architectural components
- [ ] Standardize import paths consistently
- [ ] Use lazy initialization to avoid import-time issues
- [ ] Test core functionality at each step

### After Merge
- [ ] Verify service startup works with both architectural patterns
- [ ] Test all critical functionality is preserved
- [ ] Ensure performance optimizations from both branches are maintained
- [ ] Validate security measures are not compromised
- [ ] Run comprehensive test suites

## Common Issues and Solutions

### Import Path Conflicts
**Issue**: Import errors after merging
**Solution**: Standardize import paths using consistent `src/` structure

### Service Startup Failures
**Issue**: Application fails to start after merge
**Solution**: Verify factory pattern implementation and service configuration

### Missing Dependencies
**Issue**: Runtime errors due to missing modules
**Solution**: Ensure all related components are migrated together

### Interface Implementation Mismatches
**Issue**: Abstract method errors
**Solution**: Verify all interface methods are properly implemented

## Key Commands

### Git Operations
```bash
# Create backup branch
git branch backup-branch-name-$(date +%Y%m%d)

# Switch to target branch
git checkout target-branch

# Copy files from source branch
git checkout source-branch -- path/to/files

# Commit changes
git add .
git commit -m "feat: Integrate advanced CLI features"

# Push changes
git push origin target-branch
```

### Architecture Validation
```bash
# Verify factory pattern implementation
python -c "from src.main import create_app; app = create_app(); print('Factory pattern working')"

# Test CLI functionality
python emailintelligence_cli.py --help
```

## Success Metrics

A successful integration should achieve:
- ✅ Remote branch service startup patterns work
- ✅ All local branch functionality preserved
- ✅ Advanced CLI features with constitutional analysis operational
- ✅ Interface-based architecture properly implemented
- ✅ Performance optimizations maintained
- ✅ Security measures intact
- ✅ Test suites pass
- ✅ No runtime errors in core functionality

## Rollback Procedure

If issues occur:
1. Switch to backup branch: `git checkout backup-branch-name-date`
2. Verify functionality works on backup
3. Document specific issues that occurred
4. Analyze root cause of problems
5. Implement fixes in isolated environment
6. Re-attempt merge with corrections

## Red Flags

Watch for these warning signs:
- Service configurations pointing to non-existent files
- Expected factory functions that don't exist
- Missing architectural components that other components depend on
- Import-time initialization of resources
- Conflicts in core application entry points
- Mixed import paths (old and new structures in same branch)
- Components that work in isolation but break when combined