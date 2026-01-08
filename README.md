# EmailIntelligence CLI

**AI-powered git worktree-based conflict resolution tool**

EmailIntelligence CLI implements a structured workflow for intelligent branch merge conflict resolution using constitutional/specification-driven analysis and spec-kit strategies.

## 🚀 Quick Start

### Installation

```bash
# Make the CLI executable
chmod +x emailintelligence_cli.py

# Optional: Create a symbolic link for easy access
ln -s $(pwd)/emailintelligence_cli.py /usr/local/bin/eai
```

### Basic Usage

```bash
# Setup resolution workspace for PR #123
eai setup-resolution --pr 123 --source-branch feature/auth --target-branch main

# Analyze constitutional compliance
eai analyze-constitutional --pr 123 --constitution ./constitutions/auth.yaml

# Develop spec-kit resolution strategy
eai develop-spec-kit-strategy --pr 123 --worktrees --interactive

# Execute content alignment
eai align-content --pr 123 --interactive --checkpoint-each-step

# Validate resolution
eai validate-resolution --pr 123 --comprehensive
```

## 📋 Overview

EmailIntelligence CLI transforms complex git merge conflicts into structured, analyzable problems through:

- **Git Worktree Management**: Isolated analysis environments for clean conflict detection
- **Constitutional Analysis**: Rule-based compliance checking against organizational standards
- **Spec-Kit Strategy Development**: Intelligent resolution planning with enhancement preservation
- **Interactive Workflows**: Step-by-step guidance with human-in-the-loop decision making

## 🏗️ Architecture

### Core Components

1. **Resolution Workspace**: Isolated git worktree environment for conflict analysis
2. **Constitutional Framework**: YAML/JSON-based rule sets for compliance validation
3. **Spec-Kit Engine**: Strategy generation and execution framework
4. **Validation System**: Multi-level testing and quality assurance

### Directory Structure

```
/
├── .git/
│   └── worktrees/              # Isolated worktree directories
├── resolution-workspace/       # Resolution metadata and progress
├── .emailintelligence/
│   ├── config.yaml             # Tool configuration
│   ├── constitutions/          # Constitutional rule files
│   └── strategies/            # Generated resolution strategies
└── emailintelligence_cli.py    # Main CLI tool
```

## 🎯 Commands

### setup-resolution

Initialize a resolution workspace for a specific PR.

```bash
eai setup-resolution --pr 123 --source-branch feature/auth --target-branch main [options]
```

**Arguments:**
- `--pr`: Pull request number (required)
- `--source-branch`: Source branch with conflicts (required)
- `--target-branch`: Target branch for merging (required)

**Options:**
- `--constitution`: Constitution file(s) to load (repeatable)
- `--spec`: Specification file(s) (repeatable)
- `--dry-run`: Preview setup without creating worktrees

**Output:**
- Resolution workspace metadata
- Conflict detection results
- Next steps recommendations

### analyze-constitutional

Analyze conflicts against loaded constitutional rules.

```bash
eai analyze-constitutional --pr 123 --constitution ./constitutions/auth.yaml [options]
```

**Arguments:**
- `--pr`: Pull request number (required)

**Options:**
- `--constitution`: Constitution file(s) to analyze against (repeatable)
- `--interactive`: Enable interactive analysis mode

**Output:**
- Constitutional compliance scores
- Critical issues identification
- Resolution recommendations

### develop-spec-kit-strategy

Generate intelligent resolution strategy based on conflict analysis.

```bash
eai develop-spec-kit-strategy --pr 123 --worktrees --interactive [options]
```

**Arguments:**
- `--pr`: Pull request number (required)

**Options:**
- `--worktrees`: Use worktree-based analysis
- `--alignment-rules`: Path to alignment rules file
- `--interactive`: Enable interactive strategy development
- `--review-required`: Require team review

**Output:**
- Multi-phase resolution strategy
- Enhancement preservation plans
- Risk assessment and mitigation

### align-content

Execute content alignment based on developed strategy.

```bash
eai align-content --pr 123 --interactive --checkpoint-each-step [options]
```

**Arguments:**
- `--pr`: Pull request number (required)

**Options:**
- `--strategy`: Path to strategy JSON file
- `--dry-run`: Preview alignment without applying changes
- `--preview-changes`: Show preview of changes
- `--interactive`: Interactive alignment with step-by-step confirmation
- `--checkpoint-each-step`: Checkpoint after each step

**Output:**
- Phase-by-phase execution results
- Alignment scores and metrics
- Conflict resolution status

### validate-resolution

Validate completed content alignment.

```bash
eai validate-resolution --pr 123 --comprehensive [options]
```

**Arguments:**
- `--pr`: Pull request number (required)

**Options:**
- `--comprehensive`: Run comprehensive validation
- `--quick`: Run quick validation check
- `--tests`: Specific test suites to run (comma-separated)

**Output:**
- Validation test results
- Constitutional compliance status
- Overall resolution quality score

### version

Show version information.

```bash
eai version
```

## 🆕 Modular CLI System

The CLI now supports a new modular command architecture built on SOLID principles, enabling better maintainability, testing, and extensibility.

### Command Modes

The CLI operates in two modes:

**Legacy Mode** (default):
```bash
eai setup-resolution --pr 123 --source-branch feature/auth --target-branch main
```

**Modular Mode** (recommended):
```bash
eai modular analyze /path/to/repo --base-branch main
eai modular validate
eai modular analyze-history --output report.txt
```

### Modular Commands

| Command | Description | Status |
|---------|-------------|--------|
| `analyze` | Analyze repository conflicts between branches | ✅ Implemented |
| `resolve` | Resolve specific conflicts using strategies | ✅ Implemented |
| `validate` | Run validation checks on the codebase | ✅ Implemented |
| `analyze-history` | Analyze git commit history and patterns | ✅ Implemented |
| `plan-rebase` | Generate optimal rebase plans | ✅ Implemented |

### Architecture Benefits

- **SOLID Design**: Single responsibility, dependency injection, interface segregation
- **Agent Coordination**: Commands assigned to specialized agents (analyze-agent, resolve-agent, etc.)
- **Comprehensive Testing**: Full unit and integration test coverage
- **Backward Compatible**: Legacy commands continue to work unchanged
- **Extensible**: Easy to add new commands following established patterns

### For Developers

The modular system is designed for collaborative development:
- Each command is an independent class implementing the `Command` interface
- Dependency injection enables comprehensive testing
- Agent-based coordination supports complex workflows
- Complete documentation in `docs/COMMAND_SPECIFICATION.md`

See `docs/CLI_COMMANDS.md` for detailed command reference and examples.

## ⚙️ Configuration

### Configuration File

The tool creates `~/.emailintelligence/config.yaml` with default settings:

```yaml
constitutional_framework:
  default_constitutions: []
  compliance_threshold: 0.8

worktree_settings:
  cleanup_on_completion: true
  max_worktrees: 10

analysis_settings:
  enable_ai_analysis: false
  detailed_reporting: true
```

### Constitutional Files

Constitutional rules define organizational standards and requirements.

**Example Constitution (auth.yaml):**
```yaml
name: "Authentication Security Constitution"
version: "1.0"
requirements:
  - name: "Secure password hashing"
    type: "MUST"
    validation: "bcrypt minimum cost factor 12"
    
  - name: "JWT token validation"
    type: "MUST"
    validation: "Signature and expiration validation"
    
  - name: "Session timeout"
    type: "SHOULD"
    validation: "Configurable timeout within 30 minutes"
    
  - name: "Rate limiting"
    type: "SHOULD"
    validation: "Per-user and per-IP rate limits"
```

**Requirement Types:**
- `MUST`: Critical requirements that must be satisfied
- `REQUIRED`: Important requirements with some flexibility
- `SHOULD`: Recommended standards for best practices
- `SHOULD_NOT`: Practices to avoid

## 📊 Workflow

### 1. Setup Phase
- Create isolated resolution workspace
- Initialize dual worktree environment
- Detect and catalog conflicts
- Load constitutional frameworks

### 2. Analysis Phase
- Analyze conflicts against constitutional rules
- Generate compliance assessment
- Identify critical issues and recommendations
- Create interactive analysis reports

### 3. Strategy Development Phase
- Develop multi-phase resolution strategy
- Plan enhancement preservation
- Assess risks and mitigation approaches
- Generate interactive strategy approval process

### 4. Execution Phase
- Execute content alignment phases
- Apply constitutional validation
- Track alignment scores and progress
- Handle interactive confirmations and checkpoints

### 5. Validation Phase
- Run comprehensive validation tests
- Verify constitutional compliance
- Assess overall resolution quality
- Generate validation reports

## 🔍 Examples

### Basic Resolution Workflow

```bash
# 1. Setup resolution environment
eai setup-resolution \
  --pr 142 \
  --source-branch feature/user-auth \
  --target-branch main \
  --constitution ./constitutions/security.yaml

# 2. Analyze compliance
eai analyze-constitutional \
  --pr 142 \
  --constitution ./constitutions/security.yaml \
  --interactive

# 3. Develop strategy
eai develop-spec-kit-strategy \
  --pr 142 \
  --worktrees \
  --interactive

# 4. Execute alignment
eai align-content \
  --pr 142 \
  --interactive \
  --checkpoint-each-step

# 5. Validate results
eai validate-resolution \
  --pr 142 \
  --comprehensive
```

### Advanced Configuration

```bash
# Use multiple constitutions
eai analyze-constitutional \
  --pr 142 \
  --constitution ./constitutions/security.yaml \
  --constitution ./constitutions/api.yaml \
  --constitution ./constitutions/database.yaml

# Custom alignment rules
eai develop-spec-kit-strategy \
  --pr 142 \
  --alignment-rules ./alignment-rules/custom.yaml \
  --interactive \
  --review-required

# Dry-run preview
eai setup-resolution \
  --pr 142 \
  --source-branch feature/auth \
  --target-branch main \
  --dry-run
```

## 🛠️ Development

### Requirements

- Python 3.7+
- Git (with worktree support)
- Optional: PyYAML for YAML configuration

### Dependencies

```bash
# Optional YAML support
pip install PyYAML
```

### Testing

```bash
# Make executable
chmod +x emailintelligence_cli.py

# Run basic functionality test
eai version

# Test in a git repository
cd /path/to/git/repo
eai setup-resolution --pr 1 --source-branch test --target-branch main --dry-run
```

### Customization

The tool is designed for extensibility:

1. **Custom Constitutions**: Add organization-specific rule sets
2. **Alignment Rules**: Define custom resolution strategies
3. **Validation Suites**: Extend validation testing frameworks
4. **Integration Hooks**: Connect with CI/CD pipelines

## 🚨 Troubleshooting

### Common Issues

**"Not in a git repository"**
- Ensure you're running from a git repository root
- Check that `.git` directory exists

**"No resolution workspace found"**
- Run `setup-resolution` first
- Check that resolution metadata exists in `resolution-workspace/`

**"Constitution file not found"**
- Verify file path exists
- Check permissions and file format
- Ensure YAML/JSON syntax is valid

**"Worktree creation failed"**
- Ensure sufficient disk space
- Check git version supports worktrees (git 2.5+)
- Verify write permissions to `.git/worktrees/`

### Debug Mode

```bash
# Use dry-run to preview operations
eai setup-resolution --pr 123 --source-branch feature --target-branch main --dry-run

# Check metadata manually
cat resolution-workspace/pr-123-metadata.json
```

### Log Files

Resolution operations generate metadata in `resolution-workspace/`:
- `pr-{number}-metadata.json`: Complete resolution metadata
- Strategy files and analysis results
- Validation reports and test results

## 🤝 Contributing

### Code Style
- Follow PEP 8 guidelines
- Use type hints for all function parameters
- Include comprehensive docstrings
- Maintain test coverage for new features

### Adding Features
1. Extend base classes for new functionality
2. Maintain backward compatibility
3. Add comprehensive error handling
4. Include integration tests

### Constitutional Framework
- Create organization-specific constitutions
- Test compliance scoring logic
- Validate requirement categorization
- Document validation criteria

## 📝 License

This tool is provided as-is for conflict resolution automation. Modify and adapt according to your organization's needs.

## 🆘 Support

For issues and feature requests:
1. Check troubleshooting section
2. Review metadata files in `resolution-workspace/`
3. Use `--dry-run` for safe testing
4. Validate git repository and permissions

---

**EmailIntelligence CLI v1.0.0** - Transforming git conflicts into structured solutions