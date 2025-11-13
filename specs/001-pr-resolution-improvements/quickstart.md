# Quickstart Guide: Enhanced PR Resolution with Spec Kit Methodology

## Getting Started

This guide will help you implement the Enhanced PR Resolution system with constitutional validation and automated strategy generation.

### Prerequisites

- Python 3.8+ with Git Python library
- EmailIntelligence CLI (existing)
- TaskMaster system access (optional, for task export)
- Git repository with merge conflicts to resolve

### Installation

```bash
# Clone the EmailIntelligence repository
git clone <repository-url>
cd EmailIntelligence

# Install dependencies
pip install PyYAML gitpython pytest-benchmark

# Install EmailIntelligence CLI
python emailintelligence_cli.py --install

# Verify installation
emailintelligence-cli --version
```

### Initial Setup

#### 1. Initialize Constitutional Rules

```bash
# Create constitutional rule repository
emailintelligence-cli setup-constitution --init --template organizational

# Validate constitution setup
emailintelligence-cli setup-constitution --validate

# Add custom rules (optional)
echo "# Custom rule for Python code style
- rule: *.py files must follow PEP 8
- pattern: \.py$
- severity: warning
- description: Python files should follow PEP 8 style guidelines
" >> constitutions/coding-standards.md
```

#### 2. Configure Project Settings

```bash
# Create project configuration
cat > .emailintelligence.yml << EOF
project:
  name: "MyProject"
  repository_path: "."
  default_branch: "main"
constitutional_rules:
  path: "./constitutions"
  auto_load: true
performance:
  baseline_file: ".resolution-baseline.json"
  regression_threshold: 0.1
taskmaster:
  enabled: true
  project_root: "."
  auto_export: true
EOF
```

## Basic Usage

### Step 1: Create Specification

```bash
# Detect conflicts and create specification
emailintelligence-cli create-specification \
  --branch feature/new-feature \
  --base main \
  --output spec-conflicts-$(date +%Y%m%d).md \
  --template detailed

# Review generated specification
cat spec-conflicts-20251112.md
```

**Example Specification Output:**
```yaml
---
spec_id: "550e8400-e29b-41d4-a716-446655440000"
version: "1.0.0"
title: "Feature Implementation Conflicts"
created_at: "2025-11-12T19:30:00Z"
author: "developer"
branch: "feature/new-feature"
complexity_score: 0.75
---

# Conflicting Changes Detected

## Text Conflicts
- `src/utils/helper.py` (lines 15-23): Function signature mismatch
- `tests/test_helper.py` (lines 45-52): Test expectations differ

## Binary Conflicts  
- `docs/diagram.png` (renamed: diagram-new.png, similarity: 0.85)
- `config/settings.json` (permission change: 755 → 644)

## Structural Conflicts
- `src/old_module/` moved to `src/legacy/` 
- `README.md` deleted and recreated with different content
```

### Step 2: Validate Constitutional Compliance

```bash
# Check compliance against constitutional rules
emailintelligence-cli validate-constitution \
  --spec spec-conflicts-20251112.md \
  --severity-filter warning

# Output example:
# ✅ Constitutional Compliance: 85%
# ⚠️  Warning: Python files should follow PEP 8 style
#    Location: src/utils/helper.py:45
#    Fix available: Apply autopep8 formatting
```

### Step 3: Generate Resolution Strategy

```bash
# Create conservative resolution strategy
emailintelligence-cli generate-strategy \
  --spec spec-conflicts-20251112.md \
  --strategy-type conservative \
  --risk-tolerance low \
  --include-rollback true \
  --task-export true

# Review strategy details
emailintelligence-cli generate-strategy \
  --spec spec-conflicts-20251112.md \
  --output strategy-details.json
```

**Example Strategy Output:**
```json
{
  "strategy": {
    "name": "Conservative Resolution Strategy",
    "risk_score": 0.25,
    "phases": [
      {
        "name": "Pre-resolution Validation",
        "estimated_duration": 30,
        "tasks": [
          "Create worktree isolation",
          "Backup current branch state", 
          "Validate constitutional compliance"
        ]
      },
      {
        "name": "Text Conflict Resolution",
        "estimated_duration": 120,
        "tasks": [
          "Merge src/utils/helper.py",
          "Update function signatures",
          "Verify test compatibility"
        ]
      },
      {
        "name": "Validation and Cleanup", 
        "estimated_duration": 60,
        "tasks": [
          "Run full test suite",
          "Update documentation",
          "Cleanup worktrees"
        ]
      }
    ]
  }
}
```

### Step 4: Execute Resolution (Dry Run First)

```bash
# Preview changes without executing
emailintelligence-cli execute-resolution \
  --spec spec-conflicts-20251112.md \
  --strategy conservative-strategy-id \
  --dry-run

# Review preview output
# ▶️  Phase 1: Pre-resolution Validation
#    - Create worktree: /tmp/resolution-worktree-12345
#    - Backup current state
#    
# ▶️  Phase 2: Text Conflict Resolution  
#    - Conflict: src/utils/helper.py:15-23
#    - Proposed: Merge function signatures
#    - Impact: 2 files affected
#    
# ✅ Preview complete - 3 phases, 15 minutes estimated

# Execute full resolution
emailintelligence-cli execute-resolution \
  --spec spec-conflicts-20251112.md \
  --strategy conservative-strategy-id \
  --cleanup true
```

### Step 5: Export Tasks (Optional)

```bash
# Export resolution phases to TaskMaster
emailintelligence-cli export-tasks \
  --spec spec-conflicts-20251112.md \
  --strategy conservative-strategy-id \
  --project-root . \
  --priority-default medium

# View generated tasks
emailintelligence-cli export-tasks \
  --spec spec-conflicts-20251112.md \
  --output task-export.json
```

## Advanced Usage

### Custom Constitutional Rules

Create your own constitutional rules:

```bash
# Create custom rule file
cat > constitutions/security.md << EOF
# Security Validation Rules

## API Key Protection
- rule: API keys should not be committed
- pattern: (api[_-]?key|secret[_-]?key)\s*=\s*['"][^'"]+['"]
- severity: critical
- description: API keys must not be hardcoded in source files
- auto_fix: false

## SQL Injection Prevention  
- rule: Raw SQL queries should use parameterized statements
- pattern: (SELECT|INSERT|UPDATE|DELETE).*%s.*
- severity: error
- description: Use parameterized queries to prevent SQL injection
- auto_fix: false

## File Permissions
- rule: Configuration files should have restricted permissions
- pattern: \.yml$|\.yaml$|\.json$
- severity: warning
- description: Configuration files should have 644 permissions
- auto_fix: true
- fix_command: chmod 644 {file_path}
EOF

# Reload constitutional rules
emailintelligence-cli setup-constitution --validate
```

### Performance Benchmarking

```bash
# Establish performance baseline
emailintelligence-cli performance-benchmark \
  --baseline \
  --conflict-type all \
  --iterations 20

# Compare performance against baseline
emailintelligence-cli performance-benchmark \
  --compare \
  --conflict-type text

# Performance report output:
# 📊 Resolution Performance Report
# 
# Text Conflicts: 45.2s average (65% improvement)
# Binary Conflicts: 120.5s average (52% improvement)  
# Structural Conflicts: 300.8s average (58% improvement)
# 
# Overall: 58% faster than manual resolution ✅
# Confidence: 92% (based on 100 test scenarios)
```

### Integration with CI/CD

```yaml
# .github/workflows/pr-resolution.yml
name: PR Resolution Validation
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  validate-resolution:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup EmailIntelligence CLI
        run: |
          python emailintelligence_cli.py --install
      
      - name: Check for merge conflicts
        run: |
          git checkout ${{ github.base_ref }}
          git checkout ${{ github.head_ref }}
          if git merge --no-commit ${{ github.base_ref }}; then
            echo "Conflicts detected"
            git merge --abort
            emailintelligence-cli create-specification \
              --branch ${{ github.head_ref }} \
              --base ${{ github.base_ref }} \
              --output spec-${{ github.sha }}.md
          else
            echo "No conflicts detected"
          fi
```

## Troubleshooting

### Common Issues

#### 1. Constitutional Rule Loading Errors
```bash
# Error: Constitutional rule pattern invalid
# Solution: Check regex patterns in rule files
emailintelligence-cli setup-constitution --validate

# Debug: Test individual rule
python -c "import re; re.compile('your-pattern-here')"
```

#### 2. Git Worktree Permission Issues
```bash
# Error: Cannot create worktree
# Solution: Check Git version and permissions
git --version
git worktree --version
chmod -R 755 .git
```

#### 3. TaskMaster Integration Failures
```bash
# Error: Task export failed
# Solution: Check TaskMaster configuration
emailintelligence-cli export-tasks \
  --spec spec.conflicts.md \
  --debug

# Verify TaskMaster connection
python -c "from emailintelligence_cli import EmailIntelligenceCLI; cli = EmailIntelligenceCLI(); cli.test_taskmaster_connection()"
```

### Performance Optimization

#### Caching Configuration
```bash
# Enable constitutional rule caching
export EMAILINTELLIGENCE_CACHE_RULES=true

# Configure cache directory  
export EMAILINTELLIGENCE_CACHE_DIR="/tmp/.emailintelligence-cache"

# Set cache expiration (seconds)
export EMAILINTELLIGENCE_CACHE_TTL=3600
```

#### Parallel Processing
```bash
# Increase worktree pool for parallel resolution
emailintelligence-cli execute-resolution \
  --spec spec.conflicts.md \
  --worktree-pool 5 \
  --parallel-phases

# Note: Requires sufficient system resources
```

## Best Practices

### 1. Always Use Dry Run First
```bash
# Preview changes before execution
emailintelligence-cli execute-resolution --dry-run
```

### 2. Establish Performance Baselines
```bash
# Regular baseline updates for accurate metrics
emailintelligence-cli performance-benchmark --baseline
```

### 3. Maintain Constitutional Rules
```bash
# Regular rule validation and updates
emailintelligence-cli setup-constitution --validate

# Review rule effectiveness and adjust
cat constitutions/*.md | grep -E "severity:|pattern:"
```

### 4. Version Control Specifications
```bash
# Commit specifications with resolution decisions
git add spec-*.md strategy-*.json
git commit -m "feat: Add PR resolution specification and strategy"
```

---

**Quickstart Status**: ✅ Complete
**Next Steps**: Proceed to task breakdown and implementation
**Support**: Check troubleshooting section or create GitHub issue