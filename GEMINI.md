# Gemini/Jules Agent Integration Guide - PR Resolution Enhancement

## ⚠️ Jules-Specific Agent Workflow

**Important**: This guide is specifically for Jules (Google's agentic IDE at jules.google.com) users working on the Enhanced PR Resolution with Spec Kit Methodology project.

**Jules Compatibility Notes**:
- Jules has its own task management and workflow systems
- This guide adapts Task Master patterns to Jules capabilities
- Learn from these patterns and integrate with Jules' native workflows
- All examples show Jules-specific implementation approaches

---

## Quick Start for Jules Users

### 1. Project Context Setup

**Project Location**: `specs/001-pr-resolution-improvements/`

**Key Files for Jules**:
- `spec.md` - Complete feature specification  
- `tasks-reordered.md` - **Agent-friendly task order with immediate testability**
- `plan.md` - Implementation architecture and technical decisions
- `cli-improvements.md` - CLI enhancement specifications
- `quickstart.md` - Complete usage guide

### 2. Jules Workflow Adaptation

**Instead of Task Master commands**, use Jules' native features:

```bash
# Use Jules' file explorer to navigate to:
specs/001-pr-resolution-improvements/

# Use Jules' task creation to implement phases from:
tasks-reordered.md (lines 16-184)
```

---

## Agent-Friendly Implementation Strategy

### Phase-by-Phase Development (Jules-Optimized)

**Each phase produces immediately testable outputs with Jules-compatible workflows**

#### PHASE 1: CLI Foundation (Jules-Ready)
**Jules Implementation**: Create Click CLI structure with Jules' native file management

```python
# File: src/cli/pr_resolve.py (Create in Jules)
@click.group()
def pr_resolve():
    """PR Resolution Commands"""
    pass

@pr_resolve.command()
@click.option('--session-id', required=True)
def init(session_id):
    """Initialize resolution environment"""
    click.echo(f"✅ Session initialized: {session_id}")

# Integration: Add to emailintelligence_cli.py
# from src.cli.pr_resolve import pr_resolve
# cli.add_command(pr_resolve, name='pr-resolve')
```

**Jules Test Command**:
```bash
# Use Jules terminal integration
emailintelligence-cli pr-resolve --help
# Expected: Show help message with pr-resolve commands
```

**Jules Verification**: Check command output in Jules terminal

#### PHASE 2: Git Infrastructure (Jules-Ready)
**Jules Implementation**: Git worktree management with Jules' Git integration

```python
# File: src/resolution/git_worktree.py (Create in Jules)
class GitWorktreeManager:
    def __init__(self, repo_path: str):
        self.repo = Repo(repo_path)
    
    def validate_git_version(self):
        # Validate Git 2.25+ compatibility
        git_version = self.repo.git.version()
        if "git version 2.25" not in git_version.lower():
            raise CLIError("Git 2.25+ required")
        return True
    
    def create_worktree(self, session_id: str):
        worktree_path = f"/tmp/resolution-{session_id}-{int(time.time())}"
        self.repo.git.worktree('add', worktree_path, '--detach')
        return worktree_path
```

**Jules Test Command**:
```bash
# Use Jules terminal
emailintelligence-cli pr-resolve init --session-id test-123
# Expected: Worktree creation success message
```

#### PHASE 3: Conflict Detection (Jules-Ready)
**Jules Implementation**: Real Git conflict analysis with Jules' file watching

```python
# File: src/resolution/conflicts.py (Create in Jules)
class ConflictDetector:
    def analyze_repository(self, branch: str, base: str):
        # Real Git diff analysis
        conflicts = {
            'text': [],
            'binary': [],
            'structural': []
        }
        
        try:
            # Get diff between branches
            diff_output = self.repo.git.diff(f"{base}...{branch}")
            
            # Parse conflicts
            for line in diff_output.split('\n'):
                if line.startswith('diff --git'):
                    conflicts['text'].append(self._extract_file_path(line))
            
            return conflicts
            
        except GitCommandError as e:
            raise CLIError(f"Conflict analysis failed: {e}")
    
    def _extract_file_path(self, diff_line):
        # Extract file path from git diff output
        parts = diff_line.split()
        return parts[2].replace('a/', '').replace('b/', '')
```

**Jules Test Command**:
```bash
# Create test Git repository in Jules
mkdir test-repo && cd test-repo
git init && echo "base" > file.txt && git add . && git commit -m "base"
git checkout -b feature && echo "feature" > file.txt && git add . && git commit -m "feature"

# Test conflict detection
cd ../
emailintelligence-cli pr-resolve analyze --branch feature --base main
# Expected: List of conflicts with file paths and types
```

---

## Jules-Specific Implementation Patterns

### 1. File Structure in Jules

**Jules Project Structure**:
```
EmailIntelligence/
├── src/
│   ├── cli/
│   │   └── pr_resolve.py          # Create with Jules
│   ├── resolution/
│   │   ├── git_worktree.py        # Create with Jules  
│   │   ├── conflicts.py           # Create with Jules
│   │   ├── constitutional/        # Create with Jules
│   │   ├── specification/         # Create with Jules
│   │   └── strategies/            # Create with Jules
│   └── integration/
│       └── task_master.py         # Create with Jules
├── tests/
│   ├── unit/                      # Create with Jules
│   ├── integration/               # Create with Jules
│   └── performance/               # Create with Jules
└── specs/
    └── 001-pr-resolution-improvements/
        ├── spec.md                # Already exists
        ├── tasks-reordered.md     # Use for task order
        ├── plan.md                # Use for architecture
        └── cli-improvements.md    # Use for CLI specs
```

### 2. Jules Implementation Workflow

#### Step 1: Setup Project Context
1. Open Jules workspace
2. Navigate to `EmailIntelligence/src/`
3. Use Jules' file creation to implement tasks from `tasks-reordered.md`

#### Step 2: Follow Phase Order
**Start with Phase 1**: CLI Foundation (T100-T104)
- Create `src/cli/pr_resolve.py`
- Add CLI structure to `emailintelligence_cli.py`
- Test with Jules terminal: `emailintelligence-cli pr-resolve --help`

**Continue to Phase 2**: Git Infrastructure (T110-T114)
- Create `src/resolution/git_worktree.py`
- Implement worktree management
- Test with Jules terminal: `emailintelligence-cli pr-resolve init --session-id test-123`

**Proceed through all 9 phases...**

#### Step 3: Jules Testing Integration
**Use Jules Terminal for Testing**:
```bash
# Test CLI structure
emailintelligence-cli pr-resolve --help

# Test Git infrastructure
emailintelligence-cli pr-resolve init --session-id test-123

# Test conflict detection
emailintelligence-cli pr-resolve analyze --branch feature --base main

# Test specification creation
emailintelligence-cli pr-resolve analyze --branch feature --base main --output spec.md

# Continue with remaining test commands...
```

### 3. Jules Code Generation Patterns

#### Pattern 1: Start with CLI Foundation
```python
# Jules prompt: "Create Click CLI structure for pr-resolve namespace"
# Implementation: src/cli/pr_resolve.py
```

#### Pattern 2: Add Git Infrastructure
```python  
# Jules prompt: "Implement Git worktree manager with validation"
# Implementation: src/resolution/git_worktree.py
```

#### Pattern 3: Build Conflict Detection
```python
# Jules prompt: "Create real Git conflict analysis with diff parsing"
# Implementation: src/resolution/conflicts.py
```

### 4. Jules Error Handling & Validation

**Use Jules' native error handling patterns**:

```python
# File: src/cli/pr_resolve.py
import click
from src.resolution.git_worktree import GitWorktreeManager

@click.group()
def pr_resolve():
    """PR Resolution Commands"""
    pass

@pr_resolve.command()
@click.option('--session-id', required=True, help='Unique session identifier')
@click.option('--verbose', is_flag=True, help='Verbose output')
def init(session_id, verbose):
    """Initialize resolution environment with worktree isolation"""
    try:
        worktree_manager = GitWorktreeManager('.')
        
        # Validate Git compatibility
        worktree_manager.validate_git_version()
        
        # Create worktree
        worktree_path = worktree_manager.create_worktree(session_id)
        
        if verbose:
            click.echo(f"Worktree created at: {worktree_path}")
            
        click.echo(f"✅ Session initialized: {session_id}")
        click.echo(f"Worktree: {worktree_path}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.ClickException(str(e))
```

---

## Expected Outputs with Jules

### Phase 1 CLI Output
```bash
$ emailintelligence-cli pr-resolve --help
Usage: emailintelligence-cli pr-resolve [OPTIONS] COMMAND [ARGS]...
  PR Resolution Commands
Options:
  --help  Show this message
Commands:
  init    Initialize resolution environment
```

### Phase 2 Worktree Output  
```bash
$ emailintelligence-cli pr-resolve init --session-id test-123 --verbose
✅ Git version: 2.25.0+ (compatible)
✅ Worktree created: /tmp/resolution-test-123-1634567890
✅ Session initialized: test-123
Worktree: /tmp/resolution-test-123-1634567890
```

### Phase 3 Conflict Analysis Output
```bash
$ emailintelligence-cli pr-resolve analyze --branch feature --base main
📊 Conflict Analysis:
  Text conflicts: 3 files
    - src/app.py (lines 45-67)
    - tests/test_app.py (lines 12-18)
  Binary conflicts: 1 file
    - assets/logo.png (renamed/modified)
  Structural conflicts: 2 paths
    - docs/old/ → docs/new/
```

### Phase 4 Specification Output
```markdown
# conflict-spec-20251113-123456.md

---
spec_id: "spec-123456"
created_at: "2025-11-13T12:34:56Z"
branch: "feature/test"
base: "main"
conflict_count: 3
complexity_score: 7
---

## Conflict Analysis

### Text Conflicts (3 files)
- src/app.py: Function signature mismatch
- tests/test_app.py: Test assertion changes
- config/settings.py: Configuration key conflicts

### Complexity Assessment
- Overall complexity: 7/10
- Risk factors: Core functionality changes, test coverage impact
```

---

## Jules Integration Best Practices

### 1. Use Jules' Native Features
- **File Explorer**: Navigate to `src/` and create implementation files
- **Terminal Integration**: Test CLI commands directly in Jules
- **Git Integration**: Use Jules' built-in Git features for worktree testing
- **Code Generation**: Use Jules' AI to generate implementation patterns

### 2. Follow Agent-Friendly Task Order
**Reference**: `tasks-reordered.md` (lines 16-184)
- Each phase builds on working foundations
- Every implementation produces testable outputs
- Clear success criteria for each phase

### 3. Test-Driven Development with Jules
**Use Jules Terminal for Validation**:
```bash
# After each implementation
emailintelligence-cli pr-resolve --help
emailintelligence-cli pr-resolve init --session-id test-{timestamp}
emailintelligence-cli pr-resolve analyze --branch test --base main

# Verify outputs match expected results
```

### 4. Progressive Implementation
1. **Phase 1**: CLI structure → Test `pr-resolve --help`
2. **Phase 2**: Git infrastructure → Test worktree creation
3. **Phase 3**: Conflict detection → Test conflict analysis
4. **Continue through all 9 phases...**

### 5. Documentation Integration
**Use Jules to enhance documentation**:
- Update `README.md` with new commands
- Add examples to `quickstart.md`
- Create Jules-specific implementation guides

---

## Jules-Specific Testing Strategy

### 1. Terminal Testing
```bash
# Test CLI structure
emailintelligence-cli pr-resolve --help

# Test worktree operations  
emailintelligence-cli pr-resolve init --session-id test-jules-001

# Test conflict detection
cd test-repo
emailintelligence-cli pr-resolve analyze --branch feature --base main

# Test specification creation
emailintelligence-cli pr-resolve analyze --branch feature --base main --output spec.md
```

### 2. File Validation
**Check Jules-created files**:
- `src/cli/pr_resolve.py` - CLI command structure
- `src/resolution/git_worktree.py` - Worktree management
- `src/resolution/conflicts.py` - Conflict analysis
- Generated specification files

### 3. Integration Testing
**Test complete workflow**:
```bash
# Full end-to-end test
emailintelligence-cli pr-resolve init --session-id full-test
emailintelligence-cli pr-resolve analyze --branch feature --base main --output spec.md
emailintelligence-cli pr-resolve validate --spec spec.md
emailintelligence-cli pr-resolve strategy --spec spec.md --type conservative
```

---

## Jules Adaptation Notes

### Adapting Task Master Patterns to Jules

**Instead of Task Master CLI**:
```bash
task-master init
task-master next
task-master show 1
task-master set-status --id=1 --status=done
```

**Use Jules Workflow**:
1. Navigate to `specs/001-pr-resolution-improvements/tasks-reordered.md`
2. Use Jules to implement Phase 1 tasks (T100-T104)
3. Test with Jules terminal
4. Continue to Phase 2 tasks (T110-T114)
5. Test with Jules terminal
6. Continue through all phases

### Key Differences with Jules

| Task Master | Jules Adaptation |
|-------------|------------------|
| `task-master next` | Navigate to next task in `tasks-reordered.md` |
| `task-master show <id>` | Open relevant specification file |
| `task-master set-status --id=<id> --status=done` | Mark phase complete in Jules |
| `task-master list` | Review phases in `tasks-reordered.md` |

---

## Success Criteria with Jules

### Each Phase Must Produce:
1. **Working CLI command** that tests successfully in Jules terminal
2. **Real file creation** in Jules project structure
3. **Verifiable outputs** (console output, generated files)
4. **Error handling** with clear error messages
5. **Integration test** with previous phase functionality

### Jules-Specific Deliverables:
- **CLI commands** working in Jules terminal
- **Real implementation files** created in Jules
- **Test outputs** matching expected specifications
- **Integration validation** across all phases

This guide ensures Jules users can effectively implement the PR Resolution Enhancement project using Jules' native agentic capabilities while following proven Task Master patterns.