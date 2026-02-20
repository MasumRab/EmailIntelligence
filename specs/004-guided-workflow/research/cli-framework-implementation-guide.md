# CLI Framework Implementation Guide & Case Study

**For Projects Like gemini-cli-prompt-library**  
**Date**: 2026-01-18

---

## Executive Summary

This guide provides a comprehensive analysis of Python CLI frameworks and interactive libraries for building agentic-compatible command-line tools. Based on investigation of the `gemini-cli-prompt-library` project and cross-agent session analysis, we recommend **typer + rich + InquirerPy** with proper agentic wrappers.

---

## Part 1: CLI Command Framework Comparison

### 1.1 argparse (Standard Library)

**Current Usage**: `gemini-cli-prompt-library/dspy_helm/cli.py` uses argparse

```python
# From dspy_helm/cli.py
parser = argparse.ArgumentParser(
    description="DSPy-HELM: Evaluation and Optimization Framework",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
```

| Aspect | Assessment |
|--------|------------|
| **Advantages** | Zero dependencies, always available, stable API, well-documented |
| **Disadvantages** | Verbose, no type hints, manual help formatting, no auto-completion |
| **Agentic Compatibility** | ✅ Excellent - pure text I/O, no TTY requirements |
| **Type Safety** | ❌ None - all runtime validation |
| **Learning Curve** | Medium - many concepts to learn |
| **Best For** | Simple scripts, stdlib-only requirements, legacy codebases |

**Code Example**:
```python
import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()
    
    result = {"scenario": args.scenario, "status": "ok"}
    
    if args.json:
        print(json.dumps(result))
    else:
        print(f"Scenario: {args.scenario}")
```

---

### 1.2 typer

**Recommendation**: ✅ **Primary choice for gemini-cli-prompt-library**

| Aspect | Assessment |
|--------|------------|
| **Advantages** | Type hints → CLI args, auto-completion, rich integration, Click underneath |
| **Disadvantages** | Extra dependency, slightly slower startup than argparse |
| **Agentic Compatibility** | ✅ Excellent - `--json` flag pattern, no TTY blocking |
| **Type Safety** | ✅ Full - Pydantic-style validation from type hints |
| **Learning Curve** | Low - if you know Python type hints, you know Typer |
| **Best For** | Modern CLIs, developer tools, agentic workflows |

**Why Typer Wins**:
1. **FastAPI of CLIs** - Same design philosophy, same author (tiangolo)
2. **Click underneath** - Fall back to Click when needed
3. **Auto shell completion** - Bash, Zsh, Fish, PowerShell
4. **Rich integration** - Beautiful output with zero config

**Implementation Example**:
```python
import typer
from typing import Optional
from enum import Enum

app = typer.Typer(help="DSPy-HELM Evaluation Framework")

class OutputFormat(str, Enum):
    human = "human"
    json = "json"

@app.command()
def evaluate(
    scenario: str = typer.Argument(..., help="Scenario to evaluate"),
    optimizer: Optional[str] = typer.Option(None, "--optimizer", "-o"),
    format: OutputFormat = typer.Option(OutputFormat.human, "--format", "-f"),
    evaluate_only: bool = typer.Option(False, "--evaluate-only"),
):
    """Run evaluation for a scenario."""
    result = run_evaluation(scenario, optimizer, evaluate_only)
    
    if format == OutputFormat.json:
        typer.echo(json.dumps(result))
    else:
        typer.echo(f"Score: {result['score']}")

if __name__ == "__main__":
    app()
```

---

### 1.3 cyclopts

**The Typer Alternative**

| Aspect | Assessment |
|--------|------------|
| **Advantages** | Fixes 13 Typer issues, faster, better defaults, native JSON |
| **Disadvantages** | Smaller community, less documentation, newer |
| **Agentic Compatibility** | ✅ Excellent - built-in JSON mode |
| **Type Safety** | ✅ Full |
| **Learning Curve** | Low - nearly identical to Typer |
| **Best For** | Teams frustrated with Typer edge cases |

**Key Differences from Typer**:
```python
# Cyclopts handles these better:
# 1. Boolean flags: --flag/--no-flag works correctly
# 2. List arguments: better parsing of multiple values  
# 3. Negative numbers: --count=-5 works
# 4. Empty strings: --name="" preserved
```

**When to Choose Cyclopts**:
- Need native `--json` output without custom code
- Boolean flag handling is critical
- Want faster CLI startup time

---

### 1.4 python-fire

**Zero-Boilerplate CLI**

| Aspect | Assessment |
|--------|------------|
| **Advantages** | Any object → CLI, zero decorators, introspection-based |
| **Disadvantages** | Ignores type hints, magic behavior, debugging harder |
| **Agentic Compatibility** | ✅ Excellent - native headless, JSON default |
| **Type Safety** | ❌ None - parses as Python expressions |
| **Learning Curve** | Very Low - just call `fire.Fire(your_function)` |
| **Best For** | Rapid prototyping, internal tools, debugging CLIs |

**Example**:
```python
import fire

class DSPyHELM:
    def evaluate(self, scenario: str, optimizer: str = None):
        """Run evaluation."""
        return {"scenario": scenario, "optimizer": optimizer}
    
    def list_scenarios(self):
        """List available scenarios."""
        return ["security_review", "unit_test", "documentation"]

if __name__ == "__main__":
    fire.Fire(DSPyHELM)
```

**Usage**:
```bash
python cli.py evaluate security_review --optimizer=MIPROv2
python cli.py list_scenarios
```

---

### 1.5 click

**The Foundation**

| Aspect | Assessment |
|--------|------------|
| **Advantages** | Battle-tested, composable, extensive ecosystem |
| **Disadvantages** | Decorator-heavy, code duplication, less Pythonic |
| **Agentic Compatibility** | ✅ Good - text I/O based |
| **Type Safety** | ⚠️ Partial - decorators define types |
| **Learning Curve** | Medium |
| **Best For** | Complex CLIs, plugin architectures, when Typer insufficient |

---

## Part 2: Interactive Prompt Libraries

### 2.1 InquirerPy

**Selected for gemini-cli-prompt-library** (TC-001)

| Aspect | Assessment |
|--------|------------|
| **Advantages** | Full Inquirer.js port, fuzzy search, async, rich prompts |
| **Disadvantages** | ❌ **Blocks on no TTY**, requires wrapper |
| **Agentic Compatibility** | ⚠️ **Needs wrapper** - hangs in headless mode |
| **Prompt Types** | Select, checkbox, input, confirm, fuzzy, filepath, password |
| **Best For** | Interactive human workflows with fallback |

**The Problem**:
```python
# This HANGS when run by an AI agent (no TTY):
from InquirerPy import inquirer
result = inquirer.select(message="Choose:", choices=["A", "B"]).execute()
```

**The Solution - Agentic Wrapper**:
```python
import sys
import os
from typing import List, TypeVar, Optional

T = TypeVar("T")

def is_agentic() -> bool:
    """Detect if running under an AI coding agent."""
    return any([
        not sys.stdin.isatty(),
        not sys.stdout.isatty(),
        os.environ.get("AGENT_MODE") == "1",
        os.environ.get("CI") == "true",
        os.environ.get("NONINTERACTIVE") == "1",
        os.environ.get("TERM") == "dumb",
    ])

def smart_select(
    message: str,
    choices: List[T],
    default: Optional[T] = None,
) -> T:
    """Select with agentic fallback."""
    if is_agentic():
        # In agentic mode: use default or first choice
        if default is not None:
            return default
        return choices[0]
    
    # Human mode: use InquirerPy
    from InquirerPy import inquirer
    return inquirer.select(
        message=message,
        choices=choices,
        default=default,
    ).execute()

def smart_confirm(message: str, default: bool = True) -> bool:
    """Confirm with agentic fallback."""
    if is_agentic():
        return default
    
    from InquirerPy import inquirer
    return inquirer.confirm(message=message, default=default).execute()

def smart_text(message: str, default: str = "") -> str:
    """Text input with agentic fallback."""
    if is_agentic():
        return default
    
    from InquirerPy import inquirer
    return inquirer.text(message=message, default=default).execute()
```

---

### 2.2 questionary

**Simpler Alternative**

| Aspect | Assessment |
|--------|------------|
| **Advantages** | Simpler API, good defaults, prompt-toolkit based |
| **Disadvantages** | ❌ Same TTY blocking issue, no async, fewer features |
| **Agentic Compatibility** | ⚠️ **Needs wrapper** |
| **Best For** | Simple interactive prompts |

---

### 2.3 prompt-toolkit

**Low-Level Power**

| Aspect | Assessment |
|--------|------------|
| **Advantages** | Full readline, autocomplete, syntax highlighting, multiline |
| **Disadvantages** | Complex API, overkill for simple prompts, TTY issues |
| **Agentic Compatibility** | ⚠️ Requires careful handling |
| **Best For** | REPLs, complex input scenarios, custom editors |

---

## Part 3: Output & Display Libraries

### 3.1 rich

**Recommended** ✅

| Aspect | Assessment |
|--------|------------|
| **Advantages** | Tables, progress bars, syntax highlighting, markdown, panels |
| **Disadvantages** | Terminal feature detection can fail in edge cases |
| **Agentic Compatibility** | ✅ **Excellent** - auto-detects non-TTY |
| **Performance** | Fast rendering, efficient updates |
| **Best For** | Beautiful CLI output, logging, debugging |

**Agentic-Safe Usage**:
```python
from rich.console import Console
from rich.table import Table
import sys

def get_console() -> Console:
    """Get console configured for current environment."""
    # Rich auto-detects, but we can be explicit
    force_terminal = sys.stdout.isatty()
    return Console(force_terminal=force_terminal)

console = get_console()

# Tables work in both modes
table = Table(title="Results")
table.add_column("Metric")
table.add_column("Value")
table.add_row("Score", "0.95")
console.print(table)

# For JSON output alongside rich
def output_result(result: dict, json_mode: bool = False):
    if json_mode:
        import json
        print(json.dumps(result))
    else:
        console.print(result)
```

---

### 3.2 Textual

**Full TUI Framework**

| Aspect | Assessment |
|--------|------------|
| **Advantages** | CSS styling, widgets, reactive, async, 16.7M colors |
| **Disadvantages** | Heavier weight, learning curve, overkill for simple CLIs |
| **Agentic Compatibility** | ✅ **Native headless mode** for testing |
| **Best For** | Full terminal applications, dashboards, file browsers |

**Headless Testing**:
```python
from textual.pilot import Pilot

async def test_my_app():
    """Run TUI in headless mode for testing."""
    async with MyApp().run_test() as pilot:
        await pilot.press("enter")
        await pilot.click("#submit-button")
        assert pilot.app.query_one("#result").text == "Success"
```

---

## Part 4: Recommended Stack for gemini-cli-prompt-library

### Stack Decision: Option D (from session 2026-01-13)

```
typer + rich + InquirerPy
```

### Implementation Architecture

```
gemini-cli-prompt-library/
├── src/
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py              # Typer app entry point
│   │   ├── commands/
│   │   │   ├── evaluate.py      # Evaluation commands
│   │   │   ├── optimize.py      # Optimization commands
│   │   │   └── scenarios.py     # Scenario management
│   │   └── utils/
│   │       ├── agentic.py       # is_agentic(), smart_* wrappers
│   │       ├── output.py        # Console, JSON output helpers
│   │       └── prompts.py       # InquirerPy wrappers
│   └── ...
└── dspy_helm/
    └── cli.py                   # Migrate from argparse to typer
```

### Migration Example: dspy_helm/cli.py

**Before (argparse)**:
```python
parser = argparse.ArgumentParser(description="DSPy-HELM")
parser.add_argument("--scenario", type=str)
parser.add_argument("--optimizer", choices=["MIPROv2", "BootstrapFewShot"])
args = parser.parse_args()
```

**After (typer)**:
```python
import typer
from enum import Enum
from typing import Optional

app = typer.Typer(help="DSPy-HELM: Evaluation and Optimization Framework")

class Optimizer(str, Enum):
    miprov2 = "MIPROv2"
    bootstrap = "BootstrapFewShot"
    bootstrap_random = "BootstrapFewShotWithRandomSearch"

@app.command()
def run(
    scenario: str = typer.Argument(..., help="Scenario to run"),
    optimizer: Optional[Optimizer] = typer.Option(None, "--optimizer", "-o"),
    json_output: bool = typer.Option(False, "--json", help="JSON output"),
):
    """Run a DSPy-HELM evaluation."""
    ...
```

---

## Part 5: Agentic Compatibility Patterns

### 5.1 Complete Agentic Detection Module

```python
# src/cli/utils/agentic.py
"""Agentic environment detection and compatibility utilities."""

import os
import sys
from typing import TypeVar, List, Optional, Callable, Any
from functools import wraps

T = TypeVar("T")

# Known agent environment variables
AGENT_INDICATORS = {
    "AGENT_MODE": "1",
    "CI": "true", 
    "GITHUB_ACTIONS": "true",
    "GITLAB_CI": "true",
    "JENKINS_URL": None,  # Any value
    "NONINTERACTIVE": "1",
    "NO_COLOR": None,     # Any value
}

def is_agentic() -> bool:
    """
    Detect if running under an AI coding agent or CI environment.
    
    Returns True if:
    - stdin/stdout is not a TTY
    - Known agent environment variables are set
    - Running in CI environment
    """
    # TTY checks (most reliable)
    if not sys.stdin.isatty():
        return True
    if not sys.stdout.isatty():
        return True
    
    # Terminal type check
    if os.environ.get("TERM") in ("dumb", ""):
        return True
    
    # Agent/CI environment variables
    for var, expected in AGENT_INDICATORS.items():
        value = os.environ.get(var)
        if value is not None:
            if expected is None or value == expected:
                return True
    
    return False

def is_interactive() -> bool:
    """Inverse of is_agentic()."""
    return not is_agentic()

def require_interactive(func: Callable) -> Callable:
    """Decorator that skips function in agentic mode."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_agentic():
            return None
        return func(*args, **kwargs)
    return wrapper
```

### 5.2 Smart Prompt Wrappers

```python
# src/cli/utils/prompts.py
"""Interactive prompts with agentic fallbacks."""

from typing import List, TypeVar, Optional, Dict, Any
from .agentic import is_agentic

T = TypeVar("T")

def smart_select(
    message: str,
    choices: List[T],
    default: Optional[T] = None,
    *,
    agentic_choice: Optional[T] = None,
) -> T:
    """
    Select from choices with agentic fallback.
    
    Args:
        message: Prompt message for human mode
        choices: List of choices
        default: Default for human mode
        agentic_choice: Override choice for agentic mode (defaults to first)
    """
    if is_agentic():
        if agentic_choice is not None:
            return agentic_choice
        if default is not None:
            return default
        return choices[0]
    
    from InquirerPy import inquirer
    return inquirer.select(
        message=message,
        choices=choices,
        default=default,
    ).execute()

def smart_confirm(
    message: str,
    default: bool = True,
    *,
    agentic_value: Optional[bool] = None,
) -> bool:
    """Confirm with agentic fallback."""
    if is_agentic():
        return agentic_value if agentic_value is not None else default
    
    from InquirerPy import inquirer
    return inquirer.confirm(message=message, default=default).execute()

def smart_fuzzy_select(
    message: str,
    choices: List[str],
    default: Optional[str] = None,
) -> str:
    """Fuzzy select with agentic fallback."""
    if is_agentic():
        return default or choices[0]
    
    from InquirerPy import inquirer
    return inquirer.fuzzy(
        message=message,
        choices=choices,
        default=default,
    ).execute()

def smart_checkbox(
    message: str,
    choices: List[str],
    defaults: Optional[List[str]] = None,
) -> List[str]:
    """Checkbox selection with agentic fallback."""
    if is_agentic():
        return defaults or choices[:1]
    
    from InquirerPy import inquirer
    return inquirer.checkbox(
        message=message,
        choices=choices,
        default=defaults,
    ).execute()
```

### 5.3 Output Format Handler

```python
# src/cli/utils/output.py
"""Output formatting for human and machine consumption."""

import json
import sys
from typing import Any, Dict, Optional
from enum import Enum
from rich.console import Console
from rich.table import Table

class OutputFormat(str, Enum):
    human = "human"
    json = "json"
    jsonl = "jsonl"

_console: Optional[Console] = None

def get_console() -> Console:
    """Get or create console instance."""
    global _console
    if _console is None:
        _console = Console(
            force_terminal=sys.stdout.isatty(),
            force_interactive=sys.stdin.isatty(),
        )
    return _console

def output(
    data: Any,
    format: OutputFormat = OutputFormat.human,
    *,
    title: Optional[str] = None,
) -> None:
    """
    Output data in the specified format.
    
    Args:
        data: Data to output (dict, list, or any)
        format: Output format
        title: Optional title for human format
    """
    if format == OutputFormat.json:
        print(json.dumps(data, indent=2, default=str))
    elif format == OutputFormat.jsonl:
        if isinstance(data, list):
            for item in data:
                print(json.dumps(item, default=str))
        else:
            print(json.dumps(data, default=str))
    else:
        console = get_console()
        if isinstance(data, dict):
            _output_dict(console, data, title)
        elif isinstance(data, list) and data and isinstance(data[0], dict):
            _output_table(console, data, title)
        else:
            console.print(data)

def _output_dict(console: Console, data: Dict, title: Optional[str]) -> None:
    """Output dictionary as key-value pairs."""
    from rich.panel import Panel
    from rich.pretty import Pretty
    
    content = Pretty(data)
    if title:
        console.print(Panel(content, title=title))
    else:
        console.print(content)

def _output_table(console: Console, data: list, title: Optional[str]) -> None:
    """Output list of dicts as table."""
    if not data:
        return
    
    table = Table(title=title)
    for key in data[0].keys():
        table.add_column(str(key))
    
    for row in data:
        table.add_row(*[str(v) for v in row.values()])
    
    console.print(table)
```

---

## Part 6: Comparison Matrix

### Feature Comparison

| Feature | argparse | typer | cyclopts | fire | click |
|---------|----------|-------|----------|------|-------|
| Type Hints → Args | ❌ | ✅ | ✅ | ❌ | ❌ |
| Auto Completion | ❌ | ✅ | ✅ | ❌ | ✅ |
| Rich Integration | ❌ | ✅ | ⚠️ | ❌ | ⚠️ |
| Zero Config | ⚠️ | ✅ | ✅ | ✅ | ❌ |
| Async Support | ❌ | ⚠️ | ⚠️ | ❌ | ⚠️ |
| Dependencies | 0 | 2 | 1 | 1 | 1 |
| Agentic Safe | ✅ | ✅ | ✅ | ✅ | ✅ |

### Interactive Library Comparison

| Feature | InquirerPy | questionary | prompt-toolkit |
|---------|------------|-------------|----------------|
| Fuzzy Search | ✅ | ❌ | ⚠️ |
| Async | ✅ | ❌ | ✅ |
| Customization | High | Medium | Very High |
| TTY Required | ✅ | ✅ | ✅ |
| Agentic Safe | ❌ Wrapper | ❌ Wrapper | ❌ Wrapper |

### Output Library Comparison

| Feature | rich | Textual | colorama |
|---------|------|---------|----------|
| Tables | ✅ | ✅ | ❌ |
| Progress | ✅ | ✅ | ❌ |
| Widgets | ⚠️ | ✅ | ❌ |
| Headless | ✅ Auto | ✅ Native | ✅ |
| Weight | Medium | Heavy | Light |

---

## Part 7: Decision Matrix for gemini-cli-prompt-library

### Current State
- Using: `argparse` in `dspy_helm/cli.py`
- Needs: Interactive workflows, beautiful output, agentic compatibility

### Recommended Migration Path

1. **Phase 1**: Add typer + rich alongside argparse
2. **Phase 2**: Migrate commands incrementally
3. **Phase 3**: Add InquirerPy with wrappers for guided workflows
4. **Phase 4**: Remove argparse dependency

### Technical Constraints (TC-001)

| Constraint | Implementation |
|------------|----------------|
| typer for CLI structure | `typer.Typer()` as main app |
| InquirerPy for prompts | With `is_agentic()` fallbacks |
| JSON output mode | `--json` / `--format json` flag |
| Headless safe | All interactive prompts wrapped |
| State persistence | Workflow context manager |

---

## Part 8: Testing Strategies

### Unit Testing CLI Commands

```python
from typer.testing import CliRunner
from myapp.cli import app

runner = CliRunner()

def test_evaluate_json_output():
    result = runner.invoke(app, ["evaluate", "security_review", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert "score" in data

def test_list_scenarios():
    result = runner.invoke(app, ["list-scenarios", "--format", "json"])
    assert result.exit_code == 0
    scenarios = json.loads(result.stdout)
    assert "security_review" in scenarios
```

### Testing Agentic Mode

```python
import os
from myapp.utils.agentic import is_agentic

def test_is_agentic_with_env(monkeypatch):
    monkeypatch.setenv("AGENT_MODE", "1")
    assert is_agentic() == True

def test_is_agentic_ci(monkeypatch):
    monkeypatch.setenv("CI", "true")
    assert is_agentic() == True
```

---

## References

- [Typer Documentation](https://typer.tiangolo.com/)
- [Cyclopts Documentation](https://cyclopts.readthedocs.io/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Textual Documentation](https://textual.textualize.io/)
- [InquirerPy Documentation](https://inquirerpy.readthedocs.io/)
- Cass Session: `session-2026-01-13T10-46` (CLI framework decision)
- Feature 004 Spec: `/specs/004-guided-workflow/spec.md`
