# Plan: TOML-Based Command System with Evidence Archive

**Objective:** Create a new TOML-based command system that addresses state tracking limitations and archive all evidence for future reference

**Approach:** Hybrid system where TOML commands work alongside existing JSON state management

---

## Phase 1: Create Temporary Commands Directory

### 1.1 Create Directory Structure
```
commands_temp/
├── archive/                    # Evidence archive (read-only)
│   ├── state_tracking_failures/
│   ├── command_improvements/
│   ├── refactoring_plans/
│   └── test_results/
├── active/                     # Active development area
│   ├── commands/               # TOML command definitions
│   ├── parsers/                # Command parser implementation
│   └── tests/                  # Test files
└── README.md                   # Directory structure guide
```

### 1.2 Move Evidence Files

**State Tracking Failures:**
- Copy `refactor/state.json` → `commands_temp/archive/state_tracking_failures/refactor_state.json`
- Copy `implement/state.json` → `commands_temp/archive/state_tracking_failures/implement_state.json`
- Create `state_analysis.md` documenting the inconsistencies found

**Command Improvement Proposals:**
- Move `refactor/COMMAND_IMPROVEMENTS.md` → `commands_temp/archive/command_improvements/`
- Move `task_scripts/refactoring_state.py` → `commands_temp/archive/command_improvements/refactoring_state.py`

**Refactoring Plans:**
- Move `refactor/IMPLEMENTATION_GUIDE.md` → `commands_temp/archive/refactoring_plans/`
- Move `refactor/CHANGE_SUMMARY.md` → `commands_temp/archive/refactoring_plans/`
- Move `refactor/QUICK_REFERENCE.md` → `commands_temp/archive/refactoring_plans/`
- Move `refactor/plan.md` → `commands_temp/archive/refactoring_plans/`
- Move `implement/plan.md` → `commands_temp/archive/refactoring_plans/`

**Test Results:**
- Create `test_summary.md` documenting the execution results
- Archive any test output files

---

## Phase 2: Design TOML Command Schema

### 2.1 Command Definition Schema

Based on mise-en-place and cargo-make best practices:

```toml
# Example TOML schema (archived - never implemented)

[metadata]
name = "refactor"
version = "1.0.0"
description = "Refactoring command system with automatic state tracking"

[command_config]
state_file = "refactor/state.json"
backup_enabled = true
validation_enabled = true
auto_cascade = true

[commands.init]
description = "Initialize a new refactoring project"
run = "python task_scripts/refactoring_state.py init {{args.id}} {{args.title}}"
args = [
    { name = "id", required = true, description = "Refactoring ID" },
    { name = "title", required = true, description = "Refactoring title" }
]
env = { PYTHONPATH = "{{cwd}}/task_scripts" }

[commands.status]
description = "Show refactoring status with validation"
run = "python task_scripts/refactoring_state.py status {{args.id}}"
args = [
    { name = "id", required = true, description = "Refactoring ID" },
    { name = "verbose", type = "bool", default = false, description = "Show detailed output" }
]

[commands.update_task]
description = "Update task status with automatic cascading"
run = "python -c \"from task_scripts.refactoring_state import RefactoringStateManager; m = RefactoringStateManager('refactor/{{args.id}}/state.json'); m.update_task_status('{{args.phase}}', '{{args.task}}', '{{args.status}}', create_backup=True)\""
args = [
    { name = "id", required = true, description = "Refactoring ID" },
    { name = "phase", required = true, description = "Phase ID" },
    { name = "task", required = true, description = "Task ID" },
    { name = "status", required = true, options = ["pending", "in_progress", "completed", "failed", "blocked"] }
]

[commands.validate]
description = "Validate state consistency"
run = "python -c \"from task_scripts.refactoring_state import RefactoringStateManager; m = RefactoringStateManager('refactor/{{args.id}}/state.json'); errors = m.validate_state(); print('✓ Valid' if not errors else f'✗ Errors: {errors}')\""
args = [
    { name = "id", required = true, description = "Refactoring ID" }
]

[commands.sync]
description = "Synchronize state files between refactor/ and implement/"
run = "python task_scripts/refactoring_state.py sync {{args.id}}"
args = [
    { name = "id", required = true, description = "Refactoring ID" }
]

# Example workflow command
[commands.implement]
description = "Execute implementation workflow with automatic validation"
depends = ["validate"]
run = """
python -c "
from task_scripts.refactoring_state import RefactoringStateManager
m = RefactoringStateManager('refactor/{{args.id}}/state.json')
# Implementation logic here
m.update_task_status('{{args.phase}}', '{{args.task}}', 'completed')
errors = m.validate_state()
if errors:
    print(f'Validation failed: {errors}')
    exit(1)
"
"""
args = [
    { name = "id", required = true },
    { name = "phase", required = true },
    { name = "task", required = true }
]
```

### 2.2 State File Schema (JSON - unchanged, works alongside TOML)

Existing JSON schema remains the source of truth:
- `refactor/state.json` - Primary state file
- `implement/state.json` - Secondary state file (synced via TOML commands)

---

## Phase 3: Implement Command Parser

### 3.1 Create Parser Module

**File:** `commands_temp/active/parsers/toml_command_parser.py`

```python
"""
TOML Command Parser

Parses TOML command definitions and executes them with automatic
state management, validation, and cascading.
"""

import toml
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


class TomlCommandParser:
    """Parse and execute TOML-based commands"""
    
    def __init__(self, command_file: str):
        self.command_file = Path(command_file)
        self.commands = self._load_commands()
    
    def _load_commands(self) -> Dict:
        """Load TOML command definitions"""
        with open(self.command_file, 'r') as f:
            return toml.load(f)
    
    def execute(self, command_name: str, args: Dict = None) -> Dict:
        """
        Execute a command with automatic state management.
        
        Args:
            command_name: Name of command to execute
            args: Command arguments
            
        Returns:
            Execution result with status and output
        """
        command = self.commands.get("commands", {}).get(command_name)
        if not command:
            return {"status": "error", "message": f"Command not found: {command_name}"}
        
        # Check dependencies
        deps = command.get("depends", [])
        for dep in deps:
            if isinstance(dep, str):
                result = self.execute(dep, args)
                if result.get("status") != "success":
                    return result
        
        # Execute command
        run_cmd = command.get("run")
        if not run_cmd:
            return {"status": "error", "message": "No run command specified"}
        
        # Substitute arguments
        cmd = self._substitute_args(run_cmd, args or {})
        
        # Set environment variables
        env = command.get("env", {})
        
        # Execute
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                env={**os.environ, **env}
            )
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "output": result.stdout,
                "error": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _substitute_args(self, template: str, args: Dict) -> str:
        """Substitute arguments into command template"""
        result = template
        for key, value in args.items():
            result = result.replace(f"{{{{args.{key}}}}}", str(value))
        return result
    
    def list_commands(self) -> List[Dict]:
        """List all available commands"""
        commands = []
        for name, cmd in self.commands.get("commands", {}).items():
            commands.append({
                "name": name,
                "description": cmd.get("description", ""),
                "args": cmd.get("args", [])
            })
        return commands
```

### 3.2 Create CLI Wrapper

**File:** `commands_temp/active/parsers/cli.py`

```python
#!/usr/bin/env python3
"""
CLI wrapper for TOML command system
"""

import sys
from pathlib import Path
from toml_command_parser import TomlCommandParser


def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <command> [args]")
        sys.exit(1)
    
    # Note: command file reference removed - system never implemented
    # command_file = Path(__file__).parent.parent / "commands" / "refactor.toml"
    # parser = TomlCommandParser(command_file)
    
    command_name = sys.argv[1]
    args = {}
    
    # Parse key=value arguments
    for arg in sys.argv[2:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            args[key] = value
    
    result = parser.execute(command_name, args)
    
    if result.get("status") == "success":
        print(result.get("output", ""))
        sys.exit(0)
    else:
        print(f"Error: {result.get('message') or result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

---

## Phase 4: Create Diagnostic Documentation

### 4.1 Evidence Summary

**File:** `commands_temp/README.md`

Document:
- What went wrong with the previous system
- Root causes of state tracking failures
- Lessons learned
- How the new TOML system addresses these issues

### 4.2 State Tracking Analysis

**File:** `commands_temp/archive/state_tracking_failures/analysis.md`

Document:
- Specific inconsistencies found
- Missing validation rules
- Cascading failures
- Progress calculation errors

### 4.3 Migration Guide

**File:** `commands_temp/MIGRATION.md`

Document:
- How to use TOML commands alongside JSON
- When to use TOML vs direct JSON manipulation
- Best practices for state management
- Troubleshooting common issues

---

## Phase 5: Testing and Validation

### 5.1 Create Test Cases

**File:** `commands_temp/active/tests/test_toml_commands.py`

Test:
- Command parsing
- Argument substitution
- Dependency execution
- State cascading
- Validation
- Error handling

### 5.2 Integration Tests

Test that TOML commands work with:
- Existing JSON state files
- RefactoringStateManager class
- SecurityValidator and BackupManager

---

## Key Design Decisions

1. **Hybrid Approach**: TOML for command definitions, JSON for runtime state
2. **Backward Compatible**: Existing JSON state files remain unchanged
3. **Automatic Cascading**: Built into command execution via RefactoringStateManager
4. **Validation**: Automatic after each state update
5. **Evidence Archive**: All failures and lessons preserved for future reference

## Files to Create/Modify

**Create:**
- `commands_temp/` directory structure (never implemented)
- `commands_temp/commands/refactor.toml` (never implemented)
- `commands_temp/active/parsers/toml_command_parser.py` (never implemented)
- `commands_temp/active/parsers/cli.py` (never implemented)
- `commands_temp/active/tests/test_toml_commands.py` (never implemented)
- `commands_temp/README.md` (never implemented)
- `commands_temp/MIGRATION.md` (never implemented)
- Evidence documentation files

**Move (archive):**
- All files listed in Phase 1.2

**Modify (none)**: Existing JSON state files remain unchanged

## Success Criteria

- [ ] All evidence archived in organized structure
- [ ] TOML command parser working with existing JSON state
- [ ] Automatic state cascading functional
- [ ] Validation detects all previously missed errors
- [ ] Commands work alongside existing JSON system
- [ ] Documentation complete for future reference