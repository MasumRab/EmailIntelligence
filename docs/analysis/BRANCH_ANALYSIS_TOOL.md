# Branch Analysis Tool - Standalone Documentation

## Overview

**Standalone Branch Analysis Tool** - No AI assistant required!

A universal, tool-agnostic branch analysis utility for Git repositories. Works independently without any AI assistant framework.

### Features

- ✅ **No AI Assistant Required** - Runs standalone
- ✅ **Branch Synchronization Status** - Ahead/behind detection
- ✅ **Orchestration Branch Detection** - Identifies orchestration branches
- ✅ **Backend Migration Issues** - Finds old import statements
- ✅ **Temporary Directory Detection** - Locates backup/temp folders
- ✅ **Duplicate Documentation** - Finds docs outside docs/
- ✅ **Launch Script Analysis** - Checks for orchestration features
- ✅ **Multiple Output Formats** - Text and JSON
- ✅ **Exit Codes** - Suitable for CI/CD integration

---

## Installation

No installation required! Just Python 3.7+.

```bash
# Make executable (optional)
chmod +x scripts/branch_analysis_tool.py
```

---

## Usage

### Basic Analysis

```bash
# Run full analysis
python scripts/branch_analysis_tool.py

# Or with executable permission
./scripts/branch_analysis_tool.py
```

### Output Formats

```bash
# Text report (default)
python scripts/branch_analysis_tool.py

# JSON output (for programmatic use)
python scripts/branch_analysis_tool.py --json
```

### Advanced Options

```bash
# Include remote branches
python scripts/branch_analysis_tool.py --include-remotes

# Check for stale branches
python scripts/branch_analysis_tool.py --check-stale

# Custom stale threshold (default: 90 days)
python scripts/branch_analysis_tool.py --check-stale --max-stale-days 30

# Analyze different repository
python scripts/branch_analysis_tool.py --repo /path/to/repo

# Auto-fix issues (when available)
python scripts/branch_analysis_tool.py --auto-fix
```

---

## Output Examples

### Text Report

```
================================================================================
BRANCH ANALYSIS REPORT
================================================================================

Repository: /home/masum/github/EmailIntelligenceAider
Current Branch: orchestration-tools
Analysis Time: 2026-03-15T22:12:09.344615
Total Branches: 11

--------------------------------------------------------------------------------
BRANCH STATUS SUMMARY
--------------------------------------------------------------------------------

🎯 Orchestration Branches (5):
   • 001-orchestration-tools-consistency
   • 001-orchestration-tools-verification-review
   • orchestration-tools
   • orchestration-tools-changes-emailintelligence-cli-20251112
   • orchestration-tools-changes-recovery-framework

⬆️  Branches Needing Push (0):

⬇️  Branches Needing Pull (1):
   • main (2 commits behind)

⚠️  Diverged Branches (1):
   • scientific (3 ahead, 1460 behind)

--------------------------------------------------------------------------------
ISSUES DETECTED
--------------------------------------------------------------------------------

🟠 HIGH (2):
   • [migration] scripts/currently_disabled/temp_email_nodes.py
     Old backend import detected
   • [migration] scripts/currently_disabled/test_enhanced_filtering.py
     Old backend import detected

🔵 LOW (1):
   • [cleanup] backlog
     Temporary/backup directory detected

ℹ️ INFO (2):
   • [launch_script] launch.py
     Basic launch script (no orchestration features)

--------------------------------------------------------------------------------
METRICS
--------------------------------------------------------------------------------

📊 Status Distribution:
   • up_to_date: 9
   • behind: 1
   • diverged: 1

📈 Summary:
   • Branches needing push: 1
   • Branches needing pull: 2

================================================================================
Analysis complete!
================================================================================
```

### JSON Output

```json
{
  "timestamp": "2026-03-15T22:12:24.350719",
  "repository": "/home/masum/github/EmailIntelligenceAider",
  "current_branch": "orchestration-tools",
  "total_branches": 11,
  "orchestration_branches": [
    "001-orchestration-tools-consistency",
    "orchestration-tools"
  ],
  "taskmaster_branches": [],
  "branches_needing_push": [],
  "branches_needing_pull": [
    {
      "name": "main",
      "ahead": 0,
      "behind": 2
    }
  ],
  "diverged_branches": [
    {
      "name": "scientific",
      "ahead": 3,
      "behind": 1460
    }
  ],
  "issues": [
    {
      "severity": "high",
      "category": "migration",
      "location": "scripts/example.py",
      "description": "Old backend import detected",
      "suggestion": "Update to 'from src.backend' or 'from backend.src'"
    }
  ],
  "metrics": {
    "total_branches": 11,
    "orchestration_branches": 5,
    "taskmaster_branches": 0,
    "status_distribution": {
      "up_to_date": 9,
      "behind": 1,
      "diverged": 1
    }
  }
}
```

---

## Exit Codes

The tool returns appropriate exit codes for CI/CD integration:

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success - no critical or high severity issues |
| 1 | High severity issues detected |
| 2 | Critical severity issues detected |

### CI/CD Example

```yaml
# .gitlab-ci.yml
branch_analysis:
  script:
    - python scripts/branch_analysis_tool.py --json > analysis.json
  artifacts:
    reports:
      codequality: analysis.json
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

---

## Issue Categories

### Migration Issues (High Severity)
- Old backend import statements
- Deprecated API usage
- Legacy code patterns

### Cleanup Issues (Low Severity)
- Temporary directories
- Backup folders
- Unused code

### Documentation Issues (Medium Severity)
- Duplicate documentation
- Docs outside docs/ directory
- Outdated README files

### Launch Script Issues (Info Severity)
- Missing orchestration features
- Inconsistent patterns
- Basic functionality only

---

## Programmatic Usage

### Python API

```python
from scripts.branch_analysis_tool import BranchAnalyzer, print_text_report
from pathlib import Path

# Create analyzer
analyzer = BranchAnalyzer(Path('/path/to/repo'))

# Run analysis
result = analyzer.run_full_analysis(include_remotes=False)

# Access results
print(f"Total branches: {result.total_branches}")
print(f"Current branch: {result.current_branch}")
print(f"Issues found: {len(result.issues)}")

# Check specific issues
for issue in result.issues:
    if issue.severity == 'critical':
        print(f"Critical: {issue.location} - {issue.description}")

# Generate metrics
metrics = result.metrics
print(f"Branches needing push: {metrics['branches_needing_push']}")
```

### Parse JSON Output

```bash
# Using jq
python scripts/branch_analysis_tool.py --json | jq '.issues[] | select(.severity=="high")'

# Count issues by severity
python scripts/branch_analysis_tool.py --json | jq '.issues | group_by(.severity) | map({severity: .[0].severity, count: length})'
```

---

## Comparison: Standalone vs Smart-Understand

| Feature | Standalone Tool | Smart-Understand |
|---------|----------------|------------------|
| AI Assistant Required | ❌ No | ✅ Yes |
| Architecture Analysis | Basic | Deep (with AI) |
| Quantitative Metrics | ✅ Yes | ✅ Yes |
| Mermaid Diagrams | ❌ No | ✅ Yes |
| Shell vs Python Analysis | ❌ No | ✅ Yes |
| CI/CD Integration | ✅ Excellent | ⚠️ Manual |
| Speed | Fast (seconds) | Slow (minutes) |
| Dependencies | Python 3.7+ | AI assistant + Python |

### When to Use Standalone

- ✅ Quick branch status checks
- ✅ CI/CD pipeline integration
- ✅ Automated scripts
- ✅ No AI assistant available
- ✅ Frequent analysis needed

### When to Use Smart-Understand

- ✅ Deep architecture analysis
- ✅ Comprehensive recommendations
- ✅ Mermaid diagrams needed
- ✅ Shell vs Python comparison
- ✅ Strategic planning

---

## Troubleshooting

### Git Not Found

```
Error: Git not found
```

**Solution**: Install git or ensure it's in your PATH.

```bash
# Check git installation
which git
git --version

# Install if needed
sudo apt-get install git  # Debian/Ubuntu
brew install git  # macOS
```

### Permission Denied

```
PermissionError: [Errno 13] Permission denied
```

**Solution**: Make script executable.

```bash
chmod +x scripts/branch_analysis_tool.py
```

### Not a Git Repository

```
fatal: not a git repository
```

**Solution**: Run from within a git repository or specify path.

```bash
python scripts/branch_analysis_tool.py --repo /path/to/repo
```

---

## Advanced Examples

### Find Stale Branches

```bash
# Find branches not updated in 90+ days
python scripts/branch_analysis_tool.py --check-stale --max-stale-days 90

# Find branches not updated in 30+ days
python scripts/branch_analysis_tool.py --check-stale --max-stale-days 30
```

### Migration Audit

```bash
# Check for backend migration issues
python scripts/branch_analysis_tool.py --json | jq '.issues[] | select(.category=="migration")'
```

### Branch Cleanup Planning

```bash
# Find all diverged branches
python scripts/branch_analysis_tool.py --json | jq '.diverged_branches'

# Find branches needing attention
python scripts/branch_analysis_tool.py --json | jq '
  .branches_needing_push + .branches_needing_pull | 
  map({name: .name, action: (if .ahead > 0 then "push" else "pull" end)})
'
```

---

## Integration with Other Tools

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

python scripts/branch_analysis_tool.py --json > /tmp/branch_analysis.json

# Check for critical issues
if jq -e '.issues[] | select(.severity=="critical")' /tmp/branch_analysis.json > /dev/null; then
    echo "❌ Critical issues detected!"
    exit 1
fi

exit 0
```

### GitHub Actions

```yaml
name: Branch Analysis

on:
  push:
    branches: [main, develop]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run branch analysis
        run: python scripts/branch_analysis_tool.py --json > analysis.json
      
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: branch-analysis
          path: analysis.json
```

---

## Performance

Typical performance characteristics:

| Repository Size | Analysis Time |
|-----------------|---------------|
| Small (<100 files) | <1 second |
| Medium (100-1000 files) | 1-3 seconds |
| Large (>1000 files) | 3-10 seconds |

**Note**: Performance depends on number of branches and files, not repository size.

---

## Contributing

To extend the tool with new checks:

1. Add new check method to `BranchAnalyzer` class
2. Call method in `run_full_analysis()`
3. Add issue category to documentation
4. Add tests for new functionality

---

## See Also

- **Smart-Understand Analysis**: For deep architecture analysis with AI assistance
- **Architecture Report**: `docs/analysis/branch_sync_architecture_report.md`
- **Quick Start**: `docs/analysis/QUICK_START.md`
- **Metrics**: `docs/analysis/metrics.json`

---

**Tool Version**: 1.0.0  
**Last Updated**: 2026-03-15  
**Python Requirement**: 3.7+  
**License**: Apache 2.0
